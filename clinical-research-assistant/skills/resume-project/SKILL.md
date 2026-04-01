---
name: resume-project
description: Resume a Clinical Research Assistant project from persistent state files and identify the next required phase.
---

# Resume Project

<role>
You resume an existing clinical research project from its saved state files rather than from chat memory alone.
</role>

## Purpose
Load existing state, identify project completeness, and determine the next correct action.

## Files to inspect
- `project_state.json`
- `study_spec.json`
- `dataset_profile.json` if present
- `analysis_plan.json` if present
- `evidence_bank.json` if present
- `citation_bank.json` if present
- `results_registry.json` if present
- `figure_registry.json` if present
- `manuscript_state.json`
- `decision_log.md`

## Workflow
1. Read all existing state files.
2. Summarize project status by phase.
3. Identify blockers, missing artifacts, and deferred decisions.
4. Determine the next correct command.
5. Update `project_state.json` and `decision_log.md` with a resume event.

## Rules
- Prefer persisted state over memory of prior chat if they conflict.
- Be explicit about incomplete or inconsistent state.
- Do not skip ahead to manuscript drafting if evidence or results artifacts are missing.
