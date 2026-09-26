# Denominators: one question, one denominator

**Rule (author directive 2026-09-25, L090).** Before computing any proportion or rate, write the
question as "Among [population], what share [event]?" and take the denominator from it. Name
that population in the table header or footnote, figure axis, slide footer, registry label and
prose. Once a denominator is chosen for a question, every table, figure, slide and sentence that
answers that question uses it. Changing it is a decision logged in `decision_log.md`, and every
artifact that used the old one is regenerated.

## Question to denominator

| Question | Denominator | Note |
|---|---|---|
| How often does each group undergo surgery? | All eligible patients in the group (e.g. stage I-III) | A rate |
| Which recorded reasons account for the surgery gap between groups? | All eligible patients | Reason-specific rates per patient; their differences add up to the gap |
| Is reason R more likely in group X than in group Y? | All eligible patients, then the analysis ladder on that denominator | A comparison of likelihood between groups |
| Among patients who were not operated on, which reasons were recorded? | Non-operated patients, within each group | A composition that sums to 100%; describe it within a group, never compare groups on it |
| Survival among resected patients | Resected patients | A conditional estimand; declare it (L039) |
| Treatment use by year | Eligible patients diagnosed that year | One denominator per year |

## The compositional trap

When groups differ in how many patients reach a subgroup, shares within that subgroup shift
mechanically. REPEAT DISPARITIES, NCDB, stage I-III esophageal cancer, Black vs White patients:

| Reason (NAACCR 1340) | Share of non-operated patients | Share of all stage I-III patients |
|---|---|---|
| Not part of planned first course (code 1) | 83.5% vs 77.4% | 64.0% vs 37.9% (+26.1 points) |
| Contraindicated by patient risk factors (code 2) | 9.8% vs 11.8% (looks lower) | 7.5% vs 5.8% (higher, RR 1.30) |
| Refused by patient or family (code 7) | 3.0% vs 5.0% (looks lower) | 2.3% vs 2.4% (similar) |

Non-operated patients were 77% of Black and 49% of White stage I-III patients, so every reason
other than code 1 looked smaller among Black non-operated patients. The surgery gap was 27.6
points (51.0% vs 23.4%), and code 1 accounted for 26.1 of them. "Black patients refused surgery
less often" was an artifact of the denominator.

## Rules

1. Print n/N beside every percentage, and name the denominator population once per table,
   figure or slide.
2. Keep Unknown categories consistently in or out of the denominator, and say which.
3. The N of a denominator equals a registered cohort or sub-cohort N (cohort-curation.md).
4. When two denominators both answer questions the audience needs, show them side by side, each
   labelled with its question. Never switch from one to the other between tables, slides or
   replies without saying so.
5. Differences between percentages are percentage points.
6. Hospital-based (NCDB) and population-based (SEER) data describe different populations; say
   which one a rate describes.
7. The registry key or label names the denominator, e.g. `reason_no_surgery.share_of_all_stageI_III`
   and `reason_no_surgery.share_of_nonoperated`.
