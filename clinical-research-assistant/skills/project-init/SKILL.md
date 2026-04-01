---
name: project-init
description: Initialize a new clinical research project with all state files, directory structure, and study specification. Use at the start of any new study.
---

# /project-init — Initialize Research Project

Creates the project directory, initializes all shared-state files, and populates them with the study specification. This is the entry point for any new research project.

## Workflow

### STEP 1: Gather Study Information

Ask the user for:
1. **Project name** (short identifier, used for directory name)
2. **Study aim** (1-2 sentences)
3. **Data source** (registry name, institutional dataset, prospective collection)
4. **Study design** (retrospective cohort, case-control, cross-sectional, RCT, etc.)
5. **Study period** (start and end dates or year range)
6. **Primary outcome** (name, type: binary/continuous/time-to-event, coding)
7. **Primary exposure** (name, type, reference group)
8. **Covariates for adjustment** (list, or "to be determined during analysis")
9. **Design features** (clustering? repeated measures? survival? competing risks?)
10. **Registry** (if applicable: NSQIP, NCDB, SEER, UNOS, NTDB, MBSAQIP, other)
11. **Target journal** (optional, can be set later)
12. **IRB status** (approved, pending, exempt, not needed)

Accept partial answers — fields can be populated later during `/analyze` or `/literature-review`.

### STEP 2: Create Project Directory

Create the following structure at the user's working location:

```
[project_name]/
├── project_state.json
├── study_spec.json
├── dataset_profile.json
├── analysis_plan.json
├── evidence_bank.json
├── citation_bank.json
├── results_registry.json
├── figure_registry.json
├── manuscript_state.json
├── decision_log.md
├── data/
├── outputs/
└── figures/
```

Initialize each JSON file from the corresponding template in `templates/state/`. Copy `decision_log.template.md` as `decision_log.md`.

### STEP 3: Populate State Files

Fill in from the user's answers:

**`project_state.json`:**
- `project_id`: generate from project name + date (e.g., `whipple_popf_20260401`)
- `project_name`: user's project name
- `created_at` / `updated_at`: current timestamp
- `status`: `"initialized"`
- `current_phase`: `"setup"`
- `research_question`: derived from study aim
- `target_journal`: if provided
- Set all `*_path` fields to point to the state files in this directory

**`study_spec.json`:**
- Populate all fields from user's answers
- Leave empty strings for fields not yet provided

**All other JSON files:** Initialize from templates with no data — they get populated by downstream commands.

**`decision_log.md`:** Add first entry:
```
### [DATE] — Setup
**Decision:** Project initialized with [study design] studying [outcome] in [population]
**Reason:** [study aim]
**Alternatives considered:** None (initial setup)
**Risks / unresolved issues:** [list any unknowns flagged by user]
```

### STEP 4: Confirm and Summarize

Present a compact summary:

```
Project: [name]
Location: [path]
Design: [study design]
Data source: [registry/dataset]
Outcome: [outcome name] ([type])
Exposure: [exposure name] ([type])
Journal: [target or "not set"]

State files: 10 initialized
Directories: data/, outputs/, figures/ created
```

Then:
> "Project initialized. Next steps:"
> - Upload your dataset to the `data/` directory
> - `/analyze` to begin statistical analysis
> - `/literature-review` for evidence synthesis
> - `/resume-project` to return to this project in a future session
