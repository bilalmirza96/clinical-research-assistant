# ASC 2026 Abstract — Frailty, Complications, and the Rescue Pathway After Pancreaticoduodenectomy

**Source data:** ACS-NSQIP Procedure-Targeted Pancreatectomy PUF 2020-2024, via `Tables_RescueGap.docx` and
`RescueGap_Figure_Legends.docx`. Every value is transcribed from those files and reconciled programmatically.

**Version 2.** Supersedes v1. The revision is substantive, not cosmetic: v1 rested on a claim the data
only partly support. See "What changed and why" below.

---

**Title:** Complication Prevention Alone Will Not Close the Frailty Mortality Gap After Pancreaticoduodenectomy: A Causal Mediation Analysis of the Rescue Pathway

*Alternative (retains project branding):* The Rescue Gap in Frail Older Adults Undergoing Pancreaticoduodenectomy: A Causal Mediation Analysis

**Authors:** Mirza B, Khreiss M, Luu «T», Mesropyan «L», Riall TS, Jehan F

---

## Abstract body

**Introduction:** Frailty is an established predictor of death after pancreaticoduodenectomy, and quality improvement has responded largely by targeting complication prevention. Whether that strategy can close the frailty mortality gap depends on an unresolved question: do frail patients die because they develop more complications, or because they are less likely to survive the complications they develop? Failure to rescue, defined as death after a major complication, isolates the second pathway. We decomposed frailty-associated mortality after pancreaticoduodenectomy into the complication pathway and the rescue pathway to determine which carries the effect.

**Methods:** We analyzed the ACS-NSQIP Procedure-Targeted Pancreatectomy Participant Use File (2020-2024). Pancreaticoduodenectomy was identified by CPT code (n=24,199). Frailty was defined as a 5-item modified frailty index (mFI-5) of 2 or greater. The outcome was 30-day mortality and the mediator any major complication; failure to rescue was death after a major complication. Effects were decomposed into natural indirect (complication) and natural direct (rescue) components by g-computation with an exposure by mediator interaction and 1,000 bootstrap replications, adjusted for age, sex, self-reported race and ethnicity, body mass index, American Society of Anesthesiologists class, albumin, bilirubin, preoperative sepsis, disseminated cancer, and operative year. A four-way decomposition and E-values were computed; the primary analysis was prespecified in adults 65 years or older.

**Results:** Among 24,199 patients, 5,680 (23.5%) were frail, 9,538 (39.4%) developed a major complication, and 431 (1.78%) died within 30 days. Across the frailty gradient, major complications rose by 22% in relative terms (36.2%, 39.8%, and 44.0% for mFI-5 of 0, 1, and 2 or greater) while failure to rescue rose by 65% (3.1%, 4.8%, and 5.1%). In the primary analysis among adults 65 years or older (n=14,759; 333 deaths), frail patients both developed more complications (44.9% vs 38.7%) and were less often rescued from them (5.8% vs 5.0%); frailty increased 30-day mortality by 0.61 percentage points (pp) (95% CI, 0.11 to 1.16; total-effect OR 1.29, 95% CI 1.04-1.63; E-value 1.91). Despite the higher complication burden, only 32% of this excess mortality was transmitted through complication occurrence (natural indirect effect, 0.20 pp; 95% CI, 0.11 to 0.30); the remaining 68% acted directly (natural direct effect, 0.42 pp; 95% CI, -0.06 to 0.92). Four-way decomposition localized the effect to a controlled direct effect of 0.378 pp (95% CI, 0.110 to 0.711) with a smaller pure indirect effect (0.195 pp; 95% CI, 0.110 to 0.284) and null reference and mediated interactions, indicating that frailty and complications acted additively rather than synergistically. Frail patients died more often from the same complication, including organ or space surgical site infection (4.0% vs 2.8%), which affected 17.8% of the cohort, and reoperation (13.0% vs 11.2%). Excluding isolated transfusion from the composite, 97% of the effect acted directly (0.57 pp; 95% CI, 0.03 to 1.12). Frailty conferred no measurable mortality effect below age 65 (-0.05 pp; 95% CI, -0.56 to 0.59).

**Conclusions:** Among older adults undergoing pancreaticoduodenectomy, most of the mortality associated with frailty did not flow through the occurrence of complications and persisted when complication occurrence was held constant. Complication prevention alone is therefore unlikely to close the frailty mortality gap, which was confined to patients 65 years or older. These findings support pairing preoperative frailty screening with rescue-directed care in older frail patients: a lower threshold for cross-sectional imaging and source control when intra-abdominal infection is suspected, and earlier critical-care transfer for respiratory deterioration, which carried a case-fatality above 30%.

---

## Measured section weights

| Section | v1 | v2 |
|---|---|---|
| Introduction | 653 | 666 |
| Methods | 923 | 892 |
| Results | 1,660 | 1,682 |
| Conclusions | 718 | 700 |
| **Total body** | **3,954** | **3,940** |

v2: Results / Methods = 1.89 (was 1.80) · Results / Conclusions = 2.40 (was 2.31) · Prior ASC submission = 3,873.

---

## What changed and why

### 1. The central claim was overstated, and a discussant would have caught it

v1 asserted that failure to rescue "rose disproportionately." That holds across the mFI-5 gradient (complications
+22% relative, failure to rescue +65%), but **it does not hold in the primary population**. Among adults 65 or
older, frail versus non-frail complications rose 38.7% to 44.9% and failure to rescue rose 5.0% to 5.8%: both
exactly +16% in relative terms. The disproportionality disappears in precisely the stratum the primary analysis
is built on.

v2 reports both contrasts explicitly and stops leaning on the word "disproportionate" as the load-bearing claim.

### 2. The interaction terms point somewhere subtler than "frail patients are rescued worse"

The frailty by complication interaction is **negative** on the log-odds scale (β = -1.26) and **null** on the
additive scale (reference interaction +0.038, 95% CI -0.462 to +0.522; mediated interaction +0.004, 95% CI
-0.051 to +0.051). There is no synergy: frailty does not amplify the lethality of a complication in the way
"failure to rescue" colloquially implies.

The dominant component is the controlled direct effect, defined in your own Table 5 as death from causes
*other than* the measured complication pathway, with complications held absent. That is a stronger and cleaner
finding than a rescue gap: **frail patients die more even when complication occurrence is held constant.**

Note that the Figure S2 legend states the negative interaction "indicates that the rescue disadvantage, not
additional complication burden, drives the gap." A negative multiplicative interaction does not support that
reading. Consider revising the legend before submission.

v2 reframes the spine around what the decomposition actually shows, reports the null interactions as a positive
feature (a clean additive decomposition), and lets the conclusion follow: prevention alone cannot close this gap.

### 3. The clinical lever was generic

v1 ended on "early recognition of deterioration and prespecified escalation-of-care triggers," which is the kind
of sentence any frailty abstract could end on. v2 names two specific targets drawn from Table 3: intra-abdominal
infection (organ or space surgical site infection, 17.8% of the cohort, case-fatality 4.0% vs 2.8%) and
respiratory deterioration (unplanned reintubation, case-fatality 33.0% overall and 34.3% in frail patients).

### 4. Smaller fixes

- Opening now states the stake (prevention-focused quality improvement) before posing the two-alternative question.
- The primary-stratum complication and failure-to-rescue rates (44.9% vs 38.7%; 5.8% vs 5.0%) were absent from v1 and are now reported. A reviewer would have asked for them.
- Title changed to state the implication rather than the label; the old title is retained as an alternative.
- Methods tightened by 31 characters, improving Results / Methods from 1.80 to 1.89.
- One overreach removed: organ or space surgical site infection was nearly called the most common serious complication, but bleeding/transfusion is more frequent (18.0% vs 17.8%). Now stated as an exact frequency.

---

## 12-Point Gate (v2)

| # | Gate question | Status | Note |
|---|---|---|---|
| 1 | One story or two? | ✓ | Single arc: which pathway carries frailty's mortality effect |
| 2 | Falsification arc | ✓ | Candidate mechanism (complication burden) tested and largely fails; named in Introduction, Results, Conclusions |
| 3 | Calibrated language | ✓ | "did not flow through", "unlikely to close", "support". No "drives", "predicts", "proves" |
| 4 | Race terminology | ✓ | "self-reported race and ethnicity" in Methods; NSQIP categories |
| 5 | Audience calibration | ✓ | Clinician-outcomes register; estimands named; E-value retained |
| 6 | Section weight | ⚠ accepted exception | Results 2.40× Conclusions ✓, 1.89× Methods (target 2.0). Binding constraint is the covariate enumeration, which house style mandates and a mediation design needs |
| 7 | Therapeutic implications | ✓ | Care-pathway rationale, not treatment-response prediction |
| 8 | Confounders absent | ✓ | Unmeasured confounding represented only by the E-value |
| 9 | Honesty over impact | ✓ | NDE interval printed; null interactions reported; the age <65 null reported; the disproportionality claim narrowed |
| 10 | Compliance | ⚠ | Headers, absolute numbers, no em dashes, no institutions all ✓. **Character limit unconfirmed** |
| 11 | Four-criterion rigor | ✓ | Every abstract-grade estimate carries a bootstrap CI excluding the null except the NDE, which is explicitly reported as crossing it |
| 12 | Prose over bullets | ✓ | |

---

## Open items before submission

1. **Table 3 header contradicts its footnote.** Header says "frail vs non-frail"; footnote says "non-frail / frail". The footnote is correct (Figure 4 confirms the direction independently). Fix the header, then re-check the quoted pairs.
2. **Figure S2 legend over-reads the negative interaction** (see §2 above). Revise.
3. **The natural direct effect crosses the null** (-0.06 to 0.92). v2 prints the interval and rests significance on the controlled direct effect (0.378; 0.110 to 0.711) and the transfusion-excluded analysis (0.57; 0.03 to 1.12), both of which exclude it.
4. **Confirm venue and character limit.** 3,940 characters against a 3,873-character prior ASC submission. If trimming, take it from the Methods covariate list first.
5. **Confirm author details**: first initials for Luu and Mesropyan; affiliation.
6. **E-value 1.91** is modest. Have an answer ready on residual confounding by unmeasured physiologic reserve, which is the obvious competing explanation for a dominant controlled direct effect.
