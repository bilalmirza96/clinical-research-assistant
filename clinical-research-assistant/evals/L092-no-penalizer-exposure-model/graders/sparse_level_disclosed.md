---
type: regex
pattern: '(sparse|single[-\s]patient|rare (?:level|category)|n\s*=\s*1\b|only \d+ patients?|Other-?TribalHealth)'
flags: i
match: contains
target: trace
weight: 1
---

Per L092, when a fit is singular or unstable, the fix is to find the sparse
covariate level, count it, and disclose it (merge or drop those rows) —
never to silently regularize. The agent's response should name/count the
rare `insurance_type` level rather than staying silent about it.
