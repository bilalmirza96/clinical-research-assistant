# Numeric guards: `number_format.py` and `gates.py`

Two reusable, stdlib-only tools generalized from the REPEAT DISPARITIES project's per-project
scripts (`manuscript_format.py`, `render_manuscript_numbers.py --strict`, `run_a11_precision.py`)
and lessons L087-L098. Import them; do not re-derive their rules per project.

- **`tools/number_format.py`** - one Decimal half-up formatter. `fmt(value, dp)` rounds once,
  half-up, never printing `-0.00`. `fmt_estimate(point, lo, hi, dp=None)` prints a point estimate
  and its CI limits at ONE shared precision (L097: fewest decimals held by any of the three,
  never below the main-text default of 2dp). `from_registry(entry, path="")` resolves a value
  out of a registry result, preferring the full-precision companion `current["fp"]` over the
  stored `current["value"]` (L091). `boundary_guard(stored_value, dp, fp=None)` raises
  `BoundaryError` when a stored, already-rounded value sits exactly on a half-rounding boundary
  at `dp` decimals and no `fp` companion resolves the ambiguity. `now_stamp(clock=None)` stamps
  the current date/time at call time (L098) - never a hardcoded `DATE = "..."` constant.

- **`skills/internal/analyze/scripts/gates.py`** - between-rung invariants for the analysis
  ladder, each a `(ok, message)` function: `cohort_n` (exact-N reconciliation across
  crude/modelA/modelB and every exposure group, against a pre-registered curated cohort size),
  `denominator_named` (every result states its population/denominator), `dictionary_labels`
  (every categorical level used to slice a result is dossier-defined; reuses
  `dictionary_audit.py`), `two_adjusted_models` (no third adjusted model; reuses
  `ladder_table.py`'s rung vocabulary), `no_penalizer` (grep for a nonzero lifelines
  `penalizer=`), `run_time_dates` (grep for a hardcoded `DATE = "YYYY-MM-DD"` in a record
  writer). **A failed gate means the chain stops** - fix it, or document why the check does not
  apply to this analysis, before moving to the next rung or rendering a deliverable.

## How to wire these in

- **`analyze` phases**: after each ladder rung is computed and upserted into the registry, run
  the `gates.py` CLI for that rung before starting the next one (`cohort-n` after Model B;
  `two-adjusted-models` before starting IPTW/PSM; `no-penalizer` over every script that fits a
  Cox model; `dictionary-labels` once a categorical breakdown is registered). Any record-writer
  script (an `analysis_registry.py upsert` wrapper, an A-series precision-refit script) should
  call `NF.now_stamp()` for its date argument rather than a module constant, and `run-time-dates`
  can grep the finished script for a regression.
- **`write-*` skills**: when a draft renders numbers from the registry (the project's own
  `render_manuscript_numbers.py --strict` pattern), prefer `NF.from_registry` + `NF.fmt` /
  `NF.fmt_estimate` over hand-rolled rounding, and run `number_format.py --check REGISTRY.json
  --dp <precision>` as a pre-render audit for boundary values with no `fp` companion.
- **CLI use in a build step**:
  ```
  python3 tools/number_format.py --check Reports/MASTER_ANALYSIS_REGISTRY.json --dp 2
  python3 skills/internal/analyze/scripts/gates.py cohort-n --registry REG.json \
      --expected '{"NHB": 5000, "NHW": 20000}'
  python3 skills/internal/analyze/scripts/gates.py two-adjusted-models --registry REG.json
  python3 skills/internal/analyze/scripts/gates.py no-penalizer Scripts/run_*.py
  ```
  Every subcommand and the `--check` mode exit 1 on failure, so they compose into any CI-style
  script without extra parsing.

Tests: `python3 tools/tests/test_number_format.py`, `python3 tools/tests/test_gates.py`.
