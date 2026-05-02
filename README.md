# Release-as-Knowledge (R2K)

![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)
![Version](https://img.shields.io/badge/spec-v1-2874A6.svg)
![Status](https://img.shields.io/badge/status-public%20draft-B7791F.svg)

> Turn every release from "shipping a binary" into "a structured, machine-indexable knowledge transfer".

🌐 **Website**: <https://enjtorian.github.io/release-as-knowledge>
📜 **Manifesto**: [docs/manifesto.md](./docs/manifesto.md) ・ [繁體中文](./docs/zh-tw/manifesto.md)
🇹🇼 **繁體中文 README**: [README.zh-tw.md](./README.zh-tw.md)

---

## Why R2K?

Over the past decade we have pipelined "**how to ship code**" beautifully: CI/CD, containers, GitOps, SBOM, observability — every layer has mature tooling.

But one thing was never standardized:

> ❌ **"What changed in this release, and what does it mean?"**

Today the answer lives in PR descriptions, Slack threads, engineers' memory, and hand-written release notes. Downstream consumers — customer-side SREs, support engineers, auditors, compliance teams — have to reconstruct it from these fragmented traces.

R2K argues: **a release should be a knowledge transfer, not just a binary handoff**.

---

## R2K's 4-Step adoption path (v1)

R2K does not require you to do everything at once. It is an **incrementally adoptable** path mapped to 4 levels, and **each step can be independently declared as done**:

```text
  Step 1                Step 2                  Step 3                  Step 4
┌─────────┐          ┌─────────────┐         ┌──────────────┐        ┌──────────────┐
│ LABEL   │   →      │ Snapshot    │   →     │ Diff         │   →    │ Insight      │
│ L1      │          │ L2          │         │ L3           │        │ L3+ / L4     │
│ Identify│          │ Trust       │         │ Understand   │        │ Share        │
└─────────┘          └─────────────┘         └──────────────┘        └──────────────┘
   identity           asset auto-collection    cross-asset diff       cross-asset insight
   (a few labels)     (OpenAPI/DB/Config/SBOM) (diff plugin SPI)      (insight framework)
```

### Step 1 · Docker LABEL (L1 · Identify)

Attach OCI labels to the image so anyone can `docker inspect` and read the facts — using both **OCI standard labels** (`org.opencontainers.image.*`) and **R2K-specific labels** (`dev.releaseasknowledge.*`).

```dockerfile
LABEL org.opencontainers.image.revision="${COMMIT_SHA}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"
LABEL org.opencontainers.image.source="https://github.com/your-org/your-repo"

LABEL dev.releaseasknowledge.version="1.0"
LABEL dev.releaseasknowledge.level="1"
LABEL dev.releaseasknowledge.commit="${COMMIT_SHA}"
LABEL dev.releaseasknowledge.build-time="${BUILD_TIME}"
```

A few extra lines of Dockerfile, no new tooling required, no registry change.

### Step 2 · Automated asset collection (L2 · Trust)

At build time, automatically dump the "facts" every release uses, ship them with the image, and list them in `/r2k/index.yaml`:

| Asset | Source / collector |
|---|---|
| `api/openapi.json` | API runtime / SDK generator |
| `db/schema.sql` | Atlas, Flyway, Liquibase |
| `config/env.json` | Service config templating |
| `sbom/sbom.json` | Syft / CycloneDX |
| `runtime/manifest.yaml` | Helm / K8s manifest |
| `index.yaml` | Snapshot entry index (schema + sha256 per asset) |

This step **needs many automated collectors**. R2K specifies file location and schema, but does not bind to the tools that produce them.

### Step 3 · Cross-asset diff & light insight (L3 · Understand)

Given two releases' L2 snapshots, you can do **cross-asset diff**:

- API: which endpoint was removed? which query param became required?
- DB: which migration changed a NOT NULL constraint? which index was dropped?
- Config: which env became required? which was deprecated?
- Dependency: did log4j jump majors? what CVEs got introduced?

This step **needs many diff plugins** (each asset has its own diff rules). R2K writes diff results into a unified `change.yaml` with severity. Downstream consumers consume the same schema.

### Step 4 · Insights · cross-asset analysis (L3+ / L4 · Share)

Single diffs aren't enough — **the cross-asset correlation is where insight lives**:

- API removed `GET /users` + DB renamed the `users` table → same change surface, broader impact
- A new dependency's CVE + that dependency appears in OpenAPI handlers → external attack surface widened
- A config toggle's default flips + the code path it controls has a migration → upgrade requires a maintenance window

R2K v1 provides a **pluggable insight framework** at this layer: connect to LLMs, rule engines, or your team's existing risk policy. Every insight is grounded on facts collected in steps 1-3.

---

## Each layer is independently declarable, with tools & validation

| Step | Level | Tooling (v1 plan) | Validation |
|---|---|---|---|
| 1 | L1 Identify | `r2k label`, `docker inspect` | `r2k validate identity` |
| 2 | L2 Trust | `r2k snapshot` (OpenAPI / DB / Config / SBOM collectors) | `r2k validate state` |
| 3 | L3 Understand | `r2k diff A B` (diff plugin SPI) | `r2k validate change` |
| 4 | L3+/L4 Share | `r2k insight`, `r2k explain`, registry, badge | `r2k certify` |

Just like SLSA tiers, **every level can be declared independently** — no one is forcing you to climb all four at once.

---

## v1's AB plan · when do we compute the L3 diff?

R2K v1 deliberately does not prescribe one answer to "when is the diff computed". It defines two modes:

### Mode A · Pre-computed
- The Change Manifest is computed in CI and **attached to the image**
- Customer side does not need a Diff Engine service
- ✅ Best for **air-gapped / on-prem ISVs**

### Mode B · On-demand
- CI attaches only L1 + L2 snapshots
- The Diff Engine computes at query time, **any from→to combination is queryable**
- ✅ Best for **SaaS / connected enterprise / open-source tools**

### Both modes (recommended)
- The image carries Mode A's default-pair manifest
- L2 snapshots are kept complete, allowing Mode B to recompute any other combination

| Dimension | Mode A | Mode B | Both |
|---|---|---|---|
| Air-gap friendly | ✅ Perfect | ❌ Service required | ✅ |
| Arbitrary from→to | ❌ Locked | ✅ Full | ✅ |
| Auto-benefit from rule updates | ❌ Needs rebuild | ✅ Automatic | △ Partial |
| CI integration complexity | ✅ Simple | ✅ Simple | △ Medium |
| Customer-side complexity | ✅ Simple | △ Connection required | △ Path-dependent |

> **Principle 1** ("artifact carries facts, not intelligence") makes both modes legitimate — the facts live in the image, *when* the intelligence is computed is a vendor decision.

---

## R2K is NOT

- **R2K is not SBOM** — SBOM is a subset of L2
- **R2K is not SLSA** — SLSA solves build security; R2K solves change communication
- **R2K is not release notes** — release notes are a derived byproduct; R2K is the structured primary product
- **R2K is not a tool** — R2K is a framework + naming + adoption standard, not bound to any implementation

---

## In one line

> Git tells you what changed in code.
> Docker tells you what is deployed.
> SBOM tells you what's inside.
> **R2K tells you "what changed in the system, and what it means."**

---

## 5 ways to join

| | Way | Action |
|---|---|---|
| ① | **Sign** | Add your name to [SIGNATURES.md](./SIGNATURES.md) |
| ② | **Adopt** | Start with Step 1, display the R2K Level 1 badge |
| ③ | **Share** | Blog posts, conference talks, real-world cases |
| ④ | **Extend** | Propose vendor-specific extensions (`x-yourco-*`) or diff plugins |
| ⑤ | **Challenge** | Point out where we're wrong — we'll publicly update |

---

## Documentation map

- [📜 R2K Manifesto v1](./docs/manifesto.md) ・ [繁體中文](./docs/zh-tw/manifesto.md)
- [📘 docs/index.md — full introduction](./docs/index.md)
- [🚀 docs/quickstart.md — 5 minutes to Level 1](./docs/quickstart.md)
- [❓ docs/faq.md — frequently asked questions](./docs/faq.md)
- [📖 docs/glossary.md — glossary](./docs/glossary.md)
- [👥 AUTHORS.md — authors & contributors](./AUTHORS.md)

---

## License

The entire R2K spec, Manifesto, and this document are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Share, adapt, use commercially — only requirement is attribution.

---

> **The past decade pipelined our code.**
> **The next decade will pipeline what surrounds it.**
>
> That's what R2K v1 is for.

*Release-as-Knowledge v1 · 2026-05 · CC BY 4.0*
