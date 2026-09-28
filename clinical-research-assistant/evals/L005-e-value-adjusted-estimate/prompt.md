---
name: L005-e-value-adjusted-estimate
tags: [smoke, full]
runs: 1
max_turns: 25
timeout_seconds: 600
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

For `data/cohort_50.csv`, can you fit a model for the `exposure` variable's
(delayed care) effect on survival, adjusting for age, stage, and comorbidity
index? Once you have the adjusted estimate, I'd also like to know how robust
it is — how much unmeasured confounding it would take to explain the
association away.
