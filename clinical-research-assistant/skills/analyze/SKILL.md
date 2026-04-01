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

#### After STEP 9 (Final — Code Bundle Complete)

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

### STEP 9: Reproducible Code Bundle
- Complete Python script using: pandas, numpy, scipy, statsmodels, lifelines, scikit-learn, openpyxl
- Script must: load raw data, clean data, fit models, run diagnostics, generate all outputs
- Fixed random seed (42)
- `pip install` block with Python version and all package versions
- Analysis log: rows included/excluded, missing data handling, final N, model diagnostics

---

## After Analysis

Execute the STEP 9 completion checkpoint writes above, then inform the user:

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
