# Authors and Contributors · Release-as-Knowledge v1

## Primary Author

**Ted Enjtorian**
*R2K framework observer & primary author*

- **LinkedIn**: <https://tw.linkedin.com/in/enjtorian>
- **GitHub**: [@enjtorian](https://github.com/enjtorian)

### Contributions

- **Framework conception & theory**: Identified the missing semantic layer for software releases — the gap that today is sliced across many separate tools — and named it R2K (Release-as-Knowledge).
- **4-Step adoption path**: Turned R2K from a concept into an incrementally adoptable progression of 4 levels — LABEL → Snapshot → Diff → Insight, in the spirit of SLSA tiers.
- **Manifesto and AB plan**: Authored the R2K Manifesto v1 (8 principles), and designed the Mode A (pre-computed) / Mode B (on-demand) duality for L3 computation timing.
- **Spec and documentation**: English / Traditional Chinese specs, Quick Start, FAQ, Glossary, Manifesto and other core documents.

### Background

I am a software systems architect with over 20 years of experience. Over the past decade I watched CI/CD, containers, SBOM, OpenAPI, and observability each mature into their own standards — but one thing was never formalized:

> **"What changed in this release, and what does it mean?"**

Today the answers to that question are scattered across PR descriptions, Slack threads, release-note drafts, and engineers' memory. Downstream consumers — customer-side SREs, support, compliance, auditors — must reconstruct the picture from these fragmented traces.

R2K's design intent is not to invent new tools, but to **name a semantic layer that already exists implicitly in every production system**. It integrates the existing standards (OCI, CycloneDX, OpenAPI, Atlas migration plans, …) and cleanly separates *facts* (L1 LABEL + L2 snapshot) from *intelligence* (L3 diff, L4 insight) — facts live in the image, intelligence is computed by the vendor at the time appropriate to the customer-side topology (Mode A / Mode B).

This is not an invention; it is **putting a name on an overdue structural layer**.

---

## Contributors

R2K is an open standard initiative — community contributions are welcome and will be acknowledged here.

### How to contribute

See [README.md](./README.md) and the five ways to join:

| | Way | Action |
|---|---|---|
| ① | **Sign** | Add your name to [SIGNATURES.md](./SIGNATURES.md) |
| ② | **Adopt** | Start with Step 1, display the R2K Level 1 badge |
| ③ | **Share** | Blog posts, conference talks, real-world cases |
| ④ | **Extend** | Propose vendor-specific extensions (`x-yourco-*`) or diff plugins |
| ⑤ | **Challenge** | Point out where we're wrong — we'll publicly update |

Concrete areas to contribute:

- **Spec evolution** (Manifesto / RFCs)
- **Diff plugins** (OpenAPI / DB schema / config / SBOM …)
- **Collectors** (integrations with existing tools — Atlas, Syft, OpenAPI generators, …)
- **Insight framework extensions** (rule engines, policy-as-code, LLM connectors)
- **CI / CD integrations** (GitHub Action, GitLab CI, Jenkins)
- **Translations** (Manifesto / docs in other languages)
- **Diagrams and visuals** (architecture, 4-step path, Mode A/B comparison)

---

## Acknowledgments

Special thanks to:

- The open-source community for inspiration and feedback (OCI, CycloneDX, OpenAPI, SLSA, Atlas, Syft, …)
- Early adopters who provided valuable insights
- Everyone who challenged earlier drafts — Manifesto Principle 1 itself emerged from being challenged

---

## Citation

If you use R2K in your research or work, please cite:

```
Enjtorian, T. (2026). R2K (Release-as-Knowledge): A Semantic Layer
for Software Releases. https://github.com/enjtorian/release-as-knowledge
```

BibTeX:

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

*This work (the R2K spec, Manifesto, and documentation) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
