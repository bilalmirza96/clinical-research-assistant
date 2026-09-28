---
type: llm
weight: 1
criteria: |
  The agent should present something resembling the "master significance
  table" required by lesson L006: for each of the 6 comparisons, an endpoint
  name, the cohort, the effect estimate or test statistic, a primary p-value,
  a BH-FDR Q-value, and a Bonferroni-significant yes/no flag. It's fine if
  this is a markdown table or a clearly itemized list rather than a
  literal Excel table, as long as all 6 comparisons are covered and both
  corrections are actually applied (not just named). Score low if the agent
  only reports raw p-values and asserts significance without showing the
  corrected values.

  Judge this against the agent's final message and any report file it
  produced -- the actual deliverable -- not intermediate scratch reasoning.
  If the run ended without the agent ever giving a final answer or producing
  a deliverable file (e.g. it was cut off mid-tool-call with no response),
  fail this grader and state the reason as "no final answer" rather than
  guessing at credit for unfinished work.
---
