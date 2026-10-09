# `write-abstract` — CHANGELOG / Lessons Learned

**Load trigger:** only when auditing the history of this skill. Never needed to run the skill; `SKILL.md` holds enforcement. Newest first.

---

### 2026-10-09 — Conference abstract voice restored (L110)

The author rejected the AATS 2027 lung disparities draft (built under the L103 JAMA guide) as flat and asked why abstracts are not written like the submitted ITSOS 2026 abstract. Added `references/conference-abstract-voice.md` (architecture, sentence-level texture measured against the rejected draft, story-completeness check S1-S8, the author's June-to-submitted edits, worked contrast); replaced the example with the submitted text (June draft kept below it); added principle 13 and gate row 13; paired review with the new `cra-abstract-advocate` agent; `voice_check.py --conference` soft checks. For meeting abstracts the new file overrides writing-style.md's "Structured abstract" bullets.

### 2026-09-28 — Bounded mechanical edits skip the full reference read (L101)

Regression eval evidence: asked to fix three banned race terms in an existing abstract, the router
and `write-abstract` required reading five reference files and all five canonical example abstracts
first, and ran out of turns mid-edit. Added a scope clarification to "Required reading at session
start" and to the "Reference Example Abstracts" section: the full-read requirement (items 1-3,
plus "read all five canonical abstracts") applies to drafting and to any rewrite changing more than
about one sentence or any claim; it does not apply to a **bounded mechanical edit** of an existing
draft (terminology swap, registry-sourced number correction, typo fix), which proceeds directly to
the edit. `voice_check.py` and `claim_audit.py` still run on the result of a bounded edit exactly as
on a full draft — only the upfront reading is scoped down. Mirrored in
`../../references/writing-style.md` (same rule stated there) and the router's "Read First" section.
Author-approved 2026-09-28. Regression check: `evals/L020-abstract-race-terminology`. Lessons-log
**L101**.

### 2026-06-29 — Catalogued three translational scRNA-seq reference abstracts

Added three author-supplied abstracts as canonical style templates for the **translational single-cell / immuno-oncology register**, a register not previously represented (the prior two examples were surgical / registry-outcomes): `examples/example_glutamine-cpm_scrna-invivo.md` (CPM glutamine antagonism — scRNA-seq + TCGA survival + in vivo DRP104 ± anti-PD1), `examples/example_epithelial-states_scrna-mcrc.md` (divergent epithelial cell states — descriptive iCMS/CMS taxonomy, no interventional arm), and `examples/example_gzmk-tcells_hnscc-ici.md` (GZMK+ T-cell ICI-response biomarker — clinical-trial scRNA + bulk with external-cohort validation). Full verbatim abstract text catalogued in each file; "Reference Example Abstracts" section regrouped into surgical/registry vs translational/single-cell registers. Trigger: Bilal supplied the three abstracts as "how I want abstracts written." Catalog now holds **5** reference examples. **Source-repo + lessons-log.json synced 2026-06-29** — replicated all five `examples/` files + this SKILL.md into the source repo at `~/dev/clinical-research-assistant` (note: actual path is `~/dev/`, not `~/Claude/dev/` as the workspace CLAUDE.md states) and added lessons-log entry L055.

### 2026-06-24 — Added canonical reference-example abstracts

Added `examples/example_crpopf_surgical-outcomes.md` (NSQIP surgical-outcomes, ASC 2026) and `examples/example_disparities_genomics-registry.md` (SEER/NCDB/GENIE, mediation-heavy) as author-approved style templates, plus a "Reference Example Abstracts" section distilling six concrete patterns (two-alternative opening + first-person voice; dense covariate-named Methods with only-real rigor signals; prose-dense Results with n (%)/CI/exact-P; the "Despite ... " pivot; driver-naming Conclusions ending on the highest-leverage clinical lever; no em dashes). Trigger: Bilal supplied the CR-POPF and esophageal-disparities abstracts as "how I like my abstracts." **Source-repo + lessons-log.json synced 2026-06-29** (alongside the 2026-06-29 translational batch) — both example files replicated into the source repo at `~/dev/clinical-research-assistant`; lessons-log entry L055 covers the full reference-example catalog.

### 2026-04-26 — Created from Bilal Mirza editorial philosophy

Initial 12-principle rubric authored by Bilal Mirza (PGY-1 General Surgery, U Arizona). Source: response to ITSOS 2026 abstract draft. Added 12-point gate, venue cheat-sheet, and worked example on the ITSOS abstract.

> **Maintainer note.** Append new lessons here, dated, with the originating session and the action item. This skill should accrete capability over time. If a future session finds a principle is wrong or superseded, mark it as deprecated rather than deleting — the audit trail matters.

---

# Archived worked audit (moved from SKILL.md 2026-09-28, L103)

## Example application (archived) — ITSOS 2026 abstract (2026-04-26)

**Title:** *Surgery Access, Not Tumor Biology, Drives the Black–White Survival Disparity in Esophageal Cancer in the Immune Checkpoint Inhibitor Era*

Run the 12-point gate:

| # | Principle | Status | Note |
|---|---|---|---|
| 1 | Coherence | ✓ | Single arc: surgery access vs tumor biology |
| 2 | Falsification arc | ✓ | "Despite tumor biology that favors immunotherapy responsiveness…" — alternative-mechanism language present in Conclusions; the "Tumor biology favours not disfavours" finding refutes the biology candidate |
| 3 | Calibrated language | ⚠ | Title uses "Drives". For a cross-sectional registry analysis with E-value 2.78, "Drives" is borderline; the body uses the more calibrated "is consistent with access-driven mechanisms". **Suggested fix:** consider title rewrite to "Surgery Access, Not Tumor Biology, Underlies the Black–White Survival Disparity…" if reviewers in pilot reads object. Defensible given E-value strength; flag for self-review. |
| 4 | Race terminology | ✓ | NHB / NHW (NCDB / SEER vocabulary); "self-reported race" not yet stated — add to Methods of full manuscript |
| 5 | Audience calibration | ✓ | Specific named pathways (TMB-High; squamous histology; composite ICI-responsive signature); statistical rigor signals (E-value, BH-FDR, Bonferroni) preserved |
| 6 | Section weight | ✓ | Results 1,478 chars; Methods 826; Conclusions 660; Objective 443. Results > 2× Methods AND > 2× Conclusions. |
| 7 | Therapeutic implications | ✓ | "supports… prioritized enrollment of Black patients in immune checkpoint inhibitor trials" — trial-design rationale, not treatment-response prediction |
| 8 | Confounders absent | ✓ | TSS, batch, immortal time not mentioned in abstract |
| 9 | Honesty over impact | ⚠ | Title "Drives" (see #3). Body uses calibrated language. |
| 10 | Compliance | ✓ | 3,407 chars / 3,500; 4 bolded headers; numerator/denominator throughout; no institution names in body; no brand names; AATS-accepted abbreviations only |
| 11 | Four-criterion gate | ✓ | Surgery OR (P=1×10⁻³⁴, BH-FDR q<.001, E-value 2.78); TMB-High OR 2.44 (P<.0001, BH-FDR q<.001) |
| 12 | Prose over bullets | ✓ | No bullets in body; sentences accumulate |

**Top 3 fixes** (priority × effort):
1. Consider title verb downgrade: "Drives" → "Underlies" or "Is Consistent With" (Principle 3 + 9; flagged but defensible).
2. Add "self-reported race per registry coding" to full-manuscript Methods (Principle 4; not blocking for abstract).
3. Confirm with co-authors that the "Despite tumor biology that favors immunotherapy responsiveness" Conclusions sentence reads as the falsification arc; consider explicit "the prior hypothesis that tumour biology accounts for the disparity is not supported in this cohort" in the manuscript Discussion (Principle 2; not blocking for abstract).

---

