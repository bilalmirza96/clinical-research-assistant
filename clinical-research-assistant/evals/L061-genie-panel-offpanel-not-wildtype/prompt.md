---
name: L061-genie-panel-offpanel-not-wildtype
tags: [smoke, full]
runs: 1
max_turns: 40
timeout_seconds: 900
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

I have mutation calls from a mixed-platform cohort in `data/tmb_mixed.csv`
(long format: patient_id, platform [WES or panel], panel_name, gene,
gene_mutated, plus TMB fields). Some patients were sequenced by whole-exome
sequencing and others on one of two different targeted gene panels, which
don't all cover the same genes. Can you build a patient-by-gene mutation
matrix and tell me what fraction of the cohort has an APC mutation, and
whether that differs by platform?
