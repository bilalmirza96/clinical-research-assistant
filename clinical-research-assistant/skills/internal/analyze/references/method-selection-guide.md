# Method Selection Guide

Decision table for selecting the appropriate statistical model based on outcome type and study design.

## By Outcome Type

| Outcome Type | Unadjusted Test | Multivariable Model | Effect Measure |
|---|---|---|---|
| Binary | Chi-square / Fisher's exact | Logistic regression | OR (95% CI) |
| Binary (rare events, EPV <10) | Fisher's exact | Firth logistic regression | OR (95% CI) |
| Continuous (normal) | Student's t-test / ANOVA | Linear regression | β (95% CI) |
| Continuous (non-normal) | Mann-Whitney U / Kruskal-Wallis | Linear regression (transformed) or quantile regression | β (95% CI) |
| Count | Chi-square | Poisson or negative binomial regression | IRR (95% CI) |
| Time-to-event | Log-rank test | Cox proportional hazards | HR (95% CI) |
| Time-to-event (competing risks) | Gray's test | Fine-Gray subdistribution hazard | SHR (95% CI) |
| Ordinal | Mann-Whitney U | Ordinal logistic regression | OR (95% CI) |

## By Study Design

| Design Feature | Adjustment Method |
|---|---|
| Independent observations | Standard models above |
| Clustered data (e.g., facility-level) | GEE or mixed-effects model |
| Repeated measures | Mixed-effects model or GEE |
| Matched pairs | Conditional logistic regression / McNemar's test |
| Non-randomized treatment comparison | Propensity score methods (matching, IPTW, or stratification) |

## Covariate Selection Strategy

| Strategy | When to Use |
|---|---|
| A priori (preferred) | Covariates selected based on clinical knowledge and DAG before analysis |
| Change-in-estimate | Include if covariate changes primary estimate by >10% |
| Stepwise (discouraged) | Only for exploratory/hypothesis-generating analyses; report as such |

## Events-Per-Variable (EPV) Rule

- Target EPV ≥ 10 for stable estimates
- If EPV < 10: reduce covariates, use penalized regression (Firth), or collapse categories
- If EPV < 5: model results are unreliable — consider alternative approaches

## Multiple Testing Corrections

| Method | When to Use |
|---|---|
| Bonferroni | Conservative; use for independent comparisons with strong control needed |
| Benjamini-Hochberg (FDR) | Preferred for biomarker panels and exploratory analyses |
| No correction | Pre-specified primary analysis (single primary outcome) |

## Within-Recipient Propensity Matching  *(per L039)*

When a multi-stage access-disparity study reports a **within-treatment-recipient** comparison — e.g., NHB vs. NHW *among patients who actually received the treatment* — the comparison is no longer an access question; it is an **effectiveness/quality** question. The estimand has shifted, and the matching strategy must shift with it.

### When this applies

Any sentence of the form: *"Among patients who received [treatment X], [exposure group A] had [outcome] compared to [exposure group B]…"*

Common manifestations:
- NHB vs NHW patients **who received surgery** (operative outcomes / oncologic effectiveness)
- Hispanic vs NHW patients **who received chemotherapy** (regimen response, treatment-related mortality)
- Medicaid vs private-insurance patients **who reached transplant** (graft survival, rejection)

### Required matching approach

| Element | Standard (across-recipient) PSM | Within-recipient PSM  *(this pattern)* |
|---|---|---|
| **Estimand** | Effect of receiving the treatment | Effect of exposure *conditional on having received the treatment* |
| **Cohort** | Full eligible cohort | Restricted to patients who received the treatment |
| **PS model covariates** | Pre-treatment patient + access variables (insurance, distance, facility type, comorbidities, stage) | Pre-treatment patient + access + **treatment-quality variables** (facility volume, surgeon experience, time-to-treatment, neoadjuvant receipt, regimen completeness) |
| **Caliper** | 0.20 × SD logit PS standard | Same, but verify caliper-binding diagnostic (see diagnostics-checklist L040) |
| **Interpretation** | "Disparity in access" | "Disparity in outcomes among those treated — likely reflecting treatment-quality or unmeasured tumor biology" |

### Reporting requirement

State the estimand explicitly in the abstract and Methods: *"We estimated the [Race/Insurance/Other] disparity in [outcome] among patients who received [treatment], using propensity score matching on pre-treatment access and treatment-quality covariates."* Never present a within-recipient HR/OR as if it were an access estimate.

**Anti-pattern:** Reporting a within-recipient adjusted HR and claiming it represents the "overall disparity." This understates the access component (Stage IV / pre-treatment death) and overstates the effectiveness component. The two estimands must be reported separately when both are scientifically relevant.
