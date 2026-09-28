# `write-abstract` — CHANGELOG / Lessons Learned

**Load trigger:** only when auditing the history of this skill. Never needed to run the skill; `SKILL.md` holds enforcement. Newest first.

---

### 2026-06-29 — Catalogued three translational scRNA-seq reference abstracts

Added three author-supplied abstracts as canonical style templates for the **translational single-cell / immuno-oncology register**, a register not previously represented (the prior two examples were surgical / registry-outcomes): `examples/example_glutamine-cpm_scrna-invivo.md` (CPM glutamine antagonism — scRNA-seq + TCGA survival + in vivo DRP104 ± anti-PD1), `examples/example_epithelial-states_scrna-mcrc.md` (divergent epithelial cell states — descriptive iCMS/CMS taxonomy, no interventional arm), and `examples/example_gzmk-tcells_hnscc-ici.md` (GZMK+ T-cell ICI-response biomarker — clinical-trial scRNA + bulk with external-cohort validation). Full verbatim abstract text catalogued in each file; "Reference Example Abstracts" section regrouped into surgical/registry vs translational/single-cell registers. Trigger: Bilal supplied the three abstracts as "how I want abstracts written." Catalog now holds **5** reference examples. **Source-repo + lessons-log.json synced 2026-06-29** — replicated all five `examples/` files + this SKILL.md into the source repo at `~/dev/clinical-research-assistant` (note: actual path is `~/dev/`, not `~/Claude/dev/` as the workspace CLAUDE.md states) and added lessons-log entry L055.

### 2026-06-24 — Added canonical reference-example abstracts

Added `examples/example_crpopf_surgical-outcomes.md` (NSQIP surgical-outcomes, ASC 2026) and `examples/example_disparities_genomics-registry.md` (SEER/NCDB/GENIE, mediation-heavy) as author-approved style templates, plus a "Reference Example Abstracts" section distilling six concrete patterns (two-alternative opening + first-person voice; dense covariate-named Methods with only-real rigor signals; prose-dense Results with n (%)/CI/exact-P; the "Despite ... " pivot; driver-naming Conclusions ending on the highest-leverage clinical lever; no em dashes). Trigger: Bilal supplied the CR-POPF and esophageal-disparities abstracts as "how I like my abstracts." **Source-repo + lessons-log.json synced 2026-06-29** (alongside the 2026-06-29 translational batch) — both example files replicated into the source repo at `~/dev/clinical-research-assistant`; lessons-log entry L055 covers the full reference-example catalog.

### 2026-04-26 — Created from Bilal Mirza editorial philosophy

Initial 12-principle rubric authored by Bilal Mirza (PGY-1 General Surgery, U Arizona). Source: response to ITSOS 2026 abstract draft. Added 12-point gate, venue cheat-sheet, and worked example on the ITSOS abstract.

> **Maintainer note.** Append new lessons here, dated, with the originating session and the action item. This skill should accrete capability over time. If a future session finds a principle is wrong or superseded, mark it as deprecated rather than deleting — the audit trail matters.
