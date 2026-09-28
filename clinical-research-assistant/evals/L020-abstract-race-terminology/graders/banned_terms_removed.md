---
type: regex
pattern: '(Caucasian|Oriental|European American)'
flags: i
match: not_contains
target: {source: file, path: abstract_draft.md}
weight: 2
---

Lesson L020 (abstract race terminology): the draft uses deprecated/offensive
race vocabulary ("Caucasian", "Oriental") and promotes self-reported race to
ancestry-flavored vocabulary ("European American") without ancestry data. The
edited `abstract_draft.md` should no longer contain any of these terms.
