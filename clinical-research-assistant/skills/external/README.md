# External Pasted Skills

Paste borrowed or third-party skills here when you want Clinical Research Assistant to consider them during routing.

BioMedAgent is intentionally housed here because it is a third-party/external skill, even though CRA treats `skills/external/biomedagent/` as the canonical delegated execution engine for omics, genomics, non-tabular biomedical files, and ML-heavy workflows.

Supported formats:

```text
skills/external/<skill-name>/SKILL.md
skills/external/<skill-name>.skill
skills/external/<bundle-name>/.../<skill-name>/SKILL.md
```

After pasting or removing a skill, run this from the plugin root:

```bash
python3 tools/update_skill_registry.py
```

The updater regenerates:

- `skills/references/skill-registry.yaml`
- `skills/references/external-skills.md`

The generated files are deterministic, so rerunning the updater without skill changes should produce no git diff.

If an external skill has the same `name` as an internal CRA skill, the updater keeps the internal skill canonical and gives the external copy a namespaced registry id such as `external-<bundle>-<skill>`.

External skills should usually be support skills. If an external skill becomes core to the clinical-research workflow, promote it into `skills/internal/`, update the router, and add a lesson explaining why it became first-party.
