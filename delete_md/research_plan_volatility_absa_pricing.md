# 地方宿泊施設における口コミ系列を活用したボラティリティ対応型解釈可能価格モデルの研究計画

---

# 第1章　地方宿泊施設のダイナミックプライシングにおける課題

## 1.1 中小・地方宿泊施設におけるRM導入の構造的障壁

ダイナミックプライシング（DP）は大手ホテルチェーンでは標準的手法として普及しているが（Talluri & van Ryzin, 2004; Vives, Jacob, & Payeras, 2018）、中小・独立系・地方の宿泊施設においてはRM導入率が著しく低い。文献に基づく障壁は以下の3層に構造化される。

### 1.1.1 技術的課題

**(1) ブラックボックス性と説明可能性の不足**

Mohammed & Denizci Guillet（2025b, Tourism Economics）は、27名のRM専門家へのインタビューを通じて、ホテルRMSのブラックボックス性が最大の課題であることを明らかにした。典型的発言として「なぜシステムが特定の月にのみ宿泊料金を引き上げるのか知りたい」（P18）、「アルゴリズム全体は知りたくないが、結果と入力データの簡潔な説明が欲しい」（P12）がある。RMSプロバイダー側も「特定のRMSプロバイダーは、業務保護のために透明性を意図的に制限している」（P6）と認めている。この不透明性はRM担当者による「オーバーライド（システム推薦の上書き）」を引き起こす主要因である。

**(2) データ不足と需要変動の不安定性**

Munnaluri（2022）は、小規模施設では (1) 予約データの蓄積量が限定的、(2) 季節変動が極端で安定した需要パターンの推定が困難、(3) 外部データ（競合価格、地域イベント）の取得が限定的であることを報告した。Zaki（2022, IJCHM, 被引用数60件）は、データ不足は「制御可能な障壁」に分類されるが、その解決には技術投資が必要であり中小施設には負担が大きいとした。

### 1.1.2 制度・組織的課題

Alrawadieh, Alrawadieh, & Cetin（2021, 被引用数215件）は、トルコの独立系ホテル28軒へのインタビューから、(1) RMSの導入コストが年間数万ドル規模で中小施設には負担が大きい、(2) RM専門人材の採用が困難、(3) 既存PMSとの互換性不足、の3つの主要障壁を特定した。Sun, Schuckert, & Hon（2025）は、中国の中小独立系ホテルで (1) 専任レベニューマネージャーの配置が困難、(2) RM機能がフロントデスクの兼務として扱われ専門性不足、(3) オーナー経営者の直感的意思決定がRM原則と衝突する課題を報告した。

### 1.1.3 心理的・受容性課題

Ivanov & Webster（2024, Technology in Society, 被引用数84件）は、ブルガリアのホテルマネージャー130名を対象に、4段階のAI意思決定アプローチへの選好を調査した。結果、マネージャーの大多数は意思決定の制御を維持したい（human-in-the-loop選好）。**価格設定は「制御維持」が強く選好される業務の一つ**である。

Mohammed & Denizci Guillet（2025a, IJCHM, 被引用数10件）は、RM担当者のRMSオーバーライド行動を認知バイアスの観点から分析し、RMSが信頼されていないためオーバーライドが頻発し、それは代表性・利用可能性・アンカリング等のヒューリスティクスに影響されることを実証した。

Schwartz, Webb, & Liu（2025, European Journal of Tourism Research）は、RM分析が人間の直感に反する場合、非専門家もRM専門家も正答率はともに約40%であるにもかかわらず、RM専門家は自身の判断により大きな自信を持っていることを示した（「システムは信頼しないが自分の直感は信頼する」問題）。

### 1.1.4 地方施設に特有の事情

上記の一般的課題に加え、地方宿泊施設には以下の文献に基づく特有の事情がある。

| 特有事情 | 内容 | 文献根拠 |
|---------|------|---------|
| **地域イベント依存** | 地方施設の需要は地域イベント（祭り、花見、紅葉、スポーツ大会等）に強く依存し、過去パターンの反復が成立しにくい | Talón-Ballestero, Nieto-García et al. (2022, IJHM, 被引用数65件): 需要の高ボラティリティが価格最適化をより困難にする |
| **常連客との関係性** | 地方施設はリピーター率が高い傾向にあり、価格の頻繁な変更は関係性を損なう可能性 | Gómez-Talal et al. (2025, Tourism Review, 被引用数11件): サービス品質が高い場合には価格変更の否定的影響が緩和される |
| **ブランドより口コミ依存** | ブランド力が限定的な地方施設では口コミがブランドの代替物として機能 | Abrate, Nicolau, & Viglia (2019, Tourism Management, 被引用数215件): レビュー評価が収益に正の影響; Liu et al. (2022, 被引用数37件): P2P宿泊ではeWoMの影響が特に大きい |
| **納得感の重視** | 「市場均衡価格の実現」よりも「施設オーナーが価格設定に納得すること」が重要 | Mohammed & Denizci Guillet (2025b): 「システムを信頼するため、システムの動作を理解する必要がある」(P16) |

### 1.1.5 課題の分類体系

| 類型 | 具体的課題 | 代表文献 |
|------|-----------|---------|
| 技術的 | RMSのブラックボックス性 | Mohammed & Denizci Guillet (2025b) |
| 技術的 | データ不足（予約・外部データ） | Munnaluri (2022); Zaki (2022) |
| 技術的 | 需要変動の不安定性（高ボラティリティ） | Talón-Ballestero et al. (2022) |
| 組織的 | RM専門人材不足 | Sun et al. (2025) |
| 組織的 | RMS導入・維持コスト | Alrawadieh et al. (2021) |
| 心理的 | 自動化への抵抗（制御維持願望） | Ivanov & Webster (2024) |
| 心理的 | RMSへの不信（オーバーライド頻発） | Mohammed & Denizci Guillet (2025a) |
| 心理的 | 専門家の過信（直感>分析） | Schwartz, Webb, & Liu (2025) |
| 地方特有 | 地域イベント依存の需要、常連客配慮、口コミ依存 | Abrate et al. (2019); Gómez-Talal et al. (2025) |

---

# 第2章　上記課題を踏まえた既存研究の動向

## 2.1 XAI（説明可能AI）のRMSへの統合

Mohammed & Denizci Guillet（2025b）は、XAIのRMS統合を27名のRM専門家インタビューで探索した。XAIの7種の質問駆動型説明能力（what, how, why, why not, what-if, how-to, what-else）はRMユーザーの情報ニーズと整合する。エンドユーザーは**局所的（出力固有）説明**を求め、好む形式は「250〜300語の箇条書き」「文脈化とパーソナライゼーション」「インタラクティブな対話」である。ただし、**XAIの認知度と準備状況は「低い」**。ホテルRMSにおけるXAIは未実装であり、経済的パフォーマンスへの影響が定量的に評価されていない。

Heger（2025, PhD Dissertation, University of Augsburg）は、SHAPを用いた需要予測モデルの説明可能化を提案しているが、ホスピタリティ産業に特化した検証は限定的。

Tatlıdil, Yavuz, & Yöndem（2025, IEEE）は、観光産業の契約価格最適化においてXAIを適用し、価格設定根拠の透明化を試みた。

### XAI研究の限界

XAIの説明対象はいずれも「RMSアルゴリズムの内部ロジック」であり、**「レビューから得られる顧客の声」を説明材料として活用するアプローチは提案されていない**。

## 2.2 Human-in-the-loop設計

Ivanov & Webster（2024）の結果から、マネージャーの大多数は意思決定の制御を維持したいため、「提案型」の設計が受容されやすい。Garcia, Tolvanen, & Wagner（2026, Management Science, 被引用数18件）は、ホテルマネージャーがアルゴリズム推薦に対して系統的な乖離パターンを示し、推薦からの乖離が収益損失に繋がるケースを定量化した。「human in the loop」状況において、**推薦への準拠度が収益パフォーマンスと正相関する場合がある**。

## 2.3 レビュー・口コミを価格に活かす既存研究

### 分類体系

文献調査の結果、口コミ活用研究は以下の3カテゴリに分類され、**第4のカテゴリ（口コミを価格根拠説明として提示）は文献上の空白領域**である。

| カテゴリ | 内容 | 代表文献 |
|---------|------|---------|
| **A: 予測精度向上** | 口コミ→需要/価格の「予測」精度向上 | Wu et al. (2022, 被引用78件); Degife & Lin (2024); Di Persio & Lalmi (2024) |
| **B: DP理論統合** | 口コミ→DP理論への統合（理論的モデル、未実装） | Shin et al. (2023, Management Science, 被引用110件); Correa et al. (2024) |
| **C: 消費者行動理解** | 口コミ→顧客選好の導出 | Zhang, Lu, & Liu (2021, 被引用82件); Özen & Özgül Katlav (2023, 被引用47件) |
| **D: 価格根拠説明（未存在）** | 口コミ分析結果を人間の意思決定者への「価格提案根拠」として提示 | **文献上の空白** |

### 個別研究の要約

**Shin, Vaccari, & Zeevi (2023, Management Science, 被引用数110件)**: ベイジアンDP with レビューのモデルでは、最適戦略は低い導入価格→品質がレビューで明らかになった後に値上げ。DP価値はレビューの情報量が「中程度」の場合にピーク。

**Han, Guo, Yu, & Li (2024, JTAER, 被引用数5件)**: WoMテキストマイニングで需要関数D(p,WoM)を構築。全てのポジティブ要素が等しく価格への影響を持つわけではない。DP > 固定価格（WoM情報利用時）。

**Wu, Zhong, Qiu, & Wu (2022, Tourism Economics, 被引用数78件)**: マカオのラグジュアリーホテル4軒で、レビュー感情スコアの追加が需要予測精度を統計的に有意に改善。特に**需要変動期（季節変わり目、イベント期間）での改善が顕著**。

## 2.4 特定された研究ギャップ

| ギャップ | 種類 | 内容 |
|---------|------|------|
| **ギャップ1** | 文献的空白 | ABSAと価格決定支援の未統合 — ABSAの結果を人間意思決定者への価格根拠として活用するシステムは存在しない |
| **ギャップ2** | 文献的空白 | XAIとレビュー分析の統合アプローチの不在 — XAIの説明対象は「RMSの内部ロジック」のみで、「顧客の声」を説明材料とするアプローチなし |
| **ギャップ3** | 応用領域の欠如 | 中小・地方宿泊施設を対象とした価格支援研究の不足 |
| **ギャップ4** | 方法論的限界 | 口コミのaspect別価格弾力性の未推定 |
| **ギャップ5** | 方法論的限界 | 因果推定の欠如 — 口コミ感情と需要/価格の関係の多くが相関のみ |
| **ギャップ6** | 方法論的限界 | 地方宿泊施設の価格ボラティリティと口コミ系列の時間的関係が未分析 |

---

# 第3章　口コミが価格・需要に与える影響——既存研究の事実

## 3.1 レビュースコアと宿泊料金の関係

| 研究 | データ | 結果 |
|------|-------|------|
| Anderson (2012, Cornell Hospitality Quarterly, 被引用2,637件) | 11カ国のホテルデータ | レビュースコア1ポイント上昇 → ADR（平均客室単価）11.2%上昇（稼働率を維持した場合）; RevPAR 最大5.5% |
| Torres, Singh, & Robertson (2015, 被引用260件) | 米国ホテルデータ | Tripadvisorスコア1ポイント上昇 → ADR 9%上昇 |
| Castro & Ferreira (2018, J. Hospitality & Tourism Technology, 被引用88件) | ポルトの194 Airbnbリスティング | 総合評点95以上の物件は低評点物件比で43.8%の価格プレミアム |

## 3.2 レビュースコアと販売・予約への影響

| 研究 | データ | 結果 |
|------|-------|------|
| Ye, Law, & Gu (2009, 被引用2,146件) | 中国OTAデータ | レビュースコア10%改善 → オンライン予約4.4%増加 |
| Kim, Lim, & Brymer (2015, 被引用658件) | 米国ホテルデータ | 高い口コミ評価は実際の宿泊販売と正相関。しかし長期的にはレビュー量飽和ありうる |

## 3.3 テキスト感情分析は数値スコアより強い予測力を持つ

| 研究 | データ・手法 | 結果 |
|------|----------|------|
| Almeida, Moro, & Tavares (2025, Tourism Management, 被引用20件) | ポルトガルの民泊(Inside Airbnb)、SARモデル（空間オートレグレッション） | テキスト感情分析スコアが数値レビュースコアよりR²への寄与が高い; テキスト分析を含むモデルが最高精度 |
| Di Persio & Lalmi (2024, JRFM) | ローマのAirbnb (Inside Airbnb, 22,564英語レビュー) | BoW/TF-IDF/ABSA(CNN)を適用。Forward Feature Selection でレビュー数・立地スコアが重要特徴量として選出。ニューラルネットワークが最高精度（MAE最低、R²最高）|

## 3.4 ABSAによるaspectレベルの価格・需要予測貢献

| 研究 | データ・手法 | 結果 |
|------|----------|------|
| **Degife & Lin (2024, Applied Sciences)** | 航空業界レビュー、BERT→9 aspectグループ→7層GRU | R² = 0.9899（全aspect込み）。**Safety & Security除去 → R² = 0.6752**に急落（感度分析で特定aspectの貢献度を定量化）|
| Gordan, Borza, & Egresi (2024) | ルーマニア5,028施設、GWR（地理的加重回帰） | **農村観光**で清潔さ・立地スコアの影響係数が空間的に変動。レビュー量の負の係数を確認 |
| Nieto-García et al. (2019, 被引用106件) | Airbnbデータ | **Staff & Facilitiesが最も重要な価格寄与aspect** |
| Zhang, Lu, & Liu (2021, 被引用82件) | 教師なしABSA | 顧客は各ホテル属性に異なる注目度を払い、ABSAにより各属性の相対的重要度を定量化可能。**価格への注目度はホテルカテゴリにより異なる** |
| Özen & Özgül Katlav (2023, 被引用47件) | テクノロジー対応ホテルのレビュー | ABSAにより各テクノロジー要素の顧客感情を定量化 |

## 3.5 ネガティブレビューの非対称的影響

| 研究 | 結果 |
|------|------|
| Almeida et al. (2025) | ネガティブ感情の価格への影響はポジティブの約2倍。低価格帯では約4倍 |
| Jiang (2024) | ネガティブレビューが需要に与える影響の非対称性を再確認 |

## 3.6 レビュー量の価格への影響

Gordan et al. (2024) および Gibbs et al. (2018) は、レビュー量が価格に対して**負の係数**を持つことを確認した。これは直感に反するが、「レビュー量が多い = 安価で大量集客する施設」という母集団バイアスの可能性が指摘されている。

## 3.7 農村・地方施設での口コミ研究

| 研究 | 内容 |
|------|------|
| Gordan, Borza, & Egresi (2024) | ルーマニアの農村観光5,028施設でGWRを適用。口コミスコアの影響係数が地域により空間的に変動することを実証した**唯一の農村焦点研究** |
| Almeida et al. (2025) | 都市-農村混合分析の欠如を明示的に指摘: "urban-rural mix severely lacking" |

## 3.8 口コミ→価格への4つの経路（事実の統合）

| 経路 | メカニズム | 代表的定量結果 |
|------|----------|-------------|
| **A: スコア→価格プレミアム** | 総合レビュースコアが高い → ADR/WTPが上昇 | 1pt → +9〜11.2% ADR (Anderson 2012; Torres 2015) |
| **B: テキスト感情 > 数値スコア** | テキスト分析由来の感情スコアが数値スコアより高い予測力 | R²寄与でテキスト感情 > 数値スコア (Almeida 2025) |
| **C: ABSA → aspect別予測** | 特定aspectの除去で予測精度が大幅低下 | Safety除去: R² 0.99→0.68 (Degife & Lin 2024) |
| **D: ネガティブの非対称的影響** | ネガティブ感情の影響がポジティブの2〜4倍 | 低価格帯で4倍 (Almeida 2025) |

---

# 第4章　Inside Airbnbデータセットの変数構造と地方分析の可能性

## 4.1 データセットの概要

| 項目 | 内容 |
|------|------|
| **URL** | http://insideairbnb.com/get-the-data/ |
| **ライセンス** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **更新頻度** | 四半期ごと（直近1年分を無料公開） |
| **日本データ** | **Tokyo, Kantō, Japan** — 2025年9月29日時点スナップショット |
| **全体規模** | 世界100+都市・地域。2025年より12カ国のRegional Archive Filesも提供開始 |
| **活用可能性** | ★★★★★ — **宿泊ドメインで口コミ+価格+時系列のすべてを満たす唯一のオープンデータ源** (Zhu et al., 2024, KDD: "As there is no other public dataset for hotel pricing") |

## 4.2 提供ファイルと変数の詳細

### 4.2.1 listings.csv.gz（物件詳細データ）

| 変数カテゴリ | 主要変数 | 分析上の用途 |
|------------|---------|------------|
| **物件基本** | id, listing_url, name, description, neighborhood_overview | 物件特定、テキスト特徴量 |
| **ホスト情報** | host_id, host_since, host_response_time, host_response_rate, host_acceptance_rate, host_is_superhost | ホスト品質の代理変数 |
| **立地** | neighbourhood_cleansed, latitude, longitude | 空間分析（GWR等）の基盤 |
| **物件属性** | property_type, room_type, accommodates, bathrooms, bedrooms, beds, amenities | ヘドニック価格モデルの説明変数 |
| **価格** | **price** | 目的変数 |
| **可用性** | minimum_nights, maximum_nights, availability_30/60/90/365 | 稼働率・需要の代理変数 |
| **レビュー数量** | number_of_reviews, number_of_reviews_ltm, first_review, last_review, reviews_per_month | レビュー量の時間的動態 |
| **レビュースコア（7次元）** | **review_scores_rating**, **review_scores_accuracy**, **review_scores_cleanliness**, **review_scores_checkin**, **review_scores_communication**, **review_scores_location**, **review_scores_value** | ABSAの補完的構造化スコア |
| **ホスト規模** | calculated_host_listings_count | 個人ホスト vs 事業者の識別 |

### 4.2.2 calendar.csv.gz（日次価格データ）

| 変数 | 内容 | ボラティリティ分析上の意義 |
|------|------|----------------------|
| listing_id | 物件ID | 物件単位の時系列構成 |
| date | 日付 | 時系列分析の時間軸 |
| available | 予約可否 (t/f) | 稼働率の日次推定 |
| **price** | 掲載価格 | **日次の価格変動（ボラティリティ）の直接測定が可能** |
| **adjusted_price** | 調整済み価格 | DP適用後の実効価格 |
| minimum_nights | 最低宿泊日数 | 価格戦略の制約条件 |
| maximum_nights | 最大宿泊日数 | 同上 |

### 4.2.3 reviews.csv.gz（レビュー全文テキスト）

| 変数 | 内容 | ABSA上の意義 |
|------|------|------------|
| listing_id | 物件ID | 物件単位の口コミ系列構成 |
| id | レビューID | 個別レビューの特定 |
| date | 投稿日 | 口コミの時系列分析 |
| reviewer_id | レビュアーID | レビュアー属性分析 |
| reviewer_name | レビュアー名 | 国籍・言語の推定 |
| **comments** | **レビュー全文テキスト** | **ABSA（aspect抽出・感情推定）の入力** |

## 4.3 地方・非都市部データの利用可能性

### 4.3.1 Inside Airbnbで利用可能な地方・非都市部地域

Inside Airbnbは100+地域のデータを提供しているが、その中に**明確に地方・非都市部に分類される地域**が含まれる。

| 地域名 | 国 | 地方的特性 |
|-------|---|----------|
| Barossa Valley, South Australia | 豪州 | ワイン産地、農村地域 |
| Barwon South West, Victoria | 豪州 | 地方沿岸、農牧地域 |
| Mid North Coast, New South Wales | 豪州 | 地方沿岸リゾート地域 |
| Mornington Peninsula, Victoria | 豪州 | 半島部観光地域 |
| Northern Rivers, New South Wales | 豪州 | 地方内陸・沿岸 |
| Sunshine Coast, Queensland | 豪州 | 地方リゾート地域 |
| Tasmania | 豪州 | 島嶼地域全体 |
| Western Australia | 豪州 | 州全体（広域・非都市部含む） |
| Crete | ギリシャ | 島嶼地域、観光依存 |
| South Aegean | ギリシャ | 島嶼地域群 |
| Trentino | イタリア | 山岳地域、スキー・自然観光 |
| Puglia | イタリア | 南部農村・沿岸地域 |
| Sicily | イタリア | 島嶼地域 |
| Hawaii | 米国 | 島嶼リゾート地域 |
| Bozeman, Montana | 米国 | 山岳・自然観光の小都市 |
| Pays Basque | フランス | 地方文化圏 |
| New Zealand | ニュージーランド | 国全体（農村部含む） |
| Ireland | アイルランド | 国全体（農村部含む） |

### 4.3.2 日本データの制約

**Inside Airbnbにおける日本データは Tokyo, Kantō, Japan の1地域のみ**である。長野県、北海道、沖縄、九州等の地方データは提供されていない。

この制約に対するデータ戦略は第6章で詳述する。

## 4.4 Inside Airbnbの先行研究での使用実績

| 研究 | 対象地域 | 分析内容 |
|------|---------|---------|
| Almeida et al. (2025) | ポルト | SARモデル、感情分析の価格への寄与 |
| Di Persio & Lalmi (2024) | パリ → ローマ (Inside Airbnb 2023年5月) | ABSA(CNN) + 価格予測 |
| Costa (2025) | リスボン・ポルト | 需要分析 |
| Ghosh et al. (2023, IJCHM, 被引用53件) | NYC | 価格分析 |
| Katz (2026, arXiv) | 複数都市 | calendar dataを使い supply/demand forecasting の再現可能性を実証 |
| Katz, Savage, & Coles (2025, 被引用8件) | 複数都市 (2018–2022年) | 予約リードタイム動態、COVID-19前後のvolatilityを定量化 |

---

# 第5章　ボラティリティ分析——地方宿泊施設の価格変動特性

## 5.1 ボラティリティの定義と測定

### 5.1.1 Inside Airbnb calendar.csvによる日次価格ボラティリティ

calendar.csv.gzには**日次の掲載価格（price, adjusted_price）**が含まれており、物件ごとの日次価格系列 $\{p_{i,t}\}_{t=1}^{T}$ を構成可能。ボラティリティは以下の指標で測定できる。

**標準偏差ベース**:
$$\sigma_i = \sqrt{\frac{1}{T-1} \sum_{t=1}^{T}(p_{i,t} - \bar{p}_i)^2}$$

**変動係数 (CV)**:
$$CV_i = \frac{\sigma_i}{\bar{p}_i}$$

**日次変化率の標準偏差**:
$$\sigma^{ret}_i = \text{std}\left(\frac{p_{i,t} - p_{i,t-1}}{p_{i,t-1}}\right)$$

### 5.1.2 レビュースコアのボラティリティ

listings.csvの7次元レビュースコア（rating, accuracy, cleanliness, checkin, communication, location, value）はスナップショット値であるが、reviews.csvのレビュー全文テキストに日付が付与されているため、ABSAにより**時系列の感情スコア**を構成可能：

$$s^{(k)}_{i,t} = \text{ABSA}(\text{reviews}_{i, [t-\Delta, t]})$$

この感情スコアの時間変動もボラティリティとして測定可能。

## 5.2 地方宿泊施設のボラティリティ特性に関する事実

### 5.2.1 季節変動

Hotel Booking Demand Dataset（Antonio et al., 2019）では、リゾートホテルのADRに**明確な季節変動**が確認されている。地方施設では地域イベント依存による需要の高ボラティリティ（Talón-Ballestero et al., 2022）が指摘されている。

### 5.2.2 COVID-19前後のvolatility

Katz, Savage, & Coles（2025, 被引用8件）は、Inside Airbnbの2018–2022年データを用い、COVID-19前後の予約リードタイム動態を分析し、**パンデミック前後でのvolatilityの構造的変化**を定量化した。

### 5.2.3 レビュー感情と需要変動の連動

Wu et al.（2022, 被引用78件）は、レビュー感情スコアの追加が需要予測精度を改善する効果が、**需要変動期（季節変わり目、イベント期間）で特に顕著**であることを示した。これは、**ボラティリティが高い期間にこそ口コミ情報の予測寄与が大きい**ことを示唆する。

### 5.2.4 ネガティブ感情のボラティリティ増幅効果

Almeida et al.（2025）のネガティブ非対称性（ネガティブ影響 = ポジティブの2〜4倍）は、ネガティブレビューの急増が需要の急落を引き起こし、**下方ボラティリティを増幅する**メカニズムを示唆する。

## 5.3 ボラティリティ分析の研究上の位置づけ

**事実**: 地方宿泊施設の日次価格ボラティリティと、口コミ感情スコアの時間変動の関係を直接分析した研究は、文献調査の範囲では確認されなかった。

**未解明の問い**:
1. 地方地域のAirbnb物件の日次価格変動係数（CV）は都市部と比較してどの程度大きいか？
2. 口コミ感情スコアの時間的変動は、価格ボラティリティの先行指標として機能するか？
3. 特定aspectの感情悪化は、価格下方ボラティリティと有意に関連するか？

---

# 第6章　提案するアプローチ——既存研究に基づく手法選定

## 6.1 データ戦略

### 6.1.1 日本地方データの不在への対処

Inside Airbnbにおける日本データはTokyo（関東）のみであり、長野県等の地方データは直接利用できない。以下のデータ戦略を既存研究の先例に基づいて設定する。

**戦略A: 海外地方地域データによるモデル構築 + 東京データでの検証**

| データソース | 活用方法 | 先行例 |
|------------|---------|-------|
| Tasmania, Barossa Valley, Crete, Trentino, Puglia, Sicily 等の地方地域 | 地方特性（季節変動、低需要密度、観光イベント依存）を持つ物件での ABSA + ボラティリティ分析 | Gordan et al. (2024): ルーマニア農村5,028施設でGWR; Almeida et al. (2025): ポルト(Inside Airbnb)でSAR |
| Tokyo, Kantō | 日本語レビューのABSAパイプライン検証、東京郊外（奥多摩、八王子等）の準地方物件の抽出 | Di Persio & Lalmi (2024): ローマ(Inside Airbnb)で価格予測 |
| 宿泊旅行統計調査（国土交通省観光庁） | 47都道府県の月次宿泊者数・稼働率データ。需要の地域間比較・季節指数の算出 | — |

**戦略B: 複数地方地域の統合（クロスリージョン分析）**

Inside Airbnbの12カ国Regional Archiveファイル（2025年〜提供開始）を活用し、各国内の地方地域を抽出。複数地方地域の統合データセットにより、「地方宿泊施設」としての汎化性を担保する。

### 6.1.2 ボラティリティ分析用データの構成

| データ | 変数 | 時間粒度 | ボラティリティ測定 |
|-------|------|---------|----------------|
| calendar.csv.gz | price, adjusted_price, available | 日次 | 日次価格変動係数 (CV)、日次変化率の標準偏差 |
| reviews.csv.gz | comments, date | レビュー投稿日 | ABSAによるaspect別感情スコアの移動平均・移動分散 |
| listings.csv.gz | review_scores_* (7次元) | スナップショット（四半期） | クロスセクション的な感情水準 |

## 6.2 ABSAパイプラインの設計

### 6.2.1 既存研究で検証された手法の比較

| 手法 | 研究 | 精度 | 適用ドメイン |
|------|------|------|------------|
| BERT → aspect抽出 → 9 aspectグループ → 7層GRU | Degife & Lin (2024) | R² = 0.9899 | 航空 |
| BoW / TF-IDF / ABSA(1次元CNN, HOST-GENERAL) | Di Persio & Lalmi (2024) | 最高精度:NN | Airbnb(ローマ) |
| BERT + few-shot learning | Ray, Singh, & Dash (2026) | パネルデータモデル | スマートウォッチ |
| LDA + 感情分析 | Habbat et al. (2022) | — | Booking.com |
| BiLSTM + 感情特徴量 | Nandinli, Srinu, & Senthil (2024) | — | ホテル |
| 教師なしABSA | Zhang, Lu, & Liu (2021, 被引用82件) | — | ホテル |

### 6.2.2 本研究で採用する手法の根拠

**BERT ベースABSA → aspect 感情スコアの時系列化**を基本パイプラインとする。

**根拠**:
1. Degife & Lin (2024) がBERT→GRUの組み合わせでR² = 0.9899を達成し、aspect感情スコアの需要予測への有効性を最も明確に実証した。
2. Di Persio & Lalmi (2024) がInside AirbnbデータでABSA適用の先例を示した。
3. Zhang, Lu, & Liu (2021) がaspect別顧客選好の定量化可能性を確認した。

**宿泊施設ドメインのaspect設定**:

| Aspect | 根拠 |
|--------|------|
| 清潔さ (Cleanliness) | Inside Airbnb review_scores_cleanliness に対応; Degife & Lin (2024) で最重要aspect; Nieto-García et al. (2019) |
| 立地 (Location) | review_scores_location に対応; Di Persio & Lalmi (2024) で最重要価格決定要因 |
| サービス・接客 (Service/Staff) | Nieto-García et al. (2019): Staff が最重要価格寄与aspect |
| 設備 (Facilities) | Nieto-García et al. (2019): Facilities が最重要価格寄与aspect |
| コストパフォーマンス (Value) | review_scores_value に対応 |
| チェックイン (Check-in) | review_scores_checkin に対応 |
| 正確性 (Accuracy) | review_scores_accuracy に対応; 掲載情報と実態の一致 |
| コミュニケーション (Communication) | review_scores_communication に対応 |

### 6.2.3 口コミ感情の時系列化

reviews.csvの各レビュー（日付付き）に対してABSAを適用し、物件 $i$ のaspect $k$ について期間 $[t-\Delta, t]$ の移動平均感情スコアを算出：

$$s^{(k)}_{i,t} = \frac{1}{|\mathcal{R}_{i,[t-\Delta,t]}|} \sum_{r \in \mathcal{R}_{i,[t-\Delta,t]}} \text{sentiment}^{(k)}(r)$$

移動分散（感情の安定性指標）:

$$v^{(k)}_{i,t} = \text{Var}_{r \in \mathcal{R}_{i,[t-\Delta,t]}} \left[\text{sentiment}^{(k)}(r)\right]$$

## 6.3 ボラティリティ分析手法

### 6.3.1 価格ボラティリティの定量化

calendar.csvの日次価格から、物件ごと・期間ごとのボラティリティ指標を算出:

1. **期間内変動係数**: $CV_{i,m} = \sigma(p_{i,t \in m}) / \bar{p}_{i,m}$（月次）
2. **繁閑比**: $\text{Peak-Trough Ratio}_{i} = \max_m(\bar{p}_{i,m}) / \min_m(\bar{p}_{i,m})$
3. **イベント応答度**: 地域イベント前後の価格変化率

### 6.3.2 都市部 vs 地方の比較分析

**目的**: 地方地域の物件が都市部と比較してどの程度高いボラティリティを示すかを定量的に確認する。

| 比較項目 | 都市部（例: ロンドン, パリ, 東京） | 地方（例: Tasmania, Trentino, Puglia） |
|---------|---------------------------|-----------------------------------|
| 日次価格CV | 算出 | 算出 |
| 繁閑比 | 算出 | 算出 |
| 可用性変動 | availability列の変動 | 同上 |
| レビュー頻度 | reviews_per_month | 同上 |

### 6.3.3 口コミ感情ボラティリティと価格ボラティリティの関連分析

**目的**: 口コミ感情スコアの時間的変動が、価格変動の先行指標として機能するかを検証する。

$$\text{corr}\left(\Delta s^{(k)}_{i,t-\tau},\ \Delta p_{i,t}\right) \quad \text{for} \quad \tau = 0, 1, 2, \ldots$$

グレンジャー因果性テストまたはクロス相関分析により、感情変動 → 価格変動の時間的先行関係を検証。

## 6.4 価格モデルの設計

### 6.4.1 既存研究の手法比較と選定

| 手法 | 研究 | 解釈性 | 精度 | 適用可能性 |
|------|------|-------|------|----------|
| ヘドニック価格モデル（OLS/SAR） | Abrate et al. (2019, 被引用215件); Almeida et al. (2025) | ★★★★★ | ★★★ | 係数の直接解釈可能。空間効果の組み込み実績あり |
| GWR（地理的加重回帰） | Gordan et al. (2024) | ★★★★ | ★★★★ | 地域ごとにaspect影響が変動する構造を捉えられる。農村観光での実績あり |
| XGBoost + SHAP | Di Persio & Lalmi (2024); Aggarwal (2025); Binesh et al. (2025, IJCHM, 被引用3件) | ★★★★ | ★★★★★ | 高精度+SHAP説明。宿泊施設での使用実績多数 |
| GRU（ABSA統合） | Degife & Lin (2024) | ★★ | ★★★★★ | R²=0.9899の実績だが単独では解釈困難 |
| DRL (DQN/PPO/SAC) | Wang et al. (2025); Mei (2025) | ★ | ★★★★★ | シミュレーション環境が必要。実データ不足時のリスク |

### 6.4.2 提案: 解釈性を重視した2段階モデル

**第1段階: ヘドニック価格モデル + ABSA感情スコア**

$$\ln(p_{i,t}) = \alpha + \sum_{k=1}^{K} \beta_k \cdot s^{(k)}_{i,t} + \gamma' \mathbf{x}_{i,t} + \epsilon_{i,t}$$

- $\beta_k$: aspect $k$ の感情スコア1単位変化に対する価格弾力性（**直接解釈可能**）
- $\mathbf{x}_{i,t}$: 構造化特徴量（物件属性、曜日、季節、可用性）
- 先例: Abrate et al. (2019): ヘドニック収益モデル; Almeida et al. (2025): SARモデルでの感情スコア統合

**第2段階: XGBoost + SHAP による非線形補正と説明**

$$\hat{p}_{i,t} = f_{XGB}(s^{(1)}_{i,t}, \ldots, s^{(K)}_{i,t}, \mathbf{x}_{i,t})$$

- SHAPにより各特徴量（各aspect感情スコア含む）の個別寄与を算出
- 先例: Aggarwal (2025): Tree models + SHAP for demand/price optimization; Saitta, D'Amico, & Farinella (2024): Hotel DP predictions with SHAP; Binesh et al. (2025): Deep learning + game-theoretic + SHAP for Airbnb pricing

### 6.4.3 解釈性を重視する理由（LLMによる価格「計算」は不適切）

research_design_candidates.md の候補Aで整理された通り、Liu et al. (2025) はLLMが価格計算タスクで失敗することを示した。LLMの役割は価格「計算」ではなく「説明生成」に限定すべきである。

本研究では、価格の計算はヘドニックモデル/XGBoostが担い、その出力に対する**自然言語説明**をLLMが生成する設計を採用する。これはMohammed & Denizci Guillet（2025b）の「what, why, what-if」の説明ニーズに対応し、Ivanov & Webster（2024）のhuman-in-the-loop選好にも合致する。

### 6.4.4 アブレーション設計（ABSAの貢献度定量化）

Degife & Lin (2024) の感度分析アプローチに倣い、以下のモデルバリアントを比較：

| モデル | 特徴量 | 検証内容 |
|-------|-------|---------|
| M0 | 構造化データのみ（物件属性、曜日、季節） | ベースライン |
| M1 | M0 + 総合レビュースコア (review_scores_rating) | 数値スコアの追加効果 |
| M2 | M0 + 7次元レビュースコア全て | 多次元スコアの効果 |
| M3 | M0 + ABSA全aspect感情スコア | **テキスト由来ABSAスコアの効果** |
| M4 | M0 + 7次元スコア + ABSA全aspect | 構造化スコア+テキスト感情の統合効果 |
| M5 | M4 + 感情の時系列特徴量（移動平均・移動分散） | ボラティリティ情報の追加効果 |

先例: Degife & Lin (2024): M0-M5形式のアブレーションで各aspectの寄与を定量化。Wu et al. (2022): 感情スコア追加による予測改善を統計的有意性で検証。

## 6.5 説明生成モジュール

### 6.5.1 SHAP + LLMによる自然言語説明

XGBoostモデルのSHAP値と、ABSAで抽出されたaspect感情の具体的内容を入力として、LLMが自然言語説明を生成する。

**出力例**:
「本日 +5% の価格引き上げを推薦。理由: (1) 清掃スコアが先月比 +0.3 上昇（レビューで『部屋が清潔』の言及増加）、(2) 競合施設の平均価格が +8%、(3) 予測稼働率 85%」

### 6.5.2 文献に基づく説明品質の要件

| 要件 | 根拠 |
|------|------|
| 簡潔さ（250〜300語の箇条書き） | Mohammed & Denizci Guillet (2025b): RM担当者の好む形式 |
| 7種の質問対応（what, why, why not, what-if, how-to, what-else, how） | Mohammed & Denizci Guillet (2025b): XAI説明ニーズ |
| 事実整合性 | simulation_evaluation_design.md Layer 4: 事実支持率 ≥ 0.90、幻覚率 ≤ 0.05 |

---

# 第7章　評価設計

## 7.1 5層評価フレームワーク

simulation_evaluation_design.md で設計された5層フレームワークを本研究に適用する。

| Layer | 検証の問い | 主な指標 | 根拠文献 |
|-------|----------|---------|---------|
| **L1: ABSA精度** | aspect抽出・感情推定の精度は十分か？ | F1, Cohen's κ ≥ 0.7, 300+アノテーション | Degife & Lin (2024); Liskowski & Jankowski (2026) |
| **L2: ABSAの需要/価格予測貢献** | ABSA感情スコアの追加は予測を有意に改善するか？ | M0-M5アブレーション、Diebold-Mariano検定 | Degife & Lin (2024); Wu et al. (2022) |
| **L3: 価格推薦精度** | 推薦価格は市場価格と整合するか？ | MAE(price), 方向一致率, RevPARシミュレーション | Fisher et al. (2018, 被引用285件); Garcia et al. (2026) |
| **L4: 説明品質** | LLM生成説明は妥当で有用か？ | LLM-as-Judge 5次元ルーブリック, 事実支持率 | Chen et al. (2026); Cheng et al. (2025); Pičulin et al. (2025, ICML) |
| **L5: 経済性** | 提案手法でRevPARは改善されるか？ | RevPAR改善率, 感度分析（弾力性±20%） | Wang et al. (2025); Bayoumi et al. (2013) |

## 7.2 ボラティリティ固有の評価

上記5層に加え、本研究の焦点であるボラティリティに関して以下の評価を追加する。

| 評価項目 | 方法 | 指標 |
|---------|------|------|
| **都市-地方ボラティリティ差** | calendar.csvの日次CVを都市部 vs 地方で比較 | 平均CV比, t検定/Mann-Whitney |
| **高ボラティリティ期間での予測改善** | 需要変動期（CV上位25%期間）でのM3 vs M0のRMSE改善率 | RMSE改善率, 統計的有意性 |
| **感情先行指標性** | グレンジャー因果性テスト: $\Delta s^{(k)}_{t-\tau} \to \Delta p_t$ | p値, 最適ラグ $\tau$ |
| **ネガティブ非対称性の定量化** | ネガティブ感情変化 vs ポジティブ感情変化の価格弾力性比較 | $|\beta_{neg}| / |\beta_{pos}|$の推定値 |

---

# 第8章　研究の位置づけと貢献

## 8.1 研究ギャップへの対応

| ギャップ | 本研究での対応 |
|---------|-------------|
| ABSAと価格決定支援の未統合 | ABSAスコアをヘドニック/XGBoostモデルに統合し、SHAP+LLMで価格根拠を自然言語提示 |
| XAIとレビュー分析の未結合 | 口コミのaspect感情を「説明材料」として直接活用するアーキテクチャ |
| 地方施設対象研究の不足 | Inside Airbnbの地方地域データ（Tasmania, Trentino, Puglia等）を主対象 |
| aspect別価格弾力性の未推定 | ヘドニックモデルの $\beta_k$ 係数 + SHAPで各aspectの価格寄与を定量化 |
| 価格ボラティリティと口コミ系列の関係の未分析 | 口コミ感情の時系列化 + グレンジャー因果性 + 高ボラティリティ期間での予測改善検証 |

## 8.2 LLM vs ML の役割分担

| 役割 | 担当技術 | 根拠 |
|------|---------|------|
| **aspect抽出・感情推定** | BERT ベースABSA | Degife & Lin (2024): R²=0.9899; Zhang et al. (2021) |
| **価格予測** | ヘドニック回帰 + XGBoost | Abrate et al. (2019); Aggarwal (2025); Di Persio & Lalmi (2024) |
| **特徴量重要度** | SHAP | Saitta et al. (2024); Binesh et al. (2025) |
| **自然言語説明生成** | LLM (GPT-4o等) | Mohammed & Denizci Guillet (2025b): 説明ニーズ; Liu et al. (2025): LLMは計算に不適 |
| **ボラティリティ定量化** | 統計的手法（CV, グレンジャー因果性） | Katz et al. (2025): volatility定量化実績 |

## 8.3 「ユーザスタディなし」の正当化

| 正当化ポイント | 根拠 |
|-------------|------|
| ホテルDP研究の大多数はシミュレーション評価のみ | Wang et al. (2025), Li (2026), Bayoumi et al. (2013) のいずれもフィールド実験なし |
| Fisher et al. (2018, 被引用285件) はシミュレーション→フィールド実験を2段階と位置づけ | 本研究はStage 1に相当 |
| LLM-as-Judge + 少数人間評価の相関で自動指標のcriterion validityを示す | Chen et al. (2026) |
| 5層の独立した評価のconvergence（一貫した改善傾向）が間接的証拠 | Mangold et al. (2025): multi-method evaluation推奨 |
| 限界の明示的議論: 「実マネージャーによる検証はfuture work」 | Pičulin et al. (2025, ICML): proxy task限界の指摘 |

---

# 第9章　実施ロードマップ

| フェーズ | 内容 | 主要成果物 |
|---------|------|----------|
| **Phase 0** | データ取得・前処理 | Inside Airbnb地方地域データ（Tasmania, Trentino, Puglia等）+ Tokyo。calendar/reviews/listingsの統合。地方vs都市のボラティリティ基礎統計 |
| **Phase 1** | ABSAモジュール構築・精度評価 (L1) | BERTベースABSAパイプライン。300+アノテーションによるF1・κ評価 |
| **Phase 2** | ボラティリティ分析 + アブレーション (L2) | 都市-地方CVの比較。M0-M5アブレーション。口コミ感情の先行指標性検証 |
| **Phase 3** | 価格モデル構築 + バックテスト (L3) | ヘドニック+XGBoostモデル。ヒストリカルリプレイ。SHAP可視化 |
| **Phase 4** | 説明生成 + 品質評価 (L4) | LLM説明生成モジュール。LLM-as-Judge 5次元評価。事実支持率 |
| **Phase 5** | 経済性評価 (L5) | RevPARシミュレーション。感度分析 |
| **Phase 6** | 統合・論文執筆 | 5層評価結果の統合報告 |

---

# 参考文献一覧

1. Abrate, G., Nicolau, J.L., & Viglia, G. (2019). The impact of dynamic price variability on revenue maximization. *Tourism Management*, 74, 224–233.
2. Aggarwal, K. (2025). Tree models + SHAP for demand forecasting/price optimization.
3. Almeida, A., Moro, S., & Tavares, C. (2025). Neighbourhood–sentiment interactions in tourism pricing: a spatial analysis of Airbnb listings. *Tourism Management*, 107, 105061.
4. Alrawadieh, Z., Alrawadieh, Z., & Cetin, G. (2021). Digital transformation and revenue management: Evidence from the hotel industry. *Tourism Economics*, 27(2), 328–345.
5. Anderson, C.K. (2012). The impact of social media on lodging performance. *Cornell Hospitality Report*, 12(15), 6–11.
6. Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief*, 22, 41–49.
7. Bayoumi, A.E.M. et al. (2013). Dynamic pricing for hotel revenue management using price multipliers.
8. Binesh, F. et al. (2025). Deep learning + game-theoretic + SHAP for Airbnb pricing. *IJCHM*.
9. Castro, C. & Ferreira, F.A.F. (2018). Online hotel ratings and its influence on hotel room rates. *J. Hospitality & Tourism Technology*.
10. Chen, L. et al. (2026). Criterion Validity of LLM-as-Judge for Business Outcomes in Conversational Commerce. *arXiv:2604.00022*.
11. Cheng, X., Wang, W. & Ghose, A. (2025). LLMs for Explainable Business Decision-Making. *arXiv:2601.04208*.
12. Correa, J., Mari, M., & Xia, A. (2024). Dynamic pricing with Bayesian updates from online reviews. *arXiv:2404.14953*.
13. Degife, W.A. & Lin, B.-S. (2024). A multi-aspect informed GRU: A hybrid model of flight fare forecasting with sentiment analysis. *Applied Sciences*, 14(10), 4221.
14. Di Persio, L. & Lalmi, E. (2024). Maximizing profitability and occupancy: An optimal pricing strategy for Airbnb hosts. *JRFM*, 17(9), 414.
15. Fisher, M., Gallino, S. & Li, J. (2018). Competition-based dynamic pricing in online retailing. *Management Science*.
16. Gallego, G. & van Ryzin, G. (1994). Optimal Dynamic Pricing of Inventories with Stochastic Demand over Finite Horizons. *Management Science*, 40(8), 999–1020.
17. Garcia, D., Tolvanen, J., & Wagner, A.K. (2026). Strategic responses to algorithmic recommendations. *Management Science*.
18. Ghosh, A. et al. (2023). Airbnb pricing. *IJCHM*.
19. Gibbs, C. et al. (2018). Pricing in the sharing economy. *IJHM*.
20. Gómez-Talal, I., Talón-Ballestero, P., & Leoni, V. (2025). The impact of dynamic pricing on restaurant customers' perceptions. *Tourism Review*, 80(5), 1101.
21. Gordan, C., Borza, A., & Egresi, I. (2024). Rural tourism pricing: GWR analysis. Romania.
22. Habbat, N. et al. (2022). Hotel Demand Forecasting via Booking's Comments Using Sentiment Analysis and Topic Modeling. *AI2SD*, Springer.
23. Han, W. & Bai, B. (2022). Pricing research in hospitality and tourism: a systematic review. *IJCHM*, 34(5), 1717–1738.
24. Han, R., Guo, Y., Yu, H., & Li, X. (2024). WoM text mining for dynamic pricing. *JTAER*.
25. Heger, J. (2025). Optimization and (Explainable) AI for Revenue and Risk Management. PhD Dissertation, Univ. Augsburg.
26. Ivanov, S. & Webster, C. (2024). Automated decision-making: Hoteliers' perceptions. *Technology in Society*, 76, 102430.
27. Jiang, Y. (2024). Negative review asymmetry in demand.
28. Katz, M. (2026). Supply/demand forecasting with Inside Airbnb. *arXiv*.
29. Katz, M., Savage, D., & Coles, S. (2025). Booking lead-time dynamics 2018–2022. (被引用8件).
30. Kim, W.G., Lim, H., & Brymer, R.A. (2015). The effectiveness of managing social media on hotel performance. *IJHM*.
31. Lima Santos, L., Gomes, C., & Malheiros, C. (2024). Factors influencing hotel revenue management in times of crisis. *IJFS*, 12(4), 112.
32. Liskowski, P. & Jankowski, N. (2026). Arctic-ABSA: Aspect-Based Sentiment Analysis with Arctic Foundation Models. *arXiv*.
33. Liu, F., Lai, K., Wu, J., & Luo, X. (2022). eWoM in peer-to-peer accommodation. *IJEC*, 26(2), 218–245.
34. Liu, Y., Liu, J., Wang, Y., & Xu, J. (2026). Sentiment-based consumer segmentation for differential pricing. *JORS*.
35. Mei, S. (2025). DRL + hotel RM collaborative optimization.
36. Mohammed, I. & Denizci Guillet, B. (2025a). Heuristics and biases in hotel RM override decision-making. *IJCHM*, 37(2), 358–379.
37. Mohammed, I. & Denizci Guillet, B. (2025b). Stakeholder perspectives on integrating XAI into hotel RMS. *Tourism Economics*, OnlineFirst.
38. Munnaluri, V.K. (2022). Dynamic pricing in hospitality under data scarcity. Master's Thesis, Politecnico di Milano.
39. Nandinli, A.S., Srinu, N., & Senthil, M. (2024). Sentiment-Driven Predictions with BiLSTM for Hotel Demand Forecasting. *IJME*.
40. Nieto-García, M. et al. (2019). Staff & Facilities as most important pricing aspects. Airbnb.
41. Özen, İ.A. & Özgül Katlav, E. (2023). ABSA on technology-supported hotel reviews. *JHTT*, 14(2), 102–120.
42. Pičulin, M. et al. (2025). Position: Explainable AI Cannot Advance Without Better User Studies. *ICML 2025*.
43. Ray, R.K., Singh, A., & Dash, D.P. (2026). ABSA with Panel Data Modelling for Smartwatch Markets. *JEIM*.
44. Saitta, E., D'Amico, S. & Farinella, G.M. (2024). Hotel Dynamic Pricing Predictions with SHAP.
45. Schwartz, Z., Webb, T., & Liu, X. (2025). When RM analytics defies biased intuition. *European J. Tourism Research*.
46. Shin, D., Vaccari, S., & Zeevi, A. (2023). Dynamic pricing with online reviews. *Management Science*, 69(2), 1032–1053.
47. Sun, L., Schuckert, M., & Hon, A.H.Y. (2025). Organizational structures for RM in SME hotels. *IJHM*.
48. Talón-Ballestero, P., Nieto-García, M. et al. (2022). The wheel of dynamic pricing. *IJHM*, 103, 103213.
49. Talluri, K.T. & van Ryzin, G.J. (2004). *The Theory and Practice of Revenue Management*. Springer.
50. Tatlıdil, N.M., Yavuz, R., & Yöndem, M.T. (2025). Contract Price Optimization in Tourism with XAI. IEEE.
51. Torres, E.N., Singh, D., & Robertson-Ring, A. (2015). Consumer reviews and the creation of booking transaction value. *IJHM*.
52. Vives, A., Jacob, M., & Payeras, M. (2018). Revenue management and price optimization techniques in the hotel sector. *Tourism Economics*, 24(6), 628–651.
53. Wang, X. et al. (2025). A Two-Stage DRL-Driven Dynamic Discriminatory Pricing Model for Hotel Rooms. *JTAER*, 20(4), 337.
54. Wu, D.C., Zhong, S., Qiu, R.T.R., & Wu, J. (2022). Are customer reviews just reviews? Hotel forecasting using sentiment analysis. *Tourism Economics*, 28(3), 795–816.
55. Ye, Q., Law, R., & Gu, B. (2009). The impact of online user reviews on hotel room sales. *IJHM*.
56. Zaki, K. (2022). Implementing dynamic revenue management in hotels during Covid-19. *IJCHM*, 34(5), 1768–1795.
57. Zhang, J., Lu, X., & Liu, D. (2021). Deriving customer preferences for hotels based on ABSA. *ECRA*, 49, 101094.
58. Zhu, F. et al. (2022). Modeling Price Elasticity for Occupancy Prediction in Hotel DP. *CIKM 2022*.
59. Zhu, F. et al. (2024). "As there is no other public dataset for hotel pricing." *KDD*.
