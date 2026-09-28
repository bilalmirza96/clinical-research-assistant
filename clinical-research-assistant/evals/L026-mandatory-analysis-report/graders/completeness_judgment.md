---
type: llm
weight: 1
criteria: |
  The deliverable the agent produced (or, if the run was cut short, its most
  advanced draft) should read like a genuine structured analysis report, not
  a bare chat summary: it should state the research question, describe the
  cohort and variables used, name the statistical method(s), report the
  effect estimate with a confidence interval and a p-value, and include a
  limitations section appropriate to a 50-patient synthetic cohort (e.g.
  small sample size, exploratory nature). Every percentage or count claim
  should be paired with its numerator/denominator (e.g. "31/50 (62%)"),
  not a bare percentage. Score high only if most of these are present with
  real numbers pulled from the data, not placeholders.
---
