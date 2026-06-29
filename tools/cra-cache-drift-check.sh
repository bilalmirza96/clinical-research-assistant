#!/usr/bin/env bash
# cra-cache-drift-check.sh — detect drift between the DEPLOYED plugin cache and THIS source repo.
#
# Why this exists: the plugin that `Skill` actually loads lives in the marketplace cache
# (~/.claude/plugins/cache/<marketplace>/clinical-research-assistant/<version>/), NOT in this repo.
# Sessions sometimes edit that cache directly (it's the path the skill router prints), so the
# deployed plugin can silently drift ahead of the source repo. This script makes that drift visible.
#
# Run from anywhere — resolves the repo root from its own location:
#   $ bash tools/cra-cache-drift-check.sh
#
# Exit codes:
#   0  cache matches repo (or no deployed cache found on this machine)
#   1  drift detected — deployed cache differs from the source repo
#
# Use as a session-start check, a pre-commit hook, or a CI gate.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_SRC="$REPO_ROOT/clinical-research-assistant"

if [[ -t 1 ]]; then GREEN=$'\033[32m'; RED=$'\033[31m'; YELLOW=$'\033[33m'; RESET=$'\033[0m'
else GREEN=''; RED=''; YELLOW=''; RESET=''; fi

VERSION="$(python3 -c "import json;print(json.load(open('$PLUGIN_SRC/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || true)"
if [[ -z "$VERSION" ]]; then
  printf "${RED}✗ cannot read plugin version from %s${RESET}\n" "$PLUGIN_SRC/.claude-plugin/plugin.json"
  exit 1
fi

# Locate the deployed cache (marketplace dir name may vary; version is in the path).
CACHE=""
for d in "$HOME"/.claude/plugins/cache/*/clinical-research-assistant/"$VERSION"; do
  [[ -d "$d" ]] && CACHE="$d" && break
done
# Legacy flat install fallback.
[[ -z "$CACHE" && -d "$HOME/.claude/plugins/clinical-research-assistant" ]] && CACHE="$HOME/.claude/plugins/clinical-research-assistant"

if [[ -z "$CACHE" ]]; then
  printf "${YELLOW}… no deployed CRA plugin cache found for v%s — plugin not installed here, skipping.${RESET}\n" "$VERSION"
  exit 0
fi

printf "repo  : %s ${GREEN}(v%s)${RESET}\n" "$PLUGIN_SRC" "$VERSION"
printf "cache : %s\n" "$CACHE"

# Ignore install markers and OS/python noise; compare the actual plugin payload.
DRIFT="$(diff -rq "$CACHE" "$PLUGIN_SRC" 2>/dev/null | grep -vE '/\.git($|/)|__pycache__|\.DS_Store|\.in_use|\.pyc')"

if [[ -z "$DRIFT" ]]; then
  printf "${GREEN}✓ in sync${RESET} — deployed cache matches the source repo.\n"
  exit 0
fi

printf "${RED}✗ DRIFT DETECTED${RESET} — deployed cache differs from the source repo:\n"
printf "%s\n\n" "$DRIFT"
printf "Reconcile before committing:\n"
printf "  • cache has the newer edits → copy them into %s and commit (this is the usual case).\n" "$PLUGIN_SRC"
printf "  • repo is newer            → reinstall the plugin, or copy repo→cache to redeploy.\n"
exit 1
