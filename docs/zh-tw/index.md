---
title: R2K v1 · 軟體發布即知識傳遞
description: R2K（Release-as-Knowledge）把每一次 release 從「丟一個 binary」升級為「結構化、可機器索引的知識傳遞」，提供 4 個漸進採用階段與 v1 AB plan。
tags: [r2k, manifesto, release, semantic-layer]
keywords: R2K, Release-as-Knowledge, OCI, SBOM, OpenAPI, change manifest, diff plugin, insight
author: Ted Enjtorian
date: 2026-05
---

# Release-as-Knowledge（R2K）

*Release-as-Knowledge 規格 v1 · 2026 年 5 月*

---

## 一句話定位

> Git 告訴你 **code 改了什麼**。Docker 告訴你 **部署了什麼**。SBOM 告訴你 **裡面有什麼**。
> **R2K 告訴你「系統改了什麼，以及這代表什麼意思」**。

R2K 是一個語義標準，把軟體發布從「不可被機器理解的 artifact」升級為**可結構化、可查詢、可推理的知識物件**。

---

## 為什麼需要它？

過去十年，把程式碼送出去（CI/CD、容器、GitOps、SBOM、Observability）已經高度標準化。
但有一件事一直沒被標準化：

> ❌ **「這個 release 改了什麼？意味著什麼？該怎麼處理？」**

這個問題的答案目前散落在：

- PR description / Slack thread / 工程師腦袋
- 半人工撰寫的 release note
- 各自為政的 SBOM、API diff、DB diff 工具

**下游的人**（客戶端 SRE、support、合規、稽核）必須從這些斷裂的痕跡中拼湊。R2K 認為這個現況**可以也應該**被改變。

---

## R2K 的四階段推薦進程

R2K 的核心動作，是把目前以「binary 釋出」為主的 release 流程，**改良成可漸進採用的四個階段**：

```text
  Step 1                Step 2                  Step 3                  Step 4
┌─────────┐          ┌─────────────┐         ┌──────────────┐        ┌──────────────┐
│ LABEL   │   →      │ Snapshot    │   →     │ Diff         │   →    │ Insight      │
│ L1      │          │ L2          │         │ L3           │        │ L3+ / L4     │
│ Identify│          │ Trust       │         │ Understand   │        │ Share        │
└─────────┘          └─────────────┘         └──────────────┘        └──────────────┘
   身份               資產自動收集              跨資產 diff             跨資產整合洞察
```

每一階段：

- **可獨立宣告達成**（像 SLSA tier）
- **有對應的工具**（CLI / collector / plugin / insight 框架）
- **有對應的驗證**（`r2k validate <layer>`）
- **可以遞延決定**何時進到下一層

### Step 1 · Docker LABEL（L1 · Identify）

**做什麼**：在 image 上掛 OCI label，宣告 release 的身份。

```dockerfile
LABEL dev.releaseasknowledge.version="1.0"
LABEL dev.releaseasknowledge.commit="$COMMIT_SHA"
LABEL dev.releaseasknowledge.build-time="$BUILD_TIME"
LABEL dev.releaseasknowledge.level="1"
```

**價值**：5 行 Dockerfile，不換 registry、不換 framework，就能讓任何人 `docker inspect` 拿到事實。
**驗證**：`r2k validate identity <image>`。

### Step 2 · 重要資產自動收集（L2 · Trust）

**做什麼**：build 階段把每次 release 都會用到的「事實」自動 dump 出來，與 image 一起發。

| 資產 | 預設位置 | 來源 / collector |
|---|---|---|
| OpenAPI 規格 | `/r2k/api/openapi.json` | API runtime 自動 dump、SDK 產生器 |
| DB schema | `/r2k/db/schema.sql` | Atlas / Flyway / Liquibase 匯出 |
| Config & env 模板 | `/r2k/config/env.json` | 服務設定模板序列化 |
| SBOM | `/r2k/sbom/sbom.json` | Syft / CycloneDX |
| Runtime manifest | `/r2k/runtime/manifest.yaml` | Helm / K8s 清單 |
| 身份元資料 | `/r2k/meta/manifest.json` | CI 注入（commit / branch / build time） |

**這一步需要許多自動化收集器（collector）**。R2K 規範**檔案位置與格式**，但不綁定產生它們的工具 — 你已經在用 Atlas、Syft、OpenAPI generator？很好，把它們的輸出放到 `/r2k/` 對應位置即可。

**驗證**：`r2k validate state <image>` — 檢查 schema、檢查必填、檢查與 L1 的一致性。

### Step 3 · 跨資產 Diff 與簡易洞察（L3 · Understand）

**做什麼**：對兩個 release 的 L2 snapshots 做**跨資產 diff**，產出統一的 `change.yaml`。

```yaml
version: 1
changes:
  - type: api
    action: removed
    target: GET /users
    severity: high

  - type: dependency
    action: added
    target: log4j-core@2.17.0
    severity: critical

  - type: db
    action: migration
    target: users_table
    severity: medium
```

**這一步需要許多 diff plugin** — 因為每一種資產的 diff 規則不同：

- `r2k-diff-openapi` — REST 的 breaking change 偵測
- `r2k-diff-dbschema` — DDL 變更與 NOT NULL / index 影響
- `r2k-diff-config` — 必填 / 棄用 / 預設值翻轉
- `r2k-diff-sbom` — 新增 / 升降版 / 已知 CVE 引入

R2K 提供 plugin SPI（Service Provider Interface）：你可以為自家內部協議寫 plugin，輸出依然遵守 `change.yaml` 的 schema，下游就能無縫消費。

**驗證**：`r2k validate change change.yaml`。

### Step 4 · Insights · 跨資產的洞察分析（L3+ / L4 · Share）

**做什麼**：把「單一 diff」拉到「跨資產關聯」與「組織內外共享」。

單一 diff 看 API、DB、SBOM 各自的變化，**insight** 看的是它們之間的因果與風險：

- API 拿掉 `GET /users` ＋ DB 把 `users` 表改名 → **同一變更面**，影響需要組合說明
- 新引入 dependency 的 CVE ＋ 該 dependency 出現在 OpenAPI handler → **對外暴露面變大**
- 某 config toggle 預設值翻轉 ＋ 該 toggle 控制的程式路徑有 migration → **升級需排維護視窗**

R2K v1 對這層提供**外掛式 insight 框架**：

- 可接 LLM（給 release 摘要 / risk 解釋）
- 可接規則引擎（policy as code）
- 可接你團隊既有的 risk policy

**所有 insight 都建立在前 3 步留下的事實之上**，不會憑空生成。

**驗證 / 認證**：`r2k certify <image>` 產出 badge（L1 / L2 / L3 / L4）。

---

## v1 的關鍵設計：AB Plan · L3 何時計算

R2K v1 對「Diff 何時被計算」這件事**不規定唯一答案**，而是設計 **A/B 兩個 mode**，由 vendor 依客戶端形態選擇：

### Mode A · Pre-computed（預先計算）

- CI 階段就把 Change Manifest 算好，**附在 image 上一起發**
- 客戶端不需要 Diff Engine 服務
- ✅ 適合 **air-gap / on-prem ISV**

### Mode B · On-demand（即時計算）

- CI 只附 L1 + L2 的 snapshots
- Diff Engine 在查詢時即時算，**任意 from→to 都能查**
- ✅ 適合 **SaaS / connected enterprise / 開源工具**

### 雙模式並存（推薦）

- image 內帶 Mode A 的「預設配對」manifest（解決 air-gap 場景）
- L2 snapshots 完整保留，允許 Mode B 重算任意組合（解決升級規則的場景）

| 維度 | Mode A | Mode B | 雙模式 |
|---|---|---|---|
| Air-gap 友好 | ✅ 完美 | ❌ 需服務 | ✅ |
| 任意 from→to 查詢 | ❌ 預設綁死 | ✅ 完整 | ✅ |
| Diff 規則升級自動受惠 | ❌ 需 rebuild | ✅ 自動 | △ 部分 |
| CI 整合複雜度 | ✅ 簡單 | ✅ 簡單 | △ 中等 |
| Customer 端複雜度 | ✅ 簡單 | △ 需連線 | △ 看 path |
| 適用 vendor 類型 | ISV / on-prem | SaaS | 中型混合 |

> 為什麼 v1 可以同時容納兩個 mode？因為 R2K 的**第 1 原則**「Artifact 存事實，不存解讀」把事實（L1 + L2）跟解讀（L3）拆開了 — 事實留在 image，解讀可以是 build 時算、也可以是查詢時算。

---

## R2K 的核心模型

```text
Release = Identity + State + ChangeSet
            ↑          ↑          ↑
            L1         L2         L3
          facts      facts    intelligence
```

| Layer | 性質 | 存在哪 | 對應動詞 |
|---|---|---|---|
| **Identity** | 事實 | OCI labels | Identify |
| **State** | 事實 | `/r2k/*` snapshots | Trust |
| **Change** | 解讀 | `change.yaml`（pre-computed 或 on-demand）| Understand |
| **Insight** | 解讀的解讀 | 外掛 / plugin / LLM | Share |

L1 + L2 是**事實層**（image 存），L3 是**計算層**（從事實 derive），L4 是**社會層**（跨組織分享 insight）。

---

## 對其他標準的關係

| Layer | 系統 | 關係 |
|---|---|---|
| code | Git | R2K 不重做 — Git 講 code change |
| artifact | Docker / OCI | R2K 不重做 — Docker 是 carrier |
| dependency | SBOM (CycloneDX / SPDX) | **是 R2K L2 的子集** |
| build security | SLSA | 互補 — SLSA 解 build security，R2K 解 change communication |
| API contract | OpenAPI | **是 R2K L2 的一部分**，並透過 diff plugin 進入 L3 |
| runtime | Datadog / Grafana | 互補 — observability 講「現在發生什麼」，R2K 講「版本之間改了什麼」 |

> R2K 不跟既有工具競爭，**它是把它們連在一起的語義層**。

---

## 從哪裡開始？

1. **5 分鐘到 Level 1** → [快速入門](./quickstart.md)
2. **理解動機與哲學** → [R2K Manifesto v1](./manifesto.md)
3. **遇到問題** → [常見問題](./faq.md)
4. **不確定名詞含義** → [術語表](./glossary.md)
5. **想把名字加進來** → [README.zh-tw.md](../../README.zh-tw.md)

---

## R2K 是 / 不是

✅ R2K **是**：

- 一份 framework + 命名 + 採用標準
- 對既有 OCI / SBOM / OpenAPI / migration 工具的**整合層**
- 漸進採用、每一層可獨立宣告
- CC BY 4.0 開放授權

❌ R2K **不是**：

- 一個產品 / 一個 SaaS
- 一套要替換你 CI/CD 的東西
- SBOM 的競品（SBOM 是 L2 子集）
- 一份你必須一次跨完才能用的東西

---

> **過去十年我們把程式碼管道化。**
> **下個十年要把程式碼以外的開發團隊知識管道化。**
>
> 這就是 R2K v1 想做的事。

*Release-as-Knowledge v1 · 2026-05 · CC BY 4.0*
