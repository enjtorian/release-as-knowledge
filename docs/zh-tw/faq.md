# 常見問題（FAQ） · Release-as-Knowledge v1

關於 R2K（**Release-as-Knowledge · 軟體發布即知識傳遞**）的常見問題。

---

## 一、概念

### Q：R2K 是什麼？

R2K（**Release-as-Knowledge**，中文：**軟體發布即知識傳遞**）是一個語義標準，把每一次軟體 release 從「不可被機器理解的 binary」升級為**結構化、可機器索引、可推理的知識物件**。

它由四個漸進採用的階段組成：

1. **LABEL · Identify**（OCI label 宣告身份）
2. **Snapshot · Trust**（OpenAPI / DB / Config / SBOM 自動收集）
3. **Diff · Understand**（跨資產 diff plugin）
4. **Insight · Share**（跨資產整合洞察）

### Q：R2K 不是 SBOM 嗎？

不是。**SBOM 是 R2K L2 的一個子集**（只負責 dependency 這一面）。R2K 的 L2 還包含 OpenAPI、DB schema、config 等，並在 L3 提供跨資產 diff 與 insight。

### Q：R2K 不是 SLSA 嗎？

不是。SLSA 解的是 **build security**（這顆 binary 是不是被信任的人在信任的環境下做出來的）。R2K 解的是 **change communication**（這次 release 改了什麼、意味著什麼）。兩者**互補**。

### Q：R2K 不就是 release notes 嗎？

不是。Release notes 是**衍生物**（人讀的描述）。R2K 是**主產品**（結構化、可被機器消費的事實 + 解讀）。Release notes 可以從 R2K 自動 render 出來，反過來不行。

### Q：R2K 是工具嗎？

R2K **不是工具**，是一個 framework + 命名 + 採用標準。CC BY 4.0 授權，不綁特定 implementation。可以有多個工具實作 R2K（CLI / SDK / collector / plugin）。

### Q：那「v1」是什麼意思？前面的版本去哪了？

`00-idea/` 下的所有 v1 / v2 草稿都視為 **draft**。這次正式對外發出的版本就是 **R2K v1**。它整合了之前草稿中的「8 原則 + 4 Level + Mode A/B」共識。

---

## 二、四階段推薦進程

### Q：為什麼要分四個階段？不能一次發一份完整的 spec 嗎？

因為**現實的團隊不會一次跨完所有東西**。R2K 模仿 SLSA tier 的設計：每一階段獨立宣告達成、獨立帶來價值。Step 1 只要 5 行 Dockerfile，Step 4 才需要規則引擎或 LLM。

### Q：Step 2 為什麼說「需要許多自動化收集」？

因為每一種資產（OpenAPI、DB schema、config、SBOM…）都有自己**已經存在**的最佳收集工具：

- OpenAPI → 你的 framework / SDK 產生器
- DB schema → Atlas、Flyway、Liquibase
- SBOM → Syft、CycloneDX
- config → 你自己的設定模板

R2K 不重做這些工具，**它規範這些工具的輸出該放在哪、長什麼樣**，這樣 L3 才能跨資產 diff。

### Q：Step 3 為什麼需要許多 diff plugin？

因為「diff」對不同資產意義不同：

- API diff = breaking change 偵測（路徑刪除、必填欄位、型別收窄）
- DB diff = migration 風險（NOT NULL 約束、index 影響、長表 ALTER）
- SBOM diff = 新增 / 升降版 / 已知 CVE 引入
- Config diff = 必填 / 棄用 / 預設值翻轉

每一種 diff 規則都可以是獨立的 plugin。R2K 提供 plugin SPI（Service Provider Interface），讓社群與 vendor 各自寫自己領域的 diff plugin，但**輸出統一遵守 `change.yaml` schema**。

### Q：Step 4 的 insight 跟 Step 3 的 diff 差在哪？

- **Diff（Step 3）= 單一資產內的變化**（API 變了什麼、DB 變了什麼）
- **Insight（Step 4）= 跨資產之間的關聯與意義**（API 拿掉 + DB rename → 同一變更面、影響面更大）

Insight 一定建立在 diff 之上，不會憑空生成。

---

## 三、AB Plan · L3 Diff 何時計算

### Q：什麼是 Mode A / Mode B？

R2K v1 對「Diff（L3）何時被計算」設計了**兩個 mode**：

- **Mode A · Pre-computed**：CI 階段算好 Change Manifest，附在 image。✅ 適合 air-gap / on-prem。
- **Mode B · On-demand**：CI 只附 L1+L2 snapshot，Diff Engine 在查詢時算。✅ 適合 SaaS / 任意組合查詢。

### Q：為什麼 v1 要同時容納兩個 mode？不能挑一個就好嗎？

因為兩種 vendor 的客戶端形態不同：

- 賣 on-prem 軟體給政府或銀行的 ISV → 客戶端不能上網，只能用 Mode A
- 跑 SaaS 或開源工具的 vendor → 任何 from→to 都可能被查，Mode B 才合理

R2K 的**第 1 原則**「Artifact 存事實，不存解讀」讓事實（L1+L2）跟解讀（L3）分開 — 事實留在 image，解讀的時機可以由 vendor 決定。

### Q：「雙模式並存」是什麼意思？

- image 內帶 Mode A 的「預設配對」manifest（air-gap 客戶能直接看）
- L2 snapshots 完整保留（讓有連線的客戶用 Mode B 重算其他組合）

實務上是**推薦做法**，但需要 CI 整合稍微複雜一點。

### Q：Mode A 的 manifest 過時怎麼辦？

Mode A 的 Change Manifest 算完就「凍」在 image，如果 diff plugin 規則升級（例如新發現的 CVE pattern），Mode A 不會自動受惠 — 需要 rebuild 一個新版本的 image。Mode B 則自動拿到最新規則。這是 trade-off 的一部分。

---

## 四、實作與整合

### Q：要改我現在的 CI/CD 嗎？

**不需要重寫**。R2K 是 additive instrumentation：

- Step 1 只是加 5 行 `LABEL`
- Step 2 是在 build 階段多跑幾個 collector，把輸出 COPY 進 image
- Step 3 是 build 階段（Mode A）或查詢階段（Mode B）跑 diff CLI

不換 framework、不換 registry、不改 deploy 流程。

### Q：跟 OpenAPI / SBOM / Atlas / Helm 有衝突嗎？

完全沒有。R2K 的設計原則之一就是「**標準優於發明**」 — 它把這些已存在的事實格式整合，不發明新格式。你已經在用 Atlas 出 schema、用 Syft 出 SBOM、用 OpenAPI generator 出 spec？很好，把它們的輸出放到 `/r2k/` 對應位置即可。

### Q：每一層需要什麼工具？怎麼驗證？

| Step | Level | 主要工具（v1 規劃）| 驗證 |
|---|---|---|---|
| 1 | Identify | `r2k label`、`docker inspect` | `r2k validate identity` |
| 2 | Trust | `r2k snapshot`（OpenAPI / DB / Config / SBOM collector）| `r2k validate state` |
| 3 | Understand | `r2k diff A B`（diff plugin SPI）| `r2k validate change` |
| 4 | Share | `r2k insight`、`r2k certify` | `r2k certify` |

### Q：badge 怎麼運作？

```bash
r2k certify your-image:tag --output badge.json
```

輸出包含 level（1/2/3/4）、mode（A/B/A+B）、合規狀態與檢查時間。可以掛到 README 或內部 dashboard。

### Q：可以為內部 / 私有資產寫自家的 diff plugin 嗎？

可以。R2K 提供 plugin SPI，輸出遵守 `change.yaml` schema 即可。建議命名 prefix 用 `x-yourco-*`，避免跟未來的標準 plugin 衝突。

---

## 五、定位與比較

### Q：R2K 跟 Git 的關係？

Git 講「**code 改了什麼**」，R2K 講「**系統改了什麼，意味著什麼**」。R2K 的第 1 原則就是模仿 git 的設計：commit 存 snapshot、diff 是計算的；R2K 對 OCI image 做 git 對 source code 做的事。

### Q：R2K 跟 Observability（Datadog / Grafana）的關係？

Observability 講「**現在發生什麼**」，R2K 講「**版本之間改了什麼**」。Observability 是**運行時真相**，R2K 是**發布時真相**。

### Q：R2K 在 LLM / AI 時代的角色？

LLM 開始直接消費 release（incident copilot、release reviewer、debug agent…），它們需要結構化的 context，而不是非結構化的 release note 或 chat log。R2K 提供的就是「**release 的 machine-readable 語義表達**」 — 讓 AI 能 deterministic 地推理「哪個 release 引入哪個風險、影響哪個服務」。

---

## 六、加入

### Q：怎麼加入 R2K？

| | 方式 | 行動 |
|---|---|---|
| ① | **簽名 Sign** | 把名字加進 SIGNATURES.md |
| ② | **採用 Adopt** | 從 Step 1 開始，掛 R2K Level 1 badge |
| ③ | **分享 Share** | 部落格、議程、實際案例 |
| ④ | **擴充 Extend** | 提案 vendor-specific extensions（`x-yourco-*`）或 diff plugin |
| ⑤ | **挑戰 Challenge** | 指出哪裡錯，我們公開更新 |

### Q：授權是？

CC BY 4.0。可分享、改作、商用，唯一要求是標明來源。
