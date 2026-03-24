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
