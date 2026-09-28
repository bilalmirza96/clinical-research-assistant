---
type: tool_used
tool: Bash
input_match: '(random_state\s*=\s*42|np\.random\.default_rng\(\s*42\s*\)|random_state=42|seed\s*=\s*42)'
min: 1
weight: 1
---

Lesson L033 (random_state=42 everywhere): any stochastic step the agent runs
in this task — most likely the bootstrap resampling used to build the 95% CI
around the hazard ratio — must pass an explicit seed of 42 (e.g.
`random_state=42`, `np.random.default_rng(42)`, or an equivalent seeded RNG).
At least one Bash-executed command must show this seed being set explicitly;
an unseeded `np.random.choice` / `resample` call would reproduce the exact
regression this lesson exists to prevent (cluster/bootstrap results that
silently change between runs).
