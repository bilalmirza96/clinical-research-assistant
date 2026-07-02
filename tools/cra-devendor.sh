#!/usr/bin/env bash
# cra-devendor.sh — STAGED migration: drop vendored scientific-skills that have a native namesake.
#
# Context (per L058): CRA vendors 138 scientific-skills under
#   clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills/
# The `claude-scientific-skills` plugin now installs the full K-Dense library NATIVELY
# (173 skills, a superset). Every `scientific-skills:<name>` reference resolves to the native
# skill `<name>` (see analyze/references/delegation-matrix.md → "Namespace resolution").
# The vendored copies are ~21 MB of dead weight and a silent-drift surface.
#
# This script drops ONLY the vendored skills that have a native namesake and RETAINS the
# CRA-local skills that do not exist natively (else they would be lost).
#
# ┌─ SAFETY ────────────────────────────────────────────────────────────────────────────┐
# │ DRY-RUN BY DEFAULT. It prints what it *would* delete and changes nothing.            │
# │ Pass --apply to actually delete. Even then it refuses unless the native plugin is    │
# │ present and covers every skill being dropped.                                        │
# │                                                                                       │
# │ PRECONDITION NOT YET MET: the vendored FILE-PATH references in                        │
# │   clinical-research-assistant/skills/references/kdense-delegations.md                 │
# │ (e.g. "Skill path: skills/external/.../<name>/SKILL.md") must first be rewired to the │
# │ native skill name, or they will 404 after deletion. This script warns if they remain.│
# └───────────────────────────────────────────────────────────────────────────────────────┘

set -uo pipefail

APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VEND="$REPO_ROOT/clinical-research-assistant/skills/external/scientific-agent-skills/scientific-skills"
NATIVE="$HOME/.claude/plugins/claude-scientific-skills/scientific-skills"
KDENSE_REF="$REPO_ROOT/clinical-research-assistant/skills/references/kdense-delegations.md"

if [[ -t 1 ]]; then GREEN=$'\033[32m'; RED=$'\033[31m'; YELLOW=$'\033[33m'; RESET=$'\033[0m'
else GREEN=''; RED=''; YELLOW=''; RESET=''; fi

[[ -d "$VEND" ]]   || { printf "${RED}✗ vendored dir not found: %s${RESET}\n" "$VEND"; exit 1; }
[[ -d "$NATIVE" ]] || { printf "${RED}✗ native claude-scientific-skills not installed at %s — refusing.${RESET}\n" "$NATIVE"; exit 1; }

# CRA-local skills with no native namesake — NEVER drop these.
KEEP=(autoskill bids database-lookup exa-search hugging-science optimize-for-gpu paper-lookup paperzilla polars-bio primekg)
is_keep() { local n="$1"; for k in "${KEEP[@]}"; do [[ "$k" == "$n" ]] && return 0; done; return 1; }

drop=(); keep=(); orphan=()
while IFS= read -r name; do
  [[ -z "$name" ]] && continue
  if is_keep "$name"; then keep+=("$name"); continue; fi
  if [[ -d "$NATIVE/$name" ]]; then drop+=("$name"); else orphan+=("$name"); fi
done < <(ls "$VEND" 2>/dev/null | sort)

printf "vendored : %s\n" "$VEND"
printf "native   : %s (%s skills)\n\n" "$NATIVE" "$(ls "$NATIVE" | wc -l | tr -d ' ')"
printf "${GREEN}DROP (native namesake exists): %s${RESET}\n" "${#drop[@]}"
printf "${YELLOW}KEEP (CRA-local, no native)  : %s → %s${RESET}\n" "${#keep[@]}" "${keep[*]}"
if (( ${#orphan[@]} )); then
  printf "${RED}UNEXPECTED ORPHANS (no native, not in KEEP list): %s → %s${RESET}\n" "${#orphan[@]}" "${orphan[*]}"
  printf "${RED}  Refusing to proceed — update the KEEP list or investigate before dropping.${RESET}\n"
  exit 1
fi

# Warn if the file-path references haven't been rewired yet.
if grep -q "skills/external/scientific-agent-skills" "$KDENSE_REF" 2>/dev/null; then
  printf "\n${YELLOW}⚠ %s still contains vendored file-path references (skills/external/...).\n  Rewire these to native skill names BEFORE --apply, or they will 404.${RESET}\n" "${KDENSE_REF##*$REPO_ROOT/}"
  REWIRE_PENDING=1
else
  REWIRE_PENDING=0
fi

if (( APPLY == 0 )); then
  printf "\n${GREEN}DRY RUN — nothing deleted.${RESET} Re-run with --apply to remove the %s DROP skills.\n" "${#drop[@]}"
  exit 0
fi

if (( REWIRE_PENDING == 1 )); then
  printf "\n${RED}✗ --apply refused: rewire kdense-delegations.md vendored paths first.${RESET}\n"
  exit 1
fi

for name in "${drop[@]}"; do rm -rf "${VEND:?}/$name"; done
printf "\n${GREEN}✓ removed %s vendored skills; retained %s CRA-local.${RESET}\n" "${#drop[@]}" "${#keep[@]}"
printf "Next: regenerate skills/references/skill-registry.yaml, bump the plugin version, commit, and reinstall.\n"
