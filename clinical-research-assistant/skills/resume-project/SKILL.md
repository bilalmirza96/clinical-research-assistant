---
name: resume-project
description: Resume a previously initialized clinical research project by loading all state files and presenting current progress. Use when returning to an existing study.
---

# /resume-project — Resume Existing Project

Loads all shared-state files from an existing project and resumes work from the last checkpoint.

## Workflow

### STEP 1: Locate Project

Ask the user for the project directory path, or search the current working directory for `project_state.json`.

If no `project_state.json` is found, check for `manuscript_state.json` (legacy projects from before `/project-init` existed). If found, offer to create the missing state files.

### STEP 2: Load All State Files

Read and validate each file. Report status:

| File | Status | Key Info |
|---|---|---|
| `project_state.json` | Found / Missing | Current phase, status |
| `study_spec.json` | Found / Missing | Study design, outcome, exposure |
| `dataset_profile.json` | Found / Missing | Rows, columns, variables |
| `analysis_plan.json` | Found / Missing | Steps completed |
| `evidence_bank.json` | Found / Missing | Number of evidence entries |
| `citation_bank.json` | Found / Missing | Number of verified citations |
| `results_registry.json` | Found / Missing | Primary result summary |
| `figure_registry.json` | Found / Missing | Number of figures |
| `manuscript_state.json` | Found / Missing | Sections completed |
| `decision_log.md` | Found / Missing | Number of entries |

If critical files are missing or malformed, report which ones and offer to recreate them from templates.

### STEP 3: Present Status Summary

Show a compact project status:

```
Project: [name]
Status: [status]
Current phase: [phase]
Last updated: [timestamp]

Study: [design] — [outcome] in [population]
Data: [rows] rows, [columns] columns ([dataset status])
Analysis: [X/13 steps complete]
Evidence: [N entries], [M verified citations]
Results: [primary result summary or "not yet"]
Figures: [N figures] ([M approved])
Manuscript: [sections status]
```

### STEP 4: Recommend Next Action

Based on the current state:

| Current State | Suggested Action |
|---|---|
| No dataset loaded | Upload dataset, then `/analyze` |
| Dataset loaded, no analysis | `/analyze` |
| Analysis partially complete | `/analyze` (resumes from last step) |
| Analysis complete, no figures | `/visualize` |
| Analysis complete, no literature | `/literature-review` |
| Figures complete, no manuscript | `/write-manuscript` or individual section commands |
| Manuscript partially complete | The next incomplete section command |
| Manuscript complete | Final audit via `/write-manuscript` |

Also check:
- Is there a decision log entry flagging unresolved issues? Surface it.
- Has the evidence bank been populated? If not and manuscript writing is next, suggest `/literature-review` first.
- Are there analysis plan steps marked incomplete that should have been done? Flag them.

> Present the recommendation and ask: "Would you like to continue from here, or do something different?"

### STEP 5: Load Context for Next Command

When the user selects a next action, pre-load the relevant state into the conversation so the downstream command has full context without re-asking questions:

- For `/analyze`: load study_spec, dataset_profile, analysis_plan
- For `/visualize`: load results_registry, analysis_plan, figure_registry
- For `/literature-review`: load study_spec, evidence_bank
- For `/write-introduction`: load evidence_bank, citation_bank, study_spec
- For `/write-methods-results`: load results_registry, figure_registry, analysis_plan
- For `/write-discussion`: load results_registry, evidence_bank, citation_bank
- For `/write-manuscript`: load all state files
