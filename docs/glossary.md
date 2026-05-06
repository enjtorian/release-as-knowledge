# Glossary · Release-as-Knowledge v1

Comprehensive definitions of terms used in the R2K spec.

---

## 1. Top-level concepts

### R2K (Release-as-Knowledge)
A semantic standard that upgrades every release from a non-machine-readable binary into a **structured, machine-indexable, reasoning-friendly knowledge object**. R2K v1 adopts a "4-Step adoption path" (LABEL → Snapshot → Diff → Insight) mapped to 4 levels, each independently declarable.

### 4-Step adoption path
The R2K v1 core adoption model:

1. **Step 1 · LABEL (L1 Identify)** — OCI labels declare identity
2. **Step 2 · Snapshot (L2 Trust)** — OpenAPI / DB / Config / SBOM auto-collected
3. **Step 3 · Diff (L3 Understand)** — cross-asset diff plugins
4. **Step 4 · Insight (L3+/L4 Share)** — cross-asset correlation insight

Each step is independently declarable, and each has its own tooling and validation.

### Release (in R2K's sense)
Not "an image", but a **structured knowledge object** of `Identity + State + ChangeSet`. The image is a *carrier* in R2K, not the *model*.

### Manifesto v1
The R2K design thesis: 8 principles, 4 levels, the Mode A/B duality. See [docs/manifesto.md](./manifesto.md).

---

## 2. The four levels

### L1 · Identity
Fact layer. Declares release identity through two label groups:

- **OCI standard labels** (`org.opencontainers.image.*`) — predefined by the [OCI Image Spec annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md), natively supported by all container tooling (`title`, `version`, `revision`, `created`, `source`, `licenses`, `vendor`, …)
- **R2K-specific labels** (`com.releaseasknowledge.*`) — R2K's own namespace (`version`, `level`, `commit`, `build-time`, `repo`, `snapshot.path`, `snapshot.index`, `diff.mode`, `diff.from`, …)

R2K does not redefine fields that OCI already provides. Use both groups together.
**Validation**: `r2k validate identity`.

### L2 · Trust
Fact layer. Dumps the facts every release uses into the image's `/r2k/`:

- `/r2k/api/openapi.json`
- `/r2k/db/schema.sql`
- `/r2k/config/env.json`
- `/r2k/sbom/sbom.json`
- `/r2k/runtime/manifest.yaml`
- `/r2k/meta/manifest.json`
- **`/r2k/index.yaml`** — entry index

**Validation**: `r2k validate state`.

### L3 · Understand
**Intelligence layer** (not the fact layer). Diffs two releases' L2 snapshots across assets, producing a unified `change.yaml`.
L3 has the **AB plan** (see Mode A / Mode B below).
**Validation**: `r2k validate change`.

### L4 · Share
Social layer. Shares L3 intelligence across organizations: badges, registries, release intelligence graphs.
**Validation / certification**: `r2k certify`.

---

## 3. The L3 AB plan

### Mode A · Pre-computed
The Change Manifest is computed in CI and attached to the image. Customer side does not need a Diff Engine service. ✅ Best for air-gapped / on-prem ISVs.

### Mode B · On-demand
CI attaches only L1+L2 snapshots; the Diff Engine computes at query time. Any from→to combination is queryable. ✅ Best for SaaS / connected enterprise / open-source tools.

### Both modes
The image carries Mode A's default-pair manifest, while L2 snapshots are kept complete to allow Mode B to recompute any other combination. The recommended setup in practice.

---

## 4. Structured files

### `/r2k/index.yaml`
**Entry-point index for the L2 snapshot**. Lists every R2K asset in the image (path, schema, sha256, collector). The **first thing downstream consumers should read**.
Schema: `releaseasknowledge.com/index/v1`. Top-level fields: `image.{ref,digest}`, `r2k.{spec_version,level,diff_mode}`, `assets[]`, `extensions[]`.
Plays the same role as OCI's `manifest.json` or CycloneDX's `bom-ref` table — **records facts only**, never intelligence.

### `/r2k/meta/manifest.json`
Identity meta file (L1). Contains image tag, commit, branch, build time, R2K spec version.

### `/r2k/api/openapi.json`
OpenAPI spec snapshot (L2). Dumped by framework / SDK generator at build time.

### `/r2k/db/schema.sql`
DB schema snapshot (L2). Exported by Atlas / Flyway / Liquibase / etc.

### `/r2k/config/env.json`
Config / env template (L2). Serialized service-config template.

### `/r2k/sbom/sbom.json`
Software bill of materials (L2). CycloneDX or SPDX format, produced by Syft etc.

### `/r2k/runtime/manifest.yaml`
Runtime deployment manifest (L2). Helm / K8s manifest.

### `change.yaml`
Cross-asset diff result (L3). Unified schema:

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
Certification output (L4). Includes level, mode (A / B / A+B), compliance status, check time.

---

## 5. Tools & mechanisms

### Collector (asset collector)
A tool that, at build time, dumps a single asset into the corresponding `/r2k/` location. R2K does not invent collectors — it **integrates existing tools** (Atlas, Syft, OpenAPI generator, …).

### Diff Plugin
A plugin that computes the diff for a single asset class. Registers through R2K's plugin SPI; output uniformly follows the `change.yaml` schema.
Examples: `r2k-diff-openapi`, `r2k-diff-dbschema`, `r2k-diff-sbom`, `r2k-diff-config`.

### Diff Engine
The runtime that runs diff plugins. Triggered by CI in Mode A; triggered by the query side in Mode B.

### Insight Framework
The pluggable framework at L3+ / L4. Correlates multiple diffs across assets and emits risk insight. Can plug in LLMs, rule engines, or policy-as-code.

### Plugin SPI (Service Provider Interface)
The extension interface R2K provides for diff plugins and insight modules.
Input: `/r2k/` snapshot or `change.yaml`.
Output: structured results following R2K's schema.

### Vendor Extension (`x-yourco-*`)
Vendors or teams may add custom fields on top of R2K's schema, prefixed with `x-yourco-*` to avoid collision with future standard fields.

---

## 6. Design philosophy terms

### Facts vs Intelligence (Principle 1)
- **Facts** — L1 LABEL + L2 snapshot, live in the image
- **Intelligence** — L3 Change Manifest + L4 insight, derived from facts

Analogy with git: commits store snapshots (fact), diffs are computed (intelligence).
Analogy with SBOM: stores component lists (fact), vulnerability scans are computed (intelligence).

### Layered by Query Frequency (Principle 6)
Layered by how often each layer is queried:

- 90% high-frequency lightweight queries → L1 LABEL (~50ms)
- 10% low-frequency heavy queries → L2 snapshot (~300ms)
- 1% deep-detail queries → L3 Change Manifest

### Compatible with Existing Pipelines (Principle 7)
No CI/CD rewrite, no registry change, no framework swap. R2K is additive instrumentation, adoptable incrementally.

### Manifests are the Lingua Franca (Principle 8)
Structured yaml/json bridges tools, organizations, and human/machine readability.

---

## 7. What R2K is NOT

| Term | Relationship to R2K |
|---|---|
| SBOM | **Subset of R2K L2** (covers dependencies only) |
| SLSA | **Complementary** — SLSA solves build security; R2K solves change communication |
| Release notes | A **derived byproduct** of R2K (human-readable description), not the same layer |
| OpenAPI | **Part of R2K L2**, plugged into L3 via diff plugin |
| Git | R2K does to OCI images what git does to source code, but **does not redo git** |
| Docker / OCI | The image is R2K's **carrier**, not its model |
| Datadog / Grafana | **Complementary** — observability is runtime truth; R2K is release-time truth |
| Tool / product | R2K **is not a tool**, but a framework + naming + adoption standard |
