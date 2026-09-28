# `literature-review` — CHANGELOG / Lessons Learned

**Load trigger:** only when auditing the history of this skill. Never needed to run the skill; `SKILL.md` holds enforcement. Newest first.

---

### 2026-09-25 — L082, L083, L084 — Retrieval reconciliation, computed absence statements, workbook house style

From the LUNG DISPARITIES PROJECT Phase 0 review (search run 2026-09-24; `decision_log.md`, 2026-09-25). Each number below was re-derived from the project's scripts and data before it was written here.

1. **L082 — Retrieval completeness gate** (Search Strategy; pointer in STEP 2). `scripts/lit_02_citation_chase.py` fetched the 5,589 PMIDs that citation chasing identified in PubMed efetch batches of 200. The batches at offsets 800 and 1000 still failed after the fetch helper's 5 in-place attempts; the loop appended them to `api_failures_logged` and continued, so 400 records were never retrieved or screened. One of 115 seed-review reference lists was lost the same way. The gap surfaced a day later. New rule: retry failed batches in a deferred pass with exponential backoff, reconcile identified against retrieved before screening and stop on a mismatch, and report not-retrieved records in PRISMA. The missing PMIDs are in `literature/raw/citation_chase_unretrieved_2026-09-24.json`.
2. **L083 — Absence statements computed and asserted** (STEP 3; Deliverable Builders). "None of the 7 perioperative studies examined perioperative immunotherapy" and "no abstract reported E-values" are generated from the coded extraction and asserted by `scripts/lit_07_build_report.py`. Its term screen flagged PMID 37741315, which the coded field had missed; a hand read cleared it, and `PERIOP_ICI_READ` records the reason. Extends L073 from analysis registries to literature synthesis.
3. **L084 — Workbook builders enforce the house table standard** (Deliverable Builders). `scripts/lit_06_build_excel.py` had written navy header fills, colour-filled relevance cells and Calibri: `house_style` counts 75,064 violations on the pre-rebuild workbook and 0 on the rebuilt one, which now ends with `house_style.enforce_xlsx`. Recommended for every CRA workbook builder, starting with the `analyze` L051 Master Excel Workbook. Two enforcer gaps found while verifying: `check=True` misses coloured Times New Roman text, and non-solid pattern fills survive both passes.

Recorded the same day in `00_Context/working-rules.md` and `references/lessons-log.json`.

> **Maintainer note.** Append new lessons here, newest first, dated, with the lesson ID and the originating session. Mark superseded rules deprecated rather than deleting them.
