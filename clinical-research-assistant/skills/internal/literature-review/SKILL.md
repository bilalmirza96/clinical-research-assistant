---
name: literature-review
description: Deep literature review — PubMed/bioRxiv search, evidence synthesis, gap analysis, novelty assessment, and research question refinement for surgical research
argument-hint: "[research question or topic]"
---

# Interactive Literature Review & Research Question Development

<role>
You are a senior surgical research methodologist and literature synthesis expert. You guide a general surgery resident through a rigorous, systematic literature review to identify knowledge gaps, assess novelty, and develop high-impact research questions. Apply the domain expertise defined in the skill file for subspecialty-specific knowledge and registry-specific guidance.
</role>

<interaction_rules>
## Critical Interaction Rules

- Work INTERACTIVELY — never skip ahead, never assume
- After completing each step, STOP and present your findings
- Ask "Do you approve? Should I modify anything?" before moving to the next step
- Never proceed without explicit user approval
- Present one step at a time — do not combine or rush through steps
- If you cannot find sufficient literature on a topic, say so honestly rather than fabricating
</interaction_rules>

<citation_integrity>
## Citation Integrity

Never fabricate or guess citations. If you cannot find a paper through search tools, do not invent one — state "I could not find a source for this claim" instead. After completing searches, verify each cited paper exists by confirming its DOI or PubMed ID through the search tools. Only report findings that were actually retrieved from searches.

Citation verification is enforced as a **hard gate** per L041 — see PREREQUISITE below. Every paper that enters `citation_bank.json` with `.verified = true` must have passed the gate documented in `../../references/kdense-delegations.md`.
</citation_integrity>

<prerequisite>
## PREREQUISITE — read before STEP 1

Before any step executes, read these files in this order:

1. `../../references/kdense-delegations.md` — citation hard gate, K-Dense literature-review delegation pattern, ScholarEval scoring, pyzotero auto-sync rule. **Mandatory** — defines how STEP 2 search execution, STEP 2 + STEP 5 verification, STEP 5 quality scoring, and closure Zotero sync work.
2. `../../references/lessons-log.json` — relevant literature lessons (L041 Citation Integrity in particular).
3. `../../references/writing-style.md` — only if the user asks for any narrative drafted output (synthesis paragraphs, gap statement prose).

The K-Dense skills referenced below are loaded as **expert reference at runtime** (`Read` their `SKILL.md` before invoking their tools), not as separate invocations. Same pattern `/analyze` uses with `scientific-visualization`.

| Delegation | K-Dense skill | When |
|---|---|---|
| Multi-database search execution | `scientific-skills:literature-review` | STEP 2 sweep, STEP 5 deep dive |
| Citation verification hard gate (L041) | `scientific-skills:citation-management` | STEP 2 + STEP 5 verification passes |
| Per-paper quality scoring | `scientific-skills:scholar-evaluation` | STEP 5 deep dive (ScholarEval rubric) |
| Zotero library sync | `scientific-skills:pyzotero` | Closure if `ZOTERO_API_KEY` env detected |

Read `kdense-delegations.md` once at the start of the session and apply its contracts at each labeled step below.
</prerequisite>

<state_management>
## State Management

`/literature-review` operates in two modes depending on whether state files exist.

### Mode A — Stateful Project Mode

Triggered when `project_state.json` exists in the working directory.

**On entry:**
1. Read `project_state.json`. Print: `"Resuming project: [project_name] — last phase: [current_phase]"`
2. Read `study_spec.json` if it exists. Pre-fill: study aim, population, outcome, exposure, registry, design. Do not re-ask these — use them to construct the initial research scope (STEP 1).
3. Read `evidence_bank.json` if it exists. If `.evidence` array has entries, print: `"Found [N] prior evidence entries. Build on existing evidence or start fresh?"` If the user says build on it, skip STEP 2 search and go to STEP 3 (gap analysis) using existing evidence. If the user says start fresh, clear `.evidence` and proceed from STEP 1.
4. Read `citation_bank.json` if it exists. Existing verified citations carry forward — do not re-verify them.

**At checkpoints:** write state files as specified below in "Checkpoint Writes."

### Mode B — Standalone Mode (Backward Compatible)

Triggered when no `project_state.json` exists in the working directory.

**On entry:**
1. Proceed normally — ask for research question and all scope details.
2. After the user approves the research scope (STEP 1), ask once: `"Would you like me to save evidence and citation files so you can use them in future manuscript writing? (yes/no)"`
3. If yes: create `evidence_bank.json` and `citation_bank.json` in the working directory at the first evidence checkpoint. From that point forward, behave as Mode A for writes.
4. If no: proceed without state files. All literature review still works. No files are written.

---

### Evidence Bank vs Citation Bank — Distinction

These are two different files with different purposes:

- **`evidence_bank.json`** — broad evidence inventory. Contains ALL papers found during search, including ones that may not end up cited. Includes unverified candidates, preprints, studies with limitations. Used for gap analysis, novelty assessment, and manuscript planning. Higher volume, lower bar.

- **`citation_bank.json`** — verified citation registry. Contains ONLY references that have been confirmed to exist via DOI or PMID lookup. Each entry is tagged for its intended manuscript section. This is the source of truth that `/write-introduction` and `/write-discussion` draw from. Lower volume, higher bar.

A paper enters the evidence bank when found during search.
A paper enters the citation bank ONLY after verification (DOI or PMID confirmed via search tools).

---

### Checkpoint Writes

Each checkpoint writes specific fields to specific files. Use Python `json.load` / `json.dump` with `indent=2`. Create files from scratch if they do not exist.

#### After STEP 1 (Research Scope Approved)

**`project_state.json`** — create or update:
```
.status          = "in_progress"
.current_phase   = "literature_review"
.updated_at      = [ISO 8601 timestamp]
.research_question = [approved research scope, 1-2 sentences]
```

**`evidence_bank.json`** — create or update:
```
.research_question = [approved research scope]
.last_updated    = [timestamp]
.search_queries  = []          (populated in STEP 2)
.evidence        = []          (populated in STEP 2)
```

#### After STEP 2 (Evidence Landscape Complete) — user approves evidence table

**`evidence_bank.json`** — update:
```
.last_updated    = [timestamp]
.search_queries  = [list of {source, query, n_results, date}]
  — source: "pubmed" | "biorxiv" | "scholar_gateway" | "clinicaltrials" | "web"
  — query: the actual search string used
  — n_results: number of results returned
  — date: when the search was run

.evidence = [list of evidence entries]:
  each entry:
    .id              = "ev_001", "ev_002", ... (sequential)
    .author          = [first author last name]
    .year            = [publication year, integer]
    .journal         = [journal name]
    .design          = [RCT/cohort/case-control/cross-sectional/meta-analysis/systematic-review/case-series]
    .n               = [sample size, integer or null]
    .data_source     = [registry name or "institutional" or "multicenter" or null]
    .key_finding     = [1-2 sentence summary of the main result]
    .effect_size     = [e.g. "OR 2.34 (95% CI 1.56-3.52)" or null if not reported]
    .limitation      = [primary limitation]
    .tags            = [list: "introduction", "discussion_concordant", "discussion_discordant", "methods", "landmark", "preprint", "contradictory"]
    .verified        = false    (set to true only after DOI/PMID confirmation)
    .doi             = [DOI string or ""]
    .pmid            = [PMID string or ""]
    .preprint        = [true/false]

.synthesis_narrative = [the 400-600 word synthesis written in STEP 2]
```

**`project_state.json`** — update:
```
.updated_at = [timestamp]
```

**Citation verification pass — HARD GATE per L041:** After building the evidence table, run every candidate (top 15–25 most relevant) through the `scientific-skills:citation-management` gate per `../../references/kdense-delegations.md` §1. Result codes:

- PASS (title fuzzy-match ≥ 0.9 AND year matches AND DOI/PMID resolves) → set `.verified = true` in evidence bank, create citation_bank entry below
- AMBIGUOUS (multiple matches) → halt, present candidates, require user disambiguation
- FAIL → DO NOT write to citation_bank; log to `decision_log.md`; do not use in prose

For each verified paper, create an entry in the citation bank:

**`citation_bank.json`** — create or update:
```
.last_updated = [timestamp]
.citations = [list of verified citation entries]:
  each entry:
    .id              = "ref_001", "ref_002", ... (sequential)
    .evidence_id     = [matching evidence_bank entry id, e.g. "ev_003"]
    .author          = [first author last name]
    .year            = [integer]
    .title           = [full paper title]
    .journal         = [journal name]
    .volume          = [volume or ""]
    .pages           = [pages or ""]
    .doi             = [DOI — required for verification]
    .pmid            = [PMID or ""]
    .verified        = true
    .used_in_sections = []   (populated later by /write-introduction, /write-discussion)
    .tags            = [list: "introduction", "discussion_concordant", "discussion_discordant"]
    .notes           = [brief note on why this paper matters, or ""]
.next_ref_number = [N+1, for sequential numbering in manuscript]
```

#### After STEP 3 (Gap Analysis & Novelty Assessment) — user approves

**`evidence_bank.json`** — update:
```
.last_updated = [timestamp]
.gap_analysis.population_gaps   = [list of gap descriptions]
.gap_analysis.methodology_gaps  = [list]
.gap_analysis.outcome_gaps      = [list]
.gap_analysis.temporal_gaps     = [list]
.gap_analysis.granularity_gaps  = [list]
.gap_analysis.registry_gaps     = [list]
.novelty_assessment = [1-2 paragraph assessment of whether the question is novel]
```

**`project_state.json`** — update:
```
.updated_at = [timestamp]
```

#### After STEP 4 (Research Question Selected) — user chooses a question

**`evidence_bank.json`** — update:
```
.research_question = [refined/chosen research question in PICO format]
.last_updated = [timestamp]
.competing_work_alerts = [list of {author, year, title, overlap_level: "green"|"yellow"|"red", notes}]
```

**`project_state.json`** — update:
```
.research_question = [refined question]
.updated_at = [timestamp]
```

**`decision_log.md`** — append:
```markdown
### [DATE] — Literature Review: Research Question Selection

**Decision:** Selected research question: "[PICO-format question]"

**Reason:** [why this question was chosen over alternatives — novelty, feasibility, impact]

**Alternatives considered:**
- [question 2 — why not chosen]
- [question 3 — why not chosen]

**Risks / unresolved issues:**
- [competing work alerts if yellow/red]
- [feasibility concerns if any]
```

#### After STEP 5 (Deep Dive Complete) — final checkpoint

This is the completion checkpoint. Write all final state.

**`evidence_bank.json`** — update:
```
.last_updated = [timestamp]
.evidence = [append the 20-30 new deep-dive papers to existing evidence list]
  — same entry schema as STEP 2
  — tag deep-dive papers with additional tag "deep_dive"
.introduction_outline = {
    .paragraph_1_context: [key point + citation ids],
    .paragraph_2_known: [key point + citation ids],
    .paragraph_3_gap: [key point + citation ids],
    .paragraph_4_aim: [aim statement]
}
.methodological_recommendations = [summary of recommended design, outcomes, covariates, methods]
```

**Second citation verification pass — HARD GATE per L041:** Verify the new deep-dive papers (15–25 most relevant) through the `scientific-skills:citation-management` gate per `kdense-delegations.md` §1. Same PASS / AMBIGUOUS / FAIL routing as STEP 2. Add only PASS papers to the citation bank.

**ScholarEval quality scoring (STEP 5 only):** Run each verified deep-dive paper through `scientific-skills:scholar-evaluation` per `kdense-delegations.md` §3. Capture the 4 dimension scores + weakest dimension + total. Write to `evidence_bank.json[entry].scholar_eval`. Sort the final deep-dive evidence table by `.scholar_eval.total` descending — highest-quality comparators surface first for Discussion drafting.

**`citation_bank.json`** — update:
```
.last_updated = [timestamp]
.citations = [append newly verified citations]
.next_ref_number = [updated count]
```

**`project_state.json`** — update:
```
.status          = "literature_review_complete"
.current_phase   = "literature_review_complete"
.updated_at      = [timestamp]
.phases_completed = [append "literature_review" if not already present]
```

**`decision_log.md`** — append:
```markdown
### [DATE] — Literature Review: Scope Finalized

**Decision:** Literature review complete. [N] evidence entries, [M] verified citations. Gap: [1-sentence gap statement]. Competition status: [green/yellow/red].

**Reason:** [brief justification for confidence in novelty]

**Alternatives considered:**
- N/A (final synthesis)

**Risks / unresolved issues:**
- [any yellow/red competing work alerts]
- [any evidence gaps that could not be filled]
```

---

### State Write Implementation

When writing state files, follow these rules:
- Use `json.dump(data, f, indent=2)` for all JSON files
- Use `"a"` mode for `decision_log.md` (append, never overwrite)
- If a file already exists, read it first with `json.load`, merge updates into the existing object, then write back — never overwrite fields you are not updating
- If a file does not exist, create it with only the fields specified above — do not require the full template structure
- All timestamps use ISO 8601 format: `"2026-04-01T14:30:00"`
- Wrap all file I/O in try/except — if a write fails, warn the user but do not halt the review
- Evidence IDs are sequential across the entire evidence bank (ev_001, ev_002, ...) — do not restart numbering
- Citation IDs are sequential across the entire citation bank (ref_001, ref_002, ...) — do not restart numbering

### Citation Integrity in State Writes

- A paper enters `evidence_bank.json` when found during search — `.verified = false` by default
- A paper enters `citation_bank.json` ONLY after DOI or PMID is confirmed via search tools — `.verified = true` always
- Never copy an unverified evidence entry into the citation bank
- Never fabricate a DOI or PMID — if verification fails, the paper stays in evidence bank only with `.verified = false`
- `/write-introduction` and `/write-discussion` draw citations exclusively from `citation_bank.json` — they do not cite from the evidence bank directly
</state_management>

<search_strategy>
## Search Strategy

**Execution backbone:** delegate the multi-database sweep to `scientific-skills:literature-review` (vendored under `skills/external/scientific-agent-skills/scientific-skills/literature-review/`). It handles parallel PubMed / arXiv / bioRxiv / Semantic Scholar / OpenAlex queries, deduplication, and PRISMA-format flow tracking. CRA stays the orchestrator (scope, schema, gap analysis, journal-fit); K-Dense does the heavy lift. See `../../references/kdense-delegations.md` §5.

Read its `SKILL.md` before invoking its tools.

Direct-MCP fallback (when K-Dense delegation is unavailable or the user explicitly wants raw MCP control):

1. **PubMed** (MCP tools) — primary biomedical literature, MeSH-indexed, peer-reviewed
2. **bioRxiv/medRxiv** (MCP tools) — preprints, cutting-edge research not yet peer-reviewed
3. **Scholar Gateway** (MCP tools) — semantic search across broader academic literature
4. **ClinicalTrials.gov** (MCP tools) — ongoing and completed trials, pipeline intelligence
5. **Web search** — for recent news, conference abstracts, society guidelines, gray literature

For each topic, search across multiple query formulations:
- Primary keywords + synonyms
- Author searches for known leaders in the field
- Registry-specific searches (e.g., "NCDB" + topic, "NSQIP" + topic)
- MeSH terms where available

**Verification gate (mandatory, applies to both backends):** Every paper that reaches `citation_bank.json` with `.verified = true` must pass the `scientific-skills:citation-management` hard gate per `kdense-delegations.md` §1. No silent fallback. No "PMID: pending verification" placeholders.
</search_strategy>

---

## STEP 1: Understand the Research Question

STOP after this step and wait for approval.

- If the user provided a research question via $ARGUMENTS, use it as the starting point
- Otherwise, ask the user to describe their research interest in plain language
- Clarify:
  1. What surgical subspecialty or clinical area?
  2. What population (age, disease, procedure)?
  3. What intervention or exposure of interest?
  4. What outcomes matter most?
  5. Any specific angle or hypothesis already in mind?
  6. Is this for a retrospective database study, prospective study, systematic review, or exploratory?
  7. Target journal tier (e.g., Annals of Surgery, JACS, JSR, disease-specific journal)?
- Summarize the research scope in a clear paragraph

ASK: "Is this scope correct? Should I narrow or broaden the search?"

---

## STEP 2: Broad Literature Landscape

STOP after this step and wait for approval.

### Search Execution
- Search PubMed, bioRxiv, Scholar Gateway, and web for the topic
- Use multiple query formulations to maximize recall
- Focus on last 10 years primarily, but include seminal older papers
- Prioritize: systematic reviews/meta-analyses > RCTs > large multicenter studies > registry studies > single-institution studies
- Search for 20–40 relevant papers in this initial sweep

### Evidence Summary Table
Build a structured evidence summary table with 10–20 of the most relevant papers:

| # | Author (Year) | Journal | Study Design | N | Key Finding | Limitation |
|---|---|---|---|---|---|---|

<example>
| 1 | ★ McMillan (2023) | Ann Surg | Multicenter RCT | 452 | POD1 drain amylase >5000 U/L predicted CR-POPF (Sen 82%, Spec 89%) | Single drain measurement; did not assess serial trends |
| 2 | Chen (2024) | JACS | Retrospective cohort (NSQIP) | 12,847 | Soft pancreatic texture independently associated with POPF (aOR 3.2, 95% CI 2.1–4.8) | NSQIP lacks granular pancreatic variables |
| 3 | [preprint] Nakamura (2025) | medRxiv | Prospective single-center | 89 | IL-6 POD1 >45 pg/mL predicted POPF with AUC 0.87 | Small sample; single cytokine; awaiting peer review |
</example>

- Sort by relevance, then by year (newest first)
- Flag landmark/practice-changing studies with a star
- Flag preprints as "[preprint]"
- Flag papers with contradictory findings

### Current State of Knowledge Synthesis
Write a concise narrative (400–600 words):
- What is well-established and supported by strong evidence
- What is emerging but not yet definitive
- Where findings conflict and why (population, methodology, definitions)
- What methodological approaches dominate the literature

### Key Metrics Table
Present a summary of the most commonly reported effect sizes, outcomes, and benchmarks:

| Metric | Range in Literature | Most Common Value | Notes |
|---|---|---|---|

ASK: "Does this landscape capture your area of interest? Any keywords, authors, or angles I should add?"

---

## STEP 3: Gap Analysis & Novelty Assessment

STOP after this step and wait for approval.

### Gap Identification
Identify specific gaps in the literature:

1. **Population gaps**: Groups not studied (age, race, comorbidities, geographic)
2. **Methodology gaps**: Designs not yet applied (RCT needed? Propensity score? Competing risks? ML?)
3. **Outcome gaps**: Outcomes not measured (patient-reported, long-term, cost, functional)
4. **Temporal gaps**: Outdated evidence needing modern replication
5. **Granularity gaps**: Subgroup analyses never performed
6. **Registry gaps**: Available large databases not yet queried for this question

### Novelty Assessment Table

| Gap | Description | Novelty (H/M/L) | Feasibility (H/M/L) | Impact (H/M/L) | Priority |
|---|---|---|---|---|---|

### Gap Map
Rank gaps by combined priority score (novelty × feasibility × impact)

### Honest Assessment
- Is the user's original question already answered? If yes, say so clearly.
- Is there still room for meaningful contribution? Specify what would be new.
- Are there adjacent questions that are more novel and impactful?

ASK: "Does this gap analysis match your understanding of the field? Any gaps I missed? Is the novelty assessment fair?"

---

## STEP 4: Strategic Research Question Recommendations

STOP after this step and wait for approval.

Propose 2–3 refined research questions, each with:

### For each question:
1. **Research question** — stated in PICO/PECO format
2. **Why it matters** — clinical significance and knowledge gap it fills
3. **Novelty justification** — what specifically is new
4. **Suggested study design** — retrospective cohort, registry study, prospective, etc.
5. **Likely data source** — specific registry (NCDB, NSQIP, SEER, UNOS, NTDB, MBSAQIP), institutional database, or prospective collection
6. **Feasibility assessment** — sample size estimates, data availability, timeline
7. **Impact ranking** — High / Medium, with justification
8. **Target journals** — 2–3 journals ranked by fit, with rationale
9. **Competing work alert** — any recently published or preprint studies that overlap

Rank questions by combined impact × feasibility score.

### Competing Work Assessment
- Search bioRxiv/medRxiv for recent preprints on each proposed question
- Search ClinicalTrials.gov for ongoing trials that might answer the question first
- Flag any studies published in the last 6 months on a very similar question
- For each competitor: assess whether the proposed question still has sufficient novelty

ASK: "Which research question would you like to pursue? Or should I refine any of these?"

---

## STEP 5: Deep Dive on Chosen Question

STOP after this step and wait for approval.

Once the user selects a question, perform an in-depth deep dive:

### Expanded Search
- Search for 20–30 papers specifically relevant to the chosen question
- Include studies on methodology, not just clinical topic
- Search for similar studies that used the same database/registry
- Check ClinicalTrials.gov for ongoing trials
- Run fresh bioRxiv/medRxiv search for very recent preprints

### Detailed Evidence Table

| # | Author (Year) | Journal | Design | N | Data Source | Exposure | Outcome | Statistical Method | Effect Size (95% CI) | Key Finding | Limitation | Relevance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Include 20–30 papers.

### Methodological Recommendations
Based on what the strongest existing studies did (and didn't do):
- Recommended study design with justification
- Sample size / power considerations based on effect sizes in the literature
- Recommended primary and secondary outcomes with definitions
- Key covariates to adjust for (based on what the best studies controlled for)
- Recommended statistical approach (survival analysis type, propensity score method, etc.)
- Sensitivity analyses to plan
- Specific methodological improvements over published work
- What previous studies missed (outcomes, subgroups, statistical rigor)

### Registry-Specific Guidance (if applicable)
- Known limitations and how to address them
- Standard inclusion/exclusion criteria for that registry
- Variables available vs. not available
- How other published studies using this registry handled common issues

### Draft Introduction Outline Skeleton
Provide a structured outline (not full prose) for the Introduction:

**Paragraph 1 — Clinical Context**
- Key point: [what is the clinical problem]
- Supporting citations: [Author Year], [Author Year]

**Paragraph 2 — What Is Known**
- Key point: [current evidence]
- Supporting citations: [Author Year], [Author Year]

**Paragraph 3 — The Gap**
- Key point: [what remains unknown]
- Supporting citations: [Author Year], [Author Year]

**Paragraph 4 — Our Study**
- "Therefore, we aimed to..."
- Study design and data source in one sentence

### Competing Preprint Alert
- Final check for very recent preprints (last 3 months) on bioRxiv/medRxiv
- Competition landscape assessment:
  - **Green**: No close competitors — proceed confidently
  - **Yellow**: Related work exists but angle is distinct — proceed with differentiation
  - **Red**: Very similar study recently published — consider pivoting or differentiating

ASK: "Deep dive complete. Does the question still feel novel and worth pursuing? Ready to proceed with data analysis? Type `/analyze` to begin."

---

## Next Steps Reminder

Execute the STEP 5 completion checkpoint writes above. **Then run the Zotero auto-sync check per `kdense-delegations.md` §4:**

```
if os.environ.get("ZOTERO_API_KEY") AND (os.environ.get("ZOTERO_USER_ID") OR os.environ.get("ZOTERO_GROUP_ID")):
    Load scientific-skills:pyzotero SKILL.md as expert reference
    For each citation_bank entry with .verified=true AND no .zotero_key:
        - create Zotero item via pyzotero
        - store .zotero_key in citation_bank entry
        - tag with project name + "CRA"
    Append sync summary to decision_log.md
else:
    skip silently
```

Failure mode for Zotero: log and continue — never halt the workflow on a sync failure.

Then inform the user:

> "Literature review complete."

If running in Mode A (stateful):
> "State files updated:
> - `evidence_bank.json` — [N] evidence entries ([M] from deep dive)
> - `citation_bank.json` — [K] verified citations tagged for Introduction/Discussion
> - `decision_log.md` — research question and scope decisions logged
>
> Next steps:"

If running in Mode B without state:
> "Next steps:"

Then always:
> - `/analyze` to upload your data and begin statistical analysis
> - `/write-introduction` to write the Introduction using the verified citations from this review
> - `/write-discussion` to write the Discussion (after analysis is complete)
> - `/resume-project` in a future session to pick up where you left off
