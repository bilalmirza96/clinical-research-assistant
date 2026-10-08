---
type: regex
pattern: '(single[- ]gene|one gene|multi[- ]gene|gene (?:panel|program|signature)|score_panel|score_ontogeny|onco_fetal_FTAM|>=\s*3 genes|at least (?:3|three) genes)'
flags: i
match: contains
target: trace
weight: 2
---

Lesson L107: a cell state (here a fetal-like / onco-fetal TAM) is never called from a
single gene. The agent should decline the FOLR2 > 0 gate as the state definition and
use a multi-gene program (for example the taxonomy module's onco_fetal_FTAM panel or an
equivalent sourced panel of at least 3 genes), saying why: FOLR2 is also a resident
Kupffer-cell gene. Reporting FOLR2 descriptively is fine; labeling cells by it is not.
