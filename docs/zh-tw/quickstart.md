# 快速入門 · Release-as-Knowledge v1

> 從「丟一個 binary」到「發一份知識」— 5 分鐘踏出 R2K（**軟體發布即知識傳遞**）第一步。

R2K 不要求你一次跨完所有東西。本指南帶你**依序通過四個階段**（Identify → Trust → Understand → Share），每一階段都可以**獨立宣告達成**並停下來，等團隊有空再往下一層走。

---

## 你會用到的概念

| 階段 | Level | 動作 | 預計時間 |
|---|---|---|---|
| Step 1 | L1 Identify | 在 image 上掛 OCI label | **5 分鐘** |
| Step 2 | L2 Trust | 自動收集 OpenAPI / DB / Config / SBOM | 半天 ~ 2 週 |
| Step 3 | L3 Understand | 對兩個 release 跑跨資產 diff | 2-4 週 |
| Step 4 | L3+/L4 Share | 接 insight 框架、發 badge | 持續演進 |

---

## Step 1 · 5 分鐘到 L1（Identify）

R2K Level 1 在 image 上掛**兩組 label**：

| 組別 | namespace | 由誰定義 | 工具支援 |
|---|---|---|---|
| **OCI 標準 label** | `org.opencontainers.image.*` | [OCI Image Spec — Annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md) | GHCR / ECR / Docker Hub UI、Trivy、Cosign、Skopeo… 全部原生支援 |
| **R2K 專屬 label** | `dev.releaseasknowledge.*` | R2K 規格 v1 | `r2k` CLI、R2K diff plugin / insight 框架 |

> 兩組同時掛，**不引入新工具的前提下**讓 image 既符合 OCI 慣例、也宣告為 R2K compliant。OCI label 餵給「現成的 container 生態」，R2K label 餵給「R2K 工具鏈」。

### 1.1 OCI 標準 label（先掛上）

OCI 已經有一份**預先定義好的 image annotation key 表**，凡是有 metadata 性質的訊息（commit、版本、source repo、license…）**優先用 OCI 標準的 key**。

| Label key | 說明 | 範例值 |
|---|---|---|
| `org.opencontainers.image.title` | 人類可讀的 image 名稱 | `my-service` |
| `org.opencontainers.image.description` | 短描述 | `Customer-facing API gateway` |
| `org.opencontainers.image.version` | 軟體版本（semver / 標籤） | `1.5.0` |
| `org.opencontainers.image.revision` | source 的 commit SHA | `${COMMIT_SHA}` |
| `org.opencontainers.image.created` | build 時間（RFC 3339） | `${BUILD_TIME}` |
| `org.opencontainers.image.source` | source repo URL | `https://github.com/your-org/your-repo` |
| `org.opencontainers.image.url` | 產品 / 服務首頁 | `https://your-product.example` |
| `org.opencontainers.image.documentation` | 文件 URL | `https://docs.your-product.example` |
| `org.opencontainers.image.vendor` | 發行組織 | `Your Org` |
| `org.opencontainers.image.licenses` | SPDX 授權表達式 | `Apache-2.0` |
| `org.opencontainers.image.authors` | 維護者聯絡 | `team@your-org.example` |

在 `Dockerfile` 末尾加上：

```dockerfile
# === OCI standard image labels ===
ARG COMMIT_SHA
ARG BUILD_TIME
ARG VERSION

LABEL org.opencontainers.image.title="my-service"
LABEL org.opencontainers.image.description="Customer-facing API gateway"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.revision="${COMMIT_SHA}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"
LABEL org.opencontainers.image.source="https://github.com/your-org/your-repo"
LABEL org.opencontainers.image.url="https://your-product.example"
LABEL org.opencontainers.image.documentation="https://docs.your-product.example"
LABEL org.opencontainers.image.vendor="Your Org"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.authors="team@your-org.example"
```

> 提示：你已經在用某些 OCI label？很好，**不要重複造輪子**。R2K 不重新定義這些欄位，下面 R2K 專屬 label 只補足 OCI 沒涵蓋的 R2K 特有資訊。

### 1.2 R2K 專屬 label（再加上）

`dev.releaseasknowledge.*` 這組只負責「R2K 規格自己的事」 — 這顆 image 跟著哪個 R2K 規格走、宣告達到哪一層、L3 用哪個 mode 等。

| Label key | 必填? | 說明 | 範例值 |
|---|:-:|---|---|
| `dev.releaseasknowledge.version` | ✅ | 這顆 image 遵循的 **R2K 規格版本** | `1.0` |
| `dev.releaseasknowledge.level` | ✅ | 自我宣告達到的 R2K Level（`1` / `2` / `3` / `4`） | `1` |
| `dev.releaseasknowledge.commit` | ✅ | source commit SHA（與 `org.opencontainers.image.revision` 同值，但保留給 R2K 工具直接查） | `${COMMIT_SHA}` |
| `dev.releaseasknowledge.build-time` | ✅ | R2K manifest 的 build 時間（RFC 3339） | `${BUILD_TIME}` |
| `dev.releaseasknowledge.repo` | ◯ | source repo URL（diff / insight 抓上下文用） | `https://github.com/your-org/your-repo` |
| `dev.releaseasknowledge.snapshot.path` | ◯ | L2 snapshot 在 image 內的路徑（預設 `/r2k`） | `/r2k` |
| `dev.releaseasknowledge.diff.mode` | ◯ | L3 diff 計算時機：`A` / `B` / `A+B`（見 Step 3） | `A+B` |
| `dev.releaseasknowledge.diff.from` | ◯ | Mode A 預先計算所對照的 base image | `your-image:v1.4.0` |
| `dev.releaseasknowledge.spec.url` | ◯ | 你採用的 R2K 規格文件 URL | `https://releaseasknowledge.dev/spec/v1` |

> ✅ **必填**＝Level 1 的最低門檻；◯＝隨 Level 提升再補。
> `level` 隨 Step 2 / 3 進展可被覆寫成 `2` / `3`（後 LABEL 蓋前 LABEL）。

把 R2K 專屬 label 接在 OCI label 後面：

```dockerfile
# === R2K Level 1 · Identity ===
LABEL dev.releaseasknowledge.version="1.0"
LABEL dev.releaseasknowledge.level="1"
LABEL dev.releaseasknowledge.commit="${COMMIT_SHA}"
LABEL dev.releaseasknowledge.build-time="${BUILD_TIME}"
LABEL dev.releaseasknowledge.repo="https://github.com/your-org/your-repo"
LABEL dev.releaseasknowledge.spec.url="https://releaseasknowledge.dev/spec/v1"
```

### 1.3 Build 與驗證

build 時把 `ARG` 帶進去：

```bash
docker build \
  --build-arg COMMIT_SHA=$(git rev-parse HEAD) \
  --build-arg BUILD_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --build-arg VERSION=$(git describe --tags --always) \
  -t your-image:tag .
```

驗證（兩種方式都可以）：

```bash
# 1. 用 docker / OCI 既有工具看（不需任何 R2K 工具）
docker inspect your-image:tag --format='{{json .Config.Labels}}' | jq

# 2. 用 r2k CLI 校驗 R2K 必填欄位有沒有齊
r2k validate identity your-image:tag
```

✅ 此刻你已經是 **R2K Level 1 compliant**。
下游不需要安裝任何新工具，光 `docker inspect`（OCI 工具）就能拿到事實；想做 R2K 後續操作（diff / insight）的人，再用 `r2k` CLI 讀同一份 label 即可。

---

## Step 2 · 重要資產自動收集（L2 · Trust）

在 build pipeline 裡，把每次都會用到的「事實」自動 dump 進 image 的 `/r2k/`，並用一份 **`/r2k/index.yaml`** 當作整個 snapshot 的入口清單。

### 2.1 標準目錄結構

```
/r2k/
├── index.yaml               # ⭐ snapshot 入口清單（必填）
├── meta/
│   └── manifest.json        # 身份元資料（commit / branch / build time）
├── api/
│   └── openapi.json         # OpenAPI 規格
├── db/
│   └── schema.sql           # DB schema 快照
├── config/
│   └── env.json             # config / env 模板
├── sbom/
│   └── sbom.json            # CycloneDX / SPDX
└── runtime/
    └── manifest.yaml        # Helm / K8s 清單
```

### 2.2 `/r2k/index.yaml` · snapshot 入口清單

`index.yaml` 是 **整個 L2 snapshot 的目錄**：列出有哪些資產、各自的 schema、檔案路徑、hash、產生它的 collector。下游不需要 walk 整個 `/r2k/` 就能知道這顆 image 有什麼。

它對 R2K 的角色，類似 OCI 的 `manifest.json`、SBOM 的 `bom-ref` 表：**先讀目錄，再依需要讀內容**。

#### 為什麼需要 index.yaml？

- 🧭 **可發現性**：下游讀一份檔案就知道有哪些資產、用什麼 schema
- 🔐 **完整性**：每個資產都有 `sha256`，可驗證沒被竄改
- 🧩 **可擴充**：vendor / 內部可用 `x-yourco-*` 多塞自家資產，不破壞標準欄位
- ⚡ **L3 友好**：diff plugin 直接從 `index.yaml` 找對應檔，不需要硬編碼路徑
- 📦 **與 OCI/SBOM 接軌**：`oci.image.digest` / `sbom.format` 等欄位明確指向既有標準

#### Schema

```yaml
# /r2k/index.yaml
schema: releaseasknowledge.dev/index/v1          # 這份 index 自己的 schema
generated_at: "2026-05-03T08:00:00Z"
generator: "r2k-cli@1.0.0"        # 產生 index 的工具

image:
  ref: "your-image:1.5.0"
  digest: "sha256:abc123..."       # OCI image digest（與 image label 對齊）
  oci_labels:                      # 從 OCI label 抄來的關鍵欄位（方便不開 image 也讀得到）
    revision: "0123abc..."         # = org.opencontainers.image.revision
    version:  "1.5.0"              # = org.opencontainers.image.version
    created:  "2026-05-03T07:55:00Z"

r2k:
  spec_version: "1.0"              # = dev.releaseasknowledge.version
  level: 2                         # = dev.releaseasknowledge.level
  diff_mode: null                  # L3 才會填（A / B / A+B）

assets:                            # ⭐ 核心：列出所有 L2 snapshot
  - id: api
    type: api                      # api | db | config | sbom | runtime | meta
    path: api/openapi.json
    schema: openapi/3.1            # 該檔遵循的 schema 版本
    media_type: application/vnd.oai.openapi+json
    sha256: "fa1b2c..."
    collector: "openapi-generator@7.0.0"

  - id: db
    type: db
    path: db/schema.sql
    schema: postgres/15
    media_type: application/sql
    sha256: "9d8e7f..."
    collector: "atlas@0.27.0"

  - id: config
    type: config
    path: config/env.json
    schema: releaseasknowledge.dev/config/v1
    media_type: application/json
    sha256: "2a3b4c..."
    collector: "internal-config-dumper@1.2.0"

  - id: sbom
    type: sbom
    path: sbom/sbom.json
    schema: cyclonedx/1.6
    media_type: application/vnd.cyclonedx+json
    sha256: "55aa66..."
    collector: "syft@1.10.0"

  - id: runtime
    type: runtime
    path: runtime/manifest.yaml
    schema: helm/v3
    media_type: application/yaml
    sha256: "77bb88..."
    collector: "helm@3.15.0"

# vendor / 內部自家資產用 x-* prefix，不汙染標準命名空間
extensions:
  - id: x-yourco-feature-flags
    type: x-yourco-feature-flags
    path: ext/yourco/flags.json
    schema: yourco/flags/v2
    sha256: "ee99ff..."
    collector: "yourco-flag-exporter@0.4.1"
```

#### 必填 vs 選填

| 欄位 | 必填 | 說明 |
|---|:-:|---|
| `schema` | ✅ | 固定 `releaseasknowledge.dev/index/v1` |
| `generated_at` | ✅ | RFC 3339 時間 |
| `image.ref` / `image.digest` | ✅ | 鎖定這份 index 屬於哪顆 image |
| `r2k.spec_version` / `r2k.level` | ✅ | 與 OCI label 一致 |
| `assets[].{id,type,path,schema,sha256}` | ✅ | 每個資產的最小定義 |
| `assets[].collector` | ◯ | 強烈建議；diff / insight 會用來判斷規則套用 |
| `assets[].media_type` | ◯ | 給 registry / UI 預覽用 |
| `extensions[]` | ◯ | vendor 自家資產 |

> 設計原則對齊 Manifesto 第 1 原則：**index.yaml 只記事實**（path / hash / schema），不記解讀。

### 2.3 Collector 範例（CI 腳本）

```bash
mkdir -p /r2k/{api,db,config,sbom,runtime,meta}

# 1. OpenAPI（看你的 framework 怎麼產）
curl http://localhost:8080/v3/api-docs > /r2k/api/openapi.json

# 2. DB schema（用 Atlas 為例）
atlas schema inspect --url "$DB_URL" --format '{{ sql . }}' > /r2k/db/schema.sql

# 3. Config 模板
./scripts/dump-config-template.sh > /r2k/config/env.json

# 4. SBOM（用 Syft 為例）
syft packages dir:. -o cyclonedx-json > /r2k/sbom/sbom.json

# 5. Runtime manifest
helm template ./chart > /r2k/runtime/manifest.yaml

# 6. ⭐ 最後產生 index.yaml（掃描 /r2k/ 自動填 sha256 與 path）
r2k snapshot index /r2k --out /r2k/index.yaml \
  --image-ref "your-image:1.5.0" \
  --collector openapi=openapi-generator@7.0.0 \
  --collector db=atlas@0.27.0 \
  --collector sbom=syft@1.10.0
```

### 2.4 寫進 image 並升級 label

把整個 `/r2k/` 寫進 image，並把 `dev.releaseasknowledge.level` 從 `1` 蓋成 `2`、補上 snapshot 路徑與 index 入口：

```dockerfile
# === R2K Level 2 · Trust ===
COPY --from=collector /r2k /r2k

# 升級 R2K level（後 LABEL 蓋前 LABEL）
LABEL dev.releaseasknowledge.level="2"
LABEL dev.releaseasknowledge.snapshot.path="/r2k"
LABEL dev.releaseasknowledge.snapshot.index="/r2k/index.yaml"
```

| Label key | 說明 |
|---|---|
| `dev.releaseasknowledge.level="2"` | 把宣告的 R2K Level 從 1 提升到 2 |
| `dev.releaseasknowledge.snapshot.path` | L2 snapshot 在 image 內的根目錄（預設 `/r2k`，自家專案改路徑時才需要寫） |
| `dev.releaseasknowledge.snapshot.index` | snapshot 入口清單的絕對路徑，下游 / `r2k` CLI 從這裡開始讀 |

### 2.5 驗證

```bash
# 1. 檢查 /r2k/ 結構與 index.yaml schema
r2k validate state your-image:tag

# 2. 校驗每個 asset 的 sha256 與 index 一致（防竄改）
r2k validate snapshot your-image:tag --check-hashes
```

✅ 此刻你已經是 **R2K Level 2 compliant**。

> 提示：**這一步最花時間**，因為每個 collector 都要在 CI 中跑通。建議按照「最常被問起的資產」優先順序導入：通常是 **SBOM → OpenAPI → DB → Config**。`index.yaml` 可以一邊只列已導入的資產，**不必一次列齊**。

---

## Step 3 · 跨資產 Diff（L3 · Understand）

### 3.1 直接做 diff

```bash
r2k diff your-image:v1.4.0 your-image:v1.5.0 --out change.yaml
```

CLI 會調用所有已安裝的 diff plugin，產出統一的 `change.yaml`：

```yaml
version: 1
from: your-image:v1.4.0
to:   your-image:v1.5.0
changes:
  - type: api
    plugin: r2k-diff-openapi
    action: removed
    target: GET /users
    severity: high
    detail:
      replaced_by: GET /v2/users
  - type: dependency
    plugin: r2k-diff-sbom
    action: upgraded
    target: log4j-core
    from_version: 2.16.0
    to_version: 2.17.0
    severity: critical
    cve: CVE-2021-45046
```

### 3.2 v1 的 AB plan：何時算 diff？

R2K v1 不規定唯一答案：

#### Mode A · Pre-computed（預先計算，適合 air-gap / on-prem）

CI 階段就把 `change.yaml` 算好，附在 image：

```bash
# 在 CI 中
r2k diff $PREVIOUS_IMAGE $NEW_IMAGE --out /r2k/change/default.yaml
```

```dockerfile
# === R2K Level 3 · Understand (Mode A) ===
COPY --from=diff /r2k/change /r2k/change

LABEL dev.releaseasknowledge.level="3"
LABEL dev.releaseasknowledge.diff.mode="A"
LABEL dev.releaseasknowledge.diff.from="your-image:v1.4.0"
LABEL dev.releaseasknowledge.diff.path="/r2k/change/default.yaml"
```

| Label key | 說明 |
|---|---|
| `dev.releaseasknowledge.level="3"` | 把宣告的 R2K Level 從 2 提升到 3 |
| `dev.releaseasknowledge.diff.mode` | L3 diff 的計算時機：`A`（pre-computed）/ `B`（on-demand）/ `A+B`（雙模式） |
| `dev.releaseasknowledge.diff.from` | Mode A 預先算好的對照 base image，幫 Mode B 工具知道「這份內建 manifest 是哪個 pair」 |
| `dev.releaseasknowledge.diff.path` | 內建 `change.yaml` 的絕對路徑（Mode B 找不到時 fallback） |

> 同步把 `index.yaml` 內的 `r2k.diff_mode` 也填好，讓單一入口檔即可看出這顆 image 的 L3 狀態。

#### Mode B · On-demand（即時計算，適合 SaaS / 任意組合）

不附 manifest，由 Diff Engine 在查詢時算：

```bash
r2k diff your-image:v1.4.0 your-image:v1.7.0   # 任何組合都能查
```

#### 雙模式並存（推薦）

預設 pair 用 Mode A 算進 image，L2 snapshots 完整保留，留給 Mode B 重算其它組合。

驗證：

```bash
r2k validate change /r2k/change/default.yaml
```

---

## Step 4 · Insight 與 Share（L3+ / L4）

當你已經有 `change.yaml`，就能往「跨資產關聯洞察」走：

```bash
# 把 change.yaml 餵給 insight 框架
r2k insight change.yaml

# 範例輸出：
# ⚠️  HIGH IMPACT
# - GET /users（API breaking）+ users 表 rename（DB migration）
#   → 同一變更面，建議在 release notes 並列說明
#
# 🔥 SECURITY
# - log4j-core 升版引入 CVE-2021-45046 ，且該 dependency 在 OpenAPI handler 出現
#   → 對外暴露面增加，建議列為 release blocker
```

`r2k insight` 是外掛式框架：

- 接 LLM（給 release 摘要 / risk 解釋）
- 接規則引擎（policy as code）
- 接你團隊既有的 risk policy

最後產生 badge：

```bash
r2k certify your-image:tag --output badge.json
```

```json
{
  "level": 3,
  "mode": "A+B",
  "compliant": true,
  "checked_at": "2026-05-03T00:00:00Z"
}
```

✅ 此刻你已經是 **R2K Level 3 compliant**，並準備好往 L4（跨組織共享）邁進。

---

## 各層對應工具與驗證一覽

| Step | Level | 主要工具（v1 規劃）| 驗證指令 |
|---|---|---|---|
| 1 | Identify | `r2k label`、`docker inspect` | `r2k validate identity` |
| 2 | Trust | `r2k snapshot`（OpenAPI / DB / Config / SBOM collector）| `r2k validate state` |
| 3 | Understand | `r2k diff A B`（diff plugin SPI）| `r2k validate change` |
| 4 | Share | `r2k insight`、`r2k certify`、registry / badge | `r2k certify` |

---

## 常見導入順序建議

1. **Week 1**：完成 Step 1（L1 LABEL），把 5 行 LABEL 接到所有 image build。
2. **Week 2-3**：完成 Step 2（L2 SBOM + OpenAPI），這兩個收益最快。
3. **Month 2**：補齊 L2 其他 collector（DB schema、config、runtime）。
4. **Month 3+**：建立 Step 3 baseline，跑第一條 diff plugin（通常從 OpenAPI 或 SBOM 開始）。
5. **Quarter 2**：規劃 Step 4 的 insight 與內部 badge 政策。

> 你不必、也不該一次跨完。**分階段宣告達成**才是 R2K 的設計重點。

---

## 下一步

- 讀 [完整介紹](./index.md)
- 讀 [R2K Manifesto v1](./manifesto.md) — 設計哲學與 8 原則
- 讀 [常見問題](./faq.md)
- 讀 [術語表](./glossary.md)
