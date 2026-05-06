---
title: R2K v1 · Release-as-Knowledge
description: R2K (Release-as-Knowledge) turns every software release from a binary handoff into a structured, machine-indexable knowledge transfer. 4 incremental adoption steps and a v1 AB plan for L3 computation.
tags: [r2k, manifesto, release, semantic-layer]
keywords: R2K, Release-as-Knowledge, OCI, SBOM, OpenAPI, change manifest, diff plugin, insight
author: Ted Enjtorian
date: 2026-05
---

# Release-as-Knowledge (R2K)

*Release-as-Knowledge specification v1 · May 2026*

---

## In one line

> Git tells you **what changed in code**. Docker tells you **what is deployed**. SBOM tells you **what's inside**.
> **R2K tells you "what changed in the system, and what it means."**

R2K is a semantic standard that upgrades every software release from a non-machine-readable artifact into a **structured, queryable, reasoning-friendly knowledge object**.

---

## Why we need it

Over the past decade, the *delivery* side of software has been heavily standardized: CI/CD, containers, GitOps, SBOM, observability — every layer has mature tooling.

But one thing was never formalized:

> ❌ **"What changed in this release? What does it mean? What should I do about it?"**

Today the answers to that question are scattered across:

- PR descriptions, Slack threads, engineers' memory
- Hand-written release notes
- Siloed SBOM, API diff, DB diff tools

**Downstream consumers** — customer-side SREs, support engineers, auditors, compliance teams — must reconstruct the picture from these fragmented traces. R2K argues that this can and should change.

---

## The 4-Step adoption path

R2K's core move is to take today's "ship a binary" release flow and **upgrade it into four incrementally-adoptable steps**:

```text
  Step 1                Step 2                  Step 3                  Step 4
┌─────────┐          ┌─────────────┐         ┌──────────────┐        ┌──────────────┐
│ LABEL   │   →      │ Snapshot    │   →     │ Diff         │   →    │ Insight      │
│ L1      │          │ L2          │         │ L3           │        │ L3+ / L4     │
│ Identify│          │ Trust       │         │ Understand   │        │ Share        │
└─────────┘          └─────────────┘         └──────────────┘        └──────────────┘
   identity            asset collection         cross-asset diff       cross-asset insight
```

Each step:

- **Can be independently declared** (like SLSA tiers)
- **Has its own tooling** (CLI / collector / plugin / insight framework)
- **Has its own validation** (`r2k validate <layer>`)
- **Can be deferred** until the team is ready for the next one

### Step 1 · Docker LABEL (L1 · Identify)

**What you do**: attach OCI labels to the image to declare the release's identity — using both OCI standard labels (`org.opencontainers.image.*`) and R2K-specific labels (`com.releaseasknowledge.*`).

```dockerfile
LABEL org.opencontainers.image.revision="${COMMIT_SHA}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"
LABEL org.opencontainers.image.source="https://github.com/your-org/your-repo"

LABEL com.releaseasknowledge.version="1.0"
LABEL com.releaseasknowledge.level="1"
LABEL com.releaseasknowledge.commit="${COMMIT_SHA}"
LABEL com.releaseasknowledge.branch="${GIT_BRANCH}"
LABEL com.releaseasknowledge.tag="${GIT_TAG}"
LABEL com.releaseasknowledge.build-time="${BUILD_TIME}"
```

**Value**: a few lines of Dockerfile, no registry change, no framework change. Anyone can `docker inspect` to read the facts.
**Validation**: `r2k validate identity <image>`.

### Step 2 · Automated asset collection (L2 · Trust)

**What you do**: at build time, automatically dump the "facts" every release uses, ship them with the image, and list them in `/r2k/index.yaml`.

| Asset | Default location | Source / collector |
|---|---|---|
| OpenAPI spec | `/r2k/api/openapi.json` | API runtime auto-dump, SDK generators |
| DB schema | `/r2k/db/schema.sql` | Atlas / Flyway / Liquibase export |
| Config & env template | `/r2k/config/env.json` | Service config template serialization |
| SBOM | `/r2k/sbom/sbom.json` | Syft / CycloneDX |
| Runtime manifest | `/r2k/runtime/manifest.yaml` | Helm / K8s manifest |
| Identity meta | `/r2k/meta/manifest.json` | CI-injected (commit / branch / build time) |
| **Snapshot index** | `/r2k/index.yaml` | `r2k snapshot index ...` |

**This step needs many automated collectors**. R2K specifies **placement and schema**, not the collectors themselves — already using Atlas, Syft, OpenAPI generator? Great, just point their output at the corresponding `/r2k/` location.

**Validation**: `r2k validate state <image>` — schema check, required-field check, consistency with L1.

### Step 3 · Cross-asset diff & light insight (L3 · Understand)

**What you do**: diff two releases' L2 snapshots **across assets**, producing a unified `change.yaml`.

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

**This step needs many diff plugins** — because each asset has its own diff semantics:

- `r2k-diff-openapi` — REST breaking-change detection
- `r2k-diff-dbschema` — DDL changes, NOT NULL / index impact
- `r2k-diff-config` — required / deprecated / default-flip
- `r2k-diff-sbom` — added / upgraded / known-CVE introduction

R2K provides a plugin SPI (Service Provider Interface): you can write a plugin for your in-house protocol, and as long as the output follows the `change.yaml` schema, downstream consumers see it the same way.

**Validation**: `r2k validate change change.yaml`.

### Step 4 · Insights · cross-asset analysis (L3+ / L4 · Share)

**What you do**: lift "single diffs" up to "cross-asset correlation" and "share across organizations".

A single diff tells you what changed in API, DB, or SBOM individually; **insight** tells you the causal and risk relationships between them:

- `GET /users` removed + `users` table renamed → **same change surface**, must be communicated together
- new dependency CVE + that dependency appears in OpenAPI handler → **expanded external attack surface**
- a config toggle's default flips + the code path it controls has a migration → **upgrade requires a maintenance window**

R2K v1 provides a **pluggable insight framework** at this layer:

- Connect to LLMs (release summaries / risk explanations)
- Connect to rule engines (policy-as-code)
- Connect to your team's existing risk policy

**Every insight is grounded on the facts collected in steps 1-3** — never fabricated.

**Validation / certification**: `r2k certify <image>` produces a badge (L1 / L2 / L3 / L4).

---

## The v1 key design: AB plan · when do we compute L3?

R2K v1 deliberately does **not** prescribe a single answer to "when is the diff computed". It defines **two modes**, vendor chooses based on customer-side topology:

### Mode A · Pre-computed

- The Change Manifest is computed in CI and **attached to the image**
- Customer side does not need a Diff Engine service
- ✅ Best for **air-gapped / on-prem ISVs**

### Mode B · On-demand

- CI attaches only L1 + L2 snapshots
- The Diff Engine computes the manifest at query time, **any from→to combination is queryable**
- ✅ Best for **SaaS / connected enterprise / open-source tools**

### Both modes (recommended)

- The image carries Mode A's "default-pair" manifest (covers air-gap)
- L2 snapshots remain complete, allowing Mode B to recompute any combination (covers rule upgrades)

| Dimension | Mode A | Mode B | Both |
|---|---|---|---|
| Air-gap friendly | ✅ Perfect | ❌ Service required | ✅ |
| Arbitrary from→to | ❌ Locked to default | ✅ Full | ✅ |
| Auto-benefit from rule updates | ❌ Needs rebuild | ✅ Automatic | △ Partial |
| CI integration complexity | ✅ Simple | ✅ Simple | △ Medium |
| Customer-side complexity | ✅ Simple | △ Connection required | △ Path-dependent |
| Best fit | ISV / on-prem | SaaS | Hybrid |

> Why can v1 hold both modes at once? Because **Principle 1** ("artifact carries facts, not intelligence") cleanly separates facts (L1+L2) from intelligence (L3) — the facts live in the image, *when* the intelligence is computed is a vendor decision.

---

## R2K's core model

```text
Release = Identity + State + ChangeSet
            ↑          ↑          ↑
            L1         L2         L3
          facts      facts    intelligence
```

| Layer | Nature | Stored where | Verb |
|---|---|---|---|
| **Identity** | facts | OCI labels | Identify |
| **State** | facts | `/r2k/*` snapshots | Trust |
| **Change** | intelligence | `change.yaml` (pre-computed or on-demand) | Understand |
| **Insight** | intelligence on intelligence | plugins / LLM | Share |

L1 + L2 form the **fact layer** (in the image), L3 is the **computation layer** (derived from facts), L4 is the **social layer** (sharing insight across organizations).

---

## Relationship to other standards

| Layer | System | Relationship |
|---|---|---|
| code | Git | R2K does not redo it — Git speaks code change |
| artifact | Docker / OCI | R2K does not redo it — Docker is a carrier |
| dependency | SBOM (CycloneDX / SPDX) | **Subset of R2K L2** |
| build security | SLSA | Complementary — SLSA solves build security; R2K solves change communication |
| API contract | OpenAPI | **Part of R2K L2**, plugged into L3 via diff plugin |
| runtime | Datadog / Grafana | Complementary — observability tells you "what is happening now"; R2K tells you "what changed between versions" |

> R2K does not compete with existing tools. **It is the semantic layer that connects them.**

---

## Where to start

1. **5 minutes to Level 1** → [Quick Start](./quickstart.md)
2. **Understand the motivation and philosophy** → [R2K Manifesto v1](./manifesto.md)
3. **Stuck on something** → [FAQ](./faq.md)
4. **Term you don't recognize** → [Glossary](./glossary.md)
5. **Want to put your name on it** → [SIGNATURES.md](../SIGNATURES.md)

---

## R2K is / is not

✅ R2K **is**:

- A framework + naming + adoption standard
- An **integration layer** for existing OCI / SBOM / OpenAPI / migration tooling
- Incrementally adoptable, with each layer independently declarable
- CC BY 4.0 — open licensing

❌ R2K **is not**:

- A product or a SaaS
- Something that wants to replace your CI/CD
- A competitor to SBOM (SBOM is a subset of L2)
- An all-or-nothing leap that you must complete in one go

---

> **The past decade pipelined our code.**
> **The next decade will pipeline what surrounds it.**
>
> That's what R2K v1 is for.

*Release-as-Knowledge v1 · 2026-05 · CC BY 4.0*
