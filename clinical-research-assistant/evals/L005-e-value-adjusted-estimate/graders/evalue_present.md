---
type: regex
pattern: 'E-?value[^\n]{0,60}\d'
flags: i
match: contains
target: trace
weight: 2
---

Lesson L005 (mandatory E-value): for any fully-adjusted residual exposure
effect, the agent must report a VanderWeele-Ding E-value (point estimate and
CI-limit) for the adjusted association, not just the adjusted HR/OR itself.
The word "E-value" should appear together with an actual computed number.
