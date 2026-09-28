---
type: regex
pattern: '^##\s*\d+\.\s*(Research Question|Cohort Selection|Variables|Statistical Methods|Results|Limitations|Reproducibility)'
flags: im
match: count:4
target: files
weight: 1
---

The analysis-report template (`analyze/references/analysis-report-template.md`)
requires numbered sections such as "1. Research Question", "4. Cohort
Selection (CONSORT-Style)", "5. Variables", "6. Statistical Methods",
"8. Results", "11. Limitations", and "12. Reproducibility Checklist". At
least 4 of these numbered section headings should appear somewhere in the
files the agent produced.
