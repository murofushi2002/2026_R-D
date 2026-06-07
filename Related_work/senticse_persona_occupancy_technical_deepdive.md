# 技術詳細レビュー資料
# 感情Contrastive Embedding × ペルソナ生成 × 宿泊稼働率関係分析

> 作成日: 2026年6月3日  
> バージョン: v1.0（詳細技術レビュー版）  
> 参照元計画書: `sentiment_contrastive_persona_rd_plan.md` v1.0  
> 位置付け: 上記計画書の各Stepを技術的観点から詳細に検討・補足した深堀り資料

---

## 目次

1. [アーキテクチャ全体像の技術的整理](#1-アーキテクチャ全体像の技術的整理)
2. [データ設計の技術的詳細](#2-データ設計の技術的詳細)
3. [SentiCSE Fine-tuneの数理と実装](#3-senticse-fine-tuneの数理と実装)
4. [UMAP × HDBSCAN クラスタリングの技術的評価](#4-umap--hdbscan-クラスタリングの技術的評価)
5. [LLMペルソナ命名パイプラインの詳細設計](#5-llmペルソナ命名パイプラインの詳細設計)
6. [時系列ペルソナ比率の構築と注意点](#6-時系列ペルソナ比率の構築と注意点)
7. [稼働率関係分析の統計設計](#7-稼働率関係分析の統計設計)
8. [アブレーション設計と比較実験](#8-アブレーション設計と比較実験)
9. [先行研究との差分の再確認](#9-先行研究との差分の再確認)
10. [技術的リスクと対処策](#10-技術的リスクと対処策)
11. [数値目標・評価基準サマリ](#11-数値目標評価基準サマリ)

---

## 1. アーキテクチャ全体像の技術的整理

### 1.1 パイプライン全体図（詳細版）

```
┌─────────────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                         │
│                                                                     │
│  [Inside Airbnb]                                                    │
│   reviews.csv / listings.csv / calendar.csv                         │
│        │                                                            │
│        ▼                                                            │
│  前処理・クリーニング / 言語フィルタ / 重複除去                       │
│        │                                                            │
│        ▼                                                            │
│  OSS感情分類 → high-confidence binary labels                         │
│  positive=1 / negative=0                                             │
└──────────────┬──────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────┐           │
│  FINE-TUNE STAGE            │           │
│                             │           │
│  BalancedSampler             │           │
│  (同極性=正例/異極性=負例)    │           │
│        │                   │           │
│        ▼                   │           │
│  RoBERTa-base Fine-tune     │           │
│  (SupCon Loss, τ=0.07)      │           │
│  → SentiCSE Checkpoint      │           │
└──────────────┬──────────────┘           │
               │                          │
               ▼                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│  EMBEDDING STAGE  ※ 地域・施設の両スケールで共有する単一モデル        │
│                                                                     │
│  SentiCSE.encode(airbnb_reviews)  ← 全口コミを一括でベクトル化       │
│  → embedding matrix  E ∈ ℝ^{N × 768}                               │
│    (N = 全口コミ件数, 768次元 = RoBERTa hidden dim)                   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
          ┌─────────────────────┴──────────────────────┐
          │ embeddingは共通。対象サブセットとUMAP/HDBSCAN │
          │ のフィッティングのみスケールごとに別々に実行   │
          └──────────┬──────────────────────────────────┘
                     │
               ┌─────┴────────────────────┐
               ▼                          ▼
┌──────────────────────────────┐  ┌───────────────────────────────────┐
│  REGIONAL SCALE              │  │  FACILITY SCALE (per listing)     │
│  地域全体ペルソナ             │  │  施設個別ペルソナ                   │
│  対象: 全listings の口コミ    │  │  対象: 単一 listing_id の口コミ     │
│                              │  │                                   │
│  UMAP(n=50) → HDBSCAN        │  │  UMAP(n=20) → HDBSCAN             │
│  → K_r クラスタ              │  │  → K_f クラスタ (K_f ≤ K_r)       │
└──────────────┬───────────────┘  └────────────────┬──────────────────┘
               │                                   │
               ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PERSONA NAMING STAGE (Local LLM)                                   │
│                                                                     │
│  各クラスタ代表口コミ 10件 → Qwen3:4B (Ollama) → JSON persona        │
│  {name, purpose, priorities, sentiment_tendency, price_sensitivity} │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
               ┌────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TIME-SERIES STAGE                                                  │
│                                                                     │
│  口コミ投稿月 → ソフトメンバーシップ → 月次ペルソナ比率ベクトル         │
│  P_t = [p₁_t, p₂_t, ..., p_K_t]   (ラグ補正: -1ヶ月)               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
               ┌────────────────┴────────────────────────────────────┐
               │                                                     │
               ▼                                                     ▼
┌────────────────────────────┐          ┌──────────────────────────────┐
│  OCCUPANCY PROXY           │          │  ANALYSIS STAGE              │
│                            │          │                              │
│  calendar.csv              │          │  1. Pearson相関・ラグ相関     │
│  available=='f' の比率      │◀─JOIN────│  2. 重回帰 (OLS)             │
│  → 月次稼働率 occ_t         │          │  3. Granger因果性検定         │
└────────────────────────────┘          │  4. XGBoost 予測             │
                                        └──────────────────────────────┘
```

### 1.2 データフロー上の重要な「境界線」

本研究のパイプラインには3つの重要な **モデル境界（domain shift boundary）** が存在する。

| 境界 | from → to | リスク | 緩和策 |
|------|----------|--------|--------|
| **B1: 疑似ラベル品質** | OSS感情分類 → Airbnb binary label | モデルの誤分類・曖昧表現の混入 | confidence閾値（例: 0.95）、低信頼除外、手動監査サンプル |
| **B2: クラス不均衡** | Airbnb口コミ → positive/negative教師データ | Positive過多により負例が不足 | positive=1 / negative=0 の高信頼サンプルをバランスサンプリング |
| **B3: embedding → クラスタリング** | 768次元連続空間 → 離散クラスタ | UMAPの確率的性質により再現性が低下 | `random_state=42`固定。`n_epochs`を十分に与える |

---

## 2. データ設計の技術的詳細

### 2.1 Inside Airbnb — カラム品質の評価

計画書に記載のカラム以外に、以下の品質問題が実運用で発生しうる。

#### `reviews.csv.gz` の問題点

```python
# 口コミテキストのクリーニングで想定される問題
problems = {
    "空コメント": "comments列がNaN or 空文字列 → dropna(subset=['comments'])",
    "1〜2単語のみ": "'Great!' 'Good location' など短文 → len(text.split()) < 5 で除外",
    "多言語混在": "日本語・中国語・韓国語が混在 → fasttext言語判定でフィルタ",
    "HTMLエンティティ": "&amp; &lt; など → html.unescape()で前処理",
    "個人情報リスク": "メールアドレス・電話番号が含まれる場合がある → 正規表現マスク",
    "URLが含まれる": "施設のWeb URLが貼られることがある → URL除去"
}
```

**推奨前処理コード（拡張版）**:

```python
import re
import html
import fasttext
from pathlib import Path

# fasttext言語判定モデル（lid.176.bin）を事前ダウンロード
# https://fasttext.cc/docs/en/language-identification.html
ft_model = fasttext.load_model("lid.176.bin")

def clean_review(text: str) -> str | None:
    """口コミテキストのクリーニング。不適切な場合はNoneを返す"""
    if not isinstance(text, str) or not text.strip():
        return None

    # HTMLエンティティのデコード
    text = html.unescape(text)
    # URL除去
    text = re.sub(r'https?://\S+', '', text)
    # メールアドレスマスク
    text = re.sub(r'\S+@\S+\.\S+', '[EMAIL]', text)
    # 電話番号（簡易）マスク
    text = re.sub(r'\+?\d[\d\s\-().]{7,}\d', '[PHONE]', text)
    # 連続スペース・改行の正規化
    text = re.sub(r'\s+', ' ', text).strip()

    # 最低単語数フィルタ
    if len(text.split()) < 5:
        return None

    # 最大長制限（256トークン以上は打ち切り）
    words = text.split()
    if len(words) > 256:
        text = ' '.join(words[:256])

    return text

def filter_language(text: str, target_lang: str = "en") -> bool:
    """fasttext言語判定（英語フィルタの場合）"""
    labels, probs = ft_model.predict(text.replace('\n', ' '), k=1)
    detected = labels[0].replace('__label__', '')
    return detected == target_lang and probs[0] > 0.8
```

#### `calendar.csv.gz` の問題点

カレンダーデータは特に注意が必要。Inside Airbnbのスナップショット日以降のカレンダーデータは「ホストが意図的にブロックした日付」を含む場合がある。

```python
# calendar.csvの稼働率計算における注意点

# available == 't' の内訳:
#   - 実際に空いている（未予約）
#   - ホストがブロックした（ブロック日）

# available == 'f' の内訳:
#   - 予約済み
#   ※ ただし、Airbnb APIの仕様変更により 'f' がブロック日を含む場合がある

# より精度の高い稼働率計算（San Francisco Airbnb Datathon 手法より）:
# 「レビュー数ベース稼働率」との相関で calendar 稼働率を検証

def validate_occupancy(calendar_occ: pd.Series, review_based_occ: pd.Series):
    """
    calendar由来稼働率 vs レビュー数ベース稼働率の相関でデータ品質確認
    Pearson r > 0.6 であれば calendar 稼働率の利用を承認
    """
    from scipy import stats
    merged = pd.concat([calendar_occ, review_based_occ], axis=1).dropna()
    r, p = stats.pearsonr(merged.iloc[:, 0], merged.iloc[:, 1])
    print(f"Calendar vs Review-based occupancy correlation: r={r:.3f}, p={p:.4f}")
    return r > 0.6  # 採用基準

# レビュー数ベース稼働率の計算（補助的指標）
# Airbnb Review Rate ≈ 72%（Airbnb公式推計）なので
# 実稼働泊数 ≈ (月間レビュー数 / 0.72) × 平均宿泊泊数(= 平均3泊と仮定)
def estimate_review_based_occupancy(reviews_df: pd.DataFrame,
                                     listings_df: pd.DataFrame) -> pd.DataFrame:
    monthly_reviews = (
        reviews_df.groupby(['listing_id',
                            pd.to_datetime(reviews_df['date']).dt.to_period('M')])
        .size()
        .reset_index(name='review_count')
    )
    monthly_reviews['est_nights_booked'] = monthly_reviews['review_count'] / 0.72 * 3
    # 月間稼働日数 / その月の日数
    monthly_reviews['year_month_dt'] = monthly_reviews['date'].dt.to_timestamp()
    monthly_reviews['days_in_month'] = monthly_reviews['year_month_dt'].dt.days_in_month
    monthly_reviews['review_based_occ'] = (
        monthly_reviews['est_nights_booked'] / monthly_reviews['days_in_month']
    ).clip(0, 1)
    return monthly_reviews
```

### 2.2 Airbnb疑似ラベルの品質管理

外部教師データは使わず、Airbnb口コミ自体にOSS感情分類モデルを適用する。fine-tuneに使うのは `positive=1` / `negative=0` の2値ラベルのみで、曖昧・低信頼サンプルは学習から除外する。

```
疑似ラベル生成:
  input: comments_clean
  model: distilbert-base-uncased-finetuned-sst-2-english 等
  keep: score >= 0.95
  label: positive=1, negative=0

品質管理:
  - ラベル分布をレポート化
  - positive/negative をバランスサンプリング
  - 高信頼サンプルから各100件程度を手動監査
  - 低信頼・中立的レビューはfine-tuneには使わず、embedding対象には残す
```

**疑似ラベル方式の利点**:

| 観点 | 利点 | 注意点 |
|------|------|--------|
| ドメイン整合 | Airbnb固有の文体・語彙で追加学習できる | 感情分類モデル由来のラベルノイズが残る |
| ラベル設計 | positive=1 / negative=0 で明確 | mixed/neutralは学習対象外 |
| 再現性 | モデルID・閾値・seedで再現可能 | モデル更新を避けるためIDを固定する |

---

## 3. SentiCSE Fine-tuneの数理と実装

### 3.1 数学的定式化の詳細

#### 3.1.1 Mean Poolingによる文ベクトル生成

SentiCSEは最終的に文全体を1つのベクトル $\mathbf{h} \in \mathbb{R}^{768}$ で表現する。CLSトークンよりもMean Poolingが安定的であることが実証されている（Reimers & Gurevych, 2019）。

$$
\mathbf{h} = \frac{\sum_{i=1}^{L} m_i \cdot \mathbf{t}_i}{\sum_{i=1}^{L} m_i}
$$

- $\mathbf{t}_i$: $i$ 番目トークンの隠れ状態ベクトル（768次元）
- $m_i$: Attention mask（有効トークン=1, パディング=0）
- $L$: シーケンス長（max=256）

#### 3.1.2 Supervised Contrastive Loss（Khosla et al. 2020）

バッチ内で同感情極性の文を全て正例とする多正例対応SupCon損失:

$$
\mathcal{L}_{\text{SupCon}} = \sum_{i \in \mathcal{I}} \frac{-1}{|P(i)|} \sum_{p \in P(i)} \log \frac{\exp\left(\mathbf{z}_i \cdot \mathbf{z}_p / \tau\right)}{\sum_{a \in A(i)} \exp\left(\mathbf{z}_i \cdot \mathbf{z}_a / \tau\right)}
$$

- $\mathcal{I} = \{1, \ldots, N\}$: バッチインデックス
- $P(i) = \{p \in \mathcal{I} \setminus \{i\} \mid y_p = y_i\}$: バッチ内の同極性サンプル集合（複数正例）
- $A(i) = \mathcal{I} \setminus \{i\}$: 自己以外の全サンプル（正例＋負例）
- $\mathbf{z}_i = \text{normalize}(\mathbf{h}_i)$: L2正規化済みembedding
- $\tau$: 温度パラメータ（$\tau = 0.07$ 推奨）

**SimCSEとの違い（重要）**:

| 損失 | 正例の定義 | 負例の定義 |
|------|-----------|-----------|
| SimCSE教師なし | 同一文 × 2回Dropout | バッチ内他文 |
| SimCSE教師あり | NLI含意ペア（意味的等価） | NLI矛盾ペア（ハード負例） |
| **SentiCSE** | 同感情極性ペア（感情的等価） | 異感情極性ペア（感情的対立） |

SentiCSEは「感情空間での近接性」を最適化するため、感情極性が同じ文（例: 食事PositiveとスタッフPositive）が空間的に近くなる。これは後段のクラスタリングで「感情軸での自然分離」を生む。

#### 3.1.3 Sentiment-guided Textual Similarity（SgTS）評価指標

Fine-tuneの品質評価に使う指標。

$$
\text{SgTS} = \frac{1}{|C|} \sum_{c \in C} \left( \bar{S}^{+}_c - \bar{S}^{-}_c \right)
$$

ここで:
- $C$: 感情クラス集合 $\{pos, neu, neg\}$
- $\bar{S}^{+}_c$: クラス $c$ 内の全ペア間コサイン類似度の平均（**同極性類似度**）
- $\bar{S}^{-}_c$: クラス $c$ と他クラス間のペア間コサイン類似度の平均（**異極性類似度**）

目標値:

$$
\text{SgTS} > 0 \quad \text{（かつ各 } \bar{S}^{+}_c > 0.7,\ \bar{S}^{-}_c < 0.3\text{）}
$$

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_sgts(embeddings: np.ndarray, labels: np.ndarray) -> dict:
    """
    Sentiment-guided Textual Similarity を計算
    embeddings: (N, D) L2正規化済みembedding
    labels: (N,) 0=negative, 1=neutral, 2=positive
    """
    results = {}
    label_set = np.unique(labels)

    for lbl in label_set:
        mask_same = labels == lbl
        mask_diff = labels != lbl

        emb_same = embeddings[mask_same]
        emb_diff = embeddings[mask_diff]

        if len(emb_same) < 2:
            continue

        # 同極性ペアの平均コサイン類似度
        sim_matrix_pos = cosine_similarity(emb_same)
        # 対角を除く上三角
        n = len(emb_same)
        idx = np.triu_indices(n, k=1)
        s_pos = sim_matrix_pos[idx].mean()

        # 異極性ペアの平均コサイン類似度（サンプリング）
        n_sample = min(len(emb_same) * 5, len(emb_diff))
        sampled_diff = emb_diff[np.random.choice(len(emb_diff), n_sample, replace=False)]
        sim_matrix_neg = cosine_similarity(emb_same, sampled_diff)
        s_neg = sim_matrix_neg.mean()

        results[f'label_{lbl}'] = {
            'intra_sim': s_pos,   # 目標: > 0.7
            'inter_sim': s_neg,   # 目標: < 0.3
            'sgts': s_pos - s_neg  # 目標: > 0
        }

    overall_sgts = np.mean([v['sgts'] for v in results.values()])
    results['overall_sgts'] = overall_sgts
    return results
```

### 3.2 バッチ戦略の詳細

Contrastive Learningの性能はバッチ内の多様性に強く依存する。

```
問題: ランダムバッチでは同極性サンプルが多すぎて負例が不足する場合がある
     （Airbnb口コミは一般にPositive過多になりやすい）

対策: Balanced Batch Sampler を実装

バッチ構成:
  batch_size = 64
  各ラベルから均等にサンプリング:
    positive: 22件
    neutral:  21件
    negative: 21件

期待効果:
  → バッチ内で必ず異極性ペアが多数生成される
  → SgTS の早期改善が期待できる
```

```python
from torch.utils.data import Sampler
from collections import defaultdict
import random

class SentimentBalancedSampler(Sampler):
    """感情クラスバランス付きバッチサンプラー"""
    def __init__(self, labels: list, batch_size: int):
        self.labels = labels
        self.batch_size = batch_size
        self.label_indices = defaultdict(list)
        for idx, lbl in enumerate(labels):
            self.label_indices[lbl].append(idx)

    def __iter__(self):
        per_class = self.batch_size // len(self.label_indices)
        batches = []
        label_pools = {lbl: idxs[:] for lbl, idxs in self.label_indices.items()}
        for pool in label_pools.values():
            random.shuffle(pool)

        min_len = min(len(p) for p in label_pools.values())
        for _ in range(min_len // per_class):
            batch = []
            for pool in label_pools.values():
                batch.extend(pool[:per_class])
                pool[:] = pool[per_class:]
            random.shuffle(batch)
            batches.extend(batch)
        return iter(batches)

    def __len__(self):
        return len(self.labels)
```

### 3.3 ハイパーパラメータ感度分析

| パラメータ | デフォルト値 | 試行範囲 | SgTSへの影響度 |
|-----------|------------|---------|----------------|
| `temperature` τ | 0.07 | [0.03, 0.05, 0.07, 0.10] | **高** |
| `learning_rate` | 2e-5 | [1e-5, 2e-5, 5e-5] | 中 |
| `batch_size` | 64 | [32, 64, 128] | 中（VRAMと trade-off） |
| `epochs` | 5 | [3, 5, 10] | 低（早期収束が多い） |
| `max_length` | 256 | [128, 256] | 低 |

**温度パラメータ $\tau$ について**:

$\tau$ が小さいほど損失が鋭くなり（harderな負例に強く反応）、クラスタの分離が強調される。ただし小さすぎると訓練が不安定になる。Airbnb疑似ラベルでは低信頼・中立的サンプルを除外し、positive/negativeの高信頼サンプルだけで $\tau = 0.07$ を初期値とする。

---

## 4. UMAP × HDBSCAN クラスタリングの技術的評価

### 4.1 UMAPの数学的背景と設定の意味

UMAPはリーマン多様体学習に基づく次元削減手法（McInnes et al., 2018）。

$$
\min_{Y} \sum_{i \neq j} \left[ w_{ij} \log \frac{w_{ij}}{q_{ij}} + (1 - w_{ij}) \log \frac{1 - w_{ij}}{1 - q_{ij}} \right]
$$

- $w_{ij}$: 高次元空間でのファジィ集合（$k$NN距離で定義）
- $q_{ij}$: 低次元空間での類似度（$\text{dist}(y_i, y_j)$ から算出）

**設定値の意味**:

```python
# クラスタリング用UMAP（50次元）
reducer_cluster = umap.UMAP(
    n_components=50,    # → 768次元を50次元に削減（情報を保持しつつクラスタ成形）
    n_neighbors=15,     # → 局所構造 vs 大域構造のトレードオフ
                        #    大きいと大域構造を保持（クラスタ間距離を維持）
                        #    小さいと局所密度を強調（細かいクラスタが現れる）
                        #    推奨: 口コミ数に応じて 10〜30 で調整
    min_dist=0.0,       # → 0.0にすることで「詰め込み」が最大化
                        #    クラスタリング向け設定（可視化向けは 0.1）
    metric='cosine',    # → Transformerベースembeddingはcosine距離が適切
    random_state=42,
    n_epochs=500        # → 小データセットではデフォルト(200)より多く設定
)
```

**n_neighbors の口コミ数に応じた調整ガイド**:

| 口コミ数 N | 推奨 n_neighbors | 理由 |
|-----------|----------------|------|
| < 1,000 | 5〜10 | データが少ないため局所構造を優先 |
| 1,000〜10,000 | 15 | バランス（デフォルト） |
| 10,000〜100,000 | 20〜30 | データ量が多く大域構造も捉えたい |
| > 100,000 | 30〜50 | 大域的なペルソナ群の分布を維持 |

### 4.2 HDBSCANの技術的詳細

HDBSCANは階層的密度ベースクラスタリング（Campello et al., 2013）。

**なぜ k-means ではなく HDBSCAN か**:

| 比較軸 | k-means | HDBSCAN |
|--------|---------|---------|
| クラスタ数指定 | 必要（事前にKを決定） | **不要（自動決定）** |
| クラスタ形状 | 球状のみ | 任意形状 |
| ノイズ点 | 全点をクラスタに割り当て | **ノイズ点 (-1) を明示** |
| 空間密度 | 均一密度を仮定 | 密度の不均一を許容 |
| 口コミへの適合 | ペルソナ数が不明なため不適 | **事前知識不要で適切** |

**クラスタ選択方法 (`cluster_selection_method`)**:

```python
# EOM（Excess of Mass）vs Leaf の違い
clusterer_eom = hdbscan.HDBSCAN(
    min_cluster_size=100,
    cluster_selection_method='eom'   # → 大きなクラスタを優先。ペルソナ生成に推奨
)
clusterer_leaf = hdbscan.HDBSCAN(
    min_cluster_size=100,
    cluster_selection_method='leaf'  # → 木構造の葉ノードを採用。細かいクラスタが増加
)
# ホテル口コミペルソナには 'eom' を推奨:
# 意味のある大きなゲスト集団を検出することが目的であるため
```

**ソフトクラスタリング（確率的メンバーシップ）の重要性**:

月次ペルソナ比率の計算では「各口コミがどのペルソナにどの程度属するか」の確率値が必要。

```python
# ハード割り当て（通常のHDBSCAN）
label = clusterer.labels_[i]  # → 単一クラスタID or -1

# ソフト割り当て（本研究で使用）
soft = hdbscan.membership_vector(clusterer, new_point)
# → shape: (K,) 各クラスタへの帰属確率（和=1）

# 実装上の注意: prediction_data=True が必要
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=100,
    prediction_data=True  # ← これがないと membership_vector が動作しない
)
```

### 4.3 2スケールの技術的な接続方法

地域ペルソナと施設ペルソナは**同一のSentiCSE embeddingモデル**を共有する。Fine-tuneは1回だけ行い、そのCheckpointで全口コミをベクトル化する。スケールごとに**別々に実行するのはUMAP+HDBSCANのクラスタリング**のみ（対象サブセットと次元数が異なるため）。
標準実験では、fine-tune teacher のみレビュー投稿日ベースの最新3か月に絞る。本番のembedding、クラスタリング、時系列集計、評価は全口コミを母集団とする。

施設ペルソナと地域ペルソナを比較する際は、施設口コミのembeddingを**地域側で学習済みのUMAP変換器**に通し、地域クラスタリングのソフトメンバーシップを取得することで「この施設にはどの地域ペルソナが何%来ているか」が定量化できる。

```python
def map_facility_to_regional_personas(
    facility_embeddings: np.ndarray,
    regional_clusterer: hdbscan.HDBSCAN,
    regional_reducer: umap.UMAP
) -> np.ndarray:
    """
    施設固有embeddings → 地域ペルソナへのソフトマッピング
    施設が地域ペルソナの「どのタイプのゲストが多いか」を定量化
    """
    # 施設embeddings を地域UMAP空間へ投影
    facility_in_regional_space = regional_reducer.transform(facility_embeddings)

    # 地域クラスタリングのソフトメンバーシップを取得
    soft_memberships = hdbscan.membership_vector(
        regional_clusterer, facility_in_regional_space
    )
    # shape: (n_facility_reviews, K_regional)

    return soft_memberships  # → 施設口コミの地域ペルソナへの帰属確率

# 使用例:
# 「この施設はどの地域ペルソナがどの程度来ているか」を月次で追跡
facility_regional_ratio = map_facility_to_regional_personas(
    facility_embeddings, regional_clusterer, regional_reducer
).mean(axis=0)  # → shape: (K_regional,)
```

### 4.4 クラスタリング品質の多角的評価

クラスタ品質を単一指標だけで評価することの危険性と、推奨する多角的評価アプローチ:

```python
def comprehensive_cluster_evaluation(
    embeddings: np.ndarray,    # UMAP後 (N, 50)
    labels: np.ndarray,        # HDBSCANラベル (-1 = ノイズ)
    sentiment_labels: np.ndarray,  # 感情極性ラベル
    persona_labels: list[str]  # LLM命名したペルソナ名
) -> dict:
    """多角的クラスタ品質評価"""
    from sklearn.metrics import silhouette_score, davies_bouldin_score

    valid = labels != -1
    emb_valid = embeddings[valid]
    lbl_valid = labels[valid]
    sent_valid = sentiment_labels[valid]

    # 1. 幾何学的クラスタ品質
    silhouette = silhouette_score(emb_valid, lbl_valid, metric='euclidean')
    db_index = davies_bouldin_score(emb_valid, lbl_valid)

    # 2. ノイズ比率
    noise_ratio = (~valid).mean()

    # 3. 感情純度（各クラスタ内での支配的感情の比率）
    sentiment_purity = {}
    for cluster_id in np.unique(lbl_valid):
        mask = lbl_valid == cluster_id
        sentiments = sent_valid[mask]
        dominant = np.bincount(sentiments).argmax()
        purity = (sentiments == dominant).mean()
        sentiment_purity[cluster_id] = purity
    avg_sentiment_purity = np.mean(list(sentiment_purity.values()))

    # 4. クラスタサイズの均一性（ジニ不純度）
    cluster_sizes = np.bincount(lbl_valid)
    cluster_size_cv = cluster_sizes.std() / cluster_sizes.mean()  # 変動係数

    # 5. ペルソナ名の多様性（重複命名の検出）
    unique_names = len(set(persona_labels))
    name_diversity = unique_names / len(persona_labels)

    return {
        'silhouette': silhouette,           # 目標: > 0.3
        'davies_bouldin': db_index,          # 目標: < 1.5（低いほど良い）
        'noise_ratio': noise_ratio,          # 目標: < 0.2
        'avg_sentiment_purity': avg_sentiment_purity,  # 目標: > 0.7
        'cluster_size_cv': cluster_size_cv,  # 目標: < 2.0（大小クラスタの不均一許容）
        'persona_name_diversity': name_diversity  # 目標: 1.0（全ユニーク）
    }
```

---

## 5. LLMペルソナ命名パイプラインの詳細設計

### 5.1 プロンプトエンジニアリングの詳細

計画書のプロンプトに加えて、より堅牢な命名のための設計:

#### 5.1.1 Few-shotプロンプト（品質向上版）

```python
FEW_SHOT_EXAMPLES = """
Example 1:
Reviews:
- "Perfect location, walked everywhere. Room was small but clean."
- "Great for exploring the city. Staff super helpful."
- "Amazing position near subway. Tiny room but who cares when you're out all day."
Output:
{
  "persona_name": "Urban Explorer",
  "purpose": "City sightseeing and cultural exploration",
  "top_priorities": ["location", "accessibility", "local experiences"],
  "sentiment_tendency": "positive",
  "price_sensitivity": "medium",
  "description": "Guests focused on exploring the city..."
}

Example 2:
Reviews:
- "Work trip, needed fast WiFi. Got it. Nothing special."
- "Functional for a business stay. Checked out early most days."
- "Clean, quiet, close to conference center. That's all I needed."
Output:
{
  "persona_name": "Business Traveler",
  "purpose": "Work trip with focus on productivity",
  "top_priorities": ["WiFi", "quiet environment", "proximity to business district"],
  "sentiment_tendency": "mixed",
  "price_sensitivity": "low",
  "description": "Business guests who prioritize functional amenities..."
}
"""

def name_persona_cluster_fewshot(
    reviews_sample: list[str],
    model: str = "qwen3:4b",
    language: str = "en"
) -> dict:
    """Few-shotプロンプトによるペルソナ命名（品質向上版）"""

    sample_text = "\n".join([f"- \"{r[:200]}\"" for r in reviews_sample[:10]])

    if language == "ja":
        lang_instruction = "Output in Japanese. Persona name should be in Japanese."
    else:
        lang_instruction = "Output in English."

    prompt = f"""You are a hospitality researcher specializing in guest persona analysis.

{lang_instruction}

Here are examples of how to analyze guest reviews and create personas:
{FEW_SHOT_EXAMPLES}

Now analyze these reviews from a new cluster:
{sample_text}

Output ONLY valid JSON with exactly these keys (no additional text):
{{
  "persona_name": "concise name (max 5 words)",
  "purpose": "primary stay purpose (max 20 words)",
  "top_priorities": ["priority1", "priority2", "priority3"],
  "sentiment_tendency": "positive|mixed|negative",
  "price_sensitivity": "low|medium|high",
  "description": "2-3 sentences describing this persona type"
}}"""

    import ollama, json

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.0, "num_predict": 512}
    )
    content = response['message']['content'].strip()

    # JSONブロック抽出（マークダウンコードブロック対応）
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        # フォールバック: 最初の { から最後の } を抽出
        start = content.find('{')
        end = content.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(content[start:end])
        return {"persona_name": "Unknown", "error": str(e), "raw": content}
```

### 5.2 ペルソナ命名の再現性検証

LLMの命名は同一入力でも変動しうる。`temperature=0.0` でも量子化モデルでは微妙な揺らぎが生じる。

```python
def verify_persona_consistency(
    reviews_sample: list[str],
    model: str = "qwen3:4b",
    n_trials: int = 3
) -> dict:
    """同一クラスタに対して複数回命名し、一致率を確認"""
    results = [name_persona_cluster_fewshot(reviews_sample, model) for _ in range(n_trials)]

    # persona_name の一致率
    names = [r.get('persona_name', '') for r in results]
    unique_names = len(set(names))
    consistency = 1.0 - (unique_names - 1) / max(n_trials - 1, 1)

    # top_priorities の重複率（Jaccard類似度）
    priorities = [set(r.get('top_priorities', [])) for r in results]
    if len(priorities) >= 2:
        jaccard = len(priorities[0] & priorities[1]) / len(priorities[0] | priorities[1])
    else:
        jaccard = 1.0

    return {
        'names': names,
        'name_consistency': consistency,   # 目標: > 0.7
        'priority_jaccard': jaccard,        # 目標: > 0.5
        'recommended': results[0]           # 最初の結果を採用
    }
```

### 5.3 ペルソナ命名結果の構造化と管理

```python
# persona_definitions.json の設計
PERSONA_SCHEMA = {
    "version": "1.0",
    "created_at": "2026-06-03",
    "model": "qwen3:4b",
    "city": "tokyo",
    "scale": "regional",  # or "facility"
    "personas": [
        {
            "cluster_id": 0,
            "size": 1234,           # クラスタ内口コミ件数
            "noise": False,
            "llm_output": {
                "persona_name": "Urban Explorer",
                "purpose": "...",
                "top_priorities": [...],
                "sentiment_tendency": "positive",
                "price_sensitivity": "medium",
                "description": "..."
            },
            "cluster_stats": {
                "mean_review_score": 4.2,
                "dominant_sentiment": "positive",
                "sentiment_purity": 0.78,
                "centroid_embedding": [...]  # 768次元（オプション、容量大）
            },
            "representative_reviews": [...]  # 代表口コミ10件
        }
    ]
}
```

---

## 6. 時系列ペルソナ比率の構築と注意点

### 6.1 ラグ補正の理論的根拠と感度分析

Airbnbでは宿泊後にのみレビューを投稿できる。実際の宿泊月 $t$ と口コミ投稿月 $t'$ の関係:

$$
t' = t + \Delta t_{\text{post}}
$$

実証研究（Bridges & Vásquez, 2018）では、Airbnb口コミの**中央値投稿ラグは約7日**（即日〜14日の範囲に約80%が集中）。したがって:

$$
\Delta t_{\text{lag}} = \text{round}\left(\frac{\overline{\Delta t_{\text{post}}}}{30}\right) = 0 \text{ or } 1 \text{ ヶ月}
$$

**感度分析として lag ∈ {0, 1, 2} を全て試行**し、稼働率との相関が最大となるlagを採用する。

```python
def lag_sensitivity_analysis(
    persona_ratios: pd.DataFrame,
    monthly_occ: pd.DataFrame,
    max_lag: int = 3
) -> pd.DataFrame:
    """ラグ設定の感度分析: どのラグで相関が最大か確認"""
    from scipy import stats

    persona_cols = [c for c in persona_ratios.columns if c.startswith('persona_')]
    results = []

    for lag in range(0, max_lag + 1):
        shifted_ratios = persona_ratios.copy()
        shifted_ratios.index = shifted_ratios.index - lag

        merged = shifted_ratios.join(monthly_occ.rename(columns={'occupancy_rate': 'occ'}), how='inner')

        for col in persona_cols:
            valid = merged[[col, 'occ']].dropna()
            if len(valid) < 6:
                continue
            r, p = stats.pearsonr(valid[col], valid['occ'])
            results.append({'persona': col, 'lag': lag, 'r': r, 'p': p})

    df = pd.DataFrame(results)
    best_lags = df.loc[df.groupby('persona')['r'].abs().idxmax()]
    print("各ペルソナで相関が最大となるlag:")
    print(best_lags[['persona', 'lag', 'r', 'p']].to_string())

    return df
```

### 6.2 時系列データの安定性確認

月次稼働率と月次ペルソナ比率を時系列分析に使う前に、定常性の確認が必要。

```python
from statsmodels.tsa.stattools import adfuller, kpss

def check_stationarity(series: pd.Series, name: str = "series") -> dict:
    """ADF検定 + KPSS検定で定常性を確認"""
    # 欠損値補完（線形補間）
    series = series.interpolate(method='linear').dropna()

    # ADF検定（帰無仮説: 単位根あり = 非定常）
    adf_stat, adf_p, _, _, adf_crit, _ = adfuller(series)
    adf_stationary = adf_p < 0.05  # True → 定常（単位根を棄却）

    # KPSS検定（帰無仮説: 定常）
    kpss_stat, kpss_p, _, kpss_crit = kpss(series, regression='c')
    kpss_stationary = kpss_p > 0.05  # True → 定常（非定常を棄却できない）

    result = {
        'series': name,
        'adf_p': adf_p,
        'adf_stationary': adf_stationary,
        'kpss_p': kpss_p,
        'kpss_stationary': kpss_stationary,
        'conclusion': 'stationary' if (adf_stationary and kpss_stationary)
                      else 'likely_nonstationary'
    }

    if not (adf_stationary and kpss_stationary):
        print(f"[警告] {name} が非定常の可能性があります。1階差分を検討してください。")

    return result

def make_stationary_if_needed(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """非定常系列を1階差分で定常化"""
    df = df.copy()
    for col in cols:
        result = check_stationarity(df[col], name=col)
        if result['conclusion'] == 'likely_nonstationary':
            df[f'{col}_diff'] = df[col].diff()
            print(f"  → {col} を1階差分化: {col}_diff を追加")
    return df
```

---

## 7. 稼働率関係分析の統計設計

### 7.1 重回帰モデルの仕様

$$
\text{occ}_{t} = \alpha + \sum_{k=1}^{K} \beta_k \cdot p_{k,t-\ell} + \sum_{m=2}^{12} \gamma_m \cdot D_{m,t} + \varepsilon_t
$$

- $\text{occ}_t$: 月次稼働率（0〜1）
- $p_{k,t-\ell}$: ペルソナ $k$ の $\ell$ ヶ月ラグ比率（ラグ選択は感度分析で決定）
- $D_{m,t}$: 月ダミー変数（$m=2,...,12$、$m=1$ を基準）
- $K$: ペルソナ数（通常 5〜15）

**多重共線性の確認（VIF）**:

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

def check_multicollinearity(X: pd.DataFrame) -> pd.DataFrame:
    """
    VIF（分散拡大係数）で多重共線性を診断
    VIF > 10: 深刻な多重共線性
    VIF > 5: 要注意
    """
    vif_data = pd.DataFrame({
        'Feature': X.columns,
        'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    }).sort_values('VIF', ascending=False)

    problematic = vif_data[vif_data['VIF'] > 10]
    if len(problematic) > 0:
        print(f"[警告] VIF > 10 の特徴量が {len(problematic)} 件あります:")
        print(problematic.to_string())
        print("→ PCA or Elastic Netの使用を検討してください")

    return vif_data
```

**ペルソナ比率の多重共線性問題**:

ペルソナ比率は定義上 $\sum_{k=1}^{K} p_{k,t} = 1$（完全多重共線性）。

対処法:

```python
# 方法1: 1つのペルソナを基準カテゴリとして除外（OLS）
persona_cols = [c for c in df.columns if c.startswith('persona_')]
reference = persona_cols[0]  # 最大クラスタを基準とする
X_cols = persona_cols[1:] + month_cols  # 基準ペルソナを除外
X = sm.add_constant(df[X_cols])

# 方法2: Ridge/Lasso 回帰（正則化で対処）
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

ridge_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('ridge', Ridge(alpha=1.0))
])

# 方法3: ペルソナ比率をPCA圧縮してから使用
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)  # 95%分散を説明する成分数
X_pca = pca.fit_transform(df[persona_cols])
print(f"PCA: {len(persona_cols)} → {pca.n_components_} 次元に圧縮")
```

### 7.2 Granger因果性検定の詳細設計

Granger因果性は「X の過去値が Y の予測を改善するか」を検定する。

**適用前の前提確認**:

```python
def granger_prerequisite_check(
    series_x: pd.Series,  # ペルソナ比率
    series_y: pd.Series,  # 稼働率
    max_lag: int = 3
) -> dict:
    """
    Granger因果性検定の前提条件を確認:
    1. 両系列が定常であること（非定常系列には適用不可）
    2. サンプル数が十分であること（最低 10*max_lag 以上推奨）
    """
    n = len(series_x.dropna())
    min_required = max(15, 10 * max_lag)  # 経験則

    stat_x = check_stationarity(series_x, "x")
    stat_y = check_stationarity(series_y, "y")

    issues = []
    if stat_x['conclusion'] == 'likely_nonstationary':
        issues.append("系列Xが非定常 → 差分変換が必要")
    if stat_y['conclusion'] == 'likely_nonstationary':
        issues.append("系列Yが非定常 → 差分変換が必要")
    if n < min_required:
        issues.append(f"サンプル数不足: {n} < {min_required}（max_lagを{max_lag}に設定）")

    return {'n': n, 'issues': issues, 'can_proceed': len(issues) == 0}
```

**解釈の注意点**: Granger因果性は「統計的先行性」であり、真の因果関係を保証しない。論文では以下のように慎重に表現する必要がある。

> 「ペルソナ X の比率増加が稼働率の増加に Granger 先行することが示された（F(lag=2) = 5.3, p < 0.05）。これは X タイプのゲストの増加が翌月〜翌々月の稼働率向上に関連していることを統計的に示唆するが、直接的な因果関係の解釈には留意が必要である。」

### 7.3 XGBoost予測モデルの設計詳細

**特徴量エンジニアリング**（計画書に未記載の重要要素）:

```python
def build_advanced_features(df: pd.DataFrame) -> pd.DataFrame:
    """XGBoost向け高度特徴量の追加"""
    df = df.copy()
    persona_cols = [c for c in df.columns if c.startswith('persona_')]

    # 1. ペルソナ比率の移動平均（3ヶ月）
    for col in persona_cols:
        df[f'{col}_ma3'] = df[col].rolling(3, min_periods=1).mean()

    # 2. ペルソナ比率の変化量（月次差分）
    for col in persona_cols:
        df[f'{col}_delta'] = df[col].diff()

    # 3. 稼働率の過去値（自己回帰特徴量）
    for lag in [1, 2, 3]:
        df[f'occ_lag_{lag}'] = df['occ'].shift(lag)

    # 4. 季節性の周期特徴（sin/cosエンコーディング）
    month = df.index.month if hasattr(df.index, 'month') else df['month']
    df['month_sin'] = np.sin(2 * np.pi * month / 12)
    df['month_cos'] = np.cos(2 * np.pi * month / 12)

    # 5. ペルソナ多様性指数（エントロピー）
    ratios = df[persona_cols].values
    entropy = -np.sum(ratios * np.log(ratios + 1e-9), axis=1)
    df['persona_entropy'] = entropy

    return df.dropna()
```

**SHAP値によるモデル解釈可能性**:

```python
import shap

def interpret_xgboost_model(model, X_test: pd.DataFrame) -> dict:
    """SHAP値でどのペルソナが稼働率予測に最も貢献しているかを可視化"""
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # 特徴量重要度（平均|SHAP|）
    importance_df = pd.DataFrame({
        'feature': X_test.columns,
        'mean_abs_shap': np.abs(shap_values).mean(axis=0)
    }).sort_values('mean_abs_shap', ascending=False)

    # ペルソナ関連特徴量の寄与度
    persona_features = importance_df[importance_df['feature'].str.contains('persona_')]
    non_persona_features = importance_df[~importance_df['feature'].str.contains('persona_')]

    persona_contribution = persona_features['mean_abs_shap'].sum()
    total_contribution = importance_df['mean_abs_shap'].sum()

    print(f"ペルソナ特徴量の稼働率予測への寄与率: {persona_contribution/total_contribution:.1%}")
    print("\n上位5特徴量:")
    print(importance_df.head(5).to_string())

    return {
        'shap_values': shap_values,
        'importance': importance_df,
        'persona_contribution_ratio': persona_contribution / total_contribution
    }
```

---

## 8. アブレーション設計と比較実験

### 8.1 アブレーション実験の詳細設計

本研究の核心的な貢献（**感情Contrastive embeddingの有効性**）を定量的に示すには、以下の比較実験が必要。

| モデルID | 手法 | Fine-tune | 目的 |
|----------|------|-----------|------|
| **BL-1** | 前月稼働率（ナイーブ予測） | なし | 最下位ベースライン |
| **BL-2** | 季節ダミー + OLS | なし | 季節効果のみ |
| **BL-3** | SBERT（all-MiniLM）ペルソナ + XGBoost | なし | 感情特化なしembedding |
| **BL-4** | 感情分類スコアの直接集計 | なし | 感情は使うがペルソナなし |
| **Prop-1** | SentiCSE ペルソナ（2クラス Pos/Neg）+ XGBoost | 2クラス | 本提案（簡略版） |
| **Prop-2** | SentiCSE ペルソナ（Airbnb疑似ラベル Pos/Neg）+ XGBoost | 2クラス | 本提案（フル版） |

**期待する結果**:

```
予測精度（R²）の期待される順位:
  BL-1 < BL-2 < BL-3 ≤ BL-4 < Prop-1 ≤ Prop-2

Prop-1/2 が BL-3 を上回れば:
  → 感情Contrastive embedding がSBERTより稼働率予測に有用であることの根拠
Prop-2 が BL-4 を上回れば:
  → 感情スコア直接集計よりペルソナ表現が有用であることの根拠
```

### 8.2 統計的有意性の確認

モデル間の性能差が偶然でないことを示す。

```python
from scipy import stats

def statistical_test_models(
    results_bl3: list[float],  # BL-3の各Fold R²
    results_prop2: list[float]  # Prop-2の各Fold R²
) -> dict:
    """Wilcoxon符号順位検定（ノンパラメトリック、対応ありデータ）"""
    stat, p = stats.wilcoxon(results_prop2, results_bl3, alternative='greater')
    effect_size = (np.mean(results_prop2) - np.mean(results_bl3)) / np.std(results_bl3)

    return {
        'wilcoxon_stat': stat,
        'p_value': p,
        'significant': p < 0.05,
        'effect_size_cohens_d': effect_size,
        'mean_improvement': np.mean(results_prop2) - np.mean(results_bl3)
    }
```

---

## 9. 先行研究との差分の再確認

計画書の新規性表に技術的な詳細を加えた版。

### 9.1 技術系譜と本研究の位置付け

```
技術系譜:

  SupConLoss (Khosla+ 2020, NeurIPS)
  [分類損失の代替としてContrastive Lossが有効]
          ↓ NLPへの応用
  SimCSE (Gao+ 2021, EMNLP)
  [文embeddingにContrastive Learningを適用。STS-Bで SOTA]
          ↓ 感情軸での特化
  SentiCSE (Kim+ 2024, LREC-COLING)
  [感情極性ラベルを正例/負例の決定基準に。SgTSで品質評価]
          ↓ 応用ドメインの拡張（本研究の貢献）
  SentiPersona-Airbnb [本研究]
  [Airbnb口コミ + 感情Contrastive → ペルソナ生成 → 稼働率関係分析]


  Shin et al. 2024 (ACM CHI)
  [BERT embedding → cluster → LLMペルソナ命名ワークフロー実証]
          +
  Choi et al. 2025 (ACM CHI, Proxona)
  [SBERT embedding → cluster → LLMペルソナ（YouTube コメント）]
          ↓ 感情特化embeddingへの置換 + ホテル稼働率との結合（本研究の貢献）
  SentiPersona-Airbnb [本研究]
```

### 9.2 本研究が埋める空白の詳細

#### 空白 W1: 感情Contrastive embeddingのペルソナ生成への応用

既存のペルソナ生成研究（Shin 2024, Choi 2025, Yin 2026）は全て「意味的類似性ベース」のSBERTを使用。SentiCSEのように**感情極性で空間を整形したembedding**を使うことで、単なる話題の類似ではなく「感情的な立場の類似」に基づくペルソナが生成できる。

**具体的な違いの例**:

```
SBERT embeddingの場合:
  クラスタ A: 「清掃について書いた口コミ全般」
  → 「清掃が綺麗でした」と「清掃が汚かったです」が同クラスタに入りうる

SentiCSE embeddingの場合:
  クラスタ A: 「清掃Positiveな口コミ」 ←感情で分離
  クラスタ B: 「清掃Negativeな口コミ」 ←感情で分離
  → 同じ観点でも感情的立場が異なればクラスタが分かれる
  → ペルソナが「清掃満足層」「清掃不満層」として生成される
```

#### 空白 W2: 宿泊業ペルソナと稼働率の結合

Amin et al. (2026) のスコーピングレビューが「外部変数との結合が課題」として明示。本研究は口コミペルソナという**内部シグナル**を稼働率という**経営指標**に結合する初の実装。

#### 空白 W3: ローカルLLMによるプライバシー保全ペルソナ生成

既存研究の86%がGPT-4/3.5を使用（Amin et al., 2026）。本研究はOllamaベースのローカルLLM（Qwen3:4B）を採用し、**口コミデータを外部APIに送信しないアーキテクチャ**を実現。これは旅館・ホテル業における個人情報保護（宿泊客のレビュー情報）の観点から実用上重要。

---

## 10. 技術的リスクと対処策

### 10.1 各リスクの技術的詳細

#### リスク R1: 疑似ラベルノイズ（Airbnb感情分類 → Fine-tune）

**問題の深刻度評価**: ★★★（高）

```
Inside Airbnb の特性:
  - 短文レビュー（平均 50〜150単語）
  - 民泊（キッチン付き、ホストとの交流あり）
  - 特有の観点（チェックインコード、ホスト対応、neighborhood）

疑似ラベルのリスク:
  - 一般感情モデルが宿泊文脈を誤分類する
  - 皮肉・mixed sentiment・短文が混入する
  - Positive過多で負例が不足する
```

**対処策の優先順位**:

1. confidence閾値を高めに設定（例: 0.95）
2. positive=1 / negative=0 の2値に限定し、neutral/mixedを学習対象外にする
3. ラベル別サンプルを手動監査し、必要なら閾値・モデルを変更
4. BalancedSamplerでクラス不均衡を抑える

```python
# Airbnb内疑似ラベルによる本学習
def build_airbnb_binary_teacher(reviews_df, predictions, threshold=0.95):
    labels = []
    for pred in predictions:
        if pred["score"] < threshold:
            labels.append(None)
        elif pred["label"].lower() == "positive":
            labels.append(1)
        elif pred["label"].lower() == "negative":
            labels.append(0)
        else:
            labels.append(None)

    teacher = reviews_df.assign(label_id=labels).dropna(subset=["label_id"])
    return balance_positive_negative(teacher)
```

#### リスク R2: 施設単位の口コミ疎データ問題

**問題**: 月次口コミが3件以下の施設では月次比率が不安定。

**対処策の詳細**:

```python
def handle_sparse_facility_data(
    facility_reviews_df: pd.DataFrame,
    embeddings: np.ndarray,
    min_monthly_reviews: int = 5,
    smoothing_window: int = 3
) -> pd.DataFrame:
    """
    疎データ対策:
    1. 月次レビュー数が min_monthly_reviews 未満の月はフラグ付け
    2. ベイズ移動平均でスムージング
    """
    from scipy.stats import dirichlet

    monthly_ratio = compute_monthly_persona_ratios(facility_reviews_df, embeddings, ...)
    monthly_counts = facility_reviews_df.groupby(
        pd.to_datetime(facility_reviews_df['date']).dt.to_period('M')
    ).size().rename('review_count')

    merged = monthly_ratio.join(monthly_counts)
    merged['reliable'] = merged['review_count'] >= min_monthly_reviews

    # ベイズ移動平均スムージング（信頼性の低い月の重みを下げる）
    persona_cols = [c for c in merged.columns if c.startswith('persona_')]
    weights = merged['review_count'].clip(lower=1)

    for col in persona_cols:
        merged[f'{col}_smoothed'] = (
            merged[col]
            .multiply(weights)
            .rolling(window=smoothing_window, min_periods=1, center=True)
            .sum()
            / weights.rolling(window=smoothing_window, min_periods=1, center=True).sum()
        )

    # 月次レビュー数が極端に少ない期間を除外（解析対象外フラグ）
    merged['exclude'] = merged['review_count'] < 3

    return merged
```

### 10.2 計算量の見積もりと最適化

```
処理量の見積もり（東京Airbnb、fine-tuneは最新3か月、本番embeddingは全口コミ）:

[Step 2: embedding生成]
  対象: ~75,000口コミ
  モデル: roberta-base (125M)
  バッチサイズ: 32
  1バッチの処理時間: ~0.5秒 (RTX 3070 8GB)
  必要バッチ数: 75,000 / 32 ≈ 2,344 バッチ
  推定時間: 2,344 × 0.5秒 ≈ 20分

[Step 2: Fine-tune]
  対象: 100,000ペア
  バッチサイズ: 64
  エポック数: 5
  1エポック: 100,000 / 64 ≈ 1,563 ステップ
  1ステップの処理時間: ~0.3秒 (RTX 3070 8GB)
  推定時間: 5 × 1,563 × 0.3秒 ≈ 39分

[Step 3: UMAP]
  n=75,000, d=768 → 50次元
  推定時間: 3〜10分（UMAP実装依存）

[Step 3: HDBSCAN]
  n=75,000, d=50
  推定時間: 1〜3分

[Step 4: LLMペルソナ命名]
  クラスタ数: ~10
  1クラスタの処理時間: ~5秒 (Qwen3:4B, Ollama)
  推定時間: 10 × 5秒 = 50秒

合計推定時間: ~1〜2時間（GPU使用時）
```

---

## 11. 数値目標・評価基準サマリ

### 11.1 各ステップの合格基準

| Step | 指標 | 合格基準 | 不合格時の対応 |
|------|------|---------|---------------|
| S2: Fine-tune | SgTS overall | > 0 | τ調整、BalancedSampler適用 |
| S2: Fine-tune | 同極性類似度 $\bar{S}^+$ | > 0.7 | エポック数増加 |
| S2: Fine-tune | 異極性類似度 $\bar{S}^-$ | < 0.3 | lr調整 |
| S3: クラスタリング | Silhouette係数 | > 0.3 | min_cluster_size感度分析 |
| S3: クラスタリング | ノイズ比率 | < 20% | min_samples調整 |
| S3: クラスタリング | 感情純度 | > 0.70 | SentiCSE品質の再確認 |
| S3: クラスタリング | ペルソナ数 K | 5〜15 | パラメータ再調整 |
| S4: ペルソナ命名 | 命名一致率（3試行） | > 70% | プロンプト改善 |
| S4: ペルソナ命名 | 優先度 Jaccard | > 0.5 | Few-shot例追加 |
| S6: 関係分析 | 少なくとも1ペルソナとの相関 | \|r\| > 0.3, p < 0.05 | ラグ調整・稼働率計算法見直し |
| S6: 予測 | XGBoost R² (Prop-2) | > BL-3 かつ > 0.4 | 特徴量エンジニアリング強化 |
| S6: Granger | 少なくとも1ペルソナでの有意性 | p < 0.05 | 差分変換・max_lag調整 |

### 11.2 論文投稿想定誌と要求精度

| 投稿候補誌 | IF（2025推定） | 要求水準 | 本研究の対応可否 |
|-----------|-------------|---------|----------------|
| **Tourism Management** | 12.7 | ホスピタリティ × AI の方法論的新規性 | ✅ 対応可（W1〜W3が新規性） |
| **IJHM (Int. J. Hospitality Mgmt.)** | 10.9 | 実務的含意 + 定量根拠 | ✅ 対応可 |
| **Expert Systems with Applications** | 8.5 | AI/MLの技術的新規性 + 実証実験 | ✅ 対応可 |
| **ACM CIKM / EMNLP** | - | NLP技術の新規性（SentiCSE応用） | △ 競争激しい |

---

## 付録A: 環境構築チェックリスト

```bash
# 1. Python環境（conda推奨）
conda create -n senticse python=3.11 -y
conda activate senticse

# 2. PyTorchのインストール（CUDA 12.1の場合）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. 主要パッケージ
pip install transformers>=4.41.0 sentence-transformers>=3.0.0 datasets>=2.19.0
pip install umap-learn>=0.5.6 hdbscan>=0.8.33 pynndescent
pip install scikit-learn>=1.4.0 xgboost>=2.0.0 shap>=0.45.0
pip install statsmodels>=0.14.0 scipy>=1.12.0
pip install pandas>=2.2.0 numpy>=1.26.0 pyarrow fastparquet
pip install matplotlib>=3.8.0 seaborn>=0.13.0 plotly>=5.20.0
pip install ollama>=0.2.0 fasttext tqdm

# 4. Ollamaのインストールとモデルpull（ローカルLLM）
# https://ollama.com/ からインストーラーを入手
ollama pull qwen3:4b
ollama pull llama3.2:3b  # 英語口コミ向けサブ候補

# 5. fasttext言語判定モデルのダウンロード
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

# 6. GPU動作確認
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

## 付録B: 想定KPI一覧表

| KPI | 計算式 | 理想値 | 測定タイミング |
|-----|--------|--------|--------------|
| SgTS（感情embedding品質） | $\bar{S}^+ - \bar{S}^-$ | > 0.4 | Phase 2完了後 |
| Silhouette係数 | sklearn.metrics | > 0.3 | Phase 3完了後 |
| ノイズ率 | ノイズ点数 / 全点数 | < 0.2 | Phase 3完了後 |
| 感情純度 | クラスタ内支配感情比率 | > 0.70 | Phase 3完了後 |
| 命名一致率 | 3試行での同一名率 | > 0.70 | Phase 4完了後 |
| 相関係数（最大ペルソナ） | Pearson r | \|r\| > 0.30 | Phase 6完了後 |
| XGBoost R² (Prop-2 vs BL-3) | cross-val mean | Δ > 0.05 | Phase 6完了後 |
| Granger 有意性 | F検定 p値 | p < 0.05 | Phase 6完了後 |
| SentiCSE寄与度（SHAP） | ペルソナ特徴量 SHAP比率 | > 20% | Phase 6完了後 |

---

*このドキュメントは `sentiment_contrastive_persona_rd_plan.md` の補完的な技術詳細レビュー資料であり、各Stepの数理・実装・評価設計を深堀りしたものです。実装は計画書のコードベースと組み合わせて参照してください。*
