# CRA Writing Guide: Scientific Prose That Reads as Published

> **Binding for every scientific prose deliverable produced through CRA**: abstracts, introductions,
> methods, results, discussions, full manuscripts, literature-review synthesis, cover letters,
> responses to reviewers, and grant text. On 2026-09-28, at the author's direction, this guide
> replaced the earlier author-style reference, the collective abstract style and the House
> Academic Voice sections (lessons-log L103). It is the only writing guide in CRA. Where any
> skill's own style notes conflict with it, this file wins.
>
> It was learned from 18 surgical-journal papers (15 JAMA Network surgical originals, 1 JTCVS
> Open, 2 thoracic guidelines) and validated blind. On two sets of 7 unseen paragraphs, drafts
> written with it beat the prior CRA voice (2.86 vs 2.36, then 3.21 vs 2.43, of 5). Two
> alternative revisions scored lower and were rejected. Published originals still scored 4.5 to
> 5, so the self-check in section 4 is not optional.

## How to use it (every writing task)

1. Read this whole file before drafting.
2. Draft fluently from the facts. Do not copy source wording or flatten the argument.
3. Run the section 4 self-check and revise.
4. Run the mechanical gate from the plugin root: `python3 tools/voice_check.py <draft> [--venue X] [--sections]`.
   It hard-fails on em dashes, structured-abstract section weight (Results the largest section)
   and venue character limits, and flags non-statistical "significant". A draft with hard
   failures is not deliverable.
5. Abstracts only: also run the 13-point editorial gate in `write-abstract/SKILL.md` and use the
   venue-matched example in `write-abstract/examples/` for architecture and length. **Conference
   and meeting abstracts** (AATS, ITSOS, STS, SSO, ASC and similar) follow
   `write-abstract/references/conference-abstract-voice.md` (L110), the author's own abstract voice
   from the submitted ITSOS 2026 text; for them it overrides the "Structured abstract" bullets in
   section 2 below. Everything else in this guide still applies to them.

A bounded mechanical edit of an existing draft (terminology swap, registry-sourced number
correction, typo fix) may skip step 1 but still runs `voice_check.py` and `claim_audit.py` (L101).

Scope: original investigations for JAMA Surgery and JTCVS-level journals. Built from blinded-judge comparisons of model drafts against published paragraphs, a close read of the surgical corpus, and measured corpus norms (section lengths, sentence lengths, hedge and first-person rates, section order), summarized in section 2. This guide covers what those numbers miss: how the prose moves.

House rules carried over, and only these:
- No em dashes. Use commas, parentheses, colons or a new sentence.
- Give numerator and denominator with every percentage when the data provide them.
- No claim stronger than the design supports.
- Never invent a number. A missing quantity is flagged UNSOURCED; never derive a numerator from a percentage or back-calculate P from a CI.
- Name only the analyses actually run.

No transition or vocabulary word is banned. Use Furthermore, Moreover, Additionally, Interestingly, Notably or Importantly where these authors would, which is occasionally and for a real addition or emphasis. No fixed rhetorical phrase is required either. Do not reach for a stock gap line, a stock pivot or a stock opener for the main findings.

---

## 1. What gives a model away

Ranked by how often the judges cited the pattern. Each item is a pair: model habit -> what published authors do.

**1. Wrong sentence packing for the section.** Model drafts do one of two things. Either they chain several findings into one long sentence with semicolons and "and", or they chop connected ideas into uniform one-fact sentences. -> Published authors pack by function. A limitation and its consequence share one sentence ("Because X was unavailable, Y..."). A concession and its main claim share one "Although" sentence. Separate results (mortality, then complications, then readmission) each get their own short sentence. Methods run one step per sentence. The rhythm is uneven because the content is uneven. A model that is even in either direction gets caught.

**2. Too many tidy paragraphs.** Drafts split patient flow into four or five paragraphs, give a sensitivity check its own closing paragraph, and cut a Discussion into many short blocks. -> Published sections use fewer, denser paragraphs. Screening, exclusions, crossovers and the analyzed count run as one block. A sensitivity or stratification check is folded into the end of the paragraph it belongs to. A Discussion often has a summary paragraph and then one long paragraph that works through prior studies.

**3. Over-explaining and restating.** Drafts restate the denominator on every count, spell out abbreviations again in Results after Methods defined them, coin acronyms for terms used twice, announce the design before doing it ("The analysis was conducted in 2 stages"), justify routine choices, and add modifiers that context already supplies ("procedural efficiency", "of the technology"). -> Published authors say a thing once and trust the reader. They go straight into the work ("In the first part of the study, we estimated..."), define an abbreviation once and use it bare afterward, and leave obvious context implied.

**4. Aims written as Methods, and the gap in the wrong place.** Drafts write the objective as a report of completed work ("We described trends, assessed outcomes and compared costs") or pack it into one colon sentence with (1), (2), (3). They also open a new paragraph with the gap. -> Published Introductions end the background paragraph on the gap, then give the aims a short paragraph of their own. The aim is framed as a question or purpose ("we sought to determine whether", "The goal of this study was to evaluate"), not as a list of things already done. Several aims may be posed as separate short questions.

**5. Swapped field terms.** Drafts replace the standard term with a synonym ("arm" for group, "refused" for declined, "present age" for current age, "capped" for truncated, "internal body clock" for circadian clock). They also inflate plain words ("expenditures", "driver", "facilitate", "yield") or slip into conversation ("right away", "run the model"). -> Published authors use the field's own term every time, even when it repeats. Their register is plain and technical at once: "costs", "often", "support", "declined to participate".

**6. Certainty set at the wrong level.** Drafts state prior evidence as settled, state the gap too flatly ("is unknown"), add an interpretive pivot inside Results, and close with claims the data do not carry ("these priorities follow from our findings"). -> Published authors let prior studies "suggest" an association, frame the gap as limited or not well characterized, report Results without interpretation, and end on a modest statement ("remains a priority", "may support"). Hedges cluster in the Discussion and Conclusions; Results carry almost none.

**7. Connectives at the head of every sentence.** Drafts stack sentence-initial transitions ("Together", "Despite this", "Yet", "In contrast", "Likewise") and turn each inference into its own "therefore" sentence. They also drop the one turn that matters. -> Published authors carry most logic inside the sentence: a fronted "Because" or "Although" clause, a "despite" phrase, a trailing participle ("suggesting that...", "leaving open whether..."). They keep one explicit marker, such as "However" or "Accordingly", where the argument actually turns, usually where endorsement or practice meets the gap.

**8. Abstract nouns as subjects.** Drafts make the exposure, the scenario, the model or "the data" the grammatical subject, and they use modeling jargon for people ("decedents", "risk set", "carriers" throughout). -> Published authors keep patients and the study team in subject position: "patients who underwent repair", "women were followed from", "we stratified". In a Limitations sentence, the analysis is the subject and the consequence trails ("our estimates may therefore understate...").

**9. First person removed from the Discussion, or used in the abstract Objective.** Drafts write "this cohort" and "these data" in the Discussion but "We assessed" in the structured-abstract Objective. -> Published Discussions and Limitations say "our study", "our cohort", "our data". The abstract Objective opens with an infinitive ("To evaluate...").

**10. Parallelism that is too perfect.** Drafts write paired estimates as two matched sentences, reorder lists by frequency, and make every list item grammatically identical. -> Published authors join paired values in one sentence with "vs" or "respectively", keep lists in their own (often protocol) order, and tolerate small irregularities: a list whose items are not parallel, "included" where a model would write "were", one verb governing two objects.

**11. Reordered moves.** Drafts put the citation before the claim, move a statement of the reporting standard into the middle of a paragraph, or report crossovers after both groups instead of inside the group they affected. -> Published order is claim, then support. Crossovers and conversions sit inside that group's narrative, and the reporting-standard sentence closes the paragraph that introduces the model.

**12. Stock endings.** Drafts close the Discussion or Conclusions with a future-research agenda or a two-verb flourish ("facilitate adoption and support translation"). -> Published Conclusions run two to four sentences with no statistics. They restate the finding in the design's own words and end on one calibrated implication or a short statement that a question remains.

**13. Rhetorical decoration (added 2026-09-28 from the humanizer and humanink pattern sets, L104).** Seven habits that dress up a sentence without adding a fact. Two are rationed, not removed; the rest are cut.
- *"Not X but Y" reversal.* "The leak rate was not a consequence of technique but of patient selection." -> State what the data show, then interpret: "The higher leak rate was confined to patients with albumin below 3.0 g/dL, which suggests that selection rather than technique accounted for the difference."
- *Copula avoidance (rationed).* "represents", "serves as", "stands as", "functions as" in place of "is". -> Default to "is". One such verb in a section is acceptable; two or more in a section is the tell.
- *Decorative -ing rider (rationed).* A trailing participle that adds no fact: "Follow-up was extended to 5 years, reflecting the importance of long-term outcomes." -> Cut it. A trailing participle that carries an inference stays ("..., suggesting that margin status mediated part of the benefit"), as item 7 recommends, but no more than one per paragraph.
- *Stacked hedges.* "may potentially suggest a possible association". -> One calibrated hedge per claim, or none when the design supports a direct statement ("Frailty was associated with readmission").
- *Dramatic one-line closer.* "This difference matters." after a result. -> Replace the emphasis with the next fact ("..., a difference that persisted after adjustment for comorbidity and stage").
- *Aphorism or dead metaphor.* "Surgical quality is the cornerstone of oncologic success." -> Say the literal claim ("Adequate lymph node yield is required for accurate staging").
- *Same subject opening three or more consecutive sentences.* "Patients were screened. Patients were randomized. Patients were followed." -> Combine or vary the subject. Two in a row is normal Methods prose.

---

## 2. How these authors sound

### Introduction (two to three paragraphs, about 180 to 360 words)
1. Open on the clinical stake: burden, volume, standard of care or cost. Plain declarative, often with "remains" or a rate. No gap and no aim in sentence 1.
2. Add what is known, sometimes as a short history (an old method, its limits, what replaced it). Attribute findings with soft verbs such as suggest, report or has been associated with.
3. Where guidance or enthusiasm exists, set it against the evidence: the endorsement in one sentence, then the turn ("However, ...") and the gap as the close of that paragraph. Name what is missing (a design, a population, a comparison), not a vague "little is known".
4. Last paragraph: the aim, briefly. "We sought to...", "The goal of this study was to...", or a few direct questions. No results and no hypothesis unless the study was powered to test one.
Sentences are long here (about 30 words on average) and subordinated. Participial openers and "While" clauses are common.

### Methods (median about 640 words)
- Subsections: design and population; exposure or intervention and data sources; outcomes with operational definitions; statistical analysis last.
- One step per sentence, about 18 to 25 words. Mostly passive for data handling; "we" for choices the team owns ("We excluded...", "We assumed..."). Repeat "We assumed" for each assumption rather than merging them.
- Define terms where they first appear, in the same sentence, by parenthesis or apposition.
- State a method without defending it unless the choice is unusual. Name the reporting guideline once, in the sentence that introduces the design or model.
- Numbered end-of-follow-up events or eligibility criteria are fine, and they need not be perfectly parallel.

### Results (median about 600 words, near-zero hedges)
- Paragraph 1: flow of participants in one dense block (screened, excluded with reasons in protocol order, crossovers inside the group they affected, analyzed N), then baseline characteristics with a table pointer.
- Then the primary outcome, secondary outcomes and subgroups, in the order the Methods set out.
- Make the outcome or the patients the subject of the sentence ("Ninety-day mortality was lower...", "Among 38 976 patients (mean [SD] age, 55.7 [19.8] years; 21 944 [56.3%] female),..."). Do not signpost with "For the primary outcome," or "X was distributed as follows:", and fold demographics into one parenthetical sentence rather than a list lead-in.
- JAMA typesetting (AMA style), which judges read as human: no comma in numbers (1000; 38 976 with a space from five digits up); "Supplement 1" and "eTable 3 in Supplement 1", not "supplementary material"; the SI conversion as "(to convert to g/L, multiply by 10.0)"; the symbol β for a regression coefficient; no numeral at the start of a sentence (restructure: "Recently, 2 trials..." or spell it out). `voice_check.py` flags these as review items.
- Each distinct result gets a short sentence. Paired values sit together: "(18/212 [8.5%] vs 31/208 [14.9%])". Give the denominator compactly in the parenthesis and do not rebuild "of the N patients" frames around every count.
- No literature, no mechanism and no "Despite" pivots. A single trailing participle ("suggesting that...") is the most interpretation this section allows, and many papers use none.

### Discussion (median about 660 words, the most hedges and first person)
1. First sentence: "In this [design] of [population], [main finding]." Keep the adjustment set inside that sentence ("independent of age, ... and ...") rather than in a second sentence.
2. Prior work, run as a continuous argument: agreement with a named study, then disagreement with a named reason (a different population, definition or approach), linked by "Similarly", "In contrast" or a "despite prior reports" phrase inside a sentence.
3. Mechanism, hedged with may, likely or could, in sentences of ordinary length. Technical terms stay technical.
4. An anticipated objection answered in the authors' voice ("our data suggest", "we favor").
5. An implication for a named group of patients or surgeons, framed as decision support.

### Limitations
- A headed block, usually opened by "This study has several limitations." or a close variant. Strengths, if given, come first as design features.
- "First", "Second" and "Third" are common, and they run inside one paragraph, not a paragraph each; a separate paragraph is for a different kind of point (for example, how to read a noninferiority result), introduced by a plain declarative sentence rather than another ordinal. Do not add an ordinal just to extend the list, and do not open the strengths and the limitations with two separate framing sentences. Each limitation is one or two sentences: the fact, then its consequence in a trailing clause. Name the excluded population or the unmeasured outcome. Keep examples in a trailing parenthetical "(eg, ...)".
- Say "a single state" or "a single center" before naming it. Use "likely", not "probably".

### Conclusions (one paragraph, about 55 words, two sentences)
- Sentence 1 repeats the design and the main association without numbers.
- Sentence 2 gives one implication at the level the design supports, with "may" or "should consider". Stop there.

### Structured abstract (journal abstracts, JAMA family)
Meeting abstracts do not follow these bullets: see `write-abstract/references/conference-abstract-voice.md` (L110).
- Importance: one or two sentences, the stake and the gap in the field's own phrasing.
- Objective: an infinitive ("To compare...").
- Design, Setting, and Participants: dense, dates included.
- Interventions or Exposures: a verbless noun phrase is acceptable.
- Results: participants first, then outcomes in terse, nearly list-like sentences. State the denominator once and pair values with "vs" or "respectively". No pivots and no interpretation.
- Conclusions and Relevance: two sentences with no statistics; name the design, end with a hedged implication, spell out terms in full, and do not redefine abbreviations.

---

## 3. Worked contrasts (invented studies)

**1. Aim written as Methods (Introduction, inguinal hernia).**
Before: "We therefore used a statewide registry to (1) describe trends in robotic inguinal hernia repair, (2) compare 1-year recurrence, and (3) estimate hospital costs."
After: "Therefore, using a statewide registry, we sought to answer 3 questions. How has the use of robotic repair changed over the past decade? Is robotic repair associated with a different rate of recurrence at 1 year? And what does it cost hospitals?"

**2. Gap in its own paragraph, stated too flatly (appendicitis).**
Before: "[Paragraph 3] Despite these advantages, the effect of antibiotic-first management on return to work is unknown."
After: End paragraph 2: "Several societies now endorse an antibiotic-first approach for uncomplicated appendicitis. However, despite these recommendations, data on how this strategy affects return to work are limited." Paragraph 3 then carries only the aim.

**3. Chopped Methods with a separate "therefore" (trauma triage).**
Before: "Prehospital times were missing after 2019. Therefore, we imputed them. Imputation used chained equations. Twenty data sets were created."
After: "Because prehospital times were not recorded after 2019, we imputed them with chained equations across 20 data sets."

**4. Stacked Results sentence (thyroidectomy).**
Before: "Transient hypocalcemia occurred in 41 patients (9.8%); permanent hypoparathyroidism occurred in 6 (1.4%), and recurrent laryngeal nerve palsy was seen in 9 (2.1%), while 30-day readmission was 3.3%."
After: "Transient hypocalcemia occurred in 41 of 418 patients (9.8%) and permanent hypoparathyroidism in 6 (1.4%). Recurrent laryngeal nerve palsy occurred in 9 patients (2.2%). The 30-day readmission rate was 3.3% (14/418)."

**5. Interpretive pivot inside Results (splenic injury).**
Before: "Despite higher injury grades, patients who underwent angioembolization had lower rates of splenectomy, indicating the effectiveness of this approach."
After: "Splenectomy was required in 12 of 164 patients (7.3%) who underwent angioembolization and 29 of 171 (17.0%) managed with observation alone, although injury grade was higher in the embolization group."

**6. Adjustment split off and impersonal voice (Discussion, ventral hernia).**
Before: "Preoperative smoking was associated with mesh infection in this cohort. This association held after adjustment for BMI, diabetes and wound class."
After: "In this cohort of patients undergoing open ventral hernia repair, current smoking was associated with mesh infection, independent of body mass index, diabetes and wound class. Our data suggest that..."

**7. Stacked connectives and an overclaiming close (Discussion, appendicitis).**
Before: "Together, these findings are striking. Yet prior trials reported higher failure rates. In contrast, our failure rate was low. Consequently, antibiotic-first care should be the default."
After: "Although earlier trials reported failure rates near 30%, those trials enrolled patients with appendicolith, whom we excluded, and this difference may explain the lower rate in our cohort. Whether antibiotic-first care should be the default for patients without appendicolith remains a question for a trial designed to answer it."

**8. Limitation with a coined acronym and a separate consequence (cost study, trauma).**
Before: "Our analysis was restricted to hospitals in Ohio. Hospitals in the Midwest Trauma Network (MTN) were excluded. This limits generalizability. The MTN uses a different accounting method."
After: "First, the analysis was limited to a single state, and hospitals in its largest trauma network were excluded because they use a different accounting method, which may reduce the generalizability of our estimates."

**9. Too-perfect parallel sentences (Results, thyroidectomy).**
Before: "Voice change at 2 weeks was reported by 22% of patients with nerve monitoring. Voice change at 2 weeks was reported by 27% of patients without nerve monitoring."
After: "Voice change at 2 weeks was reported by 44 of 200 patients (22.0%) with nerve monitoring and 55 of 204 (27.0%) without it."

**10. Swapped terms and a two-verb conclusion (abstract, hernia).**
Before: "Conclusions: The robotic arm showed improved procedural efficiency, which may facilitate wider adoption of the technology and support RA integration."
After: "Conclusions and Relevance: In this randomized clinical trial, robotic repair was associated with shorter length of stay than laparoscopic repair. These findings may support broader adoption in centers with established robotic programs."

---

## 4. Pre-delivery self-check

Run each item against your own draft before delivery. Fix the draft rather than explaining the choice.

1. Punctuation: no em dashes, no curly quotes. Each semicolon joins two halves of one idea, never two separate results.
2. Rhythm: do sentence lengths vary within each paragraph? In Methods, is each step its own sentence? In Results, is each distinct finding its own sentence? In the Introduction and Discussion, are concessions and causes held inside one subordinated sentence?
3. Paragraphs: is patient flow one block? Are checks folded into their parent paragraph? Is any paragraph just one or two sentences with no reason to stand alone?
4. Introduction: is the gap the last sentence of the background paragraph? Is the aim a purpose or a question, not a list of completed actions?
5. Terms: is every field term the standard one, used the same way throughout (group, declined, current age, truncated)? Are there inflated or conversational words? Is each abbreviation defined once, used bare afterward, and not coined for a term used only once or twice?
6. Restatement: delete repeated denominators in running text (keep n/N inside the parenthesis), justifications for routine methods, design announcements, and modifiers that context already supplies.
7. Certainty: do prior studies "suggest"? Is the gap soft but specific? Are Results free of pivots and interpretation? Are Conclusions free of statistics, and is no claim stronger than the design?
8. Connectives: count sentence-initial transitions per paragraph. More than two is a tell. Keep the one real turn and move the rest into subordinate clauses or trailing participles.
9. Subjects and voice: are patients, surgeons or "we" the subjects wherever possible? Does the Discussion use "our study" and "our data"? Does the abstract Objective begin "To..."?
10. Parallelism: are paired estimates in one sentence? Are lists in protocol order rather than re-sorted?
11. Numbers and typesetting: run `voice_check.py` and clear its AMA-style items (comma thousands, sentence-initial numerals, "supplementary material", spelled-out beta). Does every percentage have its numerator and denominator where the data give them? Is every number traceable to the analysis registry, and is anything else flagged UNSOURCED?
12. Ending: do the Conclusions stop on one calibrated implication, without an agenda and without a flourish?
13. Decoration (section 1 item 13): no "not X but Y" reversals, stacked hedges, one-line dramatic closers or aphorisms. Count "represents"/"serves as" per section (flag at 2 or more) and trailing -ing riders per paragraph (flag at 2 or more; cut any that add no fact). Flag three or more consecutive sentences opening with the same subject.

---

# House Document Formatting — Universal Standard (ALL CRA deliverables)

*Added 2026-08-20 per author instruction. Binding, same status as the writing guide above. Recorded as lesson **L070**.*

## Tables are black and white. Always.

No cell fills, no coloured text, no coloured borders, in any output format — `.docx`, `.xlsx`,
LaTeX, or Markdown destined for print. Structure is carried by **rules and whitespace**; emphasis is
carried by **bold weight only**.

This is a submission requirement, not a preference: most surgical journals typeset tables in
monochrome and bill for colour, and a coloured fill that survives into a submission is a copy-edit
defect the author must strip by hand from every tab and every table.

**L051 bolding is unaffected and still required** — bold cells where p<0.05 in `Table_1`, and where
BH-FDR q<0.05 in `Table_2`, `Sensitivity`, and `Supplementary_*`. Bold is monochrome emphasis and
remains the correct significance flag.

## Every section starts on a new page. Always.

*Added 2026-10-08 per author instruction (lesson **L109**).* In every document or report, each
top-level section (title page, Introduction, Methods, Results, Discussion, Significance,
References, appendices) begins on a new page. Use `pageBreakBefore` on the section heading, not an
empty paragraph holding a manual break, and leave no empty paragraphs above it. Subsections,
tables and figures within a section flow normally. `house_style.py --check` flags a Heading 1
that does not start a page, and its pandoc reference doc sets the break on the Heading 1 style.

## The default font is Times New Roman. Always.

Every document deliverable and every table. Fallback chain: Times New Roman → Liberation Serif →
generic serif.

## Implementation notes

| Output | Requirement |
|---|---|
| **Word** (`python-docx`) | Set `styles['Normal'].font.name = 'Times New Roman'` **and** the `w:eastAsia`/`w:hAnsi` run properties, since python-docx does not propagate the name to all script slots. Use table style `Table Grid` (monochrome). Set the font on every run explicitly; do not rely on style inheritance. |
| **Excel** (`openpyxl` / `xlsxwriter`) | `Font(name='Times New Roman')` on **every written cell**. **No `PatternFill`.** Mark the header with a thin black bottom border and bold, never a fill. |
| **pandoc** | Pass `--reference-doc` pointing at a reference `.docx` whose `Normal` and `Table` styles are already Times New Roman with a monochrome table grid. |
| **Figures** | May retain colour **only** where colour encodes a variable. Must still set Times New Roman, and must remain legible in greyscale per the luminance-separation constraint already in `fig_style.py`. |

## Failure mode this prevents

Library defaults are not choices. `openpyxl`, `xlsxwriter`, and `python-docx` will silently produce
Calibri with an accent-coloured header fill if you let them. Set both properties explicitly on every
deliverable.

## Figures use Times New Roman too

Set `font.family='serif'` with `font.serif=['Times New Roman','Liberation Serif','Nimbus Roman','DejaVu Serif']`
and `mathtext.fontset='dejavuserif'`. Colour is still permitted in figures **only** where it encodes a
variable, and must stay greyscale-separable.

Two traps, both of which produced a silent no-op the first time:

1. **A project-local `fig_style.py` shadows the plugin copy.** `sys.path.insert(0, <script dir>)` means
   `analysis/fig_style.py` wins over `skills/internal/visualize/scripts/fig_style.py`. Check for the
   shadow before assuming a plugin edit took effect.
2. **`setup()` applies rcParams when called, not at import.** A house-font call placed after the import
   but before `setup()` is overwritten. Apply it *after* `setup()`, or put the house font inside `setup()`.

**Verify a font change by opening the rendered image.** The first failed attempt regenerated all three
figures, updated every timestamp, and produced byte sizes close enough to the originals to look plausible
— while still rendering in Arial.

## Mechanical enforcement

`python3 tools/house_style.py FILE...` fixes `.docx` and `.xlsx` in place; `--check` audits and exits 1 on
any violation; `--reference-doc OUT` emits a Times New Roman reference doc for pandoc. In matplotlib call
`house_style.apply_matplotlib()`. This is the format counterpart to `tools/voice_check.py`.
