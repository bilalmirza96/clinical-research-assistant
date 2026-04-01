# Ownership Map

This file records the current source-of-truth ownership for major responsibilities in `clinical-research-assistant` after the first cleanup pass.

## Canonical command owners

- `/project-init` -> `clinical-research-assistant/skills/project-init/SKILL.md`
- `/resume-project` -> `clinical-research-assistant/skills/resume-project/SKILL.md`
- `/analyze` -> `clinical-research-assistant/skills/analyze/SKILL.md`
- `/visualize` -> `clinical-research-assistant/skills/visualize/SKILL.md`
- `/literature-review` -> `clinical-research-assistant/skills/literature-review/SKILL.md`
- `/write-introduction` -> `clinical-research-assistant/skills/write-introduction/SKILL.md`
- `/write-methods-results` -> `clinical-research-assistant/skills/write-methods-results/SKILL.md`
- `/write-discussion` -> `clinical-research-assistant/skills/write-discussion/SKILL.md`
- `/write-manuscript` -> `clinical-research-assistant/skills/write-manuscript/SKILL.md`

## Supporting policy owners

- Clinical analytical policy support -> `clinical-research-assistant/skills/data-analysis/SKILL.md`
- Writing style reference -> `clinical-research-assistant/skills/references/writing-style.md`

## State templates

- `templates/state/project_state.template.json`
- `templates/state/study_spec.template.json`
- `templates/state/analysis_plan.template.json`
- `templates/state/manuscript_state.template.json`
- `templates/state/decision_log.template.md`

## Delegation

- BioMedAgent is a delegated execution engine, not the manuscript orchestrator.
- Delegation rules are defined in `DELEGATION_RULES.md`.
