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
8. **Primary objective** — one sentence pre-specifying the primary contrast: population, exposure, primary outcome, time horizon, comparator. Locked at `/analyze` Phase 1.0 per L051.
9. **Secondary objectives** — numbered list; each entry pre-specifies its own outcome, exposure, time horizon, and comparator. Locked alongside the primary at `/analyze` Phase 1.0.
10. **Candidate covariates for adjustment** (list, or "to be determined during analysis"). These are CANDIDATES only; the final matching + adjustment variables are pre-specified, proposed with rationale, and PI-approved at `/analyze` HALT 2A — not at project init.
11. **Design features** (clustering? repeated measures? survival? competing risks?)
12. **Registry** (if applicable: NSQIP, NCDB, SEER, UNOS, NTDB, MBSAQIP, other)
13. **Target journal** (optional, can be set later)
14. **IRB status** (approved, pending, exempt, not needed)

Accept partial answers — fields can be populated later during `/analyze` or `/literature-review`. The primary + secondary objectives (questions 8–9) can be drafted now and finalized at `/analyze` Phase 1.0 with PI sign-off; the candidate covariates (question 10) are explicitly preliminary and get re-reviewed at HALT 2A.

### STEP 2: Create Project Directory

Create the following structure at the user's working location:

```
[project_name]/
├── project_state.json
├── study_spec.json
├── results_registry.json
├── figure_registry.json
├── manuscript_state.json
├── evidence_bank.json
├── citation_bank.json
├── decision_log.md
├── data/
│   └── working/                ← filtered cohort + filter logs land here (raw stays at canonical source)
├── specs/                      ← locked intake artifacts (populated by /analyze Phase 1, including objectives_locked.json + variables_locked.json per L051)
├── plans/                      ← analysis plan + revisions + critique audit (populated by /analyze Phase 2-3)
├── Protocol/                   ← PI-facing locked artifacts: objectives_locked_<date>.md + variables_locked_<date>.md + sap_amendments.md (populated by /analyze Phase 1.0 + HALT 2A per L051)
├── Reports/                    ← deliverables: MASTER_TABLES_<project>_<date>.xlsx (per L051) + MASTER_ANALYSIS_REGISTRY.json (per L045) + analysis_report_<slug>_<date>.md (populated by /analyze Phase 4-7)
│   └── Archives/               ← prior report versions on re-runs
├── analysis/                   ← scripts (replay_analysis.sh + intermediate code)
├── outputs/                    ← legacy generic outputs
└── figures/                    ← legacy generic figure outputs
```

Initialize each JSON file from the corresponding template in `templates/state/`. Copy `decision_log.template.md` as `decision_log.md`. Empty folders (`data/working`, `specs/`, `plans/`, `Protocol/`, `Reports/Archives`, `analysis/`) are created at this step so downstream skills have a place to write their artifacts. The `Protocol/` folder is the PI-facing artifact home — locked objectives (`objectives_locked_<date>.md`), locked variables (`variables_locked_<date>.md`), and any SAP §9-style amendments (`sap_amendments.md`) land here. The `Reports/` folder holds the Master Excel Workbook (per L051) and the JSON analysis registry (per L045) as coexisting source-of-truth artifacts.

**Data layer discipline (per data-analysis policy):** Raw source files are NOT copied into the project — they remain at their canonical location (registry export, institutional download). The `data/working/` directory is where filtered cohorts land. The `source_manifest.json` recording WHERE raw lives + sha256 at read time is created by `/analyze` Phase 1, not at project-init. See `../data-analysis/SKILL.md` "Data Provenance" section for the full discipline.

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
> "Project initialized. **Required next step: `/literature-review`** — this is now a Phase 0 prerequisite for `/analyze` per L048 (added 2026-05-24). `/analyze` will auto-invoke it if you skip and try to proceed, but running it deliberately first lets you scope without time pressure."
>
> Other next steps:
> - Upload your dataset to the `data/` directory
> - `/analyze` to begin statistical analysis (will auto-invoke `/literature-review` if Phase 0 artifacts missing)
> - `/resume-project` to return to this project in a future session

**Phase 0 prerequisite (per L048):** Before `/analyze` Phase 1 can fire, the project must contain `evidence_bank.json`, `citation_bank.json`, `novelty_assessment.json`, and `differentiation_brief.md` (all populated and PI-signed). These are produced by `/literature-review`. The CRA workflow now enforces this as a HARD GATE — `/analyze` will not lock specs or write the analysis plan without PI sign-off on the differentiation brief.

---

## CHANGELOG / Lessons Learned

### 2026-05-28 — L051 — Primary + secondary objectives at intake; Protocol/ folder

Added in tandem with the analyze/SKILL.md L051 refinement. Two changes here:

1. **STEP 1 questions updated** to capture the primary objective (question 8) and secondary objectives (question 9) as distinct fields, separate from the primary outcome (question 6) and primary exposure (question 7). The outcome is the variable; the objective is the contrast sentence. These get finalized + PI-signed at `/analyze` Phase 1.0 → `Protocol/objectives_locked_<date>.md`. Question 10 (candidate covariates) is now explicitly labeled as preliminary — the final matching + adjustment variables are pre-specified and PI-approved at `/analyze` HALT 2A, not here.

2. **STEP 2 directory tree** now includes a `Protocol/` folder for PI-facing locked artifacts (`objectives_locked_*.md`, `variables_locked_*.md`, `sap_amendments.md`) and notes that `Reports/` holds the L051 Master Excel Workbook alongside the L045 JSON registry.

See `internal/analyze/SKILL.md` CHANGELOG 2026-05-28 L051 entry for the full rationale and the companion edits in this release.
