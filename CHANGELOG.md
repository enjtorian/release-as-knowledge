# Changelog

All notable changes to **Release-as-Knowledge (R2K)** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-05

> First public release of the Release-as-Knowledge (R2K) specification.
> 4 levels · 8 principles · Mode A/B AB plan · CC BY 4.0.

### 📜 Manifesto & specification

- **Release-as-Knowledge Manifesto v1** published in English and Traditional Chinese (`docs/manifesto.md`, `docs/zh-tw/manifesto.md`).
- **8 principles** formalized, including Principle 1 *"Artifact carries facts, not intelligence"* — cleanly separating L1+L2 facts from L3+L4 intelligence.
- **4 levels** defined as an incrementally-adoptable progression with SLSA-style independent declaration:
  - **L1 · Identify** — OCI labels
  - **L2 · Trust** — `/r2k/*` snapshots
  - **L3 · Understand** — cross-asset diff (`change.yaml`)
  - **L4 · Share** — cross-asset insight & registry / badge
- **Mode A / Mode B AB plan** for L3 computation timing (pre-computed vs on-demand), with the recommended dual-mode setup for hybrid customer-side topologies.

### 🏷️ L1 · Identity

- Standardized OCI label set under `com.releaseasknowledge.*` (reverse-DNS of `releaseasknowledge.com`):
  `version`, `level`, `commit`, `build-time`, `repo`, `snapshot.path`, `snapshot.index`, `diff.mode`, `diff.from`, `spec.url`.
- Documented the **two-group label model** — OCI standard labels (`org.opencontainers.image.*`) + R2K-specific labels (`com.releaseasknowledge.*`) — so images stay native to existing container tooling while opting into R2K.

### 📦 L2 · Trust

- Standard `/r2k/` snapshot directory: `meta/`, `api/`, `db/`, `config/`, `sbom/`, `runtime/`.
- **`/r2k/index.yaml`** introduced as the snapshot entry index (schema `releaseasknowledge.com/index/v1`) with `image`, `r2k`, `assets[]`, `extensions[]` blocks; per-asset `sha256` for tamper detection; vendor extensions via `x-yourco-*`.
- Designed for **integration with existing collectors** (Atlas, Syft / CycloneDX, OpenAPI generators, Helm) rather than reinventing them.

### 🔍 L3 · Understand

- Unified `change.yaml` schema covering `api / db / config / dependency / runtime` with `severity`, `plugin`, `detail`.
- **Plugin SPI** for per-asset diff plugins (`r2k-diff-openapi`, `r2k-diff-dbschema`, `r2k-diff-config`, `r2k-diff-sbom`, …).
- L3 image labels: `level=3`, `diff.mode`, `diff.from`, `diff.path` to describe the baked manifest's pairing.

### 🧠 L3+/L4 · Share

- Pluggable **insight framework** for cross-asset correlation (LLM, rule engine, policy-as-code).
- Certification & badge: `r2k certify` outputs `level`, `mode` (A / B / A+B), `compliant`, `checked_at`.

### 📚 Documentation

- **English & Traditional Chinese parity** for the entire doc set:
  - `README.md` / `README.zh-tw.md`
  - `docs/{index,quickstart,faq,glossary,manifesto}.md`
  - `docs/zh-tw/{index,quickstart,faq,glossary,manifesto}.md`
  - `AUTHORS.md` / `AUTHORS.zh-tw.md`
- **Quick Start** walks through Step 1 → Step 4 with full label tables (OCI standard + R2K-specific), `/r2k/index.yaml` schema, Mode A label set, recommended adoption order.
- **Glossary** defines the 4-step path, 4 levels, Mode A/B, structured files (`/r2k/index.yaml`, `change.yaml`, `badge.json`), and the plugin SPI / vendor extensions.
- **FAQ** covers concepts, the 4-step path, the AB plan, integration, positioning vs SBOM / SLSA / OpenAPI / Git / observability.

### 🌳 Project metadata

- **`SIGNATURES.md`** added at repo root (English + Traditional Chinese in one file) with sections for Signatories, Adopters, and Challengers.
- **`AUTHORS.md` / `AUTHORS.zh-tw.md`** rewritten to position Ted Enjtorian as Release-as-Knowledge framework observer & primary author.
- **`mkdocs.yml`** rebranded: `site_name: Release-as-Knowledge (R2K)`, repo name & GitHub Pages URL switched to `release-as-knowledge`.
- **License**: CC BY 4.0 for the entire spec, Manifesto, and documentation.

---

**Status**: Public release ✨
**Last updated**: May 2026
