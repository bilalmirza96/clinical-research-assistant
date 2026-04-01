---
name: clinical-analysis-policy
description: Supporting policy skill containing methodological guardrails, diagnostics expectations, registry cautions, and reporting rules for clinical research analysis. NOT a command owner — the canonical /analyze command lives in skills/analyze/SKILL.md.
---

# Clinical Analysis Policy

> **This is a policy file, not a command skill.** It does not own `/analyze`, `/visualize`, `/write-manuscript`, or any other command. Command ownership is defined in the canonical skill files under `skills/`.

## Purpose

Provides shared analytical standards that all command skills reference. Any skill performing statistical work, generating figures, or writing manuscript text should apply these policies.

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

## Reference Files

For detailed lookup during analysis, consult:
- `references/method-selection-guide.md` — Model selection by outcome type and study design
- `references/registry-cautions.md` — Registry-specific coding issues and limitations
- `references/diagnostics-checklist.md` — Full diagnostic protocol per model type
