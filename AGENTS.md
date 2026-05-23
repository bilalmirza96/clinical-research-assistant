# CRA — Operating Brief for Codex (AGENTS.md)

> This file is the Codex-equivalent of `CLAUDE.md` for the Clinical Research Assistant (CRA).
> Codex reads every `AGENTS.md` from repo root down to the working directory at session start —
> this one is the authoritative routing brief for any clinical-research work performed against
> this repo or against Bilal Mirza's workspace.
>
> **Counterpart files:**
> - Claude Code reads `CLAUDE.md` (this repo's root) + `~/.claude/CLAUDE.md` (global)
> - Cowork reads `~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/CLAUDE.md`
> - **Codex reads THIS file** + `~/Claude/AGENTS.md` (if present) + any nested `AGENTS.md` files
>
> The substantive operating rules are the same across all three agents. Only the invocation
> mechanism differs — see "Skill Invocation Differences" below.

---

## 1. Identity & Context

You are working with **Bilal Mirza**, PGY-1 General Surgery resident at the University of
Arizona. Research focus: thoracic surgical oncology (esophageal, lung) and translational
immuno-oncology (HNSCC, single-cell transcriptomics). Email: `bilalmirza96@outlook.com`.

Standing identity, mentors, working style, and active projects live in three context files:
- `~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/00_Context/about-me.md`
- `~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/00_Context/active-projects.md`
- `~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/00_Context/working-rules.md`

**Read all three at the start of every session before doing anything else.** They are
prerequisite context, not optional reading. The same files are the session-start ritual for
Claude Code and Cowork — Codex must follow it too.

---

## 2. Session-Start Ritual

Before the first substantive action, in this order:

1. **Read context files** (paths above): `about-me.md`, `active-projects.md`, `working-rules.md`.
2. **If the task is a clinical-research project initiation**, additionally read
   `00_Context/clinical-research-playbook.md` (Phase 0–8 workflow with Standing Rules A and B).
3. **If working in a specific project**, check for and read that project's `CLAUDE.md`
   (Codex will also pick up any `AGENTS.md` files there automatically).
4. **Confirm the task** before executing anything. Brainstorm and present options first.

---

## 3. Path Conventions (CRITICAL)

There are **two `Claude`-named folders** on this Mac. They are NOT interchangeable:

| Path | Purpose | What lives here |
|------|---------|-----------------|
| `~/Claude/` (local filesystem) | "Hot" workspace — git repos, plugin dev, sandbox | CRA repo (`~/Claude/dev/clinical-research-assistant/`), claude-scientific-skills, engineering scratch |
| `~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/` (iCloud) | "Cool" workspace — deliverables, manuscripts, clinical projects | All clinical/translational research projects, manuscripts, grants, session logs |

**Routing rule:**
- Clinical / translational research / manuscripts / grants → **iCloud `Claude_Projects/`**
- Plugin dev, engineering scratch, sandbox → **local `~/Claude/`**

**Hard prohibitions:**
- ❌ Never clone or place a git repo inside iCloud. iCloud Drive evicts files to save space
  and corrupts `.git/index` and refs. Use GitHub as the portable mirror.
- ❌ Never edit the installed Claude Code plugin copy at `~/.claude/plugins/clinical-research-assistant/`
  directly. Always edit the source at `~/Claude/dev/clinical-research-assistant/`.
- ❌ Never modify raw data in place. Write derived files to `processed/`, `reports/`,
  `analyses/`, `outputs/`, or `archives/`.

---

## 4. Skill Invocation Differences (Claude Code vs Codex)

| | Claude Code / Cowork | Codex |
|---|---|---|
| Skill discovery | `Skill` tool + frontmatter auto-loading | Manual: `Read` the SKILL.md by absolute path |
| Invocation | Slash command (e.g. `/analyze`) | Natural-language trigger + read the SKILL.md |
| MCP servers | Configured in `.claude-plugin/plugin.json` | Configured in `~/.codex/config.toml` |
| K-Dense runtime delegation | SKILL.md `Read`s another SKILL.md at runtime | Same pattern works — `Read` the delegated SKILL.md |
| Tool gating | `ToolSearch` deferred-tool system | All tools available; no deferral mechanism |

**Practical implication for Codex:** there are no slash commands. When the user says
"do a literature review on X" or "QC this manuscript", you must:
1. Recognize the trigger phrase (see table in §5).
2. `Read` the corresponding SKILL.md from the absolute path listed.
3. Follow the workflow in that SKILL.md as if it were a prompt.
4. If the SKILL.md instructs you to delegate to a K-Dense skill, `Read` THAT SKILL.md too
   (see §6).

---

## 5. Skill Routing — Natural-Language Triggers → SKILL.md Paths

All paths are absolute on Bilal's Mac. CRA lives at
`/Users/muhammadbilalmirza/Claude/dev/clinical-research-assistant/`.

### Internal CRA skills (12)

| Trigger phrases | SKILL.md to `Read` |
|---|---|
| "use CRA", "start the clinical research assistant", "invoke the CRA router" | `clinical-research-assistant/skills/clinical-research-assistant/SKILL.md` |
| "analyze this dataset", "run statistical analysis", "do the biostats", "what does this data show" | `clinical-research-assistant/skills/internal/analyze/SKILL.md` |
| "make a figure", "visualize this", "generate Figure N", "create a Kaplan-Meier plot" | `clinical-research-assistant/skills/internal/visualize/SKILL.md` |
| "do a literature review", "systematic search for", "find papers on", "PubMed search" | `clinical-research-assistant/skills/internal/literature-review/SKILL.md` |
| "write the introduction", "draft the intro" | `clinical-research-assistant/skills/internal/write-introduction/SKILL.md` |
| "write methods", "write results", "draft methods and results" | `clinical-research-assistant/skills/internal/write-methods-results/SKILL.md` |
| "write the discussion", "draft the discussion" | `clinical-research-assistant/skills/internal/write-discussion/SKILL.md` |
| "write an abstract", "draft abstract for [journal]" | `clinical-research-assistant/skills/internal/write-abstract/SKILL.md` |
| "write the full manuscript", "assemble the manuscript" | `clinical-research-assistant/skills/internal/write-manuscript/SKILL.md` |
| "QC the manuscript", "pre-submission rigor check", "run manuscript-qc" | `clinical-research-assistant/skills/internal/manuscript-qc/SKILL.md` |
| "start a new project", "scaffold a clinical research project" | `clinical-research-assistant/skills/internal/project-init/SKILL.md` |
| "resume project X", "pick up where we left off" | `clinical-research-assistant/skills/internal/resume-project/SKILL.md` |
| (policy-only — no command) | `clinical-research-assistant/skills/internal/data-analysis/SKILL.md` |

### Reference documents (read on demand, not workflows)

| Reference | Path |
|---|---|
| K-Dense delegation contracts | `clinical-research-assistant/skills/references/kdense-delegations.md` |
| Lessons log (47 entries, machine-readable) | `clinical-research-assistant/skills/references/lessons-log.json` |
| Command contracts | `clinical-research-assistant/skills/references/command-contracts.md` |
| State schema | `clinical-research-assistant/skills/references/state-schema.md` |
| Writing style guide | `clinical-research-assistant/skills/references/writing-style.md` |
| External (K-Dense) skill registry | `clinical-research-assistant/skills/references/external-skills.md` |
| Skill registry (YAML) | `clinical-research-assistant/skills/references/skill-registry.yaml` |
| biomedagent methodology | `clinical-research-assistant/skills/references/biomedagent-methodology.md` |

### External (K-Dense) skills

138 vendored K-Dense skills live at
`clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/`.
The most relevant for clinical research are listed in §6 below. Read individual SKILL.md
files as needed. (There's also a separate vendored copy of `biomedagent` at
`clinical-research-assistant/skills/external/biomedagent/`.)

---

## 6. K-Dense Delegations (Hard Gates)

CRA delegates specific responsibilities to K-Dense skills at runtime. The contracts are
defined in `clinical-research-assistant/skills/references/kdense-delegations.md`. Codex must
honor these same contracts — they are not Claude-specific.

| Delegation | Triggered by | K-Dense SKILL.md | Gate |
|---|---|---|---|
| **Citation integrity (L041)** | Any citation in any manuscript draft | `clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/citation-management/SKILL.md` | **Hard gate**: PASS / AMBIGUOUS / FAIL. AMBIGUOUS and FAIL block submission. No silent fallback. |
| **Peer review (Check 13)** | `manuscript-qc` Check 13 (L038 audit-tagging) | `clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/peer-review/SKILL.md` | Block submission until L038 audit tags resolved. |
| **Scholar evaluation (Check 14)** | `manuscript-qc` Check 14 (L047 Introduction↔Results symmetry) | `clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/scholar-evaluation/SKILL.md` | **NOT READY** if total score < 14/20. |
| **Zotero integration** | `ZOTERO_API_KEY` environment variable detected | `clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/pyzotero/SKILL.md` | Auto-on; not a gate. |
| **Systematic literature search** | Any `literature-review` invocation | `clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/literature-review/SKILL.md` | Execution backbone — CRA orchestrates, K-Dense executes. |

**Orchestrator-contract pattern**: `/analyze` and `/visualize` (and now Codex's natural-language
equivalents) follow the same pattern — CRA's SKILL.md tells you WHAT to do; the K-Dense SKILL.md
tells you HOW. `Read` both.

---

## 7. Standing Rules (Verbatim — Same as CLAUDE.md)

These rules apply regardless of which agent is running. They are not optional.

### General behavior
- **Brainstorm and present options before executing.** Never dive straight into code or file changes.
- **Confirm the target path** before moving, renaming, or modifying any file.
- **Never delete files** without explicit confirmation from the user.
- **Summarize what you did and why** at the end of every task.
- **If uncertain about intent**, ask one focused question before proceeding.

### Skill-First Rule for Research Tasks
For any clinical research, biostatistics, manuscript-writing, literature-review, or
biomedical-data-analysis task:

- **First action**: `Read` the relevant CRA SKILL.md (from the table in §5).
- **Default to the skill** even when you think you can do it without one.
- **If the skill is missing capability**, do the new work yourself, then update **all three**:
  1. Skill source SKILL.md at
     `~/Claude/dev/clinical-research-assistant/clinical-research-assistant/skills/<skill-name>/SKILL.md`
  2. The corresponding rule in
     `~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/00_Context/working-rules.md`
  3. `lessons-log.json` at
     `~/Claude/dev/clinical-research-assistant/clinical-research-assistant/skills/references/lessons-log.json`
     — add a structured entry with `promoted_to` audit trail.

### Mandatory Analysis-Report Rule
Every clinical-research analysis must end with a date-stamped, 16-section markdown report:
- Filename pattern: `analysis_report_<short-question-slug>_YYYY-MM-DD.md`
- Saved to the project's `Analyses/` or `Reports/` folder.
- Every claim has effect size + 95% CI + P value + (where applicable) BH-FDR Q.
- Every percentage paired with numerator/denominator.
- Re-generate when the analysis is re-run; archive prior versions.
- Full template: `clinical-research-assistant/skills/internal/analyze/SKILL.md` Step 9
  and lessons-log entry **L026**.

### 12-Principle Abstract-Writing Editorial Rubric (Bilal Mirza)
Every abstract draft is run through the 12-principle gate before being declared submission-ready.
Priority principles for active editing: **3 (calibrated language), 7 (therapeutic implications at
the level data supports), 9 (honesty over impact)**. Narrative architecture: principles 1, 2, 6.
Compliance: principle 10. Rigor gate (principle 11): BH-FDR + bootstrap BCa + permutation +
jackknife. Full rubric at
`clinical-research-assistant/skills/internal/write-abstract/SKILL.md` and lessons-log
entries **L017–L025**.

### Verification Standards
- **Standing Rule A**: Every claim is backed by a reproducible computation. No fabricated numbers, no
  paraphrased estimates. If the number isn't in the analysis output, it doesn't go in the manuscript.
- **Standing Rule B**: No fabricated citations. Every citation must be resolvable via DOI, PMID, or
  PMCID and must match the claim it supports. The citation-management hard gate enforces this.

### Other
- **No raw-data mutation**: write derived files to `processed/`, `reports/`, `analyses/`,
  `outputs/`, or `archives/`. Never overwrite raw input.
- **No fabricated citations or claims.**
- **One-commit-per-file** convention from `~/Claude/rules/git-hygiene.md` for hand commits.

---

## 8. MCP Server Setup for Codex

Claude Code wires MCP servers via `.claude-plugin/plugin.json` in the plugin directory.
**Codex uses a different mechanism**: `~/.codex/config.toml`.

To get parity with the Claude side, configure the following MCP servers in
`~/.codex/config.toml` (example syntax — adapt to current Codex MCP spec):

```toml
[mcp_servers.pubmed]
command = "uvx"
args = ["mcp-pubmed"]
# Provides: search_articles, get_article_metadata, get_full_text_article, ...

[mcp_servers.consensus]
command = "uvx"
args = ["mcp-consensus"]
# Provides: search (citation-backed evidence synthesis)
# Citation policy: every result MUST be cited inline as [1], [2], ...
# with paper URLs listed at end of response.

[mcp_servers.zotero]
command = "uvx"
args = ["mcp-zotero"]
env = { ZOTERO_API_KEY = "<from 1Password>" }
# Auto-enables pyzotero K-Dense skill.

# Optional (clinical / translational):
# [mcp_servers.scientific-skills]  # if K-Dense ever ships an MCP wrapper
# [mcp_servers.benchling], [mcp_servers.dnanexus], [mcp_servers.labarchive]
```

**Caveat**: Codex MCP support is evolving. Confirm current syntax at
`https://github.com/openai/codex` before applying. If a server isn't yet supported on Codex,
fall back to using the SKILL.md's documented HTTP/REST instructions directly.

---

## 9. Pre-submission Rigor Remediation Pipeline

If any of the four rigor checks fail at `manuscript-qc` time, the pipeline is:

1. **BH-FDR**: re-run with q ≤ 0.05 (and 0.10 sensitivity), report both.
2. **Bootstrap BCa**: ≥ 2000 resamples; report 95% BCa CI.
3. **Permutation**: ≥ 10,000 permutations; report exact p-value or upper bound.
4. **Jackknife**: leave-one-out; report range of point estimates.

A manuscript with any of these four checks failing is **NOT READY for submission**, regardless
of editorial polish. Full procedure: `clinical-research-assistant/skills/internal/manuscript-qc/SKILL.md`
and lessons-log entries **L011, L023, L025**.

---

## 10. End-of-Session Protocol

Follow `SESSION-END PROTOCOL.md` at the root of the iCloud workspace:
`~/Library/Mobile Documents/com~apple~CloudDocs/Claude_Projects/SESSION-END PROTOCOL.md`.

Run it automatically — do not ask whether to run it.

Codex does not have a separate session-end mechanism; just `Read` that file and execute the
steps before declaring the session complete. The protocol updates `00_Context/session-log.md`,
`00_Context/active-projects.md`, and creates any required lessons-log entries.

---

## 11. Where Claude and Codex Diverge — Known Limitations

| Capability | Claude Code | Codex | Workaround for Codex |
|---|---|---|---|
| Slash commands (`/analyze`, `/visualize`, ...) | ✅ | ❌ | Use natural-language triggers from §5; `Read` SKILL.md manually |
| `Skill` tool with auto-loading frontmatter | ✅ | ❌ | `Read` SKILL.md by absolute path |
| Cowork connectors (Gmail, Slack, Calendar, etc.) | ✅ (Cowork only) | Partial | Configure equivalent MCP servers in `~/.codex/config.toml` |
| `ToolSearch` deferred-tool system | ✅ (Cowork) | ❌ | All Codex tools always available |
| K-Dense runtime delegation (one SKILL.md `Read`s another) | ✅ | ✅ | Same pattern works on Codex |
| Plugin marketplace UI | ✅ | ❌ | Codex reads `AGENTS.md` directly from the cloned repo |
| `.claude-plugin/plugin.json` MCP wiring | ✅ | ❌ | Use `~/.codex/config.toml` instead |
| Reading multiple `AGENTS.md` files hierarchically | N/A | ✅ | Add nested `AGENTS.md` files for project-specific overrides |

**Net effect**: ~85% of CRA functionality is portable. The skills, references, lessons-log,
delegations, and standing rules all work. The plugin runtime layer (slash commands, auto-loading,
plugin MCP wiring) is Claude-specific and must be substituted with manual `Read` + Codex's own
MCP config.

---

## 12. Quick Reference — Most Common Tasks

| Task | First action |
|---|---|
| Start a new clinical-research project | `Read` `clinical-research-assistant/skills/internal/project-init/SKILL.md` |
| Pick up an existing project | `Read` `clinical-research-assistant/skills/internal/resume-project/SKILL.md` |
| Run statistical analysis | `Read` `clinical-research-assistant/skills/internal/analyze/SKILL.md` |
| Generate a publication figure | `Read` `clinical-research-assistant/skills/internal/visualize/SKILL.md` |
| Systematic literature search | `Read` `clinical-research-assistant/skills/internal/literature-review/SKILL.md` |
| Write an abstract | `Read` `clinical-research-assistant/skills/internal/write-abstract/SKILL.md` + run 12-principle rubric |
| Pre-submission QC | `Read` `clinical-research-assistant/skills/internal/manuscript-qc/SKILL.md` — 14 checks, citation hard gate, scholar-eval ≥ 14/20 |
| Verify a citation | `Read` `clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/citation-management/SKILL.md` |

---

## 13. Document Provenance

- **Created**: 2026-05-22 by Claude (Cowork session) at Bilal's request to enable side-by-side
  Codex evaluation of the CRA infrastructure.
- **Mirrors**: `CLAUDE.md` (this repo) + iCloud `00_Context/OPERATING_BRIEF.md` + iCloud
  `00_Context/working-rules.md`.
- **Authoritative source for rules**: iCloud `00_Context/working-rules.md`. If this file
  drifts from working-rules.md, working-rules.md wins.
- **Update protocol**: when working-rules.md changes, also update this file. Same three-place
  update rule applies (skill source SKILL.md + working-rules.md + lessons-log.json), with this
  AGENTS.md as a fourth touchpoint for Codex compatibility.

---

*End of AGENTS.md — Codex should now have full operational parity with Claude Code on CRA tasks,
modulo the runtime-layer gaps listed in §11.*
