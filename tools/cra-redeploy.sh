#!/usr/bin/env bash
# cra-redeploy.sh — reconcile the DEPLOYED plugin cache with THIS source repo, safely.
#
# Companion to cra-cache-drift-check.sh. That script REPORTS drift; this one FIXES the
# half of it that can be fixed without losing work.
#
# The asymmetry that makes auto-fix safe:
#
#   repo newer + committed  → the cache is a stale deployment artifact. Overwriting it
#                             loses nothing, because anything the cache held on its own
#                             would have given it the newer mtime. AUTO-FIXED.
#   cache newer             → a session edited the deployed skill directly (the skill
#                             router prints the cache path, so this happens). That is real
#                             un-ingested work. NEVER overwritten — reported for manual
#                             ingest into the repo.
#   repo newer + uncommitted → source edit not yet committed. Not deployed, so a bad edit
#                             cannot reach the live plugin. Reported, not deployed.
#
# Every overwrite is backed up first to ~/.claude/plugins/.cra-redeploy-backups/<stamp>/.
#
# Usage:
#   bash tools/cra-redeploy.sh            # detect direction per file, auto-fix the safe ones
#   bash tools/cra-redeploy.sh --dry-run  # report what it would do, touch nothing
#   bash tools/cra-redeploy.sh --to-cache # force repo → cache for ALL differing files
#
# Exit codes:
#   0  fully in sync (possibly after fixing)
#   1  drift remains that needs a human (cache ahead, or uncommitted source)
#   2  setup problem (no repo, no cache, bad version)

set -uo pipefail

DRY_RUN=0
FORCE_TO_CACHE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --to-cache) FORCE_TO_CACHE=1 ;;
    -h|--help) sed -n '2,32p' "$0"; exit 0 ;;
    *) printf 'unknown argument: %s\n' "$arg" >&2; exit 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_SRC="$REPO_ROOT/clinical-research-assistant"

if [[ -t 1 ]]; then GREEN=$'\033[32m'; RED=$'\033[31m'; YELLOW=$'\033[33m'; DIM=$'\033[2m'; RESET=$'\033[0m'
else GREEN=''; RED=''; YELLOW=''; DIM=''; RESET=''; fi

VERSION="$(python3 -c "import json;print(json.load(open('$PLUGIN_SRC/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || true)"
if [[ -z "$VERSION" ]]; then
  printf "${RED}✗ cannot read plugin version from %s${RESET}\n" "$PLUGIN_SRC/.claude-plugin/plugin.json"
  exit 2
fi

CACHE=""
for d in "$HOME"/.claude/plugins/cache/*/clinical-research-assistant/"$VERSION"; do
  [[ -d "$d" ]] && CACHE="$d" && break
done
[[ -z "$CACHE" && -d "$HOME/.claude/plugins/clinical-research-assistant" ]] && CACHE="$HOME/.claude/plugins/clinical-research-assistant"

if [[ -z "$CACHE" ]]; then
  printf "${YELLOW}… no deployed CRA plugin cache for v%s — nothing to redeploy.${RESET}\n" "$VERSION"
  exit 0
fi

# Runtime artifacts that are never part of the plugin payload.
is_noise() {
  case "$1" in
    .git|.git/*|*/.git/*|*__pycache__*|*.pyc|*.DS_Store) return 0 ;;
    .in_use|.in_use/*|*/.in_use|*/.in_use/*) return 0 ;;
    *) return 1 ;;
  esac
}

list_files() {  # $1 = root; prints relative paths
  ( cd "$1" 2>/dev/null && find . -type f 2>/dev/null | sed 's|^\./||' )
}

mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0; }

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="$HOME/.claude/plugins/.cra-redeploy-backups/$STAMP"

printf "repo  : %s ${GREEN}(v%s)${RESET}\n" "$PLUGIN_SRC" "$VERSION"
printf "cache : %s\n" "$CACHE"
[[ $DRY_RUN -eq 1 ]] && printf "${DIM}(dry run — nothing will be written)${RESET}\n"

deployed=0; blocked=0; cache_ahead=0

backup_then_copy() {  # $1 = src, $2 = dest, $3 = relpath
  if [[ $DRY_RUN -eq 1 ]]; then return 0; fi
  if [[ -f "$2" ]]; then
    mkdir -p "$BACKUP_DIR/$(dirname "$3")"
    cp -p "$2" "$BACKUP_DIR/$3"
  fi
  mkdir -p "$(dirname "$2")"
  cp -p "$1" "$2"
}

# Union of both trees.
ALL="$( { list_files "$PLUGIN_SRC"; list_files "$CACHE"; } | sort -u )"

while IFS= read -r rel; do
  [[ -z "$rel" ]] && continue
  is_noise "$rel" && continue

  R="$PLUGIN_SRC/$rel"
  C="$CACHE/$rel"

  # Present in cache only — a session may have created it there. Never delete.
  if [[ ! -f "$R" && -f "$C" ]]; then
    printf "${YELLOW}⚠ cache-only${RESET}  %s\n" "$rel"
    printf "    ${DIM}not in source — ingest with: cp '%s' '%s'${RESET}\n" "$C" "$R"
    cache_ahead=$((cache_ahead+1))
    continue
  fi

  # Present in repo only — additive deploy, safe.
  if [[ -f "$R" && ! -f "$C" ]]; then
    if [[ $FORCE_TO_CACHE -eq 1 ]] || git -C "$REPO_ROOT" ls-files --error-unmatch "$R" >/dev/null 2>&1; then
      backup_then_copy "$R" "$C" "$rel"
      printf "${GREEN}→ deployed${RESET}   %s ${DIM}(new file)${RESET}\n" "$rel"
      deployed=$((deployed+1))
    else
      printf "${YELLOW}⚠ untracked${RESET}   %s ${DIM}(new in source, not committed — not deployed)${RESET}\n" "$rel"
      blocked=$((blocked+1))
    fi
    continue
  fi

  cmp -s "$R" "$C" && continue   # identical, nothing to do

  if [[ $FORCE_TO_CACHE -eq 1 ]]; then
    backup_then_copy "$R" "$C" "$rel"
    printf "${GREEN}→ deployed${RESET}   %s ${DIM}(forced)${RESET}\n" "$rel"
    deployed=$((deployed+1))
    continue
  fi

  if [[ "$(mtime "$C")" -gt "$(mtime "$R")" ]]; then
    printf "${YELLOW}⚠ cache ahead${RESET} %s\n" "$rel"
    printf "    ${DIM}session edited the deployed plugin. Review, then copy into the repo and commit:${RESET}\n"
    printf "    ${DIM}diff -u '%s' '%s'${RESET}\n" "$R" "$C"
    cache_ahead=$((cache_ahead+1))
    continue
  fi

  # Repo is newer. Deploy only if that version is committed.
  if git -C "$REPO_ROOT" status --porcelain -- "$R" 2>/dev/null | grep -q .; then
    printf "${YELLOW}⚠ uncommitted${RESET} %s ${DIM}(source newer but dirty — commit, then redeploy)${RESET}\n" "$rel"
    blocked=$((blocked+1))
    continue
  fi

  backup_then_copy "$R" "$C" "$rel"
  printf "${GREEN}→ deployed${RESET}   %s\n" "$rel"
  deployed=$((deployed+1))
done <<< "$ALL"

printf "\n"
if [[ $deployed -eq 0 && $cache_ahead -eq 0 && $blocked -eq 0 ]]; then
  printf "${GREEN}✓ in sync${RESET} — deployed cache matches the source repo.\n"
  exit 0
fi

[[ $deployed -gt 0 ]] && printf "${GREEN}✓ redeployed %d file(s) repo→cache${RESET}%s\n" "$deployed" \
  "$([[ $DRY_RUN -eq 0 ]] && printf ' (backups: %s)' "$BACKUP_DIR")"
[[ $cache_ahead -gt 0 ]] && printf "${RED}✗ %d file(s) where the CACHE is ahead — needs manual ingest (see above)${RESET}\n" "$cache_ahead"
[[ $blocked -gt 0 ]] && printf "${YELLOW}⚠ %d file(s) blocked on an uncommitted source edit${RESET}\n" "$blocked"

if [[ $cache_ahead -gt 0 || $blocked -gt 0 ]]; then exit 1; fi
exit 0
