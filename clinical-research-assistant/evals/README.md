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
| `L033-random-seed-everywhere` | L033 — `random_state=42` on every stochastic call | smoke, full | routing (Skill fired); saved `scripts/` analysis file (agent is asked to save one) shows an explicit seed of 42 (regex over produced files — the `analyze` skill delegates code execution to a subagent, so a top-level `tool_used: Bash` grader can't see it); final answer discloses the seed/reproducibility |
| `L026-mandatory-analysis-report` | L026 — dated 16-section analysis report | full | routing; `analysis_report_*.md` exists somewhere in the workspace; produced files contain >=4 of the template's numbered section headings; LLM judges overall report completeness (numerator/denominator pairing, limitations, etc.) |
| `L091-full-precision-rounding` | L091 — half-up full-precision rendering at `.xx5` boundaries | smoke, full | routing; final answer contains the correct half-up rounding "1.28" for the registry's 1.275 HR; final answer does NOT *report* "1.27" as the HR (reported-value context, e.g. "= 1.27"/"HR 1.27" — a mention while explaining why naive rounding is wrong is fine); LLM judges rounding consistency across both reported numbers |
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
  `skills/internal/analyze/scripts/analysis_registry.py`), including one
  `.xx5`-boundary value (the Model B HR, 1.275) chosen because Python's
  native `round()` gets it wrong (1.27 by banker's rounding) while a Decimal
  `ROUND_HALF_UP` formatter gets it right (1.28). The stage IV entry is a
  whole-cohort proportion (`stageIV_n / 50`, computed in `make_fixtures.py`
  from the same array that writes `cohort_50.csv`, never a second hand-typed
  literal) — it used to be a hardcoded 0.625 with a mismatched `n: "5/8"`
  numerator (a label/n/source_key contradiction; L091 fixture-contradiction
  finding, 2026-09-28) that made a defensible agent halt on the ambiguity
  score as a grader failure. Fixed to `10/50 = 0.2`, an exact whole-percent
  value with no rounding ambiguity of its own.
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

Each non-`load` tier is `--trust-plugin --no-publish --scaffold --keep-temp
--allow-tools Bash Write Edit --json <results-path>`, `--ablation none`
except the `ablation` tier, and `-j 2` concurrency. Cost ceilings: smoke $10,
full $40, ablation $80. Results land under `evals/results/` (gitignored —
regenerate, don't commit).

`--keep-temp` preserves every run's scaffold directory (and the trace.jsonl
inside it) instead of letting the harness delete it from its ephemeral
`/private/tmp` location the moment the run ends. After `claude plugin eval`
exits, `run_evals.sh` reads the `tracePath` every case/arm/run reported in
its `--json` output, copies each surviving `trace.jsonl` into
`evals/results/<timestamp>/traces/<case>[_<arm>][_runN].jsonl`, prints where
they landed, and then removes *only* the specific kept temp directory each
trace came from (never anything else — see "Diagnosing a failure" below).

To iterate on a single case directly:

```bash
claude plugin eval clinical-research-assistant --trust-plugin --no-publish \
  --case 'L033-random-seed-everywhere' --runs 1 --scaffold \
  --allow-tools Bash Write Edit --model sonnet --max-cost-usd 4
```

## Diagnosing a failure

A grader `explanation`/`evidence` in the `--json` output is often enough
(`aggregate-result.json` under the CLI's own auto-created
`evals/results/<timestamp>/` directory has the same shape as the file
`run_evals.sh` writes to `--json`), but when it isn't, go to the trace.

**Where traces land.** Every `smoke`/`full`/`ablation` run through
`run_evals.sh` now copies each run's full trace to
`evals/results/<timestamp>/traces/<case>.jsonl` (or
`<case>_<arm>.jsonl` / `<case>_<arm>_runN.jsonl` when a case has an ablation
arm or more than one run) — `run_evals.sh` prints the directory at the end of
every run, and each copied line is echoed as `TRACE_SAVED\t<path>`. These are
gitignored like the rest of `evals/results/`; copy anything you want to keep
out of that tree before it's cleaned up by a later run.

**Reading a trace.** Each line of `<case>.jsonl` is one JSON event in the
run's full message stream, including nested `Task`/subagent turns — this is
the only place to see tool calls a subagent made that a top-level
`tool_used` grader can't see (see the L033 grader-blind-spot finding below).
Useful greps:

```bash
# Every tool call the run made, top-level and nested
jq -r 'select(.type=="tool_use") | .name' evals/results/<timestamp>/traces/<case>.jsonl

# Every Bash command actually executed, wherever in the trace it happened
jq -r 'select(.type=="tool_use" and .name=="Bash") | .input.command' \
  evals/results/<timestamp>/traces/<case>.jsonl

# The agent's final message
jq -r 'select(.type=="text")' evals/results/<timestamp>/traces/<case>.jsonl | tail -1

# Grep for a specific lesson's signal anywhere in the run
grep -o 'random_state=42\|seed=42' evals/results/<timestamp>/traces/<case>.jsonl
```

**Deciding whether a grader failure is real.** Cross-check three things
before concluding a case caught a real plugin regression: (1) did the run
actually reach a final answer, or was it cut short by `max_turns`/
`timeout_seconds` (check the last few trace events); (2) is the grader
looking in the right place — a `tool_used` grader is blind to anything a
`Task` subagent did, and a `regex` grader with `target: trace` can match text
inside the agent's own explanation of a wrong answer, not just a reported
value (this is exactly what happened to `L091`'s `no_naive_truncation`
before it was moved to `target: last_message` with a reported-value
pattern — see the 2026-09-28 smoke result below); (3) is the fixture itself
correct — a case can't pass on a fixture that contradicts itself (the L091
`registry_mock.json` stageIV entry, also below). Only once those three are
ruled out should a failing case be treated as a finding about the plugin
rather than about the suite.

## Cost and time (fill in after each real run; last updated 2026-09-28)

| Tier | Cases x runs | Wall time | Cost |
|---|---|---|---|
| load | 8 x 0 (schema only) | ~1s | $0.00 |
| L033 single-case validation run | 1 x 1 | 121s | $0.47 |
| smoke (2026-09-28 real run) | 5 cases x 1 run | 1086s (~18 min) | $9.61 |
| full | 8 cases | not yet run at full scale | not yet run at full scale |
| ablation | 8 cases x 2 arms | not yet run at full scale | not yet run at full scale |

`full`/`ablation` have only been dry-validated for schema (`load`) so far —
run them for real before relying on cost/time estimates in a release
checklist, and update this table from the resulting JSON's
`durationSeconds` / `costUsd`. Turn/timeout budgets: `L020` runs
`max_turns: 20` / `timeout_seconds: 450` (a lighter single-file edit); every
other case (the `/analyze`-pipeline cases: L005, L006, L026, L033, L061,
L091, L092) runs `max_turns: 40` / `timeout_seconds: 900`, raised from 25/600
after the 2026-09-28 smoke run below showed several of them still mid-flight
against the tighter budget (see `L091-full-precision-rounding`'s `routing`
grader failure, "Skill called 0x", below).

### 2026-09-28 smoke result: 1/5 passed, score 0.64, $9.61, 18 min

`overallScore: 0.6433`, `casesPassed: 1/5` (only `L061` passed at
`--threshold 1.0`). Per-case: L005 0.75, L020 0.40, L033 0.667, L061 1.0,
L091 0.40. Trace diagnosis on this run found four distinct failure classes,
three of them suite defects (now fixed in this suite, not plugin
regressions) and one a genuine plugin-behavior finding left as-is:

1. **Trace loss** — the harness deleted every run's `trace.jsonl` from its
   ephemeral `/private/tmp` dir before this diagnosis could inspect most of
   them directly; the classification above was reconstructed from the
   `--json` grader `explanation`/`evidence` fields instead. Fixed:
   `tools/run_evals.sh` now runs with `--keep-temp` and copies every trace
   under `evals/results/<timestamp>/traces/` before cleaning up (see
   "Diagnosing a failure" above).
2. **Fixture contradiction (L091)** — `consistency_judgment` failed 3/3 judge
   votes with evidence `"the stage IV percentage is not safe to paste"`: the
   agent correctly noticed `registry_mock.json`'s stageIV entry claimed to be
   a proportion of the 50-patient cohort while carrying `n: "5/8"`, and
   reasonably declined to report it. `no_naive_truncation` separately failed
   on a false positive (`\b1\.27\b` matched inside the agent's own
   explanation of why naive rounding is wrong, not a reported value). Fixed:
   fixture made internally consistent (`_fixtures/registry_mock.json`,
   `_fixtures/make_fixtures.py`); `no_naive_truncation` now targets
   `last_message` with a reported-value-context pattern; `consistency_judgment`
   now explicitly protects a justified halt on a genuinely ambiguous value.
3. **Grader blind spot (L033)** — `seed_in_code` failed with `"Bash called
   0x"` even though `seed_mentioned_in_answer` (a trace regex) passed,
   meaning a seed of 42 almost certainly *was* used somewhere the agent
   described — just not through a top-level `Bash` call the `tool_used`
   grader could see, because `analyze` delegates code execution to a
   subagent via `Task`. Fixed: the prompt now asks for the analysis script to
   be saved under `scripts/`, and `seed_in_code` is now a `regex` grader over
   produced files instead of a `tool_used: Bash` grader.
4. **Genuine plugin-behavior findings (not suite defects, left as-is)** —
   L020's `banned_terms_removed` and `terminology_consistency` failed because
   the edited abstract still used deprecated race terminology; L005's
   `evalue_judgment` and L091's `routing` ("Skill called 0x") failed on what
   look like real gaps. These are exactly the kind of regression this suite
   exists to catch and were left unmodified — the orchestrator's rerun of
   the fixed smoke tier is what tells you whether they're still failing.

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
   reasonable-sounding option, and neither does `target`: an `llm` grader has
   no way to restrict what it looks at via frontmatter (unlike `regex`, which
   takes `target: trace | files | last_message | {source: file, path: ...}`)
   — case.yaml will fail to load with `graders.N.focus: Invalid input` (or
   `graders.N.target: Unrecognized key(s)`) if you add either. Steer an `llm`
   grader's scope through the `criteria` prose itself instead: say explicitly
   what it should judge (the final message, a specific produced file) and
   what to do if the run never produced a final answer (score it a fail with
   reason "no final answer" — every `llm` grader in this suite says so).
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
- **`llm` graders take no `target` field at all** (confirmed empirically:
  adding `target: last_message` to an existing `llm` grader fails load with
  `graders.N: Unrecognized key(s) in object: 'target'`) — only `regex`
  graders can be scoped with `target`. An `llm` grader's scope has to be
  steered through its `criteria` prose (see "Adding a case" above), not
  through frontmatter.
- **A `regex` grader's `target: trace` matches anywhere in the run**,
  including inside the agent's own explanation of a wrong answer (e.g. "naive
  rounding gives 1.27, not 1.28") — not just a value it actually reported.
  When a lesson is specifically about what the agent *reports* (not what it
  merely discusses), scope the grader to `target: last_message` and pattern
  on a reported-value context (`"= 1.27"`, `"HR 1.27"`, etc.), or switch to
  an `llm` grader with a precise rubric. `target: files` (no `path`) scans
  every file the run produced without needing to know its exact name or
  path — useful for a saved script whose filename the agent chooses itself.
  `target: {source: file, path: <exact path>}` is for a fixture-seeded file
  whose path is known in advance (e.g. `abstract_draft.md`).
- **A top-level `tool_used` grader can't see inside a `Task` subagent call.**
  `analyze` (and other CRA skills) delegate code execution to a subagent via
  `Task`; the subagent's own `Bash` calls never show up to a `tool_used:
  Bash` grader on the parent run, only to a `regex` grader over `target:
  trace` (the full transcript, subagent turns included) or `target: files`
  (whatever the subagent actually wrote to disk). Prefer checking the
  produced artifact over the tool call when a skill might delegate.
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
  5 approval halts before the final report). The `max_turns: 40` /
  `timeout_seconds: 900` budget on every `/analyze`-pipeline case (raised
  2026-09-28 from 25/600 — see the smoke result above) may still not be
  enough for a run to reach Phase 7 (where the analysis report and
  BH-FDR/E-value tables are actually written). Graders here mostly check the
  full conversation `trace` (not just `last_message` or final files) so that
  partial progress toward a lesson's behavior still scores, even when the
  full deliverable doesn't land in budget. A genuine miss is still a genuine
  miss — don't loosen a grader just to make a truncated run pass.
