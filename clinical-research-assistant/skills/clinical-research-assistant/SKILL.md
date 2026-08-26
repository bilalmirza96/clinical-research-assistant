---
name: clinical-research-assistant
description: Primary router for the Clinical Research Assistant plugin. Use this single entry point for clinical research, biomedical data analysis, literature review, manuscript writing, abstract editing, figure generation, citation verification, and delegated BioMedAgent or external scientific-skill workflows.
argument-hint: "[research task, project path, manuscript request, dataset question, or skill-routing request]"
allowed-tools: Read Write Edit Bash
---

# Clinical Research Assistant Router

You are the front door for the entire Clinical Research Assistant system. The user should be able to invoke only this skill and have you select the best internal subskill, delegated engine, or external pasted skill.

## Read First

1. `../references/skill-registry.yaml` — machine-readable registry of internal and external skills.
2. `../references/external-skills.md` — human-readable index of pasted external skills.
3. `../references/lessons-log.json` — machine-readable lessons from prior clinical-research sessions.
4. `../references/biomedagent-methodology.md` — Plan -> Execute -> Verify discipline and anti-misclassification rules.
5. `../references/writing-style.md` — **required whenever the selected route will produce any prose**, including literature-review synthesis, cover letters, and reviewer responses, not only the `write-*` skills. Its final section, "House Academic Voice — Universal Standard (ALL CRA prose)", is the binding voice contract and overrides any conflicting section-specific guidance elsewhere in that file. Standing rule (2026-08-06, author request): one academic voice across every prose deliverable CRA produces. Before delivering, verify mechanically with `python3 tools/voice_check.py <draft> [--venue X] [--sections]` from the plugin root; a non-zero exit means hard failures remain and the draft is not deliverable.

**Claim-audit gate (L073, NON-NEGOTIABLE).** Also run `python3 tools/claim_audit.py <draft> --registry <MASTER_ANALYSIS_REGISTRY.json>`. It catches assertions of ABSENCE - "was not formally compared", "was never tested", "is not recorded" - that a registered result contradicts. `registry_lint` H8 traces numbers that are PRESENT and is structurally blind to these. Non-zero exit blocks submission-ready status. Two standing rules behind it: never assert a negative about the analysis state from memory (grep the registry first, including in conversational answers), and never treat generated prose - a draft, a summary, an earlier turn - as evidence of what an analysis found. When a hedge is genuinely warranted, write it as a positive statement of what WAS done, naming the key, rather than a bare negative.

If `../references/skill-registry.yaml` is missing, stale, or the user says they pasted a new skill into `skills/external/`, run:

```bash
python3 tools/update_skill_registry.py
```

Run it from the plugin root (`clinical-research-assistant/`, the directory that contains `tools/` and `skills/`).

## Invocation (READ THIS FIRST)

**This router is the only invocable skill name in the plugin:**

```
Skill(skill="clinical-research-assistant:clinical-research-assistant", args="<task>")
```

Claude Code discovers plugin skills at exactly `<plugin>/skills/<name>/SKILL.md`. Every CRA
subskill lives one level deeper — `skills/internal/<name>/SKILL.md` or
`skills/external/<name>/SKILL.md` — so **`clinical-research-assistant:analyze` (and every other
subskill name) returns `Unknown skill`.** The subskills are real and correct on disk; they are
simply not reachable by name. Callers name the subskill they want in this router's `args`, and
this router reads and executes it.

Note for maintainers: the plugin being present in `installed_plugins.json`, and the deployed
cache being in sync with the source repo, are both true while a subskill remains uninvocable.
Neither check tests reachability. If a new skill must be directly invocable, place it at
`skills/<name>/SKILL.md`. See lessons-log **L072**.

## Directory Model

- `skills/clinical-research-assistant/SKILL.md` — this router.
- `skills/internal/` — native CRA skills. These are the original first-party workflows.
- `skills/external/` — pasted third-party or borrowed skills. Users can drop either:
  - a folder containing `SKILL.md`, or
  - a `.skill` package archive.
  - a larger bundle that contains one or more nested `SKILL.md` files.
- `skills/references/skill-registry.yaml` — generated routing registry.
- `skills/references/external-skills.md` — generated external skill reference list.

## Routing Workflow

### Step 1 — Classify the Request

Classify every request before acting:

| Class | Route |
|---|---|
| New project, project scaffold, study setup | `skills/internal/project-init/SKILL.md` |
| Resume existing project | `skills/internal/resume-project/SKILL.md` |
| Clinical dataset analysis, regression, survival, registry analysis | `skills/internal/analyze/SKILL.md` plus `skills/internal/analyze/references/clinical-analysis-policy.md` policy |
| Biomedical omics, scRNA-seq, genomics, VCF/BAM/FASTQ/h5ad, ML-heavy workflow | `skills/external/biomedagent/SKILL.md` as delegated engine |
| Literature review, evidence synthesis, citation search | `skills/internal/literature-review/SKILL.md` |
| Citation audit, PMID/DOI verification, bibliography cleanup | Prefer an external citation skill if registered; otherwise use `skills/internal/literature-review/SKILL.md` |
| Publication figure generation | `skills/internal/visualize/SKILL.md`; delegate compute to BioMedAgent if modality is complex |
| Introduction drafting | `skills/internal/write-introduction/SKILL.md` |
| Methods/Results drafting | `skills/internal/write-methods-results/SKILL.md` |
| Discussion drafting | `skills/internal/write-discussion/SKILL.md` |
| Abstract drafting or audit | `skills/internal/write-abstract/SKILL.md` |
| Full manuscript orchestration | `skills/internal/write-manuscript/SKILL.md` |
| Manuscript quality-control audit | `skills/internal/manuscript-qc/SKILL.md` |

### Step 2 — Select the Best Skill

Use `skill-registry.yaml` as the source of truth. Prefer routes in this order:

1. Exact user-named internal skill or canonical delegated engine.
2. Internal CRA workflow skill with matching triggers.
3. External delegated engine (`biomedagent`) for complex biomedical execution.
4. External pasted skill with matching triggers, especially when the user explicitly asks for an external/imported skill.
5. Manual execution using the closest internal skill, then record a lesson if the routing gap should become durable.

If more than one skill fits, select one primary skill and list support skills. Example:

```text
Primary route: skills/internal/analyze/SKILL.md
Support policy: skills/internal/analyze/references/clinical-analysis-policy.md
Delegation: none
Reason: Standard NCDB survival/regression analysis.
```

### Step 3 — Read Only the Needed Skill Files

After selecting a route, open only the relevant `SKILL.md` files and direct references. Do not load the whole plugin.

### Step 4 — Execute Through the Selected Skill

Follow the selected skill's workflow exactly, including state files, approval gates, mandatory analysis reports, citation integrity rules, and manuscript audit requirements.

### Step 5 — Normalize Outputs Back Into CRA State

If an internal delegated engine or external pasted skill produces outputs, translate them back into CRA's shared state when relevant:

- `project_state.json`
- `study_spec.json`
- `dataset_profile.json`
- `analysis_plan.json`
- `evidence_bank.json`
- `citation_bank.json`
- `results_registry.json`
- `figure_registry.json`
- `manuscript_state.json`
- `decision_log.md`

External skills must not become disconnected side quests. Their outputs feed the CRA project.

## External Skill Intake Rules

When the user pastes a new skill or skill bundle into `skills/external/`:

1. Run `python3 tools/update_skill_registry.py`.
2. Inspect the generated entry in `skills/references/skill-registry.yaml`.
3. If the external skill has the same `name` as an existing canonical skill, keep the canonical route unless the user explicitly asks for the alternate copy.
4. If the auto-generated triggers are weak, update the skill folder's frontmatter description or add a manual override in this router skill only if needed.
5. Use the external skill as a support route unless it clearly should become a first-party CRA internal skill.

## Learning Rule

If routing fails, the selected skill is insufficient, or an external skill should become part of the normal CRA workflow, add a structured lesson to `../references/lessons-log.json` and update the relevant internal skill or routing documentation.
