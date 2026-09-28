#!/usr/bin/env bash
# run_evals.sh — wrapper around `claude plugin eval` for the CRA regression
# eval suite (clinical-research-assistant/evals/).
#
# Usage:
#   tools/run_evals.sh smoke      # tag=smoke cases only, cheap, run before any PR
#   tools/run_evals.sh full       # every case, tag-unfiltered, the full regression suite
#   tools/run_evals.sh ablation   # full suite with a no-plugin baseline arm (with-without)
#   tools/run_evals.sh load       # schema/load validation only, $0 spend, no agent runs
#
# Every tier targets the SOURCE plugin at clinical-research-assistant/ in this
# repo (never the installed ~/.claude/plugins/cache copy) and writes results
# under clinical-research-assistant/evals/results/.
#
# Trace persistence: every non-load tier passes --keep-temp, so each run's
# scaffold dir (and the trace.jsonl inside it) survives past the run instead
# of being deleted from its ephemeral /private/tmp location. After the eval
# command exits, this script reads the tracePath every case/arm/run reported
# in its --json output, copies each surviving trace.jsonl to
# evals/results/<timestamp>/traces/<case>[_<arm>][_runN].jsonl, and then
# removes ONLY the specific kept scaffold directory that trace came from
# (tracePath's parent run directory, e.g. /private/tmp/e-XXXXXX for a
# tracePath of /private/tmp/e-XXXXXX/out/trace.jsonl) -- never anything else.
# See "Diagnosing a failure" in evals/README.md for how to use the saved
# traces.
#
# Exit codes: whatever `claude plugin eval` returns (0 pass, 1 below threshold,
# 2 cost ceiling hit). `load` always exits 0 on a clean schema load. Trace
# extraction/cleanup runs after the eval command regardless of its exit code,
# and does not change that exit code.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_PATH="$REPO_ROOT/clinical-research-assistant"
RESULTS_DIR="$PLUGIN_PATH/evals/results"

TIER="${1:-}"
if [[ -z "$TIER" ]]; then
  echo "Usage: $0 {smoke|full|ablation|load}" >&2
  exit 2
fi

mkdir -p "$RESULTS_DIR"
STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
OUT_JSON="$RESULTS_DIR/${TIER}_${STAMP}.json"

# save_traces <out_json> <traces_dir>
# Reads tracePath from every case/arm/run in <out_json> (the `claude plugin
# eval --json` report), copies each surviving trace.jsonl into <traces_dir>,
# and removes the kept --keep-temp run directory it came from. Safety guard:
# a run directory is only removed when it matches the exact shape
# `claude plugin eval --keep-temp` actually produces (an "e-*" directory
# directly under /tmp or /private/tmp) -- anything else is left in place and
# reported instead of being silently skipped or force-removed.
save_traces() {
  local out_json="$1" traces_dir="$2"
  if [[ ! -f "$out_json" ]]; then
    echo "run_evals.sh: no $out_json produced (run aborted before any output) -- nothing to save" >&2
    return 0
  fi
  mkdir -p "$traces_dir"
  python3 - "$out_json" "$traces_dir" <<'PYEOF'
import json
import os
import shutil
import sys

out_json, traces_dir = sys.argv[1], sys.argv[2]
with open(out_json) as f:
    data = json.load(f)

run_dirs = set()
saved = []

for case in data.get("cases", []):
    case_name = case.get("name", "case")
    arms = case.get("arms") or {}
    multi_arm = len(arms) > 1
    for arm_name, runs in arms.items():
        runs = runs or []
        multi_run = len(runs) > 1
        for i, run in enumerate(runs):
            trace_path = run.get("tracePath")
            if not trace_path or not os.path.isfile(trace_path):
                continue
            dest_name = case_name
            if multi_arm:
                dest_name += f"_{arm_name}"
            if multi_run:
                dest_name += f"_run{i + 1}"
            dest_path = os.path.join(traces_dir, dest_name + ".jsonl")
            shutil.copy2(trace_path, dest_path)
            saved.append(dest_path)
            # tracePath is .../<run-dir>/out/trace.jsonl -- the kept scaffold
            # dir to remove afterward is <run-dir>, two levels up.
            run_dirs.add(os.path.dirname(os.path.dirname(trace_path)))

for p in saved:
    print(f"TRACE_SAVED\t{p}")

if not saved:
    print("run_evals.sh: no tracePath entries found in the run's --json output", file=sys.stderr)

for run_dir in sorted(run_dirs):
    parent = os.path.dirname(run_dir)
    base = os.path.basename(run_dir)
    looks_like_keep_temp_dir = parent in ("/private/tmp", "/tmp") and base.startswith("e-")
    if not os.path.isdir(run_dir):
        continue
    if looks_like_keep_temp_dir:
        shutil.rmtree(run_dir, ignore_errors=True)
        print(f"TEMP_REMOVED\t{run_dir}")
    else:
        # Never rm a path that doesn't match the exact shape we expect --
        # leave it and say so rather than guessing.
        print(f"run_evals.sh: leaving unrecognized temp dir in place (not an e-* dir under /tmp or /private/tmp): {run_dir}", file=sys.stderr)

print(f"TRACES_DIR\t{traces_dir}")
PYEOF
}

COMMON=(--trust-plugin --no-publish --scaffold --keep-temp --allow-tools Bash Write Edit --json "$OUT_JSON")
# Extra arguments after the tier pass straight through, e.g. --case 'L005*' to rerun only failures.
COMMON+=("${@:2}")

case "$TIER" in
  load)
    # Pure schema/load validation. --max-cost-usd 0 aborts before any agent
    # run launches (verified empirically: the doc'd 0.01 ceiling still lets
    # the first case run to completion, since cost is checked BEFORE each
    # launch and starts at $0; 0 blocks even the first launch). Prints a
    # per-case warning list (tool-grant advisories) and an aggregate with
    # casesTotal reflecting only cases that actually ran (0 here) -- the
    # per-case warnings above the JSON are what confirm 8/8 cases parsed.
    # No agent ever runs, so there is no trace.jsonl to keep -- --keep-temp
    # is intentionally omitted here.
    exec claude plugin eval "$PLUGIN_PATH" \
      --trust-plugin --no-publish --ablation none --max-cost-usd 0 --json "$OUT_JSON"
    ;;
  smoke|full|ablation)
    case "$TIER" in
      smoke)    RUN_ARGS=(--ablation none --tag smoke --max-cost-usd 10 -j 2) ;;
      full)     RUN_ARGS=(--ablation none --max-cost-usd 40 -j 2) ;;
      ablation) RUN_ARGS=(--ablation with-without --max-cost-usd 80 -j 2) ;;
    esac
    TRACES_DIR="$RESULTS_DIR/$STAMP/traces"

    set +e
    claude plugin eval "$PLUGIN_PATH" "${COMMON[@]}" "${RUN_ARGS[@]}"
    CODE=$?
    set -e

    save_traces "$OUT_JSON" "$TRACES_DIR"
    echo "run_evals.sh: traces saved under $TRACES_DIR" >&2

    exit "$CODE"
    ;;
  *)
    echo "Unknown tier: $TIER (expected smoke|full|ablation|load)" >&2
    exit 2
    ;;
esac
