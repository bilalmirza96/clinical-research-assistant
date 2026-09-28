# CRA plugin eval suite

The first regression eval suite for the `clinical-research-assistant` plugin,
built against Claude Code 2.1.270's `claude plugin eval`. It exists to catch
regressions in the standing lessons the plugin is supposed to enforce
(`skills/references/lessons-log.json`) — the kind of defect that used to only
surface after a multi-session audit (see `rules/research-protocol.md` in the
workspace root for the HNSCC-TAM incident that motivated this).

**Rule: every new lesson ships with a case or a linter unit test.** When a
lesson is added to `lessons-log.json`, either add an eval case here (if it's
a behavioral/output regression a live agent run can catch) or a unit test
under `tools/tests/` (if it's a pure code-correctness property of a script in
`skills/*/scripts/`). A lesson with neither is not actually enforced — it is
just a note.

## Layout

```
evals/
  _fixtures/            synthetic-only data + generator (see Fixture policy)
  L###-<slug>/           one case per directory, name = lesson id + slug
    prompt.md            frontmatter (name, tags, runs, max_turns, timeout_seconds,
                          allowed_tools) + the natural-language user prompt as body
    case.yaml             schema_version 1.1; context.scaffold_script wiring
    setup.sh              scaffold script: copies fixtures into the throwaway workspace
    graders/*.md          2-4 graders per case (regex / tool_used / file_exists / llm)
  results/               claude plugin eval --json output (gitignored, regenerated per run)
README.md                this file
```

## The 8 cases

| Case | Lesson | Tags | Graders (one line each) |
|---|---|---|---|
| `L033-random-seed-everywhere` | L033 — `random_state=42` on every stochastic call | smoke, full | routing (Skill fired); Bash trace shows an explicit seed of 42 on the bootstrap resample; final answer discloses the seed/reproducibility |
| `L026-mandatory-analysis-report` | L026 — dated 16-section analysis report | full | routing; `analysis_report_*.md` exists somewhere in the workspace; produced files contain >=4 of the template's numbered section headings; LLM judges overall report completeness (numerator/denominator pairing, limitations, etc.) |
| `L091-full-precision-rounding` | L091 — half-up full-precision rendering at `.xx5` boundaries | smoke, full | routing; final answer contains the correct half-up rounding "1.28" for the registry's 1.275 HR; final answer does NOT contain the naive/wrong "1.27"; LLM judges rounding consistency across both reported numbers |
| `L061-genie-panel-offpanel-not-wildtype` | L061 — off-panel genes coded not-tested/NaN, never wild-type | smoke, full | routing; trace shows explicit "not tested"/"off-panel"/NaN reasoning about panel coverage; LLM judges whether the APC rate correctly excludes/flags panel-coverage-limited patients instead of coding them wild-type |
| `L006-bhfdr-multiple-testing` | L006/L032 — BH-FDR + Bonferroni columns when >5 tests | full | routing; trace mentions BH-FDR/Benjamini-Hochberg; trace mentions Bonferroni; LLM judges whether a real master-significance-table (endpoint, P, Q, Bonferroni flag) covers all 6 comparisons |
| `L005-e-value-adjusted-estimate` | L005 — E-value for every adjusted estimate | smoke, full | routing; trace contains "E-value" next to an actual computed number; LLM judges formula correctness (HR/OR/RR-appropriate) and plain-language interpretation |
| `L092-no-penalizer-exposure-model` | L092 — no penalizer/ridge on exposure models; sparse level found & disclosed | full | routing; **must-not** grader — no executed Bash call may pass a nonzero `penalizer=`; trace names/counts the sparse `insurance_type` level; LLM judges the model was fit unpenalized and the sparse level was handled/disclosed rather than silently regularized |
| `L020-abstract-race-terminology` | L020 — race/ethnicity terminology + registry-coding phrase in abstracts | smoke, full | routing; edited `abstract_draft.md` no longer contains "Caucasian"/"Oriental"/"European American"; edited file contains "self-reported race"; LLM judges terminology consistency across the whole abstract |

Tags: `smoke` = the 5 mechanical/cheap-signal lessons (L033, L091, L061, L020,
L005) that should be fast to catch a regression on; `full` = all 8 cases,
run before any release; `ablation` = the full suite with a no-plugin baseline
arm (`--ablation with-without`), which turns `tool_used: Skill` routing
graders into a with-only "did the plugin actually fire" signal rather than a
scored point — useful for confirming a case is actually plugin-dependent, not
just something the base model gets right unprompted.

Every prompt is a natural research request (no internal file paths, no
skill/subskill names) so it exercises real routing through the CRA router —
per workspace rule, `clinical-research-assistant` is the *only* invocable
skill name; `analyze`, `write-abstract`, etc. sit one directory level below
under `skills/internal/` and are reached through the router, never named
directly in a prompt.

## Fixture policy

`_fixtures/make_fixtures.py` (seeded, `random_state=42`) generates SYNTHETIC
data only — no real patient data, ever:

- `cohort_50.csv` — 50-row synthetic cohort (demographics, stage, treatment,
  exposure, survival time/event, a covariate with ~8% missingness, an
  insurance-type category with a single-patient level)
- `tmb_mixed.csv` — long-format mixed-platform (WES vs. two different
  targeted panels) mutation calls; one panel deliberately omits APC/SMAD4, so
  a patient on that panel simply has no row for those genes (the real-world
  GENIE-style trap)
- `tmb_panel_coverage.json` — the answer key for panel gene coverage; kept in
  `_fixtures/` for our own documentation but **deliberately not scaffolded
  into the L061 case's workspace** — the agent must infer coverage from the
  data's own structure, not read it off an answer key
- `registry_mock.json` — a `MASTER_ANALYSIS_REGISTRY.json`-shaped mock
  registry (mirrors the schema written by
  `skills/internal/analyze/scripts/analysis_registry.py`), including two
  `.xx5`-boundary values (1.275, 0.625) chosen because Python's native
  `round()` gets them wrong (1.27, 0.62/63 by banker's rounding) while a
  Decimal `ROUND_HALF_UP` formatter gets them right (1.28, 0.63)
- `abstract_draft.md` — a short synthetic disparities abstract using banned
  race terminology and mixed decimal precision
- `project_CLAUDE.md` — a minimal project brief naming `Reports/` as the
  registry location; scaffolded into each case's workspace as `CLAUDE.md`

Regenerate with `python3 evals/_fixtures/make_fixtures.py`. Never point any
case at real project data.

## Running

All commands target the plugin **path** (`clinical-research-assistant/`),
never a plugin **name** — passing a bare name resolves against the installed
`~/.claude/plugins/cache` copy, which this suite must never touch or read.

```bash
# Schema/load validation only. $0 spend: --max-cost-usd 0 aborts before any
# agent run launches (the documented 0.01 ceiling still lets ONE case run to
# completion, since cost is checked before each launch and starts at $0).
tools/run_evals.sh load

# Cheap tier: the 5 smoke-tagged cases.
tools/run_evals.sh smoke

# Every case.
tools/run_evals.sh full

# Full suite + no-plugin baseline arm.
tools/run_evals.sh ablation
```

Each tier is `--trust-plugin --no-publish --scaffold --allow-tools Bash Write
Edit --json <results-path>`, `--ablation none` except the `ablation` tier,
and `-j 2` concurrency. Cost ceilings: smoke $10, full $40, ablation $80.
Results land under `evals/results/` (gitignored — regenerate, don't commit).

To iterate on a single case directly:

```bash
claude plugin eval clinical-research-assistant --trust-plugin --no-publish \
  --case 'L033-random-seed-everywhere' --runs 1 --scaffold \
  --allow-tools Bash Write Edit --model sonnet --max-cost-usd 4
```

## Cost and time (fill in after each real run; last updated 2026-09-28)

| Tier | Cases x runs | Wall time | Cost |
|---|---|---|---|
| load | 8 x 0 (schema only) | ~1s | $0.00 |
| L033 single-case validation run | 1 x 1 | see report | see report |
| smoke | 5 cases | not yet run at full scale | not yet run at full scale |
| full | 8 cases | not yet run at full scale | not yet run at full scale |
| ablation | 8 cases x 2 arms | not yet run at full scale | not yet run at full scale |

`smoke`/`full`/`ablation` have only been dry-validated for schema (`load`)
and single-case-verified (`L033`) so far, per the build task's validation
scope — run them for real before relying on the cost/time estimates in a
release checklist, and update this table from the resulting JSON's
`durationSeconds` / `costUsd`.

## Adding a case

1. Read the lesson in `skills/references/lessons-log.json` and the skill
   section that enforces it (or note if none does yet — that's a finding in
   itself, not a reason to skip the case).
2. `mkdir evals/L###-<slug>` (folder name = lesson id + short slug).
3. Write `prompt.md`: frontmatter (`name`, `tags`, `runs: 1` unless you have a
   specific reason for more, `max_turns`, `timeout_seconds`, `allowed_tools`)
   + a natural research request as the body. Never name an internal skill or
   file path the plugin itself uses — only the CRA router should be
   discoverable, and only through it firing on its own.
4. If the case needs seeded data, add a `setup.sh` that copies only the
   fixtures it needs from `_fixtures/` (resolve fixture paths relative to
   `${BASH_SOURCE[0]}`'s own directory, since the scaffold script's cwd is
   the throwaway workspace, not the case directory) and a `case.yaml`
   pointing `context.scaffold_script` at it.
5. Add 2-4 `graders/*.md`: at least one deterministic grader on a produced
   artifact, one `tool_used: Skill` routing grader, and an `llm` grader only
   where the lesson is genuinely a judgment call (not a mechanical pattern
   check). Regex patterns are matched by a plain JS `RegExp` — do **not**
   use inline mode modifiers like `(?i)`; put case-insensitivity in the
   separate `flags: i` field instead, or the grader throws
   "Invalid regular expression" at run time. `llm` graders take `criteria`
   only — no `focus` field exists in this schema version despite being a
   reasonable-sounding option; case.yaml will fail to load with
   `graders.N.focus: Invalid input` if you add one.
6. Validate with `tools/run_evals.sh load`, then a single real run with
   `--max-cost-usd 4` before trusting the case in `smoke`/`full`.

## Gotchas discovered while building this suite

- **Target the plugin path, not the plugin name.** `claude plugin eval
  clinical-research-assistant` resolves the bare name against the installed
  marketplace cache (`~/.claude/plugins/cache/...`), not this source tree —
  exactly the thing this suite is forbidden from touching. Always pass the
  path (`./clinical-research-assistant` from the repo root, or the absolute
  path).
- **`--max-cost-usd 0.01` still runs one full case.** The ceiling is checked
  *before* each run launches; at the first launch, accumulated cost is $0,
  which is `<= 0.01`, so it launches — and can spend up to a few dollars
  before the *next* launch is blocked. Use `--max-cost-usd 0` for a genuine
  zero-spend schema/load check.
- **Grader-writing subagents (or Claude Code sessions generally) may refuse
  to `Write` a file whose path contains "report"** (e.g.
  `graders/report_file_exists.md`) — a guardrail meant for a different
  situation (Claude writing its own summary-report files) fires on any path
  that merely contains the word. Name the grader file something else (this
  suite uses `deliverable_exists.md`).
- **Two of the eight lessons (L091, L092) are not yet wired into the skill's
  active runtime instructions** — they exist in `lessons-log.json` and in
  `references/changelog.md` (a "why a rule exists" reference loaded only on
  demand), but `analyze/SKILL.md`'s operational phases don't call them out
  the way they call out L033/L005/L006. The `PREREQUISITE` section does say
  to read `lessons-log.json` up front regardless, so these cases are a fair
  regression test of that fallback path — but a fail on `L091` or `L092`
  specifically may mean "not promoted to the skill yet" rather than "the
  skill regressed." Worth promoting both into `analyze/SKILL.md` /
  `write-manuscript/SKILL.md` proper if these cases keep failing.
- **`/analyze`'s full pipeline is heavily gated** (Phase 0 literature recon,
  5 approval halts before the final report). A `max_turns: 25` /
  `timeout_seconds: 600` budget may not be enough for a run to reach Phase 7
  (where the analysis report and BH-FDR/E-value tables are actually
  written). Graders here mostly check the full conversation `trace` (not
  just `last_message` or final files) so that partial progress toward a
  lesson's behavior still scores, even when the full deliverable doesn't
  land in budget. A genuine miss is still a genuine miss — don't loosen a
  grader just to make a truncated run pass.
