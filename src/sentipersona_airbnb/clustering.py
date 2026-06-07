from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import davies_bouldin_score, silhouette_score

from .config import cfg_get, standard_files, standard_paths
from .utils import write_json


def reduce_embeddings(cfg: dict, embeddings: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    import umap

    seed = int(cfg_get(cfg, "experiment.seed"))
    n_neighbors = int(cfg_get(cfg, "clustering.n_neighbors"))
    deterministic = bool(cfg_get(cfg, "clustering.deterministic_umap"))
    random_state = seed if deterministic else None
    n_jobs = 1 if deterministic else int(cfg_get(cfg, "clustering.n_jobs", -1))
    cluster_dim = min(int(cfg_get(cfg, "clustering.n_components_cluster")), len(embeddings) - 2)
    vis_dim = int(cfg_get(cfg, "clustering.n_components_vis"))
    cluster_dim = max(2, cluster_dim)

    reducer_cluster = umap.UMAP(
        n_components=cluster_dim,
        n_neighbors=min(n_neighbors, max(2, len(embeddings) - 1)),
        min_dist=float(cfg_get(cfg, "clustering.min_dist_cluster")),
        metric="cosine",
        random_state=random_state,
        n_jobs=n_jobs,
    )
    reduced_cluster = reducer_cluster.fit_transform(embeddings)
    if bool(cfg_get(cfg, "clustering.fit_separate_visual_umap")):
        reducer_vis = umap.UMAP(
            n_components=vis_dim,
            n_neighbors=min(n_neighbors, max(2, len(embeddings) - 1)),
            min_dist=float(cfg_get(cfg, "clustering.min_dist_vis")),
            metric="cosine",
            random_state=random_state,
            n_jobs=n_jobs,
        )
        reduced_vis = reducer_vis.fit_transform(embeddings)
    else:
        reduced_vis = reduced_cluster[:, :vis_dim]
    return reduced_cluster, reduced_vis


def cluster_reduced_embeddings(cfg: dict, reduced: np.ndarray):
    import hdbscan

    min_cluster_size = max(
        5,
        int(len(reduced) * float(cfg_get(cfg, "clustering.min_cluster_size_ratio"))),
    )
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=int(cfg_get(cfg, "clustering.min_samples")),
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )
    labels = clusterer.fit_predict(reduced)
    probabilities = getattr(clusterer, "probabilities_", np.ones(len(labels)))
    return labels.astype(int), probabilities.astype(np.float32), clusterer


def evaluate_clustering(
    reduced: np.ndarray,
    labels: np.ndarray,
    sample_size: int | None = None,
    seed: int = 42,
) -> dict[str, Any]:
    valid = labels != -1
    n_clusters = len(set(labels[valid]))
    result = {
        "n": int(len(labels)),
        "n_clusters": int(n_clusters),
        "noise_ratio": float((~valid).mean()) if len(labels) else 0.0,
    }
    if valid.sum() > n_clusters and n_clusters >= 2:
        reduced_valid = reduced[valid]
        labels_valid = labels[valid]
        if sample_size and len(labels_valid) > sample_size:
            rng = np.random.default_rng(seed)
            idx = rng.choice(len(labels_valid), size=sample_size, replace=False)
            reduced_for_silhouette = reduced_valid[idx]
            labels_for_silhouette = labels_valid[idx]
        else:
            reduced_for_silhouette = reduced_valid
            labels_for_silhouette = labels_valid
        result["metric_sample_size"] = int(len(labels_for_silhouette))
        result["silhouette"] = float(
            silhouette_score(reduced_for_silhouette, labels_for_silhouette)
        )
        result["davies_bouldin"] = float(davies_bouldin_score(reduced_valid, labels_valid))
    else:
        result["metric_sample_size"] = 0
        result["silhouette"] = None
        result["davies_bouldin"] = None
    return result


def sample_representative_reviews(
    reviews: pd.DataFrame,
    reduced: np.ndarray,
    labels: np.ndarray,
    n_samples: int,
) -> dict[str, list[dict[str, Any]]]:
    samples: dict[str, list[dict[str, Any]]] = {}
    for label in sorted(set(labels)):
        if label == -1:
            continue
        idx = np.where(labels == label)[0]
        centroid = reduced[idx].mean(axis=0)
        distances = np.linalg.norm(reduced[idx] - centroid, axis=1)
        chosen = idx[np.argsort(distances)[:n_samples]]
        records = []
        for row_idx in chosen:
            row = reviews.iloc[int(row_idx)]
            records.append(
                {
                    "review_id": str(row.get("id", "")),
                    "listing_id": str(row.get("listing_id", "")),
                    "date": str(row.get("date", "")),
                    "text": row["comments_clean"],
                }
            )
        samples[str(int(label))] = records
    return samples


def run_regional_clustering(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    reviews_path = files["airbnb_reviews_all"]
    embeddings_path = files["airbnb_review_embeddings"]
    reviews = pd.read_parquet(reviews_path)
    embeddings = np.load(embeddings_path)
    if len(reviews) != len(embeddings):
        raise ValueError(
            f"Review rows ({len(reviews)}) and embeddings ({len(embeddings)}) do not match."
        )

    reduced_cluster, reduced_vis = reduce_embeddings(cfg, embeddings)
    labels, probabilities, _clusterer = cluster_reduced_embeddings(cfg, reduced_cluster)
    metrics = evaluate_clustering(
        reduced_cluster,
        labels,
        cfg_get(cfg, "clustering.metric_sample_size"),
        int(cfg_get(cfg, "experiment.seed")),
    )
    samples = sample_representative_reviews(
        reviews,
        reduced_cluster,
        labels,
        int(cfg_get(cfg, "clustering.representative_reviews_per_cluster")),
    )

    labels_path = files["regional_cluster_labels"]
    probabilities_path = files["regional_cluster_probabilities"]
    cluster_emb_path = paths["processed_dir"] / "regional_umap_cluster.npy"
    vis_path = paths["processed_dir"] / "regional_umap_vis.npy"
    np.save(labels_path, labels)
    np.save(probabilities_path, probabilities)
    np.save(cluster_emb_path, reduced_cluster.astype(np.float32))
    np.save(vis_path, reduced_vis.astype(np.float32))
    write_json(metrics, paths["reports_dir"] / "regional_clustering_metrics.json")
    write_json(samples, paths["reports_dir"] / "regional_cluster_samples.json")
    return {
        "labels": str(labels_path),
        "probabilities": str(probabilities_path),
        "cluster_embedding": str(cluster_emb_path),
        "visual_embedding": str(vis_path),
        "samples": str(paths["reports_dir"] / "regional_cluster_samples.json"),
    }
