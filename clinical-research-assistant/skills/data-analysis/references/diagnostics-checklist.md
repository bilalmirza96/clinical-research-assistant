# Diagnostics Checklist

Full diagnostic protocol per model type with specific tests and thresholds.

## All Models — Universal Checks

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Multicollinearity | VIF for all covariates | VIF > 5: concern; VIF > 10: remove | Remove or combine collinear variables |
| Events per variable | EPV = min(events, non-events) / covariates | EPV < 10: warn; EPV < 5: halt | Reduce covariates or use penalized methods |
| Influential observations | Cook's distance | Cook's D > 4/n | Investigate; report sensitivity without outliers |
| Sample size adequacy | N per group | < 20 per group: warn | Consider exact tests or non-parametric alternatives |

## Logistic Regression

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Calibration | Hosmer-Lemeshow test | p < 0.05: poor fit | Consider alternate functional forms or additional covariates |
| Calibration (visual) | Calibration plot | Deviation from 45° line | Report visually; consider recalibration |
| Discrimination | ROC/AUC | AUC < 0.6: poor | Report honestly; do not overinterpret |
| Linearity of logit | Box-Tidwell test (continuous vars) | p < 0.05: nonlinear | Use restricted cubic splines or categorize |
| Separation | Perfect/quasi-complete separation | Model fails to converge or extreme ORs | Use Firth logistic regression |
| Goodness of fit | Likelihood ratio test | Compare nested models | Report chi-square and p-value |

## Cox Proportional Hazards

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Proportional hazards | Schoenfeld residuals test | p < 0.05: PH violated | Stratify, use time-varying coefficient, or restricted mean survival time |
| Proportional hazards (visual) | Log-log plot | Non-parallel curves | Same as above |
| Influential observations | dfbeta residuals | |dfbeta| > 2/√n | Investigate and report sensitivity analysis |
| Functional form | Martingale residuals vs continuous covariate | Nonlinear pattern | Use restricted cubic splines |
| Overall fit | Cox-Snell residuals | Deviation from 45° line | Report; consider alternative model |

## Linear Regression

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Linearity | Residuals vs fitted plot | Non-random pattern | Transform outcome or use nonlinear terms |
| Homoscedasticity | Breusch-Pagan test / residual plot | p < 0.05 or funnel pattern | Use robust standard errors (HC3) |
| Normality of residuals | Q-Q plot + Shapiro-Wilk | p < 0.05 or deviation from line | Transform outcome; use robust SEs for large N |
| Independence | Durbin-Watson (if time series) | < 1.5 or > 2.5 | Use GEE or time-series methods |

## Propensity Score Methods

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Covariate balance | Standardized mean differences (SMD) | All SMD < 0.1 (ideal); < 0.2 (acceptable) | Re-specify PS model; add interaction terms |
| Balance (visual) | Love plot (before/after) | — | Must show improvement for all covariates |
| Overlap / positivity | Propensity score distribution plot | No overlap region | Trim to common support; consider IPTW trimming |
| Extreme weights (IPTW) | Weight distribution | Max weight > 10× median | Stabilize weights; truncate at 1st/99th percentile |
| Residual confounding | E-value | — | Report E-value and interpret: "An unmeasured confounder would need RR of X.XX to explain away the observed association" |

## Poisson / Negative Binomial Regression

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Overdispersion | Deviance / Pearson chi-square / n | Ratio > 1.5 | Switch to negative binomial or quasi-Poisson |
| Zero inflation | Proportion of zeros vs expected | Excess zeros | Use zero-inflated Poisson or negative binomial |
| Goodness of fit | Pearson chi-square test | p < 0.05 | Consider alternative distribution |

## Competing Risks (Fine-Gray)

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| Proportional subdistribution hazards | Scaled Schoenfeld residuals | p < 0.05: violated | Consider cause-specific Cox models or time-varying coefficients |
| Competing event rates | Report cumulative incidence | — | Always report both event types; standard KM overestimates |

## Reporting Diagnostics in Manuscripts

In the **Methods** section, state which diagnostics were performed (e.g., "Proportional hazards assumption was assessed using Schoenfeld residuals"). Do NOT report results here.

In the **Results** section or **Supplementary Material**, report diagnostic outcomes:
- "The proportional hazards assumption was met for all covariates (all p > 0.05)"
- "VIF values ranged from 1.1 to 3.2, indicating no significant multicollinearity"
- "The Hosmer-Lemeshow test indicated adequate model calibration (p = 0.42)"
