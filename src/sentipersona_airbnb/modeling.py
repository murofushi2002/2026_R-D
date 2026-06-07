from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer, RobertaTokenizer, get_linear_schedule_with_warmup

from .config import cfg_get, standard_files, standard_paths
from .evaluation import sgts_score
from .utils import seed_everything, write_json

LABEL_TO_ID = {"negative": 0, "positive": 1}
ID_TO_LABEL = {value: key for key, value in LABEL_TO_ID.items()}


class TextLabelDataset(Dataset):
    def __init__(self, texts: list[str], labels: list[int]) -> None:
        self.texts = texts
        self.labels = labels

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        return {"text": self.texts[idx], "label": self.labels[idx]}


class SentimentEncoder(nn.Module):
    def __init__(self, model_name_or_path: str) -> None:
        super().__init__()
        model_ref = str(model_name_or_path)
        if model_ref == "roberta-base" or "roberta" in model_ref.lower():
            self.tokenizer = RobertaTokenizer.from_pretrained(model_name_or_path)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False)
        self.encoder = AutoModel.from_pretrained(model_name_or_path)

    def mean_pool(
        self,
        last_hidden_state: torch.Tensor,
        attention_mask: torch.Tensor,
    ) -> torch.Tensor:
        mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        summed = torch.sum(last_hidden_state * mask, dim=1)
        counts = torch.clamp(mask.sum(dim=1), min=1e-9)
        return summed / counts

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        return self.mean_pool(outputs.last_hidden_state, attention_mask)

    def save_pretrained(self, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        self.encoder.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)


def supervised_contrastive_loss(
    embeddings: torch.Tensor,
    labels: torch.Tensor,
    temperature: float = 0.07,
) -> torch.Tensor:
    embeddings = F.normalize(embeddings, dim=1)
    logits = torch.matmul(embeddings, embeddings.T) / temperature
    labels = labels.contiguous().view(-1, 1)
    mask = torch.eq(labels, labels.T).float().to(embeddings.device)

    logits_mask = torch.ones_like(mask) - torch.eye(mask.shape[0], device=embeddings.device)
    mask = mask * logits_mask

    logits_max, _ = torch.max(logits, dim=1, keepdim=True)
    logits = logits - logits_max.detach()
    exp_logits = torch.exp(logits) * logits_mask
    log_prob = logits - torch.log(exp_logits.sum(dim=1, keepdim=True) + 1e-12)
    mean_log_prob_pos = (mask * log_prob).sum(dim=1) / mask.sum(dim=1).clamp(min=1.0)
    loss = -mean_log_prob_pos
    return loss.mean()


def collate_batch(tokenizer, max_length: int):
    def _collate(items: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
        texts = [item["text"] for item in items]
        labels = torch.tensor([item["label"] for item in items], dtype=torch.long)
        encoded = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        encoded["labels"] = labels
        return encoded

    return _collate


def make_balanced_sampler(labels: list[int]) -> WeightedRandomSampler:
    label_counts = pd.Series(labels).value_counts().to_dict()
    weights = [1.0 / label_counts[label] for label in labels]
    return WeightedRandomSampler(weights, num_samples=len(weights), replacement=True)


def prepare_teacher_dataframe(path: Path, max_samples: int | None = None) -> pd.DataFrame:
    df = pd.read_parquet(path)
    if "label_id" not in df.columns:
        df = df[df["sentiment"].isin(LABEL_TO_ID)].copy()
        df["label_id"] = df["sentiment"].map(LABEL_TO_ID).astype(int)
    else:
        df = df[df["label_id"].isin([0, 1])].copy()
        df["label_id"] = df["label_id"].astype(int)
        if "sentiment" not in df.columns:
            df["sentiment"] = df["label_id"].map(ID_TO_LABEL)
    if max_samples:
        per_class = max(1, max_samples // max(1, df["label_id"].nunique()))
        df = _sample_per_group(df, "label_id", per_class)
    return df


def _sample_per_group(
    df: pd.DataFrame,
    group_col: str,
    max_per_group: int,
    seed: int = 42,
) -> pd.DataFrame:
    sampled = [
        frame.sample(min(len(frame), max_per_group), random_state=seed)
        for _, frame in df.groupby(group_col, sort=False)
    ]
    return pd.concat(sampled, ignore_index=True)


@torch.no_grad()
def encode_texts(
    model_dir_or_name: str | Path,
    texts: list[str],
    batch_size: int = 64,
    max_length: int = 256,
    normalize: bool = True,
    device: str | None = None,
) -> np.ndarray:
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    model = SentimentEncoder(str(model_dir_or_name)).to(device)
    model.eval()
    embeddings = []
    for start in tqdm(range(0, len(texts), batch_size), desc="encoding"):
        batch_texts = texts[start : start + batch_size]
        encoded = model.tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        ).to(device)
        batch = model(encoded["input_ids"], encoded["attention_mask"])
        if normalize:
            batch = F.normalize(batch, dim=1)
        embeddings.append(batch.cpu().numpy())
    if not embeddings:
        return np.empty((0, 0), dtype=np.float32)
    return np.vstack(embeddings).astype(np.float32)


def train_senticse(cfg: dict, teacher_path: Path | None = None) -> dict[str, Any]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    seed_everything(int(cfg_get(cfg, "experiment.seed")))

    teacher_path = teacher_path or files["teacher_reviews"]
    df = prepare_teacher_dataframe(teacher_path, cfg_get(cfg, "training.max_train_samples"))
    train_df, eval_df = train_test_split(
        df,
        test_size=0.10,
        random_state=int(cfg_get(cfg, "experiment.seed")),
        stratify=df["label_id"],
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentimentEncoder(cfg_get(cfg, "training.base_model")).to(device)
    max_length = int(cfg_get(cfg, "training.max_length"))
    batch_size = int(cfg_get(cfg, "training.batch_size"))
    train_dataset = TextLabelDataset(train_df["text"].tolist(), train_df["label_id"].tolist())
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=make_balanced_sampler(train_df["label_id"].tolist()),
        collate_fn=collate_batch(model.tokenizer, max_length),
        drop_last=True,
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(cfg_get(cfg, "training.learning_rate")),
    )
    epochs = int(cfg_get(cfg, "training.epochs"))
    total_steps = max(1, len(train_loader) * epochs)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=max(1, total_steps // 20),
        num_training_steps=total_steps,
    )
    scaler = torch.cuda.amp.GradScaler(
        enabled=bool(cfg_get(cfg, "training.mixed_precision")) and device == "cuda"
    )

    metrics: list[dict[str, Any]] = []
    temperature = float(cfg_get(cfg, "training.temperature"))
    for epoch in range(epochs):
        model.train()
        losses = []
        for batch in tqdm(train_loader, desc=f"train epoch {epoch + 1}/{epochs}"):
            labels = batch.pop("labels").to(device)
            batch = {key: value.to(device) for key, value in batch.items()}
            optimizer.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=scaler.is_enabled()):
                embeddings = model(batch["input_ids"], batch["attention_mask"])
                loss = supervised_contrastive_loss(embeddings, labels, temperature)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()
            losses.append(float(loss.detach().cpu()))

        eval_metrics = evaluate_sgts_on_dataframe(
            model,
            eval_df,
            batch_size=int(cfg_get(cfg, "embedding.batch_size")),
            max_length=max_length,
            normalize=bool(cfg_get(cfg, "embedding.normalize")),
            device=device,
            samples_per_class=int(cfg_get(cfg, "training.eval_samples_per_class")),
        )
        eval_metrics["epoch"] = epoch + 1
        eval_metrics["train_loss"] = float(np.mean(losses)) if losses else float("nan")
        metrics.append(eval_metrics)

    output_dir = paths["senticse_model_dir"]
    model.save_pretrained(output_dir)
    write_json(
        {
            "model_dir": str(output_dir),
            "base_model": cfg_get(cfg, "training.base_model"),
            "device": device,
            "teacher_rows": int(len(df)),
            "train_rows": int(len(train_df)),
            "eval_rows": int(len(eval_df)),
            "metrics": metrics,
        },
        paths["reports_dir"] / "senticse_training_metrics.json",
    )
    return {"model_dir": str(output_dir), "metrics": metrics}


@torch.no_grad()
def evaluate_sgts_on_dataframe(
    model: SentimentEncoder,
    df: pd.DataFrame,
    batch_size: int,
    max_length: int,
    normalize: bool,
    device: str,
    samples_per_class: int,
) -> dict[str, float]:
    sampled = _sample_per_group(df, "sentiment", samples_per_class)
    model.eval()
    texts = sampled["text"].tolist()
    embeddings = []
    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start : start + batch_size]
        encoded = model.tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        ).to(device)
        batch = model(encoded["input_ids"], encoded["attention_mask"])
        if normalize:
            batch = F.normalize(batch, dim=1)
        embeddings.append(batch.cpu().numpy())
    embeddings_np = np.vstack(embeddings) if embeddings else np.empty((0, 0))
    return sgts_score(embeddings_np, sampled["sentiment"].tolist())


def _sample_labeled_dataframe(df: pd.DataFrame, max_samples_per_class: int | None) -> pd.DataFrame:
    if max_samples_per_class:
        return _sample_per_group(df, "label_id", max_samples_per_class)
    return df.reset_index(drop=True)


def _embedding_separation_metrics(embeddings: np.ndarray, df: pd.DataFrame) -> dict[str, Any]:
    from sklearn.metrics import silhouette_score

    labels = df["label_id"].astype(int).to_numpy()
    sentiments = df["sentiment"].tolist()
    result: dict[str, Any] = {
        "n": int(len(df)),
        "label_counts": df["sentiment"].value_counts().to_dict(),
        **sgts_score(embeddings, sentiments),
    }
    unique_labels = sorted(set(labels.tolist()))
    if len(unique_labels) == 2 and min((labels == label).sum() for label in unique_labels) > 1:
        result["silhouette_cosine"] = float(silhouette_score(embeddings, labels, metric="cosine"))
        neg_centroid = embeddings[labels == 0].mean(axis=0)
        pos_centroid = embeddings[labels == 1].mean(axis=0)
        denom = max(float(np.linalg.norm(neg_centroid) * np.linalg.norm(pos_centroid)), 1e-12)
        centroid_cosine = float(np.dot(neg_centroid, pos_centroid) / denom)
        result["centroid_cosine"] = centroid_cosine
        result["centroid_cosine_distance"] = 1.0 - centroid_cosine
    else:
        result["silhouette_cosine"] = None
        result["centroid_cosine"] = None
        result["centroid_cosine_distance"] = None
    return result


def evaluate_sentiment_encoder(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    eval_path = files["sentiment_eval_reviews"]
    df = prepare_teacher_dataframe(eval_path)
    df = _sample_labeled_dataframe(
        df,
        cfg_get(cfg, "model_evaluation.max_samples_per_class"),
    )
    texts = df["text"].tolist()
    batch_size = int(cfg_get(cfg, "embedding.batch_size"))
    max_length = int(cfg_get(cfg, "training.max_length"))
    normalize = bool(cfg_get(cfg, "embedding.normalize"))

    base_model = cfg_get(cfg, "training.base_model")
    base_embeddings = encode_texts(
        base_model,
        texts,
        batch_size=batch_size,
        max_length=max_length,
        normalize=normalize,
    )
    base_metrics = _embedding_separation_metrics(base_embeddings, df)

    finetuned_model = paths["senticse_model_dir"]
    report: dict[str, Any] = {
        "eval_reviews": str(eval_path),
        "sampled_rows": int(len(df)),
        "base_model": str(base_model),
        "base": base_metrics,
    }
    if finetuned_model.exists():
        tuned_embeddings = encode_texts(
            finetuned_model,
            texts,
            batch_size=batch_size,
            max_length=max_length,
            normalize=normalize,
        )
        tuned_metrics = _embedding_separation_metrics(tuned_embeddings, df)
        report["fine_tuned_model"] = str(finetuned_model)
        report["fine_tuned"] = tuned_metrics
        report["improvement"] = {
            "sgts_delta": tuned_metrics["sgts_delta"] - base_metrics["sgts_delta"],
            "silhouette_cosine": (
                tuned_metrics["silhouette_cosine"] - base_metrics["silhouette_cosine"]
                if tuned_metrics["silhouette_cosine"] is not None
                and base_metrics["silhouette_cosine"] is not None
                else None
            ),
            "centroid_cosine_distance": (
                tuned_metrics["centroid_cosine_distance"]
                - base_metrics["centroid_cosine_distance"]
                if tuned_metrics["centroid_cosine_distance"] is not None
                and base_metrics["centroid_cosine_distance"] is not None
                else None
            ),
        }
    else:
        report["fine_tuned_model"] = str(finetuned_model)
        report["fine_tuned"] = None
        report["improvement"] = None
        report["warning"] = "Fine-tuned model directory does not exist."

    output = paths["reports_dir"] / "sentiment_embedding_eval.json"
    write_json(report, output)
    return {"sentiment_embedding_eval": str(output)}


def encode_airbnb_reviews(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    reviews_path = files["airbnb_reviews_all"]
    reviews = pd.read_parquet(reviews_path)
    model_dir = paths["senticse_model_dir"]
    if not model_dir.exists():
        model_dir = Path(cfg_get(cfg, "training.base_model"))
    embeddings = encode_texts(
        model_dir,
        reviews["comments_clean"].tolist(),
        batch_size=int(cfg_get(cfg, "embedding.batch_size")),
        max_length=int(cfg_get(cfg, "training.max_length")),
        normalize=bool(cfg_get(cfg, "embedding.normalize")),
    )
    output = files["airbnb_review_embeddings"]
    np.save(output, embeddings)
    write_json(
        {
            "rows": int(len(reviews)),
            "embedding_shape": list(embeddings.shape),
            "model": str(model_dir),
        },
        paths["reports_dir"] / "embedding_manifest.json",
    )
    return {"embeddings": str(output), "reviews": str(reviews_path)}
