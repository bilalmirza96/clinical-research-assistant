# Clinical Research Assistant — Plugin for Claude Code

An interactive clinical research assistant plugin that guides general surgery residents through the complete research pipeline — from literature review and question refinement, through statistical analysis and figure generation, to manuscript writing — step by step, with approval gates at every stage.

## Commands

| Command | Purpose |
|---|---|
| `/literature-review` | Deep literature search, gap analysis, novelty assessment, and strategic research question refinement |
| `/analyze` | Full statistical analysis pipeline: data intake → cleaning → univariate → multivariate → sensitivity analyses → formatted Excel file |
| `/visualize` | Publication-quality figures (forest plots, ROC curves, KM curves, violin plots, etc.) for high-impact journals |
| `/write-introduction` | Introduction section using a 4-paragraph funnel-down structure |
| `/write-methods-results` | Manuscript-ready Statistical Methods and Results sections in AMA style |
| `/write-discussion` | Discussion section using a 6-paragraph reverse-funnel pyramid structure |

## Quick Start

### 1. Install the plugin

```bash
/plugin marketplace add bilalmirza96/clinical-research-assistant
/plugin install clinical-research-assistant@clinical-research-assistant
```

### 2. Follow the recommended workflow

Run the commands in this order. Each one builds on the output of the previous step.

```
/literature-review  →  /analyze  →  /visualize  →  /write-introduction  →  /write-methods-results  →  /write-discussion
```

### 3. What to expect at each step

**`/literature-review`** — Start here. Tell Claude your research question and upload any background you have. Claude searches PubMed, bioRxiv, and scholarly databases, maps the existing evidence, identifies gaps, and helps you refine your question for maximum novelty. You approve or redirect at each stage.

**`/analyze`** — Upload your dataset (Excel or CSV). Claude walks you through data cleaning, baseline characteristics (Table 1), univariate screening, multivariate modeling, and sensitivity analyses. Every statistical decision is explained and requires your approval before proceeding. Output: a formatted Excel file with all tables.

**`/visualize`** — Claude proposes a figure set based on your analysis results. Choose from 20+ figure types including forest plots, ROC curves, Kaplan-Meier curves, violin + box + jitter plots, heatmaps, and more. Output: PDF (vector) and PNG (600 DPI) files ready for journal submission.

**`/write-introduction`** — Claude drafts your Introduction paragraph by paragraph using a funnel-down structure: (1) what is known, (2) what is unknown, (3) the gap, (4) what we did. Each paragraph is presented for your approval before moving to the next. References are numbered inline and listed at the end.

**`/write-methods-results`** — Claude writes your Statistical Methods section (tests used, software, significance threshold) and Results section in the exact order of your tables and figures. All output is in chat with table/figure callouts.

**`/write-discussion`** — Claude drafts your Discussion using a reverse-funnel pyramid: (1) key findings, (2) concordant literature, (3) discordant literature, (4) clinical implications, (5) strengths and limitations, (6) conclusion. Uses the Content-Context-Conclusion (3Cs) framework throughout.

### 4. Tips

- **You can run any command independently.** The workflow above is recommended but not required. For example, you can jump straight to `/analyze` if you already have a refined question.
- **Upload your data early.** When using `/analyze`, upload your Excel/CSV in the same message as the command.
- **Be specific about your study.** The more context you give (study design, population, outcomes, covariates), the better the output.
- **Approve or redirect.** Every command pauses at key decision points. Say "approved" to continue or give specific feedback to adjust.
- **All writing outputs appear in chat.** Copy what you need into your manuscript. References are numbered with a full list at the end of each section.

## Key Features

- **Literature-driven** — searches PubMed, bioRxiv, and scholarly databases to map existing evidence and identify gaps before you start
- **Strategic advising** — recommends how to refine or pivot your research question for maximum novelty and impact
- **Interactive workflow** — Claude stops after every step and waits for your approval before proceeding
- **No black-box analysis** — every decision is explained and logged
- **Publication-ready output** — Excel tables formatted with Times New Roman 12pt, centered, black borders
- **Journal-quality figures** — 600 DPI, colorblind-safe palettes, minimalist design, 20+ figure types
- **Structured manuscript writing** — Introduction (funnel-down), Methods/Results (table/figure order), Discussion (reverse-funnel pyramid)
- **Reproducible** — complete Python code bundle with fixed random seed
- **Methodologically rigorous** — flags EPV violations, immortal time bias, overadjustment, collider bias, and other common pitfalls

## Domain Expertise

This plugin has built-in knowledge across general surgery and its subspecialties:

- **General surgery**: acute care, SSI, anastomotic leak, Clavien-Dindo, 30-day/90-day outcomes
- **Surgical oncology**: colorectal, gastric, hepatobiliary, pancreatic, breast, esophageal, melanoma/sarcoma
- **Pancreatic surgery**: POPF (ISGPS B/C), DGE, PPH, drain amylase, pancreatic texture, duct diameter
- **Esophageal cancer**: TNM (AJCC 8th ed), Mandard TRG, anastomotic leak, MIE vs open, survival endpoints
- **Transplant surgery**: graft survival, rejection, immunosuppression, CMV/BK/EBV, DCD vs DBD, delayed graft function
- **Bariatric surgery**: sleeve vs bypass, %EWL/%TWL, diabetes remission, leak rate, MBSAQIP metrics
- **Minimally invasive surgery**: robotic vs laparoscopic vs open, learning curves, cost-effectiveness
- **Trauma/critical care**: damage control, resuscitation, TBI, ISS, GCS, ICU outcomes
- **Biomarker discovery**: cytokine panels, Youden index cutoffs, multiple testing correction, ROC analysis
- **Registry analyses**: NCDB, NSQIP, UNOS/OPTN, SEER, NTDB, MBSAQIP — including known limitations

## Installation

### Claude Code (Terminal)

```bash
/plugin marketplace add bilalmirza96/clinical-research-assistant
/plugin install clinical-research-assistant@clinical-research-assistant
```

### Local Development

```bash
git clone https://github.com/bilalmirza96/clinical-research-assistant.git
cd clinical-research-assistant
# Test with: claude --plugin-dir ./plugins/clinical-research-assistant
```

## Plugin Structure

```
clinical-research-assistant/
├── .claude-plugin/
│   └── marketplace.json                          # Marketplace catalog
├── plugins/
│   └── clinical-research-assistant/
│       ├── .claude-plugin/
│       │   └── plugin.json                       # Plugin metadata
│       ├── commands/
│       │   ├── literature-review.md              # /literature-review command
│       │   ├── analyze.md                        # /analyze command
│       │   ├── visualize.md                      # /visualize command
│       │   ├── write-introduction.md             # /write-introduction command
│       │   ├── write-methods-results.md          # /write-methods-results command
│       │   └── write-discussion.md               # /write-discussion command
│       └── skills/
│           └── data-analysis/
│               └── SKILL.md                      # Auto-triggered skill
└── README.md
```

## License

MIT License — use freely, modify as needed.

## Author

Bilal Mirza — General Surgery Resident
