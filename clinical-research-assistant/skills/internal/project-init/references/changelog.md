# `project-init` — CHANGELOG / Lessons Learned

**Load trigger:** only when auditing the history of this skill. Never needed to run the skill; `SKILL.md` holds enforcement. Newest first.

---

### 2026-05-28 — L051 — Primary + secondary objectives at intake; Protocol/ folder

Added in tandem with the analyze/SKILL.md L051 refinement. Two changes here:

1. **STEP 1 questions updated** to capture the primary objective (question 8) and secondary objectives (question 9) as distinct fields, separate from the primary outcome (question 6) and primary exposure (question 7). The outcome is the variable; the objective is the contrast sentence. These get finalized + PI-signed at `/analyze` Phase 1.0 → `Protocol/objectives_locked_<date>.md`. Question 10 (candidate covariates) is now explicitly labeled as preliminary — the final matching + adjustment variables are pre-specified and PI-approved at `/analyze` HALT 2A, not here.

2. **STEP 2 directory tree** now includes a `Protocol/` folder for PI-facing locked artifacts (`objectives_locked_*.md`, `variables_locked_*.md`, `sap_amendments.md`) and notes that `Reports/` holds the L051 Master Excel Workbook alongside the L045 JSON registry.

See `internal/analyze/SKILL.md` CHANGELOG 2026-05-28 L051 entry for the full rationale and the companion edits in this release.
