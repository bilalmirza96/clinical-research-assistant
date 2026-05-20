# Intake Schemas

JSON schemas + examples for the four locked artifacts produced by `/analyze` Phase 1. Each schema is the contract between INTAKE and downstream phases.

---

## `dataset_spec.json`

### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DatasetSpec",
  "type": "object",
  "required": ["primary"],
  "properties": {
    "primary": {
      "type": "object",
      "required": ["name", "file_path", "version_hash", "n_total_raw", "inclusion_filters", "exclusion_filters"],
      "properties": {
        "name": {"type": "string", "description": "Human-readable dataset name"},
        "file_path": {"type": "string", "description": "Absolute or project-relative path"},
        "version_hash": {"type": "string", "description": "sha256 of source file at read-time"},
        "source_url": {"type": "string", "description": "Origin (registry portal URL, repo, etc.)"},
        "year_range": {"type": "array", "items": {"type": "integer"}},
        "license": {"type": "string", "description": "Use restrictions (e.g., NCDB DUA)"},
        "n_total_raw": {"type": "integer", "description": "Row count before any filtering"},
        "inclusion_filters": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["expr", "rationale"],
            "properties": {
              "expr": {"type": "string", "description": "Executable boolean expression"},
              "rationale": {"type": "string"}
            }
          }
        },
        "exclusion_filters": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["expr", "rationale"],
            "properties": {
              "expr": {"type": "string"},
              "rationale": {"type": "string"}
            }
          }
        }
      }
    },
    "merged": {
      "type": "array",
      "description": "Additional datasets joined to primary",
      "items": {
        "type": "object",
        "required": ["name", "file_path", "join_keys", "join_type"],
        "properties": {
          "name": {"type": "string"},
          "file_path": {"type": "string"},
          "version_hash": {"type": "string"},
          "join_keys": {"type": "array", "items": {"type": "string"}},
          "join_type": {"enum": ["inner", "left", "right", "outer"]}
        }
      }
    },
    "external_validation": {
      "type": "object",
      "description": "Independent dataset used for validation (if any)"
    }
  }
}
```

### Example (NSQIP distal pancreatectomy CR-POPF study)

```json
{
  "primary": {
    "name": "ACS-NSQIP Pancreas Participant User File",
    "file_path": "/path/to/canonical/nsqip_pancreas_2019_2022.csv",
    "version_hash": "sha256:abc123def456...",
    "source_url": "https://www.facs.org/quality-programs/data-and-registries/acs-nsqip/",
    "year_range": [2019, 2020, 2021, 2022],
    "license": "ACS-NSQIP DUA — N<11 cell suppression required for publication (per L007)",
    "n_total_raw": 1247032,
    "inclusion_filters": [
      {"expr": "age >= 18", "rationale": "adults only"},
      {"expr": "cpt_code in distal_panc_codes", "rationale": "study procedure"},
      {"expr": "year in [2019, 2020, 2021, 2022]", "rationale": "study window"}
    ],
    "exclusion_filters": [
      {"expr": "popf_grade.isna()", "rationale": "primary outcome required"},
      {"expr": "case_id.duplicated()", "rationale": "deduplicate"}
    ]
  }
}
```

---

## `variable_spec.json`

### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VariableSpec",
  "type": "object",
  "required": ["outcomes", "exposure", "covariates"],
  "properties": {
    "outcomes": {
      "type": "object",
      "required": ["primary"],
      "properties": {
        "primary": {"$ref": "#/definitions/variable"},
        "secondary": {"type": "array", "items": {"$ref": "#/definitions/variable"}}
      }
    },
    "exposure": {"$ref": "#/definitions/variable"},
    "covariates": {"type": "array", "items": {"$ref": "#/definitions/variable"}},
    "effect_modifiers": {"type": "array", "items": {"$ref": "#/definitions/variable"}},
    "subgroup_vars": {"type": "array", "items": {"$ref": "#/definitions/variable"}},
    "sensitivity_only_vars": {"type": "array", "items": {"$ref": "#/definitions/variable"}}
  },
  "definitions": {
    "variable": {
      "type": "object",
      "required": ["name", "label", "type", "source_columns", "derivation", "missing_handling"],
      "properties": {
        "name": {"type": "string", "description": "Snake_case identifier used in code"},
        "label": {"type": "string", "description": "Human-readable label for tables"},
        "type": {"enum": ["continuous", "binary", "categorical", "ordinal", "time-to-event"]},
        "source_columns": {"type": "array", "items": {"type": "string"}},
        "derivation": {"type": "string", "description": "Rule or expression to compute from source"},
        "missing_handling": {
          "enum": ["complete-case", "unknown-as-category", "multiple-imputation", "median-imputation", "exclude-from-analysis"]
        },
        "missing_threshold_pct": {"type": "number", "description": "Above this %, escalate to sensitivity analysis per L004"},
        "levels": {"type": "array", "description": "For categorical/ordinal"},
        "reference": {"type": "string", "description": "Reference category for categorical (per L038)"},
        "transform": {"enum": ["none", "log", "sqrt", "z-score", "categorize"]},
        "auto_collapsed_from": {"type": "string", "description": "If auto-collapsed by INTAKE per variable-collapse-defaults.md, original column name"}
      }
    }
  }
}
```

### Example (abbreviated)

```json
{
  "outcomes": {
    "primary": {
      "name": "popf_cr_grade_bc",
      "label": "Clinically Relevant POPF (ISGPS Grade B/C)",
      "type": "binary",
      "source_columns": ["POPF_GRADE"],
      "derivation": "POPF_GRADE in ['B', 'C']",
      "missing_handling": "complete-case",
      "missing_threshold_pct": 5
    },
    "secondary": [
      {"name": "any_morbidity", "label": "Any 30-day morbidity", "type": "binary", "source_columns": ["MORBIDITY_FLAG"], "derivation": "MORBIDITY_FLAG == 1", "missing_handling": "complete-case"}
    ]
  },
  "exposure": {
    "name": "asa_class",
    "label": "ASA Class",
    "type": "categorical",
    "source_columns": ["ASA_CLASS"],
    "derivation": "see variable-collapse-defaults.md",
    "missing_handling": "unknown-as-category",
    "levels": ["I-II", "III", "IV+"],
    "reference": "I-II",
    "auto_collapsed_from": "ASA_CLASS"
  },
  "covariates": [
    {"name": "age", "label": "Age, years", "type": "continuous", "source_columns": ["AGE"], "derivation": "AGE", "missing_handling": "median-imputation", "missing_threshold_pct": 5, "transform": "none"}
  ]
}
```

---

## `table_layouts.md`

Markdown skeletons for every manuscript table planned. Each skeleton uses `[auto]` as placeholders for cells that Phase 4/5 execution will populate.

### Template structure

```markdown
## Table 1 — <descriptive title>

| Column 1 (Variable)  | Column 2 (Overall) | Column 3 (Group A) | Column 4 (Group B) | Column 5 (P) | Column 6 (Test) |
|---|---|---|---|---|---|
| Variable A, mean (SD) | [auto] | [auto] | [auto] | [auto] | t-test |
| Variable B, n (%)     | [auto] | [auto] | [auto] | [auto] | chi-square |
| ... | ... | ... | ... | ... | ... |

**Footnote:** Continuous variables presented as mean (SD); categorical as n (%). Reference category for [exposure]: [reference level from variable_spec].

**Reference:** rows map to `variable_spec.json::covariates.<name>`. Cells populated from `results_registry.json::table1::<row>`.
```

### Minimum tables expected

- **Table 1** — Baseline characteristics (mapped to all `covariates` + `effect_modifiers`)
- **Table 2** — Univariate predictors of primary outcome
- **Table 3** — Multivariable model for primary outcome (the headline table)
- **Table 4** — Multivariable models for secondary outcomes (if planned)
- **Supplementary Table S1** — Complete-case vs imputed sensitivity (per L004)
- **Supplementary Table S2** — E-value sensitivity (per L005)
- **Supplementary Table S3** — Caliper-binding sensitivity (per L040) if PSM used
- **Supplementary Table SN** — DUA-compliant masked supplementary (per L007) if NCDB

---

## `figure_intent.md`

Each figure has an entry like:

```markdown
## Figure 1 — <descriptive title>

**Type:** Kaplan-Meier survival curve
**Shows:** Overall survival from index date, stratified by [exposure variable from variable_spec]
**Axes:** X = time (months); Y = survival probability (0-1)
**Strata:** levels of variable_spec.exposure
**Annotations:** at-risk table; log-rank P; HR (95% CI) inset
**Color scheme:** colorblind-safe (Okabe-Ito or viridis)
**Reference for results:** `results_registry::M{n}::km_curve_data`

**Design owner:** /visualize (this file declares intent only)
```

Minimum figures expected (varies by study type):

- **Figure 1** — Survival outcome (if time-to-event)
- **Figure 2** — Forest plot of multivariable model effect estimates
- **Figure 3** — ROC curve if discrimination is reported
- **Supplementary Figure S1** — PS balance Love plot if PSM used
- **Supplementary Figure S2** — Subgroup forest plot if subgroups pre-specified
