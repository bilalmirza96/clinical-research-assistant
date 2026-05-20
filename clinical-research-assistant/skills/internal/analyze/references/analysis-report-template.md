# Analysis Report Template

The 16-section template that `/analyze` Phase 7 produces as the master deliverable: `Reports/analysis_report_<question-slug>_<date>.md`.

Sections 1–15 are preserved from the v2 template. Sections **12a, 14a, 15a** are added in v3 to address reproducibility manifest + per-result provenance + replay command requirements.

---

## Filename and location

`Reports/analysis_report_<question-slug>_<date>.md`

The slug is the canonical short name for the research question (e.g., `cr_popf_predictors`, `esophageal_io_disparity`). Date format `YYYY-MM-DD`. Re-runs go to `Reports/Archives/` and the latest version stays at the canonical name.

---

## Template

```markdown
# Analysis Report — [Concise Title of the Question]

**Date:** YYYY-MM-DD
**Analyst:** [Name, role, institution]
**Project:** [Project name + folder]
**Scripts:** [paths to all scripts that produced these results, comma-separated]
**Datasets:** [paths to all input data files with N and date]
**Output files:** [paths to all generated tables, figures, and intermediate files]

## 1. Research Question

One sentence: the same gap statement used in the manuscript Introduction.

## 2. Estimand

- **Target population:**
- **Exposure / comparator:**
- **Outcome:**
- **Time horizon:**
- **Estimand framework:** ATE / ATT / per-protocol / intention-to-treat / etc.

## 3. Data Sources

For each source, name + version + date + N (raw) + N (after exclusions) + access date.

## 4. Cohort Selection (CONSORT-Style)

A numbered exclusion cascade with N at each step. Every excluded category has a count and a reason. Cross-reference: `data/working/filter_log.md` is the source of truth.

## 5. Variables

- **Outcome:** definition, coding, units (from `variable_spec.outcomes.primary`)
- **Exposure:** definition, coding, reference category (from `variable_spec.exposure`)
- **Confounders / covariates:** list with type, levels, missing-data handling
- **Stratification variables (if any):**
- **Effect modifiers tested (if any):**

## 6. Statistical Methods

For each analysis:
- **Method**
- **Software + version**
- **Adjustment set** (sequential M1 → M5 specification)
- **Assumption checks**
- **Significance threshold** (alpha = 0.05 two-sided default)
- **Multiple-testing correction** (BH-FDR / Bonferroni — say which family, how many)
- **Pre-specified sensitivity analyses**
- **Comparator declaration** (per L038): reference category named explicitly

## 7. Pre-Specified Sensitivity Analyses

Numbered list. Each entry: rationale + method + decision threshold.

## 8. Results

### 8.1 Cohort Characteristics
Table 1 reference + 1–2 sentence summary of demographics by exposure.

### 8.2 Primary Analysis
- **Endpoint:**
- **Result:** effect size + 95% CI + P value + N + reference category
- **BH-FDR Q value** (if part of a family)
- **E-value** (per L005)

### 8.3 Secondary Analyses
For each: same fields as primary.

### 8.4 Sensitivity Analyses
For each pre-specified sensitivity: result + interpretation (consistent / discrepant).

### 8.5 Subgroup / Stratified Analyses
Effect estimates within levels + formal interaction-term P value.

### 8.6 Multiple-Testing Master Summary
Master significance table with every test: endpoint, primary P, adjusted P, BH-FDR Q, Bonferroni significance.

## 9. Diagnostic Checks

- Schoenfeld residuals (Cox)
- VIF / multicollinearity (logistic / linear)
- Propensity-score overlap + caliper-binding (per L040)
- Influence statistics, residual plots if relevant
- Convergence diagnostics

## 10. Findings Summary (Plain Language)

3–5 bullet points stating what was learned. No numbers; substantive findings as a clinician would read them.

## 11. Limitations

- Unmeasured confounders (E-value lower bound)
- Missing-data assumptions (MAR / MCAR / MNAR rationale)
- Generalisability constraints
- Selection bias risks
- Information bias / measurement bias risks
- Compliance constraints (DUA cell-N rules per L007)
- Variable spec amendments (per soft-lock protocol) — if any, list them with rationale

## 12. Reproducibility Checklist

- [ ] All scripts saved to date-stamped folder under `Scripts/`
- [ ] All output files saved with date stamp in filename
- [ ] Random seeds fixed where stochastic methods used (per L033)
- [ ] Software environment documented (Python + R + package versions)
- [ ] Data version frozen (sha256 of raw + filter_operations.json)
- [ ] Pre-specified analysis plan archived (`plans/analysis_plan_v<n>.json`)
- [ ] Master significance table includes BH-FDR + Bonferroni
- [ ] Every reported number traceable to a registry key (see Section 14a)

## 12a. Reproducibility Manifest  *(new in v3)*

### Variables used

Auto-generated from `variable_spec.json`. One row per variable with name, label, type, source columns, derivation, missing-handling.

| Name | Label | Type | Source | Derivation | Missing |
|---|---|---|---|---|---|
| popf_cr_grade_bc | CR-POPF | binary | POPF_GRADE | POPF_GRADE in ['B','C'] | complete-case |
| ... | ... | ... | ... | ... | ... |

### Models fitted

| Model ID | Type | Outcome | Covariates | N | Events | Random seed | Convergence | Software |
|---|---|---|---|---|---|---|---|---|
| M1 | logistic | popf_cr_grade_bc | age + bmi + asa_class + ... | 7082 | 943 | 42 | TRUE | statsmodels 0.14.1 |
| M2 | cox | dgi_days | popf_cr + ... | 7082 | 1219 | 42 | TRUE | scikit-survival 0.22 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Software environment

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11.5 | Cohort assembly, regression |
| R | 4.3.1 | Figures (ggplot2 + tidyplots) |
| scikit-survival | 0.22 | Cox PH |
| statsmodels | 0.14.1 | Logistic, linear |
| ... | ... | ... |

## 13. Files Referenced

| File | Type | Description |
|---|---|---|
| `data/raw/...` | Input | Raw source; sha256 |
| `data/working/cohort.csv` | Input | Filtered cohort; sha256 |
| `data/working/filter_operations.json` | Provenance | Replayable filter sequence |
| `Scripts/.../*.py` | Script | Analysis code |
| `Tables/*.csv` | Output | Populated tables |
| `Figures/*.png` | Output | Generated figures |
| `results_registry.json` | Provenance | Per-result manifest |
| `audit_report.md` | Audit | 5-agent self-audit |

## 14. Verification Trail

Independent verification performed (numerical re-derivation, hand calculation on a 2×2 subset, alternative software) and result.

## 14a. Per-Result Provenance  *(new in v3)*

Every reported number carries a back-reference to its source in `results_registry.json`. Format: `[results_registry::M<n>::<key>]`.

Example:
> "Adjusted odds of CR-POPF were 2.14 (95% CI 1.62–2.83; P < 0.001) for ASA Class IV vs I-II (reference). **[results_registry::M1::asa_class_IV::aOR]**"

The bracketed pointer lets anyone trace the number back to the exact model output that produced it. Reviewers asking "where did 2.14 come from" get answered in one click.

## 15. Next Steps

What the analysis suggests should happen next: additional analyses, manuscript writing, peer review, replication in an external cohort.

## 15a. Replay Command  *(new in v3)*

Single shell command that re-runs the entire analysis from raw data:

```bash
cd <project_root>/analysis
./replay_analysis.sh
# Re-applies filter_operations.json to raw → produces cohort.csv
# Re-runs analysis scripts → produces all tables/figures
# Verifies sha256 of each output against this report's manifest
```

Cross-reference: `references/audit-agents.md` describes the Code-reproducibility auditor that executes this command during Phase 6.

---

## Compliance check

Before the report is declared complete, confirm:

- [ ] Every claim in §8 has effect size + 95% CI + P value + (where applicable) BH-FDR Q + reference category
- [ ] Every percentage is paired with numerator/denominator
- [ ] Every table reference resolves to an actual saved file
- [ ] Every script reference resolves to an actual saved file
- [ ] No internal hypothesis IDs (Q-numbers etc.) in user-facing text — replace with descriptive labels (per L012)
- [ ] §11 (Limitations) is not empty
- [ ] §12 + §12a (Reproducibility) have every checkbox addressed
- [ ] §14a per-result provenance pointers resolve to actual `results_registry.json` keys
- [ ] §15a replay command actually works (verified by Code-reproducibility auditor in Phase 6)
- [ ] Filename and location follow the convention
- [ ] Formatting per L042: Georgia 12pt, 1.5 line spacing, black text

If any check fails, the report is not complete. Do not exit Phase 7 until all checks pass.
```

---

## When the report is written

- **Mandatory at Phase 7** (delivery). The report is the durable deliverable; everything else is supporting state.
- **Re-generated whenever the analysis is re-run** (e.g., after PI revisions). Treat the report as a versioned artefact; archive prior versions to `Reports/Archives/`.
- **Read first by every subsequent session** that touches this analysis. The report is the single source of truth.

## Cross-references

- The report's **Methods section** is the source from which `/write-methods-results` drafts manuscript Methods.
- The report's **Results section** is the source for the manuscript's Results.
- The report's **Limitations** feed `/write-discussion`.
- The report's **§12a Reproducibility Manifest** is the source for the manuscript's Methods software + variable derivation paragraphs.
- The report's **§14a Per-Result Provenance** lets `/manuscript-qc` verify every number in the manuscript draft.
