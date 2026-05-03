---
name: analyze
description: Full interactive statistical analysis for clinical research. Activate when the user wants to analyze a dataset, run statistical models, or perform data-driven clinical research.
argument-hint: "[study aim or dataset description]"
---

# /analyze — Full Statistical Analysis

> **Canonical owner of the `/analyze` command.** Methodological guardrails and diagnostics expectations are defined in `skills/data-analysis/SKILL.md` (policy file). This skill defines the workflow.

<role>
Act as a senior clinical biostatistician operating at publication-grade standards for major surgical, oncology, transplant, and high-impact medical journals.
</role>
<biomedagent_adapted_methodology>
## BioMedAgent-adapted methodology — read first

**Before starting any analysis, read these two files in this exact order:**

1. `../references/lessons-log.json` — machine-readable memory of analytic patterns surfaced from prior sessions. Scan `trigger_patterns` for matches to the current task. If a match is found, apply the entry's `action` directly without re-deriving.
2. `../references/biomedagent-methodology.md` — the four cross-cutting ideas adapted from BioMedAgent (*Nature Biomedical Engineering*, 2026): three-phase pipeline (Plan → Execute → Verify), task classification before method selection, memory retrieval, and anti-misclassification rules.

**Apply the three-phase pipeline to every analysis** (this is the discipline behind the existing 8-step interactive workflow):
- **Phase 1 (Plan).** Steps 1–3. Restate the question, fix the estimand, list inclusion/exclusion, choose method + assumptions, pre-specify all sensitivity analyses.
- **Phase 2 (Execute).** Steps 4–7. Code only what the plan specifies; save every script to a date-stamped folder.
- **Phase 3 (Verify and revise).** Step 8 + audit. Numerical, distributional, and clinical-magnitude checks before any number is reported. If verification fails, return to Phase 1, not Phase 2.

**Classify the task before choosing a method.** Use the six-way routing table in `biomedagent-methodology.md` (descriptive / inferential test / multivariable / survival / sensitivity / subgroup).

**Apply the anti-misclassification rules** in `biomedagent-methodology.md` Section 4 before reporting any effect estimate.

**Append a new lesson at session end** to `../references/lessons-log.json` if the session surfaced a new pattern (pitfall, default sensitivity, classification trap). Format: `id`, `date_added`, `originating_session`, `category`, `trigger_patterns`, `lesson`, `action`.
</biomedagent_adapted_methodology>


## State Management

`/analyze` operates in two modes depending on whether state files exist.

### Mode A — Stateful Project Mode

Triggered when `project_state.json` exists in the working directory (created by `/project-init` or a prior `/analyze` run).

**On entry:**
1. Read `project_state.json`. Print: `"Resuming project: [project_name] — last phase: [current_phase]"`
2. Read `study_spec.json` if it exists. Pre-fill: outcome, exposure, covariates, design features, registry, study aim. Do not re-ask these.
3. Read `analysis_plan.json` if it exists. Check `steps_completed` — skip to the first step where the value is `false`. Print: `"Analysis progress: [N]/13 steps complete. Resuming at Step [X]."`
4. Read `dataset_profile.json` if it exists. If `file_path` is set and the file exists, load the dataset automatically.

**At checkpoints:** write state files as specified below in "Checkpoint Writes."

### Mode B — Standalone Mode (Backward Compatible)

Triggered when no `project_state.json` exists in the working directory.

**On entry:**
1. Proceed normally — ask for all required inputs.
2. After the user provides a dataset and study aim, ask once: `"Would you like me to save project state files so you can resume this analysis in a future session? (yes/no)"`
3. If yes: create `project_state.json`, `study_spec.json`, `analysis_plan.json`, `dataset_profile.json` in the working directory at the first checkpoint. From that point forward, behave as Mode A.
4. If no: proceed without state files. All analysis still works. No files are written.

---

### Checkpoint Writes

Each checkpoint writes specific fields to specific files. Use Python `json.load` / `json.dump` with `indent=2`. Create files from scratch if they do not exist — do not require templates.

#### After STEP 1 (Data Intake) — user approves variable list

**`project_state.json`** — create or update:
```
.status          = "in_progress"
.current_phase   = "analysis"
.updated_at      = [ISO 8601 timestamp]
.dataset.file_path = [path to dataset]
.dataset.file_type = [csv/xlsx/sas7bdat/etc]
.dataset.rows    = [row count]
.dataset.columns = [column count]
.dataset.loaded  = true
```

**`dataset_profile.json`** — create or update:
```
.file_path       = [path to dataset]
.file_type       = [csv/xlsx/sas7bdat/etc]
.loaded_at       = [ISO 8601 timestamp]
.rows_raw        = [row count before cleaning]
.columns_raw     = [column count]
.variables       = [list of {name, dtype, missing_pct, n_unique}]
.outcome_variable = [confirmed outcome variable name]
.exposure_variable = [confirmed exposure variable name]
.data_dictionary_provided = [true/false]
```

**`analysis_plan.json`** — create or update:
```
.steps_completed.data_intake = true
```

#### After STEP 3 (Data Cleaning) — user approves cleaning log

**`dataset_profile.json`** — update:
```
.rows_after_cleaning  = [row count after cleaning]
.columns_after_cleaning = [column count after cleaning]
.cleaning_log     = [list of {action, rows_affected, reason}]
.missing_summary.strategy = [complete-case/imputation/sensitivity]
.missing_summary.mechanism = [MCAR/MAR/MNAR]
.missing_summary.variables_above_20pct = [list of variable names]
.covariates       = [confirmed covariate list]
```

**`analysis_plan.json`** — update:
```
.steps_completed.missing_assessment = true
.steps_completed.cleaning = true
.missing_data_strategy = [chosen strategy]
```

**`project_state.json`** — update:
```
.updated_at = [timestamp]
```

#### After STEP 5 (Analysis Plan Approval) — user approves the plan

**`analysis_plan.json`** — update:
```
.outcome_type     = [binary/continuous/count/time-to-event]
.exposure_type    = [binary/categorical/continuous]
.study_structure  = [cohort/case-control/cross-sectional/repeated/clustered]
.planned_models.unadjusted = [test name]
.planned_models.adjusted   = [model name]
.planned_models.effect_measure = [OR/HR/beta/IRR/SHR]
.covariates_for_adjustment = [list of variable names]
.propensity_methods.needed = [true/false]
.propensity_methods.method = [matching/IPTW/both/none]
.sensitivity_analyses = [list of planned sensitivity analyses]
.steps_completed.design_inference = true
```

**`study_spec.json`** — update if fields were refined during analysis:
```
.outcome.name    = [confirmed]
.outcome.type    = [confirmed]
.exposure.name   = [confirmed]
.exposure.type   = [confirmed]
.exposure.reference_group = [confirmed]
.covariates      = [confirmed list]
.design_features = [confirmed flags]
```

**`project_state.json`** — update:
```
.updated_at = [timestamp]
```

#### After STEP 6a (Table 1) — user approves baseline table

**`analysis_plan.json`** — update:
```
.steps_completed.table1 = true
```

#### After STEP 6d (Adjusted Analysis) — user approves primary results

**`analysis_plan.json`** — update:
```
.steps_completed.unadjusted = true
.steps_completed.diagnostics = true
.steps_completed.adjusted = true
```

#### After STEP 6e-6f (Causal Inference + Sensitivity) — if performed

**`analysis_plan.json`** — update:
```
.steps_completed.causal_inference = true  (if performed, else leave false)
.steps_completed.sensitivity = true
```

#### After STEP 7 (Bias Warnings)

**`analysis_plan.json`** — update:
```
.steps_completed.bias_warnings = true
```

#### After STEP 9b (Final — Analysis Report Complete)

This is the completion checkpoint. Write all final state.

**`project_state.json`** — update:
```
.status          = "analysis_complete"
.current_phase   = "analysis_complete"
.updated_at      = [timestamp]
.phases_completed = [append "analysis" if not already present]
```

**`analysis_plan.json`** — update:
```
.steps_completed.excel_export = true
.steps_completed.code_bundle = true
```

**`results_registry.json`** — create or update:
```
.last_updated    = [timestamp]
.cohort.screened = [N screened]
.cohort.excluded = [N excluded]
.cohort.analyzed = [N in final analytic cohort]
.cohort.exclusion_reasons = [list of {reason, n}]
.primary_result.model = [e.g. "multivariable logistic regression"]
.primary_result.effect_measure = [OR/HR/beta/IRR/SHR]
.primary_result.estimate = [numeric value]
.primary_result.ci_lower = [numeric]
.primary_result.ci_upper = [numeric]
.primary_result.p_value  = [numeric]
.primary_result.n_analyzed = [N]
.primary_result.covariates_adjusted = [list of variable names]
.secondary_results = [list of {name, model, effect_measure, estimate, ci_lower, ci_upper, p_value}]
.diagnostics_summary.vif_max = [numeric]
.diagnostics_summary.epv = [numeric]
.diagnostics_summary.assumptions_met = [true/false]
.diagnostics_summary.issues = [list of strings]
.propensity_analysis.performed = [true/false]
.propensity_analysis.method = [matching/IPTW/both]
.propensity_analysis.balance_achieved = [true/false]
.propensity_analysis.max_smd_after = [numeric]
.tables = [list of {name, sheet_name, description}]
.excel_path = [path to output .xlsx]
```

**`decision_log.md`** — append one entry:
```markdown
### [DATE] — Analysis

**Decision:** [1-2 sentence summary of the primary analytical approach chosen]

**Reason:** [why this model/method was selected]

**Alternatives considered:**
- [list alternatives discussed during the analysis]

**Risks / unresolved issues:**
- [any diagnostics warnings, residual confounding concerns, or caveats]
```

---

### State Write Implementation

When writing state files, follow these rules:
- Use `json.dump(data, f, indent=2)` for all JSON files
- Use `"a"` mode for `decision_log.md` (append, never overwrite)
- If a file already exists, read it first with `json.load`, merge updates into the existing object, then write back — never overwrite fields you are not updating
- If a file does not exist, create it with only the fields specified above — do not require the full template structure
- All timestamps use ISO 8601 format: `"2026-04-01T14:30:00"`
- Wrap all file I/O in try/except — if a write fails, warn the user but do not halt the analysis

## Interaction Rules

- Semi-autonomous by default — complete a full analysis phase, then check in
- After completing each step, STOP and present findings
- Ask "Do you approve? Should I modify anything?" before moving to the next step
- Never proceed without explicit user approval on critical decisions (covariate selection, model choice, handling of failed diagnostics)
- Routine sub-steps within a phase (e.g., running VIF after fitting a model) do not need separate approval — bundle them and present the combined result
- No figures, charts, plots, or visualizations — `/visualize` handles all figure generation
- Present assumption check results as numeric summaries in tables, not diagnostic plots
- All tables must include a timestamp and dataset name

## Output Format

- Present tables inline in chat as formatted markdown tables during analysis steps
- **Final analysis output: Excel (.xlsx) only** — all tables in a single formatted workbook
- Excel format: Times New Roman 12pt, centered, bold headers, thin black borders, no color
- No Word documents during analysis — Excel is the deliverable
- No figures — `/visualize` handles figures separately

## Required Inputs

Ask for these only if not already provided or inferrable:
1. Study aim (1-2 sentences)
2. Primary outcome (name, type, coding)
3. Exposure variable (name, type, reference group)
4. Covariates for adjustment
5. Study design features (clustering, repeated measures, survival, competing risks)
6. Inclusion/exclusion criteria (if applicable)

If a data dictionary is provided, treat it as the authoritative schema.

---

## Workflow

### STEP 1: Data Intake & Validation
- Inspect variable names and types; standardize to snake_case
- Cross-check dataset against dictionary definitions (if provided)
- Show: number of rows/columns, first 5 rows, all variable names with types
- Detect: missing variables, type mismatches, impossible values, duplicate identifiers, unexpected categories, out-of-range values
- Flag extreme outliers using IQR and z-score methods

> CHECKPOINT: Present variable list and flag critical inconsistencies. Confirm exposure, outcome, and covariates with user. Do not proceed if critical inconsistencies exist.

### STEP 2: Data Understanding & Missing Data Assessment
- Variable summary table (name, type, missing %, distributions)
- Quantify percent missing per variable
- Detect co-missingness patterns
- Compare missingness by exposure/outcome groups
- Classify likely mechanism: MCAR, MAR, or MNAR
- Recommend strategy: complete-case (only if justified), multiple imputation, or sensitivity analysis

> CHECKPOINT: Present missingness table. If any covariate >20% missing, flag explicitly and agree on handling strategy with user.

### STEP 3: Data Cleaning
- Propose specific cleaning steps with rationale
- Convert declared missing codes to NA
- Parse dates and derive time variables when needed
- Enforce valid ranges per dictionary
- Recode categoricals according to dictionary
- Collapse sparse levels only if statistically justified
- Log every transformation
- Execute only after approval, then show before/after summary

> CHECKPOINT: Present data cleaning log. State rows removed and why. Get user confirmation.

### STEP 4: Research Question & Study Design Inference
- Clarify research question
- Automatically infer and state:
  - **Outcome type**: binary, continuous, count, or time-to-event
  - **Exposure type**: binary, categorical, or continuous
  - **Study structure**: cohort, case-control, cross-sectional, repeated measures, or clustered
- If unclear, ask for clarification before proceeding

### STEP 5: Statistical Analysis Plan & Model Selection
- Summarize complete analysis plan
- State planned models with justification (consult policy file for model selection table)
- Get user approval before executing

### STEP 6: Execute Analysis (One Result at a Time)

**6a. Table 1 — Baseline Characteristics**
- Continuous: mean (SD) and/or median (IQR) based on distribution
- Categorical: n (%)
- Stratify by exposure groups
- Include standardized mean differences (SMD)
- Include total N and group Ns

> CHECKPOINT: Present Table 1 for user review before modeling.

**6b. Primary Analysis — Unadjusted**
- Run appropriate unadjusted test based on outcome type
- Report: effect size, 95% CI, p-value, N analyzed

> CHECKPOINT: Present unadjusted results. Confirm covariate list for adjusted model.

**6c. Assumption Checks (Mandatory)**
- Run all diagnostics per the policy file checklist BEFORE finalizing results
- Present all diagnostics as tables
- VIF, EPV, model-specific checks

> CHECKPOINT: Present diagnostics. If assumptions fail, propose correction and get approval.

**6d. Primary Analysis — Adjusted**
- Explicitly state every covariate included
- State reference category for every categorical variable
- Present unadjusted vs adjusted side by side
- Report: adjusted effect size, 95% CI, p-value, N analyzed

**6e. Causal Inference Module** (if observational treatment comparison)
- Estimate propensity score via logistic regression
- Evaluate covariate balance with SMDs (target: all <0.1)
- Implement IPTW or matching (or both)
- Compare crude vs adjusted vs weighted estimates
- Warn if: extreme weights, poor overlap, positivity violations

**6f. Sensitivity Analyses**
- Robust standard errors (HC3)
- Firth logistic regression (if rare events)
- Restricted cubic splines (if nonlinearity suspected)
- Alternative covariate sets
- Interaction testing for subgroup analysis (only if prespecified)
- E-value for unmeasured confounding (for RR/HR)
- Influence diagnostics
- Clearly distinguish prespecified vs exploratory analyses

### STEP 7: Bias & Methodological Warnings
- Consult policy file bias checklist
- Flag all detected issues explicitly
- If a fatal flaw is detected, HALT and explain

### STEP 8: Publication-Ready Excel File
- Single .xlsx with all tables on named sheets
- All tables include: effect size label (OR/HR/beta/IRR), 95% CI, p-value, N
- Times New Roman 12pt, centered, bold headers, thin black borders, no color
- Timestamp all outputs

### STEP 9a: Reproducible Code Bundle
- Complete Python script using: pandas, numpy, scipy, statsmodels, lifelines, scikit-learn, openpyxl
- Script must: load raw data, clean data, fit models, run diagnostics, generate all outputs
- Fixed random seed (42)
- `pip install` block with Python version and all package versions
- Analysis log: rows included/excluded, missing data handling, final N, model diagnostics


### STEP 9b: Generate the Analysis Report (MANDATORY)

**Every analysis must end with a date-stamped, structured markdown report.** No analysis is considered complete without this report. The report is the durable deliverable that future sessions, co-authors, and reviewers can audit. It is what gets cited from the manuscript Methods and Results sections, and what gets attached to the regulatory submission packet.

#### Filename and location

Save to the project's `Analyses/` or `Reports/` folder (create if missing) with the filename pattern:

```
analysis_report_<short-question-slug>_YYYY-MM-DD.md
```

Example: `analysis_report_NHB_surgery_disparity_2026-04-26.md`

#### Required sections (in this exact order)

Every report must contain all of these sections. Empty sections are not acceptable; if a section does not apply, write "Not applicable — [reason]" rather than omitting it.

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

A numbered exclusion cascade with N at each step. Every excluded category has a count and a reason.

## 5. Variables

- **Outcome:** definition, coding, units
- **Exposure:** definition, coding, reference category
- **Confounders / covariates:** list with type (categorical / continuous), levels, missing-data handling
- **Stratification variables (if any):**
- **Effect modifiers tested (if any):**

## 6. Statistical Methods

For each analysis:
- **Method** (logistic / Cox / linear / Fisher exact / chi-square / Kruskal-Wallis / etc.)
- **Software + version** (Python 3.10, statsmodels 0.14, lifelines 0.30, scipy 1.15, etc.)
- **Adjustment set** (sequential M1 → M5 specification)
- **Assumption checks** (proportional-hazards, linearity, normality, missing-at-random)
- **Significance threshold** (alpha = 0.05 two-sided default)
- **Multiple-testing correction** (BH-FDR / Bonferroni — say which family of tests, how many)
- **Pre-specified sensitivity analyses** (list before reporting)

## 7. Pre-Specified Sensitivity Analyses

Numbered list. Each entry: rationale + method + decision threshold.

## 8. Results

### 8.1 Cohort Characteristics
Table 1 reference + 1–2 sentence summary of demographics by exposure.

### 8.2 Primary Analysis
- **Endpoint:**
- **Result:** effect size + 95% CI + P value + N
- **BH-FDR Q value** (if part of a family)
- **E-value** (for residual confounding, if observational)

### 8.3 Secondary Analyses
For each: same fields as primary.

### 8.4 Sensitivity Analyses
For each pre-specified sensitivity: result + interpretation (consistent / discrepant).

### 8.5 Subgroup / Stratified Analyses
Effect estimates within levels + formal interaction-term P value.

### 8.6 Multiple-Testing Master Summary
Master significance table with every test in the family: endpoint, primary P, adjusted P, BH-FDR Q, Bonferroni significance.

## 9. Diagnostic Checks

- Schoenfeld residuals (Cox)
- VIF / multicollinearity (logistic / linear)
- Propensity-score overlap (counterfactual)
- Influence statistics, residual plots if relevant
- Convergence diagnostics

## 10. Findings Summary (Plain Language)

3–5 bullet points stating what was learned. No numbers; just the substantive findings as a clinician would want to read them.

## 11. Limitations

- Unmeasured confounders (and the E-value lower bound)
- Missing-data assumptions (MAR / MCAR / MNAR rationale)
- Generalisability constraints (cohort representativeness)
- Selection bias risks
- Information bias / measurement bias risks
- Compliance constraints (DUA cell-N rules, etc.)

## 12. Reproducibility Checklist

- [ ] All scripts saved to date-stamped folder under `Scripts/`
- [ ] All output files saved with date stamp in filename
- [ ] Random seeds fixed where stochastic methods used
- [ ] Software environment documented (Python version + package versions)
- [ ] Data version frozen (registry submission date / dataset DOI)
- [ ] Pre-specified analysis plan archived (link)
- [ ] Master significance table includes BH-FDR + Bonferroni
- [ ] Every reported number traceable to a script + script line / cell

## 13. Files Referenced

| File | Type | Description |
|---|---|---|
| `Scripts/.../V4_xx.py` | Script | What it computes |
| `Tables/.../v4_t1_baseline_*.csv` | Output | What it contains |
| `Figures/.../Figure_V4_01_*.png` | Output | What it shows |

## 14. Verification Trail

What independent verification was performed (numerical re-derivation, hand calculation on a 2×2 subset, alternative software, etc.) and what was the result.

## 15. Next Steps

What the analysis suggests should happen next: additional analyses, manuscript writing, peer review, replication in an external cohort.
```

#### When the report is written

- **Mandatory at Step 8 transition** (Excel file ready). The report is built immediately after the Excel workbook so the two are date-aligned.
- **Re-generated whenever the analysis is re-run** (e.g., after PI revisions). Treat the report as a versioned artefact; archive prior versions to `Archives/` rather than overwriting in place.
- **Read first by every subsequent session** that touches this analysis. The report is the single source of truth for what was done; future sessions should not re-derive findings without first reading the latest report.

#### Cross-references

- The report's **Methods section** is the source from which the manuscript's Methods section is drafted; do not write methods text into the manuscript without first reading this report.
- The report's **Results section** is the source for the manuscript's Results.
- The report's **Limitations** feed the manuscript Discussion.
- The report's **Files Referenced** table is the cross-walk for the manuscript's reproducibility statement.

#### Compliance check

Before the report is declared complete, confirm:

- [ ] Every claim in section 8 has an effect size, 95% CI, P value, and (where applicable) BH-FDR Q.
- [ ] Every percentage is paired with numerator/denominator.
- [ ] Every table reference resolves to an actual saved file.
- [ ] Every script reference resolves to an actual saved file.
- [ ] No internal hypothesis IDs (Q-numbers etc.) in the user-facing text — replace with descriptive endpoint labels.
- [ ] Section 11 (Limitations) is not empty.
- [ ] Section 12 (Reproducibility) has every checkbox addressed.
- [ ] Filename and location follow the convention.

If any check fails, the report is not complete. Do not exit the analysis session until all checks pass.

---

---

## After Analysis

Execute the STEP 9b completion checkpoint writes above, then inform the user:

> "Analysis complete."

If running in Mode A (stateful):
> "State files updated:
> - `project_state.json` — status: analysis_complete
> - `analysis_plan.json` — 13/13 steps complete
> - `results_registry.json` — primary result recorded
> - `decision_log.md` — methodological decisions logged
>
> Next steps:"

If running in Mode B without state:
> "Next steps:"

Then always:
> - `/visualize` to generate publication-quality figures
> - `/write-methods-results` to draft the Methods and Results sections
> - `/write-manuscript` for the full manuscript pipeline
> - `/resume-project` in a future session to pick up where you left off

## CHANGELOG / Lessons Learned

This section accretes domain-specific lessons from real analyses. Append a new entry whenever a session surfaces a new pattern, gap, or correction worth carrying forward.

### 2026-04-24 — V3 Esophageal Cancer Disparity Analysis (Bilal Mirza, U Arizona)

#### Ten new mandatory checks added based on real-world findings

1. **Within-stratum sanity check for any pp-gap finding (Simpson's-paradox prevention).** A V3 deep-dive claimed NHB tumors were 25% larger at presentation (+10 mm overall, P=10⁻²²); within-stage analysis revealed identical median size in Stage I/II/III/IV strata. The overall finding was a stage-distribution artifact. **Action:** Whenever a continuous-variable pp/percent gap is reported, ALWAYS run a within-stratum analysis on the most-relevant confounder (stage, age, histology). Add a sub-step "6a.5 — Within-stratum sanity for continuous outcomes" before the primary analysis.

2. **Cox HR estimand sensitivity to cohort definition (all-stages vs surgically-curable).** Reporting Cox HR 1.15 on the all-stages cohort understated the disparity in the surgically-curable Stage I-III complete-case cohort (HR 1.45). Stage IV dilutes any access-mediated effect. **Action:** Report HR for BOTH the all-stages cohort AND the mechanism-relevant subset.

3. **Time-stratified Cox as standard for biphasic disparity questions.** Schoenfeld test for race PH was satisfied (p=0.589), but time-stratified Cox in 0–6 / 6–12 / 12–24 / 24+ month windows revealed BIPHASIC disparity (HR 1.53 / 1.19 / 1.42 / 1.34). **Action:** When the research question implicates a time-bound mechanism (e.g., surgical access acts in the first 6 months), include time-stratified Cox even when global PH holds.

4. **Unknown-as-category vs complete-case sensitivity for adjusted models.** Excluding patients with Unknown insurance/CDCC/income gave OR 0.59. Including them as their own categories gave OR 0.75. ~17% of the cohort had Unknown values. **Action:** When >5% of any covariate is Unknown, present BOTH inclusive (Unknown-as-category) and exclusive (complete-case) primary results with rationale.

5. **E-value alongside every fully-adjusted residual effect.** E-value of 2.78 (surgery OR 0.59) is strong; E-value of 1.57 (Cox HR 1.15) is modest. Reporting both side-by-side demonstrates relative robustness. **Action:** Mandatory E-value reporting (point + CI bound) for every fully-adjusted residual exposure effect in the abstract and Table 2. Use VanderWeele-Ding formula. Promote from optional to MANDATORY in Step 5.

6. **Master Significance Table with primary + secondary + BH-FDR for the entire test family.** Reporting 26 separate tests across 16 questions without family-wise correction risks 1+ false positives at α=0.05. BH-FDR revealed that some primary-significant findings (Q21 time-to-surgery, Q23_immuno) lose significance after adjustment. **Action:** For papers with >5 hypothesis tests in the same domain, generate at Step 8 a master table: Test ID, Claim, pp-gap, Primary P, Primary BH-q, Adjusted P, Adjusted BH-q, Verdict.

7. **NCDB Data Use Agreement compliance — cell N≥11 rule.** A supplementary multi-race table contained 3 cells with N<11 (Hispanic/NHAPI minor categories). NCDB DUA prohibits publication of any cell with N<11. **Action:** For any NCDB analysis, generate both a "raw" version (internal) and a DUA-compliant version with cells <11 masked as "<11" — built into Step 8 Excel as a mandatory sheet.

8. **Stage I + Unknown-stage disparity vs late-stage parity.** Late-stage (III/IV) presentation rates were statistically identical between NHB (58.9%) and NHW (59.1%); P=0.557. The disparity was in Stage I underrepresentation (−5.4 pp; P=10⁻⁶³) and Unknown-stage over-representation (+4.4 pp; P=10⁻⁴⁴). **Action:** Decompose into Stage I vs II/III vs IV vs Unknown rather than reporting binary "late-stage" rates. The Unknown-stage rate is itself an outcome (workup-completeness disparity).

9. **Adjuvant-therapy / subgroup analyses need explicit power justification.** Q26 adjuvant nivolumab uptake post-CheckMate-577 had only n=178 NHB (vs 3,702 NHW). The 7.4 pp point estimate was not statistically significant in primary (P=0.056) or adjusted (P=0.23). **Action:** For any subgroup analysis with one arm <500, compute power for the observed effect size before interpreting null findings. Report findings honestly as "trend… not significant; likely underpowered" rather than as confirmed disparities.

10. **Provider-side gating vs patient-side decisions — distinguish in registry data.** NCDB Reason for No Surgery separated "Not recommended" (provider) from "Patient refused" (patient). NHB had 9.75 pp excess in "Not recommended" but identical 0.5% rate of patient refusal — strong evidence for clinician-driven mechanism. **Action:** When studying treatment-receipt disparities, analyze the reason-for-no-treatment field by race. Provider-side excess + identical patient-side refusal = strong evidence for clinician-driven mechanism.

#### Process improvements added to the workflow

- **Step 1 expansion:** Add formal MCAR/MAR/MNAR classification when missing >5% in any covariate; add IQR + z-score outlier scan as standard.
- **Step 6c expansion:** Add Schoenfeld PH test for the exposure coefficient specifically (not just global) for any Cox model; report p-value separately.
- **Step 7 expansion:** Add facility-clustered (or institution-clustered) standard errors as standard for any registry analysis (use `cluster_col` in lifelines); flag if clusters have median <5 cases per cluster.
- **Step 8 expansion:** Master Significance Table with primary + secondary + BH-FDR across all tests in the paper, plus DUA-compliant supplementary table.

---

### 2026-05-03 — HNSCC TAM Multi-Cohort Validation (Bilal Mirza, U Arizona)

#### Pre-submission rigor remediation pipeline (apply when an analysis is being staged for manuscript drafting)

The HNSCC-TAM session demonstrated a 6-phase remediation sequence that closes most audit issues without requiring a full pipeline re-run. Apply this whenever a multi-cohort secondary analysis is being readied for manuscript drafting and an audit has surfaced critical issues. Lessons L027–L037 in `skills/references/lessons-log.json` capture the trigger patterns and actions in machine-readable form.

**Phase 0 — Five-agent self-audit (per L027).** Before any rigor remediation, run a structured 5-agent audit (numerical, statistical, biological-plausibility, code-reproducibility, completeness) producing `AUDIT_REPORT.md` with severity-graded findings (CRITICAL / HIGH / MODERATE / MINOR). Each finding cites the source CSV row and the claimed value. The HNSCC-TAM audit caught 4 critical issues invisible from the report itself: a wrong AUROC value (0.806 vs source 0.751), pseudoreplication in cross-compartment correlations (n=8 treated as independent when true n=4 patients), an "8/8 testable findings validated" overclaim, and missing random seeds throughout the pipeline.

**Phase 1 — Surgical text/numerical fixes (per L027, L036).** For every audit-flagged numerical claim, verify against the source CSV at 3-decimal precision and apply targeted Edit-tool fixes to the report. Add a §0 Phase 1 Corrections Log block at the top of the corrected document with an explicit table: ID | Section | v_old text | v_new text | Source verification. Never overwrite the original document — increment the version (e.g., insights_report_v6.md → v7.md).

**Phase 2 — Statistical rigor pass (per L031, L032, L033).** A single Python script applies bootstrap BCa 95% CIs (paired resampling, 500 iterations, seed=42) to every AUROC, BH-FDR within each (cohort × signature panel), Bonferroni for the largest validation cohort (α = 0.05/n_tests), paired Wilcoxon for any pre/post comparison, and `random_state=42` to every stochastic scanpy call (sc.tl.pca / umap / leiden / neighbors / diffmap). Output: `phase2_remediation/results/phase2_auroc_with_bca_ci.csv` with columns AUROC, BCa_CI_low_95, BCa_CI_high_95, MW_p_two_sided, BH_q, BH_significant_q05, Bonferroni_significant. Flag CIs that span 0.5 as "not statistically distinguishable from chance."

**Phase 3 — Patient-level cross-compartment re-derivation + drop-LOO sensitivity (per L029, L030).** For any small-n discovery cohort with paired pre/post sampling, the n=8 (patient × treatment) framing is pseudoreplicated. Re-derive every cross-compartment correlation under THREE framings — (a) pseudorep n=8 sanity check, (b) patient-level n=4 averaged pre+post, (c) pre-treatment baseline n=4 — using exact permutation testing (`scipy.stats.permutation_test` with `permutation_type='pairings'` and `n_resamples=np.inf` for n≤5; Monte Carlo 10,000 resamples for n=6–8). The asymptotic Spearman p-value formula breaks at |ρ|=1 (returns p=0 spuriously). At n=4 the minimum two-sided exact Spearman p is 2/24 = 0.083 — a structural floor. Reframe failing-to-reach-floor correlations as HYPOTHESIS-GENERATING in the manuscript. Separately, compute per-patient cell-pool contribution for every subtype; if any patient exceeds 50%, generate Drop-Patient-X leave-one-out sensitivity for every finding involving that subtype.

**Phase 4 — Canonical meta-validation table v2 (per L034).** A consolidation script reads all upstream CSVs and produces three deliverables: `meta_validation_v2_long.csv` (one row per Finding × Cohort × Statistic with full provenance — typically 30–50 rows), `meta_validation_v2_summary.csv` (one row per Finding with audit-correct headline — typically 12–20 rows), and `meta_validation_v2.xlsx` (formatted workbook). Headline-selection priority order: EXTERNALLY VALIDATED > HYPOTHESIS-GENERATING (audit-corrected n) > PARTIAL > ROBUST > NOVEL > largest-N fallback. The summary CSV becomes Manuscript Table 1.

**Phase 5 — Mandatory 16-section analysis report.** Per `working-rules.md`, the durable deliverable is `Reports/analysis_report_<question-slug>_<date>.md` with the 16-section template. This is the manuscript Methods source.

**Phase 6 — Numerical re-audit (per L036).** A `phase6_numerical_reaudit.py` script registers named checks via `add_check(name, claimed, observed_in_source, tolerance, unit)` covering: (a) claimed text values vs source CSV cells, (b) summary-table values vs upstream long-table values, (c) document-internal stale-string scans, (d) sample-size sums. Output: `phase6_audit_log.csv` + `phase6_audit_summary.txt` + `AUDIT_REPORT_v2.md`. Target 100% PASS at 3-decimal precision before manuscript submission.

**Cross-cutting: 4-tier evidence framework (per L035).** After all six phases, partition every finding into 4 tiers for manuscript placement: Tier 1 (ROBUST + Bonferroni-survivor) → abstract; Tier 2 (PARTIAL = BH-FDR-only) → body as supportive; Tier 3 (NOVEL single-cohort + EXTERNALLY VALIDATED cross-compartment) → main text + future-work; Tier 4 (HYPOTHESIS-GENERATING) → Discussion + Limitations only, NEVER abstract. Tier 4 framing in Limitations: "directionally consistent but not statistically distinguishable from chance after multiple-testing correction at this sample size."

**Cross-cutting: Manuscript document hierarchy (per L037).** A multi-cohort manuscript project maintains four narrative artifacts in this order: (a) `Reports/insights_report_v*.md` (technical insights), (b) `Reports/analysis_report_<slug>_<date>.md` (16-section technical report), (c) `Reports/FINAL_manuscript_brief_<date>.md` (manuscript-ready narrative for PI review — written BEFORE the manuscript itself), (d) `Manuscripts/manuscript_complete_<date>.docx` (deliverable).

#### Worked example artifacts (HNSCC-TAM session, 2026-05-03)

The HNSCC-TAM project's Phase 1–6 deliverables provide a concrete reference template:

```
TAM_Analysis/
├── AUDIT_REPORT.md                            (Phase 0 — original 5-agent audit)
├── AUDIT_REPORT_v2.md                         (Phase 6 — closure: 40 PASS / 0 FAIL)
├── phase2_remediation/
│   ├── PHASE2_REPORT.md
│   ├── scripts/phase2_rigor_pass.py
│   ├── scripts/seed_all.py
│   └── results/phase2_auroc_with_bca_ci.csv
├── phase3_remediation/
│   ├── PHASE3_REPORT.md
│   ├── scripts/phase3_pseudorep_and_pt2_sensitivity.py
│   └── results/phase3_cross_compartment_n4_vs_n8.csv
├── phase4_remediation/
│   ├── PHASE4_REPORT.md
│   ├── scripts/phase4_build_meta_validation_v2.py
│   └── results/meta_validation_v2_summary.csv
├── phase6_audit/
│   ├── phase6_numerical_reaudit.py
│   ├── phase6_audit_log.csv
│   └── phase6_audit_summary.txt
├── Reports/
│   ├── insights_report_v7.md                  (Phase 1 — corrected primary insights)
│   ├── analysis_report_hnscc-tam-multicohort-validation_2026-05-02.md  (Phase 5 — 16-section technical report)
│   └── FINAL_manuscript_brief_2026-05-03.md   (manuscript-ready narrative for PI review)
└── Manuscripts/
    ├── manuscript_draft_v1_2026-05-03.md
    ├── manuscript_complete_2026-05-03.docx
    ├── tables_standalone_2026-05-03.docx
    ├── figures_standalone_2026-05-03.docx
    └── abstract_standalone_2026-05-03.docx
```

Total wall-clock for the rigor remediation: ~90 minutes across 6 sessions. End state: every numerical claim has a source CSV, a 95% CI or paired p-value where applicable, and a documented multiple-testing-correction status.

---

> **Maintainer note:** Append new lessons here, dated, with the originating session and the action item. This skill should accrete capability over time. If a future session finds a lesson is wrong or superseded, mark it as deprecated rather than deleting — the audit trail matters.
