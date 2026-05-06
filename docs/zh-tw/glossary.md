# 術語表（Glossary） · Release-as-Knowledge v1

R2K（**Release-as-Knowledge · 軟體發布即知識傳遞**）規格中所使用術語的綜合定義。

---

## 一、最上位概念

### R2K（Release-as-Knowledge · 軟體發布即知識傳遞）
一個語義標準，把每一次 release 從「不可被機器理解的 binary」升級為**結構化、可機器索引、可推理的知識物件**。R2K v1 採用「四階段推薦進程」（LABEL → Snapshot → Diff → Insight），對應 4 個 Level，每一層可獨立宣告達成。

> 「軟體發布即知識傳遞」是 R2K 的中文正式名稱，貫穿整份規格的核心主張。

### 四階段推薦進程（4-Step Adoption Path）
R2K v1 的核心採用模型：

1. **Step 1 · LABEL（L1 Identify）** — OCI label 宣告身份
2. **Step 2 · Snapshot（L2 Trust）** — OpenAPI / DB / Config / SBOM 自動收集
3. **Step 3 · Diff（L3 Understand）** — 跨資產 diff plugin
4. **Step 4 · Insight（L3+/L4 Share）** — 跨資產整合洞察

每一步都可獨立宣告達成、有對應工具與驗證。

### Release（在 R2K 語義下）
不是「一個 image」，而是 `Identity + State + ChangeSet` 的**結構化知識物件**。Image 在 R2K 中是 carrier（承載媒介），不是 model（模型本身）。

### Manifesto v1
R2K 的設計哲學陳述，包含 8 條原則、4 個 Level、Mode A/B 雙模式。位於 [docs/zh-tw/manifesto.md](./manifesto.md)。

---

## 二、四個 Level

### L1 · Identity（身份）
事實層。透過兩組 OCI label 宣告 release 的身份：

- **OCI 標準 label**（`org.opencontainers.image.*`）— 由 [OCI Image Spec annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md) 預先定義，所有 container 工具原生支援（`title`、`version`、`revision`、`created`、`source`、`licenses`、`vendor` 等）。
- **R2K 專屬 label**（`com.releaseasknowledge.*`）— R2K 規格自己的 namespace（`version`、`level`、`commit`、`build-time`、`repo`、`snapshot.path`、`snapshot.index`、`diff.mode`、`diff.from` 等）。

R2K 不重新定義 OCI 已有的欄位，兩組同時掛即可。
**驗證**：`r2k validate identity`。

### L2 · Trust（信任）
事實層。把每次 release 都會用到的事實 dump 進 image 的 `/r2k/`：

- `/r2k/api/openapi.json`
- `/r2k/db/schema.sql`
- `/r2k/config/env.json`
- `/r2k/sbom/sbom.json`
- `/r2k/runtime/manifest.yaml`
- `/r2k/meta/manifest.json`

**驗證**：`r2k validate state`。

### L3 · Understand（理解）
**解讀層**（不是事實層）。對兩個 release 的 L2 snapshots 做跨資產 diff，產出統一的 `change.yaml`。
L3 有 **AB plan**（見下方 Mode A / Mode B）。
**驗證**：`r2k validate change`。

### L4 · Share（分享）
社會層。把 L3 的解讀跨組織共享：badge、registry、release intelligence graph。
**驗證 / 認證**：`r2k certify`。

---

## 三、L3 的 AB Plan

### Mode A · Pre-computed
CI 階段就把 Change Manifest 算好，附在 image 上一起發。客戶端不需要 Diff Engine 服務。✅ 適合 air-gap / on-prem ISV。

### Mode B · On-demand
CI 只附 L1+L2 snapshot，Diff Engine 在查詢時才即時計算。任意 from→to 都能查。✅ 適合 SaaS / connected enterprise / 開源工具。

### 雙模式並存
Image 內帶 Mode A 的「預設配對」manifest，L2 snapshots 完整保留以允許 Mode B 重算其他組合。實務推薦做法。

---

## 四、結構化檔案

### `/r2k/index.yaml`
**L2 snapshot 入口清單**。列出 image 內所有 R2K 資產（path、schema、sha256、collector），是下游讀 R2K snapshot 的**第一站**。
schema 為 `releaseasknowledge.com/index/v1`，欄位包含 `image.{ref,digest}`、`r2k.{spec_version,level,diff_mode}`、`assets[]`、`extensions[]`。
與 OCI 的 `manifest.json`、CycloneDX 的 `bom-ref` 表角色相同 — **只記事實**（path / hash / schema），不記解讀。

### `/r2k/meta/manifest.json`
身份元資料檔（L1）。包含 image tag、commit、branch、build time、R2K 規格版本。

### `/r2k/api/openapi.json`
OpenAPI 規格快照（L2）。由 framework / SDK 產生器在 build 時 dump。

### `/r2k/db/schema.sql`
DB schema 快照（L2）。由 Atlas / Flyway / Liquibase 等工具匯出。

### `/r2k/config/env.json`
config / env 模板（L2）。服務設定模板序列化結果。

### `/r2k/sbom/sbom.json`
軟體物料清單（L2）。CycloneDX 或 SPDX 格式，Syft 等工具產生。

### `/r2k/runtime/manifest.yaml`
Runtime 部署清單（L2）。Helm / K8s manifest。

### `change.yaml`
跨資產 diff 結果（L3）。統一 schema：

```yaml
version: 1
from: <image-A>
to:   <image-B>
changes:
  - type: api | db | config | dependency | runtime
    plugin: <plugin-name>
    action: added | removed | modified | migration | upgraded | downgraded
    target: <string>
    severity: low | medium | high | critical
    detail: { ... }
```

### `badge.json`
認證輸出（L4）。包含 level、mode（A / B / A+B）、合規狀態、檢查時間。

---

## 五、工具與機制

### Collector（資產收集器）
在 build 階段把單一資產 dump 進 `/r2k/` 對應位置的工具。R2K 不發明 collector，**整合既有工具**（Atlas、Syft、OpenAPI generator…）。

### Diff Plugin
針對單一資產類別計算 diff 的外掛。透過 R2K 提供的 plugin SPI 註冊，輸出統一遵守 `change.yaml` schema。
範例：`r2k-diff-openapi`、`r2k-diff-dbschema`、`r2k-diff-sbom`、`r2k-diff-config`。

### Diff Engine
執行 diff plugin 的 runtime。Mode A 中由 CI 觸發，Mode B 中由查詢端觸發。

### Insight Framework
L3+ / L4 的外掛框架。把多個 diff 結果跨資產關聯，產出風險洞察。可接 LLM、規則引擎、policy as code。

### Plugin SPI（Service Provider Interface）
R2K 為 diff plugin 與 insight 模組提供的擴充介面。
輸入：`/r2k/` snapshot 或 `change.yaml`。
輸出：遵守 R2K schema 的結構化結果。

### Vendor Extension（`x-yourco-*`）
廠商或團隊可在 R2K schema 上加自訂欄位，命名 prefix 為 `x-yourco-*`，避免與未來標準衝突。

---

## 六、設計哲學常用詞

### Facts vs Intelligence（第 1 原則）
- **Facts**（事實）：L1 LABEL + L2 snapshot，留在 image
- **Intelligence**（解讀）：L3 Change Manifest + L4 insight，從事實 derive

類比 git：commit 存 snapshot（fact），diff 是計算的（intelligence）。
類比 SBOM：存元件清單（fact），vulnerability scan 是計算的（intelligence）。

### Layered by Query Frequency（第 6 原則）
依查詢頻率分層：

- 90% 高頻輕查詢 → L1 LABEL（~50ms）
- 10% 低頻重查詢 → L2 snapshot（~300ms）
- 1% 完整深度查詢 → L3 Change Manifest

### Compatible with Existing Pipelines（第 7 原則）
不要求重寫 CI/CD、不換 registry、不換 framework。R2K 是 additive instrumentation，可漸進採用。

### Manifests are the Lingua Franca（第 8 原則）
結構化 yaml/json 是跨工具、跨組織、跨人機可讀性的橋樑。

---

## 七、R2K 不是什麼

| 詞 | R2K 與它的關係 |
|---|---|
| SBOM | **是 R2K L2 的子集**（只負責 dependency） |
| SLSA | **互補** — SLSA 解 build security，R2K 解 change communication |
| Release notes | R2K 的**衍生物**（人讀的描述），不是同一層 |
| OpenAPI | **是 R2K L2 的一部分**，並透過 diff plugin 進入 L3 |
| Git | R2K 對 OCI image 做 git 對 source code 做的事，但**不重做 git** |
| Docker / OCI | image 是 R2K 的 **carrier**，不是 model |
| Datadog / Grafana | **互補** — observability 是運行時真相，R2K 是發布時真相 |
| 工具 / 產品 | R2K **不是工具**，是 framework + 命名 + 採用標準 |
