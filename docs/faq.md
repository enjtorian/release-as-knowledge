# FAQ · Release-as-Knowledge v1

Frequently asked questions about R2K (Release-as-Knowledge).

---

## 1. Concepts

### Q: What is R2K?

R2K (**Release-as-Knowledge**) is a semantic standard that upgrades every software release from a non-machine-readable binary into a **structured, machine-indexable, reasoning-friendly knowledge object**.

It is composed of four incremental adoption steps:

1. **LABEL · Identify** (OCI labels declare identity)
2. **Snapshot · Trust** (OpenAPI / DB / Config / SBOM auto-collected)
3. **Diff · Understand** (cross-asset diff plugins)
4. **Insight · Share** (cross-asset correlation insight)

### Q: Isn't R2K just SBOM?

No. **SBOM is a subset of R2K L2** (it covers the dependency dimension only). R2K L2 also includes OpenAPI, DB schema, config, etc., and L3 adds cross-asset diff and insight on top.

### Q: Isn't R2K just SLSA?

No. SLSA solves **build security** (was this binary produced by trusted people in a trusted environment?). R2K solves **change communication** (what changed in this release, and what does it mean?). They are **complementary**.

### Q: Aren't release notes already enough?

No. Release notes are a **derived byproduct** (a human-written description). R2K is the **primary product** (the structured, machine-consumable facts plus intelligence). Release notes can be auto-rendered from R2K — the reverse is not possible.

### Q: Is R2K a tool?

R2K **is not a tool**. It is a framework + naming + adoption standard, licensed CC BY 4.0, not tied to any particular implementation. Multiple tools may implement R2K (CLI / SDK / collectors / plugins).

### Q: What does "v1" mean? Where did the previous versions go?

All v1 / v2 drafts under `00-idea/` are treated as **drafts**. The version we are publishing now is **R2K v1**.

---

## 2. The 4-Step adoption path

### Q: Why split into four steps? Why not ship one big spec?

Because **real teams won't adopt everything in one go**. R2K mirrors the SLSA tier design: each step is independently declarable and delivers value on its own. Step 1 takes 5 lines of Dockerfile; Step 4 needs a rule engine or LLM.

### Q: Why does Step 2 say "needs many automated collectors"?

Because every asset (OpenAPI, DB schema, config, SBOM…) already has its own best-of-breed collection tool:

- OpenAPI → your framework / SDK generator
- DB schema → Atlas, Flyway, Liquibase
- SBOM → Syft, CycloneDX
- config → your own config templating

R2K does not redo any of these tools. **It specifies where their outputs go and what shape they take**, so L3 can diff across them.

### Q: Why does Step 3 need many diff plugins?

Because "diff" means different things for different assets:

- API diff = breaking-change detection (path removal, required fields, type narrowing)
- DB diff = migration risk (NOT NULL, index impact, long-table ALTER)
- SBOM diff = added / upgraded / known-CVE introduction
- Config diff = required / deprecated / default-flip

Each diff rule can be an independent plugin. R2K provides a plugin SPI (Service Provider Interface) so the community and vendors write diff plugins for their own asset types, but **the output uniformly follows the `change.yaml` schema**.

### Q: How is Step 4's insight different from Step 3's diff?

- **Diff (Step 3) = what changed within a single asset** (what changed in the API, in the DB, etc.)
- **Insight (Step 4) = correlation and meaning across assets** (API removed + DB rename → same change surface, broader impact)

Insight is always grounded on diffs — never invented out of thin air.

---

## 3. The AB plan · when L3 is computed

### Q: What are Mode A and Mode B?

R2K v1 designs **two modes** for *when* the L3 diff gets computed:

- **Mode A · Pre-computed** — the Change Manifest is built in CI and attached to the image. ✅ Best for air-gap / on-prem.
- **Mode B · On-demand** — CI attaches only L1+L2 snapshots; the Diff Engine computes at query time. ✅ Best for SaaS / arbitrary-combination queries.

### Q: Why does v1 hold both modes? Why not pick one?

Because vendors face different customer-side topologies:

- An ISV selling on-prem software to government or banks → customer side has no internet, only Mode A works
- A SaaS or open-source vendor → any from→to combination may be queried, Mode B is the natural fit

R2K's **Principle 1** ("artifact carries facts, not intelligence") cleanly separates facts (L1+L2) from intelligence (L3) — the facts live in the image; the vendor decides when intelligence is computed.

### Q: What does "both modes" mean in practice?

- The image carries Mode A's "default-pair" manifest (so air-gap customers can read it directly)
- L2 snapshots are kept complete (so connected customers can recompute other combinations via Mode B)

This is the **recommended** approach in practice, but it asks slightly more of CI integration.

### Q: What if Mode A's manifest goes stale?

A Mode A Change Manifest is "frozen" into the image at compute time. If the diff plugin rules later improve (e.g. a newly recognized CVE pattern), Mode A doesn't auto-benefit — you'd need to rebuild a new image. Mode B always gets the latest rules. That trade-off is part of the choice.

---

## 4. Implementation & integration

### Q: Do I have to change my CI/CD?

**No rewrite required**. R2K is additive instrumentation:

- Step 1 is just adding ~5 `LABEL` lines
- Step 2 is running a few more collectors at build time and `COPY`ing the output into the image
- Step 3 is running the diff CLI at build time (Mode A) or query time (Mode B)

No framework swap, no registry change, no deployment-flow change.

### Q: Does R2K conflict with OpenAPI / SBOM / Atlas / Helm?

Not at all. One of R2K's design principles is **"standards over invention"** — it integrates the existing fact formats rather than inventing new ones. Already using Atlas for schema, Syft for SBOM, OpenAPI generators? Great — point their output at the corresponding `/r2k/` location.

### Q: What tools and validation does each layer need?

| Step | Level | Primary tooling (v1 plan) | Validation |
|---|---|---|---|
| 1 | Identify | `r2k label`, `docker inspect` | `r2k validate identity` |
| 2 | Trust | `r2k snapshot` (OpenAPI / DB / Config / SBOM collectors) | `r2k validate state` |
| 3 | Understand | `r2k diff A B` (diff plugin SPI) | `r2k validate change` |
| 4 | Share | `r2k insight`, `r2k certify` | `r2k certify` |

### Q: How does the badge work?

```bash
r2k certify your-image:tag --output badge.json
```

The output includes level (1/2/3/4), mode (A/B/A+B), compliance status, and check time. Embed in README or internal dashboards.

### Q: Can I write diff plugins for internal / proprietary assets?

Yes. R2K provides a plugin SPI; as long as the output follows the `change.yaml` schema, it integrates downstream. Use the `x-yourco-*` naming prefix to avoid collision with future standard plugins.

---

## 5. Positioning & comparison

### Q: How does R2K relate to Git?

Git speaks "**what changed in code**". R2K speaks "**what changed in the system, and what it means**". R2K's Principle 1 mirrors git's design: commits store snapshots, diffs are computed; R2K does to OCI images what git does to source code.

### Q: How does R2K relate to observability (Datadog / Grafana)?

Observability tells you "**what is happening now**". R2K tells you "**what changed between versions**". Observability is **runtime truth**; R2K is **release-time truth**.

### Q: What is R2K's role in the LLM / AI era?

LLMs are starting to consume releases directly (incident copilots, release reviewers, debug agents, …). They need structured context, not unstructured release notes or chat logs. R2K provides exactly that: **a machine-readable semantic representation of a release**, so AIs can reason deterministically about "which release introduced which risk and which service it affects".

---

## 6. Joining

### Q: How do I join R2K?

| | Way | Action |
|---|---|---|
| ① | **Sign** | Add your name to [SIGNATURES.md](../SIGNATURES.md) |
| ② | **Adopt** | Start with Step 1, display the R2K Level 1 badge |
| ③ | **Share** | Blog posts, conference talks, real-world cases |
| ④ | **Extend** | Propose vendor-specific extensions (`x-yourco-*`) or diff plugins |
| ⑤ | **Challenge** | Point out where we're wrong — we'll publicly update |

### Q: What's the license?

CC BY 4.0. Share, adapt, use commercially — only requirement is attribution.
