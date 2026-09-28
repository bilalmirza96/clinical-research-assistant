#!/usr/bin/env bash
# Scaffold for L020-abstract-race-terminology. Seeds the rough abstract draft
# (banned race terminology, mixed decimal precision) at the workspace root.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES="$SCRIPT_DIR/../_fixtures"

cp "$FIXTURES/abstract_draft.md" abstract_draft.md
cp "$FIXTURES/project_CLAUDE.md" CLAUDE.md
