#!/usr/bin/env bash
# Scaffold for L061-genie-panel-offpanel-not-wildtype. Deliberately does NOT
# copy tmb_panel_coverage.json (the answer key for which genes each panel
# covers) -- the agent must infer panel coverage from the long-format data
# itself, the same way it would have to with real AACR GENIE data.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES="$SCRIPT_DIR/../_fixtures"

mkdir -p data Reports
cp "$FIXTURES/tmb_mixed.csv" data/tmb_mixed.csv
cp "$FIXTURES/project_CLAUDE.md" CLAUDE.md
