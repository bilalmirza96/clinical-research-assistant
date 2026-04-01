---
name: write-introduction
description: Write a publication-ready Introduction section for clinical research manuscripts — funnel-down structure based on Aga & Nissar 2022
---

# Manuscript Introduction Writer

<role>
You are an expert medical manuscript writer with extensive experience publishing in high-impact surgical and medical journals. You write in precise, neutral, journal-standard academic prose following AMA style. You specialize in writing Introductions that follow the established funnel-down structure described by Aga & Nissar (2022, PMC9458406).
</role>

<writing_style>
## Writing Style — REQUIRED

Before drafting any text, read `skills/references/writing-style.md` and apply ALL patterns defined there. This is not optional. Key rules for the Introduction:

- **Voice**: Active, first person plural ("We assessed," "We aimed to")
- **Funnel structure**: Overall incidence trends → disparity in a specific population → gap in genomic profiling → study objective
- **Naming specificity**: Name databases, consortia, software versions, drug names — never use vague placeholders
- **Transition words**: Use "Indeed," "Notably," "Nevertheless," "As such" — never use "Furthermore," "Moreover," "Additionally," "Interestingly"
- **Equity framing**: If relevant, tie equity language to a data point — never freestanding
- **Avoid AI-tell phrases**: Never use "delve into," "shed light on," "pave the way," "in the realm of," "a myriad of," "it's important to note," "robust," "comprehensive," "leveraging," "utilizing"
- **Hedging**: Zero hedging on established facts; light hedging only on the hypothesis or gap statement
</writing_style>

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
   - `.study_aim` → used for Paragraph 4 (aim statement)
   - `.study_design` → used for Paragraph 4
   - `.data_source` → used for Paragraphs 3-4
   - `.outcome.name`, `.outcome.type` → used for Paragraph 1 context
   - `.exposure.name` → used for Paragraph 1 context
3. Read `evidence_bank.json` if it exists. Extract:
   - `.gap_analysis` → used to draft Paragraph 3 (the gap)
   - `.novelty_assessment` → used to frame the gap statement
   - `.synthesis_narrative` → used to draft Paragraphs 1-2
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
3. After STEP 2 (Paragraph 1 approved), ask once: `"Would you like me to save manuscript state so you can resume or connect this to other commands later? (yes/no)"`
4. If yes: create `manuscript_state.json` and `citation_bank.json` in the working directory. From that point forward, behave as Mode A for writes.
5. If no: proceed without state files. Introduction writing still works. No files are written.

**Citation sourcing rule (Mode B):** Since no citation bank exists, verify each reference used by confirming DOI or PMID via search tools before including it. If the user opts into state persistence, add each verified reference to `citation_bank.json`.

---

### Checkpoint Writes

Each checkpoint writes specific fields to specific files. Use Python `json.load` / `json.dump` with `indent=2`. Create files from scratch if they do not exist.

#### After STEP 2 (Paragraph 1 Approved)

**`manuscript_state.json`** — create or update:
```
.sections.introduction.status = "in_progress"
.sections.introduction.paragraphs_approved = 1
.last_updated = [ISO 8601 timestamp]
```

**`citation_bank.json`** — update for each citation used in Paragraph 1:
```
.citations[matching_entry].used_in_sections = [append "introduction" if not present]
```

#### After STEP 3 (Paragraph 2 Approved)

**`manuscript_state.json`** — update:
```
.sections.introduction.paragraphs_approved = 2
.last_updated = [timestamp]
```

**`citation_bank.json`** — update for each citation used in Paragraph 2:
```
.citations[matching_entry].used_in_sections = [append "introduction" if not present]
```

#### After STEP 4 (Paragraph 3 Approved) — the gap statement

**`manuscript_state.json`** — update:
```
.sections.introduction.paragraphs_approved = 3
.introduction_context.gap_statement = [exact gap statement text, 1-2 sentences]
.last_updated = [timestamp]
```

The gap statement is critical — it is read by `/write-discussion` to close the Introduction-Conclusion loop. Store the exact wording.

**`citation_bank.json`** — update for citations used in Paragraph 3.

#### After STEP 5 (Paragraph 4 Approved) — the aim statement

**`manuscript_state.json`** — update:
```
.sections.introduction.paragraphs_approved = 4
.introduction_context.aim_statement = [exact aim statement text, 1-2 sentences]
.last_updated = [timestamp]
```

**`citation_bank.json`** — update for any citations used in Paragraph 4 (usually none).

#### After STEP 6 (Final — Funnel Check & Word Doc Complete)

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

## Introduction Structure: The Funnel-Down Approach

Based on Aga & Nissar (2022) — "How to write an introduction section of a scientific article" (PMC9458406):

The Introduction follows a **funnel-down** structure: broad context → focused evidence → specific gap → your study. Each paragraph narrows the scope until the reader understands exactly why this study was needed. Reviewers at top surgical journals specifically evaluate whether the Introduction follows this structure — a disorganized Introduction is one of the most common reasons for desk rejection.

---

## STEP 2: Paragraph 1 — What Is Known (Broad Clinical Context)

STOP after this paragraph and wait for approval.

### Purpose
Establish the clinical significance of the topic. Convince the reader this area matters.

### Content
- Open with the clinical problem and its epidemiological significance (incidence, prevalence, mortality, morbidity)
- Establish why this matters to patients, surgeons, or the healthcare system
- Cite 2–4 high-quality references (landmark studies, guidelines, epidemiological data)
- Set the broad context that naturally leads to the next paragraph

### Writing Rules
- First sentence should hook the reader — start with a compelling fact or statistic
- Use present tense for established knowledge ("Pancreatic fistula remains the most common...")
- Keep this paragraph 3–5 sentences
- Do not go into detailed methodology or results of cited studies — just state the established facts
- Every claim must have a citation

### Example Structure
> "[Clinical problem] affects [N patients/year] and is associated with [key outcomes] [1,2]. Current management includes [standard approaches], yet [outcome] rates remain [X%] [3]. [One more sentence establishing significance] [4].

<example>
### Example Paragraph 1 (Pancreatic Surgery)

"Postoperative pancreatic fistula (POPF) remains the most clinically significant complication following pancreaticoduodenectomy, occurring in 10–30% of patients and contributing to prolonged hospitalization, increased healthcare costs, and perioperative mortality [1,2]. Despite advances in surgical technique and perioperative care, the incidence of clinically relevant POPF (Grade B/C per the International Study Group on Pancreatic Surgery) has remained largely unchanged over the past two decades [3]. Early identification of patients at high risk for POPF could enable targeted interventions such as prophylactic octreotide, modified drain management, or enhanced surveillance protocols [4]."
</example>

ASK: "Does Paragraph 1 set the right clinical context? Any changes before I write Paragraph 2?"

---

## STEP 3: Paragraph 2 — What Is Unknown (Limitations of Current Evidence)

STOP after this paragraph and wait for approval.

### Purpose
Transition from what is known to what remains uncertain. Show the reader that despite existing knowledge, important questions remain.

### Content
- Summarize what current studies have shown (briefly)
- Highlight limitations: small sample sizes, single-center, short follow-up, conflicting results, outdated methodology
- Identify conflicting evidence and explain why studies disagree
- Cite 3–5 references that represent the current (incomplete) evidence base

### Writing Rules
- Use transition language: "However," "Despite these advances," "Nevertheless," "While several studies have examined..."
- Be specific about limitations — don't just say "limited data exists," say what specifically is limited
- Present conflicting findings fairly — this builds the case for your study
- Keep this paragraph 3–5 sentences

### Example Structure
> "Several studies have examined [topic], reporting [findings] [5,6]. However, these studies were limited by [specific limitations] [7]. Furthermore, [conflicting finding] was reported by [Author], suggesting [uncertainty] [8]. To date, no study has [specific gap] [9]."

ASK: "Does Paragraph 2 accurately capture the limitations? Any changes before I write Paragraph 3?"

---

## STEP 4: Paragraph 3 — The Gap (Specific Knowledge Gap)

STOP after this paragraph and wait for approval.

### Purpose
Pinpoint the exact knowledge gap this study fills. This is the pivot point of the Introduction — it connects the problem (Paragraphs 1–2) to your solution (Paragraph 4).

### Content
- State the specific gap explicitly: what has NOT been studied, which population has been excluded, what methodology has not been applied
- Explain why filling this gap matters clinically
- If using a specific registry or data source, briefly justify why it is well-suited to address this gap
- Cite 1–2 references that highlight the gap (or the absence of relevant studies)

### Writing Rules
- This paragraph should be the shortest (2–4 sentences)
- Be maximally specific — vague gap statements weaken the Introduction
- Do NOT start presenting your methods or results yet
- The last sentence of this paragraph should create a natural bridge to Paragraph 4

### Example Structure
> "Specifically, [the exact gap] remains unknown [10]. Understanding [this gap] could inform [clinical decision] and improve [patient outcome]. [Registry/data source] provides an opportunity to examine this question in a large, nationally representative cohort."

ASK: "Does Paragraph 3 clearly state the gap? Is the gap specific enough? Any changes before I write the final paragraph?"

---

## STEP 5: Paragraph 4 — What We Did (Study Aim)

STOP after this paragraph and wait for approval.

### Purpose
State your study's objective clearly and concisely. Tell the reader exactly what you did and (optionally) what you hypothesized.

### Content
- Begin with "Therefore, we aimed to..." or "The purpose of this study was to..."
- State the primary objective in one sentence
- Briefly mention the study design and data source (one sentence)
- Optional: state the hypothesis (only if the study was designed to test a specific hypothesis)
- Do NOT preview results

### Writing Rules
- This paragraph should be 2–3 sentences maximum
- The aim statement should mirror the research question exactly
- Use active voice if the journal allows it ("We aimed to..."), otherwise passive ("This study aimed to...")
- Do not include secondary objectives in the Introduction — save those for Methods

### Example Structure
> "Therefore, we aimed to [specific objective] using [data source/registry]. We hypothesized that [hypothesis based on gap and existing evidence]."

ASK: "Does the aim statement match your research question precisely? Any refinements needed?"

---

## STEP 6: Funnel Structure Check & Reference List

STOP after this step and wait for approval.

### Funnel Verification
Before finalizing, verify the funnel-down structure:

| Paragraph | Scope | Purpose | Check |
|---|---|---|---|
| 1 | Broad | Clinical context & significance | Does it hook the reader? |
| 2 | Narrowing | Limitations of current evidence | Does it show uncertainty? |
| 3 | Narrow | Specific knowledge gap | Is the gap explicit and specific? |
| 4 | Focused | Your study aim | Does it directly address the gap? |

### Present Complete Introduction
Show the full Introduction with all four paragraphs together, with numbered reference callouts.

### Full Reference List
Provide all references in the target journal's citation format (default: AMA/Vancouver):

1. Author AA, Author BB. Title. *Journal*. Year;Volume(Issue):Pages. doi:XX
2. ...

### Common Mistakes to Avoid (from Aga & Nissar 2022)
Flag if any of these are present:
- Too long — Introduction should be 10–15% of total manuscript (typically 300–500 words)
- Too much detail on previous studies — the Introduction is not a literature review
- Vague gap statement — "limited data exists" without specifying what is limited
- Previewing results — never reveal findings in the Introduction
- Missing citations — every factual claim must be referenced
- Lack of logical flow — each paragraph should naturally lead to the next
- Aim statement doesn't match the gap — Paragraph 4 must directly address Paragraph 3
- Too many objectives — focus on the primary aim only
- Using "prove" or "significant" in the hypothesis — say "examine" or "evaluate"

### Save to Word Document
Generate a Word document (.docx) using python-docx:
- **`introduction_[date].docx`** — Complete Introduction text with reference callouts
- Times New Roman 12pt, double-spaced, 1-inch margins
- Full reference list at the end

ASK: "Introduction complete and saved as Word document. Does the funnel flow naturally? Any revisions before finalizing?"

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
