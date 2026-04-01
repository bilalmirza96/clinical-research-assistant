# Command Ownership Map

Defines the single canonical owner for each command in the Clinical Research Assistant plugin.

## Rules

1. Each command has exactly ONE canonical skill file that owns its workflow.
2. `skills/data-analysis/SKILL.md` is a **policy file** — it owns no commands.
3. `CLAUDE.md` is the **orchestrator** — it routes commands to skill files but does not override their workflows.
4. BioMedAgent (`skills/biomedagent/SKILL.md`) is a **delegated execution engine** — it is invoked by the orchestrator when data complexity requires autonomous multi-agent processing, but does not own user-facing commands.

## Command Ownership Table

| Command | Canonical Owner | Type |
|---|---|---|
| `/project-init` | `skills/project-init/SKILL.md` | Workflow skill |
| `/resume-project` | `skills/resume-project/SKILL.md` | Workflow skill |
| `/analyze` | `skills/analyze/SKILL.md` | Workflow skill |
| `/visualize` | `skills/visualize/SKILL.md` | Workflow skill |
| `/literature-review` | `skills/literature-review/SKILL.md` | Workflow skill |
| `/write-manuscript` | `skills/write-manuscript/SKILL.md` | Workflow skill |
| `/write-introduction` | `skills/write-introduction/SKILL.md` | Workflow skill |
| `/write-methods-results` | `skills/write-methods-results/SKILL.md` | Workflow skill |
| `/write-discussion` | `skills/write-discussion/SKILL.md` | Workflow skill |

## Support Files (Not Command Owners)

| File | Role |
|---|---|
| `skills/data-analysis/SKILL.md` | Analytical policy: guardrails, diagnostics, registry cautions, reporting rules |
| `skills/references/writing-style.md` | Writing style reference for manuscript skills |
| `skills/data-analysis/references/*` | Method selection, registry cautions, diagnostics checklist |
| `CLAUDE.md` | Orchestrator: routes commands, defines core rules and role |

## BioMedAgent Delegation

BioMedAgent is invoked when:
- The dataset requires autonomous multi-step processing
- Complex bioinformatics pipelines are needed
- The task exceeds what interactive step-by-step analysis can handle

BioMedAgent does NOT:
- Own any user-facing `/command`
- Override the orchestrator's routing
- Make methodological decisions without applying the policy file guardrails
