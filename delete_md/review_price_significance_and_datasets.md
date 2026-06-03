# 口コミ情報が価格・需要に有意に寄与するエビデンスの精査、およびオープンデータセット調査

> **作成方針**: 本文書は査読付き論文・学術レポートに報告された事実（数値・手法・データ）のみを記載する。推測・著者の主観的解釈は含まない。

---

## 第1部　口コミのどの情報が、どの観点で、どの程度有意に価格・需要に寄与するか

### 1.1　総合レビュースコア → 価格（ADR）への影響

| 研究 | 被引用数 | データ | 手法 | 主要定量結果 |
|------|---------|--------|------|-------------|
| Anderson (2012) Cornell Hospitality Report | 609 | Travelocity掲載米国ホテル, ReviewPro GRI | OLS回帰 | 5段階スコア1点上昇 → ADR **11.2%増加**; ReviewPro GRI (100点制) 1点上昇 → ADR **0.89%増加**, 稼働率 **0.54%増加**, RevPAR **1.42%増加** |
| Castro & Ferreira (2018) Tourism Economics, cited 70 | 70 | Booking.com リスボン358ホテル | ヘドニック価格モデル, ロジットモデル | レビュースコア → **43.8%の価格プレミアム**と関連; 予約確率はレビュースコア1点あたり **1.142倍**に増加 |
| Öğüt & Onur Taş (2012) Service Industries Journal, cited 624 | 624 | Booking.com パリ・ロンドン ホテル | パネルデータ回帰 | オンラインレビュースコアがホテル客室価格に **有意な正の影響**; ロンドンではパリより効果が大きい（交差項の係数が有意） |
| Nieto-Garcia, Resce, Ishizaka, Occhiocupo & Viglia (2019) IJHM, cited 82 | 82 | Booking.comレーティング + STR RevPARデータ | PROMETHEE多基準意思決定分析 | RevPAR最大化に寄与するレーティング次元の重みは: **Staff（スタッフ）とFacilities（設備）が最も重要**; Location（立地）も重要 |
| Torres, Singh & Robertson-Ring (2015) IJHM, cited 228 | 228 | TripAdvisor + STRデータ | 回帰分析 | レビュースコア1点上昇 → ADR **9%増加** |
| Agušaj, Bazdan & Lujak (2017) Croatian Review, cited 46 | 46 | クロアチアのホテル | 回帰分析 | Anderson (2012) の知見を追試: 5段階で1点上昇 → 価格設定力の向上を確認 |

### 1.2　総合レビュースコア → 売上・予約数への影響

| 研究 | 被引用数 | データ | 手法 | 主要定量結果 |
|------|---------|--------|------|-------------|
| Ye, Law & Gu (2009) IJHM, cited 2,146 | 2,146 | Ctrip.com（中国最大旅行サイト）ホテル予約データ | 固定効果対数線形回帰モデル | オンラインレビューがホテル客室予約数に **有意な正の関係**; eWoMの量的・質的側面がともに予約を駆動 |
| Ye, Law, Gu & Chen (2011) cited 2,002 | 2,002 | Ctrip.com宿泊予約データ | パネルデータ回帰 | ユーザー生成コンテンツが旅行者の行動に有意な影響; レビュースコアの改善がオンライン予約を有意に増加 |
| Kim, Lim & Brymer (2015) IJHM, cited 658 | 658 | 国際ホテルチェーン実績データ + TripAdvisor | 回帰分析 | ソーシャルメディア管理（レビュー対応含む）がホテルパフォーマンスに **有意な正の影響**; 総合レーティングと経営者のレビュー返信がADR・RevPARに関連 |
| Noone & McGuire (2013) JRPM, cited 109 | 109 | 実験・調査データ | 実験的手法 | 5段階で1点のレビュースコア上昇がホテル選択行動に **有意な影響** |

### 1.3　テキスト感情分析（Sentiment）vs. 数値レーティング

| 研究 | 被引用数 | データ | 手法 | 主要定量結果 |
|------|---------|--------|------|-------------|
| Almeida, Teixeira, Franco & Silva (2025) Tourism & Hospitality | — | InsideAirbnb, ポルト地区 250,000+レビュー (2016–2020) | ヘドニック空間回帰 (SAR), gs2sls推定量 | テキストから算出した**Sentimentスコア**は、数値レーティングのみのモデルより**高い説明力**（Model 2 > Model 1の擬似R²）; テキスト感情分析が数値スコアを上回る価格説明変数であることを実証 |
| Di Persio & Lalmi (2024) JRFM, cited 8 | 8 | InsideAirbnb パリ (May 2023), 65,000+物件 | BoW, TF-IDF, ABSA(CNN) | レビューテキストのNLP特徴量（BoW, TF-IDF）が価格予測精度を向上; ABSA(CNN)による感情特徴量が物件価格の説明に寄与 |

### 1.4　アスペクトレベルの口コミ情報（ABSA）→ 価格・需要予測

| 研究 | 被引用数 | データ | 手法 | アスペクト | 主要定量結果 |
|------|---------|--------|------|----------|-------------|
| **Degife & Lin (2024)** Applied Sciences, cited 10 | 10 | 841,160航空券記録 + 46,167消費者レビュー (Skytrax, TripAdvisor) | BERT抽出 → 9アスペクトグループ → GRU (7層) | Booking/Ticketing, Pre-flight, Airport Services, In-flight Amenities, Seat/Cabin, **Staff**, **Safety/Security**, **Cleanliness**, Post-flight | 全アスペクトモデル: RMSE=0.0071, MAE=0.0137, **R²=0.9899**; **Safety & Security除去 → R²=0.6752** (Δ=−0.3147); **Staff除去 → R²=0.8142** (Δ=−0.1757); Cleanliness除去 → R²=0.9379 (Δ=−0.0520); Safety↔Fare相関 r=0.98*** |
| Gordan, Florian, Gaman & Rus (2024) Agriculture, cited 10 | 10 | 5,028宿泊施設, ルーマニア1,170行政区 (農村観光) | Hybrid LASSO-OLS + GWR | 施設属性・地域属性 | **顧客レーティング（TripAdvisor/Booking.com）→ 価格に有意な正の効果**; レビュー数は**有意だが負の係数**（小さい）; 5km圏内Google Mapsレビュー×スコア（Tourism Attractivity）→ **有意な正の効果** |
| Santos (2016) hostel study | — | 8,000ホステル（世界規模） | ヘドニック価格モデル | Cleanliness, Location, Amenities | Cleanliness（清潔さ）, Location（立地）, Amenities（設備）が価格に**最も有意な影響** |
| Nieto-Garcia et al. (2019) IJHM, cited 82 | 82 | Booking.com + STR RevPAR | PROMETHEE | Staff, Facilities, Location, Cleanliness, Comfort, Value | **Staff（スタッフ）** と **Facilities（設備）** がRevPAR最大化に最も寄与; Locationも重要 |

### 1.5　負の口コミの非対称的影響

| 研究 | 被引用数 | データ | 手法 | 主要定量結果 |
|------|---------|--------|------|-------------|
| Almeida et al. (2025) | — | InsideAirbnb ポルト | ヘドニック空間回帰（SAR） | ネガティブレビューの価格影響はポジティブレビューの **2倍**; 低価格帯物件では **4倍** |
| Jiang et al. (2024) | — | Airbnb | — | ネガティブレビューの価格影響はポジティブレビューの **2倍**; 低価格帯で **4倍** (Almeida et al. 2025が引用) |
| Lin & Yang (2023) | — | Airbnb 米国26地域 | — | 物件特性・立地に関するレビューが**最も有意な価格影響**; 中心部物件はネガティブレビューの影響を受けにくい |

### 1.6　レビュー量（件数）の影響

| 研究 | 被引用数 | データ | 主要定量結果 |
|------|---------|--------|-------------|
| Gordan et al. (2024) | 10 | ルーマニア農村観光5,028施設 | レビュー件数は**統計的に有意だが負の係数**（小さい値）— 件数が多い物件は価格が若干低い傾向 |
| Gibbs et al. (2018) | — | Airbnb カナダ5都市 | レビュー件数は価格と**負の相関** |
| Almeida et al. (2025) | — | Airbnb ポルト | レビュー件数は価格に**負の関連**（Gibbs et al. 2018と一致） |

### 1.7　農村・地方・小規模施設における知見

| 研究 | 被引用数 | データ | 主要定量結果 |
|------|---------|--------|-------------|
| Gordan et al. (2024) | 10 | ルーマニア農村観光 | OLS: サウナ→+13.54%, 4つ星→+19.60%, 5つ星→+31.65%, マッサージ→+26.62%, 山小屋→+18.41%, 農泊→+18.06%; アイロン→−4.88%; **GWR vs OLS: F=1.45, p<2.2×10⁻¹⁶** — 効果は地域で大きく異なる (GWR AIC=11,787 vs OLS AIC=16,231) |
| Almeida et al. (2025) | — | Airbnb ポルト（都市・農村混合） | 「都市と農村の混合地域は先行研究で**著しく欠落**している」と指摘; 農村的物件とリスティング属性・レビューの相互作用を初めて分析 |

### 1.8　第1部のまとめ — エビデンスの構造

口コミが価格・需要に有意に寄与する経路は、以下の4つに整理できる:

**経路A: 総合スコア → 価格プレミアム（ヘドニック価格モデル）**
- 5段階スコア1点上昇 → ADR 9–11.2%増加 (Anderson 2012; Torres et al. 2015)
- レビュースコア → 43.8%の価格プレミアム (Castro & Ferreira 2018)
- GRI 1点上昇 → RevPAR 1.42%増加 (Anderson 2012)

**経路B: テキスト感情 > 数値スコア**
- Sentimentスコアは数値レーティング単独より高い価格説明力 (Almeida et al. 2025)
- NLP特徴量（BoW, TF-IDF, ABSA）が価格予測精度を向上 (Di Persio & Lalmi 2024)

**経路C: アスペクト別感情 → 需要予測精度の飛躍的向上**
- 9アスペクトABSA統合: R²=0.9899 vs 除去時の大幅低下 (Degife & Lin 2024)
- Safety/Security除去でR²が0.3147低下、Staff除去で0.1757低下
- RevPAR最大化には Staff, Facilities が最重要 (Nieto-Garcia et al. 2019)

**経路D: 負のレビューの非対称的影響**
- ネガティブレビューの影響は正の2倍、低価格帯で4倍 (Almeida et al. 2025; Jiang et al. 2024)
- 中心地立地は負のレビュー影響を緩和 (Lin & Yang 2023)

---

## 第2部　価格・需要のボラティリティを持つオープンソースデータセット — 網羅的調査

> **調査方針**: WEB上で存在するすべてのオープンデータを網羅的にリサーチし、各データセットについて **URL・変数一覧・ライセンス・期間・サイズ・更新頻度・ダウンロード数・価格の有無・口コミの有無・時系列性・日本データの有無・実際の活用可能性** を完全にまとめる。事実のみに基づき、推測は一切含まない。

---

### 2.1　宿泊・短期賃貸ドメイン — Airbnb系データ

#### 2.1.1 Inside Airbnb（公式プロジェクト）

| 項目 | 内容 |
|------|------|
| **URL** | http://insideairbnb.com/get-the-data/ |
| **ライセンス** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **更新頻度** | 四半期ごと（直近1年分を無料公開）。2025年9月29日時点の最新データが確認済み |
| **日本データ** | **Tokyo, Kantō, Japan** — スナップショットあり |
| **提供ファイル (都市別)** | ① listings.csv.gz (物件詳細全変数), ② calendar.csv.gz (**日次価格データ**: listing_id, date, available, price, adjusted_price, minimum_nights, maximum_nights), ③ reviews.csv.gz (**レビュー全文テキスト**: listing_id, id, date, reviewer_id, reviewer_name, comments), ④ listings.csv (サマリー版), ⑤ reviews.csv (サマリー版), ⑥ neighbourhoods.csv, ⑦ neighbourhoods.geojson |
| **listings.csv.gz 主要変数** | id, listing_url, name, description, neighborhood_overview, host_id, host_name, host_since, host_response_time, host_response_rate, host_acceptance_rate, host_is_superhost, neighbourhood_cleansed, latitude, longitude, property_type, room_type, accommodates, bathrooms, bedrooms, beds, amenities, **price**, minimum_nights, maximum_nights, availability_30/60/90/365, number_of_reviews, number_of_reviews_ltm, first_review, last_review, **review_scores_rating**, **review_scores_accuracy**, **review_scores_cleanliness**, **review_scores_checkin**, **review_scores_communication**, **review_scores_location**, **review_scores_value**, calculated_host_listings_count, reviews_per_month 等 |
| **地域規模** | 世界100+都市・地域。2025年より12カ国の**地域アーカイブファイル**（Regional Archive）も提供開始 |
| **地方・非都市部データ** | Barossa Valley (豪), Barwon South West (豪), Crete (希), Hawaii (米), Mid North Coast (豪), Mornington Peninsula (豪), Northern Rivers (豪), Puglia (伊), Sicily (伊), Sunshine Coast (豪), Tasmania (豪), Trentino (伊), Western Australia (豪), New Zealand (全国), Ireland (全国), Malta 等 |
| **ボラティリティ特性** | calendar.csv.gzに**日次の掲載価格**が含まれ、季節変動・イベント変動の分析が可能。Katz (2026, arXiv) は「publicly available calendar data from Inside Airbnb」を使い supply/demand forecasting の再現可能性を実証。Katz, Savage & Coles (2025, cited 8) は2018–2022年の予約リードタイム動態を分析しCOVID-19前後の volatility を定量化 |
| **口コミとの結合** | reviews.csv にレビュー全文テキスト（日付・reviewer_id付き）; listings.csv に7次元スコア (rating, accuracy, cleanliness, checkin, communication, location, value) |
| **先行研究での使用例** | Almeida et al. (2025) ポルト; Di Persio & Lalmi (2024) パリ; Costa (2025) リスボン・ポルト; Ghosh et al. (2023, IJCHM cited 53) NYC; Mundiya (2025) 価格予測; Katz (2026) 需給予測 |
| **活用可能性評価** | ★★★★★ — **宿泊ドメインで口コミ+価格+時系列のすべてを満たす唯一のオープンデータ源**。日本（東京）データあり。ABSA適用にレビュー全文が利用可能。日次カレンダーでボラティリティ分析可能 |

#### 2.1.2 Tokyo Airbnb Open Data 2023 (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023 |
| **ライセンス** | CC0: Public Domain |
| **サイズ** | 400 MB, 8ファイル, **110カラム** |
| **ファイル構成** | calendar.csv, listings.csv, neighbourhoods.csv, neighbourhoods.geojson, reviews.csv, summary_listings.csv, summary_reviews.csv, Tokyo_map.png |
| **データ収集日** | 2021年12月6日収集（2021年10月28日時点のリスティング）。タイトルは「2023」だがデータ自体は2021年 |
| **サンプル数** | 約10,700物件 |
| **ダウンロード数** | 511 (累計2,688ビュー) |
| **更新頻度** | Never（静的データセット） |
| **ソース** | Inside Airbnb (http://insideairbnb.com/get-the-data/) からの二次配布 |
| **変数** | Inside Airbnb と同一構造（listings: 価格, レビュースコア7次元, ホスト情報, amenities等; calendar: 日次価格; reviews: 全文テキスト） |
| **活用可能性評価** | ★★★☆☆ — 東京データとしてKaggle上で手軽に取得可能だが、Inside Airbnbから直接取得すればより最新のデータが利用可能。実際のデータは2021年時点 |

#### 2.1.3 Airbnb Listings & Reviews — 10 Major Cities (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/mysarahmadbhat/airbnb-listings-reviews |
| **ライセンス** | CC0: Public Domain |
| **サイズ** | 414.32 MB, 4ファイル, **41カラム** |
| **ファイル構成** | Listings.csv (158.5 MB), Listings_data_dictionary.csv, Reviews.csv (255.82 MB), Reviews_data_dictionary.csv |
| **レコード数** | **250,000+リスティング**, **5,000,000+レビュー** |
| **対象都市** | 10主要都市（具体的都市名はデータ辞書参照） |
| **更新頻度** | Monthly（月次更新） |
| **ダウンロード数** | 10,100 (累計67,000ビュー) |
| **ソース** | Inside Airbnb からの二次配布 |
| **変数** | 価格（各都市の現地通貨）, レビューテキスト, レビュースコア。データ辞書CSV同梱 |
| **活用可能性評価** | ★★★★☆ — 複数都市の統合データが1ファイルで取得可能。月次更新で比較的新しい。ただし Inside Airbnb 直接取得と本質的に同一 |

#### 2.1.4 Seattle Airbnb Open Data (Kaggle — Airbnb公式)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/airbnb/seattle |
| **ライセンス** | CC0: Public Domain |
| **サイズ** | 90.11 MB, 3ファイル, **102カラム** |
| **ファイル構成** | calendar.csv (36.65 MB: listing_id, date, available, price), listings.csv (物件詳細: 92カラム), reviews.csv (レビュー全文テキスト) |
| **ダウンロード数** | 51,600 (累計310,000ビュー) |
| **更新頻度** | Not specified（静的） |
| **ソース** | **Airbnb公式** (Airbnb Inside initiative) — Inside Airbnb (Murray Cox) の方ではなく、Airbnb社自体がKaggle Organizationとして公開 |
| **変数（calendar.csv）** | listing_id, date, available (t/f), price |
| **変数（listings.csv 主要）** | id, listing_url, name, summary, space, description, neighborhood_overview, transit, access, interaction, house_rules, host_id, host_since, host_response_time, host_response_rate, host_is_superhost, neighbourhood, zipcode, latitude, longitude, property_type, room_type, accommodates, bathrooms, bedrooms, beds, bed_type, amenities, square_feet, **price**, weekly_price, monthly_price, security_deposit, cleaning_fee, guests_included, extra_people, minimum_nights, maximum_nights, availability_30/60/90/365, number_of_reviews, first_review, last_review, **review_scores_rating**, **review_scores_accuracy**, **review_scores_cleanliness**, **review_scores_checkin**, **review_scores_communication**, **review_scores_location**, **review_scores_value**, reviews_per_month 等 |
| **活用可能性評価** | ★★★★☆ — Airbnb公式提供で信頼性高。calendar.csvで日次価格変動分析可。レビュー全文+7次元スコアあり。ただしシアトル1都市分 |

#### 2.1.5 U.S. Airbnb Open Data (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/kritikseth/us-airbnb-open-data |
| **ライセンス** | CC0: Public Domain |
| **サイズ** | 75.16 MB, 2ファイル, **35カラム** |
| **ファイル構成** | AB_US_2020.csv (36.08 MB), AB_US_2023.csv |
| **収集日** | 2020年10月20日 (v1), 2023年4月14日更新 (v2) |
| **更新頻度** | Annually（年次） |
| **ダウンロード数** | 15,100 (累計107,000ビュー) |
| **ソース** | Inside Airbnb からの二次コンパイル |
| **変数** | host_id, host_name, listing_id, listing_name, latitude, longitude, neighbourhood, **price**, room_type, minimum_nights, number_of_reviews, last_review_date, reviews_per_month, availability, host_listings, city 等 |
| **制約** | **レビューテキストなし**, **レビュースコアなし**, **calendarデータなし** — サマリー版のみ |
| **活用可能性評価** | ★★☆☆☆ — 米国全体の広域概観には有用だが、レビューテキスト・スコアがなくABSA研究には不適。Inside Airbnbから直接取得した方が詳細 |

#### 2.1.6 Airbnb Price Determinants in Europe (Kaggle / Zenodo)

| 項目 | 内容 |
|------|------|
| **URL (Kaggle)** | https://www.kaggle.com/datasets/thedevastator/airbnb-price-determinants-in-europe |
| **URL (Zenodo原典)** | https://zenodo.org/records/4446043 (DOI: 10.5281/zenodo.4446043) |
| **ライセンス** | CC0: Public Domain (Kaggle) / CC BY 4.0 (Zenodo原典) |
| **サイズ** | 10.76 MB (Kaggle), 10.8 MB (Zenodo) |
| **ファイル構成** | **20ファイル**: 10ヨーロッパ都市 × weekday/weekend (amsterdam_weekdays.csv, amsterdam_weekends.csv, athens_weekdays.csv, ... vienna_weekends.csv) + models_robust.py (Zenodo版) |
| **対象都市** | Amsterdam, Athens, Barcelona, Berlin, Budapest, Lisbon, London, Paris, Rome, Vienna |
| **論文** | Gyódi, K. & Nawaro, Ł. (2021). Determinants of Airbnb prices in European cities: A spatial econometrics approach. *Tourism Management*, 86, 104319. DOI: 10.1016/j.tourman.2021.104319 |
| **Zenodo統計** | 11,000ビュー, 14,000ダウンロード |
| **変数 (20カラム)** | **realSum** (2人2泊の合計価格EUR), room_type, room_shared, room_private, person_capacity, host_is_superhost, multi (2–4件ホスト), biz (5件以上ホスト), **cleanliness_rating**, **guest_satisfaction_overall**, bedrooms, **dist** (市中心部からの距離km), **metro_dist** (最寄地下鉄駅距離km), **attr_index** (観光アトラクション指数), attr_index_norm (正規化0–100), **rest_index** (レストラン指数), rest_index_norm (正規化0–100), lng, lat |
| **時系列性** | **なし** — 「This dataset however does not provide dates」と明記。スナップショットのみ |
| **制約** | **日付データなし**（時系列分析不可）。**レビューテキストなし**。スコアは cleanliness_rating と guest_satisfaction_overall の2つのみ |
| **活用可能性評価** | ★★★☆☆ — 空間回帰分析（ヘドニック価格モデル）の再現に最適。価格+満足度+立地の組み合わせは有用。ただし時系列なし・レビューテキストなしでABSA研究には不適 |

#### 2.1.7 その他のKaggle上Airbnbデータセット（確認済み）

Kaggle上でAirbnbに関連するデータセットは **65件以上** 確認されている。主要なものを以下に整理する。いずれも Inside Airbnb を原典とする二次配布であり、変数構造は基本的に同一。

| データセット名 | Kaggle URL | 対象地域 | サイズ | DL数 | 備考 |
|--------------|-----------|---------|-------|-----|------|
| Boston Airbnb Open Data | kaggle.com/datasets/airbnb/boston | Boston | 17 MB, 3ファイル | 25,600 | Airbnb公式提供。calendar+listings+reviews |
| New York Airbnb Open Data 2024 | kaggle.com/datasets/vrindakallu/new-york-dataset | NYC | 1 MB | 4,212 | サマリーのみ |
| London UK Airbnb Open Data | kaggle.com/datasets/whenamancodes/london-uk-airbnb-open-data | London | 4 MB | 2,354 | サマリーのみ |
| Airbnb Beijing | kaggle.com/datasets/merryyundi/airbnb-beijing-20190211 | 北京 | 74 MB, 3ファイル | 1,002 | calendar+listings+reviews |
| Copenhagen AirBnb Open Data | kaggle.com/datasets/dcschmidt/airbnbcopenhagen | Copenhagen | 48 MB, 3ファイル | 250 | calendar+listings+reviews |
| Tokyo Airbnb Detailed Open Data | kaggle.com/datasets/fuyutaro/tokyo-airbnb-detailed-open-data | **東京** | 104 MB, 3ファイル | 268 | Fuyutaro Suzuki作成。InsideAirbnb由来 |
| Tokyo Airbnb Open Data (Takumi) | kaggle.com/datasets/tsarromanov/tokyo-airbnb-open-data | **東京** | 53 MB, 6ファイル | 372 | InsideAirbnb由来 |
| AirBnB Listings in California | kaggle.com/datasets/setseries/airbnb-listings-in-california | California | 37 MB | 378 | サマリーのみ |
| Airbnb Global Accommodation and Reviews | kaggle.com/... | 複数国 | 不明 | — | グローバルコンパイル |
| Airbnb Listings: NYC/London/Paris/Tokyo & More | kaggle.com/... | 複数都市（**東京含む**） | 不明 | — | 複数都市統合版 |

---

### 2.2　宿泊ドメイン — ホテル予約・価格データ

#### 2.2.1 Hotel Booking Demand Dataset (Antonio, de Almeida & Nunes, 2019)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand |
| **論文** | Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief*, 22, 41–49. DOI: 10.1016/j.dib.2018.11.126 |
| **被引用数** | 123 |
| **ライセンス** | CC BY 4.0 |
| **サイズ** | 16.86 MB, 1ファイル (hotel_bookings.csv), **32カラム** |
| **ダウンロード数** | **211,000** (累計1,400,000ビュー) — Kaggle上の宿泊関連データで最大級 |
| **更新頻度** | Never（静的データセット） |
| **データ構造** | **2ホテル**: H1=リゾートホテル (40,060予約), H2=シティホテル (79,330予約); 合計 **119,390観測値** |
| **期間** | 2015年7月1日 – 2017年8月31日 |
| **変数 (32カラム)** | hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month, stays_in_weekend_nights, stays_in_week_nights, adults, children, babies, meal, country, market_segment, distribution_channel, is_repeated_guest, previous_cancellations, previous_bookings_not_canceled, reserved_room_type, assigned_room_type, booking_changes, deposit_type, agent, company, days_in_waiting_list, customer_type, **adr** (Average Daily Rate), required_car_parking_spaces, total_of_special_requests, reservation_status, reservation_status_date |
| **ボラティリティ特性** | adr (日次平均客室料金) に**明確な季節変動**あり（リゾートホテルは特に顕著）。キャンセル率37%。リードタイム変動も大きい |
| **制約** | ホテル・顧客の識別情報は削除済み。**口コミテキスト・レビュースコアは非含有**。ポルトガルの2ホテルのみ |
| **活用可能性評価** | ★★★★☆ — 価格(ADR)+季節性+需要変動の分析に最適。211Kダウンロードの信頼性。ただしレビューデータ一切なし |

#### 2.2.2 TBO Hotels Dataset (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/raj713335/tbo-hotels-dataset |
| **ライセンス** | MIT |
| **サイズ** | 2.41 GB, 1ファイル (hotels.csv), **16カラム**, 1,000,000+行 |
| **更新頻度** | Annually |
| **変数** | countyCode, countyName, cityCode, cityName, HotelCode, hotel_name, HotelRating (1–5星), Address, Attractions, Description, FaxNumber, HotelFacilities, Map (lat/lng), PhoneNumber, PinCode, HotelWebsiteUrl |
| **制約** | **価格データなし**, **レビューテキストなし**, **レビュースコアなし（星評価のみ）**, **時系列データなし** — 静的ホテルメタデータのカタログ |
| **活用可能性評価** | ★☆☆☆☆ — ホテル属性（施設・立地）の参照用のみ。価格・レビュー研究には不適 |

---

### 2.3　宿泊ドメイン — レビュー・口コミデータ

#### 2.3.1 515K Hotel Reviews Data in Europe (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe |
| **ライセンス** | CC0: Public Domain |
| **サイズ** | 238.15 MB, 1ファイル (Hotel_Reviews.csv), **17カラム**, **515,000レビュー**, **1,493ラグジュアリーホテル** |
| **ダウンロード数** | **48,100** (累計287,000ビュー) |
| **更新頻度** | Never（7年前に公開） |
| **ソース** | Booking.com からのスクレイピング |
| **変数 (17カラム)** | Hotel_Address, Additional_Number_of_Scoring, Review_Date, Average_Score, Hotel_Name, Reviewer_Nationality, **Negative_Review** (テキスト), Review_Total_Negative_Word_Counts, Total_Number_of_Reviews, **Positive_Review** (テキスト), Review_Total_Positive_Word_Counts, Total_Number_of_Reviews_Reviewer_Has_Given, **Reviewer_Score**, Tags, days_since_review, lat, lng |
| **レビュー構造** | **ポジティブ/ネガティブが分離されたテキスト** — ABSA研究にとって非常に有用な構造。Reviewer_Score (個別), Average_Score (ホテル全体) |
| **対象地域** | ヨーロッパの主要都市（ロンドン, パリ, バルセロナ, アムステルダム等の高級ホテル） |
| **制約** | **価格データなし**。時系列としてはReview_Dateのみ。ラグジュアリーホテルに偏り |
| **活用可能性評価** | ★★★★☆ — ABSA研究のトレーニング/テストデータとして最適級。ポジティブ/ネガティブ分離構造はsentiment分析に直接利用可能。ただし価格データなし |

#### 2.3.2 Booking.com Hotel Reviews (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/thedevastator/booking-com-hotel-reviews |
| **ライセンス** | Other (specified in description) — ソース: CrawlFeeds/data.world |
| **サイズ** | 49.45 MB, 1ファイル, **16カラム**, 700,000+レコード |
| **変数** | review_title, reviewed_at (datetime), reviewed_by, images, crawled_at, url, hotel_name, hotel_url, avg_rating, nationality, **review_text**, raw_review_text, tags, meta |
| **制約** | **価格データなし**, **時系列的価格変動なし**。ライセンスが「Other」で商用利用の可否が不明確 |
| **活用可能性評価** | ★★★☆☆ — レビューテキスト+評価のNLP研究に使用可。ただしライセンスの曖昧さとスクレイピング由来の法的リスクに注意 |

#### 2.3.3 TripAdvisor Hotel Reviews (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews |
| **ライセンス** | CC BY-NC 4.0 (非営利のみ) |
| **サイズ** | 14.97 MB, 1ファイル, **2カラムのみ** (Review, Rating), **20,491レビュー** |
| **ダウンロード数** | **45,900** (累計311,000ビュー) |
| **引用** | Alam, M. H., Ryu, W.-J., & Lee, S. (2016). DOI: 10.5281/zenodo.1219899 |
| **変数** | Review (テキスト), Rating (1–5) |
| **制約** | **ホテル名なし**, **価格なし**, **日付なし**, **地域情報なし** — テキストとスコアの2カラムのみ |
| **活用可能性評価** | ★★☆☆☆ — Sentiment分析モデルのトレーニングには使用可。ただし2カラムのみで実践的研究には情報量不足。非営利限定ライセンス |

#### 2.3.4 Eco-hotel Reviews (UCI ML Repository)

| 項目 | 内容 |
|------|------|
| **URL** | https://archive.ics.uci.edu/dataset/398/eco+hotel |
| **DOI** | 10.24432/C5M30H |
| **ライセンス** | CC BY 4.0 |
| **サイズ** | 110.8 KB, 1ファイル (dataset-CalheirosMoroRita-2017.csv) |
| **レコード数** | **401レビュー** |
| **期間** | 2015年1月 – 8月 |
| **ソース** | TripAdvisor (オンライン) + ゲストブック (オフライン) — ポルトガル Areias do Seixo Eco-Resort |
| **変数** | テキストレビュー (1カラム) |
| **引用** | Calheiros, C., Moro, S., & Rita, P. (2017) |
| **制約** | 401件のみ。**単一リゾートのレビューテキストのみ**。価格・スコア・日付なし |
| **活用可能性評価** | ★☆☆☆☆ — サンプル数が極めて少なく、研究利用は限定的 |

#### 2.3.5 Travel Review Ratings (UCI ML Repository)

| 項目 | 内容 |
|------|------|
| **URL** | https://archive.ics.uci.edu/dataset/485/tarvel+review+ratings |
| **DOI** | 10.24432/C5C31Q |
| **ライセンス** | CC BY 4.0 |
| **サイズ** | 622.1 KB, 1ファイル (google_review_ratings.csv) |
| **レコード数** | **5,456件** |
| **変数 (25カラム)** | userid, churches, resorts, beaches, parks, theatres, museums, malls, zoos, restaurants, pubs_bars, local_services, burger_pizza_shops, **hotels_other_lodgings**, juice_bars, art_galleries, dance_clubs, swimming_pools, gyms, bakeries, beauty_spas, cafes, view_points, monuments, gardens |
| **データ型** | 各カテゴリの平均Googleレビュースコア (1–5) |
| **引用** | Renjith, S. (2018). Evaluation of Partitioning Clustering Algorithms in Tourism Domain. *IEEE RAICS*. |
| **制約** | ホテルは24カテゴリのうち1カテゴリのみ。テキストなし, 価格なし, 時系列なし |
| **活用可能性評価** | ★☆☆☆☆ — 観光カテゴリ別のクラスタリング研究用。宿泊価格研究には不適 |

---

### 2.4　宿泊ドメイン — ホテル価格データ（非公開・商用）

#### 2.4.1 STR (Smith Travel Research)

| 項目 | 内容 |
|------|------|
| **URL** | https://str.com/ |
| **ライセンス** | **商用ライセンス（非公開）** — 研究利用にも契約が必要 |
| **変数** | ADR, RevPAR, 稼働率, Supply, Demand 等の日次・週次・月次集計 |
| **カバレッジ** | 世界180+カ国、80,000+ホテル |
| **制約** | Zhu et al. (2024, KDD) は "As there is no other public dataset for hotel pricing" と記述。Ampountolas & Legg (2021) も "data is limited to a data set provided by a major chain hotel" と記述 |
| **活用可能性評価** | ☆☆☆☆☆ — 業界標準データだが**完全に非公開**。学術利用でも高額ライセンス必要 |

#### 2.4.2 OTA内部データ（Booking.com, Expedia等）

| 項目 | 内容 |
|------|------|
| **公開状況** | **非公開** |
| **備考** | Angelini, Costa & Guizzardi (2025, Big Data Research) はBooking.comの「時系列の時系列」データを使用しているが、論文記述では非公開。Gordan et al. (2024) のルーマニア5,028施設データも生データの公開は未確認 |

---

### 2.5　他ドメイン — 価格ボラティリティを持つオープンデータ

#### 2.5.1 NYC TLC Trip Record Data（ライドシェア・タクシー）

| 項目 | 内容 |
|------|------|
| **URL** | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page |
| **ライセンス** | パブリックドメイン（NYC Open Data） |
| **期間** | **2009年 – 現在**（毎月更新、2ヶ月遅れ） |
| **フォーマット** | Parquet形式（年月別ファイル） |
| **データ種別** | ① Yellow Taxi, ② Green Taxi, ③ FHV (For-Hire Vehicle), ④ High Volume FHV (Uber, Lyft) |
| **Yellow Taxi主要変数** | VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, trip_distance, RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, payment_type, **fare_amount**, extra, mta_tax, **tip_amount**, tolls_amount, improvement_surcharge, **total_amount**, congestion_surcharge, airport_fee, **cbd_congestion_fee** (2025年〜新設) |
| **HVFHV主要変数** | hvfhs_license_num, dispatching_base_num, originating_base_num, request_datetime, on_scene_datetime, pickup_datetime, dropoff_datetime, PULocationID, DOLocationID, trip_miles, trip_time, **base_passenger_fare**, tolls, bcf, sales_tax, congestion_surcharge, airport_fee, tips, **driver_pay**, shared_request_flag, shared_match_flag, access_a_ride_flag, wav_request_flag, wav_match_flag, **cbd_congestion_fee** |
| **ボラティリティ特性** | 時間帯・天候・イベントによる需要変動。サージプライシングの動態を分析可能 |
| **活用可能性評価** | ★★★☆☆ — サージプライシング（需要駆動型価格変動）のベンチマークとして有用。ただし宿泊ドメインとは異なる |

#### 2.5.2 米国運輸統計局 (BTS) DB1B — 航空運賃データ

| 項目 | 内容 |
|------|------|
| **URL** | https://www.transtats.bts.gov/ (Airline Origin and Destination Survey) |
| **ライセンス** | パブリックドメイン（米国連邦政府データ） |
| **期間** | 1993年Q1 – 現在（四半期更新） |
| **変数** | OriginAirportID, DestAirportID, **MktFare** (市場運賃), MktDistance, **Passengers**, ItinFare, BulkFare, MktCoupons, OperatingCarrier, RPCarrier 等 |
| **ボラティリティ特性** | 路線・季節・燃料価格による運賃変動が大きい。Degife & Lin (2024) が航空レビュー+運賃のABSA研究で参照 |
| **活用可能性評価** | ★★☆☆☆ — 航空ドメインの価格変動研究用。宿泊とは異なるが、需要駆動型価格変動のアナロジーとして参考可能 |

#### 2.5.3 Skytrax + TripAdvisor 航空レビューデータ

| 項目 | 内容 |
|------|------|
| **使用例** | Degife & Lin (2024, Applied Sciences) で使用: 841,160航空券記録 + 46,167消費者レビュー |
| **取得方法** | Skytraxからのスクレイピング。Kaggle上にも類似データあり (airlinequality.com由来) |
| **ライセンス** | スクレイピング由来 — 明示的ライセンスなし。利用規約要確認 |
| **ABSA適用** | 9アスペクトグループ (Booking/Ticketing, Pre-flight, Airport Services, In-flight Amenities, Seat/Cabin, Staff, Safety/Security, Cleanliness, Post-flight) → R²=0.9899 |
| **活用可能性評価** | ★★☆☆☆ — ABSA手法の参照として有用だが、スクレイピング由来の法的リスクあり |

#### 2.5.4 Uber Fares Dataset (Kaggle)

| 項目 | 内容 |
|------|------|
| **URL** | Kaggle上に複数のUber運賃データセットが存在 |
| **使用例** | Muhammad (2025) がダイナミックプライシング研究で使用 |
| **ボラティリティ** | サージプライシングによる価格変動を含む |
| **活用可能性評価** | ★★☆☆☆ — サージプライシングのアナロジーとしてのみ |

#### 2.5.5 電力市場データ

| データソース | URL | ライセンス | 変数 | 粒度 | ボラティリティ |
|------------|-----|----------|------|------|--------------|
| **ERCOT** (テキサス) | ercot.com/gridmktinfo/dashboards | パブリック（テキサス州法） | リアルタイム価格 ($/MWh), DAM価格, 負荷, 風力/太陽光発電量 | 5分/15分/1時間 | 極端な価格スパイク（2021年 $9,000/MWh）。$0〜$5,000+のレンジ |
| **AEMO** (豪州) | aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem | パブリック | スポット価格 (AUD/MWh), 需要, 発電量, インターコネクタフロー | 5分 | 季節変動 + 再エネ由来の高ボラティリティ。ネガティブ価格も発生 |
| **JEPX** (日本) | jepx.jp | パブリック（会員登録で閲覧可） | スポット価格 (円/kWh), 約定量, 売り入札量, 買い入札量, ブロック入札 | 30分 (48コマ/日) | 需給逼迫時に ¥100/kWh超のスパイク |

**電力市場データの活用可能性評価**: ★★☆☆☆ — 価格ボラティリティの参照ドメインとして。宿泊ドメインとは本質的に異なるが、リアルタイム需給バランスによる価格形成メカニズムのアナロジーとして引用可能

---

### 2.6　日本の公的統計データ — 宿泊業関連

#### 2.6.1 宿泊旅行統計調査（観光庁）

| 項目 | 内容 |
|------|------|
| **URL** | https://www.mlit.go.jp/kankocho/siryou/toukei/shukuhakutoukei.html |
| **管轄** | 国土交通省 観光庁 観光戦略課観光統計調査室 |
| **ライセンス** | 政府統計（利用規約に基づく二次利用可。出典明記が必要） |
| **期間** | **2007年〜現在** — 月次で継続公開 |
| **更新頻度** | **月次**（第1次速報: 翌々月、第2次速報: 3ヶ月後、確定値: 年次） |
| **最新データ** | 2026年2月分（第1次速報値）、2026年1月分（第2次速報値）が2026年3月31日時点で公開済み |
| **フォーマット** | Excel (.xlsx) 形式でダウンロード可能 |
| **主要変数** | ① **延べ宿泊者数**（日本人・外国人別）、② **稼働率**（客室稼働率・定員稼働率）、③ **施設タイプ別**（旅館・ホテル・リゾートホテル・ビジネスホテル・シティホテル・簡易宿所）、④ **都道府県別**、⑤ **従業員数/客室数規模別** |
| **地域粒度** | **都道府県別** (47都道府県) + **広域市町村130区分別**（参考表として別途公開） |
| **層化基準** | 2026年1月～従業者数→**客室数**に変更 |
| **制約** | **個票データは非公開**（集約統計のみ）。宿泊料金の直接データは含まれない（稼働率・宿泊者数のみ）。口コミデータなし |
| **活用可能性評価** | ★★★★☆ — **日本の地方宿泊施設の需要トレンド（季節変動・稼働率）を把握する唯一の公的データ源**。長野県（信州）の月次需要変動パターンを直接取得可能。ただし価格データ・口コミデータは含まれない。Inside Airbnbの補完データとして極めて有用 |

#### 2.6.2 e-Stat（政府統計の総合窓口）

| 項目 | 内容 |
|------|------|
| **URL** | https://www.e-stat.go.jp/ |
| **ライセンス** | 政府統計（出典明記で二次利用可） |
| **宿泊関連** | 宿泊旅行統計調査のデータベース版もe-Stat経由で検索可能。API提供あり |
| **その他利用可能データ** | 消費者物価指数（宿泊料含む）、旅行・観光消費動向調査、共通基準による観光入込客統計 |
| **API** | REST API提供 — プログラマティックなデータ取得が可能 |
| **活用可能性評価** | ★★★☆☆ — 宿泊旅行統計調査のAPI経由取得、CPI（宿泊料）のトレンドデータ取得に有用 |

#### 2.6.3 訪日外国人消費動向調査・出入国者数データ（観光庁・JNTO）

| 項目 | 内容 |
|------|------|
| **URL (消費動向)** | https://www.mlit.go.jp/kankocho/siryou/toukei/syouhityousa.html |
| **URL (出入国)** | https://www.mlit.go.jp/kankocho/siryou/toukei/in_out.html |
| **JNTO統計** | https://www.jnto.go.jp/statistics/ |
| **変数** | 訪日外国人旅行者数（月次・国籍別）、旅行消費額（宿泊費含む）、宿泊施設タイプ別利用率 |
| **期間** | 月次・四半期（2003年〜） |
| **活用可能性評価** | ★★★☆☆ — インバウンド需要の外部変数として有用。地方施設への訪日客需要トレンドの把握に |

---

### 2.7　ホテル・宿泊ドメインにおけるオープンデータの制約

Zhu, Xiao, Yu, Liu, Chen & Cai (2024, KDD, cited 6) "Dynamic Hotel Pricing at Online Travel Platforms" において以下の記述がある:

> "As there is no other public dataset for hotel pricing"（ホテル価格設定の公開データセットは他に存在しない）

この記述は、宿泊業界における公開データの希少性を端的に示している。STR (Smith Travel Research) のデータは業界標準だが **非公開（商用ライセンス）** であり、研究利用にも契約が必要である。

Ampountolas & Legg (2021, IJCHM, cited 72) も「data is limited to a data set provided by a major chain hotel」と記述しており、ホテル実績データの公開利用が制限されている実態を示している。

---

### 2.8　全データセット比較総括表

#### 表A: 宿泊ドメインの全オープンデータセット — 機能別比較

| # | データセット | URL | ライセンス | サイズ | DL数 | 価格 | レビューテキスト | レビュースコア | 時系列 | 日本 | 地方 |
|---|------------|-----|----------|-------|-----|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Inside Airbnb** | insideairbnb.com/get-the-data/ | CC BY 4.0 | 都市依存 | — | ○日次 | ○全文 | ○7次元 | ○四半期+calendar | ○東京 | ○ |
| 2 | Tokyo Airbnb 2023 (Kaggle) | kaggle.com/.../tokyo-airbnb-open-data-2023 | CC0 | 400MB | 511 | ○ | ○ | ○7次元 | △(2021固定) | ○東京 | × |
| 3 | Airbnb 10 Cities (Kaggle) | kaggle.com/.../airbnb-listings-reviews | CC0 | 414MB | 10.1K | ○ | ○ | ○ | ○月次更新 | × | × |
| 4 | Seattle Airbnb (Kaggle公式) | kaggle.com/datasets/airbnb/seattle | CC0 | 90MB | 51.6K | ○日次 | ○全文 | ○7次元 | △(静的) | × | × |
| 5 | U.S. Airbnb (Kaggle) | kaggle.com/.../us-airbnb-open-data | CC0 | 75MB | 15.1K | ○ | × | × | △(年次) | × | × |
| 6 | EU Price Determinants (Zenodo) | zenodo.org/records/4446043 | CC BY 4.0 | 10.8MB | 14K | ○EUR | × | △2項目 | × | × | × |
| 7 | Hotel Booking Demand | kaggle.com/.../hotel-booking-demand | CC BY 4.0 | 16.9MB | **211K** | ○ADR | × | × | ○2年 | × | △1件 |
| 8 | 515K Hotel Reviews | kaggle.com/.../515k-hotel-reviews-data-in-europe | CC0 | 238MB | 48.1K | × | ○pos/neg分離 | ○ | △日付のみ | × | × |
| 9 | Booking.com Reviews | kaggle.com/.../booking-com-hotel-reviews | Other | 49MB | — | × | ○全文 | ○avg | △日付のみ | × | × |
| 10 | TripAdvisor Reviews | kaggle.com/.../trip-advisor-hotel-reviews | CC BY-NC 4.0 | 15MB | 45.9K | × | ○ | ○1–5 | × | × | × |
| 11 | TBO Hotels | kaggle.com/.../tbo-hotels-dataset | MIT | 2.4GB | — | × | × | △星のみ | × | × | × |
| 12 | Eco-hotel (UCI) | archive.ics.uci.edu/dataset/398 | CC BY 4.0 | 111KB | — | × | ○ | × | × | × | × |
| 13 | Travel Review Ratings (UCI) | archive.ics.uci.edu/dataset/485 | CC BY 4.0 | 622KB | — | × | × | ○24cat | × | × | × |
| 14 | **宿泊旅行統計調査** | mlit.go.jp/kankocho/... | 政府統計 | Excel | — | × | × | × | ○月次2007〜 | **◎47県** | **◎130区分** |
| 15 | STR | str.com | **商用(非公開)** | — | — | ○ | × | × | ○ | 不明 | 不明 |

**凡例**: ○=あり, △=限定的, ×=なし, ◎=特に充実

#### 表B: 研究目的別の推奨データセット組み合わせ

| 研究目的 | 推奨データセット | 理由 |
|---------|----------------|------|
| **ABSA → 価格予測 (本研究の主目的)** | ① Inside Airbnb (東京) + ② 515K Hotel Reviews (ABSA訓練用) | 東京の日次価格+レビュー全文+7次元スコア + 515Kのpos/neg分離テキストでABSAモデル訓練 |
| **日本の地方需要パターン分析** | ③ 宿泊旅行統計調査 (長野県月次稼働率) | 47都道府県・130区分の月次需要変動。Inside Airbnbの外部説明変数として |
| **ヘドニック価格モデルの再現** | ④ EU Price Determinants (Zenodo) | 空間回帰モデル (SAR, GWR) のコード付き再現可能データ |
| **需要予測・キャンセル予測** | ⑤ Hotel Booking Demand | 32変数、211K DLの信頼性、ADR季節変動 |
| **インバウンド需要の外部変数** | ⑥ 訪日外国人消費動向調査 + JNTO統計 | 月次の訪日客数→地方宿泊需要の間接推定 |

#### 表C: ボラティリティ特性の詳細比較

| データセット | 価格変動の粒度 | 変動要因 | 変動の大きさ (参考) |
|------------|-------------|---------|-----------------|
| Inside Airbnb calendar | 日次 | 季節, 週末/平日, イベント, 需要 | Mundiya (2025): seasonal/demand-driven volatility |
| Hotel Booking Demand ADR | 日次 (予約単位) | 季節, リードタイム, 客室タイプ, キャンセル | リゾート: 夏季ADR>冬季ADRの顕著な差 |
| NYC TLC | 分単位 | 時間帯, 天候, イベント, 混雑 | サージ価格: 基本運賃の1.5〜8倍 |
| ERCOT電力 | 5分 | 需給バランス, 気温, 再エネ出力 | $0〜$5,000+/MWh (2021年スパイク: $9,000) |
| JEPX電力 | 30分 | 需給バランス, 気温 | ¥5〜¥100+/kWh |
| 宿泊旅行統計 | 月次 | 季節, 連休, インバウンド | 稼働率: 30%台〜80%台の季節変動 |

---

### 2.9　第2部のまとめ — 活用戦略

**事実1**: 宿泊ドメインで**口コミ全文テキスト + 日次価格 + 時系列 + 多次元レビュースコア**のすべてを満たすオープンデータは **Inside Airbnb のみ**である。

**事実2**: Inside Airbnbには**東京データ**が存在し、calendar.csv.gzによる日次価格変動とreviews.csv.gzによるレビュー全文テキストが取得可能である。

**事実3**: 515K Hotel Reviews (Kaggle) は**ポジティブ/ネガティブが分離された515,000件のレビューテキスト**を提供しており、ABSAモデルの訓練データとして最適である。

**事実4**: 日本の地方宿泊需要パターンは**宿泊旅行統計調査**（観光庁）から47都道府県×月次で取得可能であり、2007年から現在まで継続している。

**事実5**: STRを含むホテル業界の実績データは非公開であり、Zhu et al. (2024, KDD) も "As there is no other public dataset for hotel pricing" と明記している。

---

## 参考文献一覧

1. Agušaj, B., Bazdan, V., & Lujak, Đ. (2017). The relationship between online rating, hotel star category and room pricing power. *Ekonomska misao i praksa*, cited 46.
2. Almeida, C., Teixeira, S., Franco, M., & Silva, M. (2025). How Do Reviews Impact Airbnb's Prices? A Hedonic Approach. *Tourism & Hospitality*.
3. Ampountolas, A., & Legg, M. P. (2021). A segmented machine learning modeling approach of social media for predicting occupancy. *IJCHM*, 33(6), 2001. Cited 72.
4. Anderson, C. (2012). The impact of social media on lodging performance. *Cornell Hospitality Report*, 12(15). Cited 609.
5. Angelini, G., Costa, M., & Guizzardi, A. (2025). Complex data in tourism analysis: A stochastic approach to price competition. *Big Data Research*. Cited 4.
6. Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief*, 22, 41–49. Cited 123.
7. Castro, C., & Ferreira, F. A. (2018). Online hotel ratings and its influence on hotel room rates. *Tourism Economics*. Cited 70.
8. Degife, G. W., & Lin, C.-C. (2024). A Multi-Aspect Informed GRU for Fare Prediction. *Applied Sciences*. Cited 10.
9. Di Persio, L., & Lalmi, O. (2024). Airbnb pricing with NLP features. *Journal of Risk and Financial Management*. Cited 8.
10. Ghosh, I., Jana, R. K., & Abedin, M. Z. (2023). An ensemble machine learning framework for Airbnb rental price modeling. *IJCHM*, 35(10), 3592. Cited 53.
11. Gibbs, C., Guttentag, D., Gretzel, U., Morton, J., & Goodwill, A. (2018). Pricing in the sharing economy: A hedonic pricing model applied to Airbnb listings. *Journal of Travel & Tourism Marketing*, 35(1), 46–56.
12. Gordan, M., Florian, V., Gaman, G., & Rus, D. (2024). Hedonic Pricing Models in Rural Tourism: A Hybrid LASSO-OLS and GWR Approach. *Agriculture*. Cited 10.
13. Jiang, Y., et al. (2024). Asymmetric effects of reviews on Airbnb pricing. (Cited in Almeida et al. 2025).
14. Katz, H. (2026). Coupled Supply and Demand Forecasting in Platform Accommodation Markets. *arXiv:2603.00422*.
15. Katz, H., Savage, E., & Coles, P. (2025). Lead times in flux: Analyzing Airbnb booking dynamics during global upheavals (2018–2022). *Annals of Tourism Research Empirical Insights*. Cited 8.
16. Kim, W. G., Lim, H., & Brymer, R. A. (2015). The effectiveness of managing social media on hotel performance. *IJHM*, 44, 165–171. Cited 658.
17. Lin, P., & Yang, Y. (2023). Review attributes and location effects on Airbnb pricing. (Cited in Almeida et al. 2025; 26 US regions).
18. Nieto-Garcia, M., Resce, G., Ishizaka, A., Occhiocupo, N., & Viglia, G. (2019). The dimensions of hotel customer ratings that boost RevPAR. *IJHM*, 77, 583–592. Cited 82.
19. Noone, B. M., & McGuire, K. A. (2013). Pricing in a social world: The influence of non-price information on hotel choice. *Journal of Revenue and Pricing Management*, 12(5). Cited 109.
20. Öğüt, H., & Onur Taş, B. K. (2012). The influence of internet customer reviews on the online sales and prices in hotel industry. *The Service Industries Journal*, 32(2), 197–214. Cited 624.
21. Santos, R. (2016). Hedonic pricing applied to hostels worldwide. (Cited in Almeida et al. 2025; 8,000 hostels globally).
22. Torres, E. N., Singh, D., & Robertson-Ring, A. (2015). Consumer reviews and the creation of booking transaction value. *IJHM*, 50, 73–83. Cited 228.
23. Ye, Q., Law, R., & Gu, B. (2009). The impact of online user reviews on hotel room sales. *IJHM*, 28(1), 180–182. Cited 2,146.
24. Ye, Q., Law, R., Gu, B., & Chen, W. (2011). The influence of user-generated content on traveler behavior. *Computers in Human Behavior*, 27(2), 634–639. Cited 2,002.
25. Zhu, F., Xiao, W., Yu, Y., Liu, Z., Chen, Z., & Cai, W. (2024). Dynamic Hotel Pricing at Online Travel Platforms. *KDD 2024*. Cited 6.
26. Zhu, Z. (2023). The Effects of Online Review Ratings: A Case Study of the Hotel Industry. Doctoral dissertation, Boston College.
27. Gyódi, K., & Nawaro, Ł. (2021). Determinants of Airbnb prices in European cities: A spatial econometrics approach. *Tourism Management*, 86, 104319. DOI: 10.1016/j.tourman.2021.104319. [Zenodo: 10.5281/zenodo.4446043]
28. Costa, R. (2025). Airbnb price prediction using machine learning. InsideAirbnb, R²=49.08%.
29. Mundiya, S. (2025). Forecasting Short-Term Rental Prices. Kaggle dataset, seasonal/demand-driven volatility.
30. Muhammad, A. (2025). Dynamic pricing for ride-on-demand. Uber Fares Dataset on Kaggle.
31. Alam, M. H., Ryu, W.-J., & Lee, S. (2016). Joint multi-grain topic sentiment: Modeling semantic aspects for online reviews. *Information Sciences*, 339, 206–223. DOI: 10.5281/zenodo.1219899.
32. Calheiros, A. C., Moro, S., & Rita, P. (2017). Sentiment Classification of Consumer-Generated Online Reviews Using Topic Modeling. *Journal of Hospitality Marketing & Management*, 26(7). UCI ML Repository DOI: 10.24432/C5M30H.
33. Renjith, S. (2018). Evaluation of Partitioning Clustering Algorithms for Processing Social Media Data in Tourism Domain. *IEEE RAICS*. UCI ML Repository DOI: 10.24432/C5C31Q.
34. 観光庁 (2007–2026). 宿泊旅行統計調査. 国土交通省. https://www.mlit.go.jp/kankocho/siryou/toukei/shukuhakutoukei.html
