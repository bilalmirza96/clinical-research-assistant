#!/usr/bin/env python3
"""Dependency-free tests for hooks/exit_gates.py (run: python3 tests/test_exit_gates.py).

Mirrors the RED/GREEN runner style of
skills/internal/analyze/tests/test_study_design_tools.py and hooks/tests/test_lessons_recall.py:
no pytest, a `check()` helper that prints PASS/FAIL and records failures, exit code 0 iff
everything passed.

Each case builds a real project directory + a synthetic transcript JSONL under tempfile, then
runs the hook as a real subprocess (python3 exit_gates.py) piping JSON on stdin, exactly as
Claude Code's Stop contract does, so a regression in the transcript-parsing, classification,
subprocess-timeout, or fail-open behavior is caught here rather than only at unit level.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "..", "exit_gates.py")

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def run_hook(payload, timeout=30.0):
    stdin_text = json.dumps(payload)
    proc = subprocess.run(
        [sys.executable, HOOK],
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return proc


def write_transcript(path, tool_uses):
    """tool_uses: list of (cwd, name, input_dict). One assistant message per entry."""
    with open(path, "w", encoding="utf-8") as fh:
        for cwd, name, tool_input in tool_uses:
            entry = {
                "type": "assistant",
                "cwd": cwd,
                "message": {
                    "content": [
                        {"type": "tool_use", "name": name, "input": tool_input},
                    ]
                },
            }
            fh.write(json.dumps(entry) + "\n")
        # a non-JSON line must not break parsing
        fh.write("not valid json at all\n")


def find_reports(project_dir):
    reports = os.path.join(project_dir, "Reports")
    if not os.path.isdir(reports):
        return []
    return [f for f in os.listdir(reports) if f.startswith("exit_gates_")]


# ---------------------------------------------------------------- fixtures

ABSTRACT_WITH_VIOLATIONS = """Introduction: The stake here is clear — we test the gate.

Objective: To determine whether the exit gate blocks on a hard voice failure.

Methods: We wrote a short synthetic abstract with a known violation.

Results: The abstract contains an em dash right here — which is a HARD failure. Furthermore, \
it also contains a banned transition word, which is a second HARD failure by itself, and this \
results section is padded out with extra sentences so that it comfortably remains the largest \
section of the draft, well past twice the length of the methods and conclusions sections that \
surround it here.

Conclusions: The gate should block.

[END OF ABSTRACT BODY]
"""

CLEAN_ABSTRACT = """Introduction: The stake here is clear, and we state it in the first person.

Objective: To determine whether a clean abstract passes the exit gate without triggering a block.

Methods: We wrote a short synthetic abstract with no known violations in it at all.

Results: The abstract avoids every banned transition and every AI-tell phrase, and it avoids \
the em dash character entirely, using a plain comma instead, and this results section is padded \
out with additional sentences describing the (hypothetical) findings in plain declarative prose \
so that it comfortably remains the largest section of the draft, well past twice the length of \
the methods and conclusions sections that surround it here, which is exactly what the house \
voice rubric requires of a structured abstract like this one.

Conclusions: The gate should allow the session to stop.

[END OF ABSTRACT BODY]
"""


def main():
    tmp_root = tempfile.mkdtemp(prefix="exit_gates_test_")
    try:
        # ------------------------------------------------------------ case 1
        # an abstract with an em dash and "Furthermore" -> block, report exists
        proj1 = os.path.join(tmp_root, "proj1")
        os.makedirs(os.path.join(proj1, "Reports"), exist_ok=True)
        abstract_path = os.path.join(proj1, "Reports", "abstract_test.md")
        with open(abstract_path, "w", encoding="utf-8") as fh:
            fh.write(ABSTRACT_WITH_VIOLATIONS)
        transcript1 = os.path.join(tmp_root, "transcript1.jsonl")
        write_transcript(transcript1, [
            (proj1, "Write", {"file_path": abstract_path, "content": ABSTRACT_WITH_VIOLATIONS}),
        ])

        proc = run_hook({
            "session_id": "s1",
            "transcript_path": transcript1,
            "stop_hook_active": False,
            "cwd": proj1,
            "hook_event_name": "Stop",
        })
        check(proc.returncode == 0, "case1 (dirty abstract): hook exits 0")
        out = proc.stdout.strip()
        check(bool(out), "case1: stdout is non-empty (a block decision)")
        if out:
            try:
                decision = json.loads(out)
            except (json.JSONDecodeError, ValueError):
                decision = None
            check(decision is not None and decision.get("decision") == "block",
                  "case1: decision == 'block'")
            check(decision is not None and "abstract_test.md" in decision.get("reason", ""),
                  "case1: reason names the failing file")
            check(decision is not None and "Reports" in decision.get("reason", ""),
                  "case1: reason names the report path")
        reports1 = find_reports(proj1)
        check(len(reports1) == 1, f"case1: exactly one report written under Reports/ (found {reports1})")
        if reports1:
            report_text = open(os.path.join(proj1, "Reports", reports1[0]), encoding="utf-8").read()
            check("voice_check" in report_text, "case1: report mentions voice_check")
            check("HARD FAIL" in report_text, "case1: report records a HARD FAIL")

        # ------------------------------------------------------------ case 2
        # a clean abstract -> allow
        proj2 = os.path.join(tmp_root, "proj2")
        os.makedirs(os.path.join(proj2, "Reports"), exist_ok=True)
        clean_path = os.path.join(proj2, "Reports", "abstract_clean.md")
        with open(clean_path, "w", encoding="utf-8") as fh:
            fh.write(CLEAN_ABSTRACT)
        transcript2 = os.path.join(tmp_root, "transcript2.jsonl")
        write_transcript(transcript2, [
            (proj2, "Write", {"file_path": clean_path, "content": CLEAN_ABSTRACT}),
        ])

        proc = run_hook({
            "session_id": "s2",
            "transcript_path": transcript2,
            "stop_hook_active": False,
            "cwd": proj2,
            "hook_event_name": "Stop",
        })
        check(proc.returncode == 0, "case2 (clean abstract): hook exits 0")
        check(proc.stdout.strip() == "", "case2: no block decision printed (allow)")
        reports2 = find_reports(proj2)
        check(len(reports2) == 1, f"case2: a report is still written for a clean run (found {reports2})")
        if reports2:
            report_text = open(os.path.join(proj2, "Reports", reports2[0]), encoding="utf-8").read()
            check("No hard failures" in report_text, "case2: report records no hard failures")

        # ------------------------------------------------------------ case 3
        # touched only a .py script -> allow, no report at all
        proj3 = os.path.join(tmp_root, "proj3")
        os.makedirs(proj3, exist_ok=True)
        script_path = os.path.join(proj3, "helper.py")
        with open(script_path, "w", encoding="utf-8") as fh:
            fh.write("print('hello')\n")
        transcript3 = os.path.join(tmp_root, "transcript3.jsonl")
        write_transcript(transcript3, [
            (proj3, "Write", {"file_path": script_path, "content": "print('hello')\n"}),
        ])

        proc = run_hook({
            "session_id": "s3",
            "transcript_path": transcript3,
            "stop_hook_active": False,
            "cwd": proj3,
            "hook_event_name": "Stop",
        })
        check(proc.returncode == 0, "case3 (.py script only): hook exits 0")
        check(proc.stdout.strip() == "", "case3: no block decision printed (allow)")
        check(not os.path.isdir(os.path.join(proj3, "Reports")),
              "case3: no Reports/ directory created, no report written")

        # ------------------------------------------------------------ case 4
        # stop_hook_active True -> allow immediately, even with a would-block transcript
        proc = run_hook({
            "session_id": "s4",
            "transcript_path": transcript1,  # reuse the dirty-abstract transcript from case 1
            "stop_hook_active": True,
            "cwd": proj1,
            "hook_event_name": "Stop",
        })
        check(proc.returncode == 0, "case4 (stop_hook_active=True): hook exits 0")
        check(proc.stdout.strip() == "", "case4: no block decision printed even though the "
                                          "transcript would otherwise block (loop guard)")

        # ------------------------------------------------------------ case 5
        # missing transcript_path -> allow
        proc = run_hook({
            "session_id": "s5",
            "stop_hook_active": False,
            "cwd": proj1,
            "hook_event_name": "Stop",
        })
        check(proc.returncode == 0, "case5 (missing transcript_path): hook exits 0")
        check(proc.stdout.strip() == "", "case5: no block decision printed (allow)")

        # a transcript_path that points nowhere should behave the same way
        proc = run_hook({
            "session_id": "s5b",
            "transcript_path": os.path.join(tmp_root, "does-not-exist.jsonl"),
            "stop_hook_active": False,
            "cwd": proj1,
            "hook_event_name": "Stop",
        })
        check(proc.returncode == 0, "case5b (nonexistent transcript_path): hook exits 0")
        check(proc.stdout.strip() == "", "case5b: no block decision printed (allow)")

        # ------------------------------------------------------------ bonus: malformed stdin
        proc = subprocess.run([sys.executable, HOOK], input="{not valid json",
                              capture_output=True, text=True, timeout=10.0)
        check(proc.returncode == 0, "malformed stdin: hook exits 0 (fail open)")
        check(proc.stdout.strip() == "", "malformed stdin: empty stdout")

        proc = subprocess.run([sys.executable, HOOK], input="",
                              capture_output=True, text=True, timeout=10.0)
        check(proc.returncode == 0, "empty stdin: hook exits 0 (fail open)")
        check(proc.stdout.strip() == "", "empty stdin: empty stdout")

    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    print()
    print(f"{len(FAILS)} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
