# Phase 0 Cleanup Audit

Status: **COMPLETE** (2026-04-01)

## What Was Wrong

### 1. Duplicate Command Ownership
- `skills/data-analysis/SKILL.md` (named "clinical-statistical-analyst") owned ALL commands: `/analyze`, `/visualize`, `/write-manuscript`, `/literature-review`, etc.
- `skills/analyze/SKILL.md` existed but contained the **visualize** skill content (wrong file)
- `skills/visualize/SKILL.md` had an older version of the visualize skill
- Result: ambiguous ownership, two competing "brains" for `/analyze`

### 2. No Shared State Layer
- No state templates existed
- No project initialization or resume workflow
- Each command operated statelessly

### 3. No Architecture Documentation
- No ownership map
- No clear delegation rules for BioMedAgent vs orchestrator
- No command contracts

## What Was Fixed

### A. `skills/data-analysis/SKILL.md` — Rewritten as Policy File
- **Before**: Full command owner named "clinical-statistical-analyst" with all command workflows
- **After**: Policy file named "clinical-analysis-policy" containing only methodological guardrails, diagnostics expectations, registry cautions, reporting rules, and observational language rules
- Does not own any command
- Referenced by command skills for shared standards

### B. `skills/analyze/SKILL.md` — Fixed and Made Canonical
- **Before**: Contained the visualize SKILL.md content (wrong file)
- **After**: Contains the canonical `/analyze` workflow with all 9 steps, checkpoints, and interaction rules
- References the policy file for methodological standards

### C. State Templates Created
All 5 templates created under `templates/state/`:
- `project_state.template.json` — overall project tracking
- `study_spec.template.json` — study design parameters
- `analysis_plan.template.json` — analysis progress tracking
- `manuscript_state.template.json` — manuscript progress tracking
- `decision_log.template.md` — methodological decision log

### D. New Skills Added
- `skills/project-init/SKILL.md` — initializes project with state files
- `skills/resume-project/SKILL.md` — resumes from last checkpoint

### E. Ownership Map Created
- `OWNERSHIP_MAP.md` at repo root
- Each command has exactly one canonical owner
- Policy files and support files clearly labeled as non-owners
- BioMedAgent delegation rules documented

## Remaining Ownership Issues — None

| Command | Owner | Verified |
|---|---|---|
| `/project-init` | `skills/project-init/SKILL.md` | Yes |
| `/resume-project` | `skills/resume-project/SKILL.md` | Yes |
| `/analyze` | `skills/analyze/SKILL.md` | Yes |
| `/visualize` | `skills/visualize/SKILL.md` | Yes |
| `/literature-review` | `skills/literature-review/SKILL.md` | Yes |
| `/write-manuscript` | `skills/write-manuscript/SKILL.md` | Yes |
| `/write-introduction` | `skills/write-introduction/SKILL.md` | Yes |
| `/write-methods-results` | `skills/write-methods-results/SKILL.md` | Yes |
| `/write-discussion` | `skills/write-discussion/SKILL.md` | Yes |

## Phase 1: Shared State Wiring (COMPLETE — 2026-04-01)

### What Was Done

**5 new state templates created:**
- `dataset_profile.template.json` — variable inventory, cleaning log, missing data summary
- `evidence_bank.template.json` — literature evidence entries with tags, gap analysis, novelty assessment
- `citation_bank.template.json` — verified citations with DOI/PMID, section tags, usage tracking
- `results_registry.template.json` — cohort flow, primary/secondary results, diagnostics, propensity analysis
- `figure_registry.template.json` — figure metadata, file paths, legends, approval status

**State management wired into all 9 command skills:**

| Skill | State Reads | State Writes |
|---|---|---|
| `/project-init` | — | All 10 state files (initialized from templates) |
| `/resume-project` | All 10 state files | — |
| `/analyze` | project_state, study_spec, analysis_plan | analysis_plan, dataset_profile, results_registry, project_state, decision_log |
| `/visualize` | results_registry, figure_registry, project_state | figure_registry, project_state |
| `/literature-review` | study_spec, evidence_bank, project_state | evidence_bank, citation_bank, project_state, decision_log |
| `/write-introduction` | evidence_bank, citation_bank, study_spec, manuscript_state | manuscript_state, citation_bank |
| `/write-methods-results` | results_registry, analysis_plan, figure_registry, study_spec, manuscript_state | manuscript_state |
| `/write-discussion` | results_registry, evidence_bank, citation_bank, manuscript_state | manuscript_state, citation_bank |
| `/write-manuscript` | All state files | manuscript_state, project_state |

**CLAUDE.md updated** with complete state flow diagram showing which commands read/write which files.

**Key design decisions:**
- All commands are backward compatible — they work standalone without state files
- State enables cross-session continuity and cross-command data flow
- `/write-methods-results` and `/write-discussion` enforce cross-verification against `results_registry.json` — every number in the manuscript must trace back to computed results
- `/write-introduction` and `/write-discussion` enforce verified citations from `citation_bank.json` — no citing from memory
- `/analyze` interaction style changed from micro-step to semi-autonomous (routine sub-steps bundled, only critical decisions need approval)

## Next Steps

Phase 2 candidates:
1. Reconcile the two versions of `visualize/SKILL.md` (the newer version with Wilke principles/color system should replace the older one)
2. Implement multi-agent critique panel (Methodologist, Skeptic Reviewer, Manuscript Editor) in `/analyze` and `/write-discussion`
3. Build evidence-bank population logic into `/literature-review` (structured extraction from search results → evidence_bank entries)
4. Add BioMedAgent delegation trigger logic to `/analyze` (detect when complexity exceeds standard biostatistics)
