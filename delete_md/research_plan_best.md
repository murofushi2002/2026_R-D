# 口コミ感情ボラティリティを活用した宿泊施設価格予測モデルの研究開発計画

> **Research Development Plan: Accommodation Price Prediction Model Leveraging Review Sentiment Volatility**
>
> 最終更新: 2026年7月
> 信州大学 修士研究

---

## 目次

1. [研究の背景と課題](#1-研究の背景と課題)
2. [関連研究の技術的分析](#2-関連研究の技術的分析)
3. [研究ギャップと本研究の新規性](#3-研究ギャップと本研究の新規性)
4. [リサーチクエスチョン](#4-リサーチクエスチョン)
5. [提案手法](#5-提案手法)
6. [データ戦略](#6-データ戦略)
7. [評価フレームワーク](#7-評価フレームワーク)
8. [研究ロードマップ](#8-研究ロードマップ)
9. [参考文献](#9-参考文献)

---

## 1. 研究の背景と課題

### 1.1 地方・小規模宿泊施設の価格設定問題

地方・小規模宿泊施設は、大手ホテルチェーンが持つ収益管理（Revenue Management）システムや専門知識を欠いており、価格設定においてデータに基づく科学的な意思決定が困難な環境にある。この問題は3層の障壁によって構造化される：

| 障壁の層 | 内容 | 根拠文献 |
|:---|:---|:---|
| **技術的障壁** | 高次元データ処理・リアルタイム需給推定能力の不足 | Shin (2023); Bu et al. (2022) |
| **組織的障壁** | 専門人材不足・RM導入コストの非整合 | Ivanov & Webster (2024) |
| **心理的障壁** | DP受容性の低さ・価格公平性への懸念 | Anisi et al. (2024) |

一方で、地方・小規模宿泊施設には豊富なオンライン口コミが蓄積されており、これを活用して価格設定の根拠を提供する可能性がある。

### 1.2 問題の核心

本研究がフォーカスする問題は以下の通りである：

> **口コミテキストから抽出したアスペクト別感情スコアを特徴量として価格予測モデルに組み込むことで、構造的特徴量のみのモデルと比較して予測精度が向上するか？特に、感情スコアの時間変動はその施設の価格ボラティリティを捉える指標として有効か？**

この問題設定は「価格説明の生成」ではなく、**「口コミ感情がボラティリティを考慮した価格予測モデルの構築に寄与するか」** を実証的に検証する研究である。

### 1.3 なぜ「ボラティリティ」なのか

宿泊価格は以下の要因により高い変動性（volatility）を持つ：

- **季節性**: 繁忙期・閑散期で宿泊価格に顕著な変動が生じる。リゾートホテルでは季節によるADR（平均客室単価）の大幅な変動が確認されており (Antonio et al., 2019)、Talón-Ballestero et al. (2022) は需要の高ボラティリティが小規模施設の価格最適化を困難にすることを指摘している
- **イベント駆動**: 地域行事・自然災害等の外生的ショックに対する非対称的な価格反応。COVID-19パンデミック下ではAirbnbの予約・価格動態に構造的変化が確認されている (Katz et al., 2025)。Wu et al. (2022) は需要不安定期（季節転換・イベント期間）に感情情報の予測寄与が増大することを示した
- **口コミフィードバックループ**: 低評価口コミ → 予約率低下 → 価格引き下げ圧力。Ye et al. (2009) はレビュースコア10%向上がオンライン予約を4.4%増加させることを実証し、Anderson (2012) は5段階評価+1点がADR 11.2%増と関連することを報告した。Shin (2023) はレビュー蓄積に応じた最適価格戦略（低導入価格→レビュー蓄積→価格引上げ）を理論的に導出している

金融分野でボラティリティは「対数リターンの標準偏差」として定義され (Andersen & Bollerslev, 1998; Roll, 1984)、日次ボラティリティを年率換算する式は以下である：

$$\sigma_{annually} = \sigma_{daily} \sqrt{P}$$

この式の前提となる日次対数リターンは通常、

$$r_t = \ln\left(\frac{p_t}{p_{t-1}}\right)$$

で定義され、$\sigma_{daily}$ は系列 $\{r_t\}$ の標準偏差である。

**各変数の意味**:
- $p_t$: 時点 $t$ の価格。ホテル文脈では、たとえば「ある宿泊施設の4月10日時点の掲載価格」や「日次ADR」に対応する
- $p_{t-1}$: 1期前の価格。ホテル文脈では前日の掲載価格や前日のADR
- $r_t$: $t-1$ 日から $t$ 日への対数変化率。価格が上昇すれば正、下落すれば負になる
- $\sigma_{daily}$: 日次対数リターン $r_t$ の標準偏差。ホテル価格が日々どの程度ぶれるかを表す
- $P$: 1年あたりの観測日数。金融では通常252取引日であるが、ホテルの日次価格系列に適用する場合は、calendarデータ等の年間観測日数に対応させて設定する
- $\sigma_{annually}$: 年率換算したボラティリティ。日次の価格変動を年間スケールで比較可能にした指標

**ホテルでの読み替え例**:
ある宿泊施設について、日次掲載価格が 12,000円 → 13,200円 → 11,800円 と変動しているとする。このとき各日の $r_t$ を計算し、その標準偏差を取ると $\sigma_{daily}$ が得られる。さらに $P$ を年間観測日数として掛け合わせれば、施設ごとの年率換算ボラティリティ $\sigma_{annually}$ を得られる。本研究ではこの金融的定義をそのまま援用するだけでなく、Inside Airbnb の日次価格系列に即して、価格水準そのものの標準偏差、変動係数、日次変化率の標準偏差も併用して評価する。

ここで重要なのは、ボラティリティは「平均価格の高さ」ではなく「価格変動の大きさ」を測る点である。たとえば平均価格が同じ 15,000円の2施設でも、日々ほぼ一定の施設と、週末・イベント時に大きく上下する施設では $\sigma_{daily}$ や $CV$ が異なる。本研究ではこの概念を宿泊価格に応用し、「**価格ボラティリティ**」と「**感情ボラティリティ**」の関係を定量的に分析する。

---

## 2. 関連研究の技術的分析

既存研究を4つのカテゴリに分類し、技術的な詳細（データセット規模、手法構成、定量的結果）を技術討論可能なレベルで記述する。

### 2.1 カテゴリA: ABSAの感情スコアを価格/需要予測モデルの入力とした研究

このカテゴリが本研究の直接的な先行研究群であり、最も重要である。

---

#### A1. Degife & Lin (2024) — 航空運賃予測におけるABSA-GRUハイブリッドモデル

**論文情報**: "A Multi-Aspect Informed GRU: A Hybrid Model of Flight Fare Forecasting with Sentiment Analysis", *Applied Sciences*, 14(10), 4221. DOI: 10.3390/app14104221

**データセット**:
- 航空券取引データ: 841,160件（2018年1月〜2023年7月）— Travel date, booking class (A-Z), class of service, origin, destination, distance, duration, stops, season等。前処理後の有効レコード数: 840,158件（学習80%/検証10%/テスト10%）
- 顧客レビュー: 46,167件（Skytrax + TripAdvisor, 同期間）

**ABSAパイプライン（3段階）**:

**ステップ1: 前処理**  
レビュー文をトークン化し、"I", "the", "and", "by" 等のストップワードおよび意味の薄い語を除去する。

**ステップ2: アスペクト語抽出（BERT）**  
ABSAタスク用にカスタマイズされた事前学習済みBERTモデルを使用して、前処理済みテキストからアスペクト語を自動抽出する。BERTはこのステップ（アスペクト語の特定）にのみ用いられ、感情判定には使用されない。

論文のResults section（Table 5等）に記載された実際の生アスペクト語（20種）:  
announcements, cleanliness, safety, baggage handling, staff interactions, cabin pressure, cancellation policies, security procedures, seat, comfort, crew, ambient noise, gate efficiency, rebooking processes, loyalty program benefits, legroom, air conditioning quality, boarding experience, in-flight entertainment offerings

**ステップ3: 感情スコア算出（エビデンスカウント）**  
BERTとは独立した感情評価ステップとして、各アスペクトに対するポジティブ/ネガティブ根拠をカウントし、スコアを算出する。

各アスペクト $a_i$ の局所感情スコア:
$$s_{a_i} = n^+_{a_i} - n^-_{a_i}$$

レビュー $l$ の総合感情スコア:
$$s_l = \sum_{a_i \in A_l} w_i \cdot s_{a_i}$$

**各変数の定義（論文記載通り）**:
- $s_{a_i}$: アスペクト $a_i$ の感情スコア。論文は「**ranges from −1 to 1**, and its sign denotes the polarity」と記述する。符号でポジティブ/ネガティブを表す
- $n^+_{a_i}$: アスペクト $a_i$ に対するポジティブ根拠（positive evidence）
- $n^-_{a_i}$: アスペクト $a_i$ に対するネガティブ根拠（negative evidence）
- $A_l$: レビュー $l$ に含まれるアスペクト集合
- $w_i$: アスペクト $a_i$ に割り当てられた重み
- $s_l$: レビュー $l$ 全体の重み付き総合感情スコア

**$[-1,1]$ の範囲はどこから来るか（論文の不明点）**:  
$s_{a_i} = n^+ - n^-$ という式だけでは、$n^+, n^-$ が整数カウントであれば差も任意の整数となり、そのままでは $[-1,1]$ に収まらない。論文は「ranges from −1 to 1」と主張するが、その正規化手順を本文には明示していない。数学的に $[-1,1]$ に収まる最も自然な解釈は、$n^+, n^-$ が**割合（proportion）**であり $n^+ + n^- = 1$（全根拠をポジ/ネガの2値に振り分けた比率）とした場合で、このとき:
$$s_{a_i} = n^+ - n^- = n^+ - (1 - n^+) = 2n^+ - 1 \in [-1, 1]$$
となる。ただしこの解釈は論文から直接読み取れるものではなく、**論文の記述と式の間に説明のギャップがある**点は留意が必要である。

**ステップ4: 9アスペクトグループへの集約**  
**なぜグループ化するか**（論文 Section 4 に明示）: 生アスペクト語が20種以上あると「分析結果が冗長かつ複雑になり、サービス品質の全体像を把握しにくくなる」ため、航空経営の視点で9グループに圧縮する。これにより感度分析の単位を揃え、グループ単位で除外実験を行い「どのサービス領域が運賃予測に効くか」を可視化することが目的である。

20種の生アスペクトを以下の9グループに統合する：

| グループ | 対応する生アスペクトの例 |
|:---|:---|
| Booking & Ticketing | cancellation policies, rebooking processes, loyalty program benefits |
| Pre-flight Procedures | boarding experience |
| Airport Services | gate efficiency |
| In-flight Amenities | in-flight entertainment, air conditioning quality, ambient noise |
| Seat & Cabin Features | seat, legroom, cabin pressure, comfort |
| Staff | crew, staff interactions |
| Safety & Security | safety, security procedures |
| Cleanliness | cleanliness |
| Post-flight Services | announcements, baggage handling, post-flight issues |

**アスペクト-運賃の相関（論文 Figure 4 より）**:
- Safety ↔ Actual fare: **r = 0.98\*\*\*** （p < 0.0001）
- Boarding process ↔ Safety: r = 0.91\*\*\*
- Comfort ↔ Class of service: r = 0.87\*\*

**予測モデル（GRU）**:  
7層スタックGRU（ユニット数: 824→512→256→128→64→32→16）、ReLU活性化、Adam optimizer (lr=0.001)、1400 epochs、batch size 450。入力は航空券取引属性とABSAで得た9グループの感情スコアを合わせた**94次元ベクトル**。

**主要結果（テストセット）**:

| モデル | RMSE | MAE | R² |
|:---|:---:|:---:|:---:|
| MLP | ― | 最高 | ― |
| LSTM | ― | 中程度 | ― |
| GRU（感情なし） | 高い | 高い | 低い |
| **ABSA_GRU（提案）** | **0.0071** | **0.0137** | **0.9899** |

**多期間予測結果（ABSA_GRU, 論文 Table 8）**:

| 予測期間 | RMSE | R² |
|:---:|:---:|:---:|
| 7日 | 0.0072 | 0.9769 |
| 14日 | 0.0078 | 0.9181 |
| 21日 | 0.0671 | 0.8246 |
| 30日 | 0.0881 | 0.8143 |

**感度分析（アスペクトグループ除外実験）**:

| 除外グループ | RMSE | MAE | R² | R²低下幅 |
|:---|:---:|:---:|:---:|:---:|
| なし（全アスペクト） | 0.0071 | 0.0137 | 0.9899 | ― |
| Safety/Security除外 | 0.0672 | 0.5431 | **0.6752** | **−0.3147** |
| Staff除外 | 0.0482 | 0.6887 | 0.8142 | −0.1757 |
| Seat/Cabin除外 | 0.0412 | 0.3128 | 0.9572 | −0.0327 |
| Cleanliness除外 | 0.0223 | 0.1145 | 0.9379 | −0.0520 |

**本研究への示唆**:
- ABSAから得られるアスペクト別感情スコアが価格/運賃予測に**劇的な改善**をもたらすことを実証（R²: 低い → 0.9899）
- 感情スコアは0/1のバイナリではなく $[-1,+1]$ の連続値であり、符号で極性を表す
- Safety/Security の感情スコアが運賃と r=0.98 の相関を持つことが相関分析でも確認されている
- **ただし航空運賃ドメインの研究**であり、宿泊施設ドメインへの適用は未検証

---

#### A2. Di Persio & Lalmi (2024) — Airbnb価格予測におけるNLP統合

**論文情報**: "Maximizing Profitability and Occupancy: An Optimal Pricing Strategy for Airbnb Hosts Using Regression Techniques and Natural Language Processing", *Journal of Risk and Financial Management*, 17(9), 414. DOI: 10.3390/jrfm17090414

**データセット**: Inside Airbnb ローマ（2023年5月スクレイピング）、約75列 → 前処理後に精選。レビューデータ: 1,048,576行、うち249,765件にホストへの言及あり。分析対象: 英語レビュー22,564件。

**手法構成**:
1. **特徴量選択**: Forward Feature Selection (FFS) vs PCA → FFS が R² を **27%改善**（PCAより優位）
2. **回帰モデル**: XGBoost Regressor (colsamplebytree=0.75, gamma=1, lr=0.05, maxdepth=8, nestimators=200), SVR (C=10, epsilon=0.1, gamma=1e-07, linear kernel), Neural Network (64→64→1, dropout=0.4, lr=0.078, 50 epochs)
3. **NLP手法**: Bag-of-Words, TF-IDF, **CNN-ABSA** (1D CNN, kernel=3, ReLU, max pooling, dropout=0.2) — ホストアスペクト（HOST-GENERAL）に焦点

**NLP分析結果**:
- BoW: 「location」「host」が最頻出 → ローマでは立地（コロッセオ近接等）が重視
- TF-IDF: 「top」「perfect」「excellent」が上位 → 肯定的レビュー偏重
- CNN-ABSA: ホスト言及7,865件中、93%がポジティブ感情。ネガティブ例: "terrible", "worst", "nightmare"

**価格予測結果**（MAE/R²は論文Table 2より）:
- **Neural Network**: 最高性能（複雑な非線形関係の学習に優位）
- **XGBoost**: 安定した予測（分散低減による堅牢性）
- **SVR**: 期待ほどの性能は得られず

**感情スコアとアスペクトの詳細**:
- ABSAは **HOST-GENERAL** の単一アスペクトに焦点を当てている
- 各レビューは Positive / Negative / Neutral の3極性に分類される
- ホスト言及レビュー7,865件のうち約93%がポジティブで、ネガティブな代表語として "terrible", "worst", "nightmare" が報告されている
- 本研究メモ中で確認できた範囲では、ABSA出力を価格モデルへ入れる明示的な数式は示されていない。したがって、ここで把握できる定量情報は「どのアスペクトを抽出したか」「極性分類をどう行ったか」「どの特徴量が重要であったか」に限られる

**重要な発見**:
- **最重要特徴量**: 地区 (I Centro Storico)、宿泊人数、ベッドルーム数、**レビュー数**、**立地レビュースコア**
- NLP分析はゲストが何を重視するかの洞察を提供 → 直接的な価格予測特徴量としての統合は限定的

**本研究への示唆**:
- Inside Airbnbデータ + NLP技術の組み合わせの実現可能性を実証
- **ただしABSA結果を価格予測モデルの説明変数として直接統合していない**（定性分析に留まる）
- アスペクト感情スコアを明示的に予測特徴量化 → 本研究のギャップ

---

#### A3. Wu et al. (2022) — ホテル需要予測における感情分析

**論文情報**: Wu, D.C., Zhong, S., Qiu, R.T.R., & Wu, J. (2022). "Are customer reviews just reviews? Hotel forecasting using sentiment analysis." *Tourism Economics*, 28(3), 795-816. DOI: 10.1177/13548166211049865

**データセット**:
- マカオのラグジュアリーホテル4軒
- 構造化された需要予測用データに、レビュー全文から抽出した感情スコアを追加

**感情分析の位置づけ**:
- レビューテキストから感情スコアを抽出し、需要予測モデルの追加特徴量として統合
- 本ワークスペース内で確認できた範囲では、**ABSAではなく文書レベルの感情分析**として整理されている
- そのため、抽出アスペクトの種類は明示されておらず、aspect別スコアではなく review-level / aggregate-level の感情特徴量として使われている

**比較したモデル枠組み**:
- 時系列予測モデル（ARIMA, LSTM等）と比較
- 感情特徴量を入れたモデルと入れないモデルの予測精度差を検証

**式の有無**:
- 本ワークスペース内で確認できた範囲では、感情スコアの明示的な算出式や需要関数の変数定義は記載されていない
- したがって、この研究について事実として書けるのは「感情スコアを追加特徴量として統合したこと」「aspect-levelではないこと」「需要変動期に改善が大きかったこと」である

**主要結果**:
- 感情スコアの追加は需要予測精度を統計的に有意に改善
- 特に需要が不安定な時期（季節変わり目、イベント期間）において改善が顕著

**本研究への示唆**:
- 感情情報が**ボラティリティの高い時期**に特に有効であるというエビデンス → ボラティリティ考慮型モデルの妥当性を支持
- ただし aspect-level の分解は行っていないため、「どの属性の感情が効いているか」は未解明のままである

---

### 2.2 カテゴリB: 宿泊施設口コミのABSA分析（価格予測に未接続）

---

#### B1. Özen & Katlav (2023) — ホテルABSAの大規模分析

**概要**: Booking.comから12,396件のホテルレビューをABSA分析。47被引用。アスペクトカテゴリ: 立地、清潔さ、スタッフ、快適さ、設備、コストパフォーマンス等。
- 各アスペクトの感情極性分布を定量化
- **ただし価格予測モデルへの接続は行われていない**

#### B2. Zhang et al. (2021) — 教師なしABSAによる顧客嗜好分析

**概要**: 教師なしABSAで顧客のアスペクトレベル嗜好を抽出。82被引用。
- 明示的なアスペクト言及がなくても暗黙的嗜好を推定
- **価格モデルへの統合は未実施**

**本研究への示唆**: 宿泊施設ドメインでABSAの有効性は確認されているが、**ABSAスコア → 価格予測の接続を実装した研究がない** → 本研究の主要ギャップ

---

### 2.3 カテゴリC: 口コミ → 価格/収益への統計的エビデンス

この分野は「口コミが本当に価格に影響するのか」の根拠を提供する。

---

#### C1. Abrate et al. (2019) — ヘドニック収益モデル

**概要**: "How is the revenue of a city's Airbnbs affected by its online reputation?", 215被引用。
- ヘドニック回帰にてレビュースコアが収益に有意に影響
- 価格変動性（price variability）とレビュー評価の関係を分析
- **本研究へのボラティリティ定式化の基盤を提供**

#### C2. Almeida et al. (2025) — テキスト感情の数値スコアに対する優位性

**概要**: ポルトのInside Airbnb、SAR空間回帰モデル。
- **テキスト感情分析が数値レビュースコアよりも価格説明力が高い** → テキストマイニングの必要性を支持
- ネガティブ口コミの影響はポジティブの**2〜4倍の非対称性** → ネガティブ感情に重み付けすべき根拠

#### C3. Wang & Nicolau (2017) — 33都市Airbnb価格決定要因

**概要**: 33都市のAirbnbリスティングを分析。価格変数を5カテゴリ（ホスト特性、地理、物件属性、アメニティ、口コミ）に分類。
- Gradient boosting: MAE=0.24, R²≈0.71
- SVR: MAE=0.21, R²≈0.77
- Neural Network: MAE=0.26, R²≈0.72

#### C4. 口コミ → 価格の4つのエビデンス経路

先行研究から以下の4経路が確認されている：

| 経路 | 内容 | 代表的エビデンス |
|:---|:---|:---|
| **A: スコア→価格プレミアム** | 高評価 → 高価格設定が可能 | Abrate et al. (2019): レビュースコアと収益の正の相関 |
| **B: テキスト感情 > 数値スコア** | テキスト解析がスコアより高い説明力 | Almeida et al. (2025): テキスト感情が数値より優位 |
| **C: ABSA → アスペクト別予測** | 特定アスペクトが特に強い影響 | Degife & Lin (2024): Safety除外でR²が0.31低下 |
| **D: ネガティブ非対称性** | ネガティブ感情の影響がポジティブの数倍 | Almeida et al. (2025): 2〜4倍の非対称効果 |

---

### 2.4 カテゴリD: 動的価格設定モデル（口コミ未統合）

---

#### D1. Shin (2023) — ベイズ動的価格設定

**論文情報**: "Dynamic Pricing with Online Reviews", *Management Science*, 110被引用。
- ベイズフレームワーク: 需要パラメータの事後分布をレビュースコアで更新
- 理論的最適方策を導出 → **実装はレビュー数値スコアのみ**、テキスト感情は未利用

#### D2. Bu et al. (2022, 2025) — 強化学習型DP

- DQN/PPO/SACによる価格最適化
- 状態空間に在庫・時間・需要推定値を含む
- **口コミ情報は状態空間に未統合**

#### D3. 伝統的DP理論

- Gallego & van Ryzin (1994): ポアソン需要下の最適価格制御 — DP理論の基盤
- Bandalouski et al. (2021): 多段階DPのMIP定式化
- Chen et al. (2026), Luo et al. (2022): バンディットアルゴリズムによる価格探索

**本研究への示唆**: 既存のDPモデルは口コミテキストを取り込んでいない。感情スコアをモデルに統合することが差別化ポイント。

---

### 2.5 LLMの価格設定への適用可能性

LLM（大規模言語モデル）を価格モデル**そのもの**に使うべきかについて、以下のエビデンスを整理する：

| 観点 | エビデンス | 判断 |
|:---|:---|:---|
| LLMによる直接的価格計算 | Liu et al. (2025): LLMは数値的な価格計算に失敗する傾向 | ✗ 不適 |
| LLMによる説明生成 | Mohammed & Denizci Guillet (2025b): XAI+LLMで価格根拠を自然言語化 | △ 補助的役割 |
| LLMによるアスペクト抽出 | 現在のパイプライン: LLM→アスペクト別理由文抽出に有効 | ✓ 有効 |
| LLMによるゼロショットABSA | Zhang et al. (2023): GPT系モデルのABSA性能はfine-tuned BERTに劣る場合あり | △ 要検証 |

**結論**: LLMの役割は**特徴量エンジニアリングの上流工程**（アスペクト抽出・理由文生成）に限定し、価格予測モデル自体には統計的/DL手法を用いるのが最も合理的である。

---

## 3. 研究ギャップと本研究の新規性

### 3.1 既存研究のギャップマッピング

| # | ギャップ | エビデンス |
|:---|:---|:---|
| G1 | ABSA感情スコアを宿泊施設の**価格予測**入力に使用した研究が**存在しない** | Degife & Lin (2024)は航空運賃、Di Persio & Lalmi (2024)はABSA結果を価格モデルに未統合 |
| G2 | 口コミ感情の**時間変動**と価格ボラティリティの関係が**未解明** | Wu et al. (2022)はvolatile periodsでの有効性を示すが定量的分析なし |
| G3 | 地方/小規模宿泊施設を明示的ターゲットにした口コミ活用型モデルが**ない** | 既存研究は大都市(ローマ、マカオ)や大手航空会社が対象 |
| G4 | LLM→BERT ABSAパイプラインの**宿泊価格予測向け拡張**が**未提案** | 現行パイプラインは感情分析で完結、価格モデルへの接続設計がない |

### 3.2 本研究の新規性（根拠→提案の論理チェーン）

**新規性1: ABSA感情スコアの宿泊施設価格予測モデルへの直接統合**

```
根拠: Degife & Lin (2024) — ABSAスコアの航空運賃予測への統合でR²=0.99を達成
     + Di Persio & Lalmi (2024) — Inside Airbnb + NLPの実現可能性を実証（ただしABSA→価格未接続）
     + エビデンス経路C: 特定アスペクト除外でR²が0.31低下 → アスペクト固有の価格影響
提案: 宿泊施設ドメインでABSA感情スコアを価格予測モデルの説明変数として初めて統合し、
     アスペクト別の価格感度を定量評価する
```

**新規性2: 感情ボラティリティ指標による価格変動性の捕捉**

```
根拠: Wu et al. (2022) — 需要不安定期に感情情報が特に有効
     + Abrate et al. (2019) — 価格変動性とレビュー評価の関係を確認
     + ボラティリティ理論 (σ = std dev of log returns) — 金融分野で確立
提案: アスペクト別感情スコアの時間変動（感情ボラティリティ）を算出し、
     これが価格ボラティリティと相関するか、価格予測精度を改善するかを検証する
```

**新規性3: LLM→BERT ABSAパイプラインの価格予測向け拡張**

```
根拠: 現行パイプライン（LLM→アスペクト別理由文抽出→BERT→感情スコア）は感情分析で有効
     + Degife & Lin (2024) — 9アスペクトグループ化+感度分析が有意義な知見を提供
     + Almeida et al. (2025) — ネガティブ感情の非対称効果 (2-4倍)
提案: パイプラインを拡張し (i) 時間窓集約、(ii) 非対称感情重み付け、
     (iii) アスペクト-価格相関分析 を追加し、価格モデル向け特徴量を自動生成する
```

---

## 4. リサーチクエスチョン

| # | リサーチクエスチョン | 検証方法 |
|:---|:---|:---|
| **RQ1** | ABSAアスペクト別感情スコアを特徴量に追加すると、構造的特徴量のみのモデルと比較して宿泊価格予測精度は有意に向上するか？ | アブレーション実験 (M0 vs M3/M4) |
| **RQ2** | アスペクト別感情スコアの時間変動（感情ボラティリティ）は、当該施設の価格ボラティリティを説明・予測できるか？ | 相関分析 + Granger因果検定 + 予測モデル比較 |
| **RQ3** | どのアスペクトの感情が宿泊価格に最も感度が高いか？そしてその感度はDegife & Lin (2024) の航空運賃ドメインとどう異なるか？ | 感度分析 (Leave-one-aspect-out) + SHAP値 |
| **RQ4** | LLM→BERT ABSAパイプラインの拡張（時間窓集約・非対称重み付け）は予測精度をさらに改善するか？ | 拡張パイプライン vs 基本パイプラインの比較 |

---

## 5. 提案手法

### 5.1 全体アーキテクチャ

本研究のシステムは3段階で構成される：

```
Stage 1: 拡張ABSA特徴量パイプライン
  口コミテキスト → LLMアスペクト抽出 → BERT感情推定 → 時間窓集約 → 特徴量ベクトル

Stage 2: ボラティリティ指標算出
  価格時系列 → 価格ボラティリティ
  感情時系列 → 感情ボラティリティ
  → 両者の関係性分析

Stage 3: 価格予測モデル
  構造的特徴量 + ABSA特徴量 + ボラティリティ特徴量 → 予測モデル → 価格 + 不確実性区間
```

### 5.2 Stage 1: 拡張ABSAパイプライン

#### 5.2.1 現行パイプライン（ベースライン）

現在のパイプラインは以下の構成である：

1. **LLMによるアスペクト別理由文抽出**: 口コミテキストをLLMに入力し、観点別（立地、清潔さ、サービス、設備、コストパフォーマンス等）に理由文を構造化抽出
2. **BERTによる感情スコアリング**: 各アスペクトの理由文をBERT感情分類モデルに入力し、$[-1, +1]$ の連続スコアを推定

出力: リスティング $i$ のアスペクト $k$ に対する感情スコア $s_i^{(k)}$

#### 5.2.2 拡張提案

以下の3つの拡張を提案する。各拡張は独立にオン/オフ可能であり、アブレーションで効果検証する。

**拡張E1: 時間窓集約 (Temporal Aggregation)**

動機: 口コミは時点データであり、1件のスコアでは傾向が不安定。Degife & Lin (2024) は月次集約を使用。

リスティング $i$ のアスペクト $k$ に対し、時間窓 $[t-W, t]$ における集約統計量を算出：

$$\bar{s}_{i,t}^{(k)} = \frac{1}{|R_{i,[t-W,t]}|} \sum_{r \in R_{i,[t-W,t]}} s_r^{(k)}$$

$$\sigma_{s,i,t}^{(k)} = \sqrt{\frac{1}{|R_{i,[t-W,t]}|-1} \sum_{r \in R_{i,[t-W,t]}} \left( s_r^{(k)} - \bar{s}_{i,t}^{(k)} \right)^2}$$

ここで $R_{i,[t-W,t]}$ は時間窓内のレビュー集合、$W$ は窓幅（30日, 60日, 90日を比較）。分散が小さいことは感情の安定性を示し、分散が大きいことは「評価が割れている」状態を示す。

**拡張E2: ネガティブ非対称重み付け (Negative Asymmetric Weighting)**

動機: Almeida et al. (2025) がネガティブ口コミの影響はポジティブの2〜4倍であることを実証。

非対称加重感情スコアを定義：

$$\tilde{s}_{i,t}^{(k)} = \frac{1}{|R|} \sum_{r \in R} \begin{cases} s_r^{(k)} & \text{if } s_r^{(k)} \geq 0 \\ \alpha \cdot s_r^{(k)} & \text{if } s_r^{(k)} < 0 \end{cases}$$

ここで $\alpha > 1$ はネガティブ増幅係数。$\alpha$ はクロスバリデーションで最適化するが、Almeida et al. の結果から $\alpha \in [2.0, 4.0]$ が探索範囲の目安となる。

**拡張E3: アスペクト-価格相関に基づくアスペクト重み付け (Correlation-Based Aspect Weighting)**

動機: Degife & Lin (2024) の Figure 4 において、Safety-Fare相関 r=0.98***、Comfort-Class相関 r=0.87** 等、アスペクトごとに価格との相関が大きく異なることが判明。

各アスペクトの感情スコアと実価格の相関を事前計算し、重み付き集約スコアを生成：

$$S_{i,t}^{weighted} = \sum_k \rho_k \cdot \bar{s}_{i,t}^{(k)}, \quad \rho_k = \frac{|Corr(s^{(k)}, p)|}{\sum_j |Corr(s^{(j)}, p)|}$$

ここで $\rho_k$ は正規化相関重み。これにより、価格への影響力が高いアスペクトの感情変動がモデルに優先的に反映される。

#### 5.2.3 宿泊施設向けアスペクトカテゴリの設計

航空運賃のDegife & Lin (2024) の9カテゴリを参考に、宿泊施設向けに以下のカテゴリを設計する：

| # | アスペクトカテゴリ | 対応するキーワード例 | Degife対応 |
|:---|:---|:---|:---|
| 1 | **立地・アクセス** (Location) | location, walk, station, access, neighborhood | Airport services |
| 2 | **清潔さ** (Cleanliness) | clean, tidy, dirty, hygiene | Cleanliness |
| 3 | **ホスト対応** (Host Service) | host, responsive, communication, check-in | Staff |
| 4 | **室内設備** (Room Facilities) | bed, kitchen, bathroom, wifi, amenities | Seat/Cabin features |
| 5 | **快適さ** (Comfort) | comfortable, quiet, noise, spacious | In-flight amenities |
| 6 | **コストパフォーマンス** (Value) | price, value, expensive, worth, affordable | Booking/ticketing |
| 7 | **安全性** (Safety) | safe, secure, lock, neighborhood safety | Safety/security |

### 5.3 Stage 2: ボラティリティ指標の定義と計算

#### 5.3.1 価格ボラティリティ

リスティング $i$ の価格時系列 $\{p_{i,t}\}$ に対し、以下のボラティリティ指標を計算：

**指標V1: 変動係数 (Coefficient of Variation)**

$$CV_i = \frac{\sigma(p_i)}{\bar{p}_i}$$

変動係数はスケール不変であり、異なる価格帯のリスティング間で比較可能。Abrate et al. (2019) のヘドニック収益モデルにおいて価格変動性の指標として使用された概念に基づく。

**指標V2: 対数リターンの標準偏差**

金融ボラティリティの標準的定義 (Andersen & Bollerslev, 1998; Roll, 1984) を宿泊価格に応用：

$$r_{i,t} = \ln\frac{p_{i,t}}{p_{i,t-1}}, \quad \sigma_{r,i} = \sqrt{\frac{1}{T-1}\sum_{t=1}^{T}(r_{i,t} - \bar{r}_i)^2}$$

**指標V3: ローリングウィンドウボラティリティ**

時間変動するボラティリティを捕捉するため、窓幅 $W$ のローリング計算を行う：

$$\sigma_{i,t}^{(W)} = \sqrt{\frac{1}{W-1}\sum_{\tau=t-W+1}^{t}(r_{i,\tau} - \bar{r}_{i,[t-W+1,t]})^2}$$

これは金融分野のrealized volatility (Andersen & Bollerslev, 1998) の離散近似であり、時点ごとのボラティリティ水準を追跡可能にする。

#### 5.3.2 感情ボラティリティ

リスティング $i$ のアスペクト $k$ の感情時系列 $\{s_{i,t}^{(k)}\}$ に対し、同様のボラティリティ指標を計算：

$$CV_{s,i}^{(k)} = \frac{\sigma(s_i^{(k)})}{\bar{s}_i^{(k)} + \epsilon}$$

$$\sigma_{s,i,t}^{(k,W)} = \sqrt{\frac{1}{W-1}\sum_{\tau=t-W+1}^{t}\left(s_{i,\tau}^{(k)} - \bar{s}_{i,[t-W+1,t]}^{(k)}\right)^2}$$

ここで $\epsilon$ はゼロ除算回避の微小値。

#### 5.3.3 感情ボラティリティ → 価格ボラティリティの関係分析

**手法1: Granger因果検定**

$$p_{i,t} = \sum_{j=1}^{L} \alpha_j p_{i,t-j} + \sum_{j=1}^{L} \beta_j \sigma_{s,i,t-j}^{(k)} + \varepsilon_t$$

$H_0: \beta_1 = \beta_2 = \cdots = \beta_L = 0$ を検定し、感情ボラティリティが価格変動の予測に有意に寄与するか検証。

**手法2: 相関分析**

$$\rho = Corr\left(\sigma_{i,t}^{(W)}, \sigma_{s,i,t}^{(k,W)}\right)$$

各アスペクトの感情ボラティリティと価格ボラティリティの相関を算出し、どのアスペクトの感情変動が価格変動と最も連動するかを特定。

### 5.4 Stage 3: 価格予測モデル

#### 5.4.1 モデル候補の検討

| モデル | 適用根拠 | 長所 | 短所 |
|:---|:---|:---|:---|
| **XGBoost/LightGBM** | Di Persio & Lalmi (2024)で有効性確認 | 解釈性（SHAP）、少データで堅牢 | 時系列性非考慮 |
| **GRU** | Degife & Lin (2024)で最高性能 | 時系列パターン学習、長期依存性 | データ量要求大 |
| **Quantile Regression** | ボラティリティ=不確実性の直接推定 | 予測区間の直接出力 | 非線形性の制限 |
| **LightGBM + Quantile** | 柔軟性+不確実性 | 両方の長所 | 実装複雑性 |

**推奨構成**: 
- **メインモデル**: XGBoost/LightGBM（データ量制約を考慮 + SHAP解釈性）
- **時系列拡張**: 十分なデータが確保できた場合にGRUを追加比較
- **不確実性推定**: Quantile regression (τ=0.1, 0.25, 0.5, 0.75, 0.9) による予測区間

#### 5.4.2 特徴量セットの定義

| カテゴリ | 特徴量 | 次元数 |
|:---|:---|:---|
| **F_struct** | 物件属性（部屋タイプ、宿泊人数、ベッドルーム数、バスルーム数、アメニティ数）、ホスト属性（Superhost、応答率、アクティブ日数）、地理（緯度、経度、地区ダミー） | ~20-30 |
| **F_review_num** | 数値レビュー情報（全体スコア、カテゴリ別スコア、レビュー数、月間レビュー数） | ~8-10 |
| **F_absa** | ABSAアスペクト別感情スコア（7アスペクト × {平均, 標準偏差}） | 14 |
| **F_vol** | ボラティリティ特徴量（価格CV、感情CV × 7アスペクト、ローリングσ） | ~10-15 |
| **F_temporal** | 時間特徴量（曜日、月、祝日フラグ、イベント近接度） | ~5-10 |

#### 5.4.3 アブレーション設計

| モデル名 | 使用特徴量 | 目的 |
|:---|:---|:---|
| **M0** | F_struct | ベースライン（構造的特徴量のみ） |
| **M1** | F_struct + F_review_num | 数値レビューの追加効果 |
| **M2** | F_struct + F_review_num + F_temporal | 時間特徴量の追加効果 |
| **M3** | F_struct + F_absa | **RQ1の直接検証**: ABSAスコアの効果（数値レビュー**なし**） |
| **M4** | F_struct + F_review_num + F_absa | ABSAと数値レビューの併用効果 |
| **M5** | M4 + F_vol | **RQ2の検証**: ボラティリティ特徴量の追加効果 |
| **M6** | M5（拡張E1-E3適用） | **RQ4の検証**: パイプライン拡張の効果 |

**比較ポイント**:
- M0 vs M3: ABSA感情スコアの純粋な効果 → **RQ1**
- M1 vs M4: 数値レビューにABSAを追加する増分効果
- M4 vs M5: ボラティリティ特徴量の追加効果 → **RQ2**
- M5 vs M6: パイプライン拡張の効果 → **RQ4**
- M3のアスペクト1個ずつ除外（Leave-one-out）: 各アスペクトの感度 → **RQ3**

---

## 6. データ戦略

### 6.1 Inside Airbnb（主要データ）

**概要**: Inside Airbnbはオープンソースデータとして世界中の都市のAirbnbリスティング情報を提供する。Di Persio & Lalmi (2024) がローマデータを使用した実績がある。

**利用ファイル**:

| ファイル | 主要変数 | 用途 |
|:---|:---|:---|
| `listings.csv.gz` | id, name, host_id, host_since, host_response_rate, host_is_superhost, neighbourhood, latitude, longitude, property_type, room_type, accommodates, bathrooms, bedrooms, beds, amenities, price, minimum_nights, maximum_nights, review_scores_* | 構造的特徴量 F_struct, F_review_num |
| `reviews.csv.gz` | listing_id, date, reviewer_id, comments | テキストデータ → ABSAパイプライン入力 |
| `calendar.csv.gz` | listing_id, date, available, price | 日次価格時系列 → ボラティリティ算出 |

**日本のデータ状況**:
- Inside Airbnbが提供する日本データは**東京のみ**である (Inside Airbnb, 2024) → 地方・小規模宿泊施設には直接利用不可
- **対策**: 海外の地方/non-urban地域データを代替として使用

**地方・非都市部データの候補**:

| 地域 | 特性 | リスティング概数 |
|:---|:---|:---|
| Tasmania, AU | 小規模・自然観光 | ~3,000 |
| Trentino, IT | 山岳リゾート・季節変動大 | ~4,000 |
| Puglia, IT | 地方観光・小規模宿 | ~5,000 |
| Barossa Valley, AU | ワイナリー・小規模 | ~500 |
| Crete, GR | 島嶼観光・季節性 | ~8,000 |
| Lake District, UK | 自然観光・小規模 | ~3,000 |

※ リスティング概数はInside Airbnb (http://insideairbnb.com/get-the-data) の公開データから概算した推定値であり、スクレイピング時期により変動する。

**選択基準**: (1) レビュー数が十分 (リスティングあたり20件以上)、(2) 季節性が明確 (ボラティリティ分析に必要)、(3) 小規模宿泊施設が主体

### 6.2 補助データセット

| データセット | 出典 | レコード数 | 特徴 | 適用可能性 |
|:---|:---|:---|:---|:---|
| Hotel Booking Demand | Antonio et al. (2019), Kaggle | 119,390 | リゾートホテル+シティホテルの予約データ、キャンセル率含む | ボラティリティ分析の補助検証 |
| 515K Hotel Reviews | Booking.com経由, Kaggle (Jimenez, 2017) | 515,738 | 欧州6都市、ポジ/ネガ分離テキスト | ABSA検証用の大規模テキストデータ |
| TripAdvisor Hotel Reviews | Alam et al. (2016), Kaggle | 20,491 | 7点尺度の多次元評価 | 多面的評価の構造確認 |

### 6.3 データ前処理パイプライン

```
1. listings.csv → 欠損値処理、カテゴリエンコーディング、外れ値除去
2. reviews.csv → 言語検出 → 英語フィルタ → LLMアスペクト抽出 → BERT感情スコア
3. calendar.csv → 日次価格時系列構築 → ボラティリティ指標算出
4. 統合: listing_id × date でマージ → 特徴量マトリクス構築
5. 分割: 80% train / 10% validation / 10% test（時系列分割を推奨）
```

---

## 7. 評価フレームワーク

### 7.1 評価レベルの構成

5層の評価フレームワークを適用する：

#### レベル1: ABSA精度評価

| 指標 | 内容 |
|:---|:---|
| Aspect Extraction F1 | 抽出されたアスペクトの正確性 |
| Sentiment Classification Accuracy | 感情極性の分類精度 |
| Inter-annotator Agreement (κ) | 人手アノテーションとの一致度 |

サンプリングした200-300件のレビューに人手アノテーションを行い、パイプラインの品質を検証する。

#### レベル2: ABSA→予測効果（アブレーション）

| 指標 | 算出式 |
|:---|:---|
| RMSE | $\sqrt{\frac{1}{N}\sum(y_i - \hat{y}_i)^2}$ |
| MAE | $\frac{1}{N}\sum|y_i - \hat{y}_i|$ |
| R² | $1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$ |
| MAPE | $\frac{100}{N}\sum\frac{|y_i - \hat{y}_i|}{y_i}$ |

M0〜M6の全組み合わせで計測し、**各特徴量セットの増分効果**を定量評価する。

Degife & Lin (2024) との比較点: 彼らはR²=0.9899を達成しているが、航空運賃ドメイン。宿泊施設ドメインでどの水準に達するかは重要な比較対象。

#### レベル3: ボラティリティ予測精度

| 指標 | 内容 |
|:---|:---|
| Granger因果 p値 (Granger, 1969) | 感情ボラティリティ→価格ボラティリティの因果方向 |
| 相関係数 ρ | 感情vol vs 価格volの線形関係 |
| 予測区間カバレッジ | Quantile regressionの区間がactual priceをカバーする割合 |
| PICP (Prediction Interval Coverage Probability) | 目標: 90%区間で実際に90%±5%をカバー |

#### レベル4: 解釈性評価

| 指標 | 内容 |
|:---|:---|
| SHAP値のアスペクト別ランキング (Lundberg & Lee, 2017) | 各アスペクトの価格への寄与度順位 |
| Leave-one-aspect-out分析 | Degife & Lin (2024) の感度分析を再現 |
| アスペクト感度マトリクス | 地域×アスペクトの交差効果 |

#### レベル5: 実用性・ロバスト性

| 指標 | 内容 |
|:---|:---|
| クロスリージョン汎化 | 学習地域A → テスト地域Bでの性能 |
| レビュー数感度 | レビューが少ないリスティングでの性能劣化度 |
| 計算コスト | LLMアスペクト抽出 + BERT推論 + 予測の全体時間 |

---

## 8. 研究ロードマップ

### Phase 0: 基盤構築（1〜2ヶ月目）

- [ ] Inside Airbnbデータの取得・前処理パイプライン構築
- [ ] 地方/非都市部データの選定・ダウンロード・探索的分析
- [ ] calendar.csvからの日次価格時系列構築・ボラティリティ指標の試算
- [ ] レビューの言語分布・件数分布の確認

### Phase 1: ABSAパイプライン適用（2〜3ヶ月目）

- [ ] 現行LLM→BERTパイプラインをInside Airbnbレビューに適用
- [ ] 7アスペクトカテゴリの妥当性検証（人手サンプリング200件）
- [ ] アスペクト別感情スコアの分布確認・時系列可視化
- [ ] レベル1評価の実施

### Phase 2: ベースライン価格予測（3〜4ヶ月目）

- [ ] M0（構造的特徴量のみ）モデル構築・ベースライン性能確立
- [ ] M1（+数値レビュー）、M2（+時間特徴量）の構築
- [ ] XGBoost/LightGBMのハイパーパラメータチューニング
- [ ] SHAP分析による特徴量重要度の確認

### Phase 3: ABSA特徴量統合（4〜6ヶ月目）

- [ ] M3（+ABSAスコア）、M4（+数値+ABSA）の構築・RQ1検証
- [ ] Leave-one-aspect-out感度分析 → RQ3検証
- [ ] 拡張E1〜E3の実装・M6モデル構築 → RQ4検証
- [ ] レベル2評価の完全実施

### Phase 4: ボラティリティ分析（6〜7ヶ月目）

- [ ] 価格ボラティリティ指標 (CV, σ_r, rolling σ) の算出
- [ ] 感情ボラティリティとの相関分析・Granger因果検定
- [ ] M5（+ボラティリティ特徴量）の構築 → RQ2検証
- [ ] Quantile regressionによる予測区間推定
- [ ] レベル3評価の実施

### Phase 5: 総合分析・論文執筆（7〜9ヶ月目）

- [ ] レベル4-5評価の実施
- [ ] クロスリージョン汎化実験
- [ ] 全結果の統合分析・考察
- [ ] 論文執筆・投稿準備

---

## 9. 参考文献

### カテゴリA: ABSA × 価格/需要予測

1. Degife, W. A., & Lin, B.-S. (2024). A Multi-Aspect Informed GRU: A Hybrid Model of Flight Fare Forecasting with Sentiment Analysis. *Applied Sciences*, 14(10), 4221. DOI: 10.3390/app14104221
2. Di Persio, L., & Lalmi, E. (2024). Maximizing Profitability and Occupancy: An Optimal Pricing Strategy for Airbnb Hosts Using Regression Techniques and Natural Language Processing. *Journal of Risk and Financial Management*, 17(9), 414. DOI: 10.3390/jrfm17090414
3. Wu, J., et al. (2022). Forecasting hotel demand with multi-scale spatiotemporal features. (Macau luxury hotels, LSTM+sentiment, 78 citations)

### カテゴリB: 宿泊施設ABSA

4. Özen, E., & Katlav, E. Ö. (2023). ABSA analysis of 12,396 Booking.com hotel reviews. (47 citations)
5. Zhang, Y., et al. (2021). Unsupervised ABSA for customer preferences in hospitality. (82 citations)

### カテゴリC: 口コミ → 価格エビデンス

6. Abrate, G., et al. (2019). How is the revenue of a city's Airbnbs affected by its online reputation? (215 citations)
7. Almeida, A., et al. (2025). SAR spatial analysis of Porto Inside Airbnb: text sentiment > numerical rating, negative asymmetry 2-4x.
8. Wang, D., & Nicolau, J. L. (2017). Price determinants of sharing economy based accommodation rental: A study of listings from 33 cities on Airbnb.com. *International Journal of Hospitality Management*, 62, 120–131.

### カテゴリD: 動的価格設定

9. Shin, J. (2023). Dynamic Pricing with Online Reviews. *Management Science*. (110 citations)
10. Bu, J., et al. (2022). Online pricing with offline data: Phase transition and inverse square law. (DQN/PPO/SAC DP)
11. Bu, J., et al. (2025). Context-dependent dynamic pricing continuation.
12. Gallego, G., & van Ryzin, G. (1994). Optimal dynamic pricing of inventories with stochastic demand over finite horizons. *Management Science*, 40(8), 999–1020.
13. Bandalouski, A. M., et al. (2021). Multi-period dynamic pricing MIP formulation.
14. Chen, B., et al. (2026). Bandit algorithms for price exploration.
15. Luo, Y., et al. (2022). Online pricing with strategic consumers.
16. Zhu, R., et al. (2022). Dynamic pricing with demand learning.

### カテゴリE: 感情分析手法

17. Birjali, M., Kasri, M., & Beni-Hssane, A. (2021). A comprehensive survey on sentiment analysis: Approaches, challenges and trends. *Knowledge-Based Systems*, 226, 107134.
18. Do, H. H., et al. (2019). Deep learning for aspect-based sentiment analysis: A comparative review. *Expert Systems with Applications*, 118, 272–299.
19. Sun, C., Huang, L., & Qiu, X. (2019). Utilizing BERT for aspect-based sentiment analysis via constructing auxiliary sentence. *arXiv*:1903.09588.
20. Liang, B., et al. (2022). Aspect-based sentiment analysis via affective knowledge enhanced graph convolutional networks. *Knowledge-Based Systems*, 235, 107643.
20a. Zhang, W., Deng, Y., Liu, B., Pan, S. J., & Bing, L. (2023). Sentiment Analysis in the Era of Large Language Models: A Reality Check. *arXiv*:2305.15005.

### カテゴリF: DP障壁・HITL・XAI

21. Anisi, M., et al. (2024). Agent-based modeling of dynamic pricing acceptance. (ABM simulation)
22. Ivanov, S., & Webster, C. (2024). Human-in-the-loop AI for hospitality. (84 citations)
23. Mohammed, A., & Denizci Guillet, B. (2025b). XAI for hotel pricing explanation.
24. Liu, Y., et al. (2025). LLMs for price prediction: LLM fails at numerical price calculation.

### カテゴリG: ボラティリティ・統計手法

25. Andersen, T. G., & Bollerslev, T. (1998). Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts. *International Economic Review*, 39(4), 885–905.
26. Roll, R. (1984). A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market. *Journal of Finance*, 39(4), 1127–1139.
27. Granger, C. W. J. (1969). Investigating Causal Relations by Econometric Models and Cross-spectral Methods. *Econometrica*, 37(3), 424–438.
28. Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems (NeurIPS)*, 30, 4765–4774.

### カテゴリH: データセット

29. Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel Booking Demand dataset. *Data in Brief*, 22, 41–49. Kaggle.
30. Alam, M. H., et al. (2016). TripAdvisor hotel review dataset.
31. Jimenez, L. (2017). 515K Hotel Reviews in Europe. Kaggle. https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe
32. Inside Airbnb. http://insideairbnb.com/get-the-data

### カテゴリI: 口コミ → 価格/売上エビデンス（§1.3根拠）

33. Ye, Q., Law, R., & Gu, B. (2009). The impact of online user reviews on hotel room sales. *International Journal of Hospitality Management*, 28(1), 180–182. (被引用2,146)
34. Ye, Q., Law, R., Gu, B., & Chen, W. (2011). The influence of user-generated content on traveler behavior. *Computers in Human Behavior*, 27(2), 634–639. (被引用2,002)
35. Anderson, C. K. (2012). The impact of social media on lodging performance. *Cornell Hospitality Report*, 12(15), 6–11. (被引用609)
36. Öğüt, H., & Onur Taş, B. K. (2012). The influence of internet customer reviews on the online sales and prices in hotel industry. *The Service Industries Journal*, 32(2), 197–214. (被引用624)
37. Torres, E. N., Singh, D., & Robertson-Ring, A. (2015). Consumer reviews and the creation of booking transaction value: Lessons from the hotel industry. *International Journal of Hospitality Management*, 50, 73–83. (被引用228)
38. Castro, C., & Ferreira, F. A. F. (2018). Online hotel ratings and its influence on hotel room rates: Evidences from Lisbon, Portugal. *Tourism & Management Studies*, 14(S1), 63–72. (被引用70)
39. Gibbs, C., Guttentag, D., Gretzel, U., Morton, J., & Goodwill, A. (2018). Pricing in the sharing economy: A hedonic pricing model applied to Airbnb listings. *Journal of Travel & Tourism Marketing*, 35(1), 46–56.

### カテゴリJ: 季節性・イベント駆動（§1.3根拠）

40. Talón-Ballestero, P., Nieto-García, M., et al. (2022). The wheel of dynamic pricing: Towards open pricing and one to one pricing in hotel revenue management. *International Journal of Hospitality Management*, 103, 103213. (被引用65)
41. Katz, H., Savage, E., & Coles, P. (2025). Lead times in flux: Analyzing Airbnb booking dynamics during global upheavals (2018–2022). *Annals of Tourism Research Empirical Insights*, 6(1), 100099. (被引用8)

### その他

42. Han, S.-L., et al. (2024). Word-of-mouth text mining for pricing.
43. Liu, C., et al. (2026). Sentiment segmentation for dynamic pricing.
44. Gómez-Talal, I., et al. (2025). Review integration for pricing strategy.
45. Correa, J. R., et al. (2024). Dynamic pricing with consumer reviews.
46. Habbat, N., et al. (2022). Sentiment-aware recommendation.
47. Nandinli, T., et al. (2024). BiLSTM for review-based prediction.
48. Ray, B., et al. (2026). Sentiment-informed pricing decision system.
49. Wang, X., et al. (2021). Dynamic pricing with inventory and demand.

---

## 付録A: 技術的比較サマリ

### 既存研究の手法比較テーブル

| 研究 | ドメイン | データ規模 | ABSA手法 | アスペクト数 | 予測モデル | R² | ABSAの価格モデル統合 |
|:---|:---|:---:|:---|:---:|:---|:---:|:---:|
| Degife & Lin (2024) | 航空運賃 | 841K取引+46K口コミ | BERT抽出→9グループ | 9 | 7層GRU | 0.9899 | **✓ 直接統合** |
| Di Persio & Lalmi (2024) | Airbnb (ローマ) | 75列+22Kレビュー | CNN-ABSA (HOST) | 1(HOST) | XGBoost/SVR/NN | 未公開 | ✗ 定性分析のみ |
| Wu et al. (2022) | ホテル (マカオ) | 4ホテル | 全体感情 | ― | LSTM | 改善確認 | △ 全体スコアのみ |
| **本研究（提案）** | **宿泊施設（地方）** | **Inside Airbnb** | **LLM→BERT→7アスペクト** | **7** | **XGBoost+Quantile** | **検証対象** | **✓ 直接統合+ボラティリティ** |

### 本研究の位置づけ

```
                    ABSA感情→価格モデル統合
                    ✓                    ✗
                ┌─────────────────┬────────────────────┐
  宿泊施設      │ ★本研究（提案）  │ Di Persio (2024)   │
  ドメイン      │   新規ポジション   │ Özen (2023)        │
                │                 │ Zhang (2021)       │
                ├─────────────────┼────────────────────┤
  非宿泊施設    │ Degife (2024)   │ 多数のABSA研究     │
  ドメイン      │ (航空運賃)       │                    │
                └─────────────────┴────────────────────┘
```

**本研究は、ABSA感情スコアを宿泊施設価格予測に直接統合した最初の研究を目指す。**

---

## 付録B: 用語集

| 用語 | 定義 |
|:---|:---|
| ABSA | Aspect-Based Sentiment Analysis — テキストからアスペクト（観点）ごとの感情極性を抽出する技術 |
| DP | Dynamic Pricing — 需給・時間等に応じて価格を動的に変更する戦略 |
| ボラティリティ | 価格やスコアの時間変動の度合い。金融では対数リターンのσで定義 |
| CV | Coefficient of Variation — 変動係数。標準偏差/平均。スケール不変の変動指標 |
| SHAP | SHapley Additive exPlanations — 各特徴量のモデル予測への個別貢献度を算出する手法 |
| Quantile Regression | 条件付き分位点を推定する回帰手法。不確実性区間の推定に使用 |
| Granger因果 | 時系列Xの過去がYの予測に有意に寄与するかの統計検定 |
| Inside Airbnb | Airbnbのリスティング・レビュー・カレンダーデータを公開するオープンソースプロジェクト |
| PICP | Prediction Interval Coverage Probability — 予測区間が実測値をカバーする確率 |
