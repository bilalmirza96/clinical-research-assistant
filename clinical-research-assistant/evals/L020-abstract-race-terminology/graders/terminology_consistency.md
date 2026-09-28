---
type: llm
weight: 1
criteria: |
  The revised abstract should use race/ethnicity labels that match what was
  actually measured in the dataset's own coding (e.g. "Non-Hispanic White",
  "Non-Hispanic Black", "Hispanic", "Non-Hispanic Asian/Pacific Islander" —
  the categories used in cohort_50.csv / typical NCDB-SEER-style registry
  vocabulary), consistently throughout the abstract, rather than swapping in
  ancestry-flavored terms in some places and registry labels in others.
  Score low if any sentence still implies a genetic-ancestry claim ("European
  American", "EUR", etc.) without stating that ancestry/germline data was
  measured.

  Judge this against the edited `abstract_draft.md` file on disk (the actual
  deliverable the user asked to be cleaned up in place), not the agent's
  in-chat commentary about what it plans to change. If the run ended without
  the agent ever actually editing the file (e.g. it was cut off mid-tool-call
  and `abstract_draft.md` is unchanged from the seeded draft), fail this
  grader and state the reason as "no final answer" rather than guessing at
  credit for unfinished work.
---
