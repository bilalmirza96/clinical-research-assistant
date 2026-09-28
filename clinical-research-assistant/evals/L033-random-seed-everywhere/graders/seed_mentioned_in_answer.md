---
type: regex
pattern: '(random_state\s*=\s*42|seed(?:ed)?\s*(?:=|of|:)?\s*42|reproducib\w*)'
flags: i
match: contains
target: trace
weight: 1
---

Somewhere in the run (code, or the agent's own explanation), a fixed seed of
42 or an explicit reproducibility statement should appear — the agent
should not present a stochastic bootstrap result without disclosing that it
was seeded for reproducibility.
