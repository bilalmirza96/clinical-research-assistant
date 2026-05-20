# Audit Agents — Briefs

Used by `/analyze` Phase 6 (post-execution self-audit). Five parallel `Task()` subagents (`subagent_type: general-purpose`) run against the executed analysis in a single Agent() invocation. Each receives its role brief below + the relevant inputs. Each returns structured JSON; analyze merges into `audit_report.md`.

**Total expected cost:** ~17K tokens. **Latency:** ~60–90 seconds (parallel; code-reproducibility may extend latency due to actual replay execution).

If any CRITICAL finding emerges → trigger the 6-phase remediation pipeline per L028 (see SKILL.md Phase 6).

---

## Agent 1 — Numerical

### Brief

> You are a numerical auditor. Your job is to verify that every number reported in the analysis matches the source it was computed from, at full precision.

### Inputs

- Working `analysis_report.md` draft (if generated yet) OR the structured outputs in `results_registry.json`
- `results_registry.json`
- `data/working/cohort.csv` (for source-traceable values like N, percentages)

### Method

1. Extract every number from the manuscript draft / report (regex + structured parse)
2. For each, find the matching key in `results_registry.json`
3. Compare at ±0.001 tolerance (or stricter for integer counts)
4. Flag any discrepancy

### Output schema

```json
{
  "agent": "numerical",
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MODERATE | LOW",
      "location": "<file>:<section>",
      "reported_value": "<as written>",
      "source_value": "<from registry>",
      "tolerance_exceeded_by": "<diff>",
      "registry_key": "results_registry::M<n>::<key>"
    }
  ]
}
```

### Severity rubric

- **CRITICAL** — primary effect estimate or N mismatch
- **HIGH** — secondary outcome mismatch
- **MODERATE** — formatting (e.g., 2 decimals vs 3) — flag but non-blocking
- **LOW** — typographical rounding inconsistency

---

## Agent 2 — Statistical

### Brief

> You are a statistical auditor. Your job is to verify that every model was fitted as planned, every required diagnostic was run, and all multiple-testing corrections were applied.

### Inputs

- `analysis_plan.json` (the locked plan)
- `results_registry.json` (what was actually executed)
- `../../references/diagnostics-checklist.md` (required diagnostics per method)
- `decision_log.md` (gate failures + remediations)

### Method

1. For each analysis in `analysis_plan`, verify the corresponding `results_registry` entry exists
2. For each entry, verify the model class, covariates, and reference categories match the plan
3. For each model class, verify every required diagnostic was run (per diagnostics-checklist)
4. Verify multiple-testing correction applied where required (per L006, L032)
5. Verify random seeds set (per L033)
6. Verify gate remediations are documented (per `decision_log.md`)

### Output schema

```json
{
  "agent": "statistical",
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MODERATE | LOW",
      "category": "model-spec-drift | missing-diagnostic | missing-correction | missing-seed | undocumented-remediation",
      "analysis_step": "<step name>",
      "issue": "<one sentence>",
      "recommended_fix": "<action>"
    }
  ]
}
```

### Severity rubric

- **CRITICAL** — primary model spec drifted from plan; missing PH test on Cox; missing multiple-testing correction for primary family
- **HIGH** — missing required diagnostic; missing random seed
- **MODERATE** — undocumented remediation
- **LOW** — minor diagnostic deviation

---

## Agent 3 — Biological-plausibility

### Brief

> You are a clinical content auditor. Your job is to determine whether the findings are clinically plausible given prior literature and the clinical domain.

### Inputs

- `study_spec.json` (subspecialty, clinical context, expected effect direction)
- `evidence_bank.json` if exists — for literature-grounded comparison
- `results_registry.json` (effect estimates)
- `../../../CLAUDE.md` Domain Knowledge section (subspecialty-specific reference values)

### Method

1. Identify the subspecialty + outcome type from study_spec
2. For each primary and secondary effect estimate, ask:
   - Is the **sign** in the expected direction given prior literature?
   - Is the **magnitude** within published norms? (e.g., for surgical complications, ORs of 1.2–2.5 are typical; ORs of 10+ should be flagged)
   - Are the **effect sizes consistent** with the disease biology?
3. If `evidence_bank.json` exists, compare each finding against a literature comparator (≥1 cited study per finding ideal)
4. If no `evidence_bank.json`, surface a MODERATE finding: "Biological plausibility checked against internal context only; recommend running `/literature-review` for literature-grounded validation."

### Output schema

```json
{
  "agent": "biological_plausibility",
  "literature_grounded": true|false,
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MODERATE | LOW",
      "finding": "<what was observed>",
      "literature_comparator": "<from evidence_bank if available, else null>",
      "implausibility": "<sign-reversal | magnitude-out-of-norm | inconsistent-with-biology | unverified>",
      "recommended_action": "<verify variable derivation | check for unmeasured confounder | discuss as novel finding | other>"
    }
  ]
}
```

### Severity rubric

- **CRITICAL** — sign reversal from well-established prior; effect 10× expected magnitude
- **HIGH** — effect outside published norms but biologically plausible
- **MODERATE** — finding cannot be checked against literature (no evidence_bank)
- **LOW** — minor consistency note

---

## Agent 4 — Code-reproducibility

### Brief

> You are a reproducibility auditor. Your job is to verify that the analysis can be re-executed from raw data and produce identical output.

### Inputs

- The replay command from `analysis_report.md` Section 15a
- The project working directory
- `results_registry.json` (current output for comparison)

### Method

1. **Actually execute** the replay command in a clean shell (use Bash tool)
2. Capture the produced outputs (cohort.csv, results CSVs, etc.)
3. Compute sha256 of each produced file
4. Compare against the sha256 recorded in `results_registry.json` / `filter_operations.json`
5. PASS if all hashes match; FAIL with diff details otherwise

### Output schema

```json
{
  "agent": "code_reproducibility",
  "replay_status": "PASS | FAIL | NOT_ATTEMPTED",
  "files_checked": [
    {
      "file": "data/working/cohort.csv",
      "expected_sha256": "...",
      "observed_sha256": "...",
      "match": true|false
    }
  ],
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MODERATE",
      "file": "<file>",
      "issue": "<replay failed | output differs | missing artifact>",
      "diff": "<details>"
    }
  ]
}
```

### Severity rubric

- **CRITICAL** — replay command fails to execute
- **HIGH** — replay succeeds but output differs from registry
- **MODERATE** — replay succeeds with minor differences (timestamp, log line ordering)

### Note

This is the only audit agent that does I/O. It can extend latency by minutes for complex analyses. For very large analyses (>30 min replay), surface as a MODERATE finding: "Full replay deferred due to length; sha256 of source raw data + filter_operations.json verified."

---

## Agent 5 — Completeness

### Brief

> You are a completeness auditor. Your job is to verify that every analysis in the plan was actually executed and has registered results.

### Inputs

- `analysis_plan.json` (full plan)
- `results_registry.json` (what was executed)
- `decision_log.md` (planned but skipped/deferred items)

### Method

1. Enumerate every analysis step in the plan: primary + secondary[] + sensitivity[] + subgroups[] + diagnostics
2. For each, verify a corresponding `results_registry` entry exists
3. If not present, check `decision_log.md` for documented skip/defer rationale
4. Flag any step that's neither executed nor documented as skipped

### Output schema

```json
{
  "agent": "completeness",
  "executed": <count>,
  "skipped_with_reason": <count>,
  "missing_silently": <count>,
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MODERATE",
      "planned_step": "<name from plan>",
      "status": "missing | skipped_undocumented",
      "expected_registry_key": "results_registry::M<n>::<key>",
      "recommended_action": "<execute now | document skip rationale>"
    }
  ]
}
```

### Severity rubric

- **CRITICAL** — primary analysis missing from registry
- **HIGH** — pre-specified subgroup or sensitivity missing
- **MODERATE** — secondary analysis missing without documented rationale

---

## Merge logic (analyze owns)

After all 5 subagents return:

1. Concatenate findings by severity across all agents (CRITICAL → HIGH → MODERATE → LOW)
2. Write `audit_report.md`:

```markdown
# Audit Report — <project> — <date>

## Summary
| Agent | Findings (C/H/M/L) | Status |
|---|---|---|
| Numerical | 0/0/2/0 | PASS |
| Statistical | 0/1/0/0 | PASS_WITH_NOTES |
| Biological-plausibility | 1/0/0/0 | CRITICAL |
| Code-reproducibility | 0/0/0/0 | PASS |
| Completeness | 0/0/1/0 | PASS_WITH_NOTES |

## CRITICAL findings
[detailed list with recommended remediation per finding]

## HIGH findings
[...]

## MODERATE findings
[...]

## 4-tier evidence classification (per L035)
[Tier 1 ROBUST → abstract; Tier 4 HYPOTHESIS-GENERATING → Limitations only]
```

3. If any CRITICAL finding present → automatically trigger the 6-phase remediation pipeline per L028 (see SKILL.md Phase 6). On closure, produce `audit_report_v2.md` documenting closure status.
