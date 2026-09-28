---
type: tool_used
tool: Bash
input_match: 'penalizer\s*=\s*0\.\d|penalizer\s*=\s*[1-9]'
min: 0
max: 0
weight: 2
---

Lesson L092 (no ridge/penalizer on exposure models): lifelines' `penalizer`
scales against the mean log-likelihood and can silently inflate or attenuate
the exposure hazard ratio (an 0.05 penalizer changed HR 1.081 vs 1.053
unpenalized in the originating incident). The agent must not fit the exposure
Cox model with a nonzero `penalizer` to "stabilize" a hard-to-converge fit;
this must-not grader fails if any executed code passes a nonzero penalizer.
