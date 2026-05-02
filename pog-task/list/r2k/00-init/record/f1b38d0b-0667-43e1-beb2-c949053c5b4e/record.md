# Record · R2K v1 繁中文件改寫與 Manifesto 重新落位

- Task ID: `f1b38d0b-0667-43e1-beb2-c949053c5b4e`
- Project / Module: `r2k / 00-init`
- Owner: `claude-opus-4-7`
- Status: `in_review`
- Started: `2026-05-03`
- Latest update: `2026-05-03`

---

## 1. Original Prompt

> auto mode , 不要詢問 持續執行
>
> Step 4 本次任務：
> 我所想像的 R2K：引導目前 release 主要以 binary 釋出為主的模式改良成不同步驟的推薦進程
>   1. docker label
>   2. 保存重要的資產 ex openapi.json, db schema, config setting env, SBOM 等等的資訊（這步驟需要許多自動化收集）
>   3. 提出 diff for 不同的資產，然後可以提供簡易的洞察（這步驟需要許多 diff plugin）
>   4. 提供 insights, 洞察分析（就會需要各種對於 3 的分析 呈現整合）
> 在不同層可以提供對應的工具與 valid。
> 把上述的理念視為重點，優化語句融入到目標的文件中。
> 注意：之前的演進版本都視為 draft，目前調整的版本就是 v1，所以就是針對 diff 有 AB plan。
>
> 閱讀 00-idea/r2k-v2/manifesto/R2K-Manifesto-en.md
> 閱讀 00-idea/r2k-github-repo/site/index.html
> 閱讀 00-idea/chatgpt/chatgpt-temp-6.md, chatgpt-temp-7.md
>
> 目標：
> 改寫 README.zh-tw.md 撰寫完整的介紹
> 改寫 docs/zh-tw/index.md 撰寫完整的介紹, faq.md, glossary.md, quickstart.md
> 重寫 Manifesto 放置在 docs/ 下 設計放置的位置
> 修改 AUTHORS.zh-tw.md
> 以繁體中文版為主

---

## 2. 任務目標

把原本仍掛著「POG Task」殘影的繁體中文入口（README.zh-tw、docs/zh-tw、AUTHORS.zh-tw）整理成一份**真正以 R2K v1 為核心**的文件集。

要傳達的核心理念：

> R2K = 把「以 binary 為主的 release」**升級為「結構化的知識傳遞」**，並提供四階段推薦進程：
>
> 1. **Docker LABEL** — Identity（身份）
> 2. **重要資產自動收集** — State（OpenAPI / DB schema / config & env / SBOM）
> 3. **跨資產 diff 與簡易洞察** — Change（diff plugin 生態）
> 4. **跨資產 insights 與分析整合** — Understand / Share（洞察推理）
>
> 每一層都可獨立宣告達成、都有對應工具與驗證機制；對 L3 的 diff 計算則設計 **Mode A（pre-computed）/ Mode B（on-demand）** 的 AB plan。

之前所有 v1/v2 的 Manifesto 草稿視為 **draft**；本次落地的版本是**正式 v1**。

---

## 3. Implementation Plan

### Phase 1 · Context 摸透
- ✅ 讀 `00-idea/r2k-v2/manifesto/R2K-Manifesto-en.md` 與 `R2K-Manifesto-zh.md`
- ✅ 掃 `00-idea/r2k-github-repo/site/index.html` 取站點敘事與標語節奏
- ✅ 讀 `00-idea/chatgpt/chatgpt-temp-6.md`、`chatgpt-temp-7.md`
- ✅ 讀現有 `README.*`, `docs/zh-tw/*`, `AUTHORS.zh-tw.md`, `mkdocs.yml`

### Phase 2 · 任務骨架
- ✅ 建立 `pog-task/list/r2k/00-init/r2k-v1-繁中文件改寫.yaml`
- ✅ 建立本份 `record.md`
- ✅ commit：`docs(r2k): bootstrap r2k/00-init task & record`

### Phase 3 · 文件改寫（每段 commit 一次）
- ✅ `README.zh-tw.md` — 全篇換成 R2K v1 敘事（commit `8ae9beb`）
- ✅ `docs/zh-tw/index.md` — 完整首頁（commit `2673d3f`）
- ✅ `docs/zh-tw/quickstart.md` — 對齊四階段（commit `2673d3f`）
- ✅ `docs/zh-tw/faq.md` + `docs/zh-tw/glossary.md` — 核心 QA 與術語（commit `2673d3f`）
- ✅ `docs/zh-tw/manifesto.md` + `docs/manifesto.md` — Manifesto v1 中英（commit `1e13369`）
- ✅ `AUTHORS.zh-tw.md` — 改寫成 R2K 觀察者敘事（commit `4770871`）
- ✅ `mkdocs.yml` — 對齊新導覽（commit `4770871`）

### Phase 4 · 校驗 & 收尾
- ✅ `python3 pog-task/pog-task.py` 校驗 — `[OK] r2k-v1-繁中文件改寫.yaml`、`[OK] 初始化系統任務.yaml`，0 errors
- ✅ task `status` → `in_review`、補 walkthrough 與 actual_hours

---

## 4. 關鍵設計決策

### D1. Manifesto 放置位置

> 中文版：`docs/zh-tw/manifesto.md`
> 英文版：`docs/manifesto.md`

理由：mkdocs 已經有 `docs/`（英文）與 `docs/zh-tw/`（繁中）並列的習慣，Manifesto 是入口級文件，與 `index.md` 平級而非 nested 在 `about/` 之類的子目錄，這樣 `mkdocs.yml` 導覽才會在最上層醒目地出現「Manifesto」入口。

### D2. v1/v2 的對應

- 過去的 Manifesto v1 / v2 草稿（在 `00-idea/r2k-v2/manifesto/`）都視為 **drafts**。
- 本次發出的版本 = **R2K Manifesto v1**（正式版）。
- 內容上整合 v2 草稿的「8 原則 + 4 Level + Mode A/B」，因為它們已經是設計上的最終共識。
- 對 L3 計算的 Mode A / Mode B 在文件中明確標示為 **v1 AB plan**。

### D3. 四階段推薦進程的命名統一

| 階段 | 對應 R2K Level | 名稱（zh） | 名稱（en） | 動詞 |
|---|---|---|---|---|
| 1 | L1 | 身份 | Identify | LABEL |
| 2 | L2 | 信任 | Trust | Snapshot |
| 3 | L3 | 理解 | Understand | Diff |
| 4 | L4 | 分享 | Share | Insight / Distribute |

文件全篇以這 4 個動詞作為段落主節拍，避免讀者每次切到不同文件看到不同說法。

### D4. AB plan 的呈現方式

- **Mode A · 預先計算**：CI 算好 Change Manifest 隨 image 一起發。適合 air-gap / on-prem ISV。
- **Mode B · 即時計算**：image 只帶 L1+L2 snapshot，Diff Engine 接到查詢時才算。適合 SaaS / 開源 / 任意 from→to 查詢。
- 文件中以「同一份 L1+L2 facts，兩種 L3 計算時機」描述，避免被誤解為「兩個不同產品」。

---

## 5. 相關參考文件

- `00-idea/r2k-v2/manifesto/R2K-Manifesto-en.md`、`R2K-Manifesto-zh.md`
- `00-idea/r2k-v2/ARCHITECTURE-SPEC-v0.3.md`、`MIGRATION-v1-to-v2.md`
- `00-idea/r2k-github-repo/site/index.html`
- `00-idea/chatgpt/chatgpt-temp-6.md`、`chatgpt-temp-7.md`
- 既有 `docs/zh-tw/*`、`README.*`、`AUTHORS.*`

---

## 6. Walkthrough（執行紀錄）

> 執行段落結束後逐段補上，並以 commit hash 為憑。

### 6.1 Bootstrap · `f1a4366`
建立 `pog-task/list/r2k/00-init/` 目錄、YAML、record.md，認領任務並寫入 implementation plan。pog-task validator 一次通過。

### 6.2 README.zh-tw 改寫 · `8ae9beb`
全文重寫為 R2K v1 入口：

- 開頭直接以 ASCII 流程圖呈現「Step 1 LABEL → Step 2 Snapshot → Step 3 Diff → Step 4 Insight」四階段
- 每階段段落明確帶到「需要的支撐」（5 行 Dockerfile / collector / diff plugin / insight 框架）
- 拉出獨立 section 講 v1 的 AB plan 與 Mode A/B trade-off matrix
- 補上 R2K **不是什麼** 的清單（SBOM / SLSA / release notes / 工具）
- 結尾掛上 docs/zh-tw 與 Manifesto 的導引

### 6.3 docs/zh-tw 改寫 · `2673d3f`
四份文件統一以「四階段 → 4 Level → AB plan」為主節拍：

- `index.md`：完整入口頁，含一句話定位、為何需要、四階段詳解、AB plan、與既有標準的關係
- `quickstart.md`：以 Step 1→4 的順序拆出可漸進採用的指引；每階段都附 collector/CLI 範例與 `r2k validate` 指令；給出推薦導入時間表
- `faq.md`：六大段（概念、四階段、AB plan、實作整合、定位比較、加入），重點放在「跟 SBOM/SLSA/OpenAPI/Git/Observability 的差異」
- `glossary.md`：定義四階段、四 Level、Mode A/B、`/r2k/*` 結構化檔案、collector / diff plugin / Plugin SPI / Vendor Extension 等 v1 必備術語

### 6.4 Manifesto 落地 · `1e13369`
- **位置決策**：`docs/manifesto.md`（en）與 `docs/zh-tw/manifesto.md`（zh），與各自的 `index.md` 平級。理由：mkdocs 已經採用 `docs/`（en）與 `docs/zh-tw/`（zh）並列的習慣，Manifesto 是入口級文件，平級擺放才能在 `nav` 最上層出現。
- **內容重整**：把 `00-idea/r2k-v2/manifesto/R2K-Manifesto-zh.md` 與 `R2K-Manifesto-en.md` 整合為**正式 v1**；前面所有版本標記為 draft（保留在 `00-idea/`）；明確標注「Step / Level / 動詞」對齊表，讓 Manifesto 與 quickstart / index 的敘述完全同步。

### 6.5 AUTHORS 改寫 + mkdocs 導覽 · `4770871`
- `AUTHORS.zh-tw.md`：把過去 POG Task 觀察者敘事改寫為 R2K 觀察者敘事；補上「四階段推薦進程」「Manifesto 與 AB plan」「規格與文件」三類具體貢獻；保留「不是發明，而是為一個遲來的結構層命名」的核心句；引用區改為 R2K BibTeX。
- `mkdocs.yml`：site name / description / url / repo 全面換成 R2K；`nav` 在英文與繁中區段都加上 `Manifesto` 入口（en 用 `manifesto.md`、zh 用 `zh-tw/manifesto.md`）；i18n 連結改為 `/r2k/`。

### 6.8 quickstart Step 1 / Step 2 標籤與 index.yaml 設計
依用戶指示再次補強 quickstart：

**Step 1 · L1 Identify**
- 拆成「OCI 標準 label（`org.opencontainers.image.*`）」與「R2K 專屬 label（`dev.r2k-ai.*`）」兩組
- 對 OCI 標準 label 補完整 11 個欄位的中文說明表（title / description / version / revision / created / source / url / documentation / vendor / licenses / authors）
- 對 R2K 專屬 label 補完 9 個欄位的中文說明表（version / level / commit / build-time / repo / snapshot.path / snapshot.index / diff.mode / diff.from / spec.url），並標註必填 / 選填
- build 與驗證指令同步補上 `--build-arg VERSION` 與「OCI 工具 vs R2K CLI」雙路驗證

**Step 2 · L2 Trust**
- 新增 `/r2k/index.yaml` 作為 snapshot 的入口清單
  - schema：`r2k.dev/index/v1`
  - 結構：`image.{ref,digest,oci_labels}` / `r2k.{spec_version,level,diff_mode}` / `assets[].{id,type,path,schema,media_type,sha256,collector}` / `extensions[]`
  - 與 OCI manifest 與 CycloneDX bom-ref 對齊
  - 必填 / 選填欄位表
  - 設計原則：對齊 Manifesto 第 1 原則，**只記事實**
- collector 範例補上 `r2k snapshot index ...` 一鍵生成
- L2 升級時的 label：`dev.r2k-ai.level=2` + `snapshot.path` + `snapshot.index`，附說明表
- 驗證補上 `r2k validate snapshot --check-hashes`

**Step 3 · L3 Mode A**
- Mode A 範例 label 從 2 行擴充為 4 行：`level` / `diff.mode` / `diff.from` / `diff.path`，並附說明表

**glossary.md**
- L1 條目改寫為兩組 label 並列
- 新增 `/r2k/index.yaml` 條目

### 6.9 移除演進史 + SIGNATURES + 英文版本對齊

依用戶指示一次處理三件事：

**(1) Manifesto 移除 v1/v2 演進敘事**
- `docs/zh-tw/manifesto.md` 與 `docs/manifesto.md` 同步刪除「v1 收斂了過去的所有 v1/v2 草稿」這段 caption
- 同步刪除「演進歷史 / Version history」整個段落
- 對外文件不再揭露 draft v1 / draft v2 的內部歷史，只保留正式 v1

**(2) SIGNATURES.md 落地至 repo 根目錄**
- 內容衍生自 `00-idea/r2k-github-repo/SIGNATURES.md`
- 拿掉「Past Challengers」中 v1→v2 的內部過渡敘事，改為純粹的「Challengers」段落
- 中英並陳：英文段在前、繁中段在後（與 README/AUTHORS 雙語格式一致）

**(3) 依繁中版本撰寫 en 文件**
- `README.md` — 對應 `README.zh-tw.md`
- `AUTHORS.md` — 對應 `AUTHORS.zh-tw.md`
- `docs/index.md` — 對應 `docs/zh-tw/index.md`
- `docs/quickstart.md` — 對應 `docs/zh-tw/quickstart.md`（含完整兩組 label 表 + `/r2k/index.yaml` schema + Step 3 Mode A label 表）
- `docs/faq.md` — 對應 `docs/zh-tw/faq.md`
- `docs/glossary.md` — 對應 `docs/zh-tw/glossary.md`

英文版徹底取代原本仍是 POG Task 殘留內容的 4 份文件。

### 6.7 OCI label namespace 調整
依用戶指示，把所有 OCI label namespace 由 `org.r2k.*` 改為 `dev.r2k-ai.*`，覆蓋：

- `README.zh-tw.md`（4 行 LABEL）
- `docs/zh-tw/index.md`（4 行 LABEL）
- `docs/zh-tw/quickstart.md`（5 行 L1 + 1 行 L2 + 2 行 L3 共 8 處）
- `docs/zh-tw/glossary.md`（術語表中的 `dev.r2k-ai.*` 描述）

`00-idea/` 與 `pog-task/list/` 內的歷史 / 任務檔不動（保留設計史）。

### 6.6 校驗 & 收尾
- `python3 pog-task/pog-task.py` 通過（`Total Valid: 2, Total Errors: 0`）
- `status` 由 `in_progress` → `in_review`；checklist 全部完成
- `actual_hours` 設為 4
- 在 `history` 補上 5 筆 progress 紀錄（對應 5 個 commit）

---

## 7. 產出物（Artifacts）

- `README.zh-tw.md`
- `docs/zh-tw/{index,quickstart,faq,glossary,manifesto}.md`
- `docs/manifesto.md`
- `AUTHORS.zh-tw.md`
- `mkdocs.yml`（導覽更新）
- 本任務 YAML 與 record.md
