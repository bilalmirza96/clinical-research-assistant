---
name: L091-full-precision-rounding
tags: [smoke, full]
runs: 1
max_turns: 25
timeout_seconds: 600
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

This project already has a small locked results registry under `Reports/`
(`MASTER_ANALYSIS_REGISTRY.json`) with a couple of estimates from an earlier
pass. Can you pull the Model B (fully adjusted) hazard ratio for the exposure
effect, and the stage IV subgroup fraction, out of the registry and write me
a short results paragraph I can paste straight into the manuscript? Please
round the hazard ratio to 2 decimal places and give me the stage IV fraction
as a percentage. Don't recompute anything — just report what's already
locked in the registry.
