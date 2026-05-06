# Quick Start · Release-as-Knowledge v1

> From "ship a binary" to "ship knowledge" — take the first R2K step in 5 minutes.

R2K does not require you to adopt everything at once. This guide walks you through **the four steps in order** (Identify → Trust → Understand → Share). Each step can be **independently declared as done**, and you can pause there until your team has bandwidth for the next one.

---

## Concepts you'll touch

| Step | Level | Action | Estimated time |
|---|---|---|---|
| Step 1 | L1 Identify | Attach OCI labels to the image | **5 minutes** |
| Step 2 | L2 Trust | Auto-collect OpenAPI / DB / Config / SBOM | half-day ~ 2 weeks |
| Step 3 | L3 Understand | Run cross-asset diff between two releases | 2-4 weeks |
| Step 4 | L3+/L4 Share | Plug in insight framework, issue badges | continuous |

---

## Step 1 · 5 minutes to L1 (Identify)

R2K Level 1 attaches **two groups of labels** to the image:

| Group | Namespace | Defined by | Tooling support |
|---|---|---|---|
| **OCI standard labels** | `org.opencontainers.image.*` | [OCI Image Spec — Annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md) | Native support in GHCR / ECR / Docker Hub UI, Trivy, Cosign, Skopeo… |
| **R2K-specific labels** | `com.releaseasknowledge.*` | R2K spec v1 | `r2k` CLI, R2K diff plugins / insight framework |

> Use both at the same time. You **do not introduce any new tooling** — OCI labels feed the existing container ecosystem, R2K labels feed R2K tools.

### 1.1 OCI standard labels (attach these first)

OCI already defines a **predefined set of image annotation keys**. For anything that is plain metadata (commit, version, source repo, license…), **prefer the OCI standard key** rather than inventing your own.

| Label key | Meaning | Example value |
|---|---|---|
| `org.opencontainers.image.title` | Human-readable image name | `my-service` |
| `org.opencontainers.image.description` | Short description | `Customer-facing API gateway` |
| `org.opencontainers.image.version` | Software version (semver / tag) | `1.5.0` |
| `org.opencontainers.image.revision` | Source commit SHA | `${COMMIT_SHA}` |
| `org.opencontainers.image.created` | Build time (RFC 3339) | `${BUILD_TIME}` |
| `org.opencontainers.image.source` | Source repo URL | `https://github.com/your-org/your-repo` |
| `org.opencontainers.image.url` | Product / service homepage | `https://your-product.example` |
| `org.opencontainers.image.documentation` | Docs URL | `https://docs.your-product.example` |
| `org.opencontainers.image.vendor` | Publishing organization | `Your Org` |
| `org.opencontainers.image.licenses` | SPDX license expression | `Apache-2.0` |
| `org.opencontainers.image.authors` | Maintainer contact | `team@your-org.example` |

Append to your `Dockerfile`:

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

> Tip: already using some OCI labels? Good — **don't duplicate them**. R2K does not redefine these fields. The R2K-specific labels below only fill in what OCI doesn't cover.

### 1.2 R2K-specific labels (then add these)

The `com.releaseasknowledge.*` group only covers "things specific to R2K" — which spec version this image follows, which level it self-declares, what L3 mode it uses, etc.

| Label key | Required? | Meaning | Example value |
|---|:-:|---|---|
| `com.releaseasknowledge.version` | ✅ | The **R2K spec version** this image follows | `1.0` |
| `com.releaseasknowledge.level` | ✅ | Self-declared R2K level (`1` / `2` / `3` / `4`) | `1` |
| `com.releaseasknowledge.commit` | ✅ | Source commit SHA (same value as `org.opencontainers.image.revision`, kept here so R2K tools can look it up directly) | `${COMMIT_SHA}` |
| `com.releaseasknowledge.branch` | ◯ | source git branch；diff/insight 用來判斷 release line（hotfix / main / release-x.y）| `main` 或 `release/2.4.x` |
| `com.releaseasknowledge.tag` | ◯ | source git tag；單一 tag 直接寫，多個用逗號分隔；無 tag 則省略 | `v2.4.1` 或 `v2.4.1,latest` |
| `com.releaseasknowledge.build-time` | ✅ | Build time of the R2K manifest (RFC 3339) | `${BUILD_TIME}` |
| `com.releaseasknowledge.repo` | ◯ | Source repo URL (used by diff / insight to fetch context) | `https://github.com/your-org/your-repo` |
| `com.releaseasknowledge.snapshot.path` | ◯ | Where the L2 snapshot lives in the image (defaults to `/r2k`) | `/r2k` |
| `com.releaseasknowledge.snapshot.index` | ◯ | Absolute path of the snapshot index file | `/r2k/index.yaml` |
| `com.releaseasknowledge.diff.mode` | ◯ | When L3 diff is computed: `A` / `B` / `A+B` (see Step 3) | `A+B` |
| `com.releaseasknowledge.diff.from` | ◯ | The base image that Mode A's pre-computed manifest is paired against | `your-image:v1.4.0` |
| `com.releaseasknowledge.spec.url` | ◯ | URL of the R2K spec document you follow | `https://releaseasknowledge.com/spec/v1` |

> ✅ **Required** = minimum bar for Level 1; ◯ = add as you advance.
> `level` is meant to be overwritten as you progress to Step 2 / 3 (later `LABEL` overrides earlier ones).

Append the R2K-specific block right after the OCI labels:

```dockerfile
# === R2K Level 1 · Identity ===
LABEL com.releaseasknowledge.version="1.0"
LABEL com.releaseasknowledge.level="1"
LABEL com.releaseasknowledge.commit="${COMMIT_SHA}"
LABEL com.releaseasknowledge.branch="${GIT_BRANCH}"
LABEL com.releaseasknowledge.tag="${GIT_TAG}"
LABEL com.releaseasknowledge.build-time="${BUILD_TIME}"
LABEL com.releaseasknowledge.repo="https://github.com/your-org/your-repo"
LABEL com.releaseasknowledge.spec.url="https://releaseasknowledge.com/spec/v1"
```

### 1.3 Build & verify

Pass the build args:

```bash
docker build \
  --build-arg COMMIT_SHA=$(git rev-parse HEAD) \
  --build-arg BUILD_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --build-arg VERSION=$(git describe --tags --always) \
  -t your-image:tag .
```

Verify (either path works):

```bash
# 1. Use existing docker / OCI tools (no R2K tooling required)
docker inspect your-image:tag --format='{{json .Config.Labels}}' | jq

# 2. Use the r2k CLI to check R2K's required fields
r2k validate identity your-image:tag
```

✅ At this point you are **R2K Level 1 compliant**.
Downstream consumers don't need to install anything new — `docker inspect` (OCI tooling) reads the facts. Anyone who wants to do further R2K work (diff / insight) reads the same labels via the `r2k` CLI.

---

## Step 2 · Automated asset collection (L2 · Trust)

In your build pipeline, automatically dump the "facts" every release uses into the image's `/r2k/`, and use **`/r2k/index.yaml`** as the entry-point manifest for the whole snapshot.

### 2.1 Standard directory layout

```
/r2k/
├── index.yaml               # ⭐ snapshot entry index (required)
├── meta/
│   └── manifest.json        # identity meta (commit / branch / build time)
├── api/
│   └── openapi.json         # OpenAPI spec
├── db/
│   └── schema.sql           # DB schema snapshot
├── config/
│   └── env.json             # config / env template
├── sbom/
│   └── sbom.json            # CycloneDX / SPDX
└── runtime/
    └── manifest.yaml        # Helm / K8s manifest
```

### 2.2 `/r2k/index.yaml` · the snapshot entry index

`index.yaml` is the **directory of the entire L2 snapshot**: it lists which assets exist, their schemas, file paths, hashes, and the collector that produced each. Downstream consumers don't have to walk `/r2k/` to know what's there.

Its role in R2K is analogous to OCI's `manifest.json` or CycloneDX's `bom-ref` table: **read the index first, then fetch what you need**.

#### Why an index.yaml?

- 🧭 **Discoverability** — one file tells you which assets are present and what schema each follows
- 🔐 **Integrity** — every asset has a `sha256`, so you can verify it has not been tampered with
- 🧩 **Extensibility** — vendors / internal teams can add their own assets via `x-yourco-*` without breaking standard fields
- ⚡ **L3-friendly** — diff plugins find the right files via `index.yaml` instead of hard-coding paths
- 📦 **Aligned with OCI/SBOM** — fields like `oci.image.digest` and `sbom.format` link cleanly to existing standards

#### Schema

```yaml
# /r2k/index.yaml
schema: releaseasknowledge.com/index/v1          # schema of this index file itself
generated_at: "2026-05-03T08:00:00Z"
generator: "r2k-cli@1.0.0"        # tool that produced this index

image:
  ref: "your-image:1.5.0"
  digest: "sha256:abc123..."       # OCI image digest (matches image labels)
  oci_labels:                      # key OCI labels copied here for label-less consumers
    revision: "0123abc..."         # = org.opencontainers.image.revision
    version:  "1.5.0"              # = org.opencontainers.image.version
    created:  "2026-05-03T07:55:00Z"

r2k:
  spec_version: "1.0"              # = com.releaseasknowledge.version
  level: 2                         # = com.releaseasknowledge.level
  diff_mode: null                  # filled at L3 (A / B / A+B)

assets:                            # ⭐ core: every L2 snapshot listed here
  - id: api
    type: api                      # api | db | config | sbom | runtime | meta
    path: api/openapi.json
    schema: openapi/3.1            # schema/version this file follows
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
    schema: releaseasknowledge.com/config/v1
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

# Vendor / internal extensions use the x-* prefix
extensions:
  - id: x-yourco-feature-flags
    type: x-yourco-feature-flags
    path: ext/yourco/flags.json
    schema: yourco/flags/v2
    sha256: "ee99ff..."
    collector: "yourco-flag-exporter@0.4.1"
```

#### Required vs optional fields

| Field | Required | Meaning |
|---|:-:|---|
| `schema` | ✅ | Fixed value `releaseasknowledge.com/index/v1` |
| `generated_at` | ✅ | RFC 3339 timestamp |
| `image.ref` / `image.digest` | ✅ | Pin this index to a specific image |
| `r2k.spec_version` / `r2k.level` | ✅ | Must match OCI labels |
| `assets[].{id,type,path,schema,sha256}` | ✅ | Minimum per-asset definition |
| `assets[].collector` | ◯ | Strongly recommended; diff / insight use it for rule selection |
| `assets[].media_type` | ◯ | For registry / UI previews |
| `extensions[]` | ◯ | Vendor-defined assets |

> Design principle (Manifesto Principle 1): **`index.yaml` records facts only** (path / hash / schema), never intelligence.

### 2.3 Collector example (CI script)

```bash
mkdir -p /r2k/{api,db,config,sbom,runtime,meta}

# 1. OpenAPI (depends on your framework)
curl http://localhost:8080/v3/api-docs > /r2k/api/openapi.json

# 2. DB schema (Atlas as an example)
atlas schema inspect --url "$DB_URL" --format '{{ sql . }}' > /r2k/db/schema.sql

# 3. Config template
./scripts/dump-config-template.sh > /r2k/config/env.json

# 4. SBOM (Syft as an example)
syft packages dir:. -o cyclonedx-json > /r2k/sbom/sbom.json

# 5. Runtime manifest
helm template ./chart > /r2k/runtime/manifest.yaml

# 6. ⭐ Generate the index.yaml last (scans /r2k/, fills sha256 + paths)
r2k snapshot index /r2k --out /r2k/index.yaml \
  --image-ref "your-image:1.5.0" \
  --collector openapi=openapi-generator@7.0.0 \
  --collector db=atlas@0.27.0 \
  --collector sbom=syft@1.10.0
```

### 2.4 Bake into the image and bump the label

Copy `/r2k/` into the image, override `com.releaseasknowledge.level` from `1` to `2`, and add the snapshot path / index entry:

```dockerfile
# === R2K Level 2 · Trust ===
COPY --from=collector /r2k /r2k

# Bump R2K level (later LABEL overrides earlier)
LABEL com.releaseasknowledge.level="2"
LABEL com.releaseasknowledge.snapshot.path="/r2k"
LABEL com.releaseasknowledge.snapshot.index="/r2k/index.yaml"
```

| Label key | Meaning |
|---|---|
| `com.releaseasknowledge.level="2"` | Bump declared R2K level from 1 to 2 |
| `com.releaseasknowledge.snapshot.path` | Root directory of L2 snapshot inside the image (defaults to `/r2k`; only override if you use a different path) |
| `com.releaseasknowledge.snapshot.index` | Absolute path of the snapshot index — downstream / `r2k` CLI reads this first |

### 2.5 Verify

```bash
# 1. Check /r2k/ structure & index.yaml schema
r2k validate state your-image:tag

# 2. Verify each asset's sha256 against the index (tamper detection)
r2k validate snapshot your-image:tag --check-hashes
```

✅ At this point you are **R2K Level 2 compliant**.

> Tip: **this step takes the longest**, because every collector has to be wired up in CI. Recommended priority order: **SBOM → OpenAPI → DB → Config**. `index.yaml` may list only the assets you've onboarded so far — **you don't have to ship them all at once**.

---

## Step 3 · Cross-asset diff (L3 · Understand)

### 3.1 Run the diff

```bash
r2k diff your-image:v1.4.0 your-image:v1.5.0 --out change.yaml
```

The CLI invokes every installed diff plugin and produces a unified `change.yaml`:

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

### 3.2 The v1 AB plan: when do we compute the diff?

R2K v1 does not prescribe a single answer:

#### Mode A · Pre-computed (best for air-gap / on-prem)

CI computes `change.yaml` ahead of time and ships it with the image:

```bash
# In CI
r2k diff $PREVIOUS_IMAGE $NEW_IMAGE --out /r2k/change/default.yaml
```

```dockerfile
# === R2K Level 3 · Understand (Mode A) ===
COPY --from=diff /r2k/change /r2k/change

LABEL com.releaseasknowledge.level="3"
LABEL com.releaseasknowledge.diff.mode="A"
LABEL com.releaseasknowledge.diff.from="your-image:v1.4.0"
LABEL com.releaseasknowledge.diff.path="/r2k/change/default.yaml"
```

| Label key | Meaning |
|---|---|
| `com.releaseasknowledge.level="3"` | Bump declared R2K level from 2 to 3 |
| `com.releaseasknowledge.diff.mode` | When L3 diff is computed: `A` (pre-computed) / `B` (on-demand) / `A+B` (both) |
| `com.releaseasknowledge.diff.from` | Base image that Mode A's pre-computed manifest is paired against — lets Mode B tools know which pair this baked manifest covers |
| `com.releaseasknowledge.diff.path` | Absolute path of the baked `change.yaml` (Mode B fallback when no engine is reachable) |

> Also fill `r2k.diff_mode` in `index.yaml`, so a single entry file reveals this image's L3 state.

#### Mode B · On-demand (best for SaaS / arbitrary combinations)

No baked manifest — the Diff Engine computes on demand at query time:

```bash
r2k diff your-image:v1.4.0 your-image:v1.7.0   # any combination is queryable
```

#### Both modes (recommended)

Mode A is baked for the default pair, while L2 snapshots are kept complete for Mode B to recompute any other combination.

Verify:

```bash
r2k validate change /r2k/change/default.yaml
```

---

## Step 4 · Insight & Share (L3+ / L4)

Once you have `change.yaml`, you can step up to "cross-asset correlation":

```bash
# Feed change.yaml to the insight framework
r2k insight change.yaml

# Sample output:
# ⚠️  HIGH IMPACT
# - GET /users (API breaking) + users-table rename (DB migration)
#   → same change surface; explain together in release notes
#
# 🔥 SECURITY
# - log4j-core upgrade introduces CVE-2021-45046, and the dep is reached from an OpenAPI handler
#   → external attack surface increased; suggest treating as a release blocker
```

`r2k insight` is a pluggable framework:

- Plug in LLMs (release summaries / risk explanations)
- Plug in rule engines (policy-as-code)
- Plug in your team's existing risk policy

Finally, issue a badge:

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

✅ At this point you are **R2K Level 3 compliant**, and ready to head toward L4 (cross-organization sharing).

---

## Tools & validation per layer

| Step | Level | Primary tooling (v1 plan) | Validation command |
|---|---|---|---|
| 1 | Identify | `r2k label`, `docker inspect` | `r2k validate identity` |
| 2 | Trust | `r2k snapshot` (OpenAPI / DB / Config / SBOM collectors) | `r2k validate state` |
| 3 | Understand | `r2k diff A B` (diff plugin SPI) | `r2k validate change` |
| 4 | Share | `r2k insight`, `r2k certify`, registry / badge | `r2k certify` |

---

## Suggested adoption order

1. **Week 1** — Step 1 (L1 LABEL): wire 5 lines of `LABEL` into every image build.
2. **Week 2-3** — Step 2 (L2 SBOM + OpenAPI): the two highest-leverage assets.
3. **Month 2** — Round out L2 with the remaining collectors (DB schema, config, runtime).
4. **Month 3+** — Establish a Step 3 baseline; ship the first diff plugin (usually OpenAPI or SBOM first).
5. **Quarter 2** — Plan the Step 4 insight framework and an internal badge policy.

> You don't have to — and shouldn't — finish all four steps in one go. **Step-by-step declared compliance** is exactly what R2K is designed for.

---

## Next

- Read the [full introduction](./index.md)
- Read the [R2K Manifesto v1](./manifesto.md) — design philosophy and 8 principles
- Read the [FAQ](./faq.md)
- Read the [Glossary](./glossary.md)
