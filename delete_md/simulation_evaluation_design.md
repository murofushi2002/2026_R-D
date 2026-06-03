# シミュレーション評価設計書：口コミ活用型価格決定支援エージェントの検証方法論

---

## 背景と制約

| 項目 | 内容 |
|------|------|
| **研究対象** | 地方宿泊施設を対象とした口コミベース価格決定支援エージェント |
| **現有資産** | ABSA パイプライン, 需要予測モデル（清掃スコア追加で精度向上を確認済） |
| **想定アーキテクチャ** | 候補A（LLM-as-Pricing-Advisor）+候補D要素（ヘドニック分析） |
| **重要制約** | **現場マネージャーへのユーザスタディは実施不可** |

本文書では、「フィールド実験なしでも学術的・実務的に納得感のある評価」をどのように設計するかを、文献根拠とともに定義する。

---

---

## 第1章　評価設計の全体方針 — 5層評価フレームワーク

現場マネージャーがいなくても成立する評価体系を、**5つの独立した評価層**として構成する。各層は異なる「問い」に答え、相互に補完し合う。

```
┌───────────────────────────────────────────────────────────────────┐
│  Layer 5: 経済性・感度分析        "どの程度の収益改善が期待できるか"     │
├───────────────────────────────────────────────────────────────────┤
│  Layer 4: 説明品質評価            "生成された根拠説明は妥当か"          │
├───────────────────────────────────────────────────────────────────┤
│  Layer 3: 価格推薦精度            "推薦価格は実勢と整合するか"          │
├───────────────────────────────────────────────────────────────────┤
│  Layer 2: ABSA → 需要予測精度     "ABSAの追加で予測は改善するか"        │
├───────────────────────────────────────────────────────────────────┤
│  Layer 1: ABSAモジュール精度      "個々のaspect抽出・感情分類は正確か"   │
└───────────────────────────────────────────────────────────────────┘
```

**設計原則**: 上層の評価が主観的になりやすいものこそ、複数の独立した評価軸（三角測量; triangulation）を設ける（Mangold et al., 2025）。

---

---

## 第2章　Layer 1 — ABSAモジュール精度

### 2-1. 検証の問い
> 宿泊施設口コミから aspect（清掃, 朝食, 立地, 接客 等）と sentiment を正しく抽出できるか？

### 2-2. 評価方法

| 手法 | 指標 | 説明 |
|------|------|------|
| **ゴールドスタンダード評価** | F1, Precision, Recall（aspect抽出）; Accuracy, Macro-F1（感情分類） | 手動アノテーション済みテストセットとの比較。Liskowski & Jankowski (2026) は Arctic-ABSA で 5クラス感情分類の F1 を SemEval データセット上で評価（SoTA達成） |
| **クラス別評価** | クラス別 F1 | 5段階感情分類（強ポジ/ポジ/中立/ネガ/強ネガ）で各クラスの精度偏りを確認 |
| **ドメイン適応評価** | ドメイン固有テストセットでの F1 | 日本語宿泊口コミ専用のテストセット（200〜500件手動アノテーション）を用意し、汎用モデルとの差分を測定。Tran & Tran (2026) はベトナムのホテル口コミでドメイン固有 BiLSTM を構築し、汎用モデルとの比較を実施 |

### 2-3. アノテーション設計

- **サンプルサイズ**: 最低300件（×2名のアノテータ）
- **一致度指標**: Cohen's κ ≥ 0.7 を目標
- **参考**: Öztürk (2026) は14五つ星ホテルの2022–2024年口コミからaspect-sentiment driver を抽出し、解釈可能なルールマイニングで評価

### 2-4. 根拠文献

- Liskowski, P. & Jankowski, N. (2026). Arctic-ABSA: Aspect-Based Sentiment Analysis with Arctic Foundation Models. *arXiv:2505.02780*.
- Tran, T.K. & Tran, P. (2026). Aspect-based Sentiment Analysis in Ho Chi Minh city Hotel Reviews using Aspect-Conditioned BiLSTM. *IEEE Access*.
- Öztürk, A.C. (2026). Discovering Aspect-Sentiment Drivers of Hotel Review Ratings via Interpretable High-Utility Rules. *IEEE Access*.
- Jeong, M. & Lee, S.A. (2024). Exploring the impact of ChatGPT on hotel customer experience. *Int. J. Contemp. Hosp. Manag.* (被引用43件).

---

---

## 第3章　Layer 2 — ABSA感情スコアの需要予測への貢献（アブレーション研究）

### 3-1. 検証の問い
> ABSA由来の観点別感情スコアを追加することで、需要予測精度はどの程度改善するか？

### 3-2. 評価方法 — 系統的アブレーション設計

**フィールド実験なしに最も強い因果的主張を可能とする手法**がアブレーション研究である。以下の段階的入力変数を比較する。

| モデルID | 入力変数 | 期待される役割 |
|---------|---------|--------------|
| **M0** | 構造化データのみ（カレンダー、曜日、稼働率、ADR） | ベースライン |
| **M1** | M0 + 総合レビュースコア | 総合スコアの情報量を確認 |
| **M2** | M0 + aspect別感情スコア（全aspect） | ABSA の aspect 分解の付加価値 |
| **M3** | M0 + aspect別感情スコア（SHAP上位3 aspect のみ） | 次元削減の効果 |
| **M4** | M0 + aspect別感情スコア + 時系列トレンド | トレンド情報の付加価値 |
| **M5** | M0 + aspect別感情スコア + キーフレーズ埋め込み | テキスト情報の直接利用の効果 |

### 3-3. 指標

| 指標 | 用途 |
|------|------|
| RMSE, MAE, MAPE | 点予測の精度比較 |
| R² | 説明力の比較 |
| Diebold-Mariano 検定 | M0 vs M2, M2 vs M4 等のペアワイズ有意差検定 |
| SHAP feature importance | 各 aspect の importance ランキングを可視化し、どの aspect が最も予測に貢献するかを同定 |

### 3-4. 実験プロトコル

- **時系列分割**: 学習 60% / 検証 20% / テスト 20%（time-series split, 情報リーク防止）
- **複数モデル**: XGBoost, LightGBM, GRU の3手法で評価し、特定モデルへの依存を排除
- **複数施設**: 最低3施設以上で cross-property 汎化性を確認

### 3-5. 根拠文献

- Degife, W. & Lin, X. (2024). ABSA + GRU による需要予測で、aspect スコアの追加を ablation 研究で評価（R² 比較）
- Saitta, E., D'Amico, S. & Farinella, G.M. (2024). Hotel Dynamic Pricing Predictions with SHAP. — SHAP による特徴量重要度評価を価格予測に適用
- Aggarwal, K. (2025). Tree models + SHAP for demand/price optimization — 透明性のある評価フレームワーク
- Wu, Y. et al. (2022). Sentiment-enhanced demand forecasting — 時系列評価指標の定義

---

---

## 第4章　Layer 3 — 価格推薦精度（ヒストリカル・リプレイ評価）

### 4-1. 検証の問い
> システムが提案する推薦価格は、実際の市場価格・取引価格と比較して妥当か？

### 4-2. 評価方法

#### 方法A：ヒストリカル・バックテスト（Historical Replay）

過去のデータを時系列で「再生」し、各時点でシステムの推薦価格を生成する。これを実際に設定されていた価格・結果と比較する。

```
過去データ [2023/01 ─── 2024/06]
              │
              ▼
   t=1 から t=T まで順次シミュレーション
              │
   各時点で: 口コミ + 構造化データ → エージェント → 推薦価格 p̂ₜ
              │
   比較: p̂ₜ vs 実際の設定価格 pₜ﹐ vs 市場の中央値
```

| 指標 | 定義 | 意味 |
|------|------|------|
| **MAE(price)** | mean(\|p̂ₜ − pₜ\|) | 推薦価格と実勢の乖離 |
| **方向一致率** | % of t where sign(p̂ₜ − pₜ₋₁) = sign(pₜ − pₜ₋₁) | 「上げるべきときに上げたか」 |
| **RevPAR シミュレーション** | 推薦価格 × シミュレーション稼働率 | 推定収益の比較 |
| **妥当価格帯率** | % of t where p̂ₜ ∈ [p₅th, p₉₅th] (市場分布) | 推薦が市場外れ値でないことの確認 |

#### 方法B：反実仮想（Counterfactual）シミュレーション

需要モデルを用いて「もし推薦価格を採用していたら」の仮想シナリオを推定する。

- **需要関数の推定**: 過去データからロジスティック関数 $F_i(p_{t,i}) = 1 / (1 + e^{\beta(p-\mu)})$ をfitting（Wang et al., 2025 参照）
- **反実仮想収益**: $\hat{R}_{cf} = \sum_t \hat{D}(p̂_t) \cdot p̂_t$ vs $R_{actual} = \sum_t D_t \cdot p_t$
- **感度分析**: 需要弾力性パラメータ $\beta$ を ±20% 変動させ、結果のロバスト性を確認

#### 方法C：ベンチマーク政策比較

| 比較対象 | 内容 |
|---------|------|
| **固定価格** | 期間平均価格を常に使用 |
| **曜日・季節ルール** | 経験則パターン（休日+20%、閑散期-15% 等） |
| **単純ML** | 需要予測値のみで価格設定（ABSA情報なし） |
| **提案手法** | ABSA+需要予測+LLMアドバイザー |

### 4-3. 根拠文献

- Wang, X. et al. (2025). A Two-Stage DRL-Driven Dynamic Discriminatory Pricing Model for Hotel Rooms with Fairness Constraints. *J. Theor. Appl. Electron. Commer. Res.*, 20(4), 337. — ホテル客室のシミュレーション環境構築: Poisson分布の顧客到着、ロジスティック価格受容関数、30日間エピソードの設計を詳細に記述。本研究のシミュレーション環境構築の主要参考文献
- Garcia, D., Tolvanen, J. & Wagner, A.K. (2022). Demand estimation using managerial responses to automated price recommendations. *Management Science*. (被引用30件) — 価格推薦に対するマネージャーの反応を推定し、推薦と実績の乖離分析手法を示す。実マネージャーへのアクセスがなくても、履歴データ上で「推薦 vs 実際」の分析が可能であることの先例
- Tang, J. et al. (2025). Offline feature-based pricing under censored demand: A causal inference approach. *Manufacturing & Service Operations Management*. (被引用21件) — 打ち切りデータ下のオフライン価格最適化手法。オフラインデータからの価格政策学習を理論的に正当化
- Fisher, M., Gallino, S. & Li, J. (2018). Competition-based dynamic pricing in online retailing: A methodology validated with field experiments. *Management Science*. (被引用285件) — 小売のDPでシミュレーション→フィールド実験の2段階評価を提唱。本研究はシミュレーション段階に相当
- Bayoumi, A.E.M. et al. (2013). Dynamic pricing for hotel revenue management using price multipliers. — Monte Carlo シミュレータによる価格乗数最適化の先例
- Li, L. (2026). The Application of Adaptive Reinforcement Learning in Dynamic Pricing Strategies. *Informatica*. — Kaggle ホテルデータセットでDPのベンチマーク評価を実施

---

---

## 第5章　Layer 4 — 説明品質評価（ユーザスタディ代替手法）

### 5-1. 検証の問い
> LLMが生成した価格根拠説明は、妥当で、理解可能で、有用か？

**これが最大の難所**：通常、説明品質はエンドユーザ（ここでは施設マネージャー）のユーザスタディで評価するが、本研究ではそれが不可能。以下の代替手法を組み合わせる。

### 5-2. 評価方法

#### 方法A：LLM-as-Judge（自動評価）

LLM自身を「評価者」として使い、生成された説明の品質を多次元で採点する。

**評価ルーブリック（5次元）**:

| 次元 | 定義 | 評点尺度 |
|------|------|---------|
| **事実整合性** (Factual Consistency) | 説明文がABSA結果・需要予測値と矛盾しないか | 1-5 |
| **根拠の具体性** (Evidence Specificity) | 「口コミで清掃が低評価」等の具体的根拠が含まれるか | 1-5 |
| **行動可能性** (Actionability) | マネージャーが取れる具体的行動が示唆されるか | 1-5 |
| **論理構造** (Logical Coherence) | 「原因→影響→推薦」の論理が一貫しているか | 1-5 |
| **簡潔性** (Conciseness) | 冗長でなく、要点が伝わるか | 1-5 |

**実装手順**:
1. 評価対象の「（入力データ, 推薦価格, 根拠説明）」トリプルを100件以上生成
2. GPT-4o 等の強力なLLMを Judge として使用（生成LLMとは異なるモデルを推奨）
3. 各次元について 1-5 で採点させる
4. 次元別スコアの平均・分布を報告
5. **検証**: 20件をランダム抽出し、人間（研究者自身 + ゼミメンバー等）が同じルーブリックで採点 → Judge との相関 (Spearman's ρ) を確認

**注意点**: Chen et al. (2026) は LLM-as-Judge が等重み複合スコアでは次元間異質性（dimension heterogeneity）で希釈されることを指摘。次元別報告が重要。

#### 方法B：事実整合性の自動検証（Factual Grounding Check）

LLM説明が input data と矛盾していないかを自動的に検証する。

```python
# 疑似コード
for each (input_data, recommended_price, explanation) in test_set:
    # 1. 説明文から主張を抽出
    claims = extract_claims(explanation)  
    # 例: "清掃スコアが先月比で0.3低下" 
    
    # 2. 各主張を input_data と照合
    for claim in claims:
        is_supported = verify_against_data(claim, input_data)
    
    # 3. 指標: 事実支持率 = supported_claims / total_claims
    factual_grounding_rate = supported / total
```

| 指標 | 目標 |
|------|------|
| **事実支持率** (Factual Grounding Rate) | ≥ 0.90 |
| **幻覚率** (Hallucination Rate) | ≤ 0.05 |
| **数値一致率** (Numerical Accuracy) | 説明中の数値がinputデータと±5%以内 |

#### 方法C：Proxy User Study（代理ユーザスタディ）

現場マネージャーに代わる「代理評価者」を活用する。

| 代理評価者 | 方法 | 限界と対策 |
|-----------|------|-----------|
| **観光学・経営学の教員・院生** | 5-10名に説明文を提示し、5次元ルーブリックで評価 | ドメイン知識はあるが運営経験がない → 「行動可能性」次元の評価精度が低い可能性を報告 |
| **クラウドソーシング** | Lancers/CrowdWorks で「宿泊施設の価格設定に関心がある」評価者を募集 | コストと品質管理 → Attention check 問題を挿入し、低品質回答を除外 |
| **ペルソナ設定 LLM** | GPT-4oに「地方旅館の経営者(60代, IT不慣れ)」等のペルソナを設定して評価させる | LLMのバイアスあり → あくまで補助的位置づけ |

**重要**: Pičulin et al. (2025, ICML Position Paper) は "Explainable AI Cannot Advance Without Better User Studies" と主張し、proxy task の限界を指摘している。本研究では **proxy study の限界を明示的に議論し、将来研究でのフィールド検証を推奨** するスタンスを取る。

#### 方法D：ペアワイズ比較評価

「どちらの説明が良いか？」のペアワイズ比較は絶対評価より評価者間一致度が高い (Wardatzky et al., 2025)。

| 比較対象ペア | 検証内容 |
|-------------|---------|
| 提案手法 vs ABSAなし説明 | ABSA情報の説明品質への貢献 |
| 提案手法 vs SHAP値のみの説明 | 自然言語化の付加価値 |
| 提案手法 vs 定型文テンプレート | LLM生成の柔軟性の価値 |

### 5-3. 根拠文献

- Cheng, X., Wang, W. & Ghose, A. (2025). LLMs for Explainable Business Decision-Making: A Reinforcement Learning Fine-Tuning Approach. *arXiv:2601.04208*. — LEXMA フレームワーク: RL fine-tuning で audience-appropriate な説明を生成。expert-facing / consumer-facing の2種類の説明品質を人間評価で比較。**住宅ローン審査の意思決定という、本研究と類似した「専門家向け意思決定支援」の説明評価手法**
- Chen, L. et al. (2026). Criterion Validity of LLM-as-Judge for Business Outcomes in Conversational Commerce. *arXiv:2604.00022*. — 7次元ルーブリックの LLM-as-Judge を実ビジネス成果と照合。次元間異質性 (dimension heterogeneity) と composite dilution effect を発見。本研究の LLM-as-Judge ルーブリック設計の主要参考
- Rudra, A. & Agrawal, M. (2025). A Heuristic-First Evaluation Framework for Marketing AI Agents. IEEE. — マーケティングAIエージェントの Quality, Actionability, Trust の3軸評価フレームワーク
- Wardatzky, K. et al. (2025). Whom do explanations serve? A systematic literature survey of user characteristics in explainable recommender systems evaluation. *ACM Trans. Recommender Systems*. (被引用15件) — XAI推薦システム評価における user characteristics の体系的サーベイ。**ペアワイズ比較が絶対評価より信頼性高い**ことを報告
- Pičulin, M. et al. (2025). Position: Explainable AI Cannot Advance Without Better User Studies. *ICML 2025*. — Proxy task の限界を指摘。本研究では限界として明示的に議論する根拠
- Tocchetti, A. (2024). Model explainability through human knowledge and crowdsourcing. *PhD Thesis, Politecnico di Milano*. — クラウドソーシングによるXAI説明品質評価の方法論
- Yu, F. (2025). When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation for LLMs. *arXiv:2508.02994*. (被引用9件)

---

---

## 第6章　Layer 5 — 経済性評価（収益シミュレーション）

### 6-1. 検証の問い
> 提案システムを使用した場合、収益（RevPAR）はどの程度改善されるか？

### 6-2. シミュレーション環境の構築

Wang et al. (2025) のホテルDRLシミュレーション設計を参考に、小規模地方宿泊施設向けに適応する。

#### 環境パラメータ

| パラメータ | 設定 | 根拠 |
|-----------|------|------|
| 客室数 $M$ | 10〜30室（地方旅館規模） | 対象ドメインに合わせたスケール |
| 時間軸 $T$ | 30日×12ヶ月（繁忙期・閑散期） | Wang et al. (2025) は30日を1エピソードとして設計 |
| 顧客到着 $Q_{t}$ | Poisson分布 $\mathcal{P}_i$（曜日・季節別パラメータ） | Wang et al. (2025)、Lee (2018) |
| 価格受容確率 $F(p)$ | ロジスティック関数 $1/(1+e^{\beta(p-\mu)})$ | Wang et al. (2025)、Zhu et al. (2022) |
| 宿泊日数分布 $Z(d)$ | 離散分布（1泊70%, 2泊20%, 3泊以上10%） | 地方旅館の実データから推定 |
| 口コミ生成 | aspect スコアを合成（正規分布 + トレンド成分 + ノイズ） | 実データの統計量をベースに合成 |

#### 需要関数のキャリブレーション

1. **実データからのパラメータ推定**: 過去の（価格, 稼働率）ペアからロジスティック需要関数のパラメータ $\beta, \mu$ を推定
2. **口コミスコアの需要弾力性**: ABSA感情スコアと稼働率の関係をデータから回帰分析し、口コミスコア変化が需要に与える影響量を定量化
3. **検証**: 推定した需要モデルの予測値を holdout 期間の実データと比較し、適合度を確認

### 6-3. 収益シミュレーション指標

| 指標 | 定義 | 意味 |
|------|------|------|
| **RevPAR 改善率** | $(\text{RevPAR}_{proposed} - \text{RevPAR}_{baseline}) / \text{RevPAR}_{baseline}$ | 収益改善の主指標 |
| **ADR** (Average Daily Rate) | 平均客室単価 | 価格水準の妥当性 |
| **OCC** (Occupancy Rate) | 稼働率 | 値上げによる需要減少の確認 |
| **GopPAR** (Gross Operating Profit PAR) | RevPAR − コスト | 利益ベースの評価 |
| **価格変動幅** | std(p̂ₜ) | 極端な価格変動がないことの確認 |

### 6-4. 感度分析

シミュレーションの信頼性を高めるため、以下のパラメータを変動させて結果のロバスト性を確認する。

| 変動パラメータ | 変動幅 | 検証意図 |
|-------------|-------|---------|
| 需要弾力性 $\beta$ | ±20% | 需要モデルの推定誤差に対する頑健性 |
| 口コミノイズ $\sigma$ | ×0.5, ×1.0, ×2.0 | 口コミ品質の変動への頑健性 |
| 競合価格変動 | ±10%, ±20% | 競合環境変化への頑健性 |
| 繁忙/閑散期比率 | 実データ比率  ±30% | 季節性の変動への頑健性 |
| 顧客到着率 $\lambda$ | ±30% | 集客力の変動（コロナ後回復等） |

### 6-5. 根拠文献

- Wang, X. et al. (2025). *前掲*. — 30日エピソードのホテルDRLシミュレーション環境。PPO, DDPG, TD3, ACの4手法比較。MRR, Profit, DGA, ROP の4 KPIで評価。3つの実在ホテル（青島）のデータでキャリブレーション
- Bayoumi, A.E.M. et al. (2013). *前掲*. — Monte Carlo シミュレータによる価格乗数最適化
- Binesh, F. et al. (2025). Deep learning + game-theoretic + SHAP for Airbnb pricing. — SHAPベースの説明評価をシミュレーション上で実施
- Parmar, J.R. (2025). AI-Driven Price Sensitivity Analysis and Consumer Value Optimization. — 反実仮想シミュレーションによる価格感度分析手法

---

---

## 第7章　統合評価の戦略 — 評価結果の報告と議論

### 7-1. 評価結果の統合報告構造

各 Layer の結果を以下の形式で報告する。

```
■ 第1部：コンポーネント評価
  Layer 1: ABSA → F1=X.XX, アノテーション一致 κ=X.XX
  Layer 2: アブレーション → M2 vs M0 の RMSE 改善 X.X%（p<0.05）

■ 第2部：システム評価
  Layer 3: バックテスト → MAE(price)=¥XXX, 方向一致率=XX%
  Layer 4: 説明品質 → LLM-Judge 平均 X.X/5.0, Proxy user 相関 ρ=X.XX

■ 第3部：経済性評価
  Layer 5: RevPAR 改善率 = +X.X%（95%CI: [X.X%, X.X%]）
         感度分析: β±20% でも改善率 > 0 を維持
```

### 7-2. 「ユーザスタディなし」の論文上での正当化戦略

| 正当化ポイント | 内容 | 根拠 |
|-------------|------|------|
| **先行研究の慣行** | ホテル DP 研究の大多数はシミュレーション評価のみ | Wang et al. (2025), Tuncay et al. (2024), Li (2026), Bayoumi et al. (2013) のいずれもフィールド実験なし |
| **段階的研究** | Fisher et al. (2018) の方法論では、シミュレーション検証 → フィールド実験を2段階として位置づけ。本研究は Stage 1 に相当 | Fisher, Gallino & Li (2018), *Management Science* (被引用285件) |
| **代理指標の妥当性** | LLM-as-Judge と少数の人間評価の相関を示すことで、自動指標の criterion validity を示す | Chen et al. (2026), Cheng et al. (2025) |
| **三角測量** | 5層の独立した評価の convergence（一貫した改善傾向）が実システムでも有効であることの間接的証拠 | Mangold et al. (2025) の体系的レビューが multi-method evaluation を推奨 |
| **限界の明示的議論** | "Limitations" セクションで「実マネージャーによる検証は future work」と明記 | Pičulin et al. (2025, ICML) の proxy task 限界の指摘を引用 |

### 7-3. 想定される査読コメントと対応

| 想定質問 | 対応策 |
|---------|-------|
| 「実ユーザでの検証がない」 | 5層の多角的評価 + Fisher et al.の段階的方法論 + 限界明示 |
| 「シミュレーション環境が非現実的」 | 実データからのキャリブレーション（需要関数パラメータ推定）+ 感度分析 |
| 「LLM-as-Judge は信頼できるか」 | 少数人間評価との相関提示 + Chen et al. の次元別報告 |
| 「RevPAR 改善は机上の空論」 | 感度分析での頑健性 + 既存研究との改善幅比較 |
| 「ABSA が本当に価格に影響するのか」 | Layer 2 アブレーション + SHAP の可視化で因果的示唆 |

---

---

## 第8章　実施ロードマップ

| フェーズ | 評価層 | 必要データ | 推定作業量 |
|---------|-------|----------|-----------|
| **Phase 1** | Layer 1: ABSAモジュール精度 | アノテーション済み口コミ 300件 | 3-4週間 |
| **Phase 2** | Layer 2: アブレーション | 過去予約・口コミデータ（最低6ヶ月分） | 2-3週間 |
| **Phase 3** | Layer 3: バックテスト | Phase 2 と同じデータ | 2-3週間 |
| **Phase 4** | Layer 4: 説明品質 | 100件以上の（入力, 推薦, 説明）トリプル | 2-3週間 |
| **Phase 5** | Layer 5: 収益シミュレーション | シミュレーション環境構築 + 感度分析 | 3-4週間 |
| **Phase 6** | 統合・論文執筆 | 全Layer結果 | 4-6週間 |

---

---

## 参考文献一覧

1. Wang, X., Xie, Y., Jian, L., Liu, W. & Lv, W. (2025). A Two-Stage Deep Reinforcement Learning-Driven Dynamic Discriminatory Pricing Model for Hotel Rooms with Fairness Constraints. *J. Theor. Appl. Electron. Commer. Res.*, 20(4), 337.
2. Garcia, D., Tolvanen, J. & Wagner, A.K. (2022). Demand estimation using managerial responses to automated price recommendations. *Management Science*. (被引用30件)
3. Tang, J., Qi, Z., Fang, E. & Shi, C. (2025). Offline feature-based pricing under censored demand: A causal inference approach. *Manufacturing & Service Operations Management*. (被引用21件)
4. Fisher, M., Gallino, S. & Li, J. (2018). Competition-based dynamic pricing in online retailing: A methodology validated with field experiments. *Management Science*. (被引用285件)
5. Cheng, X., Wang, W. & Ghose, A. (2025). LLMs for Explainable Business Decision-Making: A Reinforcement Learning Fine-Tuning Approach. *arXiv:2601.04208*.
6. Chen, L., Liu, Q., Lin, W. & Liang, F. (2026). Criterion Validity of LLM-as-Judge for Business Outcomes in Conversational Commerce. *arXiv:2604.00022*.
7. Liskowski, P. & Jankowski, N. (2026). Arctic-ABSA: Aspect-Based Sentiment Analysis with Arctic Foundation Models. *arXiv:2505.02780*.
8. Tran, T.K. & Tran, P. (2026). Aspect-based Sentiment Analysis in Ho Chi Minh city Hotel Reviews. *IEEE Access*.
9. Öztürk, A.C. (2026). Discovering Aspect-Sentiment Drivers of Hotel Review Ratings via Interpretable High-Utility Rules. *IEEE Access*.
10. Jeong, M. & Lee, S.A. (2024). Exploring the impact of ChatGPT on hotel customer experience. *Int. J. Contemp. Hosp. Manag.* (被引用43件)
11. Wardatzky, K. et al. (2025). Whom do explanations serve? *ACM Transactions on Recommender Systems*. (被引用15件)
12. Pičulin, M. et al. (2025). Position: Explainable AI Cannot Advance Without Better User Studies. *ICML 2025*.
13. Rudra, A. & Agrawal, M. (2025). A Heuristic-First Evaluation Framework for Marketing AI Agents. *IEEE*.
14. Yu, F. (2025). When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation. *arXiv:2508.02994*.
15. Tocchetti, A. (2024). Model explainability through human knowledge and crowdsourcing. *PhD Thesis, Politecnico di Milano*.
16. Mangold, A. et al. (2025). On the Design and Evaluation of Human-centered Explainable AI Systems. *arXiv:2510.12201*.
17. Saitta, E., D'Amico, S. & Farinella, G.M. (2024). Hotel Dynamic Pricing Predictions with SHAP.
18. Degife, W. & Lin, X. (2024). ABSA + GRU demand forecasting with ablation study.
19. Wu, Y. et al. (2022). Sentiment-enhanced demand forecasting.
20. Aggarwal, K. (2025). Tree models + SHAP for demand/price optimization.
21. Bayoumi, A.E.M. et al. (2013). Dynamic pricing for hotel revenue management using price multipliers. *J. Revenue Pricing Manag.*
22. Binesh, F. et al. (2025). Deep learning + game-theoretic + SHAP for Airbnb pricing.
23. Parmar, J.R. (2025). AI-Driven Price Sensitivity Analysis and Consumer Value Optimization.
24. Li, L. (2026). Adaptive Reinforcement Learning in Dynamic Pricing Strategies. *Informatica*.
25. Bouchair, A. (2025). IMOHAG: A simulation-based decision support framework for tourist experience management in data-poor destinations. *SSRN 6136403*.
26. Lemmens, A. et al. (2025). Personalization and targeting: How to experiment, learn & optimize. *Int. J. Research in Marketing*. (被引用16件)
27. Zhang, Q. et al. (2025). Harnessing the Power of Interleaving and Counterfactual Evaluation for Airbnb Search Ranking. *KDD 2025*.
28. Tuncay, G. et al. (2024). A reinforcement learning based dynamic room pricing model for hotel industry. *INFOR*.
