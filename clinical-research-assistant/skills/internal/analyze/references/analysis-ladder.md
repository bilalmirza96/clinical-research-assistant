# Analysis ladder: compute and compare in this order

**Rule (author directive 2026-09-25, L087).** Estimate every primary and secondary objective on
each rung below, in this order, on one analytic cohort, and report the rungs side by side. There
are exactly two adjusted models: Model A adjusts for clinical variables only, and Model B adds
everything else. The movement from one rung to the next is a finding, so every rung is decided
for every objective: run it, or record in `analysis_plan.ladder.skipped` why not. Rungs 4, 7 and
8 apply "where relevant", and "not relevant because ..." is a reason; silence is not. A deadline
shortens the prose around the ladder, never the ladder: "just give me the one adjusted model" is
answered with the ladder and a one-line summary of it.

| # | Rung | Question it answers | Runs when | Registry suffix |
|---|---|---|---|---|
| 1 | Unadjusted | How large is the raw difference? | Always (Phase 4) | `.crude` |
| 2 | Model A: clinical | Does it persist after the clinically relevant variables and confounders? | Always | `.modelA` |
| 3 | Model B: fully adjusted | Does it persist after everything else as well: socioeconomic, access, facility and any other pre-specified confounder? | Always | `.modelB` |
| 4 | Adjusted survival curves | What is the difference on the absolute scale, e.g. adjusted 2-year survival? | Time-to-event outcomes | `.adjsurv` |
| 5 | IPTW (and PSM) | Does a design-based estimator that balances covariates agree with the outcome models? | Every non-randomized comparison | `.iptw`, `.psm` |
| 6 | E-values | How strong would unmeasured confounding need to be to explain the estimate away? | Every adjusted estimate reported as a finding | `.evalue` |
| 7 | Causal mediation | How much of the difference runs through a measured intermediate (treatment received, stage at diagnosis)? | The question asks why or through what, and a mediator is measured after the exposure and before the outcome | `.mediation.<mediator>` |
| 8 | ML or other novel methods | What can the ladder not show: heterogeneity, non-linearity, decomposition, a target-trial emulation? | It answers a question rungs 1-7 cannot; exploratory unless pre-specified in the approved plan | `.<method>` |

## Covariate sets (proposed in the plan, locked at HALT 2A)

- **Model A** = the clinically relevant variables and confounders: age, sex, year of diagnosis,
  comorbidity, stage, histology, grade, tumour size, performance status, and other disease
  features present at baseline.
- **Model B** = Model A plus everything else pre-specified: socioeconomic and access factors
  (insurance, area income, area education, rurality, distance), facility type and volume, region,
  and any other confounder the DAG supports.
- **No other adjusted models.** No socioeconomic-only model, no third "combined" model, no M1-M5
  sequence (author decision 2026-09-25).
- **Never in Model A or Model B:** anything measured after the exposure that may lie on the path
  to the outcome (treatment received, pathologic stage, post-diagnosis events). Those are
  mediators and belong to rung 7; adjusting for them in a total-effect model is overadjustment.
- **In a disparities study** socioeconomic and access factors may be mediators of the exposure
  rather than confounders. The change from Model A to Model B shows how much of the difference
  they account for; it never "explains away" a disparity or shows it is "not real".

## Comparing the rungs

One table per objective, rungs as rows in the order above. `scripts/ladder_table.py` builds it,
adds E-values, and flags the problems below; Checkpoint B requires zero unresolved flags.

| Rung | Estimate (95% CI) | N | Change from unadjusted, % (log scale) | E-value (CI limit) |
|---|---|---|---|---|

- **Constant cohort.** Rungs 1-3 are fit on the same patients. If Model B needs complete
  socioeconomic data, fit rungs 1-3 on that complete-case cohort for the comparison, or keep
  everyone with an Unknown category or multiple imputation (L004). A crude estimate on 114,633
  patients and a Model B estimate on 98,000 are not comparable.
- **Attenuation metric.** Default is the percentage change on the log scale,
  100 x (ln est_crude - ln est_k) / ln est_crude, which treats protective and harmful estimates
  alike. Name the metric in the table header and use one metric per project.
- **ORs and HRs are non-collapsible**, so part of the change between nested models is not
  confounding. Rungs 4 and 5 (absolute scale, marginal estimands) are the check.
- **A sign flip across rungs** is investigated (`science-superpowers:investigating-anomalous-results`)
  before anything is reported.
- **Write it in order.** Results walk the ladder ("unadjusted HR 1.30; Model A (clinical) 1.14;
  Model B (fully adjusted) 1.09; IPTW 1.21; E-value 1.42"). The Discussion attributes the
  attenuation, not the residual, to the measured factors.

## Rung requirements

**4 Adjusted survival.** Direct (standardized) survival from the Model B Cox model averaged over
the whole cohort, or IPTW-weighted Kaplan-Meier; say which. Report the adjusted difference at the
project's single time horizon with a bootstrap CI (1,000 or more replicates, seed 42), and the
RMST difference when proportional hazards fail.

**5 IPTW and PSM.** The propensity model uses the HALT 2A matching variables (normally the Model B
set). Stabilized weights; a stated truncation rule (for example 1st/99th percentile); SMD below
0.1 on every covariate after weighting; effective sample size; robust (sandwich) standard errors;
ATE or ATT stated. PSM is the matched design variant: caliper 0.2 SD of the logit, caliper
sensitivity per L040, pairs and maximum post-match SMD registered. Doubly robust estimation
(AIPW, TMLE) is a rung-8 extension.

**6 E-values** (VanderWeele and Ding), for the point estimate and the CI limit nearer the null, on
every adjusted ratio estimate, with the formula for the measure and the outcome frequency.
`ladder_table.evalue(est, lo, hi, measure, common)` refuses an OR or HR without `common=`.

| Measure | Rare outcome (<15%) | Common outcome |
|---|---|---|
| RR | RR | RR |
| OR | RR = OR | RR = sqrt(OR) |
| HR | RR = HR | RR = (1 - 0.5^sqrt(HR)) / (1 - 0.5^sqrt(1/HR)) |

Then E = RR + sqrt(RR x (RR - 1)), inverting RR first when it is below 1. The REPEAT DISPARITIES
surgery E-value that circulated as 3.41 was the RR formula applied to an OR of 0.50 for a 48%
outcome; the correct value was 2.17.

**7 Causal mediation.** Counterfactual methods only: regression-based or g-formula natural direct
and indirect effects with the exposure-mediator interaction tested (four-way decomposition), or
interventional effects when the exposure cannot be manipulated (race). For survival, work on an
additive or AFT scale, or with g-formula survival; never the difference-of-HRs method, which is
non-collapsible (superseded in REPEAT DISPARITIES on 2026-06-23). Pre-specify mediators measured
after the exposure and before the outcome. Report the proportion mediated with a bootstrap CI and
the E-value of the residual direct effect. Report a joint share when several mediators are asked
about together, because separate shares do not add. Write "mediation analysis suggests", never
"X explains the disparity".

**8 ML and other novel methods**, chosen by question: effect heterogeneity (causal forest,
meta-learners with honest splitting); non-linear dose-response (splines, g-computed curves);
decomposition of a gap into explained and unexplained parts (Kitagawa-Oaxaca-Blinder); doubly
robust estimation (AIPW, TMLE, boosted-tree IPTW); target-trial emulation (L069); competing risks;
quantitative bias analysis. These never replace rungs 1-7. Variable importance (SHAP) is
association, not cause. Seed 42 and honest validation (cross-fitting or held-out data) are
mandatory, and results enter the registry under their own keys, labelled exploratory unless
pre-specified in the HALT 1-approved analysis plan.

## Common mistakes

| Mistake | Fix |
|---|---|
| One adjusted model because of a deadline | Run the ladder; shorten the prose, not the analysis |
| An existing single model "tightened" into a sentence because nobody wants to redo the analysis | Run the ladder on the reconciled cohort before the sentence is written; a caveat does not replace it |
| Extra adjusted models (socioeconomic-only, "combined", M1-M5) | Two adjusted models only: Model A clinical, Model B everything |
| Treatment received adjusted as a confounder | It is a mediator: rung 7 |
| Crude on the full cohort, Model B on complete cases | One cohort for rungs 1-3 |
| RR formula on a common-outcome OR or HR | `evalue(..., measure=, common=)` |
| Difference-of-HRs "proportion mediated" | Counterfactual mediation on an additive or AFT scale |
| PSM, IPTW or mediation "deferred" without a reason | Run them, or record the reason in `ladder.skipped` |
| ML importance read as a cause | State it as association; keep the ladder primary |

## Where it sits in /analyze

Phase 2 writes `analysis_plan.ladder` (rungs, covariate sets, skipped reasons). HALT 2A approves
the Model A and Model B covariate sets and the candidate mediators. Phase 4 runs rung 1, Phase 5A
rungs 2-5, Checkpoint B runs `ladder_table.py`, Phase 5B runs rung 6 with the sensitivity battery
and effect modification, and Phase 5C runs rungs 7-8. `Table_2` columns follow rung order.

Model A and Model B mean what they meant in REPEAT DISPARITIES (2026): Model A clinical, Model B
Model A plus socioeconomic and access factors. Registry keys use `.modelA` / `.modelB`.
