# Figure Type → K-Dense Skill Mapping

Used by `/visualize` Phase 2 PLAN to populate the `delegation` field in `figure_specs.json`. K-Dense Python is the default backend; R is an override available via `r-templates.md`.

---

## Primary skills (handle ~95% of cases)

| K-Dense skill | Purpose |
|---|---|
| `scientific-skills:scientific-visualization` | All standard publication figures (bar, box, violin, scatter, forest, ROC, heatmap, line+ribbon, multi-panel). Encodes journal-specific dimensions, colorblind palettes, export formats. |
| `scientific-skills:scientific-schematics` | Diagrams (CONSORT flow, mechanism, workflow). Not chart-like. Uses graphviz / matplotlib annotations / similar. |

## Specialized skills (for specific plot families)

| K-Dense skill | When |
|---|---|
| `scientific-skills:scikit-survival` | Kaplan-Meier curves, cumulative incidence plots, RMST visualizations (Python equivalent of survminer/tidycmprsk) |
| `scientific-skills:plotly` | Interactive plots (rare in manuscripts; useful for supplementary HTML) |
| `scientific-skills:seaborn` | Statistical plots with rich grouping (rare — usually covered by scientific-visualization) |
| `scientific-skills:matplotlib` | Custom plots that need fine-grained control |

---

## Mapping by figure type

| Figure type | Default delegation | Notes |
|---|---|---|
| **Forest plot** | `scientific-visualization` | matplotlib custom; CIs via `errorbar`; log-scale x-axis |
| **ROC curve** | `scientific-visualization` | uses `sklearn.metrics.roc_curve`; diagonal reference line |
| **Kaplan-Meier curve** | `scikit-survival` (data) + `scientific-visualization` (style) | include at-risk table below; log-rank P in inset |
| **Cumulative incidence (competing risks)** | `scikit-survival` (Fine-Gray) + `scientific-visualization` | stacked curves with shaded CI bands |
| **Bar + jitter (group comparison)** | `scientific-visualization` | matplotlib + seaborn; mean ± SEM bars with overlaid jittered points |
| **Violin + box + jitter** | `scientific-visualization` | seaborn violinplot + stripplot composite |
| **Cleveland dot plot** | `scientific-visualization` | matplotlib; horizontal points with error bars |
| **Heatmap** | `scientific-visualization` | seaborn heatmap with viridis or RdBu colormap |
| **Grouped/stacked bar** | `scientific-visualization` | matplotlib |
| **Line + ribbon (trend with CI)** | `scientific-visualization` | matplotlib `fill_between` for CI ribbon |
| **Histogram / density** | `scientific-visualization` | matplotlib + seaborn |
| **Scatter + fit line** | `scientific-visualization` | matplotlib with regression overlay |
| **Paired / slope chart** | `scientific-visualization` | matplotlib custom |
| **Spline plot (RCS)** | `scientific-visualization` | matplotlib; predicted values with ribbon |
| **Love plot (PSM balance)** | `scientific-visualization` | matplotlib horizontal dot plot; SMD threshold line at 0.1 |
| **Waterfall / tornado** | `scientific-visualization` | matplotlib ordered bars |
| **Volcano plot** | `scientific-visualization` | matplotlib; three-category color scheme |
| **Multi-panel composite** | `scientific-visualization` (uses `gridspec`) | preserve consistent color mapping across panels |
| **CONSORT flow diagram** | `scientific-schematics` | not a chart — uses graphviz or matplotlib annotations |
| **Mechanism / pathway diagram** | `scientific-schematics` | as above |
| **Workflow diagram** | `scientific-schematics` | as above |
| **Interactive exploratory** | `plotly` | only for supplementary HTML; rare in manuscripts |

---

## R override (when user explicitly requests R)

For each figure type above, an equivalent R approach exists. Use `references/r-templates.md` for code patterns. The aesthetic standards apply identically.

Common R override scenarios:
- User has pre-existing R analysis code and wants a consistent stack
- Specialized R package (e.g., `survminer`, `forestploter`, `rms` for splines) produces a better result than Python equivalent
- Journal explicitly requests R figures

When using R override:
1. Document the override in `figure_specs.json::backend_override: "R"`
2. Note in the figure caption draft that the figure was rendered in R + ggplot2/tidyplots
3. Save the R script alongside the figure file for reproducibility

---

## Delegation pattern at runtime

```
For each figure in figure_specs.json:
  1. Load the named K-Dense skill's SKILL.md as expert reference
  2. Read data from results_registry per figure_specs.data_source
  3. Apply aesthetic-standards.md visual rules
  4. Write Python (or R if override) code following K-Dense patterns
  5. Render PDF + PNG (600 DPI)
  6. Register output in figure_registry.json with sha256 + code_path
```

The K-Dense skill is treated as expert reference, NOT as a separate invocation. Reading its SKILL.md before writing code is what makes the generation reliable — same pattern as write-* skills reading writing-style.md.

---

## Fallback chain

If a figure type isn't covered above OR the default delegation fails:

1. Try `scientific-visualization` with matplotlib fallback
2. Try `seaborn` for statistical plot variants
3. Try `matplotlib` directly for full custom
4. Try R override per `r-templates.md`
5. Escalate to BioMedAgent for non-tabular biomedical visualization (rare for clinical work)

---

## Updating this mapping

When K-Dense adds a new visualization skill, update this matrix in a follow-up commit. The skill registry auto-indexes new K-Dense skills (`tools/update_skill_registry.py`).
