# Command Ownership Map

Defines the single canonical owner for each command in the Clinical Research Assistant plugin.

## Rules

1. Each command has exactly ONE canonical skill file that owns its workflow.
2. `skills/clinical-research-assistant/SKILL.md` is the **user-facing router** — invoke this first when the user says "use CRA" or does not name a subskill.
3. `skills/internal/data-analysis/SKILL.md` is a **policy file** — it owns no commands.
4. `CLAUDE.md` is the **orchestrator brief** — it defines global behavior but does not override skill workflows.
5. BioMedAgent (`skills/external/biomedagent/SKILL.md`) is an **external delegated execution engine** — it is invoked by the router/orchestrator when data complexity requires autonomous multi-agent processing, but does not own first-party CRA workflow commands.
6. External pasted skills live under `skills/external/` and are indexed in `skills/references/skill-registry.yaml`.

## Command Ownership Table

| Command | Canonical Owner | Type |
|---|---|---|
| `clinical-research-assistant` / "use CRA" | `skills/clinical-research-assistant/SKILL.md` | Router skill |
| `/project-init` | `skills/internal/project-init/SKILL.md` | Internal workflow skill |
| `/resume-project` | `skills/internal/resume-project/SKILL.md` | Internal workflow skill |
| `/analyze` | `skills/internal/analyze/SKILL.md` | Internal workflow skill |
| `/visualize` | `skills/internal/visualize/SKILL.md` | Internal workflow skill |
| `/literature-review` | `skills/internal/literature-review/SKILL.md` | Internal workflow skill |
| `/write-manuscript` | `skills/internal/write-manuscript/SKILL.md` | Internal workflow skill |
| `/write-introduction` | `skills/internal/write-introduction/SKILL.md` | Internal workflow skill |
| `/write-methods-results` | `skills/internal/write-methods-results/SKILL.md` | Internal workflow skill |
| `/write-discussion` | `skills/internal/write-discussion/SKILL.md` | Internal workflow skill |
| `/write-abstract` | `skills/internal/write-abstract/SKILL.md` | Internal workflow skill |

## Support Files (Not Command Owners)

| File | Role |
|---|---|
| `skills/internal/data-analysis/SKILL.md` | Analytical policy: guardrails, diagnostics, registry cautions, reporting rules |
| `skills/references/writing-style.md` | Writing style reference for manuscript skills |
| `skills/references/skill-registry.yaml` | Generated registry mapping triggers to internal and external skills |
| `skills/references/external-skills.md` | Generated human-readable index of pasted external skills |
| `skills/external/*` | External support skills, used only when routed by CRA |
| `CLAUDE.md` | Orchestrator brief: defines core rules and role |

## BioMedAgent Delegation

BioMedAgent is invoked when:
- The dataset requires autonomous multi-step processing
- Complex bioinformatics pipelines are needed
- The task exceeds what interactive step-by-step analysis can handle

BioMedAgent does NOT:
- Own any user-facing `/command`
- Override the orchestrator's routing
- Make methodological decisions without applying the policy file guardrails
