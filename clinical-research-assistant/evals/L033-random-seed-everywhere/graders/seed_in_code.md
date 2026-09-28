---
type: regex
pattern: '(random_state\s*=\s*42|np\.random\.default_rng\(\s*42\s*\)|default_rng\(\s*42\s*\)|seed\s*=\s*42)'
flags: ''
match: contains
target: files
weight: 1
---

Lesson L033 (random_state=42 everywhere): any stochastic step the agent runs
in this task — most likely the bootstrap resampling used to build the 95% CI
around the hazard ratio — must pass an explicit seed of 42 (e.g.
`random_state=42`, `np.random.default_rng(42)`, or an equivalent seeded RNG).

This grader checks the CONTENTS of whatever files the agent produced (the
prompt asks it to save its analysis script under `scripts/`) rather than a
top-level `tool_used: Bash` call, because the `analyze` skill delegates code
execution to a subagent via the `Task` tool: the actual `Bash` invocations
happen inside that subagent's own transcript, which a top-level `tool_used`
grader cannot see (it only sees tools the primary agent called directly) --
that blind spot let an unseeded bootstrap regression through undetected
(L033 grader-brittleness finding, 2026-09-28). Checking the saved script's
on-disk contents is agnostic to who executed it.
