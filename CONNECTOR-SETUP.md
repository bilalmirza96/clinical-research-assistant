# Research Connector Setup

This plugin uses cloud-based research connectors to search medical literature, clinical trials, and scientific databases. These connectors are provided by Claude.ai and need to be enabled once in your account.

## Required Connectors

| Connector | What It Does | Used By |
|---|---|---|
| **PubMed** | Search 36M+ biomedical research articles | `/literature-review`, `/write-introduction`, `/write-discussion`, `/write-manuscript` |
| **bioRxiv / medRxiv** | Search preprints (papers not yet peer-reviewed) | `/literature-review`, `/write-manuscript` |
| **Scholar Gateway** | Semantic search across academic papers | `/literature-review`, `/write-introduction`, `/write-discussion`, `/write-manuscript` |
| **Clinical Trials** | Search ClinicalTrials.gov (400K+ trials) | `/literature-review`, `/write-manuscript` |
| **BioRender** | Scientific icons and figure templates | `/visualize`, `/write-manuscript` |

## How to Enable Connectors

### Step 1: Go to Claude.ai Settings

1. Open [claude.ai](https://claude.ai) in your browser
2. Click your profile icon (bottom-left)
3. Go to **Settings** > **Connectors** (or go directly to [claude.ai/settings/connectors](https://claude.ai/settings/connectors))

### Step 2: Enable Each Connector

Turn on the following connectors (they're free):
- **PubMed**
- **bioRxiv**
- **Scholar Gateway**
- **Clinical Trials**
- **BioRender**

### Step 3: Use Claude Code with the Same Account

When you open Claude Code (the terminal app), make sure you're logged in with the same Claude.ai account. The connectors will automatically be available.

You can verify by typing `/mcp` in Claude Code — you should see all five connectors listed.

## What If I Skip This?

The plugin will still work, but with reduced capabilities:

- `/literature-review` won't be able to search PubMed or bioRxiv directly — you'd need to provide papers manually
- `/write-introduction` and `/write-discussion` won't be able to find additional references automatically
- `/visualize` won't have access to BioRender templates
- `/analyze` and `/write-methods-results` are unaffected — they only work with your local data files

## Troubleshooting

**Connectors not showing up in Claude Code?**
- Make sure you're logged into Claude Code with the same account as claude.ai
- Try restarting Claude Code after enabling connectors
- Run `/mcp` to check which connectors are active

**Getting "tool not available" errors?**
- The connector might not be enabled yet — check [claude.ai/settings/connectors](https://claude.ai/settings/connectors)
- Some connectors require accepting terms of service on first use
