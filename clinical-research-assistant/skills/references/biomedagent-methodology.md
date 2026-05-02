# BioMedAgent-Adapted Methodology for Clinical Research

> **Purpose.** Distill the four transferable ideas from BioMedAgent (*Nature Biomedical Engineering*, 2026) into a methodology that every clinical-research-assistant sub-skill (analyze, data-analysis, literature-review, visualize, write-introduction, write-methods-results, write-discussion, write-manuscript) can rely on. This is **not** a port of BioMedAgent's 65-tool catalog. It is the *philosophy*: structured pipelines, task classification, memory retrieval, and self-correcting feedback applied to clinical biostatistics and manuscript writing.

> **Citation.** Bu D, Sun J, Li K, et al. Empowering AI data scientists using a multi-agent LLM framework with self-evolving capabilities for autonomous, tool-aware biomedical data analyses. *Nat Biomed Eng.* 2026.

---

## How to use this file

At the start of any clinical-research analysis or manuscript task:

1. **Read this file once at session start** so the four ideas below are active in working memory.
2. **Read `references/lessons-log.json`** to see whether a similar prior session already surfaced a relevant pattern. Skip steps that have been solved before; do not re-derive.
3. **Apply the three-phase pipeline** below to the user's request.
4. **Apply the task-classification routing rules** before choosing a method.
5. **Apply the anti-misclassification rules** before reporting any effect estimate.
6. **At session end, append a new entry to `references/lessons-log.json`** if the session surfaced a new pattern.

---

## 1. Three-phase pipeline (Plan → Execute → Verify)

BioMedAgent's central insight is that complex biomedical analyses fail when run as a single LLM step. Break the work into three phases with explicit handoffs.

### Phase 1 — Plan
Before writing code or text, produce an explicit plan:
- Restate the research question in one sentence (the same sentence you will write in the introduction's gap statement).
- Identify the *estimand*: target population, exposure, comparator, outcome, time horizon.
- List the inclusion/exclusion criteria you will apply, by data field name, with the order of application.
- Choose the analytic method *and* its assumptions (linearity, proportional hazards, missing-at-random, no immortal-time bias).
- List every sensitivity analysis you will run before seeing the result.

The plan is the deliverable of Phase 1. Do not skip to Phase 2 until the user has approved the plan or until the plan is committed to a written file.

### Phase 2 — Execute
Code only what the plan specifies. Save every analytic script to `Scripts/` with a date-stamped folder. Save every output to a date-stamped file. Never run an unscripted analysis whose result will be referenced later.

### Phase 3 — Verify and revise
Before reporting any number, verify it three ways:
- **Numerical.** Compute the same quantity by an independent path (e.g., margin totals, alternative software, hand calculation on a 2×2 subset).
- **Distributional.** Inspect the residuals, the proportional-hazards diagnostics, the propensity-score overlap, the influence statistics — whichever applies.
- **Clinical.** Show the number to a clinician (or your own clinical reasoning) and ask "is this magnitude plausible?" An OR of 0.05 for a common exposure should trigger a sanity check; a Cox HR of 12.0 for an established risk factor should trigger a sanity check.

If verification fails, return to Phase 1 (re-plan), not Phase 2 (re-code with the same plan). This is the self-correcting feedback loop.

---

## 2. Task classification before execution

BioMedAgent classifies every task into one of five categories before tool selection. The clinical-research analogue is a six-way routing table. Classify *first*; method selection follows.

| Category | Triggering question patterns | Default analytic family |
|---|---|---|
| **Descriptive** | "characterise", "describe", "report rates of", "Table 1", "incidence", "prevalence" | Frequency tables, median (IQR), mean (SD); χ² or Fisher exact across groups; no causal language |
| **Inferential test** | "is there a difference", "compare groups", "test whether", "two-sample" | t-test / Mann-Whitney U / χ² / Fisher exact / log-rank; report point estimate + 95% CI + JAMA-format P |
| **Multivariable model** | "adjusted for", "independent of", "controlling for", "after accounting for" | Sequential adjustment M1 → M5; logistic / Cox / linear depending on outcome distribution; E-value mandatory |
| **Survival / time-to-event** | "median follow-up", "hazard", "time to", "risk over time", "Kaplan-Meier", "Cox" | Cox proportional-hazards with Schoenfeld diagnostics; Kaplan-Meier estimator; time-stratified Cox if PH violated for the exposure |
| **Sensitivity / robustness** | "robust to", "sensitive to", "what if", "alternative definition", "complete-case vs imputed" | Multiple imputation (Rubin's rules); E-value (VanderWeele-Ding); subset re-runs; alternate cohort definitions |
| **Subgroup / interaction** | "in patients with", "stratified by", "interaction", "modifies the effect" | Stratified estimates within levels; formal interaction term test (Wald or LRT); pre-specify subgroups before running them |

**Routing discipline.** A request that contains the phrase "compare groups, adjusted for X, in patients with Y" spans three categories — write the plan to address all three explicitly rather than collapsing them into one model.

---

## 3. Memory retrieval — check the lessons log first

BioMedAgent's Redis memory cache lets it skip planning steps it has solved before. The clinical-research equivalent is `references/lessons-log.json`, a structured catalogue of patterns surfaced from prior sessions.

**Workflow:**
1. At the start of every analysis, scan `lessons-log.json` for any entry whose `trigger_patterns` overlap with the current task.
2. If a match is found, apply the entry's `action` directly. Do not re-derive.
3. After the analysis, if the session surfaced a new pattern (a new pitfall, a new sensitivity analysis worth running by default, a new misclassification trap), append a new entry.
4. Mark superseded entries with `"deprecated": true` rather than deleting them — the audit trail matters.

The first 10 entries in `lessons-log.json` are seeded from the V3/V4 Esophageal Cancer Disparity analysis (Bilal Mirza, U Arizona, 2026-04-24). They cover Simpson's-paradox prevention, time-stratified Cox, multiple imputation sensitivity, E-value reporting, master significance tables with BH-FDR, NCDB DUA cell-N≥11 compliance, stage-decomposition, power-justification for subgroups, and provider-side vs patient-side gating analysis.

---

## 4. Anti-misclassification rules for clinical research

BioMedAgent's "critical routing rules to avoid misclassification" translate to an explicit list of clinical pitfalls. Halt and re-plan if any of these apply.

### Statistical pitfalls

- **Cox proportional-hazards model with PH violated for the exposure.** Run the Schoenfeld test for the exposure coefficient specifically. If p < 0.05, do not report a single HR; either time-stratify or use restricted mean survival time (RMST).
- **Linear regression with binary outcome.** Use logistic regression. Linear-probability models are acceptable only as sensitivity, not primary.
- **t-test on right-skewed data.** Switch to Mann-Whitney U or Wilcoxon; report median (IQR), not mean (SD).
- **Multiple imputation with MNAR data.** Imputation assumes MAR. If missingness mechanism is plausibly MNAR (e.g., death-censored quality-of-life), use pattern-mixture sensitivity instead.
- **Complete-case analysis when >5% of any covariate is Unknown.** Required: present BOTH inclusive (Unknown-as-category) and exclusive (complete-case) primary results with rationale.
- **Subgroup analysis with one arm <500 reported as confirmed.** Compute power for the observed effect size before interpreting null findings. Report as "trend, not significant; likely underpowered" if power <80% for the observed effect.

### Causal-inference pitfalls

- **Causal language for an unadjusted contrast.** Use association language ("was associated with") for any observational comparison; reserve "caused", "resulted in", "led to" for randomised designs or instrumental-variable analyses.
- **Mediation analysis without testing the no-interaction-with-exposure assumption.** Modern mediation requires a 4-way decomposition.
- **Adjusting for a post-exposure variable.** Collider bias. Adjust for confounders (pre-exposure), not mediators (post-exposure).
- **Immortal time bias.** If exposure is defined after time-zero (e.g., "received immunotherapy at any time"), the comparison group has accumulated person-time without the opportunity to be exposed. Use landmark analysis or time-dependent covariates.

### Reporting pitfalls

- **Reporting p < 0.05 without effect size + 95% CI.** Always report effect size and CI; star notation alone is insufficient.
- **Reporting only the primary endpoint that "worked".** Pre-specify all endpoints; run a master significance table with BH-FDR or Bonferroni across the family of tests.
- **DUA-protected cell counts < 11 in published tables.** For NCDB-derived results, mask any cell with N < 11 in publication-facing exports.

### Within-stratum sanity rule (Simpson's paradox prevention)

For any reported gap in a continuous outcome between groups (e.g., "Black patients present with tumours 10 mm larger"), always run the within-stratum analysis on the most-relevant confounder (stage, age, histology) before publishing. A gap that disappears within strata is a confounding artefact, not a finding.

---

## 5. Self-evolution — append, don't delete

BioMedAgent improves over time by accumulating successful analytic patterns. The clinical-research-assistant equivalent is the `CHANGELOG / Lessons Learned` block at the bottom of each sub-skill's `SKILL.md`.

**Rules.**
- Append new entries dated, with the originating session and the action item.
- Mark superseded entries deprecated rather than deleting.
- Cross-reference between `analyze/SKILL.md` (analytic-process lessons), `write-manuscript/SKILL.md` (manuscript-process lessons), and this file (cross-cutting methodology).
- The `lessons-log.json` is the machine-readable counterpart; keep both in sync.

---

## 6. Glossary of clinical-research-specific tasks (mapped to BioMedAgent categories)

For reference when classifying a request:

| Clinical task | BioMedAgent category | CRA skill |
|---|---|---|
| Cohort selection cascade with exclusion counts | Descriptive | `analyze`, `data-analysis` |
| Baseline characteristics by exposure (Table 1) | Descriptive | `analyze`, `data-analysis` |
| Race-disparity gap with χ² P value | Inferential test | `analyze`, `data-analysis` |
| Sequential M1 → M5 logistic regression | Multivariable model | `analyze`, `data-analysis` |
| Cox proportional-hazards for OS or DSS | Survival | `analyze`, `data-analysis` |
| Schoenfeld residual test + time-stratified Cox | Survival | `analyze`, `data-analysis` |
| Multiple imputation sensitivity (Rubin's rules) | Sensitivity | `analyze`, `data-analysis` |
| E-value (VanderWeele-Ding) for residual confounding | Sensitivity | `analyze`, `data-analysis` |
| Master significance table with BH-FDR + Bonferroni | Sensitivity | `analyze` |
| Histology-stratified analysis (EAC vs ESCC) | Subgroup | `analyze`, `data-analysis` |
| Forest plot of subgroup ORs/HRs | Subgroup, Visualization | `visualize`, `analyze` |
| Kaplan-Meier curves by group × era | Survival, Visualization | `visualize`, `analyze` |
| CONSORT cohort-selection diagram | Descriptive, Visualization | `visualize` |
| JAMA-format Table 1 / Table 2 / Table 3 build | Descriptive | `write-methods-results` |
| Three-phase manuscript drafting (Plan → Sections → Audit) | All categories | `write-manuscript` |

---

> **Maintainer.** This file is a living document. Edit it when a new BioMedAgent-style insight (memory retrieval, multi-agent decomposition, tool-awareness) proves useful in a clinical-research analysis. Keep the four core ideas (three-phase pipeline, task classification, memory retrieval, anti-misclassification rules) at the top. Move tactical details to `lessons-log.json`.
