#!/usr/bin/env python3
"""voice_check.py — mechanical enforcement of the House Academic Voice.

The voice standard lives in `skills/references/writing-style.md` -> "House Academic Voice
(Universal Standard)". Most of it needs human judgement. This script checks the part that
does not: the hard mechanical rules that a draft either passes or fails.

Run it on every CRA prose deliverable before declaring it submission-ready.

    python3 tools/voice_check.py draft.md
    python3 tools/voice_check.py draft.md --venue asc      # adds venue limit checks
    python3 tools/voice_check.py draft.md --sections       # adds abstract section-weight check
    python3 tools/voice_check.py draft.docx --venue asc --sections

Exit status is 1 if any HARD rule fails, else 0, so it can gate a workflow.
Soft findings (context-dependent words) are reported but never fail the run.

Section parsing expects the CRA structured-abstract convention, e.g. lines or bold runs
beginning `Introduction:`, `Objective:`, `Methods:`, `Results:`, `Conclusions:`.

Deliverables usually carry trailing metadata (compliance notes, alternative titles) that is
not submission body text. Mark where the body ends with a sentinel line — the CRA convention
is `[END OF ABSTRACT BODY]` — and everything after it is ignored. Without a sentinel that
metadata is silently counted into the final section and inflates the character count.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------------------
# Rule tables. Edit these here, not in the skills — the skills point at this file.
# --------------------------------------------------------------------------------------

EM_DASH = "—"          # — never permitted
EN_DASH = "–"          # – allowed only inside compounds / ranges

BANNED_TRANSITIONS = ["Furthermore", "Moreover", "Additionally", "Interestingly"]

AI_TELL_PHRASES = [
    "delve into", "shed light on", "sheds light on", "pave the way", "paves the way",
    "in the realm of", "a myriad of", "it's important to note", "it is important to note",
    "leveraging", "utilizing", "plays a crucial role", "plays a key role",
    "underscores the importance", "highlights the importance", "a testament to",
]

# Banned as vague self-praise, but legitimate in fixed statistical terms. Reported SOFT
# with context so a human can clear "robust standard errors" while catching "robust data".
CONTEXT_DEPENDENT = {
    "robust": ["robust standard error", "robust variance", "robust to ", "robustness"],
    "comprehensive": ["Comprehensive Cancer", "comprehensive genomic profiling"],
    "significant": ["statistically significant", "significance", "significantly"],
}

# Principle 3 / 9 — verbs that assert more than most designs earn.
OVERCLAIM_VERBS = [
    "is refuted", "are refuted", "is characterized by", "are characterized by",
    "independent of", "predicts", "predict ", "drives", "driving", "establishes",
    "demonstrates", "proves", "proven", "confirms",
]

VENUES = {
    # name: (body_char_limit, title_char_limit, body_limit_with_display_item)
    "asc":   (3000, 100, 2775),
    "aats":  (3500, None, None),
    "itsos": (3500, None, None),
    "asco":  (2000, None, None),
}

ABSTRACT_HEADS = ["Introduction", "Objective", "Background", "Methods", "Results",
                  "Findings", "Conclusions", "Conclusion", "Interpretation"]

BODY_END_SENTINEL = "[END OF ABSTRACT BODY]"


# --------------------------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Return plain text from .md/.txt or .docx."""
    if path.suffix.lower() == ".docx":
        try:
            from docx import Document
        except ImportError:
            sys.exit("python-docx is required to read .docx files: pip install python-docx")
        return "\n".join(p.text for p in Document(str(path)).paragraphs)
    return path.read_text(encoding="utf-8")


def strip_scaffold(text: str, stop_at: str | None = None) -> str:
    """Drop everything that is not submission body prose.

    Truncates at the body-end sentinel if present, then removes code fences, markdown
    tables, and standalone bracketed notes.
    """
    if stop_at:
        cut = text.find(stop_at)
        if cut != -1:
            text = text[:cut]
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("|"))
    text = re.sub(r"^\s*\[.*?\]\s*$", "", text, flags=re.M)   # [compliance note] lines
    text = text.replace("**", "")                             # markdown bold is not body text
    return text


def split_sections(text: str) -> dict[str, str]:
    """Pull structured-abstract sections out of the prose."""
    pattern = re.compile(
        r"(?:^|\n)\**(" + "|".join(ABSTRACT_HEADS) + r")\**\s*:\s*", re.I)
    parts = pattern.split(text)
    if len(parts) < 3:
        return {}
    out: dict[str, str] = {}
    for head, body in zip(parts[1::2], parts[2::2]):
        out[head.strip().title()] = body.strip()
    return out


def find_all(text: str, needle: str) -> list[int]:
    """Case-insensitive offsets of needle in text.

    Word boundaries are applied only on the sides that start/end with an alphanumeric
    character. Anchoring `\\b` against punctuation such as an em dash never matches, since
    two non-word characters have no boundary between them.
    """
    esc = re.escape(needle)
    lead = r"\b" if needle[0].isalnum() else ""
    trail = r"\b" if needle[-1].isalnum() else ""
    return [m.start() for m in re.finditer(rf"{lead}{esc}{trail}", text, re.I)]


def context(text: str, idx: int, width: int = 46) -> str:
    lo, hi = max(0, idx - width), min(len(text), idx + width)
    return "..." + " ".join(text[lo:hi].split()) + "..."


def excused(text: str, idx: int, exceptions: list[str]) -> bool:
    window = text[max(0, idx - 40): idx + 60].lower()
    return any(e.lower() in window for e in exceptions)


# --------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Check a CRA prose draft against the House Academic Voice.")
    ap.add_argument("path", type=Path)
    ap.add_argument("--venue", choices=sorted(VENUES), help="apply venue character limits")
    ap.add_argument("--sections", action="store_true",
                    help="check structured-abstract section weight (Results >= 2x Methods and Conclusions)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--stop-at", default=BODY_END_SENTINEL,
                    help=f"ignore everything from this marker onward (default: {BODY_END_SENTINEL!r}); "
                         "pass '' to disable")
    args = ap.parse_args()

    if not args.path.exists():
        sys.exit(f"no such file: {args.path}")

    raw = read_text(args.path)
    if args.stop_at and args.stop_at not in raw:
        print(f"note: body-end sentinel {args.stop_at!r} not found — counting the whole file. "
              f"Add the sentinel after the last body section so trailing notes are excluded.\n")
    prose = strip_scaffold(raw, args.stop_at or None)
    hard: list[str] = []
    soft: list[str] = []

    # --- HARD 1: em dashes -------------------------------------------------------------
    for i in find_all(prose, EM_DASH):
        hard.append(f"em dash: {context(prose, i)}")

    # --- HARD 2: banned transitions ----------------------------------------------------
    for w in BANNED_TRANSITIONS:
        for i in find_all(prose, w):
            hard.append(f"banned transition '{w}': {context(prose, i)}")

    # --- HARD 3: AI-tell phrases -------------------------------------------------------
    for p in AI_TELL_PHRASES:
        for i in find_all(prose, p):
            hard.append(f"AI-tell phrase '{p}': {context(prose, i)}")

    # --- SOFT: context-dependent words -------------------------------------------------
    for w, exceptions in CONTEXT_DEPENDENT.items():
        for i in find_all(prose, w):
            if not excused(prose, i, exceptions):
                soft.append(f"vague-praise word '{w}' (clear it or cut it): {context(prose, i)}")

    secs = split_sections(prose)
    sec_chars = {k: len(v) for k, v in secs.items()}

    # --- SOFT: overclaiming verbs ------------------------------------------------------
    # Scan only the body sections when they exist, so commentary *about* flagged verbs in a
    # surrounding rationale document does not report as a violation of the draft itself.
    claim_scope = "\n".join(secs.values()) if secs else prose
    for v in OVERCLAIM_VERBS:
        for i in find_all(claim_scope, v):
            soft.append(f"overclaim verb '{v.strip()}' (principle 3/9 — earn it or downgrade): "
                        f"{context(claim_scope, i)}")

    # --- Sections ----------------------------------------------------------------------
    if args.sections:
        if not secs:
            hard.append("--sections requested but no structured-abstract headings were found")
        else:
            res = sec_chars.get("Results") or sec_chars.get("Findings")
            met = sec_chars.get("Methods")
            con = sec_chars.get("Conclusions") or sec_chars.get("Conclusion") \
                or sec_chars.get("Interpretation")
            if res and met and res < 2 * met:
                hard.append(f"section weight: Results ({res}) < 2x Methods ({met}) "
                            f"= ratio {res/met:.2f}, need >= 2.00")
            if res and con and res < 2 * con:
                hard.append(f"section weight: Results ({res}) < 2x Conclusions ({con}) "
                            f"= ratio {res/con:.2f}, need >= 2.00")
            if res and res != max(sec_chars.values()):
                hard.append("section weight: Results is not the largest section")

    # --- Venue limits ------------------------------------------------------------------
    body_chars = sum(sec_chars.values()) if secs else len(prose.strip())
    if args.venue:
        limit, title_limit, with_display = VENUES[args.venue]
        if body_chars > limit:
            hard.append(f"venue {args.venue}: body {body_chars} chars exceeds limit {limit} "
                        f"(over by {body_chars - limit})")
        if with_display and body_chars > with_display:
            soft.append(f"venue {args.venue}: body {body_chars} exceeds {with_display}, the limit "
                        f"once a table or graphic is attached (over by {body_chars - with_display})")
        if title_limit:
            soft.append(f"venue {args.venue}: title limit is {title_limit} chars — verify the title "
                        f"separately, it is not parsed from the body")

    # --- Report ------------------------------------------------------------------------
    if args.json:
        print(json.dumps({"file": str(args.path), "body_chars": body_chars,
                          "sections": sec_chars, "hard": hard, "soft": soft,
                          "pass": not hard}, indent=2))
        return 1 if hard else 0

    print(f"voice_check — {args.path.name}")
    print(f"  body characters: {body_chars}")
    if sec_chars:
        print("  sections: " + ", ".join(f"{k} {v}" for k, v in sec_chars.items()))
    print()
    if hard:
        print(f"HARD FAILURES ({len(hard)}) — must fix before submission")
        for h in hard:
            print(f"  x {h}")
        print()
    if soft:
        print(f"REVIEW ({len(soft)}) — judgement calls, clear each one deliberately")
        for s in soft:
            print(f"  ? {s}")
        print()
    if not hard and not soft:
        print("clean: no hard failures, nothing flagged for review")
    elif not hard:
        print("no hard failures")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
