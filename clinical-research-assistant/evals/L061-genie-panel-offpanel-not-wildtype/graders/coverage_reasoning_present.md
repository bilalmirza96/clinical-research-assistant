---
type: regex
pattern: '(not[-\s]?tested|off[-\s]?panel|panel (?:does not|doesn.t) (?:cover|test|include)|not (?:on|covered by) (?:the |that )?panel|NaN)'
flags: i
match: contains
target: trace
weight: 1
---

Lesson L061 (GENIE panel coverage): one of the two synthetic panels in this
fixture (`PANEL_B_50gene`) does not test APC (or SMAD4). The agent's
reasoning or code should show explicit awareness that a gene absent from a
patient's panel is NOT-TESTED, not wild-type, e.g. language like "not
tested", "off-panel", or coding those cells NaN rather than 0.
