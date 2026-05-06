# Release-as-Knowledge（R2K）· 軟體發布即知識傳遞

![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)
![Version](https://img.shields.io/badge/spec-v1-2874A6.svg)
![Status](https://img.shields.io/badge/status-public%20draft-B7791F.svg)

> 把每一次 release 從「丟一個 binary」升級成「一次結構化、可機器索引、可回溯的知識傳遞」。
> R2K 中文正式名稱 ──「**軟體發布即知識傳遞**」。

🌐 **網站**: <https://enjtorian.github.io/release-as-knowledge>
📜 **Manifesto**: [docs/zh-tw/manifesto.md](./docs/zh-tw/manifesto.md) ・ [English](./docs/manifesto.md)
🇬🇧 **English README**: [README.md](./README.md)

---

## 為什麼需要 R2K？

過去十年，我們把「**怎麼把程式碼送出去**」管道化得很乾淨：CI/CD、容器、GitOps、SBOM、Observability，每一塊都有成熟的工具。

但有一件事從來沒被標準化：

> ❌ **「這個 release 改了什麼，又意味著什麼？」**

這個問題的答案目前散落在 PR description、Slack thread、工程師腦袋、release note 草稿裡。下游的人 — 客戶端的 SRE、support engineer、合規與稽核 — 必須從這些斷裂的痕跡中拼湊。

R2K 認為：**release 應該是一次知識傳遞，不只是一個 binary 移交**。

---

## R2K 的四階段推薦進程（v1）

R2K 不要求你一次性導入所有東西，而是一條**漸進採用**的路徑。它對應到 4 個 Level，每一階段都可以**獨立宣告達成**：

```text
  Step 1                Step 2                  Step 3                  Step 4
┌─────────┐          ┌─────────────┐         ┌──────────────┐        ┌──────────────┐
│ LABEL   │   →      │ Snapshot    │   →     │ Diff         │   →    │ Insight      │
│ L1      │          │ L2          │         │ L3           │        │ L3+ / L4     │
│ Identify│          │ Trust       │         │ Understand   │        │ Share        │
└─────────┘          └─────────────┘         └──────────────┘        └──────────────┘
   身份               資產自動收集              跨資產 diff             跨資產整合洞察
   (5 行 Dockerfile)  (OpenAPI/DB/Config/SBOM) (diff plugin 生態)      (insight & 風險推理)
```

### Step 1 · Docker LABEL（L1 · Identify）

在 image 上打 OCI label，宣告「這顆 image 是誰、由哪個 commit 建出、走了哪條 R2K 規格」。

```dockerfile
LABEL com.releaseasknowledge.version="1.0"
LABEL com.releaseasknowledge.commit="$COMMIT_SHA"
LABEL com.releaseasknowledge.build-time="$BUILD_TIME"
LABEL com.releaseasknowledge.branch="${GIT_BRANCH}"
LABEL com.releaseasknowledge.tag="${GIT_TAG}"
LABEL com.releaseasknowledge.level="1"
```

只要 5 行 Dockerfile 就能達到。**任何人 `docker inspect` 就能拿到事實**，不需要新工具、不需要改 registry。

### Step 2 · 重要資產自動收集（L2 · Trust）

把每個 release 都會用到的「**事實**」收集成 snapshot，跟 image 一起發：

| 資產 | 來源 | 自動化方式 |
|---|---|---|
| `api/openapi.json` | API runtime / SDK 產生器 | build 時 dump |
| `db/schema.sql` | migration 工具（Atlas、Flyway…）| build 時匯出 |
| `config/env.json` | 服務設定模板 | build 時序列化 |
| `sbom/sbom.json` | Syft / CycloneDX | build 時掃描 |
| `runtime/manifest.yaml` | Helm / K8s manifest | build 時複製 |

這一步**需要許多自動化收集器**（collector）。R2K 規範這些檔案的擺放位置與格式，但不綁定產生它們的工具。

### Step 3 · 跨資產 diff 與簡易洞察（L3 · Understand）

當你有兩個 release 的 L2 snapshot，就能對它們做 **跨資產 diff**：

- API：哪個 endpoint 被刪除了？哪個 query param 變必填？
- DB：哪一條 migration 改了 NOT NULL 約束？哪個 index 被丟掉？
- Config：哪個 env 必填？哪個被棄用？
- Dependency：log4j 跳了大版本？哪些 CVE 被引入？

這一步**需要許多 diff plugin**（每一種資產有自己的 diff 規則）。R2K 把 diff 結果寫成統一的 `change.yaml`，附上 severity，下游可以照同一個 schema 消費。

### Step 4 · Insights · 跨資產的洞察分析（L3+ / L4 · Share）

單一 diff 不夠，**跨資產的關聯**才是洞察的所在：

- API 拿掉 `GET /users` ＋ DB 把 `users` 表改名 → 同一個變更面、影響面更大
- 新引入 dependency 的 CVE ＋ 該 dependency 在 OpenAPI 出現 → 對外暴露面加大
- config 的某個 toggle 預設值翻轉 ＋ 該 toggle 控制的程式路徑有 migration → 升級需排維護視窗

R2K v1 對這層提供**外掛式的 insight 框架**：你可以接 LLM、接規則引擎、接你自己團隊的 risk policy，每一份 insight 都建立在前面 3 步留下的事實之上。

---

## 每一層都可以獨立宣告 + 都有對應工具與驗證

| Step | Level | 對應工具（v1 規劃） | 驗證 |
|---|---|---|---|
| 1 | L1 Identify | `r2k label`、`docker inspect` | `r2k validate identity` |
| 2 | L2 Trust | `r2k snapshot`（OpenAPI / DB / Config / SBOM collector）| `r2k validate state` |
| 3 | L3 Understand | `r2k diff A B`（diff plugin SPI）| `r2k validate change` |
| 4 | L3+/L4 Share | `r2k insight`、`r2k explain`、registry、badge | `r2k certify` |

像 SLSA 的 tier system 一樣，**每個 Level 都可以單獨宣告達成**，沒人逼你一次跨完。

---

## v1 的 AB Plan · L3 Diff 何時計算？

R2K v1 在 L3「Diff 何時被計算」這件事上**不規定唯一答案**，而是設計了 **A/B 兩個 mode**：

### Mode A · Pre-computed（預先計算）

- CI 階段就把 Change Manifest 算好，**附在 image 上一起發**
- 客戶端不需要 Diff Engine 服務
- ✅ 適合 **air-gap / on-prem ISV**

### Mode B · On-demand（即時計算）

- CI 只附 L1 + L2 的 snapshots
- Diff Engine 在查詢時才計算，**任意 from→to 都能查**
- ✅ 適合 **SaaS / connected enterprise / 開源工具**

### 雙模式並存（推薦）

- image 內帶 Mode A 的「預設配對」manifest
- L2 snapshots 完整保留，允許 Mode B 重算任意組合

| 維度 | Mode A | Mode B | 雙模式 |
|---|---|---|---|
| Air-gap 友好 | ✅ 完美 | ❌ 需服務 | ✅ |
| 任意 from→to 查詢 | ❌ 預設綁死 | ✅ 完整 | ✅ |
| Diff 規則升級自動受惠 | ❌ 需 rebuild | ✅ 自動 | △ 部分 |
| CI 整合複雜度 | ✅ 簡單 | ✅ 簡單 | △ 中等 |
| Customer 端複雜度 | ✅ 簡單 | △ 需連線 | △ 看 path |

> **第 1 原則**「Artifact 存事實，不存解讀」讓兩種 mode 都成為合法的實踐方式 —— 因為事實留在 image，解讀可以決定**何時**才算。

---

## R2K 不是什麼

- **R2K 不是 SBOM** — SBOM 是 L2 的子集合
- **R2K 不是 SLSA** — SLSA 解 build security，R2K 解 change communication
- **R2K 不是 release notes** — release notes 是衍生物，R2K 是結構化的主產品
- **R2K 不是工具** — R2K 是 framework + 命名 + 採用標準，不綁特定 implementation

---

## 一句話定位

> Git 告訴你 code 改了什麼。
> Docker 告訴你部署了什麼。
> SBOM 告訴你裡面有什麼。
> **R2K 告訴你「系統改了什麼，以及這代表什麼意思」。**

---

## 五種加入方式

| | 方式 | 行動 |
|---|---|---|
| ① | **簽名 Sign** | 把名字加進 [SIGNATURES.md](./SIGNATURES.md) |
| ② | **採用 Adopt** | 從 Step 1 開始，掛上 R2K Level 1 badge |
| ③ | **分享 Share** | 部落格、議程、實際案例 |
| ④ | **擴充 Extend** | 提案 vendor-specific extensions（`x-yourco-*`）或 diff plugin |
| ⑤ | **挑戰 Challenge** | 指出哪裡錯，我們公開更新 |

第 ⑤ 點重要 — Manifesto 的第 1 原則就是被挑戰之後才浮現的。

---

## 文件導引

- [📜 R2K Manifesto v1（繁中）](./docs/zh-tw/manifesto.md) ・ [English](./docs/manifesto.md)
- [📘 docs/zh-tw/index.md — 完整介紹](./docs/zh-tw/index.md)
- [🚀 docs/zh-tw/quickstart.md — 5 分鐘到 Level 1](./docs/zh-tw/quickstart.md)
- [❓ docs/zh-tw/faq.md — 常見問題](./docs/zh-tw/faq.md)
- [📖 docs/zh-tw/glossary.md — 術語表](./docs/zh-tw/glossary.md)
- [👥 AUTHORS.zh-tw.md — 作者與貢獻者](./AUTHORS.zh-tw.md)

---

## License

整個 R2K 規格、Manifesto 與本文件採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh_TW)。
你可以分享、改作、商用，唯一要求是標明來源。

---

> **過去十年我們把程式碼管道化。**
> **下個十年要把程式碼以外的開發團隊知識管道化。**
>
> 這就是 R2K v1 想做的事。

*Release-as-Knowledge v1 · 2026-05 · CC BY 4.0*
