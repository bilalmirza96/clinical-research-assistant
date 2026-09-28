---
type: llm
weight: 2
criteria: |
  When computing the APC mutation rate, the agent must not treat a patient
  whose panel does not test APC (PANEL_B_50gene patients in this fixture) as
  APC-wild-type (i.e. must not silently code their missing APC row as 0
  and fold them into the denominator as non-mutated). Instead it should
  either exclude those patients from the APC-rate denominator, report them
  separately as "not tested" / coverage-limited, or otherwise clearly flag
  that the panel-vs-WES comparison is confounded by panel gene coverage.
  A response that reports a single pooled "APC mutation rate" across all
  patients without addressing this, or that visibly fills off-panel gene
  status with 0/wild-type, should score low.

  Judge this against the agent's final message and any output file it
  produced -- the actual deliverable -- not intermediate scratch reasoning.
  If the run ended without the agent ever giving a final answer about the
  APC rate (e.g. it was cut off mid-tool-call with no response), fail this
  grader and state the reason as "no final answer" rather than guessing at
  credit for unfinished work.
---
