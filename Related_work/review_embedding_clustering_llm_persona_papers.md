# カテゴリ：口コミEmbedding × クラスタリング × LLM命名によるペルソナ生成研究

> 調査日: 2026年6月3日
> 調査テーマ: 口コミ（レビュー）テキストをBERT等でembedding化し、クラスタリングして集団を形成し、LLMにクラスタ名・ペルソナ名を命名させることで「口コミペルソナ」を生成する研究の存在調査

---

## 調査結論サマリー

**この研究アプローチは確かに存在しており、2023年〜2026年にかけて急速に研究が増加している。**

特定のパイプライン（①レビュー/UGCのBERT/LLM embedding → ②クラスタリング → ③LLMによるクラスタ命名/ペルソナ記述生成）を採用した研究が複数確認された。ただし、「ホテル口コミ」に特化したものは少なく、マーケティング（消費者調査）、HCI（UXデザイン）、コンテンツ制作支援の文脈で多く研究されている。

---

## 確認された主要論文・文献

---

## P1. Shin et al. (2024) — **最重要論文**

### ■ 参照情報

- **論文タイトル**: Understanding Human-AI Workflows for Generating Personas
- **著者**: Jeongkyu Shin, Michael A. Hedderich, Bruna John Rey, Antti Lucero, et al.
- **公開年**: 2024
- **掲載誌・学会**: Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems (ACM CHI 2024)
- **DOI**: https://doi.org/10.1145/3643834.3660729
- **URL**: https://dl.acm.org/doi/abs/10.1145/3643834.3660729
- **アクセス日**: 2026年6月3日（Scholar経由でabstract確認）
- **被引用数**: 74件（2026年6月時点）

---

### ■ 概要

- **研究の目的**: ペルソナ生成において、人間の専門家とLLMがどのように役割分担できるかを体系的に分析し、最適なHuman-AIワークフローを特定する。
- **解決しようとしている問題**: 従来のペルソナ生成は人間の専門家による手動分析（時間・コスト大）かLLM単独生成（データ根拠なし）のどちらかであり、両者を効果的に組み合わせる方法論が確立されていない。
- **提案手法の要点**: 複数のHuman-AIワークフローを比較実験し、「**LLM-summarizing**」モデル（人間がクラスタリングでユーザーグループを特定 → LLMがテキストをペルソナに要約）が最も効果的であることを示した。

---

### ■ 手法の全体構造（LLM-summarizingモデル）

- **Step 1**: ユーザーデータ（口コミ・発言・行動ログ等）の収集
- **Step 2**: テキストのBERT/Sentence-BERTによるembedding化
- **Step 3**: 人間専門家が**クラスタリング手法**（k-means等）を用いてユーザーグループを特定
- **Step 4**: 各クラスタのテキストをLLMに入力し、ペルソナ記述（名前・特性・行動傾向・ニーズ）を**自動生成**
- **Step 5**: 生成されたペルソナの評価（有用性・代表性・具体性）

---

### ■ 本研究との関連性

- ユーザー口コミ/発言テキスト → embedding → クラスタリング → LLMによるペルソナ命名・記述生成という**完全一致**するパイプラインを実証した論文。
- 「LLM-summarizing」モデルが人間のみ・LLMのみより優れることを定量的に示した点が重要。
- ホテル口コミへの直接適用例はないが、汎用的なフレームワークとして参照価値が高い。

---

## P2. Li, Liu & Yu (2025)

### ■ 参照情報

- **論文タイトル**: Consumer Segmentation with Large Language Models
- **著者**: Y. Li, Y. Liu, M. Yu
- **公開年**: 2025（掲載誌受理: 2024年）
- **掲載誌**: Journal of Retailing and Consumer Services（Elsevier）
- **DOI/URL**: https://www.sciencedirect.com/science/article/pii/S0969698924003746
- **アクセス日**: 2026年6月3日（Scholar経由でabstract確認）
- **被引用数**: 37件（2026年6月時点）

---

### ■ 概要

- **研究の目的**: マーケティングリサーチにおける消費者セグメンテーションへのLLM適用可能性の実証。
- **解決しようとしている問題**: 従来の消費者セグメンテーション（アンケート + 統計的クラスタリング）は、テキスト形式の自由回答データや複合的な選択肢データの扱いが弱い。
- **提案手法の要点（2段階アプローチ）**:
  1. **LLMモデルでテキストをembedding化**してクラスタリングを実行（従来モデルより高精度を実証）
  2. 各クラスタの特性からLLMが**ペルソナチャットボット**を生成し、マーケティング担当者がそのペルソナと対話できるシステムを構築

---

### ■ 手法の要点

- **入力データ**: 消費者調査データ（テキスト形式の多選択・自由回答）
- **Embedding**: LLMベースのテキストembedding（BERT系モデル）
- **クラスタリング**: k-meansまたは階層的クラスタリング
- **ペルソナ生成**: 各クラスタの代表テキストをLLMに入力し、消費者ペルソナ（属性・ニーズ・価値観）を記述・チャットボット化
- **評価**: クラスタリング精度（シルエット係数等）＋ペルソナの有用性

---

### ■ 本研究との関連性

- テキストデータのLLM embedding → クラスタリング → ペルソナ生成チャットボットという**完全一致**するパイプライン。
- 消費者レビューではなく調査データが対象だが、手法は直接転用可能。
- 「LLMのembeddingが従来BERT系より高精度」という知見は、ホテル口コミペルソナ生成に適用する際のモデル選択根拠になる。

---

## P3. Choi et al. (2025) — Proxona

### ■ 参照情報

- **論文タイトル**: Proxona: Supporting Creators' Sensemaking and Ideation with LLM-Powered Audience Personas
- **著者**: Yoonseo Choi, Eun Jeong Kang, Seulgi Choi, Min Kyung Lee, Juho Kim
- **公開年**: 2025
- **掲載誌・学会**: Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems (ACM CHI 2025)
- **DOI**: https://doi.org/10.1145/3706598.3714034
- **URL**: https://dl.acm.org/doi/abs/10.1145/3706598.3714034
- **アクセス日**: 2026年6月3日（Scholar経由でabstract確認）
- **被引用数**: 46件（2026年6月時点）

---

### ■ 概要

- **研究の目的**: YouTubeクリエイターが自分のオーディエンスを理解し、コンテンツ制作のアイデア出しを支援するためのLLMペルソナシステムの設計・評価。
- **解決しようとしている問題**: クリエイターは視聴者コメント（大量のUGC）を分析する時間やリソースがなく、オーディエンスの多様な特性を把握できていない。
- **提案手法の要点**: YouTubeコメントを**embedding化 → クラスタリング**して多様で代表的なオーディエンスグループを抽出し、各クラスタをLLMが**プロトタイピカル・ペルソナ**として命名・記述。クリエイターはペルソナと対話してコンテンツ戦略を検討できる。

---

### ■ 手法の全体構造

- **Step 1**: YouTubeコメント（レビュー相当のUGC）の大量収集
- **Step 2**: コメントのSentence-BERT / LLMによるembedding化
- **Step 3**: クラスタリング（具体的アルゴリズムは論文参照）で多様なオーディエンスグループを形成
- **Step 4**: 各クラスタの代表コメント群をLLMに入力し、ペルソナ名・特性・関心・動機を含む**ペルソナ記述を自動生成**
- **Step 5**: クリエイターがペルソナと対話（チャット）してアイデア検証

---

### ■ 本研究との関連性

- **コメント/口コミのembedding → クラスタリング → LLMによるペルソナ命名・記述**という構造が、ホテル口コミペルソナ生成と**ほぼ同一**。
- 「オーディエンスペルソナ」の生成評価方法論（ユーザースタディ）が参考になる。
- コメントという短文UGCを対象にしており、ホテル口コミとデータ特性が近い。

---

## P4. Yin, Liu, Lian & Cai (2026) — CoPersona

### ■ 参照情報

- **論文タイトル**: CoPersona: Leveraging LLMs and Expert Collaboration to Understand User Personas Through Social Media Data Analysis
- **著者**: M. Yin, H. Liu, B. Lian, R. Cai
- **公開年**: 2026
- **掲載誌**: Design for Augmented Intelligence（SAGE Journals）
- **DOI/URL**: https://journals.sagepub.com/doi/abs/10.1177/29776481261426454
- **アクセス日**: 2026年6月3日（Scholar経由でabstract確認）
- **被引用数**: 3件（2026年6月時点、最新論文）

---

### ■ 概要

- **研究の目的**: SNSデータからのデータドリブン・ペルソナ開発において、LLMと専門家が協調するフレームワーク（CoPersona）の構築。
- **解決しようとしている問題**: 大量のSNSデータからペルソナを生成する際、完全自動化は品質に課題があり、完全人手は非効率。LLM-専門家協調による最適バランスの確立が求められる。
- **提案手法の要点**:
  - SNS投稿のembedding化（cosine similarityベースの類似度計算も活用）
  - **エルボー法**で最適クラスタ数を決定し、ユーザーグループを形成
  - LLMにクラスタ内テキストを与え、ペルソナを命名・記述生成
  - 専門家が結果を検証・修正する**Human-in-the-Loop**設計
  - 5つの異なるユーザーペルソナを同定したことを報告

---

### ■ 本研究との関連性

- SNS投稿という口コミ類似データ → embedding → クラスタリング（エルボー法） → LLMによるペルソナ命名という**直接的に一致**するパイプライン。
- 「コスト・リソース制約下でのペルソナ生成」という実用的文脈が、旅館・ホテル業での実装と親和性が高い。
- Human-in-the-Loopの設計思想はホテル実務担当者との協働設計に応用可能。

---

## P5. Amin, Salminen et al. (2025/2026) — Scoping Review

### ■ 参照情報

- **論文タイトル**: Creating and Evaluating Personas Using Generative AI: A Scoping Review of 81 Articles
- **著者**: Danial Amin, Joni Salminen, Farhan Ahmed, Sonja M.H. Tervola, Sankalp Sethi, Bernard J. Jansen
- **公開年**: 2025（arXiv v1: 2025年4月）/ 2026（ACM CHI 2026発表）
- **掲載誌・学会**: Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems
- **arXiv**: https://arxiv.org/abs/2504.04927
- **関連DOI**: https://doi.org/10.1145/3772318.3790608
- **アクセス日**: 2026年6月3日（全文abstract確認）
- **被引用数**: 31件（arXiv版、2026年6月時点）

---

### ■ 概要（サーベイ論文として参照価値が高い）

- **調査範囲**: 2022〜2025年に発表された生成AI活用ペルソナ開発論文81本を体系的に分析
- **主要知見**:
  1. データドリブン・ペルソナ開発の典型的パイプラインは「データ収集 → クラスタリングによるセグメント特定 → LLMによるペルソナ記述生成」
  2. LLMの役割として「クラスタへの命名・ラベリング」「ペルソナナラティブ記述」が主流
  3. ペルソナ生成でLLMを活用する研究の86%がGPTモデルを使用
  4. 45%の論文が評価方法を欠いており、評価方法論の確立が今後の課題
  5. **マーケティング文脈（n=7, 8.6%）ではテキストembedding + クラスタリング + LLMによる消費者セグメンテーション**が行われていることを確認
- **本研究で引用される主要パイプライン**: Shin et al. (2024) の「LLM-summarizing」モデルが繰り返し参照される

---

### ■ 本研究との関連性

- 「口コミペルソナ生成」研究の文献的根拠として、この分野の研究動向・標準的手法・課題を俯瞰するための**最重要サーベイ**。
- 関連研究の節で引用し、提案手法の位置付けを明確化するために使用できる。

---

## P6. Zanutto (2023) — IKEAプロダクトレビュー + BERTopic + LLM命名

### ■ 参照情報

- **論文タイトル**: Leveraging LLM-Generated Keyphrases and Clustering Techniques for Topic Identification in Product Reviews
- **著者**: D. Zanutto
- **公開年**: 2023
- **掲載誌・機関**: Politecnico di Milano（修士論文）
- **URL**: https://www.politesi.polimi.it/handle/10589/227476
- **アクセス日**: 2026年6月3日（Scholar経由でabstract確認）
- **被引用数**: 1件（2026年6月時点）

---

### ■ 概要

- **研究の目的**: IKEAのプロダクトレビュー群から、LLMが生成したキーフレーズとBERT embeddingを活用したクラスタリングでトピックを自動抽出する。
- **提案手法の要点**:
  - BERT embeddingで口コミをベクトル化
  - クラスタリング（BERTopicおよびLDA等と比較）でレビュー群を集団化
  - **クラスタの重心に最も近いキーフレーズをクラスタ名として自動選択**（LLM生成キーフレーズを使用）
  - 結果としてトピック（ペルソナに準ずるセグメント）に名称を付与

---

### ■ 本研究との関連性

- プロダクトレビューという**口コミデータ**に対してBERT embedding + クラスタリング + LLM命名を適用した直接的な事例。
- ホテル口コミペルソナ生成のパイロット的な先行研究として参照価値がある。
- クラスタ命名の方法（重心近傍キーフレーズ vs. LLMによる自由記述命名）の比較視点を提供。

---

## 調査から得られた技術的知見

### ■ 確立されているパイプラインの標準形

```
[口コミ/レビュー/UGC収集]
        ↓
[BERT / Sentence-BERT / LLM embedding]
        ↓
[クラスタリング（k-means / HDBSCAN / 階層的）]
    ※ エルボー法・シルエット係数でk決定
        ↓
[各クラスタをLLMに入力]
        ↓
[LLMがクラスタに「ペルソナ名」「属性記述」「行動特性」を命名・生成]
        ↓
[口コミペルソナ群（データドリブン・ペルソナ）の完成]
```

### ■ BERTのEmbedding：事前学習の仕組みとFine-tuneの関係

本研究パイプラインでは「BERT/Sentence-BERTによるembedding」が基盤となるが、**どの学習段階のBERTを使うかで得られるベクトルの性質が大きく異なる**。

#### (1) 標準BERTの事前学習（Pre-training）

BERT（Devlin et al., 2019）は以下の2タスクで大規模コーパスから**教師なし**に事前学習される：

| タスク | 内容 | 学習される能力 |
|--------|------|---------------|
| **MLM（Masked Language Model）** | 入力トークンの15%をランダムにマスクし、元のトークンを予測 | 文脈依存の語義・構文関係 |
| **NSP（Next Sentence Prediction）** | 2文が連続するか否かを分類 | 文間の意味的接続性 |

- 学習コーパス: 原著はBooksCorpus + English Wikipedia（日本語版 cl-tohoku/bert-base-japanese は日本語Wikipediaで学習）
- 出力: 各トークンの文脈依存ベクトル（768次元）。`[CLS]`トークンのベクトルが文全体の要約表現として使われる
- **感情判定の学習は一切含まれない** → Positive/Negativeの軸ではなく、**語義的・文脈的類似性**の軸でベクトルが分布する

#### (2) Sentence-BERT（SBERT）のFine-tune

Sentence-BERT（Reimers & Gurevych, 2019）は、BERTをNLI（自然言語推論）データセットで**Contrastive Learning**によって追加学習する：

- 学習データ: 「含意（entailment）」ペアを近く、「矛盾（contradiction）」ペアを遠くなるようにコサイン類似度空間を調整
- 目的: 文レベルの意味的類似度が**コサイン距離に直接対応**するembeddingを獲得
- **感情の0/1ラベルでのFine-tuneはしていない** → クラスタリングに適した「意味的近さ」を表すベクトル空間になる
- 多言語版: `paraphrase-multilingual-mpnet-base-v2` は日本語を含む50言語対応

#### (3) 感情分類Fine-tuned BERT（例: koheiduck/bert-japanese-finetuned-sentiment）

感情ラベル付きデータで`[CLS]`の後ろに分類ヘッドを追加してFine-tuneされたモデル：

- 出力: **クラス確率**（Positive/Neutral/Negativeの確率値） → これは感情分類器の出力であってembeddingではない
- `[CLS]`の**隠れ状態（hidden state）**は感情分類に最適化されているため、クラスタリング用embeddingとして使うと「感情極性（±）」に過剰適合したクラスタが生まれる恐れがある
- 本研究の用途: 感情分類（ABSA Step 2）にはこのモデルを使う。**ペルソナ生成用のクラスタリングには使わない**

#### (4) 本研究での使い分け方針

| 用途 | 使用モデル | 理由 |
|------|-----------|------|
| **ペルソナ生成のclustering用embedding** | `paraphrase-multilingual-mpnet-base-v2`（SBERT）または `cl-tohoku/bert-base-japanese-v3` | 意味的類似性を捉えたクラスタ形成のため |
| **ABSAの感情分類** | `koheiduck/bert-japanese-finetuned-sentiment` | 感情ラベルでFine-tune済みのため |
| **長文口コミのembedding** | SBERT + sliding window → 平均プーリング | 512トークン制限を超える口コミへの対応 |

> **結論**: 本パイプラインで使うBERT embeddingは「感情0/1でFine-tuneされていない」一般意味空間のベクトルが基本。感情Fine-tuneモデルはABSAの分類ヘッドとして別途使う。

---

### ■ ホテル口コミへの直接適用例の空白

- 上記パイプラインをそのままホテル口コミ（TripAdvisor / Booking.com）に適用し、「ホテル利用者ペルソナ」を体系的に生成・評価した論文は現時点（2026年6月）では**確認されていない**。
- これは研究の**新規性ギャップ**として位置付け可能。

### ■ 関連する技術選択肢

| 要素 | 主要選択肢 | 備考 |
|------|-----------|------|
| Embeddingモデル | Sentence-BERT, OpenAI text-embedding-3, LLMベース | LLMベースがクラスタ品質で優位（Li et al., 2025） |
| クラスタリング | k-means, HDBSCAN, BERTopic | BERTopicはトピックモデリング色が強い |
| クラスタ数決定 | エルボー法, シルエット係数 | CoPersona (Yin et al., 2026) ではエルボー法を採用 |
| LLMによる命名 | GPT-4, GPT-3.5-turbo | 86%の研究がGPTモデルを使用 |
| 評価方法 | ユーザースタディ, クラスタ品質指標 | 45%の研究が評価方法を欠くという問題あり |

---

## 参考：関連する周辺研究

| 論文 | 概要 | 関連度 |
|------|------|--------|
| Petukhova et al. (2025), *Int. J. Data Science* | LLM embeddingによるテキストクラスタリング比較（128件引用） | ★★★ |
| Amin et al. (2026), *CHI*, arXiv:2504.04927 | 生成AIペルソナ開発の体系的サーベイ81本 | ★★★ |
| Shin et al. (2024), *ACM CHI* | Human-AIペルソナ生成ワークフロー（74件引用） | ★★★ |
| Choi et al. (2025), *ACM CHI* | Proxonaシステム（コメント→embedding→クラスタ→LLMペルソナ） | ★★★ |
| Li, Liu, Yu (2025), *J. Retailing* | LLM embedding+クラスタリング+ペルソナチャットボット生成 | ★★★ |
| Yin et al. (2026), *Design for Aug. Intel.* | CoPersona: SNS+embedding+クラスタ+LLM命名（エルボー法） | ★★★ |
| Zanutto (2023), *Politecnico di Milano* | IKEAレビュー+BERT+クラスタリング+LLM命名 | ★★☆ |
| Spielhofer (2025), *FH CAMPUS 02* | トピックモデリング+感情分析によるデータドリブン・ペルソナ生成 | ★★☆ |
| Kim et al. (2024), *LREC-COLING* | SentiCSE: 感情極性Contrastiveによる感情aware文embedding | ★★★ |
| Khosla et al. (2020), *NeurIPS* | Supervised Contrastive Learning（SupConLoss）: ラベル教師ありContrastive損失の基礎論文 | ★★★ |
| Gao et al. (2021), *EMNLP* | SimCSE: NLI含意/矛盾ペアを正・負例にしたContrastive文embedding | ★★★ |
| Mohanty et al. (2021), *arXiv* | 感情ベースのContrastive表現学習：DynaSentでBERT超え | ★★☆ |

---

## 技術補足カテゴリ：感情Contrastive Embedding ×ペルソナ生成

> 調査日: 2026年6月3日
> テーマ: 感情極性（Positive/Negative/Neutral）を教師信号にしたContrastive Learningで文embeddingを訓練し、そのembedding空間でペルソナ生成クラスタリングを行う研究の存在調査

---

## C1. Kim, Na, Kim, Lee & Chae (2024) — **SentiCSE（最重要・直接参照）**

### ■ 参照情報

- **論文タイトル**: SentiCSE: A Sentiment-aware Contrastive Sentence Embedding Framework with Sentiment-guided Textual Similarity
- **著者**: Jaemin Kim, Yohan Na, Kangmin Kim, Sang Rak Lee, Dong-Kyu Chae
- **公開年**: 2024
- **掲載誌・学会**: LREC-COLING 2024
- **arXiv**: https://arxiv.org/abs/2404.01104
- **GitHub**: https://github.com/nayohan/SentiCSE
- **アクセス日**: 2026年6月3日

---

### ■ 概要

- **解決しようとしている問題**: 既存の感情認識PLM（Pre-trained Language Model）は分類精度を高めることに特化しており、embedding空間自体の品質が保証されていない。つまり同じ感情の文が近く、異なる感情の文が遠いという「感情軸での幾何学的整合性」が欠如している。
- **提案手法1 — SgTS（Sentiment-guided Textual Similarity）**: 2文の感情極性の一致度を指標とした新しい類似度評価指標。同極性ペアの類似度が高く、異極性ペアの類似度が低いほどembedding品質が高いと評価する。
- **提案手法2 — SentiCSE**: SimCSEの枠組みを拡張し、**感情ラベルを正例・負例の決定基準**として使う感情aware Contrastive学習。単語レベル＋文レベルの複合的なContrastive目的関数を採用。

---

### ■ SentiCSEの学習メカニズム

```
正例ペア（同じ感情極性）:
  x_i = 「部屋がきれいで最高でした」   ← Positive
  x_j = 「清掃が行き届いていて快適」   ← Positive
  → embedding空間で距離を縮める

負例ペア（異なる感情極性）:
  x_i = 「部屋がきれいで最高でした」   ← Positive
  x_k = 「部屋が狭くて残念でした」     ← Negative
  → embedding空間で距離を広げる

損失関数（文レベルContrastive）:
  L = -log( exp(sim(h_i, h_j)/τ) / Σ_k exp(sim(h_i, h_k)/τ) )

  h_i, h_j: 同極性ペアのCLSベクトル
  h_k: 異極性テキストのCLSベクトル
  τ: 温度パラメータ（通常0.05〜0.1）
```

---

### ■ 結果

- SgTS（感情embedding品質）で既存感情認識PLM群を上回ることを定量的に実証
- SST-2, SST-5, MR, SemEval等のダウンストリーム感情分析タスクでも改善
- 感情極性が異なる文のコサイン類似度が大幅に下がり、**クラスタリング時の感情純度が向上**

---

### ■ 本研究（ホテル口コミペルソナ）への直接適用

- SentiCSEの学習方式を日本語ホテル口コミに適用する：
  - 正例: 同じアスペクトの同じ感情極性の口コミペア（食事Positive同士）
  - 負例: 同じアスペクトの異なる感情極性の口コミペア（食事Positiveと食事Negative）
- 結果として「**食事に満足した宿泊者**」「**食事に不満な宿泊者**」がembedding空間で自然分離
- クラスタリング後のペルソナが「何に感じたか」の感情軸でも定義される

> **研究空白**: SentiCSEはSSTやSemEvalなど標準英語ベンチマークのみを対象。日本語ホテル口コミへの適用・ペルソナ生成への応用は**前例なし**。

---

## C2. Khosla et al. (2020) — Supervised Contrastive Learning（SupConLoss 基礎論文）

### ■ 参照情報

- **論文タイトル**: Supervised Contrastive Learning
- **著者**: Prannay Khosla, Piotr Teterwak, Chen Wang, Aaron Sarna, Yonglong Tian, Phillip Isola, Aaron Maschinot, Ce Liu, Dilip Krishnan
- **公開年**: 2020（NeurIPS 2020）
- **arXiv**: https://arxiv.org/abs/2004.11362
- **被引用数**: 10,000件超（2026年6月時点）

---

### ■ 概要

- 自己教師ありContrastive学習（SimCLR等）を**ラベルあり教師あり設定に拡張**した基礎論文。
- **SupCon損失**: 同クラスのサンプルを複数同時に正例として扱い、embedding空間で同クラスを密集・異クラスを分離する。

```
SupCon Loss:
  L_sup = -Σ_{i∈I} (1/|P(i)|) Σ_{p∈P(i)} log(
      exp(z_i · z_p / τ)
      / Σ_{a∈A(i)} exp(z_i · z_a / τ)
  )

  P(i): i と同じラベルのサンプル集合（複数正例）
  A(i): バッチ内の i 以外の全サンプル（負例を含む）
```

- ImageNetでResNet-200が81.4%（クロスエントロピーを0.8%上回る）
- **本研究での役割**: SentiCSEの感情Contrastive損失設計の直接的な理論基盤として引用

---

## C3. Gao, Yao & Chen (2021) — SimCSE（Contrastive文embedding の基礎）

### ■ 参照情報

- **論文タイトル**: SimCSE: Simple Contrastive Learning of Sentence Embeddings
- **著者**: Tianyu Gao, Xingcheng Yao, Danqi Chen
- **公開年**: 2021（EMNLP 2021）
- **arXiv**: https://arxiv.org/abs/2104.08821
- **被引用数**: 5,000件超（2026年6月時点）

---

### ■ 概要

- **教師なしSimCSE**: 同一文を2回Dropoutで微妙に変えて正例ペアを作り、バッチ内他文を負例としてContrastive学習。
- **教師ありSimCSE**: NLIデータセットの「含意（entailment）」ペアを正例、「矛盾（contradiction）」ペアをハード負例として使用。
  - 含意 ≈ 同じ意味 → 正例
  - 矛盾 ≈ 相反する意味 → ハード負例
- STSベンチマークでSpearman相関81.6%（BERT-baseモデル）を達成。

---

### ■ SentiCSEとの関係・本研究での役割

```
SimCSE（NLI基準） → SentiCSE（感情極性基準）への発展:

  SimCSE正例: 含意ペア（「犬が走っている」→「動物が動いている」）
              ← 意味的等価性で決定
  
  SentiCSE正例: 同極性ペア（Positive口コミ × Positive口コミ）
              ← 感情極性の一致で決定

  違い: SentiCSEは「感情空間」での近接性を最適化する
```

- **本研究での役割**: 感情Contrastive embeddingパイプラインのアーキテクチャ基盤として引用

---

## C4. Mohanty, Goyal & Dotterweich (2021)

### ■ 参照情報

- **論文タイトル**: Emotions are Subtle: Learning Sentiment Based Text Representations Using Contrastive Learning
- **著者**: Ipsita Mohanty, Ankit Goyal, Alex Dotterweich
- **公開年**: 2021
- **arXiv**: https://arxiv.org/abs/2112.01054

---

### ■ 概要

- コンピュータビジョン領域で主流だったContrastive学習手法をNLPの**感情分析タスクに拡張**した初期研究の一つ。
- BERTベースのembeddingに対しContrastive fine-tuneを行い、DynaSentデータセットでBERT単体を上回ることを実証。
- 異なるドメイン（クロスドメイン）での感情分類でも精度改善を確認。

---

### ■ 本研究との関連性

- 感情Contrastive embeddingがクロスドメインに転用できることを示した点が重要。
- ホテル口コミ（ドメイン固有データ）で訓練したSentiCSE式embeddingが他施設・他地域に汎化できる根拠として引用可能。

---

## 感情Contrastive Embedding研究の調査結論

### ■ 確立された技術スタック（2021〜2024）

```
技術系譜:

  Khosla et al. 2020 (SupConLoss)          ← 教師ありContrastive損失の定式化
         ↓
  Gao et al. 2021 (SimCSE)                ← 文レベルContrastive embeddingに拡張
         ↓
  Kim et al. 2024 (SentiCSE)              ← 感情極性を基準にしたContrastive embedding
         ↓
  【本研究の提案】                          ← ホテル口コミ × 感情Contrastive × ペルソナ生成
  SentiCSE式日本語ホテル口コミ embedding
  → 感情軸でクラスタリング
  → 「清掃に厳しいゲスト」「食事に感激するゲスト」等の感情定義ペルソナを生成
```

### ■ 研究空白（新規性の根拠）

| 空白 | 既存研究の限界 | 本研究の貢献 |
|------|-------------|------------|
| 日本語対応 | SentiCSEは英語のみ | 日本語ホテル口コミへの適用 |
| ペルソナ生成への連結 | Contrastive embeddingでペルソナを作った研究なし | embedding → クラスタ → LLMペルソナ命名 |
| アスペクト × 感情の複合 | 感情全体の極性のみを扱う | 10アスペクト別の感情軸を組み合わせた複合embedding |
| ホテル稼働率との結合 | いずれの研究も稼働率を扱わない | 感情定義ペルソナ → 稼働率への影響分析 |
