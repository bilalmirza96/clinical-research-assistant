# Story arc, presenter notes, conclusions and Q&A

The deck tells ONE story; every slide answers the question the previous slide raised. The notes
are what the presenter says, word for word, in that order.

---

## 1. The arc (7-minute podium talk, ~18 slides)

Read each row as "the question this slide answers → the slide". Adapt the nouns to the study.

| Beat | Question the slide answers | Typical slide |
|---|---|---|
| Stake | Why does this matter? | Trend over decades (same time horizon as the results) |
| Question | What exactly are we asking? | Stated in the stake slide's note ("Our question was whether…") |
| Data | Where does the answer come from? | Data-sources table |
| Method | How will we compare fairly? | Analytic-approach ladder |
| Headline | Is there a gap? | KM / absolute difference |
| Robustness | Does it survive adjustment and matching, in a second registry? | Estimator forest |
| Where | Where is it largest? | By-stage bars |
| Why (treatment) | Is it a difference in treatment? | Bars + forest per modality |
| Why (biology) | Could biology explain it? | Genomics bars |
| Mechanism | Which treatment step? | Surgery bars + forest, stage-stratified |
| Reasons | Why was the step missed? | Stacked reason codes |
| Instead | What happened instead? | Stacked modality mix |
| Counterfactual | What if they got it? | Outcome among those treated (single KM) |
| Quantify | How much of the gap runs through it? | Mediation |
| Humility | Could unmeasured factors explain it? | E-value |
| Close | What should the room remember? | Three modest conclusions |

Cut a slide before shrinking type. Anything reviewer-facing (calipers, FDR, weighting variants,
all-patient denominators) becomes a **hidden backup slide** at the end.

## 2. Notes: the contract

Each note is 20–100 words, 1–3 short paragraphs separated by a blank line, and follows this shape:

1. **Hand-off sentence** that answers the previous slide's open question or poses this slide's.
2. **The finding**, stated plainly with rounded numbers.
3. **Optional** replication or caveat sentence ("The same gradient was replicated independently in
   SEER for cancer-specific survival.").

Budget: ~130 words per minute. A 7-minute talk carries 800–950 words of notes; `deck_lint.py
--minutes 7` reports the total.

### Numbers in notes

- Whole-number percentages: "30% compared with 40%", never "30.2%".
- A difference between two percentages is **percentage points**: "about 10 percentage points".
- Hazard and odds ratios may keep two decimals, or be spoken ("about a quarter lower odds").
- An odds ratio is not a risk ratio: "OR 0.73" is "about a quarter lower odds", not "27% less
  likely", especially when the outcome is common.
- Adjusted gaps on one slide and unadjusted gaps on another will both be quoted: know which is
  which, and say "adjusted" when it is.

### Words

- Transitions: vary them. "We then asked…", "To understand why…", "To quantify this…", "Having
  observed…", "Among patients who…". Do not open three notes with "next".
- Never open with Furthermore / Moreover / Additionally / Interestingly (house voice ban).
- Name the analyses in plain language: "clinical factors", "socioeconomic factors", "propensity
  matched"; never "Model A / Model B" aloud.
- Say "the difference in surgery" or "underwent surgery", not "receipt of surgery".
- Do not call a disease or stage "most curable"; say "a stage where surgical resection is the
  primary treatment".
- NCDB is hospital-based. SEER is population-based. Say so if you describe either.
- When the registry cannot identify the agent, name the exposure the registry records
  ("immunotherapy"), not the drug class the talk title uses.
- Replication line: "This was independently validated in SEER" is allowed when SEER is not shown.

## 3. Conclusions (the modesty contract)

Three numbered conclusions, each one sentence, each true of a slide the audience saw:

1. The descriptive headline ("Survival has improved over five decades, but the gains have not been
   shared equally").
2. The mechanism, with the exposures the data actually test ("…about half as likely to undergo
   surgery at every stage, not accounted for by documented refusal or contraindication, and only
   partly by hospital or socioeconomic factors; in stage IV disease, less likely to receive
   immunotherapy").
3. The quantified link, framed as an estimate, and the next step, framed as a question
   ("Mediation analysis suggests about half of the survival gap is explained by the difference in
   surgery; understanding why surgery is less often part of the treatment plan is the next step").

Rules:
- No claim of **who** decided when the data cannot say (registry reason codes mix clinician
  recommendation with patient choice).
- "Not explained by X" only when X was tested and explained essentially none of it; otherwise
  "only partly by X".
- "Mediated / explained by" is an estimate: "mediation analysis suggests…".
- Refusal/contraindication statements apply only to the treatment they were measured for.

## 4. When the talk differs from the submitted abstract

Re-analysis between submission and podium is normal. Add ONE sentence early (end of the methods
slide note): "Since the abstract was submitted, we refined several analyses; the results today
reflect the final analysis." Prepare a one-line answer for each changed claim.

## 5. Discussant and audience Q&A pack

Deliverable: `Presentations/<venue>/qa_prep_<date>.md`, answered from the registry only.

- **Order**: answer the discussant's questions in the order received.
- **Shape**: 2–4 spoken sentences per answer: direct answer first, one supporting number
  (adjusted or matched, labelled as such), one honest limit.
- **Numbers**: adjusted and propensity-matched estimates only, labelled "adjusted" / "matched";
  never a crude number in a defence.
- **Tiers**: basic (registries, definitions, why two years), intermediate (comorbidity, histology,
  hospital type, era), complex (who decided, selection among the operated, mediation assumptions,
  what to change in practice), plus the fallback: "That's a great question. We didn't examine that
  directly, and it would be a good next step."
- **Corrections**: if a pre-sent email or abstract said something the final analysis revised, list
  the corrected statement in the pack so the presenter can say "on further review…".
