# State Schema

This document defines the persistent project state used by Clinical Research Assistant v3.

The default assumption is that every project is resumable across sessions and that both manuscript outputs and machine-readable artifacts are first-class deliverables.

---

## Overview

Each project should maintain the following core files:

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

Optional artifacts may be added later, but these are the minimum architecture files.

---

## 1. `project_state.json`

The master routing and lifecycle file.

### Purpose
- identify current project status
- identify current phase
- identify data modality
- identify evidence, analysis, figure, and manuscript readiness
- identify whether BioMedAgent delegation was used

### Suggested schema

```json
{
  "project_id": "crc_YYYYMMDD_slug",
  "project_title": "",
  "created_at": "",
  "updated_at": "",
  "owner": "Bilal",
  "status": "active",
  "current_phase": "project_init",
  "data_modalities": ["clinical_tabular"],
  "target_output": "full_manuscript",
  "target_journal": null,
  "evidence_status": "not_started",
  "analysis_status": "not_started",
  "figure_status": "not_started",
  "writing_status": "not_started",
  "final_audit_status": "not_started",
  "delegation_history": [],
  "debate_history": [],
  "deliverables": []
}
```

### Status enums
- `not_started`
- `in_progress`
- `completed`
- `blocked`
- `skipped`

---

## 2. `study_spec.json`

The canonical study definition.

### Purpose
- hold all study-defining variables
- serve as the source for Methods drafting
- prevent drift in exposure/outcome/covariate definitions

### Suggested schema

```json
{
  "research_question": "",
  "study_objective": "",
  "hypothesis": "",
  "study_design": "",
  "data_source": "",
  "study_period": "",
  "population": "",
  "inclusion_criteria": [],
  "exclusion_criteria": [],
  "primary_outcome": {
    "name": "",
    "type": "",
    "coding": "",
    "time_origin": null,
    "event_definition": null
  },
  "secondary_outcomes": [],
  "primary_exposure": {
    "name": "",
    "type": "",
    "reference_group": null,
    "coding": ""
  },
  "covariates": [],
  "subgroups": [],
  "missing_data_strategy": null,
  "reporting_guideline": null,
  "target_journal": null,
  "house_style": "bilal_default"
}
```

### Core rule
This file must be updated whenever the study question, outcome definition, or covariate plan changes.

---

## 3. `dataset_profile.json`

The structured description of the actual data provided.

### Purpose
- describe file inventory and modality
- describe variable structure
- capture data quality findings before modeling
- support routing to native analysis vs BioMedAgent delegation

### Suggested schema

```json
{
  "dataset_name": "",
  "files": [
    {
      "file_name": "",
      "file_type": "csv",
      "modality": "clinical_tabular",
      "size_bytes": 0,
      "notes": ""
    }
  ],
  "row_count": null,
  "column_count": null,
  "candidate_id_columns": [],
  "candidate_time_columns": [],
  "candidate_outcome_columns": [],
  "candidate_exposure_columns": [],
  "variables": [
    {
      "name": "",
      "declared_type": null,
      "observed_type": "",
      "missing_percent": 0,
      "distinct_values": null,
      "range": null,
      "issues": []
    }
  ],
  "data_quality_flags": [],
  "requires_biomedagent": false,
  "delegation_reason": null
}
```

---

## 4. `analysis_plan.json`

The prospective analysis blueprint.

### Purpose
- define the primary analysis before execution
- force explicit model choice
- list diagnostics and sensitivity analyses
- support critique by the debate layer

### Suggested schema

```json
{
  "analysis_plan_version": 1,
  "analysis_archetype": "retrospective_cohort_binary_outcome",
  "primary_model": {
    "model_type": "logistic_regression",
    "justification": "",
    "effect_measure": "OR",
    "covariates": [],
    "reference_groups": {}
  },
  "secondary_models": [],
  "descriptive_plan": {
    "table_1_grouping": "",
    "continuous_summaries": "auto",
    "categorical_summaries": "n_percent",
    "smd_required": true
  },
  "missing_data_plan": {
    "strategy": "",
    "justification": ""
  },
  "diagnostics_plan": [],
  "sensitivity_analyses": [],
  "propensity_plan": null,
  "delegated_execution": {
    "use_biomedagent": false,
    "reason": null,
    "expected_return_objects": []
  },
  "debate_summary_id": null,
  "approved": false
}
```

### Core rule
No final modeling should begin until this file exists and is approved.

---

## 5. `evidence_bank.json`

The verified evidence store.

### Purpose
- record all candidate papers and guidance documents
- preserve structured literature synthesis
- support section-specific citation allocation

### Suggested schema

```json
{
  "query_history": [],
  "records": [
    {
      "record_id": "ev_001",
      "title": "",
      "authors": [],
      "year": 0,
      "source_type": "pubmed_article",
      "journal": "",
      "pmid": null,
      "doi": null,
      "guideline_body": null,
      "trial_id": null,
      "study_design": "",
      "population": "",
      "sample_size": null,
      "key_findings": [],
      "limitations": [],
      "relevance_tags": [],
      "section_tags": [],
      "verification_status": "verified",
      "notes": ""
    }
  ]
}
```

### Verification status enums
- `verified`
- `partially_verified`
- `unverified`
- `excluded`

### Core rule
Only verified or explicitly allowed partially verified records may feed the citation bank.

---

## 6. `citation_bank.json`

The only citations allowed for narrative prose.

### Purpose
- prevent ungrounded Introduction and Discussion drafting
- map verified sources to manuscript sections

### Suggested schema

```json
{
  "style": "AMA",
  "entries": [
    {
      "citation_id": "cit_001",
      "record_id": "ev_001",
      "formatted_citation": "",
      "section_permissions": ["introduction", "discussion"],
      "claim_scope": ["burden", "gap", "comparison_study"],
      "priority": "high"
    }
  ]
}
```

### Core rule
Introduction and Discussion may cite only from this file.

---

## 7. `results_registry.json`

The canonical results object store.

### Purpose
- hold every final numeric result used in tables, figures, and prose
- prevent manuscript-text drift from analytic outputs

### Suggested schema

```json
{
  "results": [
    {
      "result_id": "res_001",
      "analysis_label": "primary_adjusted_model",
      "result_type": "effect_estimate",
      "outcome": "",
      "exposure": "",
      "subgroup": null,
      "estimate_label": "adjusted OR",
      "estimate": 0,
      "ci_lower": 0,
      "ci_upper": 0,
      "p_value": null,
      "q_value": null,
      "n_analyzed": null,
      "table_id": "tbl_003",
      "source_model": "logistic_regression",
      "status": "final"
    }
  ],
  "tables": [
    {
      "table_id": "tbl_001",
      "title": "",
      "type": "table_1",
      "sheet_name": "",
      "status": "final"
    }
  ]
}
```

### Core rule
Results prose should pull from this file rather than from memory of prior chat text.

---

## 8. `figure_registry.json`

The canonical figure object store.

### Purpose
- maintain traceability from results to figures
- allow legends to be generated from structured figure metadata

### Suggested schema

```json
{
  "figures": [
    {
      "figure_id": "fig_001",
      "figure_number": "Figure 1",
      "title": "",
      "figure_type": "forest_plot",
      "source_result_ids": ["res_001", "res_002"],
      "status": "planned",
      "destination": "manuscript",
      "file_paths": {
        "pdf": null,
        "png": null
      },
      "legend_draft": "",
      "notes": ""
    }
  ]
}
```

### Status enums
- `planned`
- `in_progress`
- `generated`
- `approved`
- `supplementary_only`
- `dropped`

---

## 9. `manuscript_state.json`

The section-by-section manuscript tracker.

### Purpose
- track drafting status
- allow exact resumption
- support final assembly

### Suggested schema

```json
{
  "title": "",
  "sections": {
    "abstract": "not_started",
    "introduction": "not_started",
    "methods": "not_started",
    "results": "not_started",
    "discussion": "not_started",
    "references": "not_started",
    "tables": "not_started",
    "figures": "not_started",
    "final_audit": "not_started"
  },
  "word_counts": {},
  "last_completed_section": null,
  "final_outputs": []
}
```

---

## 10. `decision_log.md`

Human-readable project memory.

### Purpose
- record major decisions and why they were made
- preserve context for future resumptions
- make debate outcomes legible

### Example entries
- why Cox rather than logistic was selected
- why a variable was dropped for EPV concerns
- why BioMedAgent was invoked
- why a figure was moved to supplement
- why a citation was excluded from the final narrative

---

## Debate Summary Records

Debate outputs should be stored in `project_state.json` or a dedicated future file.
For now, the suggested structure is:

```json
{
  "debate_id": "deb_001",
  "phase": "analysis_plan",
  "agents": ["methodologist", "skeptic_reviewer", "manuscript_editor"],
  "recommended_action": "",
  "points_of_agreement": [],
  "key_disagreements": [],
  "decision_rationale": "",
  "unresolved_risks": []
}
```

---

## Delegation Return Contract

When BioMedAgent is used, its outputs must be written back into the shared state layer.
Minimum required return objects:

- updated `dataset_profile.json`
- updated `analysis_plan.json` or execution plan metadata
- machine-readable output summaries
- file paths to generated artifacts
- structured result objects that can be converted into `results_registry.json`
- execution notes for `decision_log.md`

BioMedAgent must not return only a prose narrative.

---

## Minimal Valid Project

A project is considered minimally initialized when these files exist:

- `project_state.json`
- `study_spec.json`
- `manuscript_state.json`
- `decision_log.md`

A project is considered manuscript-ready only when these also exist and are populated:

- `evidence_bank.json`
- `citation_bank.json`
- `analysis_plan.json`
- `results_registry.json`
- `figure_registry.json`

---

## File Ownership Rules

### Single source of truth
- study definition lives in `study_spec.json`
- evidence lives in `evidence_bank.json`
- allowed citations live in `citation_bank.json`
- model plan lives in `analysis_plan.json`
- numeric truth lives in `results_registry.json`
- figure truth lives in `figure_registry.json`

### Never duplicate canonical data in multiple files unless needed for export

---

## Implementation Priority

The first implementation pass should create and wire:

1. `project_state.json`
2. `study_spec.json`
3. `evidence_bank.json`
4. `citation_bank.json`
5. `analysis_plan.json`
6. `results_registry.json`
7. `figure_registry.json`
8. `manuscript_state.json`
9. `decision_log.md`

That is enough to support the v3 architecture without overengineering the initial rollout.
