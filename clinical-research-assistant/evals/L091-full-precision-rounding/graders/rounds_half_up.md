---
type: regex
pattern: '\b1\.28\b'
flags: ''
match: contains
target: trace
weight: 2
---

Lesson L091 (one Decimal ROUND_HALF_UP formatter, boundary guard): the
registry's Model B hazard ratio is stored as 1.275. Rendered at 2 decimal
places with correct half-up rounding this is 1.28. Python's native
`round(1.275, 2)` gives 1.27 because of float representation — exactly the
bug this lesson exists to prevent. The final answer should contain "1.28".
