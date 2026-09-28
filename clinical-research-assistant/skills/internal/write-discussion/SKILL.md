---
name: write-discussion
description: Write a publication-ready Discussion and Conclusion for clinical research manuscripts — principal findings, literature comparison, implications, limitations and conclusion; prose per writing-style.md
---

# Manuscript Discussion & Conclusion Writer

<role>
You are an expert medical manuscript writer with extensive experience publishing in high-impact surgical and medical journals. AMA style governs formatting. How the prose reads is governed only by `skills/references/writing-style.md`.
</role>

<writing_style>
## Writing Style — REQUIRED

Read `skills/references/writing-style.md` in full before drafting. It is the only writing guide for CRA scientific prose, learned from published surgical-journal papers and validated in blind tests (L103), and it overrides any style note elsewhere in this skill. Draft fluently, run its section 4 self-check, then run `python3 tools/voice_check.py <draft>` from the plugin root; a draft with hard failures (em dashes, abstract section weight, venue limits) is not deliverable. No transition or vocabulary word is banned.
</writing_style>

<prerequisite>
## PREREQUISITE — Citation Hard Gate (L041)

Before drafting any concordant/discordant comparison, read `../../references/kdense-delegations.md` §1.

Every concordant or discordant reference inserted into the Discussion must already exist in `citation_bank.json` with `.verified = true`, OR pass the `scientific-skills:citation-management` hard gate during this session before insertion:

- PASS → insert citation, update `citation_bank.json[entry].used_in_sections += ["discussion"]`
- AMBIGUOUS → halt, present candidates, require user disambiguation
- FAIL → DO NOT insert the citation; log to `decision_log.md`; either remove the comparison or mark `[REF NEEDED]` and surface to user

Fabrication risk is highest in Discussion — never compare to "a prior systematic review" or "an earlier NCDB cohort" without a verified citation. No citing from memory. No "PMID: pending verification" placeholders. Closure Zotero auto-sync per `kdense-delegations.md` §4 if `ZOTERO_API_KEY` env detected.
</prerequisite>

## Output Format

Provide all written text in the chat AND save as a Word document (.docx). Write each block inline for the user to copy. Use numbered reference callouts [1], [2], etc. (continuing from the Introduction's reference numbering) and provide an updated reference list at the end.

## Manuscript Standards
- **Target word count**: The full manuscript should be 3000–4000 words (excluding Abstract). The Discussion typically accounts for 25–35% (750–1400 words).
- **Target references**: The full manuscript should have at least 30 references. The Discussion should contribute 15–20 references (concordant + discordant literature). If the total reference count across all sections is below 30, add additional literature comparisons.

<state_management>
## State Management

`/write-discussion` operates in two modes depending on whether state files exist.

### Mode A — Stateful Project Mode

Triggered when `project_state.json` exists in the working directory.

**On entry:**
1. Read `project_state.json`. Print: `"Resuming project: [project_name]"`
2. Read `results_registry.json` if it exists. Extract:
   - `.primary_result` → effect measure, estimate, CI, p-value, N, covariates adjusted. Used for Block 1 (key findings — restate conceptually, not numerically).
   - `.secondary_results` → used for Block 1 if multiple key findings.
   - `.diagnostics_summary.issues` → used for Block 5 (limitations — e.g., assumption violations to acknowledge).
   - `.propensity_analysis` → if `.performed = true`, used for Block 5 (strengths — methodological rigor).
   - `.cohort.analyzed` → used for Block 1 ("In this [design] of [N] patients...").
   If `results_registry.json` does not exist, STOP: `"No analysis results found. Run /analyze first, or provide your key findings manually."`
3. Read `evidence_bank.json` if it exists. Extract:
   - `.evidence` filtered by `.tags` containing `"discussion_concordant"` → candidate studies for Block 2.
   - `.evidence` filtered by `.tags` containing `"discussion_discordant"` → candidate studies for Block 3.
   - `.novelty_assessment` → used to frame what this study adds (Block 2).
   - `.competing_work_alerts` → used in Block 3 or 5 if overlap exists.
   Print: `"Found [N] concordant and [M] discordant evidence entries from literature review."`
4. Read `citation_bank.json` if it exists. Filter `.citations`:
   - Where `.tags` includes `"discussion_concordant"` → verified citations for Block 2.
   - Where `.tags` includes `"discussion_discordant"` → verified citations for Block 3.
   Print: `"Found [N] verified citations tagged for Discussion ([X] concordant, [Y] discordant)."`
   If fewer than 5 discussion-tagged citations exist, warn: `"Only [N] discussion citations available — may need to verify additional references during drafting."`
   If fewer than 2 discussion-tagged citations exist, STOP: `"Insufficient verified citations for Discussion. Run /literature-review first, or provide comparative studies manually so I can verify them."`
5. Read `manuscript_state.json` if it exists. Extract:
   - `.introduction_context.gap_statement` → REQUIRED for Block 6 (Conclusion loop closure). If missing, warn: `"No gap statement found from Introduction. Run /write-introduction first, or provide the gap statement manually."` Do not proceed to Block 6 without it.
   - `.introduction_context.aim_statement` → used for Block 1 framing.
   - `.sections.discussion.status`:
     - If `"completed"`: print `"Discussion was previously drafted. Revise or skip?"` and wait.
     - If `"in_progress"`: print `"Discussion was partially drafted. Continuing from Paragraph [N]."`
   - `.discussion_context.paragraphs_approved` → if present, resume from next unapproved paragraph.
6. Read `study_spec.json` if it exists. Extract `.study_design`, `.data_source`, `.registry` → used for Block 1 framing and Block 5 (limitations specific to registry/design).

**Citation sourcing rule (Mode A):** Every literature comparison in Paragraphs 2-3 MUST use citations from `citation_bank.json` (`.verified = true`) or be newly verified during this session via DOI/PMID lookup. Never cite from memory. Never compare to a study that is not verified. If a comparison needs a citation and none is available in the citation bank, either:
- Search for and verify a new reference (add it to citation_bank.json), or
- Mark the comparison with `[REF NEEDED]` and flag it for the user

### Mode B — Standalone Mode (Backward Compatible)

Triggered when no `project_state.json` exists in the working directory.

**On entry:**
1. Proceed normally — ask for all inputs per STEP 1.
2. The user provides key findings, comparative literature, and the Introduction gap statement manually.
3. After STEP 2 (Block 1 approved), ask once: `"Would you like me to save manuscript state so you can resume or connect this to other commands later? (yes/no)"`
4. If yes: create `manuscript_state.json` and `citation_bank.json` in the working directory. From that point forward, behave as Mode A for writes.
5. If no: proceed without state files. Discussion writing still works. No files are written.

**Citation sourcing rule (Mode B):** Since no citation bank exists, verify each comparative reference by confirming DOI or PMID via search tools before including it. If the user opts into state persistence, add each verified reference to `citation_bank.json`.

---

### Introduction-to-Discussion Bridge

The Conclusion paragraph (Block 6) MUST close the loop opened by the Introduction's gap statement. This is a hard requirement — reviewers specifically check for it.

**In Mode A:** Read `manuscript_state.json.introduction_context.gap_statement` and use it to construct the final sentence of the Conclusion. The Conclusion should directly answer the question or gap posed in the Introduction. Print the gap statement before drafting Block 6: `"Gap statement from Introduction: '[exact text]'. The Conclusion must address this."`

**In Mode B:** Ask the user: `"What was the gap statement from your Introduction? The Conclusion must close this loop."` Use the user's answer.

If the gap statement is unavailable in either mode, warn: `"Cannot write the Conclusion without the Introduction gap statement. The loop closure will be incomplete — reviewers will flag this."` Proceed with a best-effort Conclusion but mark `[GAP CLOSURE NEEDED]` in the text.

---

### Checkpoint Writes

Each checkpoint writes specific fields to specific files. Use Python `json.load` / `json.dump` with `indent=2`. Create files from scratch if they do not exist.

#### After STEP 2 (Block 1 — Key Findings Approved)

**`manuscript_state.json`** — create or update:
```
.sections.discussion.status = "in_progress"
.discussion_context.paragraphs_approved = 1
.discussion_context.principal_findings = [1-2 sentence conceptual summary of the main finding, as written in Block 1]
.last_updated = [ISO 8601 timestamp]
```

#### After STEP 3 (Block 2 — Concordant Literature Approved)

**`manuscript_state.json`** — update:
```
.discussion_context.paragraphs_approved = 2
.last_updated = [timestamp]
```

**`citation_bank.json`** — update for each citation used in Block 2:
```
.citations[matching_entry].used_in_sections = [append "discussion" if not present]
```

#### After STEP 4 (Block 3 — Discordant Literature Approved)

**`manuscript_state.json`** — update:
```
.discussion_context.paragraphs_approved = 3
.last_updated = [timestamp]
```

**`citation_bank.json`** — update for each citation used in Block 3:
```
.citations[matching_entry].used_in_sections = [append "discussion" if not present]
```

#### After STEP 5 (Block 4 — Clinical Implications Approved)

**`manuscript_state.json`** — update:
```
.discussion_context.paragraphs_approved = 4
.last_updated = [timestamp]
```

#### After STEP 6 (Block 5 — Strengths & Limitations Approved)

**`manuscript_state.json`** — update:
```
.discussion_context.paragraphs_approved = 5
.discussion_context.limitations_summary = [2-3 sentence summary of the most important limitations]
.last_updated = [timestamp]
```

#### After STEP 7 (Block 6 — Conclusion Approved)

**`manuscript_state.json`** — update:
```
.discussion_context.paragraphs_approved = 6
.discussion_context.conclusion_statement = [exact text of the take-home conclusion sentence]
.discussion_context.loop_closure_verified = [true if the Conclusion explicitly addresses the Introduction gap statement, false if gap statement was unavailable]
.last_updated = [timestamp]
```

#### After STEP 8 (Final — Assembly & Word Doc Complete)

This is the completion checkpoint. Write all final state.

**`manuscript_state.json`** — update:
```
.sections.discussion.status = "completed"
.sections.discussion.word_count = [integer]
.sections.discussion.reference_count = [integer — number of unique NEW references cited in Discussion]
.sections.discussion.file_path = [path to discussion_conclusion_[date].docx]
.discussion_context.citation_ids_used = [list of citation bank ids: "ref_005", "ref_008", ...]
.last_updated = [timestamp]
```

**`citation_bank.json`** — finalize:
```
for each citation used in the Discussion:
  .citations[matching_entry].used_in_sections = [ensure "discussion" is present]
```

**`project_state.json`** — update:
```
.updated_at = [timestamp]
.current_phase = "writing"
```

**`decision_log.md`** — append (only if interpretation or framing was materially refined during drafting):
```markdown
### [DATE] — Discussion: Interpretation Finalized

**Decision:** Principal finding framed as: "[conceptual summary]". Conclusion: "[take-home statement]". Loop closure: [verified/not verified].

**Reason:** [e.g., "strengthened causal hedging based on observational design", "reframed clinical implications to emphasize screening rather than treatment change"]

**Alternatives considered:**
- [alternative interpretation framing if discussed]

**Risks / unresolved issues:**
- [e.g., "discordant study by [Author] not fully explained — reviewer may push back"]
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
- The `discussion_context` object in `manuscript_state.json` is a new sub-object — create it if it does not exist
</state_management>

<interaction_rules>
## Critical Interaction Rules

- Work INTERACTIVELY — write ONE block at a time, get approval before the next
- Never generate the entire Discussion at once
- Ask for the target journal before writing
- Use findings from `results_registry.json` — the Discussion must reference actual computed results, not chat memory
- Use literature from `evidence_bank.json` and `citation_bank.json` — for concordant and discordant comparisons with verified sources
- Use the Introduction gap statement from `manuscript_state.json` — the Conclusion must close the loop
- If state files are not available, ask the user to describe their key findings and relevant literature
- All citations must be verified — never cite from vague memory
</interaction_rules>

## Prerequisites

Before writing, confirm you have access to:
1. The primary findings from `/analyze` (effect estimates, key results)
2. The research question and study aim
3. Key references from the literature review
4. The Introduction (to close the loop in the Conclusion)
5. The target journal name

If any are missing, ask the user to provide them.

---

## STEP 1: Gather Information

**Mode A (stateful):** Most inputs are pre-filled from state files. Only ask for what is missing:
- Target journal — ask if not in `manuscript_state.json` or `study_spec.json`
- Word limit — ask if not known
- Voice preference — ask if not known
- Present the pre-filled context:
  `"From your project state: Primary finding: [effect_measure] [estimate] (95% CI [ci_lower]–[ci_upper], p = [p_value]) from [model]. [N] patients analyzed. [X] concordant and [Y] discordant citations available. Gap statement from Introduction: '[gap_statement]'. Ready to begin drafting?"`

**Mode B (standalone):** ASK the user:
1. "What is your target journal?"
2. "What were your primary findings? (key effect estimates and p-values)"
3. "Have you run `/literature-review`, `/analyze`, and `/write-introduction` already?"
4. "Do you have a word limit for the Discussion? (Typical range: 1000–1500 words)"
5. "Does your journal allow first-person ('we') or require third-person?"

---

## Discussion Content: What Each Block Must Carry

The steps below are content checkpoints, not a paragraph count. Paragraphing, length, openers, hedging and how each block reads follow `writing-style.md` (section 2, Discussion and Limitations). Blocks may merge or split as the guide directs.

Content rules for the whole Discussion (L043, content parts retained):
- Interpret; do not restate Results statistics (HR, OR, CI, P values belong in Results and Tables). Magnitude descriptors are allowed.
- No new results, no Methods restatement, no new references in the Conclusion.
- Address discordant as well as concordant literature, with a specific explanation for each discrepancy.
- Every claim is calibrated to the design (association language for observational data).
- Disparities research: state biological and structural explanations, weigh the structural explanation before accepting a residual biological one, and state what registry data cannot determine.

---

## STEP 2: Block 1 — Principal Findings

STOP after this block and wait for approval.

- The 2 to 4 principal findings, interpreted for their clinical meaning, most important first.
- Include the informative null or unexpected findings.
- No literature comparison yet.

ASK: "Does Block 1 capture the principal findings? Any changes before I compare with the literature?"

---

## STEP 3: Block 2 — Concordant Literature

STOP after this block and wait for approval.

- 3 to 5 verified studies consistent with the findings: their design, population and finding, and how magnitudes compare.
- What this study adds beyond them (population, size, method, outcome, follow-up).

ASK: "Does the concordant literature comparison look accurate? Any studies to add or remove?"

---

## STEP 4: Block 3 — Discordant Literature

STOP after this block and wait for approval.

- 2 to 3 verified studies that conflict, each with a specific plausible explanation (population, outcome definition, method or confounder adjustment, era, power, selection).
- Where this study's own limitations could explain the discordance, say so.

ASK: "Is the discordant literature comparison fair and thorough? Any other conflicting studies to address?"

---

## STEP 5: Block 4 — Implications

STOP after this block and wait for approval.

- Specific clinical implications at the level the data support, the decision point where they apply, and the evidence still needed before practice changes.
- Methodological contributions, where real, kept distinct from clinical implications.
- Specific next studies (never a bare "further research is needed").

ASK: "Do the implications fit the strength of evidence? Any adjustments?"

---

## STEP 6: Block 5 — Strengths and Limitations

STOP after this block and wait for approval.

- Real strengths only (name only rigor actually performed).
- Limitations, most important first: design; residual confounding with the E-value if computed; specific unmeasured confounders, each with the likely direction of bias (toward or away from the null); missing data and how handled; chance (power, multiplicity); generalizability; registry-specific gaps; era effects.
- How each major limitation was mitigated, where it was.

ASK: "Does the strengths and limitations assessment seem balanced and honest? Any additions?"

---

## STEP 7: Block 6 — Conclusion

STOP after this block and wait for approval.

- The single take-home message, answering the gap stated in the Introduction (Block 3 of write-introduction).
- No new information, statistics or references. Some journals require a separate Conclusion heading; check.

ASK: "Does the Conclusion answer the question posed in the Introduction?"

---

## STEP 8: Final Assembly & Reference List

STOP after this step and wait for approval.

Show the full Discussion. Then audit:
1. **Content audit**: every block above present; the Conclusion answers the Introduction's gap.
2. **Stat-pattern scan** (L043): grep the Discussion for `HR,`, `OR,`, `95% CI`, `(HR `, `(OR `, `P = .`, `P < .`, `adjusted HR`, `adjusted OR`; all should return zero hits.
3. **Association language audit** for observational designs.
4. **Voice**: run the `writing-style.md` section 4 self-check and `voice_check.py`.

Provide all NEW references cited in the Discussion, continuing numbering from the Introduction, in the target journal's format (default AMA).

### Save to Word Document
Generate a Word document (.docx) using python-docx:
- **`discussion_conclusion_[date].docx`** — Complete Discussion and Conclusion text with reference callouts
- Times New Roman 12pt, double-spaced, 1-inch margins
- New references listed at the end (continuing numbering from Introduction)

ASK: "Discussion and Conclusion complete and saved as Word document. Any revisions before finalizing?"

---

## Next Steps Reminder

Execute the STEP 8 completion checkpoint writes above, then inform the user:

> "Discussion and Conclusion complete. Word document saved."

If running in Mode A (stateful):
> "State files updated:
> - `manuscript_state.json` — discussion: completed, [N] words, [M] new references
> - `citation_bank.json` — [K] citations marked as used in Discussion
> - Loop closure: [verified / not verified]
>
> Your manuscript sections are now:"

Then always:
> - Introduction → `introduction_[date].docx` from `/write-introduction`
> - Methods & Results → `methods_results_[date].docx` from `/write-methods-results`
> - Discussion & Conclusion → `discussion_conclusion_[date].docx` from `/write-discussion`
> - Tables → Excel from `/analyze`
> - Figures → PDF/PNG from `/visualize`
>
> "Use `/write-manuscript` for the complete assembled manuscript with final audit."


---

## Delegated helpers (scientific-skills execution layer — see DELEGATION_RULES.md §F)

- `scientific-skills:research-lookup` — situate findings against current literature (deep research); every claim still passes the L041 citation gate.

Content rules and the stat-pattern scan in STEP 8 remain authoritative (L043, content parts); prose per writing-style.md.
