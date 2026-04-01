---
name: project-init
description: Initialize a clinical research project, create the shared state files, and determine the correct starting phase.
argument-hint: "[research question or study idea]"
---

# Project Initialization

<role>
You initialize a new Clinical Research Assistant project and create the persistent state foundation required for resumable work.
</role>

## Purpose
Create the minimum valid project state for a new or newly formalized study.

## Required outputs
Create or overwrite as needed:
- `project_state.json`
- `study_spec.json`
- `manuscript_state.json`
- `decision_log.md`

## Workflow
1. Identify the project title or working title.
2. Capture the research question and study objective.
3. Capture the study design and data source if known.
4. Capture current project status:
   - idea only
   - literature underway
   - dataset available
   - analysis underway
   - writing underway
5. Determine the earliest correct next phase.
6. Create the minimum shared state files.
7. Summarize what is known, what is missing, and what command should be run next.

## Rules
- Do not fabricate missing details.
- Leave unknown fields null or empty.
- Prefer creating a clean skeleton over pretending the project is more complete than it is.
- If state files already exist, load them first and either update them or explain the conflict.

## Next-step guidance
Typical outputs should recommend one of:
- `/literature-review`
- `/analyze`
- `/resume-project`
