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
| **Caliper-binding diagnostic**  *(per L040)* | Caliper-sensitivity table across 3+ widths (e.g., 0.1 / 0.2 / 0.25 × SD logit PS) | Matched-pair count near-identical across calipers → caliper is NOT binding | If matched-pair counts plateau, smaller caliper is not changing the matched set — note this as evidence of stable matched cohort. If counts shift materially (>10%), the matched estimate is caliper-sensitive — report all three caliper estimates and choose the pre-specified one as primary |

### Caliper-binding interpretation  *(per L040)*

When a PSM caliper-sensitivity table shows nearly identical matched-pair counts across several caliper widths, the caliper is not the constraint — the underlying overlap region is. This is a **positive signal**: it means the matched cohort is stable and not artificially produced by a permissive caliper. **State this explicitly** in the Methods and Supplementary: *"Caliper sensitivity analysis (0.10, 0.20, 0.25 × SD logit PS) produced n = X, X, X matched pairs respectively; the caliper was not the binding constraint, indicating overlap region (rather than caliper width) determined the matched cohort."* Conversely, if matched-pair counts shift meaningfully across calipers, the matched estimate is caliper-sensitive and the choice of caliper drives the result — report all calipers and pre-specify the primary.

## Small-Cohort / Single-Cell Discovery Diagnostics  *(per L030)*

For small-n discovery cohorts (typically n ≤ 10 patients), and especially scRNA-seq / paired pre-post designs where each patient contributes many cells, run these subject-level sensitivity checks before reporting any cross-cell finding:

| Check | Method | Threshold | Action if Failed |
|---|---|---|---|
| **Subject-level dominance** | For each cell-type pool, compute per-patient contribution as a fraction of total cells | Any single patient contributes > 50% of a cell-type pool | Generate Drop-Patient-X leave-one-out (LOO) sensitivity for every finding involving that subtype. If the finding disappears under LOO, reframe as HYPOTHESIS-GENERATING |
| **Pseudoreplication** | Identify the true independent unit (patient ≠ cell ≠ time-point) | Cells or paired samples treated as independent observations | Reframe at the patient level: average within-patient first, then perform inference on n = patients |
| **Exact-test p-value floor** | For paired Spearman / Wilcoxon at n ≤ 5, compute the exact distribution-floor p | n = 4 → 2-sided exact Spearman p-floor = 2/24 = 0.083 | A "p = 0" from asymptotic formulas is spurious. Use `scipy.stats.permutation_test(permutation_type='pairings', n_resamples=np.inf)` for n ≤ 5; Monte Carlo 10,000 for n = 6–8 |
| **Random seed mandate** | Verify `random_state=42` set on every stochastic step (scanpy: pca / umap / leiden / neighbors / diffmap) | Any step missing the seed | Re-run the affected step with seed set. Without this, downstream cluster labels and embeddings drift run-to-run |

**Reporting standard:** Any small-n discovery finding that survives drop-LOO and exact-test p-floor passes Tier-1 evidence in the manuscript. Findings that depend on a single patient → relegate to Discussion + Limitations only, framed as hypothesis-generating.

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
