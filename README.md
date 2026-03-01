# Clinical Research Assistant — Plugin for Claude Code & Cowork

An interactive clinical research assistant plugin that guides surgical residents through rigorous, publication-ready statistical analysis, figure generation, and manuscript writing — step by step, with approval gates at every stage.

Built for **transplant surgery**, **pancreatic surgery**, **esophageal cancer**, and **biomarker discovery** research.

## Commands

| Command | Purpose |
|---|---|
| `/analyze` | Full statistical analysis pipeline: data intake → cleaning → univariate → multivariate → sensitivity analyses → formatted Excel file |
| `/visualize` | Publication-quality figures (forest plots, ROC curves, KM curves, etc.) for high-impact journals |
| `/write-methods-results` | Manuscript-ready Statistical Methods and Results sections in AMA style |

## Key Features

- **Interactive workflow** — Claude stops after every step and waits for your approval before proceeding
- **No black-box analysis** — every decision is explained and logged
- **Publication-ready output** — Excel tables formatted with Times New Roman 12pt, centered, black borders
- **Journal-quality figures** — 600 DPI, colorblind-safe palettes, minimalist design
- **Manuscript text** — Methods and Results written in the exact order of your tables and figures
- **Reproducible** — complete Python code bundle with fixed random seed
- **Domain-aware** — knows ISGPS POPF definitions, Clavien-Dindo, AJCC staging, NCDB limitations, and more
- **Methodologically rigorous** — flags EPV violations, immortal time bias, overadjustment, collider bias, and other common pitfalls

## Installation

### Claude Code (Terminal)

```bash
# Add this repository as a marketplace
/plugin marketplace add YOUR_GITHUB_USERNAME/clinical-research-assistant

# Install the plugin
/plugin install clinical-research-assistant@clinical-research-assistant
```

### Cowork (Desktop App)

1. Download or clone this repository
2. Zip the `clinical-research-assistant` folder
3. Open Claude Desktop → Cowork → Customize → Browse Plugins → Upload
4. Upload the zip file

### Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR_GITHUB_USERNAME/clinical-research-assistant.git

# Add as local marketplace in Claude Code
/plugin marketplace add /path/to/clinical-research-assistant
/plugin install clinical-research-assistant@clinical-research-assistant
```

## Plugin Structure

```
clinical-research-assistant/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── commands/
│   ├── analyze.md               # /analyze command
│   ├── visualize.md             # /visualize command
│   └── write-methods-results.md # /write-methods-results command
├── skills/
│   └── data-analysis/
│       └── SKILL.md             # Auto-triggered skill
└── README.md
```

## Workflow

```
/analyze  →  /visualize  →  /write-methods-results
   │              │                    │
   ▼              ▼                    ▼
 Excel file    PDF/PNG figures    Word document
 (all tables)  (all figures)     (Methods + Results)
```

1. **`/analyze`**: Upload your data and data dictionary. Claude walks you through cleaning, research question definition, univariate analysis, multivariate modeling, assumption checks, sensitivity analyses. Outputs a single Excel file with all manuscript and supplementary tables.

2. **`/visualize`**: Claude determines which figures are appropriate for your study, generates them one at a time with journal-quality aesthetics. Outputs PDF and PNG files.

3. **`/write-methods-results`**: Claude writes the Statistical Methods and Results sections following the exact order of your tables and figures. Also writes figure legends and a limitations paragraph. Outputs a formatted Word document.

## Domain Expertise

This plugin has built-in knowledge of:

- **Transplant surgery**: graft survival, rejection, immunosuppression, CMV/BK/EBV, IVIG, DCD vs DBD, delayed graft function
- **Pancreatic surgery**: POPF (ISGPS B/C), DGE, PPH, Clavien-Dindo, drain amylase, pancreatic texture, duct diameter, cytokine biomarkers
- **Esophageal cancer**: TNM (AJCC 8th ed), Mandard TRG, anastomotic leak, conduit choice, MIE vs open, lymph node yield, OS/DFS/DSS
- **Biomarker discovery**: cytokine panels, Youden index cutoffs, multiple testing correction (Bonferroni, FDR), sensitivity/specificity/PPV/NPV
- **Registry analyses**: NCDB, UNOS/OPTN, NSQIP — including known limitations and facility clustering

## License

MIT License — use freely, modify as needed.

## Author

Bilal Mirza — Transplant Surgery Resident
