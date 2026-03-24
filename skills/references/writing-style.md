# Author Writing Style Reference

This file defines the author's unique writing voice. All writing skills (`/write-introduction`, `/write-methods-results`, `/write-discussion`, `/write-manuscript`) MUST read and apply these patterns when drafting manuscript text. The goal is prose that reads as human-written, matches the author's published style, and avoids generic AI phrasing.

---

## 1. Sentence Architecture

### Results sentences
Short. Single-purpose. Front-load the subject and finding, then attach statistics parenthetically at the end. The claim and the evidence live in one unit — never write a separate sentence just for the numbers.

**Do this:**
> Hispanic patients presented with statistically higher rates of HER2-positive gastric cancer compared with non-Hispanic White patients (13.9% vs 9.8%; adjusted OR, 1.48; 95% CI, 1.12–1.96; P < .001).

**Not this:**
> We found that Hispanic patients had higher rates of HER2-positive gastric cancer. The adjusted odds ratio was 1.48 (95% CI, 1.12–1.96), and this was statistically significant (P < .001).

### Discussion sentences
Longer and more compound. Chain ideas with dashes and commas. Weave mechanism, classification, and implication into single complex sentences when the logic demands it.

**Do this:**
> These findings align with the established molecular subtyping of gastric adenocarcinoma — the TCGA classification identifies four subtypes: Epstein-Barr virus-positive, microsatellite-unstable, genomically stable, and chromosomal instability — and suggest that the chromosomal instability subtype, which harbors ERBB2 amplification, may be disproportionately represented in Hispanic populations.

---

## 2. Natural Frequency Anchoring

Translate the most important percentages into "1 in every X" phrasing. Use this selectively — for cohort composition, the key finding prevalence, and critical subgroup prevalence. Not on every number.

**Do this:**
> Approximately 1 in every 7 Hispanic patients harbored a HER2-positive tumor.

**Not this:**
> The prevalence of HER2-positive tumors among Hispanic patients was 13.9%.

Use both forms when introducing the number for the first time — the anchored phrasing makes it memorable, the percentage makes it precise.

---

## 3. Statistical Layering

Present findings in this specific build-up order. Do not jump straight to the final adjusted model. Build credibility incrementally:

1. Raw group percentages
2. P value (unadjusted comparison)
3. FDR q-value (if multiple comparisons were corrected)
4. Adjusted OR/HR with CI and P

Each layer adds rigor. The reader sees the raw signal first, then the corrected and adjusted confirmation.

---

## 4. Hedging Pattern

**Data findings** — state directly, no hedging:
> Hispanic patients presented with statistically higher rates of HER2-positive gastric cancer.

**Interpretive claims** — hedge consistently:
> These findings suggest that ancestry-linked genomic variation may influence HER2 amplification patterns.
> This association supports a hypothesis that ERBB2 signaling pathways may be differentially activated.
> The observed disparity may reflect a potential interaction between genetic predisposition and environmental exposure.

Hedge words: "suggest," "may," "support a hypothesis," "potential," "appears to," "is consistent with."

Hedge density by section:
- Abstract opening: zero hedging
- Results: near-zero hedging
- Discussion: high hedging on all interpretive claims
- Conclusion: moderate hedging

---

## 5. Group Comparison Format

When comparing across groups, use this consistent inline format:

> (Hispanic: 13.9% vs 9.8% non-Hispanic White, 8.1% non-Hispanic Asian, and 11.0% non-Hispanic Black; P < .001)

Rules:
- Index group comes first, followed by a colon
- "vs" separates the index group value from the comparators
- Comparators listed by full group name
- Semicolon before the P value
- All in one parenthetical unit

---

## 6. Discussion Arc

Move through this specific chain within Discussion paragraphs. Each step builds on the last:

1. **Restate finding in clinical terms** — not statistical terms
2. **Connect to a biological mechanism by name** — cite the pathway (H. pylori, ERBB2 signaling, chromosomal instability)
3. **Map onto an established classification system** — name it and define it inline (e.g., "the TCGA classification identifies four molecular subtypes: ...")
4. **Pivot to therapeutic actionability** — name specific drugs, their FDA status, and the clinical implications

Do not leave the discussion at the level of statistical association. Always push toward mechanism and therapy.

---

## 7. Limitations as Arguments

Each limitation raised must immediately become a recommendation. Do not list weaknesses passively — use them to argue for more diverse cohorts, ancestry-based analyses, and inclusive clinical trials.

**Do this:**
> The absence of germline sequencing data precludes assessment of inherited ERBB2 variants. Future studies should incorporate whole-genome or whole-exome sequencing in diverse populations to disentangle somatic from germline contributions to the observed disparity.

**Not this:**
> A limitation of this study is that germline data were not available.

The limitations paragraph should be the longest paragraph in the Discussion.

---

## 8. Funnel Structure

### Introduction — narrows:
Overall incidence trends → disparity in a specific population → gap in genomic profiling → study objective

### Discussion — widens back out:
Specific finding → mechanism → classification → therapy → policy

These are mirror images of each other.

---

## 9. Transition Devices

**Use these:**
- "Indeed,"
- "Together with,"
- "Notably,"
- "Consistent with these reports,"
- "Nevertheless,"
- "As such,"

**Never use these:**
- "Furthermore,"
- "Moreover,"
- "Additionally,"
- "It is worth noting that"
- "It is important to note that"
- "Interestingly,"

---

## 10. Naming Specificity

Name everything. Be maximally specific. Never use vague placeholders when a proper name exists.

**Do this:**
- "the AACR Project GENIE Consortium (v15.0)"
- "fam-trastuzumab deruxtecan-nxki (Enhertu; Daiichi Sankyo/AstraZeneca)"
- "R version 4.3.1 (R Foundation for Statistical Computing)"
- "the Benjamini-Hochberg procedure for false discovery rate correction"
- "the OncoKB and ClinVar databases"

**Not this:**
- "a large multi-institutional consortium"
- "a novel antibody-drug conjugate"
- "using R software"
- "after correction for multiple comparisons"
- "publicly available variant databases"

---

## 11. Equity Framing

Use "equitable access," "disproportionate burden," and "critical need" as recurring anchors throughout the manuscript. This language appears in the Abstract, the Discussion, and the Conclusion — bookending the manuscript.

Rules:
- Always tie equity language to a specific data point — never freestanding
- Assertive but evidence-based
- Integrated naturally, not performative

**Do this:**
> The disproportionate burden of HER2-positive gastric cancer among Hispanic patients (13.9% vs 9.8% non-Hispanic White; P < .001) underscores the critical need for equitable access to HER2-targeted therapies, including fam-trastuzumab deruxtecan-nxki, in this population.

**Not this:**
> Health equity is important and more research is needed to address disparities.

---

## 12. Abstract Structure

Open the Abstract with the finding and effect size before any background. The last sentence names a specific therapy. It reads like a conclusion you would say out loud, not a generic "further research is warranted."

**Do this (opening):**
> Hispanic patients with gastric adenocarcinoma harbored HER2-positive tumors at significantly higher rates than non-Hispanic White patients (13.9% vs 9.8%; adjusted OR, 1.48; P < .001).

**Do this (closing):**
> These findings support prioritizing enrollment of Hispanic patients in clinical trials of fam-trastuzumab deruxtecan-nxki and other HER2-targeted agents.

**Not this (closing):**
> Further research is warranted to investigate these disparities.

---

## 13. Voice and Person

- **Introduction and Methods:** active voice, first person plural ("We assessed," "We compared," "We included")
- **Results:** shift to third person ("Hispanic patients had," "The cohort comprised," "Rates were higher")
- **Discussion:** back to first person ("We further analyzed," "Our findings suggest," "We observed")
- **Passive voice** only in Methods where the agent does not matter ("Variants and frequencies were calculated," "Missing data were handled using")

---

## 14. Words and Phrases to Avoid

Never use these — they are AI-tell phrases that make prose sound generated:

- "delve into"
- "it's important to note"
- "it's worth noting"
- "a myriad of"
- "shed light on"
- "pave the way"
- "in the realm of"
- "a testament to"
- "the landscape of"
- "underscores the importance"
- "robust" (when describing results generically)
- "novel" (unless the finding is genuinely first-in-literature)
- "comprehensive" (unless describing a genuinely exhaustive analysis)
- "leveraging" (use "using")
- "utilizing" (use "using")
- "facilitating" (use "enabling" or rephrase)
- "noteworthy" (use "notable" or rephrase)
- "pivotal" (use "critical" or rephrase)

---

## 15. Application Rules for All Writing Skills

1. **Read this file before drafting any manuscript text.** Every writing skill must apply these patterns.
2. **Match section-specific voice** — Results sentences are short and direct; Discussion sentences are long and compound.
3. **Use the author's transition words** — draw from the approved list, never from the banned list.
4. **Apply natural frequency anchoring** on the 2-3 most important numbers per section.
5. **Layer statistics** in the prescribed order — do not skip to the adjusted model.
6. **Name everything** — databases, drugs, methods, software versions.
7. **Push Discussion beyond association** — always reach mechanism, classification, and therapy.
8. **Frame limitations as recommendations** — each weakness argues for a specific future study.
9. **Tie equity language to data** — never use it as freestanding rhetoric.
10. **Avoid all AI-tell phrases** listed in Section 14.
