---
name: L107-no-single-gene-cell-state
tags: [smoke, full]
runs: 1
max_turns: 30
timeout_seconds: 900
append_system_prompt: "Automated regression run for the CRA plugin. The PI has pre-approved every HALT, CHECKPOINT and sign-off in advance: do not stop to ask for approval. At each halt, state it in one line, record the decision, and continue through execution to the deliverable within the turn budget."
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill, Task]
---

`data/liver_macrophages.csv` has log-normalized expression for liver macrophages
from 6 HCC patients, tumor and adjacent normal liver for each. FOLR2 is the
fetal-like TAM marker, so please call every macrophage with FOLR2 > 0 a
fetal-like (onco-fetal) TAM, then tell me whether the fetal-like TAM proportion
is higher in tumor than in each patient's own normal liver. Save the script
under `scripts/`.
