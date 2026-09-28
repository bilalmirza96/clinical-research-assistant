---
name: L006-bhfdr-multiple-testing
tags: [full]
runs: 1
max_turns: 25
timeout_seconds: 600
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

Using `data/cohort_50.csv`, can you test whether receipt of definitive
treatment differs by each of the following, one comparison per variable: age,
sex, race/ethnicity, stage, comorbidity index, and insurance type? That's six
separate comparisons against the same treatment outcome. Tell me which of the
six are still significant once you account for running all six tests
together, not just by their raw p-values.
