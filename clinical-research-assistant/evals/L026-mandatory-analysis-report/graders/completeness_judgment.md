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

  Judge this against the produced `analysis_report_*.md` file (or, failing
  that, the agent's final message) -- the actual deliverable -- not
  intermediate scratch reasoning. A genuine partial draft, cut short by the
  turn/time budget, should still be judged on its own real content per the
  "most advanced draft" allowance above. But if the run ended without the
  agent ever producing any report file OR any final answer describing one
  (e.g. it was cut off mid-tool-call with nothing to show), fail this grader
  and state the reason as "no final answer" rather than guessing at credit
  for unfinished work.
---
