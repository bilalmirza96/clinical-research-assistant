#!/usr/bin/env bash
# Scaffold for L091-full-precision-rounding. Seeds a pre-existing results
# registry (mirroring MASTER_ANALYSIS_REGISTRY.json) so the agent reads
# locked values rather than recomputing them.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES="$SCRIPT_DIR/../_fixtures"

mkdir -p data Reports
cp "$FIXTURES/cohort_50.csv" data/cohort_50.csv
cp "$FIXTURES/registry_mock.json" Reports/MASTER_ANALYSIS_REGISTRY.json
cp "$FIXTURES/project_CLAUDE.md" CLAUDE.md
