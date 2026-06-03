# 地方宿泊施設における口コミ活用型価格決定支援エージェントの研究基盤：体系的文献調査

---

# 要約

本文献調査は、地方・中小宿泊施設における価格設定支援の研究を位置づけるために、以下の5つの問いに対して体系的に文献を整理したものである。(1) 地方・中小宿泊施設において既存のダイナミックプライシング（DP）やレベニューマネジメントシステム（RMS）が十分に導入・信頼されない理由、(2) 導入障壁の文献上の整理、(3) 既存研究・ソリューションによる対応、(4)「口コミを活用した価格決定支援エージェント」という研究方向の妥当性、(5) 有望な技術的・実務的設計。調査の結果、中小宿泊施設におけるRM導入の障壁は、技術的課題（ブラックボックス性、データ不足）、組織的課題（専門人材不足、コスト）、心理的課題（信頼不足、自動化への抵抗）の3層に分類されることが判明した。近年の研究では、説明可能AI（XAI）の導入（Mohammed & Denizci Guillet, 2025）やhuman-in-the-loop設計（Ivanov & Webster, 2024）が注目されているが、口コミ情報を価格「決定支援」に統合するシステムの研究は極めて少なく、特に地方宿泊施設の文脈では顕著な研究ギャップが存在する。

---

# 1. 問題設定

## 1.1 研究の背景

ダイナミックプライシング（DP）は、航空産業での導入（1980年代）を起点にホテル産業へ普及し、現在では大手ホテルチェーンのレベニューマネジメント（RM）において標準的手法となっている（Talluri & van Ryzin, 2004; Vives, Jacob, & Payeras, 2018）。RMSは、需要予測・価格最適化・在庫管理を統合するソフトウェアシステムであり、IDeaS、Duetto、Atomize等の商用プロダクトが市場を形成している。

しかし、これらのRMSの恩恵を享受しているのは主に大手チェーンホテルであり、中小・独立系・地方の宿泊施設においてはRMの導入率が著しく低い。Alrawadieh, Alrawadieh, & Cetin（2021）は、トルコ・イスタンブールのホテルを対象とした質的研究で、独立系ホテルにおけるRM導入の主要障壁として、コスト、専門人材不足、既存システムとの互換性を特定した。Sun, Schuckert, & Hon（2025）は、中国の中小独立系ホテルを対象に、RM導入のための組織構造上の課題を調査し、レベニューマネージャーの配置や役割定義の困難さを報告している。

## 1.2 本調査の焦点

本調査は、「ダイナミックプライシングそのものの導入」ではなく、「口コミ（オンラインレビュー）を活用した価格決定支援エージェント」という研究方向を位置づけることを目的とする。この方向性を採用する理由は以下の通りである。

1. 地方宿泊施設において、完全自動の価格決定は受け入れられにくい（Ivanov & Webster, 2024; Mohammed & Denizci Guillet, 2025a）。
2. 地方施設は大都市のホテルチェーンと比較してデータ量が限定的であり、従来の需要予測モデルの精度が低下する可能性がある（Munnaluri, 2022; Zaki, 2022）。
3. 口コミは、地方施設において宿泊意思決定に特に強い影響を与える情報源である（Abrate, Nicolau, & Viglia, 2019; Cıftcı, Berezına, & Cavusoglu, 2020）。
4. 「価格の自動決定」ではなく「価格決定の根拠提示」という設計思想が、現場の経験知との共存を可能にする。

---

# 2. 地方宿泊施設におけるダイナミックプライシング導入の市場課題

## 2.1 導入率の偏りと実態

RM研究の系譜的レビューによれば、RM技術は航空産業（1970年代末）からホテル産業（1990年代）へ移行し、大手チェーンでは広く普及している（Denizci Guillet & Mohammed, 2015; Vives, Jacob, & Payeras, 2018）。しかし、中小宿泊施設におけるRM導入は著しく遅れている。

Alrawadieh, Alrawadieh, & Cetin（2021）は、トルコの独立系ホテル28軒にインタビューを行い、(1) RMSの導入コストが年間数万ドル規模であるため中小施設には負担が大きい、(2) RM専門人材の採用が困難、(3) 既存のPMS（Property Management System）との互換性不足、という3つの主要障壁を特定した。被引用数215件（2026年時点）のこの研究は、中小ホテルのRM導入障壁に関する代表的文献である。

Sun, Schuckert, & Hon（2025）は、中国の中小独立系ホテルのRM導入における組織構造の課題を調査した。研究によれば、中小独立系ホテルでは(1) 専任レベニューマネージャーの配置が困難、(2) RM機能がフロントデスクやセールス部門の兼務として扱われ専門性が不足、(3) オーナー経営者の直感的意思決定がRM原則と衝突する、といった課題が存在する。

Lima Santos, Gomes, & Malheiros（2024）は、ポルトガルのホテル産業を対象にRM導入要因を調査し、COVID-19後の危機的状況においてRM導入は進んだものの、中小施設においては財務的制約と人材不足が依然として主要障壁であると報告している。

## 2.2 導入障壁の構造化

文献から導出される導入障壁を、**技術的課題**、**制度・組織的課題**、**心理的・受容性課題**の3層に構造化する。

### 2.2.1 技術的課題

**ブラックボックス性と説明可能性不足**

Mohammed & Denizci Guillet（2025b, Tourism Economics）は、27名のRM専門家へのインタビューを通じて、ホテルRMSのブラックボックス性が最大の課題であることを明らかにした。インタビュー参加者からの典型的発言として、「なぜシステムが特定の月にのみ宿泊料金を引き上げるのか知りたい」（P18）、「アルゴリズム全体は知りたくないが、結果と入力データの簡潔な説明が欲しい」（P12）がある。RMSプロバイダー側も「特定のRMSプロバイダーは、業務保護のために透明性を意図的に制限している」（P6）と認めている。

この不透明性は、RM担当者による「オーバーライド（システム推薦の上書き）」を引き起こす主要因である。Mohammed & Denizci Guillet（2025a, IJCHM）は、RMSユーザーがシステム推薦を上書きする際に、代表性ヒューリスティクスやアンカリングなどの認知バイアスに影響されることを実証した。Garcia, Tolvanen, & Wagner（2026, Management Science）は、ホテル価格設定における実データ分析から、ホテルマネージャーがアルゴリズム推薦に対して系統的な偏向（systematic bias）を持つことを示し、推薦からの乖離が収益損失に繋がるケースを定量化した。この論文は被引用数18件であり、人間とアルゴリズムの相互作用に関する重要な実証研究である。

**データ不足と需要変動の不安定性**

Munnaluri（2022）は、ホスピタリティ産業におけるデータスパーシティ（data scarcity）の下でのDP問題を研究し、小規模施設では(1) 予約データの蓄積量が限定的、(2) 季節変動が極端で安定した需要パターンの推定が困難、(3) 外部データ（競合価格、地域イベント）の取得が限定的であることを報告した。

Zaki（2022, IJCHM, 被引用数60件）は、COVID-19下のホテルRMを調査し、「制御可能な障壁」と「制御不可能な障壁」を区別した。データ不足は制御可能な障壁に分類されるが、その解決には技術投資が必要であり、中小施設には負担が大きい。

### 2.2.2 制度・組織的課題

**専門人材不足**

Sun et al.（2025）が指摘するように、中小独立系ホテルでは専任のRM担当者を配置する財務的余裕がない場合が多く、RM機能は他業務との兼任で担われる。このことは、RMSの高度な機能を十分に活用できないという二次的障壁を生む。

**システムコストとROI不明確性**

Alrawadieh et al.（2021）は、「コストは我々のホテルにとって重要な障壁であるが、チェーンホテルにとってはそうではない」というインタビュー結果を報告している。Mohammed & Denizci Guillet（2025b）も、XAI統合のコスト（技術アップグレード、継続的メンテナンス、スタッフ研修）が特に中小施設にとって大きな負担であることを指摘した。

**組織文化と変革抵抗**

Mohammed & Denizci Guillet（2025b）のインタビュー結果では、「ホテル業界は技術に関しては一般に遅れており、変化に対する十分な意欲がない」（P22）、「ホテルがXAIを採用するかどうかはその文化次第であり、迅速に導入する施設もあれば後発組もいる」（P6）という発言が記録されている。

### 2.2.3 心理的・受容性課題

**自動価格変更に対する心理的抵抗**

Ivanov & Webster（2024, Technology in Society, 被引用数84件）は、ブルガリアのホテルマネージャー130名を対象に、4つのAI意思決定アプローチ（human only, human-in-the-loop, human-on-the-loop, human-out-of-the-loop）に対する選好を23の意思決定タスク×8部門で調査した。主要な結果は以下の通りである:

- マネージャーの大多数は意思決定プロセスの制御を維持したい（human-in-the-loop選好）。
- 感情知能（emotional intelligence）が高いマネージャーほどAI関与に否定的。
- 顧客・従業員との対話が必要な意思決定はhuman only/human-in-the-loopが選好される。
- マネージャーの個人属性（性別、年齢、教育、経験、職位）やホテル属性（規模、カテゴリ、立地）は選好に有意な影響を示さない。
- AIに対する一般的態度が個別意思決定のAI選好の最良の予測因子である。

**信頼不足とオーバーライド**

Mohammed & Denizci Guillet（2025a, IJCHM, 被引用数10件）は、RM担当者のRMSオーバーライド行動を認知バイアスの観点から分析した。結果として、(1) RMSが信頼されていないためオーバーライドが頻発し、(2) オーバーライドは代表性・利用可能性・アンカリング等のヒューリスティクスに影響されることが実証された。これは、「AIシステムによる価格推薦 → 人間の判断 → 最終価格決定」というプロセスにおいて、人間側の認知的限界がパフォーマンスを低下させるメカニズムを明示的に記述した重要な研究である。

Schwartz, Webb, & Liu（2025, European Journal of Tourism Research）は、RM分析が人間の直感に反する場合（容量制約下でのチャネル需要相関）、非専門家もRM専門家も正答率はともに約40%であるにもかかわらず、RM専門家は自身の判断により大きな自信を持っていることを示した。これは「システムは信頼しないが自分の直感は信頼する」という課題の定量的証拠である。

## 2.3 地方施設特有の事情

上記の一般的課題に加え、地方宿泊施設には以下の特有の事情がある（これらは文献から直接的に示されている事項と、複数文献を踏まえた考察を含む）。

**地域イベント依存**: 地方施設の需要は地域イベント（祭り、花見、紅葉シーズン、スポーツ大会等）に強く依存する傾向がある。Talón-Ballestero, Nieto-García et al.（2022, IJHM, 被引用数65件）は、DP研究のレビューにおいて、需要の高ボラティリティが価格最適化をより困難にすることを指摘している。【考察】地域イベントの需要影響は、大都市ホテルのような安定した出張・観光需要と比較して予測が困難であり、従来のRMSの需要予測モデルが前提とする「過去パターンの反復」が成立しにくい。

**常連客との関係性**: 【考察】地方施設はリピーター率が高い傾向にあり、価格の頻繁な変更は常連客との関係性を損なう可能性がある。Gómez-Talal, Talón-Ballestero, & Leoni（2025, Tourism Review, 被引用数11件）は、レストランにおけるDPが顧客の価格感情に与える影響を調査し、サービス品質が高い場合には価格変更の否定的影響が緩和されることを示した。

**ブランドよりも口コミ依存**: Abrate, Nicolau, & Viglia（2019, Tourism Management, 被引用数215件）は、Review ratingが収益に明確な正の影響を及ぼすことを実証した。【考察】ブランド力が限定的な地方施設においては、口コミはブランドの代替物として機能し、宿泊選択の主要決定因子となる可能性が高い。Cıftcı, Berezına, & Cavusoglu（2020）は、オンラインレビューが「RMの新たなレバー」であることを指摘している。

**価格よりも納得感の重視**: 【考察】地方施設においては、「市場均衡価格の実現」よりも「施設オーナー・マネージャーが価格設定に納得すること」が重要であると推測される。Mohammed & Denizci Guillet（2025b）の知見—「システムを信頼するため、システムの動作を理解する必要がある」（P16）—は、この推測を間接的に支持する。

## 2.4 課題の分類体系

| 類型 | 具体的課題 | 代表文献 | 課題の性質 |
|------|-----------|---------|----------|
| 技術的課題 | RMSのブラックボックス性 | Mohammed & Denizci Guillet (2025b) | 技術+心理 |
| 技術的課題 | データ不足（予約データ、外部データ） | Munnaluri (2022); Zaki (2022) | 技術 |
| 技術的課題 | 需要変動の不安定性（小規模施設） | Talón-Ballestero et al. (2022) | 技術 |
| 技術的課題 | 既存システム（PMS等）との互換性 | Alrawadieh et al. (2021) | 技術 |
| 組織的課題 | RM専門人材不足 | Sun et al. (2025) | 制度・運用 |
| 組織的課題 | RMSの導入・維持コスト | Alrawadieh et al. (2021) | 制度 |
| 組織的課題 | 組織文化と変革抵抗 | Mohammed & Denizci Guillet (2025b) | 制度・心理 |
| 組織的課題 | オーナー経営者の直感的意思決定との矛盾 | Sun et al. (2025) | 運用・心理 |
| 心理的課題 | 自動化への抵抗（制御維持願望） | Ivanov & Webster (2024) | 心理 |
| 心理的課題 | RMSへの不信（オーバーライド頻発） | Mohammed & Denizci Guillet (2025a) | 心理 |
| 心理的課題 | 専門家の過信（直感>分析） | Schwartz, Webb, & Liu (2025) | 心理 |
| 地方特有 | 地域イベント依存の需要パターン | — | 技術・運用 |
| 地方特有 | 常連客との関係性への配慮 | — | 心理・運用 |
| 地方特有 | ブランドより口コミ依存 | Abrate et al. (2019) | 市場構造 |

---

# 3. 既存研究・既存ソリューションによる対応

## 3.1 説明可能AI（XAI）のRMSへの統合

### Mohammed & Denizci Guillet (2025b) — XAIとホテルRMSの統合に関するステークホルダー観点

- **論文情報**: Mohammed, I. & Denizci Guillet, B. (2025). "Stakeholder perspectives on integrating explainable artificial intelligence into hotel revenue management system." *Tourism Economics*, OnlineFirst. doi:10.1177/13548166251382289
- **研究背景**: RMSのブラックボックス性が不信とオーバーライドを引き起こしている。XAIがこの問題を解決できるかを、27名のRM専門家（RMエグゼクティブ18名、技術専門家9名; 米国、香港、オーストラリア、中国、フランス等10カ国）へのインタビューで探索。
- **手法**: TTF（Task-Technology Fit）とTOE（Technology-Organisation-Environment）フレームワークに基づく質的分析。テーマ的内容分析（thematic content analysis）を適用。
- **主な知見**:
  - XAIの認知度と準備状況は「低い」。多くのRM担当者はXAIの能力を知らない。
  - XAIの能力（what, how, why, why not, what-if, how-to, what-elseの7種の質問駆動型説明）はRMユーザーの情報ニーズと整合する。
  - **エンドユーザー**は局所的（出力固有）説明を求め、**システムプロバイダー**は全体的（モデルレベル）説明を求める。説明ニーズの二極化。
  - ユーザーの好む説明形式は「簡潔さ」（250〜300語の箇条書き）「文脈化とパーソナライゼーション」「インタラクティブな対話」。
  - 採用阻害要因: プライバシー（11回言及）、セキュリティ（9回）、互換性（8回）、資源制約（5回）。
- **対応できる課題**: ブラックボックス性、不信、オーバーライド。
- **限界**: ホテルRMSにおけるXAIは未実装であり、経済的パフォーマンス（ADR, RevPAR, 稼働率）への影響が定量的に評価されていない。中小施設のRM担当者のサンプルが限定的。

### Heger (2025) — 収益管理におけるXAIの最適化と応用

- **論文情報**: Heger, J. (2025). "Optimization and (Explainable) Artificial Intelligence for Data-Driven Decision Support in Revenue and Risk Management." PhD Dissertation, University of Augsburg.
- **研究背景**: RM・リスク管理における意思決定支援のためにXAIを応用する方法論的フレームワークを提案。
- **手法**: SHAP（SHapley Additive exPlanations）等のXAI手法を用いて、需要予測モデルの出力を説明可能にする。
- **対応できる課題**: 予測結果の説明可能性。
- **限界**: ホスピタリティ産業に特化した検証は限定的。

### Tatlıdil, Yavuz, & Yöndem (2025) — 観光業における契約価格最適化とXAI

- **論文情報**: Tatlıdil, N.M., Yavuz, R., & Yöndem, M.T. (2025). "Contract Price Optimization in Tourism with Explainable AI." *2025 10th International Conference*, IEEE.
- **研究背景**: 観光産業の価格連鎖における各レベルの意思決定を説明可能にする。
- **対応できる課題**: 価格設定根拠の透明化。

## 3.2 Human-in-the-loop設計と自動化レベル

### Ivanov & Webster (2024) — ホテル経営者の自動意思決定に対する知覚

- **論文情報**: Ivanov, S. & Webster, C. (2024). "Automated decision-making: Hoteliers' perceptions." *Technology in Society*, 76, 102430. doi:10.1016/j.techsoc.2023.102430
- **被引用数**: 84件
- **研究背景**: ホテル経営者がどの程度の自動化をどの業務に受け入れるかを、4段階のAI関与レベルで定量的に調査。
- **手法**: ブルガリアの130名のホテルマネージャーに対するサーベイ。23の意思決定×8部門を4つのAI意思決定アプローチにマッピング。クラスター分析でAI態度による2グループを特定。
- **主な知見**:
  - マネージャーの大多数は意思決定の制御を維持したい（human-in-the-loop選好）。
  - 感情知能を必要としない業務、顧客・従業員との直接対話が不要な業務はAI委任に寛容。
  - **価格設定は「制御維持」が強く選好される業務の一つ**。
  - AI態度がAI意思決定アプローチ選好の最良予測因子。
- **対応できる課題**: 自動化への抵抗、制御維持願望。「提案型」の設計が受容されやすい。
- **限界**: ブルガリアの単一国研究。ホテルカテゴリ・地域による差異が未分析。

### Garcia, Tolvanen, & Wagner (2026) — アルゴリズム推薦に対する戦略的反応：ホテル価格設定からの実証

- **論文情報**: Garcia, D., Tolvanen, J., & Wagner, A.K. (2026). "Strategic responses to algorithmic recommendations: evidence from hotel pricing." *Management Science*. doi:10.1287/mnsc.2022.03740
- **被引用数**: 18件
- **研究背景**: RM企業のアルゴリズム推薦に対してホテルマネージャーがどのように反応するかを、大規模な実データで分析。
- **手法**: RMコンサルティング企業のデータを使用。アルゴリズムの価格推薦と、マネージャーが実際に設定した価格の乖離を分析。
- **主な知見**:
  - ホテルマネージャーはアルゴリズム推薦からの系統的乖離パターンを示す。
  - 推薦からの乖離は調整コストの差異から生じる。
  - 「human in the loop」状況において、推薦への準拠度が収益パフォーマンスと正相関する場合がある。
- **対応できる課題**: 人間ーアルゴリズム相互作用の理解、推薦型システムの設計改善。
- **限界**: 推薦を無視する理由（情報不足、不信、状況的要因）の区別が限定的。

### Salgado-Criado (2025) — AIの人間監視：オペレーションズ・マネジメントの観点

- **論文情報**: Salgado-Criado, J. (2025). "Human oversight of artificial intelligence: An operations management perspective." *Journal of Industrial Engineering and Management*. doi:10.3926/jiem.8567
- **被引用数**: 4件
- **研究背景**: AIに対する人間の監視を、意思決定支援システムの観点から整理。ホテルRMを事例に含む。
- **主な知見**: 人間の監視はhuman-in-the-loop状況では意思決定の質を改善するが、システムの複雑性が人間の認知能力を超える場合にはかえって悪化する。

## 3.3 レビュー・口コミを価格判断に活かす研究

### Abrate, Nicolau, & Viglia (2019) — 動的価格変動性の収益最大化への影響

- **論文情報**: Abrate, G., Nicolau, J.L., & Viglia, G. (2019). "The impact of dynamic price variability on revenue maximization." *Tourism Management*, 74, 224–233.
- **被引用数**: 215件
- **研究背景**: ホテルの動的価格変動性が収益に与える影響を、ヘドニック収益モデルを用いて検証。
- **手法**: ヘドニック収益モデルを適用し、(1) 戦略的客室非可用性（strategic room unavailability）、(2) レビュー評価、(3) 価格変動性が収益に与える影響を分解。
- **主な知見**: レビュー評価と戦略的客室非可用性は収益に明確な正の影響を持つ。**レビュー評価が高い施設は、DP戦略からの収益を高めやすい**。
- **対応できる課題**: 口コミ評価と収益の関係の定量化。
- **限界**: レビューのaspectレベル分析はなし。テキスト内容の分析は行われていない。

### Wu, Zhong, Qiu, & Wu (2022) — 顧客レビューはただのレビューか？感情分析によるホテル需要予測

- **論文情報**: Wu, D.C., Zhong, S., Qiu, R.T.R., & Wu, J. (2022). "Are customer reviews just reviews? Hotel forecasting using sentiment analysis." *Tourism Economics*, 28(3), 795–816. doi:10.1177/13548166211049865
- **被引用数**: 78件
- **研究背景**: 顧客レビューの感情情報がホテルの需要予測精度を向上させるかを検証。マカオのラグジュアリーホテル4軒を対象。
- **手法**: レビューテキストから感情スコアを抽出し、従来の構造化データに基づく需要予測モデルの追加特徴量として統合。時系列予測モデル（ARIMA, LSTM等）と比較。
- **主な知見**: **感情スコアの追加は需要予測精度を統計的に有意に改善する**。特に需要変動期（季節変わり目、イベント期間）での改善が顕著。
- **対応できる課題**: レビューの需要予測への有効性の実証。
- **限界**: ラグジュアリーホテルのみを対象としており、中小・地方施設への一般化が未検証。aspectレベルの分析は行われていない。

### Zhang, Lu, & Liu (2021) — ABSA（アスペクトレベル感情分析）に基づくホテル顧客選好の導出

- **論文情報**: Zhang, J., Lu, X., & Liu, D. (2021). "Deriving customer preferences for hotels based on aspect-level sentiment analysis of online reviews." *Electronic Commerce Research and Applications*, 49, 101094. doi:10.1016/j.elerap.2021.101094
- **被引用数**: 82件
- **研究背景**: ホテルの属性（価格、立地、清潔さ、サービス等）ごとの顧客選好を、教師なしABSAで抽出する手法を提案。
- **手法**: 教師なしのaspectレベル感情分析アプローチ。暗黙のホテルaspect（implicit aspect）を認識するパイプラインを構築。
- **主な知見**: 顧客は各ホテル属性に異なる注目度を払っており、ABSAにより各属性の相対的重要度を定量化できる。**価格への注目度はホテルカテゴリにより異なる**。
- **対応できる課題**: 口コミから顧客の属性別選好を導出する技術的基盤。
- **限界**: 抽出した選好を価格設定に直接活用する方法論は提示されていない。

### Özen & Özgül Katlav (2023) — テクノロジー対応ホテルのABSAによる顧客分析

- **論文情報**: Özen, İ.A. & Özgül Katlav, E. (2023). "Aspect-based sentiment analysis on online customer reviews: a case study of technology-supported hotels." *Journal of Hospitality and Tourism Technology*, 14(2), 102–120.
- **被引用数**: 47件
- **研究背景**: テクノロジーを積極的に導入するホテルのレビューに対してABSAを適用し、顧客がどのテクノロジー要素（客室内タブレット、モバイルチェックイン、AI応対等）を評価し、どれを不満と感じているかを特定。
- **対応できる課題**: 宿泊施設のaspectごとの顧客感情の定量化手法。

### Degife & Lin (2024) — ABSAとGRUの統合による航空運賃予測

（前回調査文書に詳述。Applied Sciences, 14(10), 4221.）

- **核心的貢献**: ABSAで抽出した9つのaspectグループの感情スコアをGRU需要予測モデルに直接統合し、R² = 0.9899を達成。Safety & Securityを除去するとR²が0.6752に急落するという感度分析により、特定aspectの予測貢献度を定量化。
- **対応できる課題**: ABSAスコアの需要/価格予測モデルへの統合手法の実証。
- **限界**: 航空産業であり宿泊産業への直接適用は未検証。動的価格最適化（prescriptive）ではなく予測（predictive）にとどまる。

### Di Persio & Lalmi (2024) — NLPと回帰手法によるAirbnb最適価格設定

（前回調査文書に詳述。JRFM, 17(9), 414.）

- **核心的貢献**: BoW, TF-IDF, ABSA（CNN）をAirbnb価格予測に適用。ABSAのHOST-GENERAL aspectでは93%がポジティブ。Forward Feature Selectionがレビュースコアを重要特徴量として選出。
- **対応できる課題**: レビュー情報の宿泊価格予測への統合。
- **限界**: ABSAが1aspect（HOST-GENERAL）のみ。静的価格予測。

## 3.4 価格決定支援システム（DSS）のアプローチ

### Gao (2025) — 動的価格アルゴリズムとデータ分析によるホテルRM最適化

- **論文情報**: Gao, J. (2025). "Optimizing hotel revenue management through dynamic pricing algorithms and data analysis." *Journal of Computational Methods in Sciences and Engineering*, 25(1).
- **被引用数**: 11件
- **研究背景**: 価格最適化アルゴリズムの設計において、意思決定支援技術の統合を検討。
- **対応できる課題**: アルゴリズムベースの価格支援ツールの設計原則。

### Han & Bai (2022) — ホスピタリティと観光における価格研究の体系的レビュー

- **論文情報**: Han, W. & Bai, B. (2022). "Pricing research in hospitality and tourism and marketing literature: a systematic review and research agenda." *International Journal of Contemporary Hospitality Management*, 34(5), 1717–1738.
- **被引用数**: 70件
- **研究背景**: 2000年以降のホスピタリティ・観光・マーケティングの価格研究を体系的レビュー。
- **主な知見**: シェアリングエコノミー（Airbnb）の価格研究が急増傾向。レビュー評価の価格影響に関する研究は増加しているが、レビューテキストの内容分析を価格設定に活用する研究は依然として限定的。「レビュー感情→価格設定への統合」は今後の重要な研究課題として特定されている。

## 3.5 中小事業者向け簡易型RM/価格支援

文献において、中小宿泊施設に特化した簡易型RM/意思決定支援ツールの体系的な学術研究は限られている。商用ソリューションでは、Atomize（スウェーデン発、AI価格推薦）、RoomPriceGenie（スイス発、中小ホテル向け自動価格設定）等が存在するが、これらのシステムに関する査読付き学術論文は少ない。

Nair（2019, IJHM, 被引用数87件）は、カタールのホテルにおける価格戦略と非価格戦略の分析を行い、9つの価格戦略と4つの非価格戦略の使用状況を報告した。この研究は、RM戦略が価格だけでなく非価格要因（サービス品質、口コミ対応等）との相互作用で効果を発揮することを示唆している。

---

# 4. 口コミ活用型価格決定支援エージェントという方向性の妥当性

## 4.1 口コミを使うことが地方宿泊施設の価格決定支援に適している理由

### 4.1.1 文献に基づく根拠

**(1) 口コミは需要・収益と有意に相関する**

Abrate, Nicolau, & Viglia（2019, 被引用数215件）は、レビュー評価が収益に正の影響を持つことを定量的に示した。Wu et al.（2022, 被引用数78件）は、レビュー感情スコアが需要予測精度を統計的に有意に改善することを実証した。これらは、口コミが単なる「評判指標」ではなく、需要と価格の説明変数として機能することの文献的根拠である。

**(2) ブランド力が限定的な施設では口コミの影響力がより大きい**

Cıftcı, Berezına, & Cavusoglu（2020）は、オンラインレビューが宿泊選択において価格と並ぶ重要な決定因子であることを示した。Liu, Lai, Wu, & Luo（2022, 被引用数37件）は、P2P宿泊（ホテルチェーンのブランドを持たない施設）においてeWoM（電子口コミ）の影響が特に大きいことを実証した。地方の独立系宿泊施設もブランド認知が限定的であり、口コミの信号としての重要性が相対的に高い。

**(3) 既存DPでは拾いにくい情報を口コミが補完する**

従来のRMSは構造化データ（過去の予約データ、競合価格、カレンダー情報）に依拠する。しかし、**顧客がどのサービス属性に不満を持ち、何を高く評価しているか**という情報は構造化データには含まれない。Zhang, Lu, & Liu（2021, 被引用数82件）は、ABSAにより各属性の顧客選好を定量化できることを示した。Degife & Lin（2024）は、ABSAスコアの追加が予測精度を大幅に改善する（R²: 基準モデル → 0.9899）ことを実証した。

### 4.1.2 研究ギャップとして整理すべき点

口コミ感情を**価格決定の「根拠提示」に統合**した研究は、文献調査の範囲では確認されなかった。既存研究は以下のいずれかに分類される:

- **カテゴリA**: 口コミ → 需要/価格の「予測」精度向上（Wu et al., 2022; Degife & Lin, 2024; Di Persio & Lalmi, 2024）。
- **カテゴリB**: 口コミ → DP理論への統合（Shin et al., 2023; Correa et al., 2024）。ただし理論的モデルであり実装はされていない。
- **カテゴリC**: 口コミ → 消費者行動の理解（Zhang et al., 2021; Özen & Özgül Katlav, 2023）。

**カテゴリD（未存在）**: 口コミの分析結果を、**人間の意思決定者に対する「価格提案の根拠説明」**として提示するシステム。すなわち、「清潔さに関する口コミ感情が先月比で-15%低下しているため、価格引き下げの検討が必要」のような説明を伴う価格支援エージェントは、文献上の空白領域である。

## 4.2 「根拠提示型」設計の利点

### 4.2.1 完全自動ではなく提案型にする利点（文献根拠あり）

- Ivanov & Webster（2024）の結果から、ホテルマネージャーは価格決定において「制御維持」を強く望む。
- Mohammed & Denizci Guillet（2025a）の結果から、システムが「なぜその価格を推薦するのか」を説明できない場合、オーバーライドが頻発し、認知バイアスが介入する。
- Mohammed & Denizci Guillet（2025b）の結果から、RM担当者は「what if」「why」「why not」の説明を最も求めている。

これらの知見を統合すると、(1) 最終決定権は人間が保持、(2) システムは口コミ分析に基づく根拠を提示、(3) 根拠はaspectレベルで具体的、(4) 対話的（what-ifシナリオ提示）、という設計原則が導かれる。

### 4.2.2 需要予測モデル単独より顧客評価シグナルを併用する意義（文献根拠+考察）

文献根拠: Wu et al.（2022）は感情スコア追加による予測改善を実証。Degife & Lin（2024）は9つのaspect感情スコアの個別貢献度を感度分析で定量化。

【考察】地方施設では予約データが少なく、従来の時系列モデルの精度が低い可能性がある。口コミは外部から無償で取得可能なデータソースであり、データスパーシティの補完手段として有効であると推測される。さらに、「口コミで言及された具体的な改善点」は、施設オーナーにとって直感的に理解しやすい説明材料であり、アルゴリズムの出力（需要予測値、最適価格）よりも「納得」を得やすい可能性がある。

---

# 5. 研究ギャップ

以下の研究ギャップが特定された。各ギャップの種類（文献的空白/方法論的限界/応用領域の欠如）を明示する。

## ギャップ1: ABSAと価格決定支援の未統合（文献的空白）

ABSAで抽出されたaspect感情スコアを、価格「予測」に統合した研究は存在する（Degife & Lin, 2024; Di Persio & Lalmi, 2024）。しかし、ABSAの結果を**人間の意思決定者に対する価格根拠**として活用するシステムの研究は存在しない。

## ギャップ2: XAIとレビュー分析の統合アプローチの不在（文献的空白）

Mohammed & Denizci Guillet（2025b）はXAIのRMS統合を探索しているが、XAIの説明対象は「RMSアルゴリズムの内部ロジック」であり、「レビューから得られる顧客声」を説明材料として活用するアプローチは提案されていない。

## ギャップ3: 中小・地方宿泊施設を対象とした価格支援研究の不足（応用領域の欠如）

RM研究の大部分は大手チェーンホテル、ラグジュアリーホテル、大都市の施設を対象としている（Wu et al., 2022のマカオラグジュアリーホテル; Di Persio & Lalmi, 2024のローマAirbnb）。地方の中小独立系宿泊施設に特化した価格決定支援の研究は極めて限定的である。Sun et al.（2025）が中小独立系ホテルの組織構造を扱っているが、技術的な価格支援システムは提案していない。

## ギャップ4: 口コミのaspect別価格弾力性の未推定（方法論的限界）

Zhang et al.（2021）はaspectごとの顧客選好を定量化し、Degife & Lin（2024）はaspect感情スコアの予測貢献度を感度分析で示した。しかし、「特定のaspect（例: 清潔さ）の感情悪化が、価格弾力性をどの程度変化させるか」を推定した研究は存在しない。

## ギャップ5: 価格提案の受容性評価の方法論的不在（方法論的限界）

Ivanov & Webster（2024）はAI意思決定アプローチの選好を調査し、Mohammed & Denizci Guillet（2025a）はオーバーライド行動の認知的要因を分析した。しかし、**口コミ情報に基づく価格提案を施設マネージャーが実際に「納得する」かどうか**を検証した研究はない。

## ギャップ6: 因果推定の欠如（方法論的限界）

口コミ感情と需要/価格の関係について、多くの研究が相関関係のみを示し、因果的識別を行った研究は少ない。内生性問題（人気施設がポジティブレビューを集めやすい）が未解決。

---

# 6. 今後の有望な研究方向

## 6.1 研究テーマの設定

**推奨テーマ**: 「地方宿泊施設における口コミ分析に基づく説明可能な価格決定支援システムの設計と評価」

このテーマは、「ダイナミックプライシング研究」ではなく「価格決定支援エージェント研究」として位置づけられる。DP研究は最適価格の「計算」に焦点を当てるが、本研究は最適価格の「説明」と「現場の意思決定支援」に焦点を当てる。この位置づけは以下の文献的根拠に基づく:

- [文献根拠] Ivanov & Webster（2024）: ホテルマネージャーは価格決定の制御維持を望む → 完全自動ではなく提案型が適切。
- [文献根拠] Mohammed & Denizci Guillet（2025b）: 説明可能性への需要は高いが、XAI導入は未実現 → 説明可能な支援システムの研究に機会がある。
- [文献根拠] Wu et al.（2022）; Degife & Lin（2024）: レビュー感情は需要予測に有効 → 予測への統合から、説明への活用へ拡張可能。

## 6.2 研究課題の候補

### RQ1: 口コミのaspect感情は、宿泊施設の需要/価格にどの程度影響するか？

- 技術構成: BERTベースABSA → aspect感情スコア → 需要/価格予測モデルへの統合。
- [文献根拠] Degife & Lin（2024）のABSA_GRUアプローチを宿泊施設データに適用。

### RQ2: aspercレベルの口コミ分析は、施設マネージャーにとって価格設定根拠として理解可能・有用か？

- 技術構成: ABSAの結果を自然言語で要約し、価格提案の根拠として提示するインターフェース設計。
- [文献根拠] Mohammed & Denizci Guillet（2025b）のXAI説明ニーズ分析（what, why, what-if）。
- [考察] 口コミの具体的内容（「朝食が美味しい」「浴室が古い」）は、数値的需要予測よりも直感的理解が容易であり、XAIの「何を説明するか」問題に対する新たなアプローチとなりうる。

### RQ3: 提案型エージェントは、施設マネージャーの価格決定の質を向上させるか？

- [文献根拠] Garcia, Tolvanen, & Wagner（2026）のアルゴリズム推薦と人間の反応の分析手法を応用。
- 評価指標: (1) 提案受容率、(2) 収益パフォーマンス、(3) マネージャーの意思決定効率。

## 6.3 技術構成の候補

### 6.3.1 口コミ感情分析（ABSA）

- **手法**: 事前学習済みBERTまたはドメイン適応BERTを用いたaspect抽出と感情分類。宿泊施設ドメインのaspectとして、清潔さ、立地、サービス・接客、食事、部屋の設備、コストパフォーマンス、温泉・大浴場（日本の宿泊施設特有）、チェックイン/アウトを設定。
- [文献根拠] Zhang, Lu, & Liu（2021）; Özen & Özgül Katlav（2023）; Degife & Lin（2024）。

### 6.3.2 需要予測との組み合わせ

- ABSA感情スコアを需要予測モデル（GRU, LSTM, XGBoost等）の追加特徴量として統合。
- [文献根拠] Degife & Lin（2024）のABSA_GRUモデル; Wu et al.（2022）の感情スコア統合。
- [考察] 地方施設ではデータスパーシティが問題となるため、transfer learning（大規模データで事前学習し、少量のターゲットデータでfine-tuning）が有効と推測される。

### 6.3.3 説明生成

- aspect感情スコアの変動要因を自然言語で要約するモジュール。
- [考察] LLM（大規模言語モデル）を用いた要約生成が候補。「先月比で『清潔さ』に関するネガティブレビューが20%増加しています。具体的には『浴室のカビ』『タオルの臭い』が言及されています。競合施設の同aspect感情と比較して下回っており、価格調整の検討を推奨します」のような説明文を自動生成。
- [文献根拠] Mohammed & Denizci Guillet（2025b）が指摘する「文脈化とパーソナライゼーション」「インタラクティブな対話」の説明要件に合致。

### 6.3.4 価格提案根拠の可視化

- ダッシュボード形式で、(1) aspect別感情トレンド、(2) 感情スコアと需要/稼働率の相関、(3) 競合施設との感情比較、(4) 推薦価格とその根拠のサマリーを表示。
- [文献根拠] Heger（2025）のSHAPベース説明可視化; Mohammed & Denizci Guillet（2025b）の「250〜300語の箇条書き」の簡潔さ要件。

### 6.3.5 Human-in-the-loop設計

- システムは価格を「推薦」し、最終決定は施設マネージャーが行う。
- What-ifシナリオ機能: 「もし朝食の改善を行い、食事aspectの感情スコアが+0.2向上した場合、推薦価格は¥XXXに変化します」。
- [文献根拠] Ivanov & Webster（2024）のhuman-in-the-loop選好; Mohammed & Denizci Guillet（2025b）の「what-if」説明ニーズ。

## 6.4 実証の仕方

### 6.4.1 精度評価

- 需要/価格予測精度: RMSE, MAE, R²。ABSA統合モデル vs 非統合モデルの比較。
- [文献根拠] Degife & Lin（2024）; Wu et al.（2022）の評価指標。

### 6.4.2 受容性評価

- 実際の宿泊施設マネージャーを対象としたユーザースタディ。提案受容率、信頼度（Likertスケール）、意思決定時間を測定。
- [文献根拠] Ivanov & Webster（2024）のサーベイ設計; Mohammed & Denizci Guillet（2025b）のインタビュー手法。
- [考察] 日本の地方宿泊施設（旅館含む）を対象としたフィールドスタディが、研究の独自性を高める。

### 6.4.3 説明可能性評価

- 説明の質を「理解度」「有用性」「信頼向上度」の3軸で評価。
- [文献根拠] Mohammed & Denizci Guillet（2025b）のTTFフレームワークに基づく評価。

### 6.4.4 現場意思決定支援としての有効性評価

- A/Bテスト: エージェント使用群 vs 非使用群の収益パフォーマンス比較。
- [考察] 実環境でのA/Bテストは倫理的・実務的制約が大きいため、シミュレーション環境での検証が現実的第一段階と推測される。

---

# 7. 結論

本文献調査により、以下の5点が明らかになった。

1. **地方・中小宿泊施設におけるRM導入の障壁は多層的**である。技術的課題（ブラックボックス性、データ不足）、組織的課題（人材不足、コスト）、心理的課題（自動化抵抗、不信）が相互に関連するが、心理的課題が最も根深い。

2. **既存のXAI・human-in-the-loop研究**は、RMSの透明性向上と人間の意思決定支援に焦点を当てているが、「何を説明するか」の具体的な情報源として**口コミのaspect感情**を活用するアプローチは存在しない。

3. **口コミ/感情分析の価格・需要への統合研究**は急速に進展しているが、全て「予測精度向上」が目的であり、「価格決定根拠の提示」という意思決定支援の枠組みでは位置づけられていない。

4. **「口コミ活用型価格決定支援エージェント」**という方向性は、(a) 口コミの需要/収益への影響の文献的根拠、(b) human-in-the-loop設計への実務的需要、(c) XAI統合の研究ニーズ、の3つの文献的知見の交差点に位置し、研究として妥当性がある。

5. **主要な研究ギャップ**は、ABSAと価格決定支援の未統合、XAIとレビュー分析の未結合、中小・地方施設を対象とした研究の不足であり、これらは独自の研究貢献の機会を提供する。

---

# 参考文献

1. Abrate, G., Nicolau, J.L., & Viglia, G. (2019). The impact of dynamic price variability on revenue maximization. *Tourism Management*, 74, 224–233.
2. Alrawadieh, Z., Alrawadieh, Z., & Cetin, G. (2021). Digital transformation and revenue management: Evidence from the hotel industry. *Tourism Economics*, 27(2), 328–345. doi:10.1177/1354816620901928
3. Cıftcı, O., Berezına, K., & Cavusoglu, M. (2020). Winning the battle: The importance of price and online reviews for hotel selection. *Advances in Hospitality and Tourism Research*, 8(1), 177–202.
4. Correa, J., Mari, M., & Xia, A. (2024). Dynamic pricing with Bayesian updates from online reviews. *arXiv preprint*, arXiv:2404.14953.
5. Degife, W.A. & Lin, B.-S. (2024). A multi-aspect informed GRU: A hybrid model of flight fare forecasting with sentiment analysis. *Applied Sciences*, 14(10), 4221.
6. Denizci Guillet, B. & Mohammed, I. (2015). Revenue management research in hospitality and tourism: a critical review of current literature and suggestions for future research. *International Journal of Contemporary Hospitality Management*, 27(4), 526–560.
7. Di Persio, L. & Lalmi, E. (2024). Maximizing profitability and occupancy: An optimal pricing strategy for Airbnb hosts using regression techniques and NLP. *Journal of Risk and Financial Management*, 17(9), 414.
8. Garcia, D., Tolvanen, J., & Wagner, A.K. (2026). Strategic responses to algorithmic recommendations: evidence from hotel pricing. *Management Science*. doi:10.1287/mnsc.2022.03740
9. Gao, J. (2025). Optimizing hotel revenue management through dynamic pricing algorithms and data analysis. *Journal of Computational Methods in Sciences and Engineering*, 25(1).
10. Gómez-Talal, I., Talón-Ballestero, P., & Leoni, V. (2025). The impact of dynamic pricing on restaurant customers' perceptions and price sentiment. *Tourism Review*, 80(5), 1101.
11. Han, W. & Bai, B. (2022). Pricing research in hospitality and tourism and marketing literature: a systematic review and research agenda. *International Journal of Contemporary Hospitality Management*, 34(5), 1717–1738.
12. Heger, J. (2025). Optimization and (Explainable) Artificial Intelligence for Data-Driven Decision Support in Revenue and Risk Management. PhD Dissertation, University of Augsburg.
13. Ivanov, S. & Webster, C. (2024). Automated decision-making: Hoteliers' perceptions. *Technology in Society*, 76, 102430.
14. Lima Santos, L., Gomes, C., & Malheiros, C. (2024). Factors influencing hotel revenue management in times of crisis: Towards financial sustainability. *International Journal of Financial Studies*, 12(4), 112.
15. Liu, F., Lai, K., Wu, J., & Luo, X. (2022). How electronic word of mouth matters in peer-to-peer accommodation: the role of price and responsiveness. *International Journal of Electronic Commerce*, 26(2), 218–245.
16. Mohammed, I. & Denizci Guillet, B. (2025a). Heuristics and biases in human–algorithm interaction and hotel revenue management override decision-making. *International Journal of Contemporary Hospitality Management*, 37(2), 358–379.
17. Mohammed, I. & Denizci Guillet, B. (2025b). Stakeholder perspectives on integrating explainable artificial intelligence into hotel revenue management system. *Tourism Economics*, OnlineFirst. doi:10.1177/13548166251382289
18. Mohammed, I. & Denizci Guillet, B. (2025c). Application of heuristics to revenue management system override decision-making. *Journal of Hospitality & Tourism Research*, 49(7), 1285–1302.
19. Munnaluri, V.K. (2022). Dynamic pricing in the hospitality industry in the presence of data scarcity. Master's Thesis, Politecnico di Milano.
20. Nair, G.K. (2019). Dynamics of pricing and non-pricing strategies, revenue management performance and competitive advantage in hotel industry. *International Journal of Hospitality Management*, 82, 287–297.
21. Özen, İ.A. & Özgül Katlav, E. (2023). Aspect-based sentiment analysis on online customer reviews: a case study of technology-supported hotels. *Journal of Hospitality and Tourism Technology*, 14(2), 102–120.
22. Salgado-Criado, J. (2025). Human oversight of artificial intelligence: An operations management perspective. *Journal of Industrial Engineering and Management*.
23. Schwartz, Z., Webb, T., & Liu, X. (2025). When hospitality revenue management analytics defies our biased intuition. *European Journal of Tourism Research*, 2025.
24. Shin, D., Vaccari, S., & Zeevi, A. (2023). Dynamic pricing with online reviews. *Management Science*, 69(2), 1032–1053.
25. Sun, L., Schuckert, M., & Hon, A.H.Y. (2025). Enhancing organizational structures for revenue management in small and medium-sized independent hotels: Evidence from China. *International Journal of Hospitality Management*, 2025. doi:10.1016/j.ijhm.2025.103980
26. Talón-Ballestero, P., Nieto-García, M., et al. (2022). The wheel of dynamic pricing: Towards open pricing and one to one pricing in hotel revenue management. *International Journal of Hospitality Management*, 103, 103213.
27. Talluri, K.T. & van Ryzin, G.J. (2004). *The Theory and Practice of Revenue Management*. Springer.
28. Tatlıdil, N.M., Yavuz, R., & Yöndem, M.T. (2025). Contract Price Optimization in Tourism with Explainable AI. *2025 10th International Conference*, IEEE.
29. Vives, A., Jacob, M., & Payeras, M. (2018). Revenue management and price optimization techniques in the hotel sector: A critical literature review. *Tourism Economics*, 24(6), 628–651.
30. Wu, D.C., Zhong, S., Qiu, R.T.R., & Wu, J. (2022). Are customer reviews just reviews? Hotel forecasting using sentiment analysis. *Tourism Economics*, 28(3), 795–816.
31. Zaki, K. (2022). Implementing dynamic revenue management in hotels during Covid-19: value stream and wavelet coherence perspectives. *International Journal of Contemporary Hospitality Management*, 34(5), 1768–1795.
32. Zhang, J., Lu, X., & Liu, D. (2021). Deriving customer preferences for hotels based on aspect-level sentiment analysis of online reviews. *Electronic Commerce Research and Applications*, 49, 101094.
