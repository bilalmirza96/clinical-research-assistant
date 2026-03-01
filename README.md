# Clinical Research Assistant — Plugin for Claude Code & Cowork

An interactive clinical research assistant plugin that guides general surgery residents through deep literature review, rigorous publication-ready statistical analysis, figure generation, and manuscript writing — step by step, with approval gates at every stage.

Built for **general surgery** and all subspecialties: surgical oncology, transplant, bariatric, minimally invasive surgery, trauma/critical care, and more.

## Commands

| Command | Purpose |
|---|---|
| `/literature-review` | Deep PubMed/bioRxiv search, evidence synthesis, gap analysis, novelty assessment, and research question refinement |
| `/analyze` | Full statistical analysis pipeline: data intake → cleaning → univariate → multivariate → sensitivity analyses → formatted Excel file |
| `/visualize` | Publication-quality figures (forest plots, ROC curves, KM curves, etc.) for high-impact journals |
| `/write-methods-results` | Manuscript-ready Statistical Methods and Results sections in AMA style |

## Key Features

- **Interactive workflow** — Claude stops after every step and waits for your approval before proceeding
- **No black-box analysis** — every decision is explained and logged
- **Literature-powered** — deep PubMed/bioRxiv search with evidence tables, gap analysis, and novelty assessment
- **Publication-ready output** — Excel tables formatted with Times New Roman 12pt, centered, black borders
- **Journal-quality figures** — 600 DPI, colorblind-safe palettes, minimalist design
- **Manuscript text** — Methods and Results written in the exact order of your tables and figures
- **Reproducible** — complete Python code bundle with fixed random seed
- **Domain-aware** — covers all general surgery subspecialties, registries (NCDB, NSQIP, SEER, UNOS, NTDB, MBSAQIP), and clinical definitions
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
│   └── marketplace.json                          # Marketplace metadata
├── plugins/
│   └── clinical-research-assistant/
│       ├── .claude-plugin/
│       │   └── plugin.json                       # Plugin metadata
│       ├── commands/
│       │   ├── literature-review.md              # /literature-review command
│       │   ├── analyze.md                        # /analyze command
│       │   ├── visualize.md                      # /visualize command
│       │   └── write-methods-results.md          # /write-methods-results command
│       ├── skills/
│       │   └── data-analysis/
│       │       └── SKILL.md                      # Auto-triggered skill
│       └── README.md
└── README.md
```

## Workflow

```
/literature-review  →  /analyze  →  /visualize  →  /write-methods-results
        │                  │              │                    │
        ▼                  ▼              ▼                    ▼
  Research question    Excel file    PDF/PNG figures    Word document
  + evidence table    (all tables)   (all figures)     (Methods + Results)
```

1. **`/literature-review`**: Describe your research interest. Claude searches PubMed and bioRxiv, builds evidence summary tables, synthesizes current knowledge, identifies gaps, assesses novelty, and recommends 2–3 refined research questions ranked by impact and feasibility. Deep dives on your chosen question with 20–30 papers, provides methodological recommendations, drafts an Introduction skeleton, and alerts to competing preprints.

2. **`/analyze`**: Upload your data and data dictionary. Claude walks you through cleaning, research question definition, univariate analysis, multivariate modeling, assumption checks, sensitivity analyses. Outputs a single Excel file with all manuscript and supplementary tables.

3. **`/visualize`**: Claude determines which figures are appropriate for your study, generates them one at a time with journal-quality aesthetics. Outputs PDF and PNG files.

4. **`/write-methods-results`**: Claude writes the Statistical Methods and Results sections following the exact order of your tables and figures. Also writes figure legends and a limitations paragraph. Outputs a formatted Word document.

## Domain Expertise

This plugin has built-in knowledge of:

- **General surgery (acute care)**: SSI, anastomotic leak, Clavien-Dindo classification, emergency general surgery outcomes
- **Surgical oncology**: colorectal (TME, lymph node harvest, sidedness), gastric (D2, FLOT), hepatobiliary (ALPPS, PVE, HCC staging), breast (margins, sentinel node, genomic assays), melanoma/sarcoma
- **Bariatric surgery**: sleeve, bypass, %EWL/%TWL, MBSAQIP metrics, comorbidity resolution, weight regain
- **Minimally invasive surgery**: robotic vs lap vs open, learning curves (CUSUM), conversion rates, cost-effectiveness
- **Trauma & critical care**: damage control, TBI, ISS, GCS, TRISS, massive transfusion, REBOA
- **Transplant surgery**: graft survival, rejection, immunosuppression, CMV/BK/EBV, IVIG, DCD vs DBD, delayed graft function
- **Pancreatic surgery**: POPF (ISGPS B/C), DGE, PPH, Clavien-Dindo, drain amylase, pancreatic texture, duct diameter, cytokine biomarkers
- **Esophageal cancer**: TNM (AJCC 8th ed), Mandard TRG, CROSS vs FLOT, MIE vs open, anastomotic leak, OS/DFS/DSS
- **Biomarker discovery**: cytokine panels, liquid biopsy, ctDNA, Youden index cutoffs, multiple testing correction, sensitivity/specificity/PPV/NPV
- **Registry analyses**: NCDB, NSQIP, SEER, UNOS/OPTN, NTDB, MBSAQIP — including known limitations and facility clustering
- **Advanced methods**: survival analysis (KM, Cox, competing risks, landmark, RMST), propensity scores (matching, IPTW, doubly robust), causal inference

## License

MIT License — use freely, modify as needed.

## Author

Bilal Mirza — General Surgery Resident
