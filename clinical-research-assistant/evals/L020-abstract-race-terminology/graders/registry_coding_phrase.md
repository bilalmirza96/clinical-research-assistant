---
type: regex
pattern: 'self-reported race'
flags: i
match: contains
target: {source: file, path: abstract_draft.md}
weight: 1
---

Per L020's remediation, the draft should add "self-reported race per registry
coding" (or clearly equivalent phrasing) once, typically in Methods, to
preempt the reviewer question about race versus genetic ancestry.
