# `figure_specs.json` Schema

JSON schema + example for the locked artifact produced by `/visualize` Phase 2 PLAN.

---

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FigureSpecs",
  "type": "object",
  "required": ["version", "generated_at", "target_journal", "figures"],
  "properties": {
    "version": {"type": "string", "description": "Schema version; current: 1.0"},
    "generated_at": {"type": "string", "format": "date-time"},
    "target_journal": {"type": "string"},
    "subspecialty": {"type": "string", "description": "From study_spec"},
    "figures": {
      "type": "array",
      "items": {"$ref": "#/definitions/figure"}
    }
  },
  "definitions": {
    "figure": {
      "type": "object",
      "required": [
        "figure_id", "manuscript_number", "title", "type",
        "delegation", "data_source", "dimensions",
        "annotations", "color_palette", "export_formats"
      ],
      "properties": {
        "figure_id": {"type": "string", "pattern": "^fig_[0-9]{3}$"},
        "manuscript_number": {"type": ["integer", "string"], "description": "1, 2, 'S1', 'S2' (supplementary)"},
        "title": {"type": "string", "description": "Descriptive title for caption"},
        "type": {
          "enum": [
            "kaplan-meier", "cumulative-incidence", "forest", "roc",
            "bar-beeswarm", "violin-box-jitter", "cleveland-dot",
            "heatmap", "line-ribbon", "scatter-fit", "histogram",
            "spline", "love-plot", "waterfall", "volcano",
            "multi-panel", "consort", "mechanism", "workflow",
            "custom"
          ]
        },
        "delegation": {
          "type": "string",
          "description": "K-Dense skill path or 'R-override'",
          "examples": [
            "scientific-skills:scientific-visualization",
            "scientific-skills:scikit-survival",
            "scientific-skills:scientific-schematics"
          ]
        },
        "backend_override": {"enum": ["Python", "R"], "default": "Python"},
        "data_source": {
          "type": "string",
          "description": "Pointer into results_registry.json (e.g., 'results_registry::M1::asa_class_IV::aOR')"
        },
        "dimensions": {
          "type": "object",
          "required": ["width_in", "height_in"],
          "properties": {
            "width_in": {"type": "number", "description": "Width in inches; single column 3.5, double 7"},
            "height_in": {"type": "number"},
            "journal_column": {"enum": ["single", "double", "full-page"]}
          }
        },
        "panels": {
          "type": "object",
          "description": "Multi-panel composition if applicable",
          "properties": {
            "rows": {"type": "integer", "minimum": 1},
            "cols": {"type": "integer", "minimum": 1},
            "labels": {"type": "array", "items": {"type": "string"}, "description": "Panel labels like ['A', 'B', 'C']"}
          }
        },
        "annotations": {
          "type": "object",
          "properties": {
            "p_value_format": {"enum": ["JAMA", "two-decimal", "scientific"], "default": "JAMA"},
            "show_ci": {"type": "boolean", "default": true},
            "comparator_label": {"type": "string", "description": "Reference category per L038"},
            "significance_threshold": {"type": "number", "default": 0.05},
            "reference_lines": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "axis": {"enum": ["x", "y"]},
                  "value": {"type": "number"},
                  "style": {"enum": ["solid", "dashed", "dotted"], "default": "dashed"},
                  "label": {"type": "string"}
                }
              }
            }
          }
        },
        "color_palette": {
          "type": "object",
          "properties": {
            "scheme": {"enum": ["cra-default", "okabe-ito", "viridis", "RdBu", "custom"]},
            "colors": {"type": "array", "items": {"type": "string"}, "description": "If scheme=custom; hex codes"},
            "colorblind_safe": {"type": "boolean", "default": true}
          }
        },
        "axis_labels": {
          "type": "object",
          "properties": {
            "x": {"type": "string"},
            "y": {"type": "string"},
            "x_units": {"type": "string"},
            "y_units": {"type": "string"}
          }
        },
        "legend": {
          "type": "object",
          "properties": {
            "show": {"type": "boolean", "default": true},
            "position": {"enum": ["inside", "below", "right", "none"], "default": "inside"},
            "title": {"type": "string"}
          }
        },
        "caption_draft": {
          "type": "string",
          "description": "One-paragraph caption stub for manuscript paste"
        },
        "export_formats": {
          "type": "array",
          "items": {"enum": ["PDF", "PNG", "TIFF", "SVG"]},
          "default": ["PDF", "PNG"]
        }
      }
    }
  }
}
```

---

## Example: NSQIP distal pancreatectomy CR-POPF study figures

```json
{
  "version": "1.0",
  "generated_at": "2026-05-20T22:54:00Z",
  "target_journal": "JAMA Surgery",
  "subspecialty": "surgical-oncology",
  "figures": [
    {
      "figure_id": "fig_001",
      "manuscript_number": 1,
      "title": "CONSORT-style cohort flow",
      "type": "consort",
      "delegation": "scientific-skills:scientific-schematics",
      "backend_override": "Python",
      "data_source": "data/working/filter_operations.json",
      "dimensions": {"width_in": 5.0, "height_in": 6.5, "journal_column": "single"},
      "annotations": {"p_value_format": "JAMA", "show_ci": false},
      "color_palette": {"scheme": "cra-default", "colorblind_safe": true},
      "caption_draft": "Cohort flow diagram. From an initial ACS-NSQIP Pancreas PUF cohort (N = 1,247,032 records, 2019–2022), inclusion (age ≥ 18, distal pancreatectomy CPT codes) and exclusion (null primary outcome, duplicates) filters yielded the final analytic cohort (N = 7,082).",
      "export_formats": ["PDF", "PNG"]
    },
    {
      "figure_id": "fig_002",
      "manuscript_number": 2,
      "title": "Forest plot of multivariable predictors of CR-POPF",
      "type": "forest",
      "delegation": "scientific-skills:scientific-visualization",
      "backend_override": "Python",
      "data_source": "results_registry::M1::all_covariates",
      "dimensions": {"width_in": 7.0, "height_in": 5.0, "journal_column": "double"},
      "annotations": {
        "p_value_format": "JAMA",
        "show_ci": true,
        "comparator_label": "ASA Class I-II (reference); Open approach (reference)",
        "reference_lines": [{"axis": "x", "value": 1.0, "style": "dashed", "label": "OR = 1"}]
      },
      "color_palette": {"scheme": "cra-default", "colors": ["#2C3E50"], "colorblind_safe": true},
      "axis_labels": {"x": "Adjusted Odds Ratio (95% CI)", "y": "Predictor"},
      "legend": {"show": false},
      "caption_draft": "Forest plot showing multivariable-adjusted odds ratios (aOR; 95% CI) for predictors of clinically relevant postoperative pancreatic fistula (CR-POPF; ISGPS Grade B/C) after distal pancreatectomy. Reference categories: ASA Class I–II; Open surgical approach. Dashed line at aOR = 1.0.",
      "export_formats": ["PDF", "PNG"]
    },
    {
      "figure_id": "fig_003",
      "manuscript_number": 3,
      "title": "Adjusted odds of 30-day outcomes by CR-POPF status",
      "type": "cleveland-dot",
      "delegation": "scientific-skills:scientific-visualization",
      "data_source": "results_registry::M2_thru_M9::all_outcomes",
      "dimensions": {"width_in": 7.0, "height_in": 4.5, "journal_column": "double"},
      "annotations": {
        "p_value_format": "JAMA",
        "show_ci": true,
        "comparator_label": "No CR-POPF (reference)"
      },
      "color_palette": {"scheme": "cra-default", "colorblind_safe": true},
      "caption_draft": "Adjusted odds ratios (95% CI) for 30-day postoperative outcomes comparing CR-POPF (ISGPS Grade B/C) versus no CR-POPF (reference). Outcomes include any morbidity, sepsis, unplanned reintubation, return to OR, readmission, and 30-day mortality.",
      "export_formats": ["PDF", "PNG"]
    }
  ]
}
```

---

## Versioning rule

When `figure_specs.json` is revised at HALT 1, the prior version is preserved as `figure_specs_v<n>.json` immediately before overwriting. Current file always at `figure_specs.json` (no version suffix). Matches the versioning rule from `/analyze` Concern #8.
