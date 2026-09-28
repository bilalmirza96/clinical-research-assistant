---
name: L026-mandatory-analysis-report
tags: [full]
runs: 1
max_turns: 40
timeout_seconds: 900
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

Can you run a complete analysis of whether the `exposure` variable (delayed
care) in `data/cohort_50.csv` is associated with receipt of definitive
treatment and with survival? This is a real deliverable for the project, not
just a quick look — please give me a written report I can file and hand to a
co-author, not just a chat summary.
