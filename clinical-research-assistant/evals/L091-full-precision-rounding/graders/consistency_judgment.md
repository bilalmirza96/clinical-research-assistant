---
type: llm
weight: 1
criteria: |
  The agent sourced both numbers (the Model B hazard ratio and the stage IV
  proportion) from the registry rather than recomputing or inventing them,
  and applied one consistent, correct rounding rule across both -- it should
  not use a different rounding convention for one number than the other.
  The Model B hazard ratio (registry value 1.275) rounds half-up to 1.28 at
  2 decimal places, not 1.27 (Python's native `round()` under banker's
  rounding). The stage IV proportion (registry value 0.2, n=10/50) is an
  exact whole-cohort fraction with no rounding ambiguity -- expressed as a
  percentage it is exactly 20%, so any answer that reports something other
  than 20% for it (without a stated reason) is wrong regardless of rounding
  convention.

  If, despite the registry now being internally consistent, the agent still
  flags a specific number as ambiguous or unsafe to report and explains a
  concrete, genuine reason tied to the actual data (not merely hedging) --
  do not penalize that halt as a rounding-consistency failure. Judge the
  rounding rule actually applied to whichever numbers the agent did report;
  do not fail the run solely for having asked a clarifying question or
  flagged a real data issue.

  Judge this against the agent's final message (the results paragraph it
  was asked to produce) -- the actual deliverable -- not intermediate
  scratch reasoning. If the run ended without the agent ever giving a final
  answer (e.g. it was cut off mid-tool-call with no response), fail this
  grader and state the reason as "no final answer" rather than guessing at
  credit for unfinished work.
---
