# オープンデータセット調査：宿泊施設・観光関連

> 調査日: 2026年5月11日  
> 調査目的: 宿泊施設のレビュー・価格・需要データ、および観光・スキー施設関連のオープンデータセットを網羅的に調査し、各データセットのURL・カラム定義・ファイル形式・変数の型を記録する  
> 調査対象: Inside Airbnb / Booking.com / TripAdvisor / 国土交通省観光庁 / JNTO / スキーリゾートデータ

---

## 収録データセット一覧

| ID  | データセット名 | 提供者 | 形式 | ライセンス |
|-----|----------------|--------|------|------------|
| D1 | Inside Airbnb | Inside Airbnb (Murray Cox) | CSV/GeoJSON | CC0 / CC BY 4.0 |
| D2 | 515K Hotel Reviews Data in Europe | Kaggle (Jiashen Liu) / Booking.com | CSV | CC0 |
| D3 | Hotel Booking Demand | Kaggle (Jesse Mostipak) / Antonio et al. | CSV | CC BY 4.0 |
| D4 | Trip Advisor Hotel Reviews | Kaggle (Larxel) / Alam et al. 2016 | CSV | CC BY-NC 4.0 |
| D5 | 宿泊旅行統計調査 | 国土交通省観光庁 | Excel | 政府統計（利用自由） |
| D6 | 訪日外客統計 | JNTO（日本政府観光局） | Excel/PDF | 利用自由（出典記載要） |
| D7 | Ski Resorts and Snow Coverage | Kaggle (Ulrik Thyge Pedersen) | CSV | CC BY 4.0 |

---

## D1. Inside Airbnb

### ■ 参照情報

- **データセット名**: Inside Airbnb
- **提供者**: Murray Cox / Inside Airbnb Project
- **URL（ダウンロード）**: https://insideairbnb.com/get-the-data/
- **データ辞書（Data Dictionary）**: https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing
- **アクセス日**: 2026年5月11日（ダウンロードページ確認済）
- **ライセンス**:  
  - データ: [Creative Commons CC0 1.0（パブリックドメイン）](http://creativecommons.org/publicdomain/zero/1.0/)  
  - サイト全般: [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/)

---

### ■ 概要

- **目的・背景**: Airbnbが居住用不動産の住宅供給に与える影響について、地域コミュニティへの情報提供と政策議論を目的として公開されたミッション駆動型プロジェクト。Airbnbの公開ウェブサイトをスクレイピングして収集した非営利目的のデータ。
- **ドメイン**: 民泊・短期賃貸（Airbnb）
- **地理的範囲**: 世界100都市以上（Tokyo, New York, Paris, London, Barcelonaなど）。日本ではTokyo（東京）のデータが含まれる（最終更新: 2025年9月29日）
- **時間範囲**: 各都市のデータは過去1年分（四半期ごと）のスナップショット。過去データはアーカイブとして保管。Historical data available (2015年頃〜現在)
- **更新頻度**: 概ね四半期ごと（都市によって異なる）

---

### ■ データ構造

各都市ごとに以下のファイルセットが提供される:

| ファイル名 | 内容 | 形式 |
|-----------|------|------|
| `listings.csv.gz` | リスティング詳細データ（全カラム） | CSV（gzip圧縮） |
| `calendar.csv.gz` | カレンダー（365日分の空き状況・価格） | CSV（gzip圧縮） |
| `reviews.csv.gz` | レビュー詳細データ（コメント全文含む） | CSV（gzip圧縮） |
| `listings.csv` | リスティングサマリー（可視化用の主要カラムのみ） | CSV |
| `reviews.csv` | レビューサマリー（日付・listing ID） | CSV |
| `neighbourhoods.csv` | 地区名リスト（地理フィルター用） | CSV |
| `neighbourhoods.geojson` | 地区境界の地理データ | GeoJSON |

- **レコード数（参考）**: 都市規模による。例）ニューヨーク 約40,000件（listings）、東京 約10,000件（listings）
- **主要ファイルサイズ（参考）**: `listings.csv.gz` 数MB〜数十MB（都市規模依存）

---

### ■ カラム詳細

#### listings.csv（詳細版）— 主要カラム

> Data Dictionary（Googleスプレッドシート）に全カラムの公式定義あり。以下は主要カラム抜粋。カラム名・型・説明は公開Data Dictionaryに基づく。

| カラム名 | 型 | 説明 |
|----------|----|------|
| `id` | integer | リスティングのAirbnb ID |
| `name` | string | リスティング名（タイトル） |
| `description` | string | リスティングの説明文（テキスト） |
| `neighborhood_overview` | string | 近隣エリアの説明文 |
| `host_id` | integer | ホストのAirbnb ID |
| `host_name` | string | ホスト名 |
| `host_since` | date | ホスト登録日 |
| `host_response_time` | string | 返信時間（within an hour / within a few hoursなど） |
| `host_response_rate` | string | 返信率（パーセンテージ形式） |
| `host_acceptance_rate` | string | 受諾率（パーセンテージ形式） |
| `host_is_superhost` | boolean | スーパーホスト認定の有無 |
| `host_listings_count` | integer | ホストのリスティング数 |
| `host_total_listings_count` | integer | ホストの総リスティング数（全種別） |
| `neighbourhood_cleansed` | string | 正規化済み地区名 |
| `latitude` | float | 緯度（Airbnbにより0〜150m程度の誤差あり） |
| `longitude` | float | 経度（同上） |
| `property_type` | string | 物件タイプ（Entire rental unit, Private room in houseなど） |
| `room_type` | string | 部屋タイプ（Entire home/apt \| Private room \| Shared room \| Hotel room） |
| `accommodates` | integer | 最大収容人数 |
| `bathrooms_text` | string | バスルーム数（"1 bath"などテキスト形式） |
| `bedrooms` | integer | 寝室数 |
| `beds` | integer | ベッド数 |
| `amenities` | string | アメニティリスト（JSON配列形式） |
| `price` | string | 1泊あたりの宿泊料金（"$100.00"形式） |
| `minimum_nights` | integer | 最低宿泊日数 |
| `maximum_nights` | integer | 最大宿泊日数 |
| `has_availability` | boolean | 空き有無 |
| `availability_30` | integer | 今後30日間の空き日数 |
| `availability_60` | integer | 今後60日間の空き日数 |
| `availability_90` | integer | 今後90日間の空き日数 |
| `availability_365` | integer | 今後365日間の空き日数 |
| `number_of_reviews` | integer | 総レビュー数 |
| `number_of_reviews_ltm` | integer | 過去12ヶ月のレビュー数 |
| `first_review` | date | 最初のレビュー日 |
| `last_review` | date | 最終レビュー日 |
| `review_scores_rating` | float | 総合評価スコア（1〜5、またはNaN） |
| `review_scores_accuracy` | float | 正確さのスコア |
| `review_scores_cleanliness` | float | 清潔さのスコア |
| `review_scores_checkin` | float | チェックインのスコア |
| `review_scores_communication` | float | コミュニケーションのスコア |
| `review_scores_location` | float | ロケーションのスコア |
| `review_scores_value` | float | コスパのスコア |
| `instant_bookable` | boolean | 即時予約可能か否か |
| `calculated_host_listings_count` | integer | 計算済みホストのリスティング数 |
| `reviews_per_month` | float | 月あたりレビュー数 |

#### calendar.csv（詳細版）

| カラム名 | 型 | 説明 |
|----------|----|------|
| `listing_id` | integer | リスティングID（listings.csv の id と対応） |
| `date` | date | 日付（YYYY-MM-DD形式） |
| `available` | boolean | その日の空き状況（t = 空き、f = 予約済/ブロック） |
| `price` | string | その日の宿泊料金（"$100.00"形式） |
| `adjusted_price` | string | 週末・最低宿泊数調整後の価格（"$100.00"形式） |
| `minimum_nights` | integer | 当日から適用される最低宿泊日数 |
| `maximum_nights` | integer | 当日から適用される最大宿泊日数 |

#### reviews.csv（詳細版）

| カラム名 | 型 | 説明 |
|----------|----|------|
| `listing_id` | integer | リスティングID |
| `id` | integer | レビューID |
| `date` | date | レビュー投稿日 |
| `reviewer_id` | integer | レビュアーのAirbnb ID |
| `reviewer_name` | string | レビュアー名 |
| `comments` | string | レビュー本文（自然言語テキスト） |

#### listings.csv（サマリー版 — 可視化用）

| カラム名 | 型 | 説明 |
|----------|----|------|
| `id` | integer | リスティングID |
| `name` | string | リスティング名 |
| `host_id` | integer | ホストID |
| `host_name` | string | ホスト名 |
| `neighbourhood_group` | string | 地区グループ（一部都市のみ存在） |
| `neighbourhood` | string | 地区名 |
| `latitude` | float | 緯度 |
| `longitude` | float | 経度 |
| `room_type` | string | 部屋タイプ |
| `price` | integer | 1泊料金（数値のみ） |
| `minimum_nights` | integer | 最低宿泊日数 |
| `number_of_reviews` | integer | 総レビュー数 |
| `last_review` | date | 最終レビュー日 |
| `reviews_per_month` | float | 月あたりレビュー数 |
| `calculated_host_listings_count` | integer | 計算済みホストのリスティング数 |
| `availability_365` | integer | 年間空き日数 |
| `number_of_reviews_ltm` | integer | 過去12ヶ月のレビュー数 |
| `license` | string | 物件の許可番号（都市の規制による） |

---

### ■ 用途・活用例

- Airbnb価格の決定要因分析（属性・レビュースコア・立地）
- 感情分析（レビューテキスト）と価格の相関研究
- 短期賃貸が住宅市場に与える影響の定量分析
- 需要予測・稼働率モデリング（calendar.csvの空き状況データ活用）

---

### ■ 制約・利用条件

- 位置情報はAirbnbによって0〜150m程度匿名化されている（同一建物の複数リスティングが散在して見える）
- カレンダーデータは「予約済み」と「ホストによるブロック」を区別しないため、稼働率計算には推定が必要
- ホストが最低宿泊数を変更した場合、過去のレビューデータと整合しないことがある
- 提供データはスナップショット（特定時点のデータ）であり、削除済みリスティングは含まれない
- 日本（Tokyo）データは利用できるが、日本語レビュー比率が高い（英語NLP処理時に注意）
- Airbnbの利用規約上、他者のデータ収集に関する議論があるため、利用目的を確認すること

---

## D2. 515K Hotel Reviews Data in Europe

### ■ 参照情報

- **データセット名**: 515K Hotel Reviews Data in Europe
- **提供者**: Jiashen Liu（Kaggle）/ データ原典: Booking.com（パブリック情報）
- **URL**: https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe
- **アクセス日**: 2026年5月11日（ページ確認済）
- **ファイル**: `Hotel_Reviews.csv`（238.15 MB）
- **ライセンス**: [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)

---

### ■ 概要

- **目的**: ヨーロッパの高級ホテルのBooking.comレビューを用いたNLP・感情分析・推薦システム研究の基盤データ
- **ドメイン**: ホテル（高級ホテル、ヨーロッパ）
- **地理的範囲**: ヨーロッパ主要都市（イギリス、フランス、スペイン、イタリア、オランダ、オーストリアなど）
- **対象**: 1,493施設のホテル
- **レコード数**: 515,000件のレビュー
- **収集元**: Booking.com（パブリック情報のスクレイピング）
- **時間範囲**: 記載なし（データ収集時点によるスナップショット）
- **前処理**: Unicodeと句読点の除去、テキストの小文字化が施されている

---

### ■ データ構造

- **ファイル数**: 1ファイル（`Hotel_Reviews.csv`）
- **カラム数**: 17カラム
- **ファイルサイズ**: 238.15 MB

---

### ■ カラム詳細

| カラム名 | 型 | 説明 |
|----------|----|------|
| `Hotel_Address` | string | ホテルの住所 |
| `Review_Date` | date | レビュー投稿日 |
| `Average_Score` | float | ホテルの平均スコア（過去1年の最新コメントを基に算出） |
| `Hotel_Name` | string | ホテル名 |
| `Reviewer_Nationality` | string | レビュアーの国籍 |
| `Negative_Review` | string | ネガティブレビュー本文（レビューなしの場合は 'No Negative'） |
| `Review_Total_Negative_Word_Counts` | integer | ネガティブレビューの単語数 |
| `Positive_Review` | string | ポジティブレビュー本文（レビューなしの場合は 'No Positive'） |
| `Review_Total_Positive_Word_Counts` | integer | ポジティブレビューの単語数 |
| `Reviewer_Score` | float | レビュアーがつけたスコア（自身の体験に基づく） |
| `Total_Number_of_Reviews_Reviewer_Has_Given` | integer | そのレビュアーがこれまでに投稿した総レビュー数 |
| `Total_Number_of_Reviews` | integer | そのホテルの有効総レビュー数 |
| `Tags` | string | レビュアーがホテルにつけたタグ（カンマ区切りリスト形式） |
| `days_since_review` | integer | レビュー日からデータ収集日（スクレイプ日）までの日数 |
| `Additional_Number_of_Scoring` | integer | レビュー本文なしでスコアのみをつけたゲスト数 |
| `lat` | float | ホテルの緯度 |
| `lng` | float | ホテルの経度 |

---

### ■ 用途・活用例

- ホテルの属性（ロケーション・清潔さ・サービスなど）ごとの感情分析（ABSA）
- レビュースコアと価格の関係分析
- レビュアーの国籍と評価スコアの相関分析
- ホテル推薦システムの構築
- Reviewer_Score を目的変数とした回帰・分類モデルの構築

---

### ■ 制約・利用条件

- テキストデータはUnicodeと句読点の除去・小文字化処理済み（preprocessing済み）
- Average_Score はBooking.com独自の算出方法によるため、実際のレビュースコア平均とは異なる場合がある
- 対象ホテルは「高級ホテル」に限定されており、低価格帯やブティックホテルは含まない
- ポジティブ・ネガティブの2種類のレビューが1行に含まれる構造（Booking.com特有のフォーマット）
- 収集元のBooking.comの著作権・利用規約に注意

---

## D3. Hotel Booking Demand

### ■ 参照情報

- **データセット名**: Hotel Booking Demand
- **提供者**: Jesse Mostipak（Kaggle）
- **原論文**: Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief*, 22, 41–49. https://doi.org/10.1016/j.dib.2018.11.126
- **URL（Kaggle）**: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
- **URL（原論文）**: https://www.sciencedirect.com/science/article/pii/S2352340918315191
- **TidyTuesday README（列定義出典）**: https://github.com/rfordatascience/tidytuesday/blob/master/data/2020/2020-02-11/readme.md
- **アクセス日**: 2026年5月11日（KaggleページおよびTidyTuesdayのREADME確認済）
- **ファイル**: `hotel_bookings.csv`（16.86 MB）
- **ライセンス**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

### ■ 概要

- **目的**: ホテルの予約需要データを用いたキャンセル予測・需要予測・EDA研究の基盤データセット
- **ドメイン**: ホテル予約・需要管理（Revenue Management）
- **地理的範囲**: ポルトガル（H1: リゾートホテル、H2: シティーホテル、具体的な施設名は匿名化）
- **対象ホテル数**: 2施設（Resort Hotel 1軒、City Hotel 1軒）
- **時間範囲**: 2015年7月〜2017年8月
- **レコード数**: 119,390件
- **カラム数**: 32カラム
- **個人情報**: 個人を特定できる情報（PII）は全て除去済み

---

### ■ データ構造

- **ファイル数**: 1ファイル（`hotel_bookings.csv`）
- **カラム数**: 32カラム
- **ファイルサイズ**: 16.86 MB

---

### ■ カラム詳細

> 全カラムの定義はTidyTuesdayのREADME（https://github.com/rfordatascience/tidytuesday/blob/master/data/2020/2020-02-11/readme.md）に一次情報として記載されている。

| カラム名 | 型 | 説明 |
|----------|----|------|
| `hotel` | character | ホテル種別 (Resort Hotel または City Hotel) |
| `is_canceled` | double | キャンセル有無（1=キャンセル、0=完了） |
| `lead_time` | double | 予約登録日から到着日までの日数 |
| `arrival_date_year` | double | 到着年 |
| `arrival_date_month` | character | 到着月 |
| `arrival_date_week_number` | double | 到着週番号（年内通算） |
| `arrival_date_day_of_month` | double | 到着日（日） |
| `stays_in_weekend_nights` | double | 宿泊した（または予約した）週末泊数（土・日） |
| `stays_in_week_nights` | double | 宿泊した（または予約した）平日泊数（月〜金） |
| `adults` | double | 大人の人数 |
| `children` | double | 子供の人数 |
| `babies` | double | 乳幼児の人数 |
| `meal` | character | 食事プラン（Undefined/SC:なし、BB:朝食のみ、HB:朝食+夕食、FB:3食） |
| `country` | character | 顧客の出身国（ISO 3155-3:2013形式） |
| `market_segment` | character | 市場セグメント（TA=旅行代理店、TO=ツアーオペレーター等） |
| `distribution_channel` | character | 予約流通チャネル（TA/TO/Direct/Corporate等） |
| `is_repeated_guest` | double | リピート客か否か（1=リピーター、0=初回） |
| `previous_cancellations` | double | 当該顧客の過去キャンセル件数 |
| `previous_bookings_not_canceled` | double | 当該顧客の過去非キャンセル予約件数 |
| `reserved_room_type` | character | 予約した部屋タイプのコード（匿名化） |
| `assigned_room_type` | character | 実際に割り当てられた部屋タイプのコード（匿名化） |
| `booking_changes` | double | 予約登録からチェックインorキャンセルまでの変更回数 |
| `deposit_type` | character | デポジット種別（No Deposit / Non Refund / Refundable） |
| `agent` | character | 予約した旅行代理店のID（匿名化） |
| `company` | character | 支払い担当企業・団体のID（匿名化） |
| `days_in_waiting_list` | double | 予約確定前のウェイティングリスト滞在日数 |
| `customer_type` | character | 顧客タイプ（Contract / Group / Transient / Transient-party） |
| `adr` | double | 平均日額料金（Average Daily Rate）：全宿泊取引額÷総宿泊泊数 |
| `required_car_parking_spaces` | double | 顧客が要求した駐車スペース数 |
| `total_of_special_requests` | double | 特別リクエスト数（ツインベッド・高層階等） |
| `reservation_status` | character | 最終予約ステータス（Canceled / Check-Out / No-Show） |
| `reservation_status_date` | double | 最終ステータスが設定された日付 |

---

### ■ 用途・活用例

- 予約キャンセル予測モデル（`is_canceled`を目的変数）
- 需要予測・価格最適化（`adr`と`lead_time`・`market_segment`の関係分析）
- 収益管理（Revenue Management）アルゴリズムの研究
- 顧客タイプ別行動分析（`customer_type`・`market_segment`）

---

### ■ 制約・利用条件

- 地理的に2施設（ポルトガル）のみへの限定により汎化性に課題
- ホテル名・国名・代理店名・部屋タイプはすべて匿名化済み
- `adr`（平均日額料金）が0またはマイナスのデータが一部存在（外れ値処理要）
- 2015〜2017年のデータであり、パンデミック後の需要パターンを反映しない
- `reservation_status_date`は数値（Excelシリアル日付）として格納されている場合がある

---

## D4. Trip Advisor Hotel Reviews

### ■ 参照情報

- **データセット名**: Trip Advisor Hotel Reviews
- **提供者**: Larxel（Kaggle）
- **原典論文**: Alam, M. H., Ryu, W.-J., Lee, S. (2016). Joint multi-grain topic sentiment: modeling semantic aspects for online reviews. *Information Sciences*, 339, 206–223. https://doi.org/10.5281/zenodo.1219899
- **URL（Kaggle）**: https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews
- **アクセス日**: 2026年5月11日（ページ確認済）
- **ファイル**: `tripadvisor_hotel_reviews.csv`（14.97 MB）
- **ライセンス**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

---

### ■ 概要

- **目的**: TripAdvisorのホテルレビューを対象としたNLP・感情分析・評価予測研究用データセット
- **ドメイン**: ホテルレビュー（多言語NLP・感情分析）
- **地理的範囲**: 記載なし（TripAdvisorからのクローリング）
- **レコード数**: 20,000件のレビュー
- **収集元**: TripAdvisor（公開データのクローリング）

---

### ■ データ構造

- **ファイル数**: 1ファイル（`tripadvisor_hotel_reviews.csv`）
- **カラム数**: 2カラム

---

### ■ カラム詳細

| カラム名 | 型 | 説明 |
|----------|----|------|
| `Review` | string | レビュー本文（自然言語テキスト） |
| `Rating` | integer | 評価スコア（1〜5の整数） |

---

### ■ 用途・活用例

- レビューテキストから評価スコアを予測する分類モデルの構築
- LDA・GSM等のトピックモデリング
- 感情分析（ポジティブ/ネガティブ分類）
- BERTなどの事前学習モデルのファインチューニング用データ

---

### ■ 制約・利用条件

- **カラム数がわずか2つ**（Review と Rating のみ）のため、ホテル名・立地・価格帯などのメタデータを持たない。価格分析・施設属性研究への単独利用は不向き
- ライセンスが **CC BY-NC 4.0**（非商用限定）のため商業利用不可
- ホテル名・地域などの識別子が存在しないため、他データとの結合が困難
- レビュー数は20,000件と比較的小規模
- 対象ホテル・地域の詳細は不明（記載なし）

---

## D5. 宿泊旅行統計調査

### ■ 参照情報

- **データセット名**: 宿泊旅行統計調査
- **提供者**: 国土交通省観光庁 観光戦略課観光統計調査室
- **URL（ダウンロードページ）**: https://www.mlit.go.jp/kankocho/siryou/toukei/shukuhakutoukei.html
- **アクセス日**: 2026年5月11日（ページ確認済。最終更新: 2026年4月30日）
- **ファイル形式**: Excel（.xlsx）、PDF（報告書）
- **ライセンス**: 政府統計（著作権は国土交通省観光庁。非営利・学術目的であれば原則利用自由、出典明記必要。詳細は[サイトポリシー](https://www.mlit.go.jp/kankocho/site-policy.html)参照）

---

### ■ 概要

- **目的**: わが国の宿泊旅行の実態（宿泊者数・施設数・稼働率など）を把握し、観光政策立案に資する基礎統計
- **ドメイン**: 日本国内の宿泊施設（ホテル・旅館・簡易宿所・会社団体の宿泊施設）
- **地理的範囲**: 日本全国（都道府県別・広域市町村（130区分）別集計あり）
- **時間範囲**: 2007年（平成19年）〜現在（月次）
- **更新頻度**: 月次発表（第1次速報: 翌月末頃、第2次速報: 翌々月末頃、確定値: 翌年後半）
- **調査対象**: 全国の宿泊施設（2010年より従業者数9人以下の小規模施設も対象）

---

### ■ データ構造

- **形式**: Excel(.xlsx) — スナップショット形式（月次・年次）
- **集計単位**: 都道府県 × 宿泊施設種別 × 月次（個票データは非公開）
- **主な提供ファイル**:

| ファイル種別 | 説明 | 例 |
|-------------|------|-----|
| 第1次速報（月次集計結果） | 翌月末公表の速報値（Excelのみ） | `2026年3月分集計結果.xlsx` |
| 第2次速報（月次集計結果＋推移表） | 翌々月末公表、報道発表資料（PDF）・推移表（Excel）あり | 2026年2月分など |
| 確定値（年次集計結果＋報告書） | 翌年中頃公表、2.5MB程度のExcelと7MB程度のPDF報告書 | `2024年1〜12月分年の確定値.xlsx` |
| 広域市町村（130区分）別参考表 | 年次確定値と組み合わせて公開 | `2024年広域市町村集計.xlsx` |

---

### ■ カラム詳細（集計表内の主要変数）

> 本データは**個票データではなく集計統計**（都道府県 × 施設種別 × 月次の集計値）として提供される。以下の変数は公開Excel集計表の内容に基づく。

| 変数名（日本語） | 変数名（英語相当） | 型 | 説明 |
|----------------|-------------------|-----|------|
| 調査年月 | survey_year_month | date（年月） | 統計の対象年月 |
| 都道府県 | prefecture | categorical | 集計対象の都道府県名（47都道府県） |
| 宿泊施設種別 | accommodation_type | categorical | ホテル / 旅館 / 簡易宿所 / 会社・団体の宿泊施設 |
| 施設数 | num_facilities | integer | 稼働施設数 |
| 客室数 | num_rooms | integer | 総客室数 |
| 延べ宿泊者数 | total_overnight_stays | integer | 月間延べ宿泊者数（個人×泊数） |
| 日本人延べ宿泊者数 | overnight_stays_japanese | integer | 日本人客の延べ宿泊者数 |
| 外国人延べ宿泊者数 | overnight_stays_foreign | integer | 外国人客の延べ宿泊者数 |
| 延べ宿泊者数（前年同月比） | yoy_overnight_stays | float（%） | 前年同月比（パーセント） |
| 客室稼働率 | room_occupancy_rate | float（%） | 月間平均客室稼働率 |
| 定員稼働率 | capacity_occupancy_rate | float（%） | 定員ベースの稼働率 |

- **補足**: 2026年1月調査分より、層化変数が「従業者数」から「**客室数**」に変更された（調査精度向上のため）
- **補足**: 集計単位が都道府県レベルであり、個別施設のデータは含まれない

---

### ■ 関連データ・参考リンク

- **旅行・観光消費動向調査**: https://www.mlit.go.jp/kankocho/tokei_hakusyo/shohidoko.html（旅行消費額の統計）
- **共通基準による観光入込客統計**: https://www.mlit.go.jp/kankocho/tokei_hakusyo/irikomikyaku.html（地域別観光入込客数）
- **政府統計の総合窓口（e-Stat）**: https://www.e-stat.go.jp/（各種政府統計の一元ダウンロード窓口）

---

### ■ 制約・利用条件

- **個票データは非公開**。分析単位は都道府県×施設種別の集計値であり、施設ごとの個別データは得られない
- 小規模施設（従業者数9人以下）は**2010年4月調査分より**調査対象に追加されたため、それ以前のデータと接続する際には注意が必要
- Excel形式で提供されるが、複数シートにわたる複雑なレイアウトであるため、機械的なデータ処理には前処理が必要
- 2024年（令和6年）集計分について一部正誤表が公表されており（千葉県・石川県・関東/北陸信越運輸局等）、確認要
- 外国人延べ宿泊者数は速報値段階では推計誤差を含む

---

## D6. 訪日外客統計

### ■ 参照情報

- **データセット名**: 訪日外客統計（月別・時系列）
- **提供者**: JNTO（日本政府観光局 / Japan National Tourism Organization）
- **URL（統計ページ）**: https://www.jnto.go.jp/statistics/data/visitors-statistics/
- **URL（ポータルサイト）**: https://statistics.jnto.go.jp/
- **URL（英語版グラフポータル）**: https://statistics.jnto.go.jp/en/graph/
- **アクセス日**: 2026年5月11日（ページ確認済）
- **ファイル形式**: Excel（.xlsx）、PDF
- **ライセンス**: JNTO著作権下（出典明記のうえ利用可。詳細はサイトポリシー参照）

---

### ■ 概要

- **目的**: 日本への訪日外客数の月別・国籍別・目的別時系列統計を提供し、観光政策・インバウンド研究の基礎データとなる
- **ドメイン**: インバウンド観光（観光・ビジネス・留学など目的を含む）
- **地理的範囲**: 日本全国（入国港別・都道府県別 overnight stays データあり）
- **時間範囲**: 2003年（月次データ）〜現在
- **更新頻度**: 月次（推計値: 翌月中旬、暫定値: 翌々月中旬）

---

### ■ データ構造（主要ファイル）

| ファイル種別 | 内容 | 形式 |
|-------------|------|------|
| 月次報告（推計値） | 当月訪日外客数の速報（PDF） | PDF |
| 月次推計値 統計表 | 直近2ヶ月の推計値（Excel） | Excel |
| 月次暫定値 | 詳細な国籍別内訳 | PDF |
| 時系列推移表（国籍/月別） | 2003年〜現在（年別・月別・国籍別） | Excel / PDF |
| 国籍/目的別訪日外客数 | 2004年〜2024年の目的別内訳 | PDF |

---

### ■ カラム詳細（時系列推移表）

> 時系列Excelファイル（"国籍/月別 訪日外客数（2003～2026年）"）の主要変数。

| 変数名（日本語） | 型 | 説明 |
|----------------|-----|------|
| 年月 | date（年月） | 統計対象の年月 |
| 総数 | integer | 訪日外客総数 |
| 東アジア（韓国・中国・香港・台湾など） | integer | 国籍別訪日外客数 |
| 東南アジア（タイ・シンガポール・マレーシアなど） | integer | 〃 |
| 北米（米国・カナダ） | integer | 〃 |
| ヨーロッパ（英・仏・独など） | integer | 〃 |
| 前年同月比 | float（%） | 前年同月比の変化率 |

> 用途別内訳（観光・商用・留学等）は別ファイル（「国籍/目的別 訪日外客数」）で提供。
> 都道府県別 overnight stays は MLIT/観光庁「宿泊旅行統計調査」との組み合わせで活用可。

---

### ■ 用途・活用例

- 観光地の需要予測・季節性分析（月次時系列）
- インバウンド市場の地域別動向分析
- COVID-19前後の需要変動の定量分析（2019年vs.2020〜2022年）
- 長野・北海道など特定地域への訪日客推移の研究基礎データ

---

### ■ 制約・利用条件

- 個人レベルのデータは含まれず、月次・国籍別の集計値のみ
- 推計値は正式確定前の暫定値であり、後に修正されることがある
- 都道府県別 overnight stays（宿泊者数）は本データではなく「宿泊旅行統計調査（D5）」を参照すること
- 施設ごとの価格・レビューデータは含まれない
- 日本語・英語のどちらのページでも同一データにアクセス可能だが、ダウンロードファイルは日本語表記

---

## D7. Ski Resorts and Snow Coverage

### ■ 参照情報

- **データセット名**: Ski Resorts and Snow Coverage（スキーリゾートと積雪データ）
- **提供者**: Ulrik Thyge Pedersen（Kaggle）
- **URL**: https://www.kaggle.com/datasets/ulrikthygepedersen/ski-resorts
- **アクセス日**: 2026年5月11日（ページ確認済）
- **ファイル**:  
  - `resorts.csv`（70.92 kB）  
  - `snow.csv`（別ファイル）
- **総カラム数**: 29カラム（2ファイル合計）
- **ライセンス**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

### ■ 概要

- **目的・概要**: 世界各地のスキーリゾートの位置情報・標高・積雪量・リフト数・コース数に加え、近隣施設情報（レストラン・ホテル・交通）、スキーパス料金を含む複合データセット
- **ドメイン**: スキーリゾート、ウィンタースポーツ観光
- **地理的範囲**: 世界（詳細な対象国・地域の記載はKaggleページに確認できず）
- **時間範囲**:  
  - `resorts.csv`: 静的（スキーリゾートの属性スナップショット）  
  - `snow.csv`: 冬季シーズンの積雪量時系列データ（詳細な年範囲は記載なし）

---

### ■ データ構造

- **ファイル数**: 2ファイル（`resorts.csv` + `snow.csv`）
- **総カラム数**: 29カラム
- `resorts.csv`: リゾート属性（位置・標高・コース情報・価格等）— 25カラム
- `snow.csv`: 積雪データの時系列 — 4カラム程度

---

### ■ カラム詳細（resorts.csv）

> ⚠️ 以下のカラム名はKaggleページのdataset description（英語記述）から取得した情報に基づく。ページ上では10 of 25 Columnsのプレビューのみ表示。全カラム名の確定にはデータ直接ダウンロードが必要。

| カラム名（推定） | 型 | 説明 |
|----------------|-----|------|
| `Resort` | string | スキーリゾート名 |
| `Country` | string | 所在国 |
| `Latitude` | float | 緯度 |
| `Longitude` | float | 経度 |
| `Highest_point` | integer | 最高地点（メートル） |
| `Lowest_point` | integer | 最低地点（スキーエリア）（メートル） |
| `Vertical_drop` | integer | 標高差（Highest - Lowest、メートル） |
| `Snow_cannons` | integer | 人工降雪機の数（記載なし可能性あり） |
| `Surface_lifts` | integer | サーフェスリフト数 |
| `Chair_lifts` | integer | チェアリフト数 |
| `Gondolas` | integer | ゴンドラ数 |
| `Total_slopes` | integer | 全コース数 |
| `Beginner_slopes` | integer | 初級コース数 |
| `Intermediate_slopes` | integer | 中級コース数 |
| `Advanced_slopes` | integer | 上級コース数 |
| `Season` | string | 営業シーズン（例: "December to April"） |
| `Price` | float | 1日スキーパスの料金（通貨単位は記載なし） |
| `Nightskiing` | boolean | ナイタースキーの有無 |
| `Snow_parks` | integer? | スノーパーク数（記載なし可能性あり） |

#### snow.csv（概要）

| カラム名（推定） | 型 | 説明 |
|----------------|-----|------|
| `Resort` | string | スキーリゾート名（resorts.csv と対応） |
| `Date` | date | 計測日 |
| `Snow_depth` | float | 積雪深（センチメートル） |
| `Snowfall` | float | 降雪量（センチメートル） |

---

### ■ 用途・活用例

- スキーリゾートの価格（スキーパス料金）と積雪量・標高差・リフト数の関係分析
- スキー観光需要の季節性モデリング
- ウィンタースポーツ観光地の比較・クラスタリング

---

### ■ 制約・利用条件

- データソース（スクレイピング元）が明記されていない
- カラム名・単位の一部がデータダウンロードなしでは確定できない（⚠️ 本文書の一部列名は推定）
- 日本のスキーリゾート（長野・北海道など）が含まれるかは確認できず
- 価格の通貨単位の記載が不明（要確認）
- 積雪時系列データの対象期間・更新状況が不明
- 宿泊施設との直接のリンクは存在しない（スキーリゾート近接ホテルの価格・レビューは別途取得要）

---

## 補足：日本のスキー施設・観光に関する国内オープンデータ

### 日本索道工業会（索道統計）

- **URL**: https://www.japan-ropeway.or.jp/
- **内容**: ロープウェイ・ゴンドラ・スキーリフト等の設置数・利用者数統計（年次）
- **状況**: ウェブページはアクセス可能だが、詳細なCSV/Excelのバルクダウンロードページは確認できず（⚠️ 本調査時点でバルクデータの公開は未確認）

### 観光庁「共通基準による観光入込客統計」

- **URL**: https://www.mlit.go.jp/kankocho/tokei_hakusyo/irikomikyaku.html
- **内容**: 都道府県・市町村単位の観光入込客数（スキー場等の個別観光地別データを含む都道府県もある）
- **形式**: Excel（年次） — 都道府県ごとに提供
- **備考**: 「スキー場」の入込客数が識別できる都道府県があり、長野県・北海道などの観光需要時系列分析に利用可能

### SnowJapan（スキー場積雪情報）

- **URL**: https://www.snowjapan.com/
- **内容**: 日本全国のスキー場の積雪深・降雪量・営業状況のリアルタイム・過去データ
- **状況**: 個別スキー場のデータページは公開されているが、**バルクダウンロード・CSVエクスポート機能は提供されていない**（スクレイピングによる取得のみ。利用規約の確認要）

### 気象庁 アメダス（地域気象観測データ）

- **URL**: https://www.jma.go.jp/jma/menu/menureport.html
- **内容**: 日本全国の地点別気温・降水量・積雪量等の時系列データ（1時間・1日値）
- **形式**: CSV（地点別ダウンロード）
- **備考**: スキーリゾート近接地点のアメダスデータと宿泊統計を組み合わせることで「積雪量と宿泊需要」の関係を分析できる可能性がある。長野（野沢温泉・白馬等）・北海道（ニセコ等）の地点データが利用可能

---

*本ドキュメントは一次情報（各データセット公式ページ・論文・READMEファイル）に基づいて作成。二次情報による推定・未確認箇所には ⚠️ マークを付与した。*
