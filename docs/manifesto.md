---
title: The R2K Manifesto v1 · Release-as-Knowledge
description: R2K v1 design thesis — 8 principles, 4 levels, and the Mode A/B AB plan for L3 computation. CC BY 4.0.
tags: [r2k, manifesto, release-as-knowledge]
keywords: R2K, Manifesto, Release-as-Knowledge, OCI, SBOM, OpenAPI
author: Ted Enjtorian
date: 2026-05
---

# The Release-as-Knowledge Manifesto · v1

> **Release-as-Knowledge**
> 8 Principles · 4 Levels · Mode A/B · CC BY 4.0

---

## We believe

A software release should be **a knowledge transfer, not just a binary handoff**.

When a team builds a release, it accumulates a great deal of implicit knowledge:

- Which APIs changed, which are breaking
- Which DB migrations are dangerous and need a maintenance window
- Which configs are now required, which are deprecated
- Which breaking changes affect which customers

**This knowledge does not currently ship with the image.** It stays in PR descriptions, Slack threads, and engineers' memory.

Downstream consumers — support engineers, customer DevOps teams, auditors, compliance teams — must reconstruct it from these fragmented traces. **We believe this can and should change.**

---

## 8 Principles

### 1. Artifact carries facts, not intelligence

The OCI image should store L1 (LABELs) + L2 (snapshots: API spec, DB schema, config) — these are **facts**.
L3 (Change Manifest) is **intelligence** — computed from facts, not baked into the image.

This mirrors two mature designs:
- **git**: commits store snapshots, diffs are computed
- **SBOM**: stores component lists, vulnerability scans are computed

**R2K does to OCI images what git does to source code**: facts live in the artifact, intelligence is derived.

### 2. Knowledge ships with the artifact

Knowledge cannot live only in PR descriptions. It must travel with the image, be machine-indexable, and be consumable by non-developers.

### 3. Implicit becomes explicit

What is trivial to engineers is a landmine to customers. R2K forces this knowledge to be structured and machine-readable.

### 4. Standards over invention

OCI, CycloneDX, OpenAPI, Atlas migration plans — industry standards that have been running for years. R2K's schema integrates these existing standards rather than inventing new formats.

### 5. Designed for non-developers

R2K serves support engineers, customer DevOps, auditors, and compliance teams — not the developers themselves.

### 6. Layered by query frequency

90% high-frequency lightweight queries use LABELs (~50ms). 10% low-frequency heavy queries use metadata layers (~300ms). 1% deep-detail queries use the full Change Manifest.

### 7. Compatible with existing pipelines

No CI/CD rewrite, no registry change, no framework swap required. Start with 5 lines of Dockerfile changes at Level 1. **Adopt incrementally.**

### 8. Manifests are the lingua franca

Structured yaml/json bridges tools, organizations, and human/machine readability.

---

## 4-Step Adoption Path · 4 Levels

R2K provides an **incremental adoption** path:

| Step | Level | Name | Verb | Nature | Cost | Independently declarable |
|---|---|---|---|---|---|---|
| 1 | **L1** | Identify | LABEL | facts | 1-2 weeks | ✓ |
| 2 | **L2** | Trust | Snapshot | facts | 2-3 weeks | ✓ |
| 3 | **L3** | Understand | Diff | **intelligence** | 6-8 weeks | ✓ |
| 4 | **L4** | Share | Insight / Distribute | social | 4 weeks | ✓ |

- L1+L2 are the **fact layer** — stored in the image
- L3 is the **computation layer** — derived from L1+L2
- L4 is the **social layer** — sharing insight across organizations

Like SLSA's tier system, **each level can be independently declared.**

### One-line summary

> **L1 = Identify · L2 = Trust · L3 = Understand · L4 = Share**

### What each step needs

- **Step 1 (L1)**: OCI labels — 5 lines of Dockerfile to start.
- **Step 2 (L2)**: **Many automated collectors** (OpenAPI / DB schema / config / SBOM, each with its own collector). R2K specifies placement and schema, not the collectors themselves.
- **Step 3 (L3)**: **Many diff plugins**, because diff rules differ per asset. R2K provides the plugin SPI; outputs all share one `change.yaml` schema.
- **Step 4 (L3+/L4)**: Cross-asset insight. R2K provides a pluggable insight framework (LLM, rule engine, policy-as-code).

---

## Two modes for L3 computation · the v1 AB plan

L3 is derived — but **when** it gets derived has two options:

### Mode A · Pre-computed
- Change Manifest computed in CI and attached to the image
- No Diff Engine service required on the customer side
- ✅ Best for: **air-gapped on-prem ISVs**

### Mode B · On-demand
- CI attaches only L1+L2 snapshots
- Diff Engine computes the manifest at query time
- Any from→to combination is queryable
- ✅ Best for: **SaaS / connected enterprise / open-source tools**

### Both modes (recommended)
- The image carries Mode A's default-pair manifest
- L2 snapshots remain complete, allowing Mode B to recompute any combination
- Both customer types benefit

### Trade-off matrix

| Dimension | Mode A | Mode B | Both |
|---|---|---|---|
| Air-gap friendly | ✅ Perfect | ❌ Service required | ✅ |
| Arbitrary from→to | ❌ Locked | ✅ Full | ✅ |
| Auto-benefit from rule updates | ❌ Needs rebuild | ✅ Automatic | △ Partial |
| CI integration complexity | ✅ Simple | ✅ Simple | △ Medium |
| Customer-side complexity | ✅ Simple | △ Connection required | △ Path-dependent |
| Best for | ISV / on-prem | SaaS | Hybrid |

R2K **as a framework does not prescribe which** — but **Principle 1 (facts vs intelligence) makes both modes legitimate**.

The choice depends on whether your customer side can connect to your service.

---

## What R2K is NOT

- **R2K is not SBOM** (SBOM is a subset of L2)
- **R2K is not SLSA** (SLSA solves build security; R2K solves change communication)
- **R2K is not release notes** (release notes are a derived byproduct; R2K is the structured primary product)
- **R2K is not a tool** (R2K is a framework + naming + adoption standard, not tied to any specific implementation)

---

## 5 ways to join

| | Way | Action |
|---|---|---|
| ① | **Sign** | Add your name to SIGNATURES.md |
| ② | **Adopt** | Start with Step 1 (L1), display the R2K Level 1 badge |
| ③ | **Share** | Blog posts, conference talks, real-world cases |
| ④ | **Extend** | Propose vendor-specific extensions (`x-yourco-*`) or diff plugins |
| ⑤ | **Challenge** | Point out where we're wrong — we'll publicly update |

The fifth way matters — Principle 1 itself was added because someone challenged the earlier draft.
**A manifesto is something that gets refined by being challenged.**

---

## License & Reproduction

This Manifesto is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Share, adapt, use commercially — only requirement is attribution.

---

> **The past decade pipelined our code.**
> **The next decade will pipeline what surrounds it.**
>
> That's what R2K v1 aims to do.

---

*Release-as-Knowledge Manifesto v1 · 2026-05 · CC BY 4.0*
