#!/usr/bin/env python3
"""Dependency-free tests for hooks/lessons_recall.py (run: python3 tests/test_lessons_recall.py).

Mirrors the RED/GREEN runner style of
skills/internal/analyze/tests/test_study_design_tools.py: no pytest, a `check()`
helper that prints PASS/FAIL and records failures, exit code 0 iff everything
passed.

Each case runs the hook as a real subprocess (python3 lessons_recall.py) piping
JSON on stdin, exactly as Claude Code's UserPromptSubmit contract does, so a
regression in the stdin-parsing or fail-open behavior is caught here rather
than only in a unit-level import.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "..", "lessons_recall.py")

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def run_hook(stdin_text, timeout=2.0):
    start = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, HOOK],
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    return proc, elapsed_ms


def run_prompt(prompt):
    stdin_text = json.dumps({
        "prompt": prompt,
        "session_id": "test-session",
        "cwd": HERE,
        "hook_event_name": "UserPromptSubmit",
    })
    return run_hook(stdin_text)


def parsed_context(proc):
    """Returns the additionalContext string, or None if stdout was empty."""
    out = proc.stdout.strip()
    if not out:
        return None
    payload = json.loads(out)  # must be valid JSON when non-empty
    check(
        payload.get("hookSpecificOutput", {}).get("hookEventName") == "UserPromptSubmit",
        "output shape: hookSpecificOutput.hookEventName == 'UserPromptSubmit'",
    )
    check(
        "additionalContext" in payload.get("hookSpecificOutput", {}),
        "output shape: hookSpecificOutput.additionalContext present",
    )
    return payload["hookSpecificOutput"]["additionalContext"]


# ---------------------------------------------------------------- GENIE / TMB / off-panel

genie_prompt = (
    "For the GENIE panel-coverage analysis, remember: off-panel gene / gene not "
    "assayed by the patient's panel should be coded NaN, not wild-type. Also double "
    "check TMB mut/Mb comparisons across panels before reporting gene enrichment "
    "and WES results."
)
proc, elapsed = run_hook(json.dumps({"prompt": genie_prompt}))
check(proc.returncode == 0, "GENIE prompt: hook exits 0")
ctx = parsed_context(proc)
check(ctx is not None, "GENIE prompt: produces additionalContext")
check(ctx is not None and "L093" in ctx, "GENIE prompt: surfaces L093 (genomic-platform-and-units)")
check(ctx is not None and "L061" in ctx, "GENIE prompt: surfaces L061 (genie-panel-coverage-offpanel-not-wildtype)")
if ctx is not None:
    n_lessons = sum(1 for line in ctx.splitlines() if line.startswith("- L"))
    check(n_lessons <= 6, f"GENIE prompt: never more than 6 lessons (got {n_lessons})")

# ---------------------------------------------------------------- abstract drafting

abstract_prompt = (
    "Please run an abstract structural review before I draft the abstract -- I want "
    "to confirm the abstract reports race or ethnicity using registry-coded language, "
    "not TCGA / SEER / NCDB / GENIE cohort by race labels, and that Methods section "
    "approaching size of Results isn't happening."
)
proc, _ = run_hook(json.dumps({"prompt": abstract_prompt}))
check(proc.returncode == 0, "abstract prompt: hook exits 0")
ctx = parsed_context(proc)
check(ctx is not None, "abstract prompt: produces additionalContext")
if ctx is not None:
    check(
        any(lid in ctx for lid in ("L020", "L021", "L062")),
        "abstract prompt: surfaces at least one of L020/L021/L062",
    )

# ---------------------------------------------------------------- bare acknowledgements

for ack in ("ok", "yes please"):
    proc, _ = run_hook(json.dumps({"prompt": ack}))
    check(proc.returncode == 0, f"ack '{ack}': hook exits 0")
    check(proc.stdout.strip() == "", f"ack '{ack}': produces no output")

# ---------------------------------------------------------------- generic unrelated prompt

proc, _ = run_hook(json.dumps({"prompt": "what is the weather in Tucson"}))
check(proc.returncode == 0, "unrelated prompt: hook exits 0")
check(proc.stdout.strip() == "", "unrelated prompt: produces no output")

# ---------------------------------------------------------------- malformed stdin

proc, _ = run_hook("{not valid json")
check(proc.returncode == 0, "malformed stdin: exits 0 (fail open)")
check(proc.stdout.strip() == "", "malformed stdin: empty stdout")

proc, _ = run_hook("")
check(proc.returncode == 0, "empty stdin: exits 0 (fail open)")
check(proc.stdout.strip() == "", "empty stdin: empty stdout")

# ---------------------------------------------------------------- runtime budget

timings = []
for prompt in (genie_prompt, abstract_prompt, "what is the weather in Tucson", "ok"):
    _, elapsed_ms = run_hook(json.dumps({"prompt": prompt}))
    timings.append(elapsed_ms)
max_ms = max(timings)
check(max_ms < 300, f"runtime: every call under 300 ms (max observed {max_ms:.1f} ms, includes interpreter startup)")
print(f"  (timings ms: {[round(t, 1) for t in timings]})")

print()
print(f"{len(FAILS)} failure(s)")
sys.exit(1 if FAILS else 0)
