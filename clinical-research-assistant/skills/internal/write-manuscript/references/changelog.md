# `write-manuscript` — CHANGELOG / Lessons Learned

**Load trigger:** only when auditing the history of this skill. Never needed to run the skill; `SKILL.md` holds enforcement. Newest first.

---

### 2026-09-27 — One precision per estimate; run-time record dates (L097, L098)
Print an estimate and its CI limits at one number of decimals (the fewest any holds, never below the main text), re-rounded half-up through the boundary guard; never pad stored strings with zeros (3-decimal and 3-significant-figure storage look alike once trailing zeros drop); footnote cells left mixed by an unstored final 5. Scan every table for the class when an audit flags one instance. Record writers stamp dates at run time, never from a fixed constant.

### 2026-09-26 — One formatter, full precision, boundary guard (L091)
Every manuscript surface (text, tables, figures, supplement) renders numbers through one Decimal ROUND_HALF_UP formatter reading full-precision values (registry `current.fp` companions preferred). A boundary guard fails strict builds when a value is printed from a stored rounded number on a rounding boundary (e.g., 0.275 to 2 dp) until a gated full-precision refit is registered. E-values are computed from full-precision inputs. Reference implementation: REPEAT DISPARITIES `Scripts/manuscript_format.py`, `Scripts/render_manuscript_numbers.py --strict`, `Scripts/run_a11_precision.py`.

### 2026-05-03 — HNSCC TAM Multi-Cohort Validation (Bilal Mirza, U Arizona)

- **Manuscript brief precedes manuscript drafting** (L037). For multi-cohort projects, the FINAL manuscript brief is the PI-review artifact; the manuscript drafts against it after PI sign-off.
- **Tier-based claim placement** (L035) — partition every finding into Tier 1–4 BEFORE drafting; the Tier determines where it can appear (abstract / body / discussion-only).
- **Canonical Table 1 = `meta_validation_v2_summary.csv`** (L034) — the 17-finding (or N-finding) summary table from Phase 4 of the rigor remediation pipeline becomes Manuscript Table 1 directly. Drop the `Source_phase` column for publication; keep all other columns.
- **Internal audit must verify abstract numbers vs Results vs Tables** (L036). The Phase 8 internal consistency check should be programmatic — claimed numbers in the abstract grep against the source CSV. Target 100% match at 3-decimal precision.
