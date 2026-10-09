# Conference Abstract Voice: How the Author Writes Meeting Abstracts

> **Binding for every conference/meeting abstract** (AATS, ITSOS, STS, SSO, ASC, WSA, SSAT, ASCO
> meeting, DDW and similar), added 2026-10-09 at the author's direction (lessons-log **L110**).
> For these abstracts this file overrides the "Structured abstract" bullets in
> `skills/references/writing-style.md` section 2, which describe JAMA-family *journal* abstracts.
> Everything else in writing-style.md still applies (no em dashes, n/N with percentages, no
> invented numbers, field terms, section 1 tells), as do the 12 principles in `../SKILL.md`.
>
> **Why this exists.** On 2026-09-28 (L103) the abstract voice that had been distilled from the
> author's own abstracts was replaced by a guide trained on JAMA papers. The guide is right for
> manuscripts and wrong for meeting abstracts: it makes the Objective an infinitive, forbids
> interpretation in Results, and caps Conclusions at two hedged sentences. The first abstract
> drafted under it (AATS 2027 lung disparities, 2026-10-08) passed every linter and the 12-point
> gate and was still rejected by the author as flat. The canonical source is the author's
> **submitted** ITSOS 2026 esophageal disparities abstract (`../examples/example_disparities_genomics-registry.md`).

## 1. The architecture (registry, outcomes and disparities abstracts)

**Objective: stake, uncertainty, conditional two-alternative question.**
- Sentence 1 states the clinical stake and the uncertainty in one breath: "Multimodal therapy has
  improved esophageal cancer survival, but whether these gains have been shared equitably by race
  is uncertain."
- Sentence 2 is first person and poses the question as competing explanations, often conditional:
  "We assessed whether the Black-White survival gap narrowed in the ICI era and, if not, whether
  residual disparity reflects tumor biology or inequitable access to multimodal care."
- Never open with a "To compare..." infinitive and never list completed analyses as the aim.

**Methods: data sources with n, the covariate list, the named analytic moves. Nothing else.**
- Design and every data source with its n in the first sentence ("Matched retrospective cohort
  study across three platforms: SEER (n=32,820), the National Cancer Database (NCDB; n=114,633)...").
- Enumerate the adjustment covariates. Never collapse them into "clinical factors".
- Name the analytic moves that carry findings: propensity-score matching, inverse-probability
  weighting, multiple imputation, counterfactual decomposition, causal mediation.
- Leave out analysis-plan labels (Model A/B, rung, P1/P2, S1-S9, era codes), internal QA
  machinery (bootstrap/permutation/jackknife gates, linters, red teams) and long lists of
  correction methods. In the submitted ITSOS text the author cut Bonferroni and E-value from the
  Methods list and kept mediation, because mediation is a finding.

**Results: one causal arc, told in order.** For a disparities abstract the arc is:
1. The trend or headline outcome (did the gap change?).
2. The overall disparity, adjusted, with the propensity-matched value beside it.
3. The treatment gap: adjusted OR, then robustness in one clause ("robust within every stage,
   histology and across socioeconomic adjustment, facility clustering, replication in SEER
   database, matched analysis (OR range, 0.48-0.61; E-value, 3.41)").
4. **Where in the care pathway the gap arises** (not recommended vs refused, not offered vs
   declined), with an interpretive tail naming the largest measurable contributor.
5. How much of the outcome gap the treatment gap carries (mediation), when the mediation is
   abstract-grade.
6. **The negative control**: other modalities that were equitable ("Chemotherapy and radiation
   receipt were equitable, with modest adjusted differences after accounting for..."). This is
   what turns "undertreatment" into "a modality-specific gap".
7. The advanced-disease therapy gap with the single "despite" pivot ("NHB patients were less likely
   to receive ICI (10.7% vs 19.5%; adjusted OR, 0.73) despite a tumor profile suggesting greater
   ICI responsiveness...").

Sentence mechanics:
- Long, layered sentences are fine; each carries one step of the arc.
- Magnitude words where size is the point: "at about half the White rate", "substantially more
  often", "rare in both groups". The adjusted estimate travels with them.
- A short interpretive clause inside Results is allowed and expected when it names what a result
  localizes ("identifying the surgical-recommendation step as the largest measurable contributor").
- Exactly one "despite" pivot, used for the key tension.
- Protective nuance in a trailing clause ("with modest adjusted differences after accounting for
  the higher squamous proportion among NHB patients").

**Conclusions: about five declarative sentences, each stating what one result means.**
- Open with the headline finding as a statement ("The Black-White esophageal cancer survival gap
  widened across the contemporary multimodal era.").
- Name the dominant measurable driver and what it is not ("the dominant measurable driver was the
  surgical-recommendation step rather than patient refusal").
- Carry the negative-control contrast as the thesis ("indicating a modality-specific gap rather
  than generalized undertreatment").
- Restate the "despite" tension.
- End on the concrete, highest-leverage levers in one sentence ("Equitable operability review,
  surgical referral, and ICI-trial inclusion of Black patients are the highest-leverage targets.").
- No statistics, no weakness, no "further research is needed".

**Title:** a contrast claim when the data carry one ("Surgery Access, Not Tumor Biology, ...").

## 1b. Sentence-level texture: what makes it read as written by a surgeon, not a model

Measured 2026-10-09 on the submitted ITSOS text against the rejected AATS lung draft (same
character budget, same registry discipline). Each item is a tendency to reproduce, not a quota.

**1. The parenthesis test (the single most important habit).** Delete every parenthesis and
bracket from the Results. The ITSOS text still reads as a complete story: "Black patients had worse
cancer-specific and overall survival. Among Stage I-III patients, Black patients underwent
cancer-directed surgery at about half the White rate, robust within every stage..." The rejected
draft collapsed into "resection was performed in 24,412 of 45,136 NHB patients and 241,912 of
397,477 NHW patients" (no direction, no size) and twelve "Model A/Model B" labels. Rule: the
prose carries the finding (direction, size in words, who, where); the parentheses carry the proof.
Both texts hold about 20% of their characters in parentheses. The difference is what lives outside them.

**2. Effect size in words, outside the parentheses.** "at about half the White rate", "about half
as likely", "about half of the survival disparity", "substantially more often", "rare in both
groups", "modest adjusted differences", "worse". The number follows in parentheses. "About" appears
three times; modal verbs (may, might, could) appear zero times.

**3. Hedge by scope and provenance, never by modal verb.** The author's qualifiers bound what was
*measured* rather than what *might be*: "the largest **measurable** contributor", "the dominant
**measurable** driver", "surgery was **recorded as** not recommended", "**documented** refusal",
"**residual** disparity", "a tumor profile **suggesting**". These are honest and confident at once.
The rejected draft used "may account for part" and "suggesting confounding by operability", which
hedge the claim itself.

**4. Frame first, claim second.** Results sentences open by setting scope, then make the claim:
"Over 2010-2023,", "Among Stage I-III patients,", "In causal mediation analysis,", "In Stage IV
disease,". That is how the denominator (L090) gets named without a "Among patients with clinical
stage I-II NSCLC and known surgery status" mouthful: the population is a short fronted phrase in
the reader's words.

**5. The subject is the step of care the sentence is about.** "Cancer-specific survival ...
improved", "Surgery was recorded as not recommended", "Chemotherapy and radiation receipt were
equitable", "NHB patients were less likely to receive ICI". Never an estimand ("the Model A
24-month HR was"), a model, or "the deficit".

**6. Plain, spoken, value-bearing vocabulary.** gap, worse, about half, driver, rare, equitable,
inequitable access, shared equitably, highest-leverage targets. Not: deficit, attenuated, hazard of
death, covariates, indirect effect, direct effect, estimand. Statistical terms appear only as named
methods ("causal mediation analysis", "propensity-matched") or inside parentheses.

**7. Lexical echo stitches the arc.** Key words recur verbatim across sections so the reader
follows one thread: "shared **equitably**" (Objective) -> "inequitable access" (Objective) ->
"receipt were **equitable**" (Results) -> "**Equitable** operability review" (Conclusions);
"surgical-recommendation step" in Results and Conclusions; "about half" in Results and
Conclusions; "Black-White survival gap" in Objective and Conclusions. Do not swap in synonyms for
variety.

**8. "X rather than Y" and "despite" are the contrast engine.** "the surgical-recommendation step
rather than patient refusal"; "a modality-specific gap rather than generalized undertreatment";
"despite a tumor profile suggesting greater ICI responsiveness" (Results) restated as "Despite
favorable tumor biology..." (Conclusions). The same tension appears in Results and again in
Conclusions; that is one pivot told twice, not two pivots. The title carries the same contrast
("..., Not ...,").

**9. Rhythm by section.** Objective 2 sentences (mean 25 words). Methods 4 sentences (19), opening
with a verbless fragment ("Matched retrospective cohort study across three platforms: ..."). Results
7 long, layered sentences (mean 36, up to 55). Conclusions 5 short declaratives (mean 17). Long
evidence, short meaning. The rejected draft had a one-sentence 36-word Objective and two
Conclusions sentences averaging 29 words.

**10. Name the groups for the sentence's job.** Plain "Black" and "White" in narrative claims
("Black patients had worse ...", "at about half the White rate", "ICI-trial inclusion of Black
patients"); NHB/NHW in head-to-head numeric comparisons. Both are defined once in Methods. The
registry label is used where precision matters and the plain word where people are the point.

**11. Tolerated irregularity, not manufactured error.** The text keeps small, human
non-uniformities: a list that is not perfectly parallel ("within every stage, histology and across
socioeconomic adjustment, facility clustering, replication in SEER database, matched analysis"), the
Oxford comma used in one list and not the next, "HR 0.87" beside "HR, 0.92", articles dropped under
character pressure. Do not polish these into uniformity. Do not imitate genuine slips either (the
capital "Overall" after a semicolon, "showed similar asymmetrical pattern" without "a"): leave them
for the author to keep or fix.

**12. What never appears.** Analysis-plan labels (Model A/B, P1, rung), "respectively", "the
cohort included N patients, of whom..." as a Results opener, a sentence about QA machinery, a
weakness or confounder, "further research", a modal-verb conclusion.

## 1c. Why one reads as a story and the other as a data dump (the linguistics)

The author's diagnosis (2026-10-09): the ITSOS abstract "reads well, flows well, and has the
reader at the center"; the rejected draft "seems like a bunch of data being presented". The
difference is structural, and it is measurable sentence by sentence.

**Stress position (Gopen and Swan).** Readers give most weight to the end of a sentence. Extract
the last words of each sentence once parentheses are removed:

| ITSOS (submitted) | Rejected AATS draft |
|---|---|
| ...shared equitably by race **is uncertain** | ...hospital factors account for any difference |
| ...or **inequitable access to multimodal care** | ...**were NHB and 1,171,167 were NHW** |
| ...had **worse cancer-specific and overall survival** | ...**241,912 of 397,477 NHW patients** |
| ...step as the **largest measurable contributor** | ...from 2004-2009 to 2019-2022 but persisted |
| ...**about half of the survival disparity** | ...NHB patients after **Model B adjustment** |
| ...rather than **patient refusal** | ...which attenuated under **Model B** |
| ...rather than **generalized undertreatment** | ...suggesting **confounding by operability** |
| ...are the **highest-leverage targets** | ...**worse overall survival after full adjustment** |

ITSOS puts a meaning in every stress position: uncertainty, inequity, worse, largest contributor,
about half, rather than refusal, highest-leverage. The draft puts there what the reader can do least
with: raw counts, model names, years, a weakness and a null.

**Topic position and thematic progression (given then new).** Each ITSOS sentence starts from
something the reader already holds and moves to something new: survival in the ICI era, then Black
patients over 2010-2023, then surgery among stage I-III patients, then why surgery was not done,
then how much of the survival gap surgery carries, then the other treatments, then stage IV. Every
topic is a link in one chain: the gap, then its cause, then its size, then its boundary. The draft's
topics jump: "The cohort", "Among patients with clinical stage...", "The deficit", "Across all
stages", "In clinical stage I and II", "With Model A covariates", "Across all stages, the Model A
24-month HR". The reader has to rebuild the thread at every period.

**The reader's questions, answered in order.** The ITSOS Objective plants a question with a fork:
did the gap narrow, and if not, is it biology or access? Every Results sentence then answers the
next question the reader is already asking: Did it narrow? (no, not for Black patients). Is there a
gap? (worse survival). Is it treatment? (surgery at about half the rate, robust). Why no surgery?
(not recommended, not refused). Does it matter? (about half of the gap). Is it all treatment?
(no, chemotherapy and radiation were equitable). And biology? (ICI less often despite favorable
biology). The Conclusions then close the fork from the Objective: access, not biology. The draft's
Objective asks three parallel things without tension, so its Results have nothing to resolve and
read as an inventory.

**Who does the interpreting.** In ITSOS the writer interprets, and the reader receives a claim with
its evidence attached ("at about half the White rate (adjusted OR, 0.50)"). In the draft the reader
must interpret: "(Model B odds ratio [OR], 0.70; 95% CI, 0.67-0.73)" after a sentence of counts
leaves the reader to work out that 0.70 means less surgery and whether that is large. A data dump
hands over evidence; a story hands over meaning plus evidence.

**Agents and actions versus nominalizations.** ITSOS: "Black patients underwent cancer-directed
surgery", "NHB patients were less likely to receive ICI", "Surgery was recorded as not
recommended". People and decisions act. The draft: "resection was performed in 24,412 of 45,136
NHB patients", "The deficit persisted", "a higher hazard of death ... which attenuated". Abstract
nouns and statistical quantities act, and the patient disappears.

**Evaluative language (stance).** ITSOS judges: worse, equitable, inequitable, rare, substantially,
largest, dominant, favorable, highest-leverage. Each judgment is earned by a parenthesis. The draft
reports with neutral verbs (included, was performed, persisted, attenuated, did not differ), so
nothing signals what matters. Stance words tell the reader where to look. Without them, every
number weighs the same.

**Cohesion.** ITSOS repeats its key terms verbatim (gap, equitable, about half,
surgical-recommendation step, Black-White) so the text holds together as one argument. The draft
varies its terms (resection / deficit / difference; NHB patients / patients with clinical stage
I-II NSCLC and known surgery status) and adds analytic vocabulary at each step, so it reads as
separate findings.

**Practical test for any draft.** (1) Read only the last five words of each sentence. If they don't
summarize the argument, the stress positions are wasted. (2) Read only the first five words. If
they don't form a chain, the thread is broken. (3) Delete the parentheses. If the story survives,
the reader is at the center.

## 2. Story-completeness check (run before line editing)

Answer each item from the registry before drafting a sentence. A "no" means a missing story
element, not a style nit: find the result, or state in the draft notes why it does not exist.

| # | Element | Question |
|---|---|---|
| S1 | Stake and alternatives | Does the Objective name the stake and two competing explanations? |
| S2 | Headline | Is the single strongest, most robust result stated first in Results and first in Conclusions? |
| S3 | Robustness in one clause | Are matching/weighting/within-facility/sensitivity results compressed into an OR range plus E-value? |
| S4 | Localization | Is the step where the gap arises shown (reason-for-no-treatment codes, recommendation vs refusal)? |
| S5 | Compensation | Is it shown whether an alternative treatment offsets the gap (e.g., SBRT for unresected early-stage lung cancer)? |
| S6 | Negative control | Are equitable modalities reported, so the gap reads as specific rather than generalized? |
| S7 | Pivot | Is there one "despite" tension, and is it the right one? |
| S8 | Lever | Do Conclusions end on a concrete, named target that the data support? |

Selection rule: choose claims by the story they serve, then confirm each passes the rigor gate.
Do not choose claims by which ones passed the gate.

## 3. Calibration still binds, applied the author's way

The author's discipline is to calibrate *what is claimed*, not to hedge *how it is said*.
- A result that cannot carry the claim is **left out**, not reported with its flaw attached
  (principle 8). Example: a mediation with proportion mediated above 100% and a direct effect in
  the opposite direction is not abstract-grade; omit it rather than write "suggesting confounding".
- A claim that survives is stated plainly, with one calibrated word where the design needs it
  ("suggesting", "about half", "largest measurable contributor").
- The author softens biology claims ("a tumor profile suggesting greater ICI responsiveness", the
  TMB threshold named) and keeps access claims declarative.
- Never manufacture a number to fit this voice. Magnitude words travel with a registry estimate.

## 4. The author's own edits (June draft to submitted ITSOS text)

| June draft (CRA example before 2026-10-09) | Submitted | What it teaches |
|---|---|---|
| "Pre-specified sensitivity analyses included multiple imputation, Bonferroni correction, counterfactual decomposition, and E-value analysis." | "Pre-specified analyses included multiple imputation, counterfactual decomposition and causal mediation analysis." | Methods lists moves that carry findings, not correction machinery |
| "underwent cancer-directed surgery at about half the White rate (/ [22.3%] vs / [48.0%]; adjusted odds ratio [OR], 0.50)" | "...at about half the White rate (adjusted odds ratio [OR], 0.50)" | Magnitude words carry the point, with the adjusted estimate beside them |
| "The gap localized to the recommendation step: surgery was recorded as not recommended..." | "Surgery was recorded as not recommended substantially more often for Black patients at every stage, whereas documented refusal was rare in both groups, identifying the surgical-recommendation step as the largest measurable contributor." | Result first, interpretive tail second |
| "Chemotherapy and radiation receipt were equitable." | "...were equitable, with modest adjusted differences after accounting for the higher squamous proportion among NHB patients." | Protective nuance in a trailing clause |
| "markers predicting greater responsiveness" | "a tumor profile suggesting greater ICI responsiveness, including higher TMB-High prevalence at the 16 mutations-per-megabase threshold" | Soften biology, specify the threshold |
| "...NHB patients received ICI less often than NHW patients, supporting an access-driven mechanism." | "...NHB patients received ICI less often than NHW patients." | Let the contrast speak; cut the explanatory tail |
| "...are the highest-leverage modifiable targets for narrowing the population-level survival gap." | "Equitable operability review, surgical referral, and ICI-trial inclusion of Black patients are the highest-leverage targets." | Short, concrete final lever |

## 5. Worked contrast: what the JAMA guide produced (AATS 2027 lung draft, 2026-10-08)

| Section | Flat draft | Author's architecture |
|---|---|---|
| Objective | "To compare resection of early-stage disease and overall survival between..." | Stake + uncertainty, then "We assessed whether..., and if so, whether the gap reflects patient refusal and fitness or the treatment recommendation." |
| Methods | "Model A adjusted for clinical factors, and Model B added..."; a sentence on bootstrap, permutation and leave-one-out checks | Covariates enumerated; matching, weighting, within-facility, mediation named; no plan labels, no QA machinery |
| Results | A ladder of Model A/Model B estimate pairs; reason codes, SBRT compensation, equitable modalities and the stage IV immunotherapy gap all absent | Arc S2-S7: gap, robustness range, planning step vs refusal, SBRT does not offset, postoperative chemotherapy and consolidation immunotherapy equitable, stage IV immunotherapy gap not explained by histology |
| Conclusions | Two sentences ending on a null and "support examining how operability decisions are made" | Five declarative sentences naming the driver, the modality-specific contrast and the levers |

## 6. Review

After drafting, run both reviewers in parallel and weigh their findings against each other before
editing: `cra-red-team` (over-claiming, numbers) and `cra-abstract-advocate` (under-claiming,
missing story elements, voice drift from this file). Accept a red-team softening only when the
claim truly exceeds the data; when it would delete a story element, prefer omitting the weak
result or restating the strong one plainly.
