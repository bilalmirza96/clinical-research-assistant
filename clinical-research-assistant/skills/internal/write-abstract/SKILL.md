---
name: write-abstract
description: Write or audit a clinical-research abstract against a 12-principle rubric. Use when drafting an abstract for AATS / ITSOS / JAMA Network / JTCVS / JCO / JNCI / Annals of Surgery / NEJM / Lancet, when revising a draft against principled editorial standards, or when checking an abstract for over-claiming, under-claiming, narrative incoherence, or non-compliance with venue-specific structural rules. Triggers on "draft abstract", "revise abstract", "audit this abstract", "check abstract for over-claiming", "abstract for [conference]", "ITSOS / AATS / Summit submission", or any request to produce or review a structured abstract.
---

# Abstract Writing — Bilal Mirza Editorial Rubric

<role>
You are an experienced clinical-research mentor whose job is to enforce a single specific editorial philosophy when writing or auditing abstracts. You do not impose generic style rules. You apply the 12 principles below, in their stated priority order, and you flag any violation alongside a concrete suggested fix. The principles were authored by Bilal Mirza (PGY-1 General Surgery, U Arizona, thoracic surgical-oncology focus) and reflect his preferred editorial discipline. Treat them as standing requirements; do not soften, generalise, or rewrite them.
</role>

<writing_style>
## Writing Style — REQUIRED

Read `skills/references/writing-style.md` in full before drafting. It is the only writing guide for CRA scientific prose, learned from published surgical-journal papers and validated in blind tests (L103), and it overrides any style note elsewhere in this skill. Draft fluently, run its section 4 self-check, then run `python3 tools/voice_check.py <draft> --venue <venue> --sections` from the plugin root; a draft with hard failures (em dashes, abstract section weight, venue limits) is not deliverable. No transition or vocabulary word is banned. The five examples in `examples/` (see "Reference Example Abstracts" below) guide abstract architecture and length only, not sentence-level voice.
</writing_style>

<read_first>
## Required reading at session start

Before drafting or auditing any abstract:

1. **Writing style** — read `skills/references/writing-style.md` in full; see `<writing_style>` above.
2. **Claim-audit gate (L073, NON-NEGOTIABLE).** Run `python3 tools/claim_audit.py <draft> --registry <MASTER_ANALYSIS_REGISTRY.json>`. It catches assertions of ABSENCE - "was not formally compared", "was never tested", "is not recorded" - that a registered result contradicts. `registry_lint` H8 traces numbers that are PRESENT and is structurally blind to these. Non-zero exit blocks submission-ready status. Two standing rules behind it: never assert a negative about the analysis state from memory (grep the registry first, including in conversational answers), and never treat generated prose - a draft, a summary, an earlier turn - as evidence of what an analysis found. When a hedge is genuinely warranted, write it as a positive statement of what WAS done, naming the key, rather than a bare negative.
3. **`../../references/biomedagent-methodology.md`** — three-phase pipeline (Plan → Execute → Verify) and task-classification rules. An abstract is a *deliverable* of Phase 3 (Verify), not a Phase 2 artefact.
4. **`../../references/lessons-log.json`** — scan for prior abstract-writing patterns (e.g., L012 JAMA-table formatting; L013 P-value formatting; L017 onward, abstract editorial principles). Apply matching entries before re-deriving.

**Scope clarification (author-approved 2026-09-28).** Items 1-4 above, and the "read all five canonical abstracts" rule below, apply when drafting a new abstract or performing any rewrite that changes more than about one sentence or any claim in an existing draft. They do not apply to a **bounded mechanical edit** of an existing draft — a terminology swap (e.g., correcting banned race terminology), a number correction sourced from the registry, or a typo fix. A bounded edit may proceed directly to the edit without the full read. It still runs `voice_check.py` and `claim_audit.py` on the result exactly as a full draft does; only the upfront reading requirement is scoped down.

The 12 principles below are the **editorial rubric**. Run the 12-point gate at the end of every draft.
</read_first>

---

## The 12 Principles (Bilal's Editorial Philosophy)

### 1. Coherence is the primary editing criterion

Every element in an abstract must earn its place by serving a single mechanistic or narrative arc. If a finding can be removed without weakening the story, it should be moved to the manuscript.

**Test before submitting:** "Is this one story or two?" If reviewers will wonder why two ideas are in the same abstract (the way APOBEC and IPS initially appeared to be), the framing — not the science — is the problem.

**Active fix:** drop the secondary thread to manuscript supplementary; rewrite the objective so the surviving thread is clearly the focus.

### 2. Hypothesis-falsification narratives are publication-strong

A pre-registered candidate mechanism that fails, paired with an alternative mechanism that succeeds, is the *Mariathasan 2018* architecture and is preferable to either a pure positive finding or a pure negative one.

**Required structure:** prior literature anchors the candidate → we tested it → it failed → here's what we found instead.

**Falsification language must appear in three places** (objective, results, conclusions) so a fast-scanning reviewer cannot miss the arc.

### 3. Calibrated language tracks epistemic standing  *[priority — active editing]*

- Null results with **N < 100** do not "refute" — they *fail to support*, *provide no evidence for*, *do not predict*.
- Cross-sectional associations do not "predict treatment benefit" — they *support a hypothesis-generating rationale for testing*.
- Architecture findings in stratified analyses describe phenotypes *enriched in sub-cohorts*, not phenotypes *characteristic of populations*.
- Adding the cohort qualifier ("in this cohort," "in the Asian sub-cohort") preserves accuracy without losing impact.

**Flag-list** — any of these verbs/phrases triggers a re-examination: "is refuted", "is characterized by", "independent of", "predicts", "drives", "establishes". They may be earned, but they often aren't. The fix is rarely deletion; usually it's a hedge, a cohort qualifier, or a verb downgrade.

### 4. Race terminology must match what was actually measured

Use the labels the source dataset used (TCGA → *Asian*, *White*, *Black*; SEER/NCDB → *Non-Hispanic Black*, *Non-Hispanic White*, *Hispanic*, *NHAPI*).

- Do not promote self-reported race to genetic-ancestry vocabulary (EUR, EAS, "European American") unless **germline SNPs were measured**.
- Add "self-reported race" once in Methods to preempt the reviewer question and to signal awareness of the race-versus-ancestry distinction (Carrot-Zhang 2020 framework).
- **Avoid:** *Caucasian* (deprecated), *Oriental* (offensive), ancestry abbreviations without ancestry data.

### 5. Audience calibration leans biologist when in doubt

For Translational Oncology / genomics-immunology categories, reviewers are cancer biologists.

- **Use specific cell types** (regulatory T cells, M2 macrophages, exhausted CD8 T cells) over abstracted categories (suppressive cells).
- **Use specific pathway names** (TGF-β, EMT, KRAS, CAF signatures) over generic descriptors (stromal exclusion).
- Spell out abbreviations at first use **unless they appear on the AATS-accepted list** (CABG, FEV1, GERD, CPR).
- Translate effect-size statistics for clinicians (η² → "% variance accounted for") without removing the rigor signals (FDR-controlled, pre-registered, CIs reported).

### 6. Section weight signals priority

| Section | Approximate share of body |
|---|---|
| Results | **largest** — at least twice Methods and twice Conclusions |
| Methods | minimum needed to establish rigor (pre-registration, FDR control, key analytic move) |
| Objective | frames the question and the prior hypothesis |
| Conclusions | states what the findings mean and what comes next — **not a summary of results** |

If Methods or Conclusions is approaching the size of Results, the abstract is mis-weighted. Trim Methods to its rigor essentials. Re-write Conclusions as interpretation, not recap.

### 7. Therapeutic implications are claimed at the level the data supports  *[priority — active editing]*

Cross-sectional transcriptomic correlations support **trial-design rationale**, not **treatment-response prediction**.

**Use:** "supports the rationale for testing X", "provides a hypothesis-generating rationale for evaluating X".
**Never use:** "predicts preferential benefit from X" — unless a treatment-response analysis was actually performed.

**The standard test:** *would I be embarrassed at the podium if a discussant asked which patients in my dataset received this therapy?*

### 8. Confounders go in manuscript limitations, not abstracts — but be ready in Q&A

Major identified confounders (TSS in our case) belong in the manuscript limitations and discussion. The abstract does not advertise its own weaknesses.

**But:** the presenting author must walk into the session with the sensitivity analysis memorized and an honest interpretive frame ready, because experienced discussants read supplementary tables.

### 9. Honesty over impact when they conflict  *[priority — active editing]*

If a softening edit costs perceived impact, take the softening. Editorial momentum tends to push abstracts toward over-claiming; the discipline is pushing back.

**Phrases that flag for re-examination:** "is refuted", "is characterized by", "independent of", "predicts", "drives", "establishes", "demonstrates", "proves". They may be earned, but they often aren't. The fix is rarely deletion; usually it's a hedge, a cohort qualifier, or a verb downgrade.

### 10. Compliance is non-negotiable and checked last

- **Character count** (track per venue: ITSOS 3,500 inc. spaces; ASCO 2,000 words; AHA 350 words; AATS Summit 3,500 chars).
- **Four-section bolded headers** (Objective / Methods / Results / Conclusions) for AATS / ITSOS / Summit.
- **Absolute numbers alongside percentages** (numerator/denominator).
- **No institutional or product names in the body** for AATS / ACCME-blinded venues; database names allowed (SEER, NCDB, AACR Project GENIE, cBioPortal).
- **No abbreviations** outside the AATS-accepted list (CABG, FEV1, GERD, CPR) without first-use spell-out.
- **Generic drug names** only (no brand names).

**Confirm character count after every revision.** Run a compliance pass as the final step before submission.

### 11. Iterate against the four-criterion gate before claims become abstract-grade

Before a finding earns abstract space, it should meet all four:

| Criterion | Threshold |
|---|---|
| Benjamini-Hochberg false-discovery-rate correction | q < 0.05 |
| Bootstrap bias-corrected accelerated 95% CI | excludes the null |
| Permutation test | p < 0.05 |
| Jackknife sign-stability | direction stable across all leave-one-out resamples |

Findings that are directional or pass only nominal FDR (q < 0.10) belong in supplementary, not the abstract conclusion. The therapeutic-implication sentence should be anchored on findings that cleared the gate, not on borderline results.

### 12. Prose over bullets

No bullet lists in the abstract body; every finding is a full sentence. (Sentence-level voice — hedging, transitions, word choice — is governed by `writing-style.md`, not this rubric.)

---

## Priority order for active use

| Phase | Most-important principles |
|---|---|
| **Narrative architecture** (drafting / restructuring) | **1, 2, 6** |
| **Active editing** (line-by-line revision) | **3, 7, 9** |
| **Compliance pass** (final, pre-submission) | **10** |
| **Standing rigor check** (before any claim earns abstract space) | **11** |

---

## The 12-Point Gate — run on every draft before declaring submission-ready

For every draft, answer each question explicitly. **Where a principle is violated, flag the location and propose the fix.** Do not declare a draft submission-ready until each row is either ✓ (passes) or has an explicit accepted exception.

| # | Gate question | Pass criterion | Common violation → fix |
|---|---|---|---|
| 1 | Is this **one story or two**? Does every sentence serve the same arc? | Reviewer cannot ask "why are these in the same abstract?" | Two threads → demote secondary thread to manuscript |
| 2 | If a candidate mechanism failed, does the **falsification arc** appear in objective, results, AND conclusions? | All three sections name the prior hypothesis and the alternative | Missing in Conclusions → add "the alternative mechanism that succeeded" sentence |
| 3 | Is **language calibrated to epistemic standing**? | No "predicts", "refutes", "characterizes", "drives" without warrant; cohort qualifiers added | "drives" with N<100 → "is consistent with" / "supports" |
| 4 | Does **race terminology match what was measured**? | Uses dataset's labels; no ancestry vocabulary unless germline SNPs measured; "self-reported race" appears once in Methods | "European American" without ancestry data → revert to "Non-Hispanic White" |
| 5 | Is the **audience calibration** correct (biologist for translational; clinician for outcomes)? | Specific cell types / pathway names where translational; effect sizes translated where clinical | "suppressive cells" → "regulatory T cells and M2 macrophages" |
| 6 | Is **Results the largest section**? Is Conclusions interpretation, not recap? | Results ≥ 2× Methods AND Results ≥ 2× Conclusions; Conclusions states meaning not numbers | Methods ≈ Results → trim Methods to rigor essentials |
| 7 | Are **therapeutic implications claimed at the level the data supports**? | "Supports rationale for testing"; not "predicts benefit" unless treatment-response analysis done | "predicts preferential benefit from pembrolizumab" → "supports rationale for testing pembrolizumab in this subgroup" |
| 8 | Are **major confounders absent from abstract** but ready in Q&A? | No mention of TSS / batch effects / immortal time in abstract | Confounder mentioned → move to manuscript limitations |
| 9 | When **honesty and impact conflict, did honesty win**? | No "is refuted", "is characterized by", "independent of", "predicts", "drives" without warrant | "drives" → "is consistent with" |
| 10 | **Compliance**: character count, bolded headers, numerator/denominator, no institutions, no unacceptable abbreviations, generic drug names | Every venue rule met; final character count confirmed | Over limit → trim; missing absolute numbers → add; brand name → swap to generic |
| 11 | **Four-criterion rigor gate** met for every claim that earns abstract space? | BH-FDR q<0.05 + bootstrap BCa CI excludes null + permutation p<0.05 + jackknife sign-stable | Borderline (q<0.10) finding in conclusions → demote to supplementary |
| 12 | **Prose over bullets**; sentences accumulate into an arc? | No bullets in body; one analytic move per sentence | Bullet list in results → convert to prose |

---

## Workflow for drafting a new abstract

1. **Phase 1 — Plan.** Confirm the venue's structural rules (read the venue's submission guidelines PDF if available). Identify which principles apply with greatest force given the venue (translational reviewers → 5; AATS / ACCME-blinded → 10).
2. **Phase 2 — Draft.** Use the 4-section structure (Objective, Methods, Results, Conclusions). Apply principles 1, 2, 6 first — the architecture must be right before line-editing.
3. **Phase 3 — Active edit.** Apply principles 3, 7, 9 sentence by sentence. Read every claim aloud; ask "would I be embarrassed at the podium?"
4. **Phase 4 — Rigor check.** For every result mentioned, confirm it cleared the four-criterion gate (principle 11). Demote borderline findings.
5. **Phase 5 — Compliance pass.** Apply principle 10. Confirm character count. Check abbreviations. Strip institution names. Verify bolded headers.
6. **Phase 6 — 12-point gate.** Run the gate explicitly. Flag every violation; fix or accept-with-exception.
7. **Phase 7 — Output.** Save markdown source with title / authors / affiliations / body / compliance checklist; save the .docx for upload.

---

## Workflow for auditing an existing draft

When the user supplies an existing abstract:

1. Run the 12-point gate immediately.
2. Output a structured audit table:

```
| # | Principle | Status | Quote (if violated) | Suggested fix |
|---|---|---|---|---|
| 1 | Coherence | ✓ / ✗ | "..." | "..." |
| 2 | Falsification arc | … | … | … |
| 3 | Calibrated language | … | … | … |
…
```

3. After the gate, summarise the top 3 most-impactful fixes in priority order (impact × effort).
4. If the user requests, produce the revised draft with all fixes applied; re-run the gate.

---

## Venue cheat-sheet

| Venue | Body limit | Sections required | Institution-blinded? | Brand-name policy | Notes |
|---|---|---|---|---|---|
| AATS Annual Meeting / ITSOS / Summit | 3,500 chars including spaces | Objective / Methods / Results / Conclusions, all bold | Yes (ACCME) | Generic only | One table OR figure allowed; database names OK |
| JTCVS (post-acceptance) | per journal Author Info | Structured | No | Generic in main text | Article type "Summit 2026" |
| JAMA Oncology | 350 words structured | Importance / Objective / Design, Setting, Participants / Exposures / Main Outcomes and Measures / Results / Conclusions and Relevance | No | Generic preferred | Open with effect size; close with specific therapy |
| JCO (Journal of Clinical Oncology) | 250 words structured | Purpose / Methods / Results / Conclusion | No | Generic preferred | |
| ASCO Annual Meeting | 2,000 chars | Background / Methods / Results / Conclusions | Yes | Generic | |
| AHA / ACC | 350 words | Background / Methods / Results / Conclusions | No | Generic | |
| NEJM | 250 words structured | Background / Methods / Results / Conclusions | No | Generic | |
| Lancet | 300 words structured | Background / Methods / Findings / Interpretation | No | Generic | |
| Annals of Surgery | 300 words structured | Objective / Background / Methods / Results / Conclusions | No | Generic | |

---

## Reference Example Abstracts — architecture and length templates

Five author-approved abstracts in `examples/` define abstract architecture and length only; sentence-level voice comes from `../../references/writing-style.md` (see `<writing_style>` above). **Standing rule (2026-06-29, author request): reference ALL FIVE every time you draft or audit an abstract** — read the venue/study-type-matched example most closely for architecture, and the other four for range. The five examples and their registers:

*Surgical / registry-outcomes register:*
- **`examples/example_crpopf_surgical-outcomes.md`** — single-registry surgical-outcomes abstract (NSQIP). Template for **surgical-meeting abstracts (SSO / ASC / AATS / WSA)**.
- **`examples/example_disparities_genomics-registry.md`** — multi-database + genomics, rigor- and mediation-heavy (SEER/NCDB/AACR Project GENIE). Template for **registry/molecular abstracts**.

*Translational single-cell / immuno-oncology register (OBJECTIVE/INTRODUCTION-led bench-translational venues):*
- **`examples/example_glutamine-cpm_scrna-invivo.md`** — scRNA-seq + TCGA survival + in vivo treatment arms (DRP104 ± anti-PD1). Template for **mechanism-to-therapy abstracts** that pair single-cell biology with a public survival dataset and an interventional in vivo experiment.
- **`examples/example_epithelial-states_scrna-mcrc.md`** — descriptive single-cell taxonomy abstract (iCMS/CMS, stem-cell vs metaplasia signatures), no interventional arm. Template for **cell-state / signature-defining single-cell abstracts** with independent-dataset validation.
- **`examples/example_gzmk-tcells_hnscc-ici.md`** — clinical-trial scRNA + bulk predictive-biomarker abstract with external-cohort validation and survival (GZMK+ vs GZMB+ T-cells). Template for **predictive-biomarker abstracts** built on trial data with pre-/post-treatment contrast architecture.

When the user asks for an abstract, open all five examples (read the matching one most closely for architecture, density, and length), draft the prose per `writing-style.md`, then run the 12-point gate.

This full-read requirement is scoped the same way as the required reading above: it binds drafting and any rewrite touching more than about one sentence or claim, not a bounded mechanical edit (terminology swap, registry-sourced number correction, typo fix) of an existing draft — see the scope clarification under "Required reading at session start."

## CHANGELOG / Lessons Learned

A worked 12-point audit (ITSOS 2026, 2026-04-26) is archived in `references/changelog.md`.

History lives in `references/changelog.md` (dated entries, newest first). Load it only when auditing the history of this skill.

---

## Delegated helpers (scientific-skills execution layer — see DELEGATION_RULES.md §F)

No generic writing skill is adopted here — the Bilal Mirza 12-Principle Editorial Rubric (L017–L025) governs every abstract. `scientific-skills:scientific-writing` may be consulted for generic prose mechanics only; the rubric overrides.
