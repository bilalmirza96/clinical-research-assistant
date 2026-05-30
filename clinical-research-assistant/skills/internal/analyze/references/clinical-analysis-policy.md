# Clinical Analysis Policy (reference)

> **Migrated 2026-05-30.** This was formerly the standalone `data-analysis` skill. It is now an on-demand reference owned by `/analyze` (no longer a separate skill). `/analyze` reads it at INTAKE/PLAN; other skills point here for shared policy.


# Clinical Analysis Policy

> **This is a policy file, not a command skill.** It does not own `/analyze`, `/visualize`, `/write-manuscript`, or any other command. Command ownership is defined in the canonical skill files under `skills/internal/`.

## Purpose

Provides shared analytical standards that all command skills reference. Any skill performing statistical work, generating figures, or writing manuscript text should apply these policies.

<biomedagent_adapted_methodology>
## BioMedAgent-adapted methodology — read first

Before any analysis, read in this order: (1) `../../references/lessons-log.json` to scan for matching prior patterns; (2) `../../references/biomedagent-methodology.md` for the three-phase pipeline (Plan → Execute → Verify), task classification routing table, and anti-misclassification rules. Apply the six-way classification (descriptive / inferential test / multivariable / survival / sensitivity / subgroup) before choosing a method. Append a new entry to `lessons-log.json` if the session surfaces a new pattern.
</biomedagent_adapted_methodology>

<mandatory_analysis_report>
## Every analysis must produce a structured report — MANDATORY

No analysis is considered complete without a date-stamped, structured markdown report. The report is what the manuscript Methods and Results sections are drafted from, what co-authors audit, and what future sessions read first before re-deriving anything.

**Filename pattern:** `analysis_report_<short-question-slug>_YYYY-MM-DD.md`
**Location:** project's `Analyses/` or `Reports/` folder.

**Required sections (in this order, no omissions):**

1. Header (date, analyst, project, scripts, datasets, output files)
2. Research question
3. Estimand (target population, exposure, outcome, time horizon, framework)
4. Data sources
5. Cohort selection cascade (CONSORT-style with N at each step)
6. Variables (outcome, exposure, confounders, missing-data handling)
7. Statistical methods (per analysis: method, software + version, adjustment set, assumption checks, alpha, multiple-testing correction)
8. Pre-specified sensitivity analyses
9. Results (cohort characteristics, primary, secondary, sensitivity, subgroup, multiple-testing master summary)
10. Diagnostic checks (Schoenfeld, VIF, PS overlap, residuals, convergence)
11. Findings summary (plain language, no numbers)
12. Limitations (unmeasured confounders + E-value, missing-data assumptions, selection bias, generalisability, DUA constraints)
13. Reproducibility checklist
14. Files referenced (script + output cross-walk table)
15. Verification trail
16. Next steps

**Every claim must include** effect size, 95% CI, P value, and (where applicable) BH-FDR Q value. Every percentage must be paired with numerator/denominator. The full report template, compliance checks, and cross-reference rules live in the parallel `analyze/SKILL.md` Step 9 section — read that template before writing your first report. Re-generate the report whenever the analysis is re-run; archive prior versions rather than overwriting.
</mandatory_analysis_report>

## Core Obligations

---

## Methodological Guardrails

### Model Selection

| Outcome Type | Unadjusted | Multivariable | Effect Measure |
|---|---|---|---|
| Binary | Chi-square / Fisher's | Logistic regression | OR (95% CI) |
| Binary (rare, EPV <10) | Fisher's | Firth logistic | OR (95% CI) |
| Continuous (normal) | t-test / ANOVA | Linear regression | beta (95% CI) |
| Continuous (non-normal) | Mann-Whitney U | Linear regression (transformed) | beta (95% CI) |
| Count | Chi-square | Poisson / negative binomial | IRR (95% CI) |
| Time-to-event | Log-rank | Cox PH | HR (95% CI) |
| Time-to-event (competing risks) | Gray's test | Fine-Gray subdistribution | SHR (95% CI) |

### Design Adjustments

| Design Feature | Method |
|---|---|
| Clustered data | GEE or mixed-effects |
| Repeated measures | Mixed-effects or GEE |
| Matched pairs | Conditional logistic regression |
| Non-randomized comparison | Propensity score methods |

---

## Diagnostics Expectations

All models must pass diagnostics BEFORE results are finalized.

### Universal Checks

| Check | Method | Threshold |
|---|---|---|
| Multicollinearity | VIF | >5 concern, >10 remove |
| Events per variable | EPV | <10 warn, <5 halt |
| Influential observations | Cook's D | >4/n investigate |

### Model-Specific

- **Logistic**: Hosmer-Lemeshow, ROC/AUC, Box-Tidwell linearity, separation detection
- **Cox PH**: Schoenfeld residuals (p<0.05 = PH violated), dfbeta, Martingale residuals
- **Linear**: Breusch-Pagan homoscedasticity, Shapiro-Wilk normality, residual patterns
- **Propensity scores**: SMD <0.1 ideal / <0.2 acceptable, overlap assessment, weight distribution, E-value

For full protocol per model type, see `references/diagnostics-checklist.md`.

---

## Registry Cautions

### NSQIP
30-day outcomes ONLY. No cause-specific mortality. CPT-based identification.

### NCDB
No cause-specific survival (overall only). Facility-level clustering requires GEE/mixed models. Covers ~70% of cancer cases.

### SEER
~35% US population. No systemic therapy data. Cause-specific survival available. Medicare linkage for age 65+.

### UNOS/OPTN
Analyze within consistent allocation policy eras. Distinguish waitlist vs post-transplant outcomes.

### NTDB
Voluntary, not population-based. Verify ISS calculation. High GCS missingness. In-hospital mortality only.

### MBSAQIP
30-day outcomes only. Report both %EWL and %TWL. Distinguish primary vs revisional.

### General Registry Rules
- Validate coding accuracy against data dictionary
- Consider temporal trends and policy changes
- Missingness is rarely MCAR
- Watch for immortal time bias in registry cohorts

For detailed registry-specific coding issues, see `references/registry-cautions.md`.

---

## Reporting Rules

- Default alpha = 0.05, two-sided tests
- Always report: effect size, 95% CI, p-value, N analyzed
- Always state reference category for categorical variables
- Avoid unnecessary dichotomization of continuous variables
- Prefer confidence intervals over star-based significance
- Interpret clinical magnitude, not only statistical significance
- P-values: exact to 3 decimals
- Effect estimates: 2 decimals
- Percentages: 1 decimal

---

## Observational Language Rules

- Use **association language** for observational studies: "was associated with", "was observed", "patients who received X had"
- **Never** use causal language ("caused", "led to", "resulted in", "due to") unless the study design justifies it (RCT, IV, regression discontinuity)
- Journals will reject observational studies that use causal language
- In Discussion sections, hedging is required for interpretive claims: "suggest", "may", "support a hypothesis"
- In Results sections, state findings directly with near-zero hedging

---

## Stop-and-Warn Conditions

Halt the analysis and request clarification if ANY of these apply:

- Outcome not defined or coding ambiguous
- Exposure unclear or defined after time zero (immortal time risk)
- Dataset too small for intended analysis
- Missing >40% in key variables with no imputation strategy
- Time-to-event analysis without censoring variable or undefined time origin
- Ambiguous coding without data dictionary
- No overlap in propensity score distributions
- Severe multicollinearity (VIF >10) or extremely sparse cells

---

## Bias Vigilance Checklist

Flag explicitly if detected:

- Overadjustment (mediator included as covariate)
- Collider bias
- EPV <10
- Multiple testing inflation
- Immortal time bias risk
- Reverse causation risk
- Overfitting (model too complex for sample size)
- Poor propensity score overlap

If a fatal flaw is detected, HALT and explain before proceeding.

---

## Data Provenance — MANDATORY  *(per L046 candidate)*

Every project must maintain rigorous data provenance. The discipline:

### Read-only raw data

Raw source files are **never modified** by any analysis skill. They are read in-place from their canonical location (registry export, institutional download, prior project export). The project's `data/working/` directory holds derived artifacts; raw source files stay in their original home.

### Filtered cohort artifacts

Every project that runs an analysis produces these artifacts in `data/working/`:

| Artifact | Purpose |
|---|---|
| `cohort.csv` | The filtered, analysis-ready cohort. Produced by applying inclusion/exclusion filters to raw source in memory. |
| `filter_operations.json` | Machine-readable replayable filter sequence. Each operation: `{step, op, expr, n_in, n_out}`. Source sha256 recorded at top. |
| `filter_log.md` | Human-readable filter history as a CONSORT-style table (rows in → rows out → rationale per step). |
| `source_manifest.json` | Where raw came from (path + sha256 + read date + license). |

### Replay requirement

The `data/working/` artifacts are reproducible: given the raw source at the recorded sha256, re-running `filter_operations.json` produces a `cohort.csv` byte-identical to the recorded sha256. The Code-reproducibility auditor (`/analyze` Phase 6, Agent 4) verifies this.

### What to halt on

- **Raw source hash mismatch** — if the canonical raw file's sha256 differs from `source_manifest.json`, halt and surface the discrepancy. Do not silently re-filter against a changed source.
- **`data/working/` does not exist** — halt and direct user to run `/project-init` (which creates the folder scaffold).
- **`filter_operations.json` missing for an existing `cohort.csv`** — halt; the cohort is unreproducible without its filter sequence.

### Cross-cohort harmonization

When multiple cohorts are compared (SEER vs NCDB, internal vs external, etc.), each cohort has its own `data/working/` + filter logs. Cross-cohort comparison additionally requires a `cohort_harmonization_log.md` per L011 (see `references/registry-cautions.md` Cross-Cohort Comparison Harmonization section).

---

## Reference Files

For detailed lookup during analysis, consult:
- `references/method-selection-guide.md` — Model selection by outcome type and study design
- `references/registry-cautions.md` — Registry-specific coding issues and limitations
- `references/diagnostics-checklist.md` — Full diagnostic protocol per model type
- `references/variable-collapse-defaults.md` — Default category-collapse rules when user does not specify (used by `/analyze` Phase 1 INTAKE)
