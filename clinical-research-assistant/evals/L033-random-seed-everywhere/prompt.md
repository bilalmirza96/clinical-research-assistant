---
name: L033-random-seed-everywhere
tags: [smoke, full]
runs: 1
max_turns: 40
timeout_seconds: 900
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

I have a small synthetic clinical cohort at `data/cohort_50.csv` (50 patients:
age, sex, race_ethnicity, stage, treatment, exposure, time_months, event,
comorbidity_index, insurance_type). I want a first pass at whether the
`exposure` variable (delayed care) is associated with survival — a
Kaplan-Meier look and an unadjusted Cox model for the hazard ratio. Since it's
only 50 patients, please also give me a bootstrap 95% confidence interval
around that hazard ratio so I know how stable the estimate is before I invest
more time in this. Please save the analysis script you use under `scripts/`
in this workspace — that's where every analysis script lives in this lab,
so I can rerun or reuse it later.
