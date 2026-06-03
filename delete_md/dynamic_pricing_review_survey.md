# ダイナミックプライシングと口コミ分析に関する既存研究の体系的調査

---

## 1. 口コミ（レビュー・感情）を活用したダイナミックプライシング研究

### 1.1 Shin, Vaccari, & Zeevi (2023) — Dynamic Pricing with Online Reviews

- **論文情報**: Shin, D., Vaccari, S., & Zeevi, A. (2023). "Dynamic Pricing with Online Reviews." *Management Science*, 69(2), 1032–1053. doi:10.1287/mnsc.2022.4387
- **被引用数**: 110件以上（2026年4月時点）

#### 研究背景

オンラインマーケットプレイスにおいて、消費者の購買意思決定にレビューが強く影響する状況下で、販売者がどのように価格を動的に調整すべきかという問題を扱う。レビューは消費者の「製品品質に対する信念」を形成するシグナルとして機能する。この研究では、レビューが価値ベース（value-based）である場合、すなわち消費者の事後的な評価を反映する場合に焦点を当て、ダイナミックプライシングの価値を理論的に分析している。

#### 手法

モデル構造は、販売者と消費者の双方がベイズ的に製品品質 $\theta$ についての信念を更新するフレームワークである。

- **需要モデル**: 消費者は製品品質の事前分布 $\theta \sim F_0$ を持ち、過去のレビュー $r_1, r_2, \ldots, r_{t-1}$ を観測してベイズ更新を行う。消費者 $t$ は、期待効用 $\mathbb{E}[\theta | r_1, \ldots, r_{t-1}] - p_t \geq 0$ のとき購入する。
- **レビュー生成**: 購入した消費者は、製品品質に依存したノイズ付き信号 $r_t = \theta + \epsilon_t$ をレビューとして公開する。$\epsilon_t$ は独立な平均ゼロのノイズ。
- **販売者の最適化**: 販売者は割引累積利益 $\sum_{t=1}^{T} \delta^{t-1} p_t \cdot D_t(p_t)$ を最大化する。ここで $D_t(p_t)$ は時点 $t$ における需要関数であり、レビュー履歴に依存する。
- **価格決定ロジック**: 最適価格は消費者の事後的な品質推定値 $\hat{\theta}_t$ に依存し、$p_t^* = \hat{\theta}_t / 2$（線形需要の場合）のような構造を持つ。

#### 主な結果

- ダイナミックプライシングの価値（固定価格に対する利益の改善率）は、レビューの情報量が「中程度」の場合に最大となる。レビューが極めて情報量豊富（品質がすぐに判明する）な場合やほぼ無情報の場合には、動的価格設定の付加価値は低い。
- 最適な動的価格政策では、初期に低い「紹介価格」を設定してレビュー蓄積を促進し、品質が判明した後に価格を引き上げるという時間的構造が現れる。

#### 限界・今後の課題

- 消費者の戦略的行動（将来の価格低下を見越して購入を遅延する行動）は考慮されていない。
- レビューの操作（fake reviews）や選択バイアス（購入者のみがレビューを書く）の問題は扱われていない。
- 複数製品・競争環境への拡張が未解決である。

---

### 1.2 Correa, Mari, & Xia (2024) — Dynamic Pricing with Bayesian Updates from Online Reviews

- **論文情報**: Correa, J., Mari, M., & Xia, A. (2024). "Dynamic Pricing with Bayesian Updates from Online Reviews." *arXiv preprint*, arXiv:2404.14953. [cs.LG]
- **被引用数**: 5件（2026年4月時点）

#### 研究背景

新製品の市場投入時には品質が不確実であり、レビューを通じて消費者と販売者の双方が品質を学習する。このモデルは、Shin et al. (2023)のフレームワークを拡張し、販売者の価格設定問題をバンディット問題として定式化する点に独自性がある。

#### 手法

- **モデル構造**: 製品品質 $\theta \in \{H, L\}$（高品質/低品質の2値）を仮定し、販売者と消費者がベイズ更新で信念を形成する。
- **バンディット定式化**: 販売者の意思決定を"basic bandits problem"として定式化する。各時点で価格を選択し、レビューからのフィードバック（購入/非購入、レビュー内容）を観察する。
- **カタラン数との接続**: 販売者の将来割引報酬の計算がカタラン数（Catalan numbers）と密接に関連することを証明した。これにより、最適方策の効率的な計算が可能となる。具体的には、品質学習の各経路における購入/非購入の組み合わせ数がカタラン数 $C_n = \frac{1}{n+1}\binom{2n}{n}$ に従う。
- **静的 vs 動的価格の比較**: 最適な静的価格（固定価格）と最適な動的価格を、品質の学習確率の観点から比較分析する。

#### 主な結果

- 動的価格設定は、製品品質の効果的な学習確率を高めることが示された。
- カタラン数を用いた閉じた形の報酬計算が可能であり、計算効率が高い。
- 静的/動的の両方の最適価格に対する明示的な特性付けを提供。

#### 限界・今後の課題

- 品質が2値であるという単純化された仮定を使用。連続的品質へ拡張が必要。
- 消費者の異質性（valuationの分布が異なる消費者群）は考慮されていない。
- 実データを用いた検証が行われていない。

---

### 1.3 Han, Guo, Yu, & Li (2024) — Research on Dynamic Pricing and Long-term Profit of Companies under Influence of Word of Mouth

- **論文情報**: Han, F., Guo, Y., Yu, H., & Li, B. (2024). "Research on Dynamic Pricing and Long-term Profit of Companies under Influence of Word of Mouth." *Journal of Theoretical and Applied Electronic Commerce Research*, 19(3), 105. doi:10.3390/jtaer19030105
- **被引用数**: 5件

#### 研究背景

口コミ（Word of Mouth, WoM）が消費者の購買行動に影響を与え、それが長期的な企業利益に影響するメカニズムを検証する。特に、オンラインレビューからテキストマイニングで抽出される各種要因（positive/negative textual factors）が顧客満足に与える影響の非対称性に着目している。

#### 手法

- **テキスト分析**: オンラインレビューからポジティブ/ネガティブなテキスト要因を抽出する。全てのポジティブ要因が均等に満足度に寄与するわけではないことを実証的に示す。
- **需要関数**: 口コミの量と極性（valence）を説明変数として組み込んだ需要モデルを構築。需要は $D(p, WoM) = a - bp + c \cdot WoM_{pos} - d \cdot WoM_{neg}$ の形式で定式化される。
- **動的価格最適化**: 口コミのダイナミクス（過去のレビューが将来の需要に影響する遅延効果）を考慮した多期間利益最大化問題として定式化。

#### 主な結果

- 全てのポジティブなテキスト要因が顧客満足に有意に影響するわけではない。ネガティブ要因もまた、影響度が一様ではない。
- 口コミの影響を組み込んだ動的価格設定は、長期利益の観点で、口コミを無視した固定価格戦略を上回る。

#### 限界・今後の課題

- テキスト分析の粒度がaspectレベルまで到達しておらず、感情分析の精度に改善の余地がある。
- 競合他社のレビューとの相互作用は考慮されていない。

---

### 1.4 Liu, Liu, Wang, & Xu (2026) — Consumer Segmentation and Pricing Optimisation with Online Reviews

- **論文情報**: Liu, S., Liu, Z., Wang, J., & Xu, L. (2026). "Consumer Segmentation and Pricing Optimisation with Online Reviews: A Sentiment Analysis-Based Decision-Making Framework." *Journal of the Operational Research Society*. doi:10.1080/01605682.2026.2630957

#### 研究背景

オンラインレビューの感情分析結果を用いて消費者をセグメンテーションし、各セグメントの価格感応度に基づいた差別的価格設定（differential pricing）を行うフレームワークを提案する。従来モデルがレビューの集計的指標（平均星評価）のみを使用していた限界を克服する。

#### 手法

- **消費者セグメンテーション**: 感情分析により消費者を感情極性パターンで分類。各セグメント内の価格感応度（price sensitivity）パラメータを推定する。
- **差別的価格モデル**: 各セグメントに対して異なる価格 $p_k$ を設定し、小売業者の利益 $\Pi = \sum_{k=1}^{K} (p_k - c) \cdot D_k(p_k)$ を最大化する。ここで $D_k$ はセグメント $k$ の需要関数。
- **感情スコアの活用**: レビューから抽出した感情スコアを、消費者の品質認知のプロキシとして需要関数に組み込む。

#### 主な結果

- 感情ベースのセグメンテーションにより、均一価格設定と比較して小売業者の利益が改善されることを、数値実験で検証。
- レビュー感情に基づく消費者分類が、従来の人口統計学的セグメンテーションよりも需要予測精度が高いケースがあることを示した。

#### 限界・今後の課題

- セグメンテーションの動的性質（消費者のセグメント帰属が時間とともに変化する可能性）は未対応。
- 競争市場における適用可能性が未検証。

---

### 1.5 Gómez-Talal, Talón-Ballestero, & Leoni (2025) — The Impact of Dynamic Pricing on Restaurant Customers' Perceptions and Price Sentiment

- **論文情報**: Gómez-Talal, I., Talón-Ballestero, P., & Leoni, V. (2025). "The Impact of Dynamic Pricing on Restaurant Customers' Perceptions and Price Sentiment." *Tourism Review*, 80(5), 1101. doi:10.1108/TR-08-2024-0584
- **被引用数**: 11件

#### 研究背景

レストラン産業におけるダイナミックプライシングの導入が、消費者のレビューの感情極性にどのように影響するかを実証的に分析する。ダイナミックプライシングは航空・ホテル産業では広く普及しているが、レストラン産業では消費者の受容度が十分に理解されていない。

#### 手法

- **感情分析**: ダイナミックプライシングを導入したレストランと導入していないレストランの顧客レビューに対して、事前学習済みモデルを用いた感情分析を適用。
- **頻出語分析**: レビュー中の最頻出語句を抽出し、ダイナミックプライシングに対する消費者の言及パターンを特定。
- **比較分析**: DP導入前後、およびDP導入店と非導入店の間で、感情スコアの差を統計的に検定。

#### 主な結果

- ダイナミックプライシング導入後もレストランの顧客レビューの全体的な感情極性は大きく低下しない。
- 価格に関する否定的な言及は存在するが、サービス品質や料理に関するポジティブな感情がそれを補償する傾向がある。
- レベニューマネジメント手法をレストランに適用する際の消費者受容の条件を実証的に示した。

#### 限界・今後の課題

- 対象がスペイン国内のレストランに限定されており、一般化に限界がある。
- 感情分析の手法がaspectレベルまで踏み込んでいない。
- 長期的な顧客ロイヤルティへの影響は追跡されていない。

---

### 1.6 Anisi, Kremer, & Olafsson (2024) — Insights from Dynamic Pricing Scenarios for Multiple-Generation Product Lines

- **論文情報**: Anisi, A., Kremer, G.O., & Olafsson, S. (2024). "Insights from Dynamic Pricing Scenarios for Multiple-Generation Product Lines with an Agent-Based Model Using Text Mining and Sentiment Analysis." *International Journal of Advances in Production Research*, 2024. doi:10.22032/dbt.59756
- **被引用数**: 13件

#### 研究背景

多世代製品ライン（例：Apple iPhoneの異なるバージョン）のダイナミックプライシングにおいて、消費者レビューの感情が需要と代替効果に与える影響をエージェントベースモデル（ABM）でシミュレーションする。

#### 手法

- **第1フェーズ — テキストマイニング**: Rプログラミング言語を使用し、Appleコミュニティフォーラムの2021年消費者レビューに対して感情分析を実施。レビューのpolarity（positive/negative/neutral）を分類。
- **第2フェーズ — エージェントベースモデル**: 消費者エージェントの購買行動をシミュレーション。各エージェントは、価格、製品世代、および感情スコアに基づいて購買意思決定を行う。
- **需要モデル**: 代替効果（substitution effect）を考慮した需要モデルを提案。一つの世代の需要が他の世代の価格と感情スコアに依存する。$D_i = f(p_i, p_j, S_i, S_j)$ の形式で、$S_i$ はworld代 $i$ の感情スコア。
- **価格シナリオ**: 複数の価格設定シナリオ（skimming, penetration, dynamicなど）を比較。

#### 主な結果

- 感情スコアを考慮した需要モデルは、感情を無視したモデルと比較して動的価格シナリオの評価精度が向上する。
- 旧世代製品のポジティブな感情は、新世代への移行を遅らせるカニバリゼーション効果を生む。

#### 限界・今後の課題

- ABMのパラメータ設定が実データとの整合性を十分に検証されていない。
- ABSAレベルの分析は行われておらず文書レベルの感情分析にとどまる。

---

## 2. ABSA（Aspect-Based Sentiment Analysis）を用いた価格・需要モデル研究

### 2.1 Degife & Lin (2024) — A Multi-Aspect Informed GRU: A Hybrid Model of Flight Fare Forecasting with Sentiment Analysis

- **論文情報**: Degife, W.A. & Lin, B.-S. (2024). "A Multi-Aspect Informed GRU: A Hybrid Model of Flight Fare Forecasting with Sentiment Analysis." *Applied Sciences*, 14(10), 4221. doi:10.3390/app14104221
- **被引用数**: 10件

#### 研究背景

航空運賃の予測に際して、従来手法は取引データ（便名、クラス、距離、季節性）のみに依拠していたが、消費者のサービスに対する評価（安全性、座席、食事、接客対応）が運賃動態に影響を与える可能性がある。ABSAにより各サービス属性（aspect）ごとの感情を数値化し、運賃予測モデルに統合することを目的とする。

#### 手法

**（1）Aspect抽出方法**:
- 事前学習済みBERTモデルを使用し、46,167件の消費者レビュー（2018年1月〜2023年7月、SkytraxおよびTripAdvisor）からaspect語（例: safety, seat, comfort, food, crew, baggage, customer service）を自動抽出。
- トークン化およびストップワード除去の前処理を実行。

**（2）Aspect分類**:
- 抽出されたaspectを航空管理の観点から9つのグループに統合：Booking & Ticketing, Pre-flight Procedures, Airport Services, In-flight Amenities, Seat & Cabin Features, Staff, Safety & Security, Cleanliness, Post-flight Services。

**（3）Sentiment推定方法**:
- 各レビューの感情スコアを以下の式で計算:

$$s_l = \sum_{a_i \in A_l} w_i \cdot s_{a_i}$$

$$s_{a_i} = n^+_{a_i} - n^-_{a_i}$$

ここで $A_l$ はレビュー $l$ に含まれるaspectの集合、$w_i$ はaspect $a_i$ の重み、$n^+_{a_i}$, $n^-_{a_i}$ はそれぞれポジティブ/ネガティブなエビデンスの数。

**（4）GRUモデルへの統合**:
- 7層のスタック型GRUモデル（ユニット数: 824, 512, 256, 128, 64, 32, 16）を構築。
- 入力特徴量は、航空運賃取引データの属性（便名、クラス、距離、季節など）に加え、ABSAで得られた各aspectグループの感情スコアを含む94次元ベクトル。
- GRUの各ゲートの数式:

$$z_t = \sigma(W_z x_t + U_z h_{t-1} + b_z)$$
$$r_t = \sigma(W_r x_t + U_r h_{t-1} + b_r)$$
$$\tilde{h}_t = \tanh(W_h x_t + U_h(r_t \odot h_{t-1}) + b_h)$$
$$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$$

- 活性化関数: ReLU、最適化: Adam（学習率0.001）、エポック数: 1400、バッチサイズ: 450。

#### 技術的ポイント（従来手法との差分）

- 従来の運賃予測モデル（MLP、LSTM、基本GRU）がaspect感情を入力に含まない点に対し、ABSAスコアを追加入力とする「ABSA_GRU」モデルを提案。
- 感度分析（sensitivity analysis）により、各aspectグループの運賃予測への寄与度を定量化。Safety & Securityを除外するとR²が0.9899から0.6752に急落し、このaspectが運賃予測に最も影響するaspectであることを示した。

#### 主な結果

- ABSA_GRUモデルの性能: RMSE = 0.0071, MAE = 0.0137, R² = 0.9899（全aspectを含む場合）。
- ABSA非統合GRUモデルと比較して、RMSE、MAE、R²のいずれにおいても改善。
- 7日間予測でRMSE = 0.0072, R² = 0.9769; 30日間予測でRMSE = 0.0881, R² = 0.8143と、期間が長くなるにつれて予測精度が低下する傾向。

#### 限界・課題

- フライト運賃取引データがプライバシー上の理由で非公開であり、再現性に制約がある。
- ABSAモデル自体の精度（aspect抽出および感情分類の精度）に関する詳細な評価が不足。
- 外部要因（燃料価格、為替変動、パンデミック）の影響は明示的にモデル化されていない。
- 動的な価格最適化（prescriptive analytics）ではなく、価格予測（predictive analytics）にとどまっている。

---

### 2.2 Di Persio & Lalmi (2024) — Maximizing Profitability and Occupancy: An Optimal Pricing Strategy for Airbnb Hosts

- **論文情報**: Di Persio, L. & Lalmi, E. (2024). "Maximizing Profitability and Occupancy: An Optimal Pricing Strategy for Airbnb Hosts Using Regression Techniques and Natural Language Processing." *Journal of Risk and Financial Management*, 17(9), 414. doi:10.3390/jrfm17090414
- **被引用数**: 8件

#### 研究背景

Airbnbの物件オーナーにとって、収益最大化と稼働率維持のバランスが重要な課題である。物件特性（立地、部屋数、アメニティ）に加え、ゲストレビューの内容が物件の市場価値に影響する。ABSAを用いてレビューから特定のaspect（ホストの対応、清潔さ、立地など）ごとの感情を抽出し、価格予測モデルの特徴量として活用する。

#### 手法

**（1）Aspect抽出・感情推定**:
- ローマ（イタリア）のAirbnbデータ（Inside Airbnb, 2023年5月時点）を使用。約1,048,576件のレビューから22,564件の英語レビューを分析対象とした。
- BoW（Bag-of-Words）およびTF-IDFによるキーワード分析に加え、ABSAとして1次元CNNモデル（カーネルサイズ3、ReLU活性化関数、ドロップアウト率0.2）を適用。
- 「HOST-GENERAL」aspectに焦点を当て、各レビューをPositive / Negative / Neutralの3極性に分類。結果として約93%のレビューがポジティブ感情。

**（2）価格予測への組み込み**:
- XGBoost、SVR（Support Vector Regression）、ニューラルネットワーク（2層全結合、各64ニューロン、学習率0.078、ドロップアウト率0.4、50エポック）で価格を予測。
- Forward Feature Selection（FFS）で上位10特徴量を選定。レビュー数（number of reviews）やレビューの立地スコア（review score for location）が重要な特徴量として選出。

#### 技術的ポイント

- PCA（主成分分析）とFFSの比較を行い、FFSがR²指標で27%の改善を達成。
- ABSAの結果は直接的に価格予測モデルの数値的特徴量としてではなく、ホスト行動の改善指針として活用される「解釈支援型」の統合アプローチ。
- これは、ABSAスコアを直接需要関数に埋め込むDegife & Lin (2024)とは異なるアプローチ。

#### 主な結果

- ニューラルネットワークが最も高い精度（MAE最低、R²最高）を達成。
- ゲストにとって立地が最も重要な価格決定要因であり、レビュースコアも有意に寄与。
- ABSAの結果として、ホストの対応が93%ポジティブであるが、残りの7%は対応の遅さ、プライバシー侵害、虚偽広告が原因。

#### 限界・課題

- ABSAの対象がHOST-GENERALの1aspect のみであり、他のaspect（清潔さ、設備、立地の詳細など）への拡張が必要。
- ローマのデータのみであり、他都市・他文化圏への一般化は未検証。
- 動的な価格設定への拡張はされておらず、静的な価格予測にとどまっている。

---

### 2.3 Ray, Singh, & Dash (2026) — Quantifying Consumer Perceptions in Smartwatch Markets: Integrating ABSA with Panel Data Modelling

- **論文情報**: Ray, R.K., Singh, A., & Dash, D.P. (2026). "Quantifying Consumer Perceptions in Smartwatch Markets: Integrating Aspect-Based Sentiment Analysis with Panel Data Modelling." *Journal of Enterprise Information Management*. doi:10.1108/JEIM-05-2025-0403

#### 研究背景

スマートウォッチ市場において、消費者のオンラインレビューから抽出されるaspect-sentimentペアが、製品の市場パフォーマンス（売上や価格プレミアム）にどのように影響するかを定量化する。ヘドニック-効用フレームワーク（hedonic-utilitarian framework）に基づき、ヘドニックaspect（デザイン、外観）が効用的aspect（バッテリー、正確さ）よりも消費者知覚に対する寄与が大きいかを検証する。

#### 手法

**（1）ABSA**:
- 事前学習済みBERTベースのモデルを用い、各レビューからaspect-sentimentペアを抽出。positive, negative, neutralの3分類。
- few-shot learningアプローチでアルゴリズムを適応させ、ドメイン固有のaspectを効率的に識別。

**（2）パネルデータモデル**:
- 抽出されたaspect-sentimentスコアを独立変数とし、製品の月次売上高または価格プレミアムを従属変数としたパネルデータ回帰分析を実施。
- 固定効果モデルおよびランダム効果モデルを比較。

#### 技術的ポイント

- ABSAとパネルデータ分析の組み合わせにより、因果的解釈に近い知見を得ようとしている点がユニーク。
- ヘドニック-効用フレームワークを用いたaspectの分類体系を導入。

#### 限界・課題

- スマートウォッチという単一カテゴリーに限定されており、他のカテゴリーへの一般化は検証されていない。
- パネルデータの期間や製品数に関する詳細が限定的。

---

### 2.4 Degife & Lin (2023) + Habbat et al. (2022) — Hotel Demand Forecasting via Booking's Comments Using Sentiment Analysis and Topic Modeling

- **論文情報**: Habbat, N., Anoun, H., Hassouni, L., & Nouri, H. (2022). "Hotel Demand Forecasting via Booking's Comments Using Sentiment Analysis and Topic Modeling Techniques." *International Conference on Advanced Intelligent Systems for Sustainable Development* (AI2SD), pp. 113–126. Springer.

#### 研究背景

ホテルの需要予測において、Booking.comのレビューテキストから抽出される感情とトピック情報が、従来の構造化データ（価格、曜日、季節）に基づく予測モデルを補完できるかを検証する。

#### 手法

- LDA（Latent Dirichlet Allocation）によるトピックモデリングとsentiment分析を組み合わせ、レビューから多言語aspectの認識を試みる。
- 抽出されたトピック分布と感情スコアを、需要予測モデル（回帰分析）の追加特徴量として使用。

#### 技術的ポイント

- 多言語レビュー（フランス語、英語など）からPOSタグを抽出してaspectを認識するパイプラインを提案。
- トピックモデリングとABSAのハイブリッドアプローチ。

#### 限界・課題

- LDAによるトピック抽出はaspect粒度が荒い場合があり、BERTベースのABSAと比較して精度が劣る。
- 需要予測の精度向上度合いが定量的に十分報告されていない。

---

### 2.5 Nandinli, Srinu, & Senthil (2024) — Sentiment-Driven Predictions with Bi-Directional LSTM for Hotel Demand Forecasting

- **論文情報**: Nandinli, A.S., Srinu, N., & Senthil, M. (2024). "Sentiment-Driven Predictions with Bi-Directional LSTM for Hotel Demand Forecasting." *International Journal of Management and Economics*, 2024.

#### 研究背景

ホテル需要予測を、(1) データソースからの共通特性発見、(2) 予測モデルの情報形成と方向付けの2観点から分析し、感情分析を時系列モデルに統合する。

#### 手法

- Bi-directional LSTM（BiLSTM）をベースとした時系列予測モデルに、レビューの感情特徴量を追加入力として統合。
- 順方向および逆方向のLSTMセルにより、過去と将来のコンテキストの両方を捉える。

#### 技術的ポイント

- BiLSTMの双方向構造が、レビュー感情の時間的変化パターン（例：特定イベント後の感情悪化）を効果的に捕捉。

#### 限界・課題

- ABSAではなく文書レベルの感情分析にとどまっている。
- ホテルの種類やクラスによるモデルの適合度の差異が十分に議論されていない。

---

## 3. 代表的なダイナミックプライシングモデル（レビューなし）

### 3.1 伝統的レベニューマネジメント：Gallego & van Ryzin (1994)

- **論文情報**: Gallego, G. & van Ryzin, G. (1994). "Optimal Dynamic Pricing of Inventories with Stochastic Demand over Finite Horizons." *Management Science*, 40(8), 999–1020.
- **被引用数**: 3,000件以上

#### 実装背景

航空券・ホテル客室などの腐敗性在庫（perishable inventory）を対象とした、有限期間における最適動的価格設定の基礎理論を確立した論文。販売期限を過ぎると価値がゼロになる財について、残存在庫と残存期間に応じて最適価格を動的に決定する。

#### 手法

- **需要関数**: 需要は強度関数 $\lambda(p)$ に従うポアソン過程でモデル化される。$\lambda(p)$ は価格 $p$ に対して単調減少であり、$p \cdot \lambda(p)$ は凹関数（収益率関数が凹）であると仮定。
- **状態空間**: 状態は残存在庫 $n$ と残存時間 $t$。
- **ベルマン方程式**: 最適価格は以下の最適性方程式を満たす:

$$V_t(n) = \max_p \left\{ \lambda(p) \cdot [p + V_{t-1}(n-1) - V_{t-1}(n)] + [1 - \lambda(p)] \cdot V_{t-1}(n) \right\}$$

ここで $V_t(n)$ は在庫 $n$ を時間 $t$ だけ残して販売する場合の最適期待収益。

- **最適価格**: 最適価格は $p^*(n, t) = \arg\max_p \lambda(p)(p - \Delta V)$ で与えられ、$\Delta V = V_{t-1}(n) - V_{t-1}(n-1)$ はオポチュニティコスト（1単位を今売ることの機会費用）。

#### 長所

- 閉じた形の解析解が得られる場合がある（指数型需要の場合）。
- 固定価格政策との比較で、ダイナミックプライシングの上界を理論的に提供。Gallego & van Ryzinは固定価格がダイナミックプライシングの期待収益の少なくとも $1 - 1/e \approx 63.2\%$ を達成することを証明。

#### 短所

- 需要関数の形状（特に凹収益率仮定）を事前に知っている必要がある。
- 消費者の戦略的行動や競合他社の存在を考慮していない。

#### 現代的課題

- データ駆動的な需要推定との統合（demand learning）が重要な拡張方向。
- AI・機械学習による需要関数のノンパラメトリック推定との接続。

---

### 3.2 Wang, Chen, & Simchi-Levi (2021) — Multimodal Dynamic Pricing

- **論文情報**: Wang, Y., Chen, B., & Simchi-Levi, D. (2021). "Multimodal Dynamic Pricing." *Management Science*, 67(10), 6136–6152. doi:10.1287/mnsc.2020.3819
- **被引用数**: 96件

#### 実装背景

需要関数が複数のモード（局所的最適価格）を持つ場合のダイナミックプライシング問題を扱う。従来の文脈付き動的価格設定の研究は、需要モデルの単峰性（unimodal）を仮定していたが、実際の市場では需要関数が多峰性を持つケースが存在する。

#### 手法

- **需要モデル**: $D_t = d(x_t, p_t; \theta^*) + \epsilon_t$ の形式で、$x_t$ はコンテキスト特徴量、$p_t$ は価格、$\theta^*$ は未知パラメータ、$\epsilon_t$ はノイズ。
- **リニアコンテキスト付きバンディットとの接続**: 需要関数が $d(x_t, p_t) = x_t^\top \beta + p_t \gamma$ の線形構造を持つ場合、線形コンテキスト付きバンディット（linear contextual bandit）問題に帰着する。
- **多峰性への対応**: 需要関数が複数の局所最適を持つ場合、explore-then-commit型やUCB型の探索戦略が非効率になるリスクがある。モード間を効率的に探索するアルゴリズムを提案。
- **リグレット解析**: $T$ 期間にわたる累積リグレットの上界 $O(\sqrt{T \log T})$ を導出。

#### 長所

- 需要関数の多峰性を明示的に扱った最初の動的価格設定研究の一つ。
- 線形コンテキスト付きバンディットとの接続により、既存アルゴリズムの応用が可能。

#### 短所

- 需要モデルの線形性仮定が依然として制約的。
- 非定常環境（需要パラメータが時間変動する場合）への対応が限定的。

---

### 3.3 Bu, Simchi-Levi, & Wang (2022) — Context-Based Dynamic Pricing with Partially Linear Demand Model

- **論文情報**: Bu, J., Simchi-Levi, D., & Wang, C. (2022). "Context-Based Dynamic Pricing with Partially Linear Demand Model." *Advances in Neural Information Processing Systems* (NeurIPS 2022).
- **被引用数**: 20件

#### 実装背景

ECやサービス産業において、製品の需要は価格だけでなく消費者特性（コンテキスト）にも依存する。従来の完全線形モデルでは、需要のコンテキスト依存構造を十分に捉えられない。

#### 手法

- **部分線形需要モデル（Partially Linear Model）**: $D_t = g(x_t) + p_t \cdot \beta + \epsilon_t$。ここで $g(\cdot)$ はコンテキスト $x_t$ に対する非パラメトリック関数、$\beta$ は価格係数。
- **学習アルゴリズム**: バイアス付き線形コンテキスト付きバンディット（biased linear contextual bandit）の手法を応用し、非パラメトリック部分 $g(\cdot)$ と線形部分 $\beta$ を同時推定する2段階手法を提案。
- **リグレット上界**: 部分線形構造を活用し、リグレット上界 $\tilde{O}(T^{(d_x+2)/(d_x+3)})$ を導出。ここで $d_x$ はコンテキストの次元。
- **リグレット下界**: マッチする下界も導出し、提案手法の最適性を示す。

#### 長所

- コンテキスト部分にノンパラメトリック構造、価格部分に線形構造を許容するセミパラメトリックモデルの導入。
- リグレットの上界と下界が一致（minimax optimal）。

#### 短所

- 非パラメトリック部分の推定にはコンテキスト次元 $d_x$ が増加すると次元の呪いが発生。
- 価格と需要の関係が線形であるという仮定は依然として制約的。

---

### 3.4 Chen, Simchi-Levi, & Wang (2026) — Utility Fairness in Contextual Dynamic Pricing with Demand Learning

- **論文情報**: Chen, X., Simchi-Levi, D., & Wang, Y. (2026). "Utility Fairness in Contextual Dynamic Pricing with Demand Learning." *Management Science*. doi:10.1287/mnsc.2023.03956
- **被引用数**: 22件

#### 実装背景

ダイナミックプライシングにおける公平性（fairness）の問題を扱う。異なる消費者グループ（人種、性別、地域などのセンシティブ属性）に対して異なる価格を設定することは、倫理的・法的に問題があるため、効用公平性制約の下での最適価格設定を研究する。

#### 手法

- **公平性制約付きContextual Bandit**: コンテキスト $x_t$ に基づく動的価格設定において、異なるセンシティブグループ間の効用格差を制約に加える。
- **需要モデル**: $D_t = x_t^\top \theta^* - \alpha \cdot p_t + \epsilon_t$（線形需要）。
- **公平性定義**: 効用公平性（Utility Fairness）として、各グループ $g$ の平均消費者余剰 $U_g = \mathbb{E}[v_g - p_g]$ が均等になるように制約。
- **アルゴリズム**: 公平性制約を満たしつつ、最適リグレット上界 $\tilde{O}(\sqrt{T})$ を達成するアルゴリズムを提案。

#### 長所

- ダイナミックプライシングにおけるアルゴリズム的公平性を厳密に定式化した先駆的研究。
- 最適なリグレット上界を達成しつつ公平性を保証。

#### 短所

- 公平性の定義が効用ベースに限定されており、他の公平性概念（例：価格公平性、機会の平等）との比較が不十分。
- 線形需要の仮定。

#### 現代的課題

- AI駆動のパーソナライズド価格設定における差別防止は、規制当局の関心事項であり、今後の法的・倫理的フレームワークとの整合が必要。

---

### 3.5 Luo, Sun, & Liu (2022) — Contextual Dynamic Pricing with Unknown Noise

- **論文情報**: Luo, Y., Sun, W.W., & Liu, Y. (2022). "Contextual Dynamic Pricing with Unknown Noise: Explore-then-UCB Strategy and Improved Regrets." *Advances in Neural Information Processing Systems* (NeurIPS 2022).
- **被引用数**: 26件

#### 実装背景

多くの動的価格設定の理論研究は、ノイズ分布が既知であることを仮定しているが、実務ではノイズの分布やサポートが不明な場合が多い。

#### 手法

- **需要モデル**: $D_t = x_t^\top \theta^* + \alpha p_t + \epsilon_t$。ノイズ $\epsilon_t$ の分布は未知。
- **Explore-then-UCB戦略**: 初期探索フェーズで価格をランダムに設定してノイズ分布を推定し、その後UCB（Upper Confidence Bound）型アルゴリズムに移行する2段階戦略。
- **適応的ビニング**: ノンパラメトリックコンテキスト付きバンディットの適応的ビニング手法を応用し、コンテキスト空間を適応的に分割。
- **リグレット**: サブガウシアンノイズの仮定の下で、$\tilde{O}(d^{2/3} T^{2/3})$ のリグレット上界を導出（$d$ は特徴量次元）。

#### 長所

- ノイズ分布の知識を必要としない実用的な設定での理論保証。
- 2段階戦略の各フェーズのサンプル数配分を理論的に最適化。

#### 短所

- リグレット率が $O(\sqrt{T})$ に到達していない（$O(T^{2/3})$）点で、既知ノイズの場合と比較してギャップがある。

---

### 3.6 Zhu, Xiao, Yu, Wang, Chen, & Lu (2022) — Modeling Price Elasticity for Occupancy Prediction in Hotel Dynamic Pricing

- **論文情報**: Zhu, F., Xiao, W., Yu, Y., Wang, Z., Chen, Z., & Lu, Q. (2022). "Modeling Price Elasticity for Occupancy Prediction in Hotel Dynamic Pricing." *Proceedings of the 31st ACM International Conference on Information & Knowledge Management* (CIKM 2022), pp. 3659–3668.
- **被引用数**: 16件

#### 実装背景

ホテルのダイナミックプライシングにおいて、価格弾力性を用いた稼働率予測モデルを構築する。従来の需要予測モデルが価格変動の影響を直接的にモデル化していない問題を解決する。

#### 手法

- **需要関数**: 価格弾力性 $\epsilon$ を用いた需要モデル：

$$D(p) = D_0 \cdot \left(\frac{p}{p_0}\right)^{-\epsilon}$$

ここで $D_0$ はベース需要、$p_0$ はベース価格。

- **弾力性推定**: 過去の価格-需要データから、時間変動する弾力性パラメータ $\epsilon_t$ を推定。季節性、曜日効果、イベント効果を考慮。
- **稼働率予測**: 推定された弾力性を用いて、候補価格 $p$ に対する稼働率を予測し、収益 $R(p) = p \cdot D(p)$ を最大化する価格を選択。

#### 長所

- 実際のホテルチェーンのデータを用いた実証検証。
- 価格弾力性の時間変動を明示的にモデル化。

#### 短所

- 弾力性推定の精度がデータ量に依存し、新規ホテルや特殊期間のデータ不足時に不安定。
- 消費者の異質性（ビジネス客 vs レジャー客で弾力性が異なる）の明示的なモデル化は限定的。

---

### 3.7 Bandalouski, Egorova, Kovalyov et al. (2021) — Dynamic Pricing with Demand Disaggregation for Hotel Revenue Management

- **論文情報**: Bandalouski, A.M., Egorova, N.G., Kovalyov, M.Y., et al. (2021). "Dynamic Pricing with Demand Disaggregation for Hotel Revenue Management." *Journal of Heuristics*, 25, 753–783. doi:10.1007/s10732-021-09480-2
- **被引用数**: 20件

#### 実装背景

ホテルの需要を複数のセグメント（レジャー客、ビジネス客、団体客など）に分解（disaggregation）し、各セグメントごとに価格を最適化するモデルを提案。

#### 手法

- **需要の双方向性**: ホテルの価格が需要に影響し、需要が価格設定に影響するという双方向の関係を明示的にモデル化。
- **線形回帰ベース**: 各セグメントの需要関数を $D_k(p_k) = a_k - b_k \cdot p_k$ の線形モデルで推定。価格弾力性係数 $b_k$ はセグメント間で異なる。
- **最適化**: 全セグメントの総収益 $\sum_k p_k \cdot D_k(p_k)$ を、容量制約の下で最大化する。

#### 長所

- 需要分解アプローチにより、セグメント間の異なる価格感応度を活用。
- 実装が比較的シンプルで実務適用が容易。

#### 短所

- 線形需要関数は現実のS字型需要曲線を十分に捉えられない場合がある。
- セグメント間の需要の相互作用（カニバリゼーション）のモデル化が限定的。

---

### 3.8 Bu, Simchi-Levi, & Wang (2025) — Context-Based Dynamic Pricing with Separable Demand Models

- **論文情報**: Bu, J., Simchi-Levi, D., & Wang, C. (2025). "Context-Based Dynamic Pricing with Separable Demand Models." *Management Science*. doi:10.1287/mnsc.2022.02260
- **被引用数**: 12件

#### 実装背景

Bu et al. (2022, NeurIPS)の拡張として、コンテキストと価格の効果が分離可能（separable）な需要モデルにおける動的価格設定を研究する。

#### 手法

- **分離可能需要モデル**: $D_t = f(x_t) \cdot h(p_t) + \epsilon_t$。ここで $f(\cdot)$ はコンテキスト効果、$h(\cdot)$ は価格効果であり、積の形で分離される。
- **学習アルゴリズム**: コンテキスト付きバンディットのフレームワーク内で、$f$ と $h$ を段階的に推定する手法を提案。
- **リグレット解析**: 分離可能構造を活用したリグレット上界を導出。

#### 長所

- 完全な線形需要よりも柔軟性が高く、コンテキストと価格の交互作用を特定の方法で許容。

#### 短所

- 分離可能仮定は、コンテキストが価格弾力性自体を変化させるケース（例：富裕層は弾力性が低い）をモデル化できない。

---

### 3.9 Demand Learning の古典的フレームワーク

#### 3.9.1 Besbes & Zeevi (2009)

- **論文情報**: Besbes, O. & Zeevi, A. (2009). "Dynamic Pricing Without Knowing the Demand Function: Risk Bounds and Near-Optimal Algorithms." *Operations Research*, 57(6), 1407–1420.

- **手法**: 需要関数のパラメトリック形状を仮定せず、リグレット最小化の観点から動的価格設定を行う。Explore-then-exploit戦略で、初期に複数の価格を試し、推定された需要曲線に基づいて最適価格にコミットする。
- **リグレット**: $O(T^{2/3})$のリグレット上界を導出し、この率が情報理論的に最適であることを示した。
- **現代的意義**: ノンパラメトリック需要学習の基礎理論として、Bu et al. (2022)、Luo et al. (2022)を含む後続研究に大きな影響を与えた。

#### 3.9.2 Kleinberg & Leighton (2003)

- **論文情報**: Kleinberg, R. & Leighton, T. (2003). "The Value of Knowing a Demand Curve: Bounds on Regret for Online Posted-Price Auctions." *44th Annual IEEE Symposium on Foundations of Computer Science* (FOCS), pp. 594–605.

- **手法**: オンライン投稿価格オークションにおいて、需要曲線の知識なしに価格を逐次設定する問題を定式化。$O(\log \log T)$ の競争比を達成するアルゴリズムを提案。
- **現代的意義**: 動的価格設定のオンライン学習としての定式化における先駆的研究。

---

## 4. 総合整理

### 4.1 既存研究の構造的整理（3層構造）

既存研究は以下の3層構造で整理できる。

**第1層：理論的基盤（Classic Dynamic Pricing）**

Gallego & van Ryzin (1994)を原点とする在庫ベースの動的価格設定理論。需要関数が既知であることを前提とし、ベルマン方程式に基づく最適方策を導出する。この層の主な貢献は、ダイナミックプライシングの理論的上界の提供と、固定価格方策との性能比較である。

**第2層：需要学習と最適化の統合（Demand Learning + Pricing）**

Besbes & Zeevi (2009)、Wang, Chen, & Simchi-Levi (2021)、Bu et al. (2022, 2025)、Chen et al. (2026)を代表とする、需要関数が未知の状況において探索と活用のトレードオフを管理しながら価格を最適化する研究群。コンテキスト付きバンディットやオンライン学習理論を活用し、リグレット解析によって理論的保証を提供する。この層の主な進展は、部分線形モデル、分離可能モデル、公平性制約などの実践的拡張である。

**第3層：非構造化データの統合（Reviews/Sentiment + Pricing）**

Shin et al. (2023)、Correa et al. (2024)、Han et al. (2024)、Degife & Lin (2024)、Di Persio & Lalmi (2024)に代表される、オンラインレビューや感情分析の結果をダイナミックプライシングのフレームワークに統合する研究群。さらに、ABSAレベルの粒度で顧客感情を定量化し、需要モデルの特徴量として活用する最新の試みが含まれる。

### 4.2 現在の研究ギャップ（未解決問題）

1. **ABSAとダイナミックプライシングの直接的統合の不在**: Degife & Lin (2024)はABSAスコアを価格「予測」に使用しているが、ABSAスコアを動的な価格「最適化」（prescriptive analytics）に直接統合した研究は存在しない。第2層の需要学習理論と第3層の感情分析技術を橋渡しする統合フレームワークが欠如している。

2. **Aspectレベル価格弾力性の未解明**: 消費者の価格感応度が製品のaspect（例：ホテルの清潔さ、立地、サービス）によって異なる可能性が高いが、aspectごとの価格弾力性を推定した研究はない。「清潔さに不満のある消費者は価格に対してより弾力的になるか？」といった問いに対する定量的回答がない。

3. **レビューの動的性質の未モデル化**: レビューは時間とともに蓄積・変化するが、ほとんどの研究がレビューの静的なスナップショットを使用している。レビュー感情の時系列的変化が需要関数のパラメータにどのように影響するかを明示的にモデル化した研究は限られている。

4. **因果推定の欠如**: レビュー感情と需要の関係について、多くの研究が相関関係のみを示しており、因果的な影響を識別する研究が不足している。「ポジティブなレビューが需要を増加させるのか、需要が高い（人気のある）製品がポジティブレビューを集めやすいのか」という内生性の問題が未解決。

5. **多言語・多文化のABSA適用**: ホスピタリティ産業ではレビューが多言語で書かれるが、多言語ABSAを一貫して適用し、その結果を需要・価格モデルに統合した研究は少ない。

6. **公平性と説明可能性**: Chen et al. (2026)が公平性制約を導入しているが、レビュー感情を組み込んだ場合の公平性問題（特定の消費者グループが不利な感情を持ちやすい場合）、および感情ベースのダイナミックプライシングの説明可能性が未検討。

### 4.3 今後有望な研究方向

1. **ABSA統合型リアルタイムプライシング**: BERTベースのABSAモデルをリアルタイムレビューストリームに適用し、aspectごとの感情スコアの変化をコンテキスト付きバンディットの追加コンテキスト変数として組み込む。目的は、第2層（Bu et al., 2022のContextual Bandit）と第3層（Degife & Lin, 2024のABSA）を統合した、リグレット保証を持つ処方的価格最適化フレームワークの構築。

2. **Aspect-wise Price Elasticity Estimation**: ABSAで特定された各aspectの感情スコアと価格-需要関係の相互作用を推定する。仮説として、$D(p, s_1, \ldots, s_K) = \exp(\sum_k \beta_k s_k) \cdot h(p)$ のような乗法的構造や、$\epsilon(s) = \epsilon_0 + \sum_k \gamma_k s_k$ のようにaspect感情が弾力性自体に影響するモデルを検証。

3. **因果推論に基づくレビュー-需要モデル**: 操作変数法（IV）、回帰不連続デザイン（RDD）、差分の差分法（DID）を用いて、レビュー感情が需要に与える因果的影響を識別する。例えば、プラットフォームのレビュー表示ルール変更（外生的ショック）を利用した自然実験的アプローチ。

4. **多言語ABSAとグローバル価格設定**: mBERTやXLM-Rなどの多言語Transformerモデルを用いて、複数言語のレビューから統一的なaspect-sentimentスコアを抽出し、地域間の感情差異を考慮した差別的価格設定の最適化。

5. **公平な感情ベースプライシング**: レビュー感情が特定の消費者属性と相関する場合（例：非ネイティブスピーカーの否定的体験がレビューに反映されやすい）に、Chen et al. (2026)の公平性フレームワークを拡張し、感情バイアスを考慮した公平な価格設定アルゴリズムの開発。

---

## 参考文献一覧

1. Shin, D., Vaccari, S., & Zeevi, A. (2023). Dynamic Pricing with Online Reviews. *Management Science*, 69(2), 1032–1053.
2. Correa, J., Mari, M., & Xia, A. (2024). Dynamic Pricing with Bayesian Updates from Online Reviews. *arXiv preprint*, arXiv:2404.14953.
3. Han, F., Guo, Y., Yu, H., & Li, B. (2024). Research on Dynamic Pricing and Long-term Profit of Companies under Influence of Word of Mouth. *Journal of Theoretical and Applied Electronic Commerce Research*, 19(3), 105.
4. Liu, S., Liu, Z., Wang, J., & Xu, L. (2026). Consumer Segmentation and Pricing Optimisation with Online Reviews. *Journal of the Operational Research Society*.
5. Gómez-Talal, I., Talón-Ballestero, P., & Leoni, V. (2025). The Impact of Dynamic Pricing on Restaurant Customers' Perceptions and Price Sentiment. *Tourism Review*, 80(5), 1101.
6. Anisi, A., Kremer, G.O., & Olafsson, S. (2024). Insights from Dynamic Pricing Scenarios for Multiple-Generation Product Lines with an Agent-Based Model Using Text Mining and Sentiment Analysis. *International Journal of Advances in Production Research*.
7. Degife, W.A. & Lin, B.-S. (2024). A Multi-Aspect Informed GRU: A Hybrid Model of Flight Fare Forecasting with Sentiment Analysis. *Applied Sciences*, 14(10), 4221.
8. Di Persio, L. & Lalmi, E. (2024). Maximizing Profitability and Occupancy: An Optimal Pricing Strategy for Airbnb Hosts Using Regression Techniques and NLP. *Journal of Risk and Financial Management*, 17(9), 414.
9. Ray, R.K., Singh, A., & Dash, D.P. (2026). Quantifying Consumer Perceptions in Smartwatch Markets: Integrating ABSA with Panel Data Modelling. *Journal of Enterprise Information Management*.
10. Habbat, N., Anoun, H., Hassouni, L., & Nouri, H. (2022). Hotel Demand Forecasting via Booking's Comments Using Sentiment Analysis and Topic Modeling. *AI2SD*, Springer.
11. Nandinli, A.S., Srinu, N., & Senthil, M. (2024). Sentiment-Driven Predictions with Bi-Directional LSTM for Hotel Demand Forecasting. *International Journal of Management and Economics*.
12. Gallego, G. & van Ryzin, G. (1994). Optimal Dynamic Pricing of Inventories with Stochastic Demand over Finite Horizons. *Management Science*, 40(8), 999–1020.
13. Wang, Y., Chen, B., & Simchi-Levi, D. (2021). Multimodal Dynamic Pricing. *Management Science*, 67(10), 6136–6152.
14. Bu, J., Simchi-Levi, D., & Wang, C. (2022). Context-Based Dynamic Pricing with Partially Linear Demand Model. *NeurIPS 2022*.
15. Chen, X., Simchi-Levi, D., & Wang, Y. (2026). Utility Fairness in Contextual Dynamic Pricing with Demand Learning. *Management Science*.
16. Luo, Y., Sun, W.W., & Liu, Y. (2022). Contextual Dynamic Pricing with Unknown Noise: Explore-then-UCB Strategy and Improved Regrets. *NeurIPS 2022*.
17. Zhu, F., Xiao, W., Yu, Y., Wang, Z., Chen, Z., & Lu, Q. (2022). Modeling Price Elasticity for Occupancy Prediction in Hotel Dynamic Pricing. *CIKM 2022*.
18. Bandalouski, A.M., Egorova, N.G., Kovalyov, M.Y., et al. (2021). Dynamic Pricing with Demand Disaggregation for Hotel Revenue Management. *Journal of Heuristics*, 25, 753–783.
19. Bu, J., Simchi-Levi, D., & Wang, C. (2025). Context-Based Dynamic Pricing with Separable Demand Models. *Management Science*.
20. Besbes, O. & Zeevi, A. (2009). Dynamic Pricing Without Knowing the Demand Function. *Operations Research*, 57(6), 1407–1420.
21. Kleinberg, R. & Leighton, T. (2003). The Value of Knowing a Demand Curve. *FOCS 2003*, 594–605.
22. Talluri, K.T. & van Ryzin, G.J. (2004). *The Theory and Practice of Revenue Management*. Springer.
