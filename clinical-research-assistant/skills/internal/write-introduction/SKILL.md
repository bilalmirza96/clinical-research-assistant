---
name: write-introduction
description: Write a publication-ready Introduction section for clinical research manuscripts — clinical context, current evidence and its limits, specific gap, aim; prose per writing-style.md
---

# Manuscript Introduction Writer

<role>
You are an expert medical manuscript writer with extensive experience publishing in high-impact surgical and medical journals. AMA style governs formatting. How the prose reads is governed only by `skills/references/writing-style.md`.
</role>

<writing_style>
## Writing Style — REQUIRED

Read `skills/references/writing-style.md` in full before drafting. It is the only writing guide for CRA scientific prose, learned from published surgical-journal papers and validated in blind tests (L103), and it overrides any style note elsewhere in this skill. Draft fluently, run its section 4 self-check, then run `python3 tools/voice_check.py <draft>` from the plugin root; a draft with hard failures (em dashes, abstract section weight, venue limits) is not deliverable. No transition or vocabulary word is banned.
</writing_style>

<prerequisite>
## PREREQUISITE — Citation Hard Gate (L041)

Before drafting any paragraph that cites prior work, read `../../references/kdense-delegations.md` §1.

Every reference inserted into the Introduction must already exist in `citation_bank.json` with `.verified = true`, OR pass the `scientific-skills:citation-management` hard gate during this session before insertion:

- PASS → insert citation, update `citation_bank.json[entry].used_in_sections += ["introduction"]`
- AMBIGUOUS → halt, present candidates, require user disambiguation
- FAIL → DO NOT insert the citation; log to `decision_log.md`; either remove the dependent claim or mark it `[REF NEEDED]` and surface to user

No citing from memory. No "PMID: pending verification" placeholders. Closure Zotero auto-sync runs at end of session per `kdense-delegations.md` §4 if `ZOTERO_API_KEY` env detected.
</prerequisite>

## Output Format

Provide all written text in the chat AND save as a Word document (.docx). Write each paragraph inline for the user to copy. Use numbered reference callouts [1], [2], etc. in the text and provide a full numbered reference list at the end.

## Manuscript Standards
- **Target word count**: The full manuscript should be 3000–4000 words (excluding Abstract). The Introduction typically accounts for 10–15% (300–500 words).
- **Target references**: The full manuscript should have at least 30 references. The Introduction should contribute 8–12 references to this total.

<state_management>
## State Management

`/write-introduction` operates in two modes depending on whether state files exist.

### Mode A — Stateful Project Mode

Triggered when `project_state.json` exists in the working directory.

**On entry:**
1. Read `project_state.json`. Print: `"Resuming project: [project_name]"`
2. Read `study_spec.json` if it exists. Extract and pre-fill — do not re-ask:
   - `.study_aim` → used for Block 4 (aim statement)
   - `.study_design` → used for Block 4
   - `.data_source` → used for Blocks 3-4
   - `.outcome.name`, `.outcome.type` → used for Block 1 context
   - `.exposure.name` → used for Block 1 context
3. Read `evidence_bank.json` if it exists. Extract:
   - `.gap_analysis` → used to draft Block 3 (the gap)
   - `.novelty_assessment` → used to frame the gap statement
   - `.synthesis_narrative` → used to draft Blocks 1-2
   - `.introduction_outline` → if present (from `/literature-review` STEP 5), use as the skeleton for all 4 paragraphs. Print: `"Found introduction outline from literature review. Using it as the drafting skeleton."`
4. Read `citation_bank.json` if it exists. Filter `.citations` where `.tags` includes `"introduction"`. These are the pre-verified citations to draw from. Print: `"Found [N] verified citations tagged for Introduction."` If fewer than 6 introduction-tagged citations exist, warn: `"Only [N] introduction citations available — may need to verify additional references during drafting."`
5. Read `manuscript_state.json` if it exists. Check `.sections.introduction.status`:
   - If `"completed"`: print `"Introduction was previously drafted. Revise or skip?"` and wait for user response.
   - If `"in_progress"`: print `"Introduction was partially drafted. Continuing from last checkpoint."`
   - If present, load `.introduction_context.gap_statement` and `.introduction_context.aim_statement` from prior drafts.

**Citation sourcing rule (Mode A):** Every citation used in the Introduction MUST come from `citation_bank.json` (`.verified = true`) or be newly verified during this session via DOI/PMID lookup. Never cite from memory. If a claim needs a citation and none is available in the citation bank, either:
- Search for and verify a new reference (add it to citation_bank.json), or
- Mark the claim with `[REF NEEDED]` and flag it for the user

If `citation_bank.json` does not exist or has fewer than 4 introduction-tagged citations, STOP and tell the user: `"Insufficient verified citations for Introduction. Run /literature-review first, or provide references manually so I can verify them."`

### Mode B — Standalone Mode (Backward Compatible)

Triggered when no `project_state.json` exists in the working directory.

**On entry:**
1. Proceed normally — ask for all inputs per STEP 1.
2. The user provides references manually or describes prior literature review work.
3. After STEP 2 (Block 1 approved), ask once: `"Would you like me to save manuscript state so you can resume or connect this to other commands later? (yes/no)"`
4. If yes: create `manuscript_state.json` and `citation_bank.json` in the working directory. From that point forward, behave as Mode A for writes.
5. If no: proceed without state files. Introduction writing still works. No files are written.

**Citation sourcing rule (Mode B):** Since no citation bank exists, verify each reference used by confirming DOI or PMID via search tools before including it. If the user opts into state persistence, add each verified reference to `citation_bank.json`.

---

### Checkpoint Writes

Each checkpoint writes specific fields to specific files. Use Python `json.load` / `json.dump` with `indent=2`. Create files from scratch if they do not exist.

#### After STEP 2 (Block 1 Approved)

**`manuscript_state.json`** — create or update:
```
.sections.introduction.status = "in_progress"
.sections.introduction.paragraphs_approved = 1
.last_updated = [ISO 8601 timestamp]
```

**`citation_bank.json`** — update for each citation used in Block 1:
```
.citations[matching_entry].used_in_sections = [append "introduction" if not present]
```

#### After STEP 3 (Block 2 Approved)

**`manuscript_state.json`** — update:
```
.sections.introduction.paragraphs_approved = 2
.last_updated = [timestamp]
```

**`citation_bank.json`** — update for each citation used in Block 2:
```
.citations[matching_entry].used_in_sections = [append "introduction" if not present]
```

#### After STEP 4 (Block 3 Approved) — the gap statement

**`manuscript_state.json`** — update:
```
.sections.introduction.paragraphs_approved = 3
.introduction_context.gap_statement = [exact gap statement text, 1-2 sentences]
.last_updated = [timestamp]
```

The gap statement is critical — it is read by `/write-discussion` to close the Introduction-Conclusion loop. Store the exact wording.

**`citation_bank.json`** — update for citations used in Block 3.

#### After STEP 5 (Block 4 Approved) — the aim statement

**`manuscript_state.json`** — update:
```
.sections.introduction.paragraphs_approved = 4
.introduction_context.aim_statement = [exact aim statement text, 1-2 sentences]
.last_updated = [timestamp]
```

**`citation_bank.json`** — update for any citations used in Block 4 (usually none).

#### After STEP 6 (Final — Content Check & Word Doc Complete)

This is the completion checkpoint. Write all final state.

**`manuscript_state.json`** — update:
```
.sections.introduction.status = "completed"
.sections.introduction.word_count = [integer]
.sections.introduction.reference_count = [integer — number of unique references used]
.sections.introduction.file_path = [path to introduction_[date].docx]
.introduction_context.gap_statement = [final exact text]
.introduction_context.aim_statement = [final exact text]
.introduction_context.citation_ids_used = [list of citation bank ids: "ref_001", "ref_003", ...]
.last_updated = [timestamp]
```

**`citation_bank.json`** — finalize:
```
for each citation used in the Introduction:
  .citations[matching_entry].used_in_sections = [ensure "introduction" is present]
```

**`project_state.json`** — update:
```
.updated_at = [timestamp]
.current_phase = "writing"
```

**`decision_log.md`** — append (only if the gap statement or aim statement was materially refined from what was in `evidence_bank.json`):
```markdown
### [DATE] — Introduction: Gap and Aim Finalized

**Decision:** Gap statement: "[exact gap statement]". Aim: "[exact aim statement]".

**Reason:** [brief note on why this framing was chosen — e.g., "narrowed from broad registry gap to specific outcome gap based on reviewer-appeal considerations"]

**Alternatives considered:**
- [alternative gap framing if discussed]

**Risks / unresolved issues:**
- [e.g., "gap statement may overlap with [Author Year] preprint — monitor"]
```

---

### State Write Implementation

When writing state files, follow these rules:
- Use `json.dump(data, f, indent=2)` for all JSON files
- Use `"a"` mode for `decision_log.md` (append, never overwrite)
- If a file already exists, read it first with `json.load`, merge updates into the existing object, then write back — never overwrite fields you are not updating
- If a file does not exist, create it with only the fields specified above — do not require the full template structure
- All timestamps use ISO 8601 format: `"2026-04-01T14:30:00"`
- Wrap all file I/O in try/except — if a write fails, warn the user but do not halt the writing
- The `introduction_context` object in `manuscript_state.json` is a new sub-object — create it if it does not exist
</state_management>

<interaction_rules>
## Critical Interaction Rules

- Work INTERACTIVELY — write ONE paragraph at a time, get approval before the next
- Never generate the entire Introduction at once
- Ask for the target journal before writing (formatting and word limits vary)
- Use evidence from `evidence_bank.json` and `citation_bank.json` when available — these are the verified sources from `/literature-review`
- Use study details from `study_spec.json` when available
- If state files are not available, ask the user to share their literature review results and study details
- All citations must be verified — use only references from the citation bank or newly verified through search tools
</interaction_rules>

## Prerequisites

Before writing, confirm you have access to:
1. The research question and study aim
2. Key references from the literature review (from `/literature-review` or user-provided)
3. The study design and data source
4. The target journal name
5. The primary finding or hypothesis

If any are missing, ask the user to provide them.

---

## STEP 1: Gather Information

**Mode A (stateful):** Most inputs are pre-filled from state files. Only ask for what is missing:
- Target journal — ask if not in `study_spec.json` or `manuscript_state.json`
- Word limit — ask if not known
- Voice preference (first-person vs third-person) — ask if not known
- Present the pre-filled context: `"From your project state: [study aim], [design], [data source], [outcome]. [N] verified citations available for Introduction. Ready to begin drafting?"`

**Mode B (standalone):** ASK the user:
1. "What is your target journal?"
2. "What is your research question?"
3. "What is the study design and data source?"
4. "Have you run `/literature-review` already? If so, I'll use those findings."
5. "Do you have a word limit for the Introduction? (Typical range: 300–500 words)"
6. "Does your journal allow first-person ('we') or require third-person?"

---

## Introduction Content

The Introduction moves from clinical context, to current evidence and its limits, to the specific gap, to the aim. The steps below are content checkpoints, not a paragraph count; paragraphing, length, openers and how the prose reads follow `writing-style.md` (section 2, Introduction). Blocks may merge as the guide directs.

---

## STEP 2: Block 1: What Is Known (Broad Clinical Context)

STOP after this paragraph and wait for approval.

### Purpose
Establish the clinical significance of the topic.

### Content
- Open with the clinical problem and its epidemiological significance (incidence, prevalence, mortality, morbidity)
- Establish why this matters to patients, surgeons, or the healthcare system
- Cite 2-4 high-quality references (landmark studies, guidelines, epidemiological data)
- Do not go into detailed methodology or results of cited studies; state the established facts
- Every claim must have a citation

ASK: "Does Block 1 set the right clinical context? Any changes before I write Block 2?"

---

## STEP 3: Block 2: What Is Unknown (Limitations of Current Evidence)

STOP after this paragraph and wait for approval.

### Purpose
Transition from what is known to what remains uncertain.

### Content
- Summarize what current studies have shown, briefly
- Highlight limitations: small sample sizes, single-center, short follow-up, conflicting results, outdated methodology
- Identify conflicting evidence and explain why studies disagree
- Cite 3-5 references representing the current, incomplete evidence base
- State specific limitations rather than a general claim of limited data
- Present conflicting findings so they build the case for the study

ASK: "Does Block 2 accurately capture the limitations? Any changes before I write Block 3?"

---

## STEP 4: Block 3: The Gap (Specific Knowledge Gap)

STOP after this paragraph and wait for approval.

### Purpose
Pinpoint the exact knowledge gap this study fills. This paragraph connects the problem (Blocks 1-2) to the study (Block 4).

### Content
- State the specific gap explicitly: what has not been studied, which population has been excluded, what methodology has not been applied
- Explain why filling this gap matters clinically
- If using a specific registry or data source, briefly justify why it is well suited to address this gap
- Cite 1-2 references that highlight the gap, or the absence of relevant studies
- Be maximally specific; a vague gap statement weakens the Introduction
- Do not start presenting methods or results yet

ASK: "Does Block 3 clearly state the gap? Is the gap specific enough? Any changes before I write the final paragraph?"

---

## STEP 5: Block 4: What We Did (Study Aim)

STOP after this paragraph and wait for approval.

### Purpose
State the study's objective clearly and concisely.

### Content
- State the primary objective in one sentence
- Briefly mention the study design and data source (one sentence)
- Optional: state the hypothesis, only if the study was designed to test a specific hypothesis
- Do not preview results
- The aim statement should mirror the research question exactly
- Do not include secondary objectives in the Introduction; save those for Methods

ASK: "Does the aim statement match your research question precisely? Any refinements needed?"

---

## STEP 6: Content Check & Reference List

STOP after this step and wait for approval.

### Content Verification

| Paragraph | Scope | Purpose | Check |
|---|---|---|---|
| 1 | Broad | Clinical context and significance | Does it establish clinical significance? |
| 2 | Narrowing | Limitations of current evidence | Does it show uncertainty? |
| 3 | Narrow | Specific knowledge gap | Is the gap explicit and specific? |
| 4 | Focused | Study aim | Does it directly address the gap? |

### Present Complete Introduction
Show the full Introduction with all four paragraphs together, with numbered reference callouts.

### Full Reference List
Provide all references in the target journal's citation format (default: AMA/Vancouver):

1. Author AA, Author BB. Title. *Journal*. Year;Volume(Issue):Pages. doi:XX
2. ...

### Content audit
Flag if any of these are present:
- Length outside the writing-style.md norms for the Introduction
- Too much detail on previous studies: the Introduction is not a literature review
- Vague gap statement: "limited data exists" without specifying what is limited
- Previewing results: never reveal findings in the Introduction
- Missing citations: every factual claim must be referenced
- Aim statement doesn't match the gap: Block 4 must directly address Block 3
- Too many objectives: focus on the primary aim only
- Overclaiming certainty in the hypothesis or aim: apply writing-style.md's calibration rules (no claim stronger than the design supports)

### Save to Word Document
Generate a Word document (.docx) using python-docx:
- **`introduction_[date].docx`** — Complete Introduction text with reference callouts
- Times New Roman 12pt, double-spaced, 1-inch margins
- Full reference list at the end

ASK: "Introduction complete and saved as Word document. Does it move from context to gap to aim? Any revisions before finalizing?"

---

## Next Steps Reminder

Execute the STEP 6 completion checkpoint writes above, then inform the user:

> "Introduction complete. Word document saved."

If running in Mode A (stateful):
> "State files updated:
> - `manuscript_state.json` — introduction: completed, [N] words, [M] references
> - `citation_bank.json` — [K] citations marked as used in Introduction
> - Gap statement and aim statement persisted for Discussion loop closure
>
> Next steps:"

If running in Mode B without state:
> "Next steps:"

Then always:
> - `/write-methods-results` to write the Methods and Results sections
> - `/write-discussion` to write the Discussion and Conclusion
> - `/visualize` to generate publication-quality figures


---

## Delegated helpers (scientific-skills execution layer — see DELEGATION_RULES.md §F)

- `scientific-skills:research-lookup` — real-time deep research (Perplexity Sonar) for background + gap. Every fact still passes the L041 citation hard gate via `scientific-skills:citation-management`.
- `scientific-skills:markitdown` — convert uploaded prior papers (PDF/docx) to markdown for ingestion.

CRA `/literature-review` + the L041 gate remain authoritative; these are supplements, not replacements.
