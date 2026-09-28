---
type: llm
weight: 1
criteria: |
  The agent sourced both numbers (the Model B hazard ratio and the stage IV
  subgroup fraction) from the registry rather than recomputing or inventing
  them, applied one consistent half-up rounding rule to both, and did not
  silently use a different rounding convention for the two numbers. The
  stage IV fraction (registry value 0.625) expressed as a whole percent
  should be 63% (half-up), not 62% (Python's banker's-rounding default).
  Score high only if the rounding is consistent and correct for both values.
---
