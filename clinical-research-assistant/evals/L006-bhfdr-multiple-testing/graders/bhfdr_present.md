---
type: regex
pattern: '(BH-?FDR|Benjamini-?Hochberg|false discovery rate)'
flags: i
match: contains
target: trace
weight: 1
---

Lesson L006/L032 (master significance table with BH-FDR): with more than 5
hypothesis tests in the same domain, the agent must apply a Benjamini-Hochberg
false-discovery-rate correction, not just report 6 raw p-values.
