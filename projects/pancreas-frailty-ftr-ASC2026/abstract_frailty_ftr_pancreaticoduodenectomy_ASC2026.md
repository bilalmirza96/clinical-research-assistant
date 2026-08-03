# ASC 2026 Abstract — The Rescue Gap in Frail Older Adults Undergoing Pancreaticoduodenectomy

**Source data:** ACS-NSQIP Procedure-Targeted Pancreatectomy PUF 2020-2024, via `Tables_RescueGap.docx` and
`RescueGap_Figure_Legends.docx`. Every value below is transcribed from those files and was reconciled
programmatically against them. Nothing is estimated, rounded differently, or interpolated.

---

**Title:** The Rescue Gap: Frailty-Associated Mortality After Pancreaticoduodenectomy Reflects Failure to Rescue More Than Complication Occurrence

*Alternative (shorter):* The Rescue Gap in Frail Older Adults Undergoing Pancreaticoduodenectomy: A Causal Mediation Analysis

**Authors:** Mirza B, Khreiss M, Luu «T», Mesropyan «L», Riall TS, Jehan F

---

## Abstract body

**Introduction:** Frailty is an established predictor of mortality after pancreaticoduodenectomy, yet the mechanism underlying that excess mortality remains undefined. Frail patients may die more often because they develop more complications, or because they are less able to survive the complications they develop. Failure to rescue, defined as death following a major complication, isolates the second mechanism and reflects the management of complications rather than their incidence. We assessed whether frailty-associated mortality after pancreaticoduodenectomy is transmitted through increased complication occurrence or through failure to rescue.

**Methods:** We conducted a retrospective cohort study using the ACS-NSQIP Procedure-Targeted Pancreatectomy Participant Use File (2020-2024). Pancreaticoduodenectomy was identified by CPT code (n=24,199). Frailty was defined as a 5-item modified frailty index (mFI-5) of 2 or greater. The outcome was 30-day mortality; the mediator was any major complication; failure to rescue was death after a major complication. Natural indirect (complication) and natural direct (failure-to-rescue) effects were estimated by g-computation with an exposure by mediator interaction and 1,000 bootstrap replications, adjusted for age, sex, self-reported race and ethnicity, body mass index, American Society of Anesthesiologists class, albumin, bilirubin, preoperative sepsis, disseminated cancer, and operative year. A four-way decomposition and E-values were computed; the primary analysis was prespecified in adults 65 years or older.

**Results:** Among 24,199 patients, 5,680 (23.5%) were frail, 9,538 (39.4%) developed a major complication, and 431 (1.78%) died within 30 days, with failure to rescue in 4.3%. Across the frailty gradient, major complications rose modestly (36.2%, 39.8%, and 44.0% for mFI-5 of 0, 1, and 2 or greater) while failure to rescue rose disproportionately (3.1%, 4.8%, and 5.1%). In the primary analysis among adults 65 years or older (n=14,759; 333 deaths), frailty increased 30-day mortality by 0.61 percentage points (pp) (95% CI, 0.11 to 1.16; total-effect OR 1.29, 95% CI 1.04-1.63; E-value 1.91). Despite the higher complication burden among frail patients, only 32% of this excess mortality was transmitted through complication occurrence (natural indirect effect, 0.20 pp; 95% CI, 0.11 to 0.30), with the remaining 68% acting directly (natural direct effect, 0.42 pp; 95% CI, -0.06 to 0.92). Four-way decomposition confirmed a dominant controlled direct effect (0.378 pp; 95% CI, 0.110 to 0.711) alongside a smaller pure indirect effect (0.195 pp; 95% CI, 0.110 to 0.284), with null reference and mediated interactions. Frail patients also died more often from the same complication, with higher case-fatality across nearly every complication type, including organ or space surgical site infection (4.0% vs 2.8%) and reoperation (13.0% vs 11.2%). When isolated transfusion was excluded from the complication composite, 97% of the frailty effect acted through the direct pathway (0.57 pp; 95% CI, 0.03 to 1.12). Frailty conferred no measurable mortality effect among patients younger than 65 years (-0.05 pp; 95% CI, -0.56 to 0.59; OR 0.97, 95% CI 0.52-1.67).

**Conclusions:** Among older adults undergoing pancreaticoduodenectomy, the excess mortality associated with frailty was attributable less to the occurrence of complications than to a diminished capacity to survive them, and this rescue gap was confined to patients 65 years or older. Most of the frailty-associated mortality would persist even if complication occurrence were held constant, indicating that prevention alone is unlikely to close it. These findings support pairing preoperative frailty screening with structured rescue pathways, including early recognition of deterioration and prespecified escalation-of-care triggers, for older frail patients in whom a complication is far more likely to prove fatal.

---

## Measured section weights

| Section | Characters |
|---|---|
| Introduction | 653 |
| Methods | 923 |
| Results | 1,660 |
| Conclusions | 718 |
| **Total body** | **3,954** |

Results / Methods = 1.80 · Results / Conclusions = 2.31 · Prior ASC submission (CR-POPF) = 3,873 characters.

---

## 12-Point Gate

| # | Gate question | Status | Note |
|---|---|---|---|
| 1 | One story or two? | ✓ | Single arc: complication occurrence vs failure to rescue |
| 2 | Falsification arc | ✓ | Candidate mechanism (complication burden) tested and largely fails; alternative (rescue failure) carries the effect. Named in Introduction, Results, and Conclusions |
| 3 | Calibrated language | ✓ | "reflects", "attributable less to", "supports". No "drives", "predicts", "proves". Age qualifier carried throughout |
| 4 | Race terminology | ✓ | "self-reported race and ethnicity" in Methods; NSQIP categories; no ancestry vocabulary |
| 5 | Audience calibration | ✓ | Clinician-outcomes register; estimands named (NIE, NDE, CDE, PIE); E-value retained |
| 6 | Section weight | ⚠ **accepted exception** | Results 2.31× Conclusions ✓, but 1.80× Methods (target 2.0). Closing the gap requires deleting the covariate enumeration, which house style mandates and which a mediation design needs for interpretability. Documented rather than fixed |
| 7 | Therapeutic implications | ✓ | "support pairing screening with rescue pathways" — care-pathway rationale, not treatment-response prediction |
| 8 | Confounders absent from abstract | ✓ | Unmeasured confounding represented only by the E-value; see Q&A prep |
| 9 | Honesty over impact | ✓ | NDE confidence interval (-0.06 to 0.92) printed rather than hidden; null in patients <65 reported in line with positives |
| 10 | Compliance | ⚠ | Four bolded headers ✓; absolute numbers with percentages ✓; no em dashes ✓; no institution or product names ✓. **Character limit unconfirmed** |
| 11 | Four-criterion rigor | ✓ | Every abstract-grade estimate carries a bootstrap 95% CI excluding the null, except the NDE, which is explicitly reported as crossing it |
| 12 | Prose over bullets | ✓ | No bullets in body |

---

## Open items before submission

1. **Table 3 column header contradicts its own footnote.** The header reads "Case-fatality, frail vs non-frail, %" while the footnote reads "The final column shows non-frail / frail case-fatality." These specify opposite orders. The footnote is the correct one: in most rows the second value is higher, and Figure 4 independently states that frailty shifts lethality upward for nearly every complication. The abstract's case-fatality sentence follows the footnote reading. **Fix the header before submission**, and re-check the two quoted pairs (organ/space SSI 4.0 vs 2.8; reoperation 13.0 vs 11.2) once corrected.

2. **The natural direct effect crosses the null** (0.42 pp; 95% CI, -0.06 to 0.92). This is the abstract's most exposed point and a discussant will find it. The abstract prints the interval and rests the significance claim on two estimates that do exclude the null: the controlled direct effect (0.378 pp; 0.110 to 0.711) and the transfusion-excluded sensitivity analysis (0.57 pp; 0.03 to 1.12). Q&A framing: the complication pathway is small and precisely estimated, the direct pathway is large but less precisely estimated, and every specification places the majority of the effect outside complication occurrence.

3. **Confirm the venue and its character limit.** Written for Academic Surgical Congress at 3,954 characters against a prior 3,873-character ASC submission. If a trim is needed, take it from Methods (compress the covariate list, roughly 200 characters) before touching Results.

4. **Confirm author details**: first initials for Luu and Mesropyan, and the shared affiliation for the title block.

5. **E-value is 1.91**, which is modest. Defensible for a registry mediation analysis and reported transparently, but worth having a prepared answer on residual confounding by unmeasured physiologic reserve.
