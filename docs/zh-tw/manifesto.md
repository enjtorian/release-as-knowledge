---
title: R2K Manifesto v1 · 軟體發布即知識傳遞
description: R2K v1 的設計哲學陳述 — 8 條原則、4 個 Level、L3 的 Mode A/B 雙模式 AB plan。CC BY 4.0。
tags: [r2k, manifesto, release-as-knowledge]
keywords: R2K, Manifesto, Release-as-Knowledge, OCI, SBOM, OpenAPI
author: Ted Enjtorian
date: 2026-05
---

# Release-as-Knowledge Manifesto · v1

> **Release-as-Knowledge** · 軟體發布即知識傳遞
> 8 條原則 · 4 個 Level · Mode A/B 雙模式 · CC BY 4.0

---

## 我們相信

軟體發布應該是**一次知識傳遞，不只是一個 binary 移交**。

開發團隊在 build 一個 release 時，腦中累積了大量隱性知識：

- 哪些 API 變了、哪些是 breaking
- 哪些 DB migration 風險高、需要排維護視窗
- 哪些 config 必填、哪些被棄用
- 哪些 breaking change 會影響哪些客戶

**這些知識目前不會跟著 image 一起發布出去**。它們留在 PR description、Slack thread、工程師的記憶裡。

下游的人 — 支援工程師、客戶 DevOps、稽核者、合規團隊 — 必須從這些斷裂的痕跡中拼湊。**我們認為這個現況可以也應該被改變**。

---

## 八條原則

### 1. Artifact 存事實，不存解讀
*Artifact carries facts, not intelligence*

OCI image 該存 L1（LABEL）+ L2（snapshots：API spec、DB schema、config），這些是**事實**。
L3（Change Manifest）是**解讀**，從事實計算出來，不必烘焙進 image。

類比兩種成熟設計：
- **git**：commit 存 snapshot，diff 是計算的
- **SBOM**：存元件清單，vulnerability scan 是計算的

**R2K 對 OCI image 做 git 對 source code 做的事**：事實留在 artifact，解讀是 derive 的。

### 2. 知識隨產物發布
*Knowledge ships with the artifact*

知識不能只活在 PR description。它必須跟 image 一起傳遞，被機器索引、被非開發者消費。

### 3. 隱性轉顯性
*Implicit becomes explicit*

工程師腦中 trivial 的東西，在客戶端是地雷。R2K 強迫把這類知識結構化、可機器讀。

### 4. 標準優於發明
*Standards over invention*

OCI、CycloneDX、OpenAPI、Atlas migration plan — 業界已經跑了多年的標準。R2K 的 schema 是把這些既有標準整合，不發明新格式。

### 5. 為非開發者設計
*Designed for non-developers*

R2K 的服務對象是支援工程師、客戶 DevOps、稽核者、合規團隊 — 不是開發者本身。

### 6. 依查詢頻率分層
*Layered by query frequency*

90% 高頻輕查詢用 LABEL（~50ms）。10% 低頻重查詢用 metadata layer（~300ms）。1% 完整深度查詢用 Change Manifest。

### 7. 相容既有 pipeline
*Compatible with existing pipelines*

不要求重寫 CI/CD、不換 registry、不換 framework。從 Level 1 的 5 行 Dockerfile 改變開始，**漸進採用**。

### 8. Manifest 是共通語
*Manifests are the lingua franca*

結構化 yaml/json 是跨工具、跨組織、跨人機可讀性的橋樑。

---

## 四階段推薦進程 · 四個 Level

R2K 提供一條**漸進採用**的路徑：

| Step | Level | 名稱 | 動詞 | 性質 | 成本 | 可獨立宣告 |
|---|---|---|---|---|---|---|
| 1 | **L1** | Identify | LABEL | facts | 1-2 週 | ✓ |
| 2 | **L2** | Trust | Snapshot | facts | 2-3 週 | ✓ |
| 3 | **L3** | Understand | Diff | **intelligence** | 6-8 週 | ✓ |
| 4 | **L4** | Share | Insight / Distribute | social | 4 週 | ✓ |

- L1+L2 是**事實層** — 留在 image
- L3 是**計算層** — 從 L1+L2 derive
- L4 是**社會層** — 跨組織分享 insight

像 SLSA 的 tier system 一樣，**每個 Level 都可以單獨宣告達成**。

### 一句話總結

> **L1 = Identify · L2 = Trust · L3 = Understand · L4 = Share**

### 各層需要的支撐

- **Step 1（L1）**：OCI label，5 行 Dockerfile 起步。
- **Step 2（L2）**：**需要許多自動化收集器**（OpenAPI / DB schema / config / SBOM 各自 collector），R2K 規範擺放與 schema，不發明 collector。
- **Step 3（L3）**：**需要許多 diff plugin**，每一種資產的 diff 規則都不同。R2K 提供 plugin SPI，輸出統一的 `change.yaml`。
- **Step 4（L3+/L4）**：跨資產整合洞察。R2K 提供外掛式 insight 框架（可接 LLM、規則引擎、policy as code）。

---

## L3 的 AB Plan · 何時計算 Diff？

L3 是 derived 的 — 但「在哪一刻 derive」有兩個選項：

### Mode A · 預先計算

- CI 階段就把 Change Manifest 算好 + attach 到 image
- 客戶端不需要 Diff Engine 服務
- ✅ 適用：**air-gap on-prem ISV**

### Mode B · 即時計算

- CI 只 attach snapshots（L1+L2）
- Diff Engine 在查詢時即時計算
- 任意 from→to 組合都可查
- ✅ 適用：**SaaS / connected enterprise / 開源工具**

### 雙模式並存（推薦）

- 主 image 內帶 Mode A 預設組合 manifest
- L2 snapshots 完整保留，允許 Mode B 重算任意組合
- 兩種客戶端都能受惠

### 取捨對照表

| 維度 | Mode A | Mode B | 雙模式 |
|---|---|---|---|
| Air-gap 友好 | ✅ 完美 | ❌ 需服務 | ✅ |
| 任意 from→to 查詢 | ❌ 預設綁死 | ✅ 完整 | ✅ |
| Diff 規則升級自動受惠 | ❌ 需 rebuild | ✅ 自動 | △ 部分 |
| CI 整合複雜度 | ✅ 簡單 | ✅ 簡單 | △ 中等 |
| Customer 端複雜度 | ✅ 簡單 | △ 需連線 | △ 看 path |
| 適用 vendor 類型 | ISV / on-prem | SaaS | 中型混合 |

R2K **作為 framework 不規定哪一個** — 但**第 1 原則**（facts vs intelligence）讓兩種模式都成為合法的實踐方式。

選擇取決於你的客戶端是否能連到你的服務。

---

## 不是什麼

- **R2K 不是 SBOM**（SBOM 是 L2 的子集合）
- **R2K 不是 SLSA**（SLSA 解決 build security，R2K 解決 change communication）
- **R2K 不是 release notes**（release notes 是衍生物；R2K 是結構化的主產品）
- **R2K 不是工具**（R2K 是 framework + 命名 + 採用標準，沒有特定 implementation 綁死）

---

## 五種加入方式

| | 方式 | 行動 |
|---|---|---|
| ① | **簽名 Sign** | 把名字加進 SIGNATURES.md |
| ② | **採用 Adopt** | 從 Step 1（L1）開始，掛上 R2K Level 1 badge |
| ③ | **分享 Share** | 部落格、議程、實際案例 |
| ④ | **擴充 Extend** | 提案 vendor-specific extensions（`x-yourco-*`）或 diff plugin |
| ⑤ | **挑戰 Challenge** | 指出哪裡錯，我們公開更新 |

第 ⑤ 點重要 — Manifesto 的第 1 原則就是被挑戰之後才浮現的。
**Manifesto 是被挑戰才會精煉的東西**。

---

## License & Reproduction

整份 Manifesto 採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh_TW)。
你可以分享、改作、商用 — 唯一要求是標明來源。

---

> **過去十年我們把程式碼管道化。**
> **下個十年要把程式碼以外的開發團隊知識管道化。**
>
> 這就是 R2K v1 想做的事。

---

*Release-as-Knowledge Manifesto v1 · 2026-05 · CC BY 4.0*
