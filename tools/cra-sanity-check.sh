#!/usr/bin/env bash
# cra-sanity-check.sh — verifies every path referenced by AGENTS.md §5–§6 resolves
#
# Run from anywhere — script resolves the repo root from its own location.
#   $ bash tools/cra-sanity-check.sh
#   $ ./tools/cra-sanity-check.sh
#
# Exit codes:
#   0  all paths resolve, lessons-log ≥ 47 entries, K-Dense count == 138
#   1  one or more paths missing OR lessons-log count below threshold
#
# Use as a pre-commit hook, a session-start sanity check, or a CI gate.

set -uo pipefail

# ── Resolve repo root from script location ──────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/clinical-research-assistant/skills"
KDENSE_ROOT="$SKILLS_ROOT/external/scientific-agent-skills/scientific-skills"

# ── Colors (disabled if not a tty) ──────────────────────────────────────
if [[ -t 1 ]]; then
  GREEN=$'\033[32m'; RED=$'\033[31m'; YELLOW=$'\033[33m'; RESET=$'\033[0m'
else
  GREEN=''; RED=''; YELLOW=''; RESET=''
fi

# ── Expected paths (kept in sync with AGENTS.md §5–§6) ──────────────────
EXPECTED_INTERNAL_SKILLS=(
  analyze
  data-analysis
  literature-review
  manuscript-qc
  project-init
  resume-project
  visualize
  write-abstract
  write-discussion
  write-introduction
  write-manuscript
  write-methods-results
)

EXPECTED_REFERENCES=(
  biomedagent-methodology.md
  command-contracts.md
  external-skills.md
  kdense-delegations.md
  lessons-log.json
  skill-registry.yaml
  state-schema.md
  writing-style.md
)

EXPECTED_KDENSE_DELEGATIONS=(
  citation-management
  peer-review
  scholar-evaluation
  pyzotero
  literature-review
)

ROUTER_SKILL="$SKILLS_ROOT/clinical-research-assistant/SKILL.md"
LESSONS_LOG="$SKILLS_ROOT/references/lessons-log.json"
EXPECTED_KDENSE_COUNT=138
EXPECTED_MIN_LESSONS=47

# ── Counters ────────────────────────────────────────────────────────────
fail=0
warn=0

check_file () {
  local label="$1" path="$2"
  if [[ -f "$path" ]]; then
    printf "  ${GREEN}✓${RESET} %s\n" "$label"
  else
    printf "  ${RED}✗ MISSING${RESET} %s  (expected at %s)\n" "$label" "${path#$REPO_ROOT/}"
    fail=$((fail + 1))
  fi
}

# ── Header ──────────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════════════════════"
echo "  CRA sanity check"
echo "  Repo root: $REPO_ROOT"
echo "════════════════════════════════════════════════════════════════"

# ── Router skill ─────────────────────────────────────────────────────────
echo
echo "Router skill:"
check_file "clinical-research-assistant (router)" "$ROUTER_SKILL"

# ── Internal skills (12) ────────────────────────────────────────────────
echo
echo "Internal CRA skills (expected 12):"
for skill in "${EXPECTED_INTERNAL_SKILLS[@]}"; do
  check_file "$skill" "$SKILLS_ROOT/internal/$skill/SKILL.md"
done

# ── Reference docs (8) ──────────────────────────────────────────────────
echo
echo "Reference docs (expected 8):"
for ref in "${EXPECTED_REFERENCES[@]}"; do
  check_file "$ref" "$SKILLS_ROOT/references/$ref"
done

# ── K-Dense delegation targets (5) ──────────────────────────────────────
echo
echo "K-Dense delegation targets (expected 5):"
for kd in "${EXPECTED_KDENSE_DELEGATIONS[@]}"; do
  check_file "$kd/SKILL.md" "$KDENSE_ROOT/$kd/SKILL.md"
done

# ── K-Dense total skill count ───────────────────────────────────────────
echo
if [[ -d "$KDENSE_ROOT" ]]; then
  kdense_count=$(ls -1 "$KDENSE_ROOT" 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$kdense_count" -eq "$EXPECTED_KDENSE_COUNT" ]]; then
    printf "K-Dense skill count: ${GREEN}%s${RESET} (expected %s) ✓\n" "$kdense_count" "$EXPECTED_KDENSE_COUNT"
  else
    printf "K-Dense skill count: ${YELLOW}%s${RESET} (expected %s) — drift detected, update AGENTS.md if intentional\n" \
      "$kdense_count" "$EXPECTED_KDENSE_COUNT"
    warn=$((warn + 1))
  fi
else
  printf "${RED}✗${RESET} K-Dense root missing: %s\n" "${KDENSE_ROOT#$REPO_ROOT/}"
  fail=$((fail + 1))
fi

# ── Lessons-log entry count ─────────────────────────────────────────────
echo
if [[ -f "$LESSONS_LOG" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    lesson_count=$(python3 -c "
import json, sys
with open('$LESSONS_LOG') as f:
    data = json.load(f)
if isinstance(data, dict) and 'lessons' in data:
    print(len(data['lessons']))
elif isinstance(data, list):
    print(len(data))
else:
    print(0)
" 2>/dev/null || echo "?")
    if [[ "$lesson_count" == "?" ]]; then
      printf "${YELLOW}⚠${RESET} Could not parse lessons-log.json\n"
      warn=$((warn + 1))
    elif [[ "$lesson_count" -ge "$EXPECTED_MIN_LESSONS" ]]; then
      printf "Lessons-log entries: ${GREEN}%s${RESET} (≥ %s expected) ✓\n" "$lesson_count" "$EXPECTED_MIN_LESSONS"
    else
      printf "Lessons-log entries: ${RED}%s${RESET} (< %s expected) — regression?\n" "$lesson_count" "$EXPECTED_MIN_LESSONS"
      fail=$((fail + 1))
    fi
  else
    printf "${YELLOW}⚠${RESET} python3 not available; skipping lessons-log count\n"
    warn=$((warn + 1))
  fi
fi

# ── AGENTS.md presence ──────────────────────────────────────────────────
echo
check_file "AGENTS.md (Codex operating brief)" "$REPO_ROOT/AGENTS.md"

# ── Summary ─────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════"
if [[ $fail -eq 0 && $warn -eq 0 ]]; then
  printf "  ${GREEN}SANITY OK${RESET} — all paths resolve, counts match expected\n"
elif [[ $fail -eq 0 ]]; then
  printf "  ${YELLOW}SANITY OK (with %d warning(s))${RESET}\n" "$warn"
else
  printf "  ${RED}SANITY FAILED${RESET} — %d missing path(s), %d warning(s)\n" "$fail" "$warn"
fi
echo "════════════════════════════════════════════════════════════════"

[[ $fail -eq 0 ]] && exit 0 || exit 1
