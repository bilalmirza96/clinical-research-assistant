# Content lessons: claims a slide can and cannot make

Each entry is a mistake that reached a draft of the gold-standard deck or its notes and had to be
walked back, sometimes hours before the talk. Check every slide and note against this list.
The analysis-level versions of these rules (denominators L090, data dictionary L089, cohort
reconciliation L088, the analysis ladder L087) live in `analyze/references/`; a slide may not
make a claim the analysis rules would not allow.

## Denominators

1. **Shares within a subgroup are compositional.** Reason-for-no-surgery shares among NON-operated
   patients sum to 100%, so when one group has more non-operated patients (mostly "not planned"),
   every other reason looks smaller. "Black patients refused less (3% vs 5% of non-operated)" was
   an artifact: among ALL patients refusal was equal (2.3% vs 2.4%) and contraindication slightly
   higher. Rule: compare *likelihood* between groups on the all-patient denominator, then confirm
   with adjusted and matched models. A within-subgroup mix may be shown, but never read across groups.
2. **Match the cohort exactly when stratifying.** A subgroup analysis must reproduce the registered
   overall estimate on the same cohort object before its strata are trusted (e.g. overall HR 1.140
   re-derived exactly), and stratum Ns plus excluded categories must equal registered denominators.
3. **Two cohorts can look like one number.** The registered survival model excluded 119 patients
   with zero follow-up; the KM display export included them. Hence a 9.9- vs 9.8-point gap.
   State which cohort a slide uses.

## Registry variables

4. **Read the data dictionary before naming a code.** NAACCR 1340 code 1 is "not part of the
   planned first course", which by rule includes a patient choosing an offered non-operative
   option. It is NOT "surgery not recommended" and NOT "not offered". Code 2 includes progression
   before planned surgery. Code 7 is refusal of a *specifically recommended* operation. Cite the
   dictionary page when challenged.
5. **Never claim who decided** when the registry cannot say. Locate the difference ("at treatment
   planning; surgery was less often part of the plan"), not the actor.
6. **Name exposures as recorded.** NCDB records "immunotherapy" without the agent; call it
   immunotherapy, not checkpoint inhibitors, even when the talk title says "ICI era".
7. **Composite categories need their real definition on the slide.** "Chemo/RT, no surgery" meant
   chemotherapy OR radiation; the note said "chemoradiation". Say what the code means.

## Measures

8. **Relative survival ≠ overall survival.** A SEER*Explorer relative-survival trend can frame the
   stake; do not compare its values with cohort OS on another slide.
9. **Keep one time horizon.** The talk's outcome was two-year survival, so the trend slide was
   switched from five-year to two-year relative survival for consistency (and its year range
   follows the series: 1975–2021).
10. **"Points", not "percent", for differences.** 40% vs 30% is a 10-point gap.
11. **OR ≠ RR.** With a common outcome, "OR 0.73" is not "27% less likely".
12. **Arithmetic on the slide must survive subtraction** (40.0 − 30.2 = 9.8, so do not print 9.9).

## Claims

13. **NCDB is hospital-based**, never "population-based" (even in notes).
14. **"Not explained by X" only if X explained nothing.** Socioeconomic adjustment moved the surgery
    OR from 0.49 to 0.60: that is "only partly explained".
15. **Mediation is an estimate under assumptions**: "mediation analysis suggests about half…".
16. **"Similar" is the honest word** for a non-significant difference with a CI touching 1
    (HR 1.08, 0.99–1.17); not "equal", not "no difference".
17. **An interaction test on a subsample is not the final answer.** A 30k-subsample race × histology
    test (P=.83) was superseded by the full-cohort test (P=.12, and P=.006 for SEER CSS).
18. **A separate treatment's share of a gap is not additive with another's**; report the joint
    share when asked "how much is treatment overall".
19. **Genomic cohorts with small minority N are hypothesis-generating** (133 Black patients, no
    PD-L1, no outcome linkage): say so.

## Talk vs abstract

20. When the final analysis revises an abstract claim, disclose once ("Since the abstract was
    submitted, we refined several analyses…") and keep a corrected-statement list in the Q&A pack.
