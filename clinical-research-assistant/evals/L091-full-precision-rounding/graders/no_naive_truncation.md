---
type: regex
pattern: '\b1\.27\b'
flags: ''
match: not_contains
target: trace
weight: 1
---

The final answer should not contain the naive/incorrect rounding "1.27" for
the Model B hazard ratio (registry value 1.275, which must round half-up to
1.28 at 2 decimal places per L091).
