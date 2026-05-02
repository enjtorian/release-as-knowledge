# 作者與貢獻者 · Release-as-Knowledge v1

> R2K（Release-as-Knowledge · **軟體發布即知識傳遞**）

## 主要作者

**Ted Enjtorian**
*R2K 框架觀察者與主要作者*

- **LinkedIn**: <https://tw.linkedin.com/in/enjtorian>
- **GitHub**: [@enjtorian](https://github.com/enjtorian)

### 貢獻內容

- **框架構想與理論**：辨識出「軟體 release 缺少語義層」這個被多方工具切碎的核心缺口，並把它命名為 R2K（Release-as-Knowledge），中文定名為「**軟體發布即知識傳遞**」。
- **四階段推薦進程**：把 R2K 從一個概念整理成可漸進採用的 4 個 Level — LABEL → Snapshot → Diff → Insight，對齊 SLSA tier 的精神。
- **Manifesto 與 AB plan**：撰寫 R2K Manifesto v1（8 條原則），並針對 L3 計算時機提出 Mode A（pre-computed）/ Mode B（on-demand）雙模式設計。
- **規格與文件**：英文 / 繁中規格、Quickstart、FAQ、Glossary、Manifesto 等核心文件的撰寫與架構設計。

### 背景

我是一位有超過 20 年經驗的軟體系統架構師。在過去十年見證了 CI/CD、容器、SBOM、OpenAPI、Observability 各自走向成熟；但有一件事始終沒被標準化：

> **「這個 release 改了什麼？意味著什麼？」**

這個問題的答案散落在 PR description、Slack thread、release note 草稿、工程師腦袋。下游的人 — 客戶端 SRE、support、合規與稽核 — 必須從這些斷裂的痕跡中拼湊。

R2K 的設計重點不是發明新的工具，而是**為一個已經存在於每個生產系統裡、卻從未被命名的語義層命名**。它整合了既有標準（OCI、CycloneDX、OpenAPI、Atlas migration plan…），並把「事實」（L1 LABEL + L2 snapshot）與「解讀」（L3 Diff、L4 Insight）拆開 — 事實留在 image，解讀則由 vendor 依客戶端形態決定計算時機（Mode A / Mode B）。

這不是發明，而是**為一個遲來的結構層命名**。

---

## 貢獻者

R2K 是一個開放的標準倡議，歡迎社群貢獻。貢獻者將在此被表彰。

### 如何貢獻

請參閱 [README.zh-tw.md](./README.zh-tw.md) 以及五種加入方式：

| | 方式 | 行動 |
|---|---|---|
| ① | **簽名 Sign** | 把名字加進 SIGNATURES.md |
| ② | **採用 Adopt** | 從 Step 1 開始，掛 R2K Level 1 badge |
| ③ | **分享 Share** | 部落格、議程、實際案例 |
| ④ | **擴充 Extend** | 提案 vendor-specific extensions（`x-yourco-*`）或 diff plugin |
| ⑤ | **挑戰 Challenge** | 指出哪裡錯，我們公開更新 |

具體可貢獻方向：

- **規格演進**（Manifesto / RFC）
- **Diff plugin**（OpenAPI / DB schema / config / SBOM…）
- **Collector**（與既有工具整合，如 Atlas、Syft、OpenAPI generator）
- **Insight 框架擴充**（規則引擎、policy as code、LLM 連接）
- **CI / CD 整合**（GitHub Action、GitLab CI、Jenkins）
- **翻譯**（其他語言的 Manifesto / docs）
- **圖表與視覺**（架構圖、四階段進程圖、Mode A/B 對照圖）

---

## 致謝

特別鳴謝：

- 開源社群提供的靈感與回饋（OCI、CycloneDX、OpenAPI、SLSA、Atlas、Syft…）
- 提供寶貴見解的早期採用者
- 對早期草稿提出挑戰的所有人 — Manifesto 的第 1 原則就是被挑戰之後才浮現的

---

## 引用

如果您在研究或工作中使用 R2K，請引用：

```
Enjtorian, T. (2026). R2K (Release-as-Knowledge): A Semantic Layer
for Software Releases. https://github.com/enjtorian/release-as-knowledge
```

BibTeX：

```bibtex
@misc{r2k2026,
  author = {Enjtorian, Ted},
  title = {R2K (Release-as-Knowledge): A Semantic Layer for Software Releases},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/enjtorian/release-as-knowledge}},
  note = {Licensed under CC BY 4.0}
}
```

---

*本作品（R2K 規格、Manifesto、文件）採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh_TW) 授權。*
