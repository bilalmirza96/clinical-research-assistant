# Internal CRA Skills

This folder contains first-party Clinical Research Assistant skills.

These are the original native workflows that CRA owns:

- `project-init`
- `resume-project`
- `analyze`
- _(merged into `analyze` 2026-05-30; policy now at `analyze/references/clinical-analysis-policy.md`)_
- `literature-review`
- `visualize`
- `write-introduction`
- `write-methods-results`
- `write-discussion`
- `write-abstract`
- `write-manuscript`

The user should normally invoke `skills/clinical-research-assistant/SKILL.md`, not these directly. The router reads `skills/references/skill-registry.yaml`, selects the best internal skill, and then follows that skill's workflow.

When adding a new first-party CRA capability, put it here and run:

```bash
python3 tools/update_skill_registry.py
```
