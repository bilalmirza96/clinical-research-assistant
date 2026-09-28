#!/usr/bin/env python3
"""UserPromptSubmit hook: inject only the CRA lessons relevant to the current prompt.

Reads clinical-research-assistant/skills/references/lessons-log.json (located
relative to this script's own path, never via cwd), scores each lesson's
trigger_patterns against the incoming prompt, and emits the top matches as
additionalContext for the model to apply before acting.

Contract (Claude Code UserPromptSubmit hooks):
  stdin:  JSON {"prompt": ..., "session_id": ..., "cwd": ..., "hook_event_name": ...}
  stdout: JSON {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                        "additionalContext": "<text>"}}  (exit 0)
          or nothing at all (exit 0) when there is nothing worth adding.
  This hook must never exit non-zero and must never print to stdout on error
  (fail open — a broken hook must not break the user's prompt).

Run under 150 ms for a lessons-log.json of ~100 entries.
"""
import json
import os
import re
import sys

# ---------------------------------------------------------------- constants

MIN_PROMPT_LEN = 12
MAX_LESSONS = 6
MIN_SCORE = 2
MAX_RULE_CHARS = 240
MAX_BLOCK_CHARS = 1500
HEADER = "CRA lessons matching this prompt (from lessons-log.json; apply before acting):"

SEVERITY_WEIGHTS = {
    "CRITICAL": 3,
    "HIGH": 3,
    "MEDIUM": 2,
    "MODERATE": 2,
    "LOW": 1,
}
DEFAULT_WEIGHT = 2  # missing / unrecognized severity value (e.g. None, "standing-rule")

# Bare acknowledgements that should never trigger a lookup even if long enough.
_ACK_PATTERN = re.compile(
    r"^(ok(ay)?|yes|yes please|no|no thanks|thanks|thank you|sure|sounds good|"
    r"got it|great|perfect|cool|continue|go ahead|proceed|do it|sounds great)[.!]?$",
    re.IGNORECASE,
)


def _lessons_log_path():
    # Locate relative to this script's own path: hooks/lessons_recall.py ->
    # ../skills/references/lessons-log.json
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "skills", "references", "lessons-log.json")


def _load_lessons(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    lessons = data.get("lessons", []) if isinstance(data, dict) else data
    return lessons or []


def _should_skip(prompt):
    stripped = prompt.strip()
    if len(stripped) < MIN_PROMPT_LEN:
        return True
    if stripped.startswith("/"):
        # Bare slash command (with or without arguments) is routing, not a
        # research question the lessons log should weigh in on.
        return True
    if _ACK_PATTERN.match(stripped):
        return True
    return False


def _severity_weight(severity):
    if not isinstance(severity, str):
        return DEFAULT_WEIGHT
    return SEVERITY_WEIGHTS.get(severity.strip().upper(), DEFAULT_WEIGHT)


def _pattern_matches(pattern, prompt_lower):
    if not pattern:
        return False
    pat_lower = pattern.lower()
    needs_word_boundary = len(pattern) <= 4 or not re.search(r"[a-zA-Z]", pattern)
    if needs_word_boundary:
        return re.search(r"\b" + re.escape(pat_lower) + r"\b", prompt_lower) is not None
    return pat_lower in prompt_lower


def _actionable_line(lesson):
    # Different eras of the log use different keys for the actionable line;
    # prefer the most explicit one available.
    for key in ("rule", "action", "lesson"):
        val = lesson.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _score_lessons(lessons, prompt):
    prompt_lower = prompt.lower()
    scored = []
    seen_ids = set()
    for lesson in lessons:
        lid = lesson.get("id")
        if not lid or lid in seen_ids:
            continue
        patterns = lesson.get("trigger_patterns") or []
        match_count = sum(1 for p in patterns if _pattern_matches(p, prompt_lower))
        if match_count == 0:
            continue
        weight = _severity_weight(lesson.get("severity"))
        score = match_count * weight
        if score < MIN_SCORE:
            continue
        seen_ids.add(lid)
        scored.append((score, lid, lesson))
    # Highest score first; stable tie-break on id for determinism.
    scored.sort(key=lambda t: (-t[0], t[1]))
    return scored[:MAX_LESSONS]


def _format_block(scored):
    if not scored:
        return ""
    lines = [HEADER]
    for score, lid, lesson in scored:
        severity = lesson.get("severity")
        severity_label = severity.strip().upper() if isinstance(severity, str) and severity.strip() else "UNRATED"
        rule = _actionable_line(lesson)
        if len(rule) > MAX_RULE_CHARS:
            rule = rule[: MAX_RULE_CHARS - 1].rstrip() + "…"
        lines.append(f"- {lid} [{severity_label}]: {rule}")
    block = "\n".join(lines)
    if len(block) > MAX_BLOCK_CHARS:
        block = block[: MAX_BLOCK_CHARS - 1].rstrip() + "…"
    return block


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw)
        prompt = payload.get("prompt", "")
        if not isinstance(prompt, str) or _should_skip(prompt):
            return 0

        lessons = _load_lessons(_lessons_log_path())
        scored = _score_lessons(lessons, prompt)
        block = _format_block(scored)
        if not block:
            return 0

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": block,
            }
        }
        sys.stdout.write(json.dumps(output))
        return 0
    except Exception:
        # Fail open: never surface an error to stdout, never exit non-zero.
        return 0


if __name__ == "__main__":
    sys.exit(main())
