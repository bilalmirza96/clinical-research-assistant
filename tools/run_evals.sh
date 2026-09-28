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
# Exit codes: whatever `claude plugin eval` returns (0 pass, 1 below threshold,
# 2 cost ceiling hit). `load` always exits 0 on a clean schema load.

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

COMMON=(--trust-plugin --no-publish --scaffold --allow-tools Bash Write Edit --json "$OUT_JSON")

case "$TIER" in
  load)
    # Pure schema/load validation. --max-cost-usd 0 aborts before any agent
    # run launches (verified empirically: the doc'd 0.01 ceiling still lets
    # the first case run to completion, since cost is checked BEFORE each
    # launch and starts at $0; 0 blocks even the first launch). Prints a
    # per-case warning list (tool-grant advisories) and an aggregate with
    # casesTotal reflecting only cases that actually ran (0 here) -- the
    # per-case warnings above the JSON are what confirm 8/8 cases parsed.
    exec claude plugin eval "$PLUGIN_PATH" \
      --trust-plugin --no-publish --ablation none --max-cost-usd 0 --json "$OUT_JSON"
    ;;
  smoke)
    exec claude plugin eval "$PLUGIN_PATH" \
      "${COMMON[@]}" --ablation none --tag smoke --max-cost-usd 10 -j 2
    ;;
  full)
    exec claude plugin eval "$PLUGIN_PATH" \
      "${COMMON[@]}" --ablation none --max-cost-usd 40 -j 2
    ;;
  ablation)
    exec claude plugin eval "$PLUGIN_PATH" \
      "${COMMON[@]}" --ablation with-without --max-cost-usd 80 -j 2
    ;;
  *)
    echo "Unknown tier: $TIER (expected smoke|full|ablation|load)" >&2
    exit 2
    ;;
esac
