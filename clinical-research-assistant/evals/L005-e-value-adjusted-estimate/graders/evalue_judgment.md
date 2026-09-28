---
type: llm
weight: 1
criteria: |
  The E-value should be computed correctly for the measure actually used
  (e.g. if the adjusted estimate is a hazard ratio, the HR->RR-approximation
  formula; if an odds ratio, the OR formula, which additionally requires the
  agent to state or assume whether the outcome is common, per L087). The
  agent should interpret the E-value in plain language (how strong an
  unmeasured confounder would have to be, on both the risk-ratio and
  CI-limit scale) rather than just stating a bare number. Score low if the
  E-value is asserted without any interpretation, or computed with a formula
  mismatched to the reported measure.
---
