# `/analyze --quick` — exploratory tier

**Load trigger:** only when `/analyze` is invoked with `--quick`. Full `/analyze` never needs this file.

Moved verbatim from `SKILL.md` on 2026-09-27 (progressive-disclosure restructure; see `changelog.md`). "Phase 4.1" below refers to `SKILL.md` Phase 4.1; the four standing study-design rules in `SKILL.md` bind this tier too (L089 dictionary definitions, L090 named denominators).

---

## `/analyze --quick` — exploratory tier (per L058)

**Purpose.** A deliberately lightweight path for exploratory looks (a single 2×2, one KM curve, a quick descriptive contrast) and for the moment you would otherwise abandon the plugin and hand-run Python. It keeps the load-bearing rigor — a reproducible seeded run and inline verification — while dropping the full halt ladder. It exists so that "quick" never means "outside the plugin" (the manual-execution reliability gap).

**Invoke:** `/analyze --quick "<one pre-named contrast>"`. What runs:

```
resource check (light)
→ single analysis with random_state=42 (appropriate test by outcome class, per Phase 4.1)
→ ✓ INLINE verify (science-superpowers:verifying-results-before-claiming): fresh re-run, read estimate + 95% CI + p, confirm reproduction
→ write the result to the EXPLORATORY log ONLY (never to SCAR) → one concise result card → STOP
```

**Where the number goes — the structural firewall (closes the laundering path).** A `--quick` result is written **only** to `Reports/exploratory_quick_log.md` (+ `exploratory_quick_log.json`), tagged `mode=quick`, `evidence_class=EXPLORATORY-UNGATED`, `literature_vetted=false`, carrying the contrast, seed, estimate, 95% CI, and p. It is **never** written to `MASTER_ANALYSIS_REGISTRY.json` / SCAR, nor to any Master Excel tab. Because L045 makes the SCAR registry the **sole** source for every manuscript and abstract number, keeping quick results out of it makes an exploratory estimate **structurally ineligible** for a manuscript — the exclusion is enforced by the artifact boundary, not by a banner. `write-abstract` / `write-manuscript` read SCAR and never the exploratory log. (Do **not** call `scripts/analysis_registry.py` in `--quick` mode; its schema has no exploratory field and writing there would defeat the firewall.)

**`EXPLORATORY-UNGATED` is not an L035 tier.** The HALT 3 evidence tiers (1–4, per L035) are an *earned, post-audit* partition defined by which multiple-testing correction a result survives across the full family of tests. A `--quick` run has no family, no BH-FDR/Bonferroni, and no red-team audit, so it has **no L035 tier at all**. It carries the orthogonal provenance class `EXPLORATORY-UNGATED` — never "Tier 4" — so a quick result and a genuinely-earned Tier-4 result are never conflated.

**Dropped vs. full `/analyze`:** Phase 0 lit-recon hard gate, HALT 0/1/2/2A/2B/3, Master Excel scaffolding + shell sign-off, the red-team subagent, SCAR registration, and the 16-section report. **Never dropped:** the random seed, the inline verification re-run, the dictionary definition of any coded variable the contrast uses (L089), and a named denominator for any proportion (L090).

**Hard guardrails:**

- A `--quick` result is `EXPLORATORY-UNGATED`, is **forbidden from any abstract, table, or manuscript primary/secondary result**, and carries no `novelty_assessment` — it **must not seed a `study_spec`** or any confirmatory artifact. The result card banner states this, but the real barrier is that the number never enters SCAR (above).
- **No adjusted / matched / weighted models** in `--quick` — those require the HALT 2A variable-approval gate. If the question needs adjustment, `--quick` refuses and points to full `/analyze`.
- **One contrast only** — a single pre-named comparison, no multiple-testing family. Needing several is the signal to switch to full `/analyze`.
- **Promotion path:** to turn a `--quick` finding into a manuscript result, run the full `/analyze` pipeline (Phase 0 → HALT 3); it re-derives the number under a HALT 1-approved, audited plan and writes it to SCAR. The exploratory log records the question so the confirmatory run can reference what prompted it.
