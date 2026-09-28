#!/usr/bin/env bash
# Scaffold for L033-random-seed-everywhere. Copies the synthetic fixture data
# into the throwaway eval workspace. Runs with the workspace as cwd; resolves
# fixture sources relative to this script's own location so it works
# regardless of cwd.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES="$SCRIPT_DIR/../_fixtures"

mkdir -p data Reports
cp "$FIXTURES/cohort_50.csv" data/cohort_50.csv
cp "$FIXTURES/project_CLAUDE.md" CLAUDE.md
