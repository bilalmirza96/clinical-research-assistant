# Figure Aesthetic Standards — Non-Negotiable

Read at PREREQUISITE by `/visualize`. These standards layer on top of whatever K-Dense skill is delegated for execution. When CRA standards conflict with K-Dense defaults, CRA wins (these encode accumulated journal-specific preferences).

---

## General style

- Clean, minimalist design — no chartjunk, no unnecessary gridlines, no 3D effects
- White background only
- Font: Arial or Helvetica throughout (standard for medical journals)
- High resolution: 300 DPI minimum, 600 DPI preferred
- Consistent color palette across all figures in the manuscript

## Typography

- Consistent font hierarchy:
  - Title: 12pt bold
  - Axis labels: 10–12pt
  - Tick labels: 9–10pt
  - Annotations: 9pt
- Direct labeling preferred over legends when possible
- Avoid rotated text — use horizontal orientation or abbreviate
- Annotation text in the same font family as the rest of the figure

## Color palette

Primary palette (colorblind-safe, muted, journal-appropriate):

| Color | Hex | Use |
|---|---|---|
| Navy | `#2C3E50` | Default primary group; "treated" / "exposed" |
| Muted red | `#C0392B` | Default secondary group; "control" / "unexposed" |
| Steel blue | `#2980B9` | Tertiary |
| Forest green | `#27AE60` | Quaternary |
| Warm gray | `#7F8C8D` | Reference lines, low-emphasis elements |

**For two-group comparisons:** navy vs muted red.

**Never use** rainbow palettes, neon colors, default ggplot2 colors, or red+green (colorblind hazard).

## Color usage rules

- Maximum 6–7 colors in a single figure
- **Sequential data:** single-hue gradient (light to dark blue) — e.g., viridis
- **Diverging data:** two-hue gradient through white (blue-white-red, or RdBu)
- **Categorical data:** qualitative palette with maximum contrast — Okabe-Ito recommended
- Always provide colorblind-safe alternatives
- Test every figure in grayscale — must remain interpretable in print

In tidyplots (when using R override):
```r
adjust_colors(new_colors = c("#2C3E50", "#C0392B", "#2980B9", "#27AE60", "#7F8C8D"))
```

In matplotlib/seaborn (K-Dense default):
```python
# Use Okabe-Ito or the CRA palette
sns.set_palette(['#2C3E50', '#C0392B', '#2980B9', '#27AE60', '#7F8C8D'])
```

## Data-ink ratio

- Maximize data-ink ratio — remove all non-essential visual elements
- No background gridlines unless they aid reading
- Remove top and right spines (open plot style) — every figure
- Never use 3D effects, drop shadows, gradient fills, or beveled edges

Matplotlib equivalent: `sns.despine(top=True, right=True)` or remove spines manually.
R tidyplots equivalent: `theme_tidyplot()` or `theme_minimal_xy()`.

## Axis and labels

- Axis labels must include units in parentheses (e.g., `"IL-6 (pg/mL)"`)
- Y-axis should start at 0 for bar charts (unless scientifically justified otherwise)
- Tick marks facing outward
- No axis titles that just repeat the variable name — make them descriptive

## Legends

- Inside the plot area when space permits, otherwise below
- No box border around legend
- Concise labels
- Prefer direct labeling over legends when fewer than 4 groups

## Statistical annotations

- P-values: bracket annotations with **exact p-values** (e.g., `p = 0.003`), **not stars** (per L013)
- Non-significant comparisons: show `p = 0.42` or `NS` — never omit
- Confidence intervals: shown as error bars or shaded bands
- P-value format follows JAMA convention (per L013):
  - Two decimals if ≥ 0.01 (e.g., `p = 0.56`)
  - Three decimals if `0.001 ≤ p < 0.01` (e.g., `p = 0.003`)
  - `p < 0.001` if smaller
  - Never `p = 0.000`

## Comparator declaration (per L038)

Every grouped or stratified figure must declare its reference category in the caption. Example caption stub:

> *"Adjusted odds ratios for clinically relevant POPF. Reference category: ASA Class I-II. Whiskers represent 95% confidence intervals; vertical dashed line at OR = 1.0."*

## Annotation best practices

- Text annotations highlight key findings directly on the figure
- Reference lines (horizontal/vertical dashed) for clinical thresholds (e.g., OR = 1, ROC diagonal)
- Bracket annotations for group comparisons with exact P-values
- Annotation boxes: thin border, white fill, slight transparency — never obscure data

## Multi-panel layout

- Python (default): `matplotlib.gridspec` or `seaborn.FacetGrid` for composition
- R (override): `patchwork` package
- Shared axes when comparing the same variable across panels
- Consistent color mapping across all panels
- Panel labels: A, B, C (bold, upper-left corner of each panel)
- Equal spacing between panels

## Dimensions (journal-specific)

| Journal type | Single column | Double column | Reference |
|---|---|---|---|
| Default (clinical) | 3.5 × 2.5 in | 7 × 5 in | Most medical journals |
| Nature | 89 mm wide | 183 mm wide | Strict spec |
| Science | 55 mm wide | 175 mm wide | Strict spec |
| Cell | 85 mm wide | 178 mm wide | Strict spec |
| JAMA Surgery / Annals of Surgery | 3.5 in | 7 in | Standard |

For specific journal style guides, see `scientific-skills:scientific-visualization` which encodes journal-specific dimensions.

## Output formats

- **Primary: PDF** (vector) — required for journal submission
- **Secondary: PNG** at 600 DPI — for review and presentation
- **TIFF** at 600 DPI with LZW compression — only when journal explicitly requires it
- Never JPEG for scientific figures (compression artifacts)

## Formatting for embedded documents (per L042)

When figures are embedded in Word manuscripts (rather than journal upload), the surrounding text formatting:
- Georgia 12pt, 1.5 line spacing, black text (RGB 0,0,0)

Figure captions in the manuscript body inherit this formatting.

## Anti-patterns to reject

| Anti-pattern | Fix |
|---|---|
| Default ggplot2 / matplotlib rainbow colors | Use CRA palette or Okabe-Ito |
| Stars (`*`, `**`, `***`) for P-values | Use exact P-values per L013 |
| Stratified figure without reference category in caption | Add reference declaration per L038 |
| 3D bar chart | Use 2D bar with clear axes |
| Pie chart with > 5 slices | Use horizontal bar instead |
| Truncated y-axis on a bar chart | Start at 0 unless scientifically justified |
| Red + green for two groups | Use navy + muted red (colorblind-safe) |
| Y-axis label "Value" or "Count" | Descriptive: "IL-6 concentration (pg/mL)" |
