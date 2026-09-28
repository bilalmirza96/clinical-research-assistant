---
type: regex
pattern: '(=\s*1\.27\b|\bwas\s+1\.27\b|\bHR\s+1\.27\b|\b1\.27\s*\()'
flags: i
match: not_contains
target: last_message
weight: 1
---

The final answer should not REPORT the naive/incorrect rounding "1.27" as the
Model B hazard ratio (registry value 1.275, which must round half-up to 1.28
at 2 decimal places per L091). This only fails on a reported-value context
("= 1.27", "was 1.27", "HR 1.27", "1.27 (") appearing in the agent's final
message -- not on a mention of "1.27" while explaining why naive/banker's
rounding is wrong (e.g. "naive rounding would give 1.27, but the correct
value is 1.28"), and not on anything said mid-run that never made it into
the final answer.
