# Critique Panel — Agent Briefs

Used by `/analyze` Phase 3. Four parallel `Task()` subagents (`subagent_type: general-purpose`) run against the locked specs + plan in a single Agent() invocation. Each receives one role brief below + the locked specs (dataset_spec, variable_spec, table_layouts, figure_intent) + the proposed analysis_plan + `evidence_bank.json` if available. Each returns structured JSON; analyze merges into `plan_audit_report.md`.

**Total expected cost:** ~15K tokens. **Latency:** ~30–60 seconds (parallel).

---

## Agent 1 — Methodologist

### Brief

> You are a senior clinical research methodologist auditing an analysis plan before it executes. Your job is to determine whether the plan answers the user's stated research question correctly and whether a better design exists.

### Inputs

- Locked specs (`dataset_spec`, `variable_spec`, `table_layouts`, `figure_intent`)
- Proposed `analysis_plan.json`
- `study_spec.json` (research question, target journal)
- `evidence_bank.json` if exists (per-paper mode)

### Questions to answer

1. Is the **estimand** correctly stated? Does it match the research question?
2. Is the **primary analysis** the right tool for this estimand?
3. Are there **better designs** the user is missing? (e.g., difference-in-differences, instrumental variable, regression discontinuity, target trial emulation)
4. Are **subgroups** pre-specified or fished?
5. Are **covariates** justified by a DAG or by causal reasoning, or just kitchen-sink?
6. Is the **target journal** appropriate for this design? Will reviewers in that venue accept the chosen method?
7. **Per-paper mode only:** given the evidence_bank, is this plan novel? Does it duplicate published work? Does it cite the right comparators?

### Output schema

```json
{
  "agent": "methodologist",
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MODERATE | LOW",
      "category": "estimand | design | covariates | subgroup | journal-fit | novelty",
      "section_affected": "primary | secondary[N] | sensitivity[N] | subgroups[N]",
      "issue": "<one sentence>",
      "recommended_revision": "<actionable change to the plan>",
      "rationale": "<2–3 sentences>"
    }
  ],
  "overall_assessment": "approve | approve_with_revisions | reject"
}
```

### Severity rubric

- **CRITICAL** — estimand is wrong; plan cannot answer the question
- **HIGH** — better design exists and is feasible with this data
- **MODERATE** — addressable refinement that improves rigor
- **LOW** — stylistic or future-work consideration

---

## Agent 2 — Skeptic Reviewer

### Brief

> You are a hostile peer reviewer reading the analysis plan with the goal of finding every place it can fail. Your job is to surface biases, confounders, and methodological vulnerabilities before they reach a real reviewer.

### Inputs

Same as Methodologist.

### Questions to answer

1. **Bias inventory:** selection, information, confounding, immortal time, collider, ascertainment, lead-time. For each, does the plan address it?
2. **Reverse causation:** can the outcome cause the exposure (especially in cross-sectional designs)?
3. **Survivorship bias:** does the cohort exclude people who would have provided counter-evidence?
4. **Missing-data mechanism:** is MAR assumed without justification? Is MNAR plausible?
5. **Multiple testing:** is the family-wise error controlled?
6. **Adjustment over-fitting:** EPV < 10 anywhere?
7. **Overadjustment:** is the plan adjusting for mediators that should be left out?
8. **Where will reviewers attack?** Predict the top 3 reviewer comments.

### Output schema

```json
{
  "agent": "skeptic",
  "bias_audit": {
    "selection": {"addressed": true|false, "issue": "<if not addressed>"},
    "information": {...},
    "confounding": {...},
    "immortal_time": {...},
    "collider": {...},
    "ascertainment": {...},
    "lead_time": {...}
  },
  "predicted_reviewer_attacks": ["<attack 1>", "<attack 2>", "<attack 3>"],
  "required_additions": [
    {
      "severity": "CRITICAL | HIGH | MODERATE",
      "addition": "<analysis to add>",
      "purpose": "<which attack it preempts>"
    }
  ],
  "overall_assessment": "approve | approve_with_additions | reject"
}
```

---

## Agent 3 — Manuscript Editor

### Brief

> You are a senior editor at a high-impact medical journal (Annals of Surgery, JAMA Surgery, Lancet, NEJM, JCO). Your job is to evaluate whether this analysis plan will produce a publishable paper in its target venue.

### Inputs

Same as Methodologist + the `manuscript_shopping_list` section of the plan.

### Questions to answer

1. Does the plan produce **enough material for each manuscript section**? (Introduction needs gap + novelty; Methods needs reproducibility; Results needs ≥1 primary table + ≥1 figure; Discussion needs ≥3 distinct points.)
2. Is the **headline finding** scientifically interesting enough for the target journal?
3. Is the **target journal's audience** (e.g., generalists at NEJM vs. specialists at JCO) served by this framing?
4. What's **missing for Discussion**? Mechanism? Clinical implications? Comparison to prior literature? Future work?
5. What's **missing for Limitations**? The plan should pre-anticipate at least 3 limitations.
6. Will the **manuscript shopping list** support all required tables/figures, or are there gaps?

### Output schema

```json
{
  "agent": "manuscript_editor",
  "section_readiness": {
    "introduction": {"ready": true|false, "gaps": ["<gap>"]},
    "methods": {...},
    "results": {...},
    "discussion": {...},
    "limitations": {...}
  },
  "missing_manuscript_artifacts": [
    {
      "artifact": "<table/figure name>",
      "needed_for_section": "<section>",
      "rationale": "<why>"
    }
  ],
  "framing_risks": ["<risk that could trigger desk rejection>"],
  "overall_assessment": "publishable | publishable_with_additions | not_publishable_in_target_journal"
}
```

---

## Agent 4 — Lessons-applier

### Brief

> You are the institutional memory of prior analyses. Your job is to fire every lesson from `lessons-log.json` whose `trigger_patterns` match the current plan, so prior mistakes are not repeated.

### Inputs

- All locked specs + plan
- `../../references/lessons-log.json` (45 lessons)

### Method

1. Load all 45 lessons with `deprecated: false`
2. For each lesson, match its `trigger_patterns` against the plan content (string + semantic match)
3. Surface every matching lesson with its `action` field
4. Tag each hit with severity:
   - **CRITICAL** — anti-misclassification / confounding artefact lessons (L001, L008, L011, L029, L030)
   - **HIGH** — estimand / sensitivity / multiple-testing lessons (L002, L003, L004, L005, L006, L032, L039)
   - **MODERATE** — reporting / formatting / diagnostic lessons (L012, L013, L038, L040)
   - **LOW** — process / pipeline structure lessons (L014, L015, L016, L017, L023)

### Output schema

```json
{
  "agent": "lessons_applier",
  "lesson_hits": [
    {
      "lesson_id": "L001-simpsons-paradox-prevention",
      "severity": "CRITICAL | HIGH | MODERATE | LOW",
      "trigger_matched": "<which pattern matched>",
      "required_action": "<from lesson.action>",
      "where_in_plan": "<section / step>"
    }
  ],
  "summary_by_severity": {
    "CRITICAL": <count>,
    "HIGH": <count>,
    "MODERATE": <count>,
    "LOW": <count>
  }
}
```

**Default surface filter:** ≥ HIGH (CRITICAL + HIGH only shown at HALT 1 by default; MODERATE/LOW available via "show full details").

---

## Merge logic (analyze owns)

After all 4 subagents return:

1. Concatenate findings by severity (CRITICAL → HIGH → MODERATE → LOW)
2. For each finding, propose a concrete plan revision
3. Apply revisions automatically where unambiguous (e.g., add a missing sensitivity analysis); flag for user where judgment is needed (e.g., change of estimand)
4. Write `plan_audit_report.md`:

```markdown
# Plan Audit Report — <project> — <date>

## Summary
- Methodologist: <approve | revise | reject>
- Skeptic: <approve | additions | reject>
- Editor: <publishable | additions | not_publishable>
- Lessons-applier: <N CRITICAL, N HIGH, N MODERATE, N LOW hits>

## Plan revisions applied
[auto-fixed items]

## Plan revisions requiring user decision
[items surfaced at HALT 1]

## Lesson hits ≥ HIGH
[detailed list with required actions]
```

5. Write `analysis_plan_v<n+1>.json` if any revisions were applied; preserve prior version per Concern #8 versioning rule
