// Build: 自律型GSE — APEX サービス・ポジショニング (日本語版)
// For: 朝 永隆 様 (デロイト トーマツ ジャパン) — 提案書添付資料
// Author: Keven Markham, DMTSP

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
  TabStopType,
} = require('docx');

const AZURE = "0078D4";
const TEAL = "008272";
const SLATE_BG = "F1F5F9";
const HEAD_BG = "0F172A";
const BORDER = "CCCCCC";

const JP_FONT = "Yu Gothic";
const JP_FONT_UI = "Yu Gothic UI";

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: BORDER };
const cellBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };

function jpRun(text, opts = {}) {
  return new TextRun({
    text,
    bold: opts.bold,
    italics: opts.italics,
    size: opts.size || 22,
    color: opts.color,
    font: { name: opts.ui ? JP_FONT_UI : JP_FONT, eastAsia: opts.ui ? JP_FONT_UI : JP_FONT },
  });
}

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120, ...opts.spacing },
    alignment: opts.align,
    children: [jpRun(text, opts)],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [jpRun(text, { bold: true, size: 32, color: HEAD_BG, ui: true })],
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: AZURE, space: 4 } },
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 140 },
    children: [jpRun(text, { bold: true, size: 26, color: AZURE, ui: true })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [jpRun(text, { bold: true, size: 22, color: TEAL, ui: true })],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    children: [jpRun(text, { size: 22 })],
  });
}

function bulletRich(runs, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    children: runs,
  });
}

function headerCell(text, width) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: HEAD_BG, type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    children: [new Paragraph({ children: [jpRun(text, { bold: true, color: "FFFFFF", size: 20, ui: true })] })],
  });
}

function dataCell(text, width, opts = {}) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.shaded ? { fill: SLATE_BG, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 140, right: 140 },
    children: [new Paragraph({ children: [jpRun(text, { bold: opts.bold, size: 20 })] })],
  });
}

// =====================================================================
// CONTENT (日本語)
// =====================================================================

const cover = [
  new Paragraph({
    spacing: { after: 200 },
    children: [jpRun("デロイト ・ DMTSP ・ コンシューマー インダストリー", { bold: true, size: 18, color: AZURE, ui: true })],
  }),
  new Paragraph({
    spacing: { after: 120 },
    children: [jpRun("自律型グランドサポート機材（自律型GSE）", { bold: true, size: 44, color: HEAD_BG, ui: true })],
  }),
  new Paragraph({
    spacing: { after: 80 },
    children: [jpRun("APEX 準拠サービスとケイパビリティのポジショニング", { bold: true, size: 28, color: TEAL, ui: true })],
  }),
  new Paragraph({
    spacing: { after: 360 },
    children: [jpRun("デロイト トーマツ ジャパン 自律型GSE市場調査プロジェクト 提案書 添付資料", { italics: true, size: 22, color: "475569" })],
  }),
  p("作成者：Keven Markham（ケビン・マーカム）／Specialist Master, Deloitte Microsoft Technology & Services Practice (DMTSP)", { size: 20 }),
  p("送付先：朝 永隆（あさ ながたか）様 ／ デロイト トーマツ ジャパン", { size: 20 }),
  p("作成日：2026年5月1日", { size: 20 }),
  p("機密区分：社内限り（デロイト グローバル）", { size: 20, italics: true }),
  new Paragraph({ children: [new PageBreak()] }),
];

const execSummary = [
  h1("1. エグゼクティブサマリー"),
  p("自律型グランドサポート機材（GSE）—— 自律走行式トーイングトラクター、ベルトローダー、プッシュバックトラクター、GPU、給排水車両等 —— は、デロイトの APEX フレームワークが本来的に対応するために構築された3つの大きな潮流の交点に位置している。すなわち、(1) 産業用フリート・テレメトリの大規模化、(2) 時間制約の厳しい航空機ターン運用、(3) 自律型エアサイド運用に対する安全ケース要求を強める規制環境、の3点である。"),
  p("APEX（Agentic Platform for Enterprise eXecution）は、Microsoft ネイティブ基盤上にエージェント型 AI を展開するための DMTSP のドメイン正規リファレンス・フレームワークである。製品ではなく、業界共通の「文法」（Core）と業界別「方言」（Edition）を提供するフレームワークの集合体である。自律型GSEに対しては、以下の3つの APEX プラクティスが直接的に適用される。"),
  bulletRich([
    jpRun("ICE — 産業用・商用機材プラクティス", { bold: true, size: 22, ui: true }),
    jpRun("：機材自体のフリート健全性管理、稼働率最適化、補修部品トリアージ、コンプライアンス検査。GSE資産そのものの自然な収まり先。", { size: 22 }),
  ]),
  bulletRich([
    jpRun("TH — トラベル＆ホスピタリティ プラクティス（航空サブバリアント）", { bold: true, size: 22, ui: true }),
    jpRun("：ターン運用、運航障害リカバリー、ランプディスパッチ。自律型GSEが航空運用モデル内でどう機能するかを規定する。", { size: 22 }),
  ]),
  bulletRich([
    jpRun("AXLE — 自動車向け深掘りプログラム", { bold: true, size: 22, ui: true }),
    jpRun("：GSE OEM が安全ケース構築・V&V ハーネス・ODD（運用設計領域）規律のために必要とする自律走行車両エンジニアリングの深掘り。", { size: 22 }),
  ]),
  p("これら3プラクティスを組み合わせることで、本提案チームは (a) 空港運営者が自律型GSEに何を求めるか、(b) 勝者となる GSE OEM とそうでない OEM を分ける成功要因は何か、を体系的に把握できる。本書の第4章および第5章で、それぞれを詳述する。"),
];

const aboutAPEX = [
  h1("2. APEX 概要（1ページ要約）"),
  p("APEX は、エンタープライズイベントを「解決済み・監査可能な意思決定」へと変換する、マニフェスト駆動型のエージェント型プラットフォームである。データ層には Microsoft Fabric、インテリジェンス層には Azure AI サービスを採用し、すべてのスキーマ・エージェント・ツール・オーケストレーション・HITL（Human-in-the-Loop）ゲートをバージョン管理された契約により規定する。"),
  h3("7層リファレンス・アーキテクチャ"),
  p("各プラクティスは共通の7層を継承する：L1 エッジ＆ソース、L2 取込み＆統合、L3 ストレージ、L4 セマンティック、L5 インテリジェンス、L6 オーケストレーション、L7 エクスペリエンス。各層は具体的な Microsoft サービスにマッピングされる。自律型GSEの場合、L1 は車両バス、ランプ・テレメトリ、CDM/A-CDM フィードであり、L7 はOCC（オペレーションコントロールセンター）ディスパッチャー、ランプコーディネーター、整備リードである。"),
  h3("現時点のカタログ"),
  p("7プラクティス全体で 45 のサービスをカタログ化（GA：RC、HLS、ER、AXLE の 25 サービス／構築中：TMT、TH、ICE の 20 サービス、いずれも 2026 年中の GA を目標）。各サービスはサブスクリプション可能な SKU として、シナリオ・ペルソナ・KPI・SLO・成果物バンドル・前提条件・商務条件をパッケージ化している。"),
  h3("自律型GSEにおける本フレームワークの意義"),
  p("自律型GSEは APEX の典型的な対象領域である。すなわち、異種ソースからの高頻度イベントストリーム、安全に関わる時間制約付き意思決定、規制対応の監査証跡、運営者・OEM・ANSP・規制当局の境界を跨ぐ意思決定の合成 —— こうした要件を満たす必要があるからである。APEX はクライアントを共有ランタイムへ強制することなく、マニフェスト規律（スキーマ・ゲート・証跡）を提供する。"),
];

// Service mapping table
const serviceTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1500, 2400, 2100, 3360],
  rows: [
    new TableRow({ tableHeader: true, children: [
      headerCell("サービス ID", 1500),
      headerCell("サービス名", 2400),
      headerCell("APEX プラクティス", 2100),
      headerCell("自律型GSEへの適用", 3360),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-FAF-01", 1500, { bold: true }),
      dataCell("フィールド資産障害対応", 2400),
      dataCell("ICE — 産業用・商用機材", 2100),
      dataCell("バッテリー・駆動系・センサースタックの故障を、ターン運用に影響が及ぶ前に予兆検知・トリアージ。フリート全体の健全性テレメトリを航空運用クロックに同期させる。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-SPA-02", 1500, { bold: true }),
      dataCell("補修部品供給トリアージ", 2400),
      dataCell("ICE", 2100),
      dataCell("自律型プラットフォームでは LiDAR・IMU・コンピュートモジュール・駆動用バッテリーが長納期。MTBF とターン密度の予測に基づき、ハブ空港へ部品を事前配置。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-WCP-03", 1500, { bold: true }),
      dataCell("保証クレーム・パターン分析", 2400),
      dataCell("ICE", 2100),
      dataCell("OEM 向け：手動クレーム審査より早期に、フリート全体の故障モードパターンを検出。フィールドからエンジニアリングへのフィードバックループを閉じる。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-CRP-04", 1500, { bold: true }),
      dataCell("契約更新時の収益保護", 2400),
      dataCell("ICE", 2100),
      dataCell("自律型GSEのサービス契約における劣化シグナル（稼働率低下、ディスパッチ信頼性低下）を更新前に検知し、OEM・リース会社の継続収益を保護。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-AaS-05", 1500, { bold: true }),
      dataCell("As-a-Service 稼働率最適化", 2400),
      dataCell("ICE", 2100),
      dataCell("GSE-as-a-Service 商務モデルの中核サービス。資産別稼働率・SLA 適合性・従量課金テレメトリを管理。OEM が販売モデルからサブスクリプションモデルへ移行可能。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-CIR-06", 1500, { bold: true }),
      dataCell("コンプライアンス検査対応", 2400),
      dataCell("ICE", 2100),
      dataCell("FAA Part 139、EASA／CAA、JCAB の検査体制、SAE J3016 自律レベル区分、ICAO Annex 14 エアサイド安全規定に直接適合。検査ごとに監査品質の証跡を維持。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-TH-DRO-02", 1500, { bold: true }),
      dataCell("運航障害リカバリー・オーケストレーション", 2400),
      dataCell("TH — トラベル＆ホスピタリティ（航空）", 2100),
      dataCell("天候・IRROPS・スポット閉鎖が連鎖した際、自律型GSEの配備が制約変数となる。DRO は乗務員・ゲート・機体と並行して GSE 配備を再最適化。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-TH-HER-06", 1500, { bold: true }),
      dataCell("例外ルーティング（ランプ適応）", 2400),
      dataCell("TH（航空向け転用）", 2100),
      dataCell("元はハウスキーピング向けだが、同一の例外ルーティング・パターンがランプ例外（停止トラクター、プッシュバック窓欠落、GPU 停止等）に転用可能。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ER-FWO-04", 1500, { bold: true }),
      dataCell("フィールド作業指示最適化", 2400),
      dataCell("ER — エネルギー＆リソース", 2100),
      dataCell("Crew-Skills × Route-Optimiser ペア（ER-A07/A08）が、ハブ空港圏内の自律型GSE保守ディスパッチへ初回完了率目標とともに転用可能。", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-AXLE", 1500, { bold: true }),
      dataCell("自律走行車両 深掘りプログラム", 2400),
      dataCell("AXLE — 自動車", 2100),
      dataCell("GSE OEM 向け：ODD 定義、V&V ハーネス、安全ケース構成、OTA アップデート規律。ICE の商務フレームに対する自動車工学側の補完。", 3360, { shaded: true }),
    ]}),
  ],
});

const serviceMapping = [
  h1("3. 自律型GSEに対する APEX サービス・マッピング"),
  p("以下の表は、APEX のカタログ済みサービスを自律型GSE問題領域へマッピングしたものである。各行はシナリオ・KPI・HITL ゲート・成果物バンドルが定義されたサブスクリプション SKU である。標準的な Wave 1 案件では 2〜3 サービスでスタートし、ポートフォリオを順次拡張する。"),
  serviceTable,
  p(""),
  h3("常時付帯する横断ケイパビリティ"),
  bullet("マニフェストモデル：すべてのスキーマ（車両テレメトリ、作業指示、検査イベント等）をバージョン固定し、バンプ分類とマイグレーション規律を適用。"),
  bullet("HITL ゲート分類：すべての意思決定が HITL／ACK_ONLY／ZERO_TOUCH／ESCALATION のいずれかを明示宣言。自律型エアサイドの安全ケースに不可欠。"),
  bullet("インディペンデンス姿勢：データ平面はクライアントテナントに常駐し、デロイト側にクライアント識別可能なテレメトリを保持しない。空港運営者のデータ主権要件に整合。"),
  bullet("オブザーバビリティ：Application Insights、Fabric モニタリング、独自エージェント・テレメトリ。規制当局が読解可能な監査証跡をサポート。"),
];

const airportNeeds = [
  h1("4. 自律型GSE導入を駆動する空港側の課題とニーズ"),
  p("APEX TH（航空）および ICE プラクティスの枠組みから抽出。ACI、IATA AHM、JCAB／FAA エアサイド姿勢（2026年時点）と整合確認済み。"),
  h2("4.1 運用ドライバー"),
  bullet("ターン時間の圧縮：ハブ空港のナローボディ機ターンが 30 分を切る傾向にあり、地上サービスのばらつきが、天候・ATC 以外で最大の遅延残差要因となっている。"),
  bullet("ランプ要員不足：パンデミック後のランプ要員離職は、北米・EU・日本いずれにおいても構造的問題。採用サイクルが主要ハブのフリート増強に追いつかない。"),
  bullet("スポット混雑と A-CDM の精緻化：CDM／A-CDM のマイルストーン（TOBT、TSAT、ATOT）が厳格化しており、場当たり的な GSE 配備ではマイルストーン窓に収まらない。"),
  bullet("世代混在のフリート：多くのハブで3世代の GSE が同時運用されており、自律型プラットフォームは少なくとも 10 年間は手動機材と共存しなければならない。"),
  h2("4.2 安全・規制ドライバー"),
  bullet("エアサイド安全ケース：自律型GSEは ICAO Annex 14／FAA Part 139 検査体制下で ODD で限定された安全運用を立証する必要があり、安全ケース構築こそが最大のエンジニアリング負荷。"),
  bullet("FOD（落下物）・ランプインシデント低減：自律型GSEのテレメトリは、ヒヤリハット事象の可視化を初めて実現する。空港当局は当該証跡の提出をますます要求するようになっている。"),
  bullet("ICAO／IATA AHM 整合：機材独立な車両データ標準（AHM 950／956）が普及しつつあり、自律型プラットフォームは準拠テレメトリを発出する必要がある。"),
  bullet("自律型エアサイドのサイバーセキュリティ：ENISA、TSA、JCAB が自律型エアサイドのガイダンスを精緻化中。OT／IT 分離と OTA アップデート制御は今や調達基準の一部となっている。"),
  h2("4.3 商務・サステナビリティ ドライバー"),
  bullet("GSE-as-a-Service 商務モデル：空港・グランドハンドラーは資本支出より「ターン課金／稼働時間課金」を志向。これにはテレメトリ・SLA 規律・従量課金基盤が前提となる。"),
  bullet("電動化との重畳：自律化と eGSE（電動GSE）が同時期に到来しており、充電窓スケジューリングが新たな制約として最適化モデルを変容させる。"),
  bullet("空港のネットゼロ・コミットメント：主要ハブの大半が 2030／2035 年エアサイド・ネットゼロ目標を掲げており、自律＋電動 GSE が信頼できる遵守経路。"),
  bullet("保険・リスク移転：保険会社は自律型GSE のリスクを依然プライシング中。構造化された運用データはアンダーライター信頼を加速し、保険料を低下させる。"),
  h2("4.4 統合・データ ドライバー"),
  bullet("AODB（空港運用データベース）統合：自律型GSE は TOBT／TSAT を読み取り、自機の位置・状態を発出して初めてゲートレベルで有用となる。"),
  bullet("マルチステークホルダー間データ契約：運営者・OEM・グランドハンドラー・ANSP それぞれが同一テレメトリの異なるビューを必要とする。同意・データ共有のフレームワークは未成熟。"),
  bullet("レガシー無線ディスパッチ：多くのランプ運用が依然として音声無線で稼働している。自律型プラットフォームはディスパッチ・ツールの再構築を要求するが、これは運用全体に便益をもたらす。"),
];

const successFactors = [
  h1("5. 自律型GSE開発企業の主要成功要因"),
  p("APEX の AXLE（自動車自律走行 深掘り）と ICE（産業用フリート）プラクティス・パターン、および隣接する自律モビリティ・プログラムにおける DMTSP の実績から導出。"),
  h2("5.1 エンジニアリング・製品の成功要因"),
  bullet("ODD 規律：勝者となる OEM は、緊密かつ証跡付きの ODD（運用設計領域）を公開し、計測された V&V とともに段階的に拡張する。あらゆる気象条件・路面条件で「Level-4」を過剰主張しない。"),
  bullet("センサー冗長化＋エアサイドで信用される故障モード：マルチモーダル・センサースタック（LiDAR＋レーダー＋カメラ＋IMU）と独立故障経路。FOD・低い太陽高度・水溜まり下での「セーフ・ストップ」挙動を実証可能とする。"),
  bullet("車両バス＋テレメトリの習熟：CAN、J1939、OEM 固有バスへのファーストクラス統合と、無損失なクラウド・テレメトリ。テレメトリのない自律走行は安全ケースを成立させない。"),
  bullet("OTA アップデート規律：段階的ロールアウト、署名付きアップデート、決定論的ロールバック。TSA／ENISA／JCAB のエアサイド・サイバー要件と整合。"),
  bullet("ツイントラック HMI：自律運用 HMI とテレオペレーション・フォールバック HMI を、初期段階から両立させる。"),
  h2("5.2 運用・商務の成功要因"),
  bullet("初日からの A-CDM／AODB 統合：勝者は TOBT／TSAT 取り込みとイベント発出を出荷時から実装。敗者は統合をフェーズ2の課題として後送りにする。"),
  bullet("GSE-as-a-Service 商務モデル：稼働率課金（ターン単位、kWh 単位、稼働時間単位）契約は、OEM の経済性と運営者の成果を整合させる。一括売り切りは継続関係を先に潰してしまう。"),
  bullet("ハブ空港への部品事前配置：自律部品（コンピュートモジュール、LiDAR、駆動用バッテリー）は長納期。ハブ空港にて部品を事前配置する OEM ほど、ディスパッチ信頼性で先行する。"),
  bullet("サービスネットワーク密度：自律 MTBF は改善中だが、依然として高密度のフィールドサービス体制を要求する。同シフト内に技術者を派遣できる OEM がハブ案件を獲得する。"),
  bullet("混在フリートのオーケストレーション：自律型と手動機材は今後 10 年は混在運用される。ランプ・ディスパッチツールへ開放 API を公開する OEM ほど、パイロット転換が早い。"),
  h2("5.3 安全・規制・信頼の成功要因"),
  bullet("既製の安全ケース成果物：STPA、FMEA、ハザードログ、ODD トレーサブルなテスト証跡を製品同梱とし、空港ごとに場当たり的に作成しない。"),
  bullet("独立 V&V ハーネス：第三者監査済みの検証は、社内主張より早く規制当局の信頼を獲得する。特に JCAB、EASA 管轄では効果が大きい。"),
  bullet("エアサイドのサイバー姿勢：OT／IT 分離、署名済みファームウェア、セキュアブート証跡、SBOM の提示が 2026 年の調達ではほぼ必須。"),
  bullet("透明なインシデント・テレメトリ：勝者となる OEM は明確なデータ共有契約のもと、ヒヤリハットおよび介入データを運営者へ公開。信頼は積み上がり、不透明性は信頼を侵食する。"),
  h2("5.4 エコシステム・パートナーシップの成功要因"),
  bullet("航空会社グレード SLA を強制機能とする：公表 OTP（定時運航率）に紐づく SLA（例：プッシュバック・ディスパッチ信頼性 99.5%）に向けた設計が、上流のアーキテクチャを正しく駆動する。"),
  bullet("Microsoft／ハイパースケーラー連携：Fabric／Azure AI Foundry／Azure AI Agent Service は 2026 年時点でエアサイドにおいて最も規制信頼性の高いスタックである。本スタック上に構築する OEM は、運営者 IT の反対論を未然に回避できる。"),
  bullet("グランドハンドラーとの共同開発：Swissport、dnata、Menzies などは GSE の日常運用主体であり、ここでの OEM パートナーシップがフリート転換を加速する。"),
  bullet("標準化への関与：IATA AHM ワーキンググループ、ISO TC 20/SC 9、SAE G-31（航空自律化）への積極参画は、空港当局に対する長期姿勢を示す。"),
];

const deloitteFit = [
  h1("6. デロイトのケイパビリティ・フック（DMTSP × APEX）"),
  p("デロイト Microsoft プラクティス（DMTSP）は APEX フレームワークと、それを実装するエンジニアリング能力を提供する。自律型GSE案件のエンゲージメント・モデルには、定型の4ワークストリームがある。"),
  h3("ワークストリーム A — 運営者側 実装"),
  bullet("Foundation Wave：Fabric ワークスペース・トポロジー、ICE スキーマ展開、最初の 2〜3 ICE サービス稼働（典型例：FAF-01＋AaS-05＋CIR-06）。"),
  bullet("Intelligence Wave：TH（航空）の運航障害リカバリーをランプディスパッチへ統合。プラクティス横断のオブザーバビリティを整備。"),
  bullet("Optimisation Wave：複数ハブ展開、マルチハンドラー・テナンシー、ネットゼロ KPI の統合。"),
  h3("ワークストリーム B — OEM 側 製品＆テレメトリ"),
  bullet("AXLE 深掘り：ODD 定義、V&V ハーネスのスキャフォールディング、安全ケース・コンテンツの規律化。"),
  bullet("ICE-AaS-05：As-a-Service 稼働率テレメトリ実装と従量課金統合。"),
  bullet("ICE-WCP-03：稼働中フリートのテレメトリに対する保証パターン分析。フィールドからエンジニアリングへのループを閉じる。"),
  h3("ワークストリーム C — 規制・安全ケース"),
  bullet("ICE-CIR-06 実装：FAA Part 139、EASA、JCAB に整合した監査品質の証跡パイプライン。"),
  bullet("HITL 分類：あらゆる自律意思決定面でのゲート明示宣言。規制当局レビューに耐える形式。"),
  h3("ワークストリーム D — 商務モデル"),
  bullet("GSE-as-a-Service 契約のサブスクリプション価格・SLA 設計。"),
  bullet("テレメトリ裏付け型のアンダーライティングを伴う保険・リスク移転スキームの構造化。"),
  bullet("プラクティスあたりの投資レンジ：Wave 1 で 3〜8 百万米ドル、Wave 2 で 5〜12 百万米ドル、Wave 3 で 3〜6 百万米ドル。Wave 1 サービスのみで 18 ヶ月時点に累積 2〜4 倍の ROI を見込む。"),
];

const closingCV = [
  h1("7. 著者プロフィール — Keven Markham"),
  p("Specialist Master、Deloitte Microsoft Technology & Services Practice（DMTSP）所属。Microsoft プラットフォーム（Azure、Fabric、Power Platform、Copilot、Foundry、Security）で 22 年超の経験を有する。APEX フレームワーク主任アーキテクト。輸送・空港隣接領域では、複数空港にまたがる資産健全性プログラム、ランプ運用データ・アーキテクチャ、自動車（AXLE）から産業用フリート（ICE）への自律モビリティ・パターンの転用を手掛けている。"),
  h3("本件に関連する APEX 著作"),
  bullet("APEX Core（マニフェストモデル、HITL 分類、7層リファレンス・アーキテクチャ）。"),
  bullet("APEX-ICE プラクティス（フィールド資産障害対応、As-a-Service 稼働率最適化、コンプライアンス検査対応）。"),
  bullet("APEX-TH 航空サブバリアント（運航障害リカバリー・オーケストレーション、ランプ例外ルーティング・パターン）。"),
  bullet("APEX-AXLE 補完プログラム（自律走行車両の深掘りスキャフォールディング）。"),
  h3("提案書への CV 同梱について"),
  p("最新の CV は、ご依頼に従い 2026 年 5 月 4 日 EOD（米国東部時間）までに別便にて送付いたします。希望書式（デロイト グローバル標準 CV／提案固有のワンページ版のいずれか）について、受領後にご確認をお願い申し上げます。"),
  new Paragraph({ children: [new PageBreak()] }),
  h1("付録A — 参照ドキュメント"),
  bullet("APEX Solution Overview（DMTSP、APEX Core v1.2 時点の最新版、2026年4月17日）"),
  bullet("APEX Comprehensive Solutions Reference（7プラクティス・45サービスのカタログ）"),
  bullet("Transportation AHM ・ APEX & AXLE for Fleet Asset Management デック（DMTSP）"),
  bullet("AXLE-3D Factory KPIs リファレンス（DMTSP）"),
  bullet("APEX Stacked Architecture Narrated リファレンス（DMTSP）"),
  p("いずれの参照ドキュメントも DMTSP SharePoint よりご請求のうえ提供可能です。"),
];

// =====================================================================
// DOCUMENT
// =====================================================================

const doc = new Document({
  creator: "Keven Markham, DMTSP",
  title: "自律型GSE — APEX サービス・ポジショニング",
  description: "デロイト トーマツ ジャパン 自律型GSE 提案書 添付資料",
  styles: {
    default: { document: { run: { font: { name: JP_FONT, eastAsia: JP_FONT }, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: { name: JP_FONT_UI, eastAsia: JP_FONT_UI }, color: HEAD_BG },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: { name: JP_FONT_UI, eastAsia: JP_FONT_UI }, color: AZURE },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: { name: JP_FONT_UI, eastAsia: JP_FONT_UI }, color: TEAL },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
        ] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
          children: [
            jpRun("デロイト ・ DMTSP", { bold: true, size: 18, color: AZURE, ui: true }),
            jpRun("\t自律型GSE — APEX サービス・ポジショニング", { size: 18, color: "475569", ui: true }),
          ],
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: AZURE, space: 4 } },
        }),
      ]}),
    },
    footers: {
      default: new Footer({ children: [
        new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
          children: [
            jpRun("社内限り（デロイト グローバル）  ・  2026年5月1日", { size: 16, color: "94A3B8" }),
            jpRun("\tページ ", { size: 16, color: "94A3B8" }),
            new TextRun({ children: [PageNumber.CURRENT], color: "94A3B8", size: 16 }),
            jpRun(" / ", { size: 16, color: "94A3B8" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], color: "94A3B8", size: 16 }),
          ],
        }),
      ]}),
    },
    children: [
      ...cover,
      ...execSummary,
      ...aboutAPEX,
      ...serviceMapping,
      ...airportNeeds,
      ...successFactors,
      ...deloitteFit,
      ...closingCV,
    ],
  }],
});

const outDir = path.resolve(__dirname, "..", "docs", "APEX - Design and Build");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, "Autonomous-GSE-APEX-Services-Positioning-JP.docx");

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log("Wrote:", outPath);
});
