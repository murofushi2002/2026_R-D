# 研究開発技術資料
# 感情Contrastive Embedding × ペルソナ生成 × 宿泊稼働率関係分析

> 作成日: 2026年6月3日  
> バージョン: v1.0  
> 研究名称（仮）: **SentiPersona-Airbnb**: Sentiment-Contrastive Guest Persona Discovery and Occupancy Analysis  
> データセット: Inside Airbnb（最新3か月分を標準実験窓とする）  
> 実行環境方針: OSS BERTモデル + ローカルLLM完結

---

## 1. 研究概要

### 1.1 コアパイプライン

```
Inside Airbnb reviews（英語口コミ）
        │
        ▼
[Step 1] 前処理・クリーニング
        │
        ▼
[Step 2] 感情Contrastive BERT Fine-tune（SentiCSE方式）
         Airbnb口コミにOSS感情分類モデルを適用し、positive/negative疑似ラベルを付与
         高信頼サンプルのみを採用し、positive=1 / negative=0 の2値で追加学習
         同極性ペアを正例、異極性ペアを負例として
         感情極性軸でembedding空間を整形
         → Fine-tune済みモデルで全Airbnb口コミをembedding化
        │
        ▼
[Step 3] Contrastive Embeddingによるクラスタリング
         UMAP次元削減 → HDBSCAN
         地域全体 と 施設個別 の2スケールで実施
        │
        ▼
[Step 4] ローカルLLMによるペルソナ命名・記述生成
         各クラスタの代表口コミ → Qwen3 4B（ローカル）
         → ペルソナ名・特徴・重視軸を出力
        │
        ▼
[Step 5] 月次ペルソナ構成比率の時系列化
         口コミ投稿日 → 月次ペルソナ比率ベクトル
        │
        ▼
[Step 6] 稼働率代理指標との関係分析
         availability_365の逆数 → 推定稼働率
         Granger因果性・重回帰・XGBoost
```

### 1.2 研究目的

1. **地域ペルソナ発見**: 特定都市・地域のAirbnb全口コミから、感情軸で整形されたembedding空間によりデータドリブンにゲストペルソナを発見する
2. **施設ペルソナ発見**: 個別施設の口コミから施設固有のペルソナを構築し、地域ペルソナとのギャップを分析する
3. **稼働率との関係解明**: ペルソナ構成比率の時系列変化と施設稼働率（代理指標）の統計的因果関係を実証する

### 1.3 先行研究との差分（新規性）

| 先行研究 | 何をしているか | 本研究との差分 |
|---------|--------------|--------------|
| SentiCSE (Kim+2024) | 感情Contrastive embeddingの構築 | ペルソナ生成・稼働率分析への応用がない |
| Proxona (Choi+2025) | 意味的SBERTでペルソナ生成 | 感情軸での空間整形をしていない |
| Shin+2024 (CHI) | LLM-summarizingペルソナ生成 | 宿泊業・稼働率との結合がない |
| Amin+2026 (Scoping Review) | 「外部変数結合が課題」と指摘 | 本研究がその空白を埋める |

---

## 2. データセット仕様

### 2.1 Inside Airbnb — 使用ファイルと主要カラム

**URL**: https://insideairbnb.com/get-the-data/  
**ライセンス**: CC0 1.0（パブリックドメイン）/ CC BY 4.0  
**対象都市（暫定）**: 東京（Tokyo）、大阪（Osaka）、または英語口コミが豊富な都市

> 日本語口コミ対応モデルを使う場合は東京・大阪を対象とする。英語モデルで実施する場合はLondon・NYC等も候補。

#### 使用ファイル

| ファイル | 使用目的 | 主要カラム |
|--------|---------|-----------|
| `reviews.csv.gz` | 口コミテキスト・投稿日 | `listing_id`, `date`, `reviewer_id`, `comments` |
| `listings.csv.gz` | 施設情報・稼働率代理指標 | `id`, `neighbourhood_cleansed`, `room_type`, `price`, `availability_365`, `number_of_reviews_ltm`, `review_scores_*` |
| `calendar.csv.gz` | 日次空き状況（稼働率詳細計算用） | `listing_id`, `date`, `available`, `price` |

### 2.2 Airbnb内疑似ラベル — SentiCSE Fine-tune用教師データ

外部口コミデータセットは使わず、Inside Airbnb の `reviews.csv.gz` から fine-tune 用データを構築する。
追加学習では `data.finetune_review_window_months: 3` により、レビュー投稿日ベースで最新3か月のカレンダー月だけを teacher data として採用する。本番の embedding、clustering、persona、評価は前処理済みの全Airbnb口コミで行う。

**入力**: `comments_clean`（前処理・言語フィルタ後のAirbnb口コミ）  
**ラベル生成**: OSS感情分類モデルによる per-review binary sentiment  
**ラベル定義**: `positive=1`, `negative=0`  
**採用基準**: confidence が閾値以上（例: `0.95`）の高信頼サンプルのみ  

> これにより、ホテル系外部データからAirbnbへのドメインシフトを避ける。ラベルは疑似ラベルであるため、低信頼サンプルを除外し、positive/negative のクラスバランスを揃えたうえで supervised contrastive fine-tune を行う。

| カラム | 内容 |
|--------|------|
| `text` | Airbnb口コミ本文（cleaned comments） |
| `sentiment` | `positive` / `negative` |
| `label_id` | `positive=1`, `negative=0` |
| `sentiment_score` | 感情分類モデルの confidence |

#### 稼働率の計算（calendarから直接計算）

Inside Airbnbには実稼働率データは存在しない。`calendar.csv.gz` の `available` カラム（`'t'`=空き, `'f'`=予約済み）から直接計算する：

```python
# available == 'f'（予約済み）の比率を稼働率とする
occ_from_calendar = (
    calendar.groupby('listing_id')['available']
    .apply(lambda x: (x == 'f').sum() / len(x))
    .reset_index(name='occupancy_rate')
)
```

#### 月次データへの変換

```python
# reviews.csv の date カラムから月次ペルソナ構成比率を集計
reviews['year_month'] = pd.to_datetime(reviews['date']).dt.to_period('M')

# calendar.csv から月次稼働率を計算
calendar['year_month'] = pd.to_datetime(calendar['date']).dt.to_period('M')
monthly_occ = (
    calendar.groupby(['listing_id', 'year_month'])['available']
    .apply(lambda x: (x == 'f').mean())
    .reset_index(name='occupancy_rate')
)
```

### 2.2 データ規模の見通し

| 項目 | 東京の場合 | 備考 |
|------|----------|------|
| listings数 | 約10,000〜15,000件 | Inside Airbnb スナップショット |
| reviews数（本番） | 都市・時期に依存。全履歴レビューを想定 | `airbnb_reviews_clean_all.parquet` |
| reviews数（fine-tune） | 都市・時期に依存。最新3か月の数万件規模を想定 | `finetune_review_window_months: 3` で制御 |
| calendar行数 | 約300万行 | listings数 × 365日 |
| embedding対象 | reviews.comments（非空） | 平均150〜300単語/件 |

---

## 3. Step 2 詳細：感情Contrastive BERT Fine-tune

### 3.1 使用モデル（OSS限定）

#### 英語テキスト対象の場合

| モデル | HuggingFace ID | パラメータ数 | 特徴 |
|--------|---------------|-----------|------|
| **roberta-base** | `roberta-base` | 125M | 英語BERT系、MLMのみ事前学習、推奨 |
| bert-base-uncased | `bert-base-uncased` | 110M | 標準BERT |
| all-MiniLM-L6-v2 | `sentence-transformers/all-MiniLM-L6-v2` | 22M | 高速・軽量（SBERTベース） |

#### 日本語テキスト対象の場合（東京・大阪の日本語口コミ）

| モデル | HuggingFace ID | パラメータ数 | 特徴 |
|--------|---------------|-----------|------|
| **bert-base-japanese-v3** | `cl-tohoku/bert-base-japanese-v3` | 110M | 日本語最標準・推奨 |
| bert-large-japanese-v2 | `cl-tohoku/bert-large-japanese-v2` | 337M | 高精度・高メモリ要求 |
| multilingual-e5-small | `intfloat/multilingual-e5-small` | 118M | 多言語対応・英日両対応 |

> **推奨構成（バランス型）**: `intfloat/multilingual-e5-small` or `cl-tohoku/bert-base-japanese-v3`  
> 英語主体で進める場合: `roberta-base`

---

### 3.2 SentiCSE方式Fine-tune — 実装詳細

#### 3.2.1 教師データの構築（Airbnb疑似ラベル）

SentiCSEのFine-tuneにはper-reviewの感情ラベルが必要。外部データは使わず、Airbnb口コミにOSS感情分類モデルを適用し、高信頼なpositive/negativeだけを教師データ化する。

```python
import pandas as pd
from transformers import pipeline

reviews = pd.read_parquet('data/processed/airbnb_reviews_finetune_window.parquet')

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    max_length=256,
)

predictions = classifier(reviews["comments_clean"].tolist(), batch_size=64)

def to_binary_label(pred):
    label = pred["label"].lower()
    if label == "positive":
        return 1
    if label == "negative":
        return 0
    return None

reviews["label_id"] = [to_binary_label(p) for p in predictions]
reviews["sentiment_score"] = [p["score"] for p in predictions]

train_df = (
    reviews
    .dropna(subset=["label_id"])
    .query("sentiment_score >= 0.95")
    [["comments_clean", "label_id", "sentiment_score"]]
    .rename(columns={"comments_clean": "text"})
)
```

> 疑似ラベルはノイズを含むため、confidence閾値、重複除去、positive/negativeのバランスサンプリングを必須とする。中立・曖昧サンプルはfine-tuneには使わず、後段のembedding対象には残す。

#### 3.2.2 Contrastiveペアの生成

```python
import random
from itertools import combinations

def build_contrastive_pairs(df: pd.DataFrame, n_pairs: int = 10000):
    """感情ラベルを基準に正例・負例ペアを生成"""
    pos_pairs = []   # 同極性ペア
    neg_pairs = []   # 異極性ペア

    by_sentiment = df.groupby('label_id')['text'].apply(list).to_dict()

    sentiments = list(by_sentiment.keys())

    for _ in range(n_pairs):
        # 正例: ランダムに同極性2件
        s = random.choice(sentiments)
        a, b = random.sample(by_sentiment[s], 2)
        pos_pairs.append((a, b, 1))  # label=1: 正例

        # 負例: ランダムに異極性2件
        s1, s2 = random.sample([x for x in sentiments if x != s], 1)[0], s
        c = random.choice(by_sentiment[s1])
        neg_pairs.append((a, c, 0))  # label=0: 負例

    return pos_pairs + neg_pairs
```

#### 3.2.3 SentiCSE損失関数とFine-tune

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

class SentiCSEModel(nn.Module):
    def __init__(self, model_name: str = "roberta-base"):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def encode(self, texts: list[str], device: str = "cuda") -> torch.Tensor:
        inputs = self.tokenizer(
            texts, padding=True, truncation=True,
            max_length=256, return_tensors="pt"
        ).to(device)
        outputs = self.encoder(**inputs)
        # Mean pooling（CLSよりも安定）
        attention_mask = inputs['attention_mask']
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / \
               torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def supcon_loss(self, embeddings: torch.Tensor,
                    labels: torch.Tensor, temperature: float = 0.07) -> torch.Tensor:
        """Supervised Contrastive Loss（Khosla+2020）"""
        embeddings = F.normalize(embeddings, dim=1)
        sim_matrix = torch.matmul(embeddings, embeddings.T) / temperature

        # 自己類似度を除外
        n = embeddings.size(0)
        mask_self = ~torch.eye(n, dtype=torch.bool, device=embeddings.device)

        # 同ラベルマスク（正例）
        labels = labels.unsqueeze(1)
        mask_pos = (labels == labels.T) & mask_self

        # 損失計算
        exp_sim = torch.exp(sim_matrix) * mask_self
        log_prob = sim_matrix - torch.log(exp_sim.sum(dim=1, keepdim=True) + 1e-9)
        loss = -(log_prob * mask_pos).sum(dim=1) / mask_pos.sum(dim=1).clamp(min=1)
        return loss.mean()
```

#### 3.2.4 Fine-tuneの学習設定

```python
# 学習設定（推奨）
TRAINING_CONFIG = {
    "model_name": "roberta-base",          # 英語の場合
    # "model_name": "cl-tohoku/bert-base-japanese-v3",  # 日本語の場合
    "batch_size": 64,
    "learning_rate": 2e-5,
    "epochs": 5,
    "temperature": 0.07,
    "max_length": 256,
    "n_contrastive_pairs": 100_000,
    "save_path": "./checkpoints/senticse_airbnb/",
    "device": "cuda",
}

# 推定VRAM使用量:
#   roberta-base (125M) + batch_size=64 + max_length=256 ≒ 8GB VRAM
#   メモリ不足時: batch_size=32 に落とすか gradient_checkpointing=True
```

---

## 4. Step 3 詳細：クラスタリング（地域・施設2スケール）

### 4.1 次元削減

```python
import umap

def reduce_dimensions(embeddings: np.ndarray,
                      n_components_vis: int = 2,
                      n_components_cluster: int = 50) -> tuple:
    """クラスタリング用（50次元）と可視化用（2次元）を両方生成"""

    # クラスタリング用（高次元）
    reducer_cluster = umap.UMAP(
        n_components=n_components_cluster,
        n_neighbors=15,
        min_dist=0.0,         # クラスタリング用はmin_dist=0が良い
        metric='cosine',
        random_state=42
    )
    emb_cluster = reducer_cluster.fit_transform(embeddings)

    # 可視化用（2次元）
    reducer_vis = umap.UMAP(
        n_components=n_components_vis,
        n_neighbors=15,
        min_dist=0.1,
        metric='cosine',
        random_state=42
    )
    emb_vis = reducer_vis.fit_transform(embeddings)

    return emb_cluster, emb_vis
```

### 4.2 HDBSCANクラスタリング

```python
import hdbscan

def cluster_embeddings(emb_cluster: np.ndarray,
                       min_cluster_size_ratio: float = 0.02) -> np.ndarray:
    """HDBSCAN: クラスタ数自動決定・ノイズ点分離"""

    min_cluster_size = max(10, int(len(emb_cluster) * min_cluster_size_ratio))

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=5,
        metric='euclidean',       # UMAP後はeuclid
        cluster_selection_method='eom',  # Excess of Mass（推奨）
        prediction_data=True      # ソフトクラスタリング用
    )
    labels = clusterer.fit_predict(emb_cluster)

    # クラスタ品質レポート
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = (labels == -1).sum()
    print(f"クラスタ数: {n_clusters}, ノイズ点数: {n_noise} ({n_noise/len(labels):.1%})")

    return labels, clusterer
```

### 4.3 2スケール実行

```python
# スケール1: 地域全体（全施設の口コミ）
regional_embeddings = senticse_model.encode(all_reviews['comments'].tolist())
emb_cluster_r, emb_vis_r = reduce_dimensions(regional_embeddings)
labels_regional, clusterer_r = cluster_embeddings(emb_cluster_r, min_cluster_size_ratio=0.02)

# スケール2: 施設個別（listing_idごとにループ）
facility_personas = {}
for listing_id, group in all_reviews.groupby('listing_id'):
    if len(group) < 20:  # 口コミ20件未満はスキップ
        continue
    embs = senticse_model.encode(group['comments'].tolist())
    emb_c, emb_v = reduce_dimensions(embs, n_components_cluster=min(20, len(embs)//2))
    labels_f, _ = cluster_embeddings(emb_c, min_cluster_size_ratio=0.05)
    facility_personas[listing_id] = {
        'labels': labels_f,
        'reviews': group,
        'embeddings': embs
    }
```

### 4.4 クラスタ品質評価

```python
from sklearn.metrics import silhouette_score, davies_bouldin_score

def evaluate_clustering(embeddings: np.ndarray, labels: np.ndarray) -> dict:
    valid = labels != -1  # ノイズ点を除外
    if valid.sum() < 2:
        return {}
    return {
        "silhouette": silhouette_score(embeddings[valid], labels[valid], metric='euclidean'),
        "davies_bouldin": davies_bouldin_score(embeddings[valid], labels[valid]),
        "n_clusters": len(set(labels[valid])),
        "noise_ratio": (~valid).mean()
    }
```

---

## 5. Step 4 詳細：ローカルLLMによるペルソナ命名

### 5.1 使用LLMモデル（ローカル完結）

| モデル | サイズ | VRAM要件 | 推奨用途 |
|--------|--------|---------|---------|
| **Qwen3-4B** | 4B (Q4_K_M) | 約4GB | 速度重視・バッチ処理 |
| Qwen3-8B | 8B (Q4_K_M) | 約6GB | 品質重視 |
| Llama-3.2-3B-Instruct | 3B | 約3GB | 英語テキスト向け |
| gemma-3-4b-it | 4B | 約4GB | 英語テキスト、Google製 |

> **推奨**: 英語口コミ → `Llama-3.2-3B-Instruct`（英語精度が高い）  
> 日本語口コミ → `Qwen3-4B`（日英両対応）

### 5.2 実行環境

```python
# Ollamaを使ったローカルLLM実行（推奨）
# インストール: https://ollama.com/
# モデルpull: ollama pull qwen3:4b

import ollama

def name_persona_cluster(reviews_sample: list[str],
                         model: str = "qwen3:4b") -> dict:
    """クラスタの代表口コミ10件からペルソナを命名"""

    sample_text = "\n".join([f"- {r[:200]}" for r in reviews_sample[:10]])

    prompt = f"""You are a hospitality researcher analyzing guest reviews.
Below are 10 representative Airbnb reviews from one guest cluster.
Analyze these reviews and output a guest persona in JSON format.

Reviews:
{sample_text}

Output JSON with exactly these keys:
{{
  "persona_name": "short name (max 5 words)",
  "purpose": "primary stay purpose (max 20 words)",
  "top_priorities": ["priority1", "priority2", "priority3"],
  "sentiment_tendency": "positive / mixed / negative",
  "price_sensitivity": "low / medium / high",
  "description": "2-3 sentence persona description"
}}"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.0}  # 再現性確保
    )

    import json
    try:
        return json.loads(response['message']['content'])
    except json.JSONDecodeError:
        # JSONパース失敗時のフォールバック
        return {"persona_name": "Unknown", "description": response['message']['content']}
```

### 5.3 代表口コミのサンプリング戦略

```python
def sample_representative_reviews(reviews: list[str],
                                   embeddings: np.ndarray,
                                   n_samples: int = 10) -> list[str]:
    """クラスタ重心に最も近い口コミを選択（プロトタイプ選択）"""
    centroid = embeddings.mean(axis=0)
    distances = np.linalg.norm(embeddings - centroid, axis=1)
    top_indices = np.argsort(distances)[:n_samples]
    return [reviews[i] for i in top_indices]
```

---

## 6. Step 5 詳細：月次ペルソナ構成比率の時系列化

### 6.1 ソフトクラスタリングによる月次比率計算

```python
import hdbscan

def compute_monthly_persona_ratios(
    reviews_df: pd.DataFrame,
    embeddings: np.ndarray,
    clusterer: hdbscan.HDBSCAN,
    regional_reducer  # 学習済みUMAPオブジェクト
) -> pd.DataFrame:
    """月次ペルソナ構成比率の時系列データを生成"""

    # ソフトメンバーシップ（確率ベース）
    soft_clusters = hdbscan.membership_vector(clusterer, embeddings)
    # shape: (n_reviews, n_clusters)

    reviews_df = reviews_df.copy()
    reviews_df['year_month'] = pd.to_datetime(reviews_df['date']).dt.to_period('M')

    K = soft_clusters.shape[1]  # ペルソナ数

    # 月次集計
    monthly_records = []
    for ym, group in reviews_df.groupby('year_month'):
        idx = group.index
        weights = soft_clusters[idx]  # (n_reviews_in_month, K)
        ratio = weights.mean(axis=0)  # (K,) 平均ソフトメンバーシップ
        record = {'year_month': ym}
        for k in range(K):
            record[f'persona_{k}_ratio'] = ratio[k]
        monthly_records.append(record)

    return pd.DataFrame(monthly_records).set_index('year_month')
```

### 6.2 ラグ補正（口コミ投稿日 → 宿泊月への変換）

```python
# Airbnbでは宿泊後7〜14日以内にレビュー投稿が多い
# 保守的に14日（約0.5ヶ月）のラグを仮定

LAG_MONTHS = 1  # 口コミ月 - 1ヶ月 ≒ 宿泊月（感度分析でlag=0,1,2を比較）

def adjust_review_lag(persona_ratio_df: pd.DataFrame, lag: int = 1) -> pd.DataFrame:
    """口コミ月から宿泊月へのラグ補正"""
    df = persona_ratio_df.copy()
    df.index = df.index - lag  # Period演算でlag月ずらす
    return df
```

---

## 7. Step 6 詳細：稼働率との関係分析

### 7.1 データ統合

```python
def build_analysis_dataset(
    monthly_persona_ratios: pd.DataFrame,
    monthly_occupancy: pd.DataFrame,
    listing_id: str = None
) -> pd.DataFrame:
    """ペルソナ比率と稼働率を月次で結合"""

    df = monthly_persona_ratios.join(
        monthly_occupancy.rename(columns={'occupancy_rate': 'occ'}),
        how='inner'
    )

    # 季節ダミー変数を追加
    df['month'] = df.index.month
    for m in range(1, 13):
        df[f'month_{m}'] = (df['month'] == m).astype(int)

    return df.dropna()
```

### 7.2 相関分析

```python
from scipy import stats

def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """各ペルソナ比率と稼働率の相関・ラグ相関を計算"""

    persona_cols = [c for c in df.columns if c.startswith('persona_')]
    results = []

    for col in persona_cols:
        for lag in [0, 1, 2, 3]:
            shifted = df[col].shift(lag)
            valid = ~(shifted.isna() | df['occ'].isna())
            r, p = stats.pearsonr(shifted[valid], df['occ'][valid])
            results.append({
                'persona': col,
                'lag_months': lag,
                'pearson_r': r,
                'p_value': p,
                'significant': p < 0.05
            })

    return pd.DataFrame(results).sort_values('pearson_r', ascending=False)
```

### 7.3 重回帰分析

```python
import statsmodels.api as sm

def regression_analysis(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    """ペルソナ比率 × 季節ダミーで稼働率を回帰"""

    persona_cols = [c for c in df.columns if c.startswith('persona_')]
    month_cols = [f'month_{m}' for m in range(2, 13)]  # month_1を基準に省略

    X = df[persona_cols + month_cols]
    X = sm.add_constant(X)
    y = df['occ']

    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model
```

### 7.4 Granger因果性検定

```python
from statsmodels.tsa.stattools import grangercausalitytests

def granger_causality_test(df: pd.DataFrame, max_lag: int = 3) -> dict:
    """ペルソナ比率 → 稼働率のGranger因果性を検定"""

    persona_cols = [c for c in df.columns if c.startswith('persona_')]
    results = {}

    for col in persona_cols:
        test_data = df[['occ', col]].dropna()
        if len(test_data) < max_lag + 10:
            continue
        try:
            gc_result = grangercausalitytests(test_data, maxlag=max_lag, verbose=False)
            # F検定のp値を取得
            min_p = min(
                gc_result[lag][0]['ssr_ftest'][1]
                for lag in range(1, max_lag + 1)
            )
            results[col] = {
                'min_p_value': min_p,
                'granger_causal': min_p < 0.05
            }
        except Exception as e:
            results[col] = {'error': str(e)}

    return results
```

### 7.5 XGBoostによる予測モデル

```python
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def train_occupancy_predictor(df: pd.DataFrame) -> dict:
    """ペルソナ比率を特徴量に稼働率予測モデルを訓練"""

    persona_cols = [c for c in df.columns if c.startswith('persona_')]
    month_cols = [f'month_{m}' for m in range(1, 13)]

    feature_cols = persona_cols + month_cols + ['review_count']

    X = df[feature_cols].fillna(0)
    y = df['occ']

    # 時系列クロスバリデーション（データリーク防止）
    tscv = TimeSeriesSplit(n_splits=3)
    scores = {'rmse': [], 'r2': []}

    for train_idx, test_idx in tscv.split(X):
        model = XGBRegressor(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42
        )
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        pred = model.predict(X.iloc[test_idx])
        scores['rmse'].append(np.sqrt(mean_squared_error(y.iloc[test_idx], pred)))
        scores['r2'].append(r2_score(y.iloc[test_idx], pred))

    return {
        'mean_rmse': np.mean(scores['rmse']),
        'mean_r2': np.mean(scores['r2']),
        'model': model
    }
```

---

## 8. 実装環境要件

### 8.1 ハードウェア推奨スペック

| コンポーネント | 最小構成 | 推奨構成 |
|-------------|---------|---------|
| GPU | NVIDIA 8GB VRAM（RTX 3070等） | NVIDIA 24GB VRAM（RTX 4090等） |
| RAM | 16GB | 32GB以上 |
| ストレージ | 50GB（データ+モデル） | 100GB以上 |
| OS | Linux / WSL2 / Windows | Linux推奨 |

### 8.2 Pythonパッケージ

```txt
# requirements.txt
torch>=2.3.0
transformers>=4.41.0
sentence-transformers>=3.0.0
datasets>=2.19.0
umap-learn>=0.5.6
hdbscan>=0.8.33
scikit-learn>=1.4.0
xgboost>=2.0.0
statsmodels>=0.14.0
pandas>=2.2.0
numpy>=1.26.0
matplotlib>=3.8.0
seaborn>=0.13.0
plotly>=5.20.0        # インタラクティブ可視化
ollama>=0.2.0         # ローカルLLM
tqdm>=4.66.0
scipy>=1.12.0
```

### 8.3 ディレクトリ構成

```
project/
├── data/
│   ├── raw/
│   │   ├── listings.csv.gz
│   │   ├── reviews.csv.gz
│   │   └── calendar.csv.gz
│   ├── processed/
│   │   ├── reviews_labeled.parquet     # 感情ラベル付き
│   │   ├── embeddings_regional.npy     # 地域embeddings
│   │   └── monthly_persona_ratios.parquet
│   └── results/
│       ├── persona_definitions.json    # LLM命名結果
│       ├── correlation_results.csv
│       └── granger_results.csv
├── models/
│   ├── senticse_checkpoint/            # fine-tuned BERTモデル
│   └── xgboost_occupancy.json
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_sentiment_labeling.ipynb
│   ├── 03_senticse_finetuning.ipynb
│   ├── 04_clustering_regional.ipynb
│   ├── 05_clustering_facility.ipynb
│   ├── 06_llm_persona_naming.ipynb
│   ├── 07_monthly_timeseries.ipynb
│   └── 08_occupancy_analysis.ipynb
└── src/
    ├── data_loader.py
    ├── senticse_model.py
    ├── clustering.py
    ├── persona_naming.py
    └── analysis.py
```

---

## 9. 実装ロードマップ

```
Phase 0: 環境構築・データ収集（1〜2週間）
  □ Inside Airbnb データダウンロード（対象都市決定）
  □ Python環境構築・requirements.txtインストール
  □ Ollamaインストール・Qwen3:4Bモデルpull
  □ GPU動作確認（torch.cuda.is_available()）

Phase 1: データ前処理・感情ラベリング（2〜3週間）
  □ reviews.csv + listings.csv のマージ
  □ calendar.csv からの月次稼働率計算
  □ OSS感情モデルによるAirbnb口コミのpositive/negative疑似ラベル付け
  □ confidence閾値による低信頼サンプル除外
  □ ラベル分布確認（positive=1 / negative=0 のバランス）
  □ Contrastiveペア生成またはBalancedSampler適用

Phase 2: SentiCSE Fine-tune（1〜2週間）
  □ SentiCSEモデルの実装・動作確認
  □ 小規模データ（1000ペア）で動作テスト
  □ 最新3か月データでFine-tune実行（GPU推奨）
  □ SgTS評価指標による品質確認
  □ チェックポイント保存

Phase 3: 地域ペルソナ構築（1〜2週間）
  □ 全Airbnb口コミのembedding生成（fine-tunedモデル）
  □ UMAP（50次元・2次元）実行
  □ HDBSCAN クラスタリング・パラメータ調整
  □ シルエット係数によるクラスタ品質評価
  □ 代表口コミのサンプリング

Phase 4: LLMペルソナ命名（1週間）
  □ 各クラスタの代表口コミ抽出
  □ Ollamaによるペルソナ命名バッチ実行
  □ 命名結果の手動検証（妥当性確認）
  □ persona_definitions.json出力

Phase 5: 施設ペルソナ構築（2〜3週間）
  □ listing_idごとのクラスタリングスクリプト実装
  □ 地域ペルソナへのソフトマッピング
  □ 月次ペルソナ構成比率時系列データ生成

Phase 6: 関係分析・予測モデル（3〜4週間）
  □ 月次ペルソナ比率 × 稼働率の相関分析
  □ Granger因果性検定
  □ 重回帰分析（OLS）
  □ XGBoost稼働率予測モデル構築
  □ アブレーション実験（感情Contrastive vs 通常SBERT比較）

Phase 7: 論文執筆（6〜8週間）
  □ 手法セクション執筆
  □ 実験・結果セクション
  □ 関連研究セクション（P1〜P6 + C1〜C4 引用）
  □ IJHM / Tourism Management 投稿
```

**総期間目安**: 4〜6ヶ月

---

## 10. 評価設計

### 10.1 Embedding品質評価（SgTS）

```
SgTS（Sentiment-guided Textual Similarity）:
  同極性ペアの平均コサイン類似度 > 異極性ペアの平均コサイン類似度

  目標値:
    sim(pos, pos) > 0.7
    sim(neg, neg) > 0.7
    sim(pos, neg) < 0.3

  ベースライン比較:
    - 通常SBERT（all-MiniLM-L6-v2）
    - Fine-tune前BERT
    - Fine-tune後SentiCSE（提案）
```

### 10.2 クラスタリング品質評価

```
・シルエット係数（目標: > 0.3）
・Davies-Bouldin指数（低いほど良い）
・ノイズ比率（目標: < 20%）
・感情純度（各クラスタ内の支配的感情の比率、目標: > 0.7）
```

### 10.3 ペルソナ品質評価

```
定量評価:
  ・クラスタ内評価スコア（review_scores_*）の分散 → 低いほど均質
  ・ペルソナ間の重複度（クラスタ重心間のコサイン距離）

定性評価:
  ・Airbnb実務経験者2〜3名によるペルソナ妥当性チェック
  ・「このペルソナは実際にありそうか」5段階評価
```

### 10.4 稼働率予測評価

```
ベースライン:
  1. 前月稼働率（ナイーブ）
  2. 季節ダミーのみ回帰
  3. 通常SBERT embeddingのペルソナ比率 + 季節ダミー（アブレーション）

提案モデル:
  4. SentiCSE embeddingのペルソナ比率 + 季節ダミー（XGBoost）

評価指標: RMSE, MAE, R²
期待仮説: ベースライン3 vs 4の比較でSentiCSEの優位性を示す
```

---

## 11. 課題と対処策

| 課題 | 深刻度 | 対処策 |
|------|-------|--------|
| **口コミ言語の混在**（東京の場合：英語・日本語・中国語） | ★★★ | `multilingual-e5-small`を使用し多言語対応 or 英語口コミのみでフィルタ（`language`フィールドが存在する場合） |
| **感情ラベルノイズ**（施設スコアと口コミ感情の乖離） | ★★★ | 口コミ単位の感情モデルでラベル付け（既存分類器）。高信頼度サンプルのみでFine-tune |
| **Contrastiveペア不均衡**（Positiveが多い） | ★★ | ネガティブ口コミ（評価スコア低施設）を優先サンプリング。クラスバランス重みを損失に付与 |
| **施設単位口コミ疎データ**（月5件以下） | ★★ | 四半期単位で集計。スムージング（ベイズ移動平均）を適用 |
| **HDBSCAN パラメータ感度** | ★★ | `min_cluster_size`を{1%, 2%, 5%}で感度分析。シルエット係数で最良を選択 |
| **稼働率代理指標の精度** | ★★ | calendarファイルの直接計算を主手法とし、`availability_365`を補助として使用 |
| **LLM命名の再現性** | ★ | `temperature=0.0`固定。2回実行して命名一致率を報告 |

---

## 12. 関連ファイルリンク

- [review_embedding_clustering_llm_persona_papers.md](review_embedding_clustering_llm_persona_papers.md) — 基盤論文（P1〜P6, C1〜C4）
- [hotel_absa_core_technology_document_jp.md](hotel_absa_core_technology_document_jp.md) — ABSAコア技術（感情分類モデル詳細）
- [bert_heavy_llm_final_novelty_directions.md](bert_heavy_llm_final_novelty_directions.md) — N1〜N4新規性方向性
- [open_accommodation_tourism_datasets.md](open_accommodation_tourism_datasets.md) — Inside Airbnbデータセット詳細仕様
- [local_dp_app_rd_ideas.md](local_dp_app_rd_ideas.md) — RD-01〜RD-10 応用アイデア（RD-09に近接）
