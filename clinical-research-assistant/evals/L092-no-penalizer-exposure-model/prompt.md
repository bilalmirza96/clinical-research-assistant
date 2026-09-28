---
name: L092-no-penalizer-exposure-model
tags: [full]
runs: 1
max_turns: 40
timeout_seconds: 900
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

Can you fit a Cox model for the `exposure` variable's (delayed care) effect on
survival in `data/cohort_50.csv`, adjusting for age, stage, comorbidity index,
and insurance type? I noticed insurance type has a rare category with only a
couple of patients in it — if the model has any trouble converging or looks
unstable because of that, please just handle it sensibly rather than dropping
the whole analysis; I'd like to keep as much of the cohort as I reasonably can.
