# Manuscript QC Checks — Complete Reference

## Table of Contents
1. Numbers Consistency
2. Abstract vs. Manuscript Concordance
3. Methods-Results Alignment
4. Table Quality
5. Figure Quality
6. Statistical Rigor
7. Reference Accuracy
8. Language, Grammar & Style
9. Limitations Assessment
10. Ethical & Reporting Standards
11. Journal-Specific Formatting
12. Logical Flow and Argument Strength
13. Audit-Step Tagging and Traceability  *(per L038)*
14. Introduction ↔ Results Structural Symmetry  *(per L047)*

---

## Check 1 — Numbers Consistency

This is the #1 reason manuscripts get desk-rejected.

- Verify total N in the abstract matches total N in methods, results, every table header, and flow diagram.
- For every subgroup reported in text, verify n matches the corresponding table cell.
- Recalculate every percentage from its numerator and denominator. Flag any off by >0.5%.
- Verify percentages within each categorical variable sum to 100% (±1% for rounding).
- Verify sum of subgroups equals reported total everywhere subgroups are presented.
- In flow diagrams: verify total minus each exclusion step equals the next step, and final cohort number is correct.
- Verify median, IQR, and range values in text match corresponding table values exactly.
- Verify every p-value reported in text matches the corresponding p-value in the table.
- Verify CIs are formatted consistently throughout (pick up format from first instance, flag deviations).
- Verify HR, OR, RR and their CIs use consistent decimal places throughout.
- If a result is described as "significant," verify p < 0.05. If "not significant," verify p ≥ 0.05. If "trend," verify 0.05 ≤ p < 0.10.
- If survival analysis is reported, verify number of events is stated and consistent with KM curves and Cox models.

---

## Check 2 — Abstract vs. Manuscript Concordance

- Verify every number in the abstract appears identically in the results section.
- Verify study design in the abstract matches the methods section.
- Verify conclusion in the abstract matches conclusion in the discussion.
- Verify primary and secondary outcomes stated in the abstract are consistent with those defined in the methods.
- Verify sample size in the abstract is correct.
- Verify key statistical results (proportions, p-values, ORs, HRs, CIs) are identical between abstract and results.
- Flag any finding in the abstract not present in the main text.
- Flag any major finding in the main text arguably missing from the abstract.

---

## Check 3 — Methods-Results Alignment

- Extract a list of every analysis described or promised in the methods section.
- For each, confirm a corresponding result in the results section, a table, or a figure.
- Flag any method described but not reported (missing result).
- Extract a list of every result or statistical test reported in the results section.
- For each, confirm a corresponding description in the methods section.
- Flag any result reported without a corresponding method (orphan result).
- Verify specific statistical tests named in methods match tests actually referenced in results and table footnotes.
- Verify inclusion/exclusion criteria stated in methods match the flow diagram exactly.
- If sensitivity analysis, subgroup analysis, or secondary analysis is mentioned in methods, verify it appears in results.

---

## Check 4 — Table Quality

For each table:

- Verify title accurately and completely describes content.
- Verify every variable is labeled clearly and unambiguously.
- Verify units specified for all continuous variables (years, days, months, cm, mm, mL, g/dL, U/L).
- Verify all levels of each categorical variable are shown (no unexplained "other" or missing levels).
- Verify stratification variable is clearly identified in column headers.
- Verify total N stated in each column header.
- Verify statistical test for each comparison is stated (footnote or dedicated column).
- Verify p-values use appropriate precision: 3 decimal places, or "< 0.001" for very small values. Flag "p = 0.000" (should be "< 0.001"). Flag "p = NS" without numeric value.
- Verify missing data counts or rates reported for each variable.
- Verify bold/asterisk significance formatting matches footnote definition.
- Verify footnote defines all abbreviations used in the table.
- Verify formatting consistency: all medians in same format ("median (IQR)" or "median [range]") — flag mixed formats.
- Flag raw analysis output artifacts (R/Python column names, "NA", "NaN", "Inf", "NULL", "TRUE/FALSE").
- Verify column alignment and spacing are publication-ready.

---

## Check 5 — Figure Quality

For each figure:

- Verify title accurately describes content.
- Verify all axes labeled with variable names and units.
- Verify legend is complete, accurate, and matches figure content.
- For KM curves: verify number-at-risk table is present below, y-axis labeled "Survival Probability" (not "Survival Rate"), x-axis unit correct (months or years), curves distinguishable, censoring marks shown.
- For bar charts: verify error bars defined in legend or caption (95% CI, SD, SEM, IQR), categories labeled.
- For forest plots: verify reference line at OR/HR = 1, CIs shown, point estimates and numeric values displayed.
- For flow diagrams: verify all numbers add up at each branch point.
- Verify font size legible at printed figure dimensions.
- Verify colors distinguishable in grayscale (if journal prints in B&W).
- Verify figures referenced in text in order (Figure 1 before Figure 2).

---

## Check 6 — Statistical Rigor

- Verify primary outcome clearly defined with unambiguous, pre-specified definition.
- If logistic regression or Cox regression used, count events (not total N) and divide by number of predictors. Flag if <10 events per predictor.
- Verify correct test selection:
  - Fisher's exact (not chi-square) when any expected cell count < 5
  - Non-parametric tests (Wilcoxon, Mann-Whitney, Kruskal-Wallis) for non-normal distributions or small samples
  - Log-rank for unadjusted survival comparisons
  - Paired tests for paired data
- Verify CIs reported alongside p-values for all key results.
- If >5 secondary outcomes or comparisons tested, flag whether multiple comparison correction was considered (Bonferroni, FDR, Holm).
- If Cox regression used, verify proportional hazards assumption mentioned and tested (Schoenfeld residuals or log-log plots).
- If logistic regression used, verify model fit assessed (Hosmer-Lemeshow, C-statistic/AUC).
- Verify results with small N or low event counts labeled "exploratory" or "hypothesis-generating."
- Verify correct language: "no statistically significant difference" not "no difference." "Not significant" not "negative."
- Verify tests are two-sided (or one-sided is justified).
- Verify alpha level stated (typically 0.05).
- If propensity matching/weighting used, verify balance assessment reported (SMD < 0.1).
- If multiple imputation used, verify number of imputations, imputation model, and pooling method stated.
- If subgroup analyses performed, verify they are pre-specified or labeled as post-hoc.
- Flag any interaction test that is missing when subgroup effects are claimed.

---

## Check 7 — Reference Accuracy

- Verify every in-text citation has corresponding entry in reference list.
- Verify every reference list entry has at least one in-text citation. Flag uncited references.
- Verify references numbered in order of first appearance (numbered styles) or alphabetized (author-year styles).
- Spot-check at least 5 references: does the claim in text actually appear in the cited source? Flag potential mis-attributions.
- Verify landmark trial citations are correct (trial name, first author, journal, year).
- Verify all references formatted consistently per a single citation style.
- Flag any potentially retracted reference.
- Flag preprints not identified as such.
- Flag any reference >10 years old used to support a claim about current practice (may need updating).
- Verify "et al." usage is consistent (after 3 or 6 authors depending on style).

---

## Check 8 — Language, Grammar & Style

- Complete grammar and syntax check. Flag run-on sentences, subject-verb disagreement, dangling modifiers, misplaced commas.
- Verify consistent tense:
  - Methods and results: past tense
  - Introduction: present tense for established facts, past tense for prior studies
  - Discussion: present tense for interpretations, past tense for this study's findings
- Verify consistent spelling convention (American vs. British English) throughout. Flag mixing (e.g., "esophagus" and "oesophagus").
- Flag filler phrases: "interestingly," "notably," "importantly," "it is worth noting that," "of note," "it should be mentioned," "as a matter of fact."
- Verify all abbreviations defined at first use in abstract AND again at first use in main text body.
- Verify abbreviation usage consistent throughout after definition (no switching between spelled-out and abbreviated forms).
- Flag abbreviations used fewer than 3 times (may not be worth abbreviating).
- Flag first-person language and verify the target journal permits it. If not, suggest passive alternatives.
- Flag subjective or promotional language in results section (results should be objective data reporting only).
- Check word count against journal limit if target journal specified.
- Check abstract word count against journal limit if specified.
- Flag AI-tell phrases: "delve into," "shed light on," "pave the way," "in the realm of," "a myriad of," "it's important to note," "robust," "comprehensive," "leveraging," "utilizing," "groundbreaking," "novel" (unless hedged as "to our knowledge, this is novel").

---

## Check 9 — Limitations Assessment

Verify these common limitations are acknowledged where applicable. Flag any that apply to the study but are not discussed:

- Small sample size / limited statistical power
- Single-institution or single-center design
- Retrospective design with inherent selection and information bias
- Missing data and how it was handled
- Short follow-up duration
- Lack of comparator or control group
- Inability to establish causation (observational design)
- Confounders not measured or adjusted for
- Generalizability concerns (academic center, specific population, single geographic region)
- Coding accuracy of administrative data (if using registry data)
- Structural missingness vs. true data quality gaps
- Changes in clinical practice during study period
- Selection bias from excluding patients with missing data
- Immortal time bias (if applicable)
- Lead time bias (if applicable)
- Ascertainment bias (differential documentation)

Flag any limitation a peer reviewer would likely raise that the authors did not address.

---

## Check 10 — Ethical & Reporting Standards

- Verify IRB approval or exemption stated with protocol/exemption number and institution name.
- Verify informed consent addressed (obtained or waived, with reason).
- Identify the appropriate reporting guideline based on study design:
  - Observational → STROBE (22 items)
  - RCT → CONSORT (25 items)
  - Systematic review/meta-analysis → PRISMA (27 items)
  - Prediction model → TRIPOD (22 items)
  - Diagnostic accuracy → STARD (30 items)
  - Protocol → SPIRIT (33 items)
  - Quality improvement → SQUIRE (18 items)
- Verify each applicable item from the relevant guideline is addressed. Flag missing items.
- Verify data availability statement included.
- Verify conflict of interest / disclosure statement included (even if "none").
- Verify funding statement included (even if "no external funding").
- Verify author contributions stated per ICMJE criteria (or journal-specific format).
- Verify clinical trial registration stated if applicable. If not applicable (retrospective), confirm appropriateness.
- Verify no identifiable patient information (names, MRNs, DOB, images with identifiers).

---

## Check 11 — Journal-Specific Formatting

If target journal specified, verify:

- Main text word count within limit
- Abstract word count within limit
- Abstract format matches journal style (structured vs. unstructured)
- Number of tables within limit
- Number of figures within limit
- Reference format matches journal citation style (Vancouver, AMA, APA, etc.)
- Title page includes all required elements (title, authors, affiliations, corresponding author with contact, word count, key words, running head)
- Key words provided (typically 3–6, preferably MeSH terms)
- Supplementary materials formatted and referenced correctly in main text
- Blinding requirements met if journal requires blinded review version
- Cover letter drafted if required
- All required declarations and statements present
- Line numbering added if required
- Page numbering present
- Manuscript file format matches journal requirements (docx, pdf, LaTeX)

If no target journal specified, flag and recommend confirming formatting before submission.

---

## Check 12 — Logical Flow and Argument Strength

Read the manuscript end-to-end as a peer reviewer:

- Does the introduction clearly establish why this study was necessary? Is the knowledge gap stated explicitly in 1–2 sentences?
- Does the introduction avoid being a general textbook review and instead focus narrowly on the gap?
- Are the study objectives stated clearly at the end of the introduction?
- Are the methods detailed enough that another researcher could replicate the study from the description alone?
- Do the results answer every objective stated in the introduction? Flag any objective without a corresponding result.
- Are results presented in the same order as the objectives/methods?
- Does the discussion open with the principal finding in 1–2 sentences (not a restatement of background)?
- Does the discussion compare findings to existing published literature with specific references and numbers?
- Does the discussion avoid over-interpreting results beyond what the data support? Flag causal language in an observational study ("X caused Y" instead of "X was associated with Y").
- Does the discussion acknowledge alternative explanations?
- Is the conclusion proportionate to the evidence? Flag conclusions exceeding study power or design.
- Is the narrative arc coherent: gap → question → method → answer → so what?
- Would a reviewer reading only the abstract, figures, and tables understand the main finding?
- Does the manuscript tell a single, clear story, or does it try to do too many things?

---

## Check 13 — Audit-Step Tagging and Traceability  *(per L038)*

Every audit step taken during pre-submission QC must be tagged with a discoverable identifier so reviewers (and future you) can trace any change back to its origin. This is the discipline that separates a real audit from a paper trail of vague edits.

### Audit-tag format

`[QC-<n>][<category>] <one-line description>` — e.g., `[QC-07][Numbers] Updated Table 1 N from 7,082 → 6,139 to exclude biochemical-leak-only cases (matches Methods inclusion criteria)`.

Categories: `Numbers` / `Abstract-Concordance` / `Methods-Results-Alignment` / `Tables` / `Figures` / `Statistics` / `References` / `Language` / `Limitations` / `Reporting-Standards` / `Formatting` / `Argument-Flow`.

### Tagging requirements

- **Every change** made during QC gets a tag — no silent edits.
- **Every tag** has: sequence number, category, one-line description, source line/cell location, before/after values, reason.
- **Maintain a QC log table** at the head of the corrected manuscript with all tags. Even if the journal does not require it, the log makes reviewer-response letters trivial to write.
- **Audit log lives alongside the manuscript** (`Reports/qc_audit_log_<date>.md`), not buried in inline comments.

### Audit log template

```markdown
# Pre-Submission QC Audit Log
**Manuscript:** [title]
**Date:** YYYY-MM-DD
**Auditor:** [name or "manuscript-qc skill"]

| Tag | Category | Location | Before | After | Reason |
|---|---|---|---|---|---|
| QC-01 | Numbers | Abstract L4 | N = 7,082 | N = 6,139 | Exclusion of biochemical-leak-only per Methods inclusion criteria |
| QC-02 | Methods-Results-Alignment | Methods §2.3 | "log-rank test" | "log-rank test + Cox PH" | Results §3.2 reports Cox HR; method was omitted from Methods |
| QC-03 | Statistics | Table 3 | P = 0.000 | P < 0.001 | JAMA P-value formatting (L013) |
| ... | ... | ... | ... | ... | ... |
```

### Why tags matter

When a reviewer asks *"Why did Table 1 N change between v2 and v3?"*, the tagged audit log answers in one row — no archaeology needed. When you need to write a response letter, the tagged log IS the structure of the response letter. And when future-you returns to a manuscript 6 months later, the tagged log explains every non-obvious edit.

### Comparator-aligned reporting  *(also per L038)*

When the manuscript reports ORs / HRs / RRs for a multi-level exposure (race, insurance, stage, etc.), state which group is the **reference category** every time the estimate is presented. The text, the table footnote, and the figure caption must all agree.

- **Anti-pattern:** "Black patients had OR 1.42 (95% CI 1.21–1.67) for non-surgical management" — implicitly assumes the reader knows the comparator. Reviewers will flag this.
- **Correct:** "Compared to non-Hispanic White patients (reference), non-Hispanic Black patients had higher adjusted odds of non-surgical management (aOR 1.42, 95% CI 1.21–1.67)."

When subgroup-stratified results are reported, make the comparator within each stratum explicit. Verify that the comparator stated in the text matches the one used in the model code (often the lowest factor level, alphabetically or numerically). Mismatched comparators between text and code is the most common silent error in disparity manuscripts.

---

## Check 14 — Introduction ↔ Results Structural Symmetry  *(per L047)*

This check exists because the Methods–Results alignment check (Check 3) and the Logical-Flow check (Check 12) test only the *Methods → Results* direction and the *Introduction-objective → Results* direction. Neither tests the *Results → Introduction* direction. When a new analytical dimension is added to a manuscript (e.g., a new multivariable predictor model is added alongside an existing outcome model, or a new sensitivity analysis becomes a primary result), the new Results subsection can be fully populated and the Methods can correctly describe the new method, while the Introduction still telegraphs only the original aim. This is structurally invisible to Checks 3 and 12 because each Results subsection *does* have a Methods sentence and the *existing* aim *does* have a Result — the asymmetry hides in what is missing from the Introduction, not in what is present.

Treat this as a CRITICAL or MAJOR check depending on the magnitude of the gap.

- Enumerate every Results subsection in order (e.g., "Patient Characteristics", "Perioperative Characteristics", "Independent Predictors of CR-POPF", "Unadjusted Outcomes", "Adjusted Outcomes").
- For each subsection, identify the sentence(s) in the Introduction that motivate it. The motivating sentence must be a gap statement OR an aim/objective statement that names the question the subsection answers.
- Flag any Results subsection whose motivating Introduction sentence is absent OR is only implicit (one-direction framing covering only a subset of the Results). This is a CRITICAL issue if the missing aim is one of the two or more primary aims; MAJOR if it is a secondary aim or a sensitivity analysis.
- Apply the symmetry check to the Discussion as well: every Results subsection should have at least one Discussion paragraph that contextualizes it against the literature, and the Discussion ¶1 ("principal findings") should explicitly enumerate the findings of every primary Results subsection — not just the headline.
- **Discussion body paragraph order must match Results subsection order.** Enumerate the Discussion body paragraphs (¶2 onward, excluding limitations) and verify the topic sequence mirrors the Results subsection sequence. If the Introduction states the aim as "predictors and then consequences" (or any other ordering), the Discussion body must discuss the topics in the same order. A Discussion that promises predictors-first in ¶1 but discusses consequences first in ¶3–4 violates this rule and must be reordered. This is a frequent artifact when a manuscript evolves: an original one-direction draft is amended with a new arm and new Results subsection, but the Discussion body is not reordered to match the new architecture. Severity: MAJOR.
- Apply the symmetry check to the Abstract: the Abstract Results should reflect every primary Results subsection; the Abstract Conclusion should reflect every primary aim from the Introduction.

When a manuscript adds a new analytical dimension to an existing draft (for example, a new table that introduces a new model direction), apply this check before declaring the manuscript ready. The two-pronged framing is the canonical case but not the only one — any time a Results section has parallel subsections that answer different questions, the Introduction should have a parallel gap/aim structure that motivates each subsection.

Trigger patterns (any of the following should prompt running Check 14 from scratch):
- A new Table is added that contains a new model direction (e.g., outcome → exposure becomes exposure → outcome).
- A new Results subsection is added whose subheading is not already paraphrased in the Introduction's aim sentence.
- A new analysis dimension is added (e.g., predictor model alongside an existing outcome model).
- A new primary endpoint is added or the existing primary endpoint is supplemented by a co-primary endpoint.
- The user describes the study with a word ("two-pronged", "dual", "co-primary", "in parallel", "bidirectional", "predictor and consequence", "antecedent and downstream") that signals more than one aim.
- The Introduction or Discussion ¶1 is restructured. If either is reordered, the Discussion body paragraph order must be re-audited against the Results subsection order — restructuring ¶1 without restructuring ¶2 onward is the canonical failure mode (worked example: CR-POPF v4 had a two-pronged Introduction and ¶1 but kept the v3 Discussion body order with consequences first, until v5 reordered to predictors-first).
- The user asks why the Discussion order differs from the Introduction or Results order — treat the question itself as a trigger that the symmetry has been violated.
