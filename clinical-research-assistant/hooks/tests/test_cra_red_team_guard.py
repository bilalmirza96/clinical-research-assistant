#!/usr/bin/env python3
"""Dependency-free tests for hooks/cra_red_team_guard.py (run: python3 tests/test_cra_red_team_guard.py).

Mirrors the RED/GREEN runner style of tests/test_lessons_recall.py and
tests/test_exit_gates.py: no pytest, a `check()` helper that prints PASS/FAIL and records
failures, exit code 0 iff everything passed.

Each case runs the hook as a real subprocess (python3 cra_red_team_guard.py) piping JSON on
stdin, exactly as Claude Code's PreToolUse contract does, so a regression in the
stdin-parsing, tokenizing, or fail-open behavior is caught here rather than only in a
unit-level import.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "..", "cra_red_team_guard.py")

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def run_hook(stdin_text, timeout=5.0):
    return subprocess.run(
        [sys.executable, HOOK],
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def run_bash(command, agent_type="cra-red-team", tool_name="Bash"):
    payload = {
        "session_id": "test-session",
        "transcript_path": "/tmp/does-not-matter.jsonl",
        "cwd": HERE,
        "permission_mode": "default",
        "agent_id": "test-agent-id",
        "agent_type": agent_type,
        "hook_event_name": "PreToolUse",
        "tool_name": tool_name,
        "tool_input": {"command": command},
        "tool_use_id": "test-tool-use-id",
    }
    return run_hook(json.dumps(payload))


# --------------------------------------------------------------------- allowed (RED->GREEN)

ALLOWED_COMMANDS = [
    "cat Reports/MASTER_ANALYSIS_REGISTRY.json",
    "head -50 data/raw/cohort.csv",
    "tail -n 20 Reports/red_team_2026-09-28.md",
    "wc -l data/raw/cohort.csv",
    "ls -la Reports/",
    "grep -n 'crude_OR' Reports/MASTER_ANALYSIS_REGISTRY.json",
    "rg 'UNSOURCED' Reports/",
    "find data/raw -name '*.csv'",
    "jq '.M2.crude_OR' Reports/MASTER_ANALYSIS_REGISTRY.json",
    "sort data/raw/cohort.csv",
    "uniq -c data/raw/cohort.csv",
    "diff a.csv b.csv",
    "awk '{print $1}' data/raw/cohort.csv",
    "python3 tools/registry_lint.py Reports/MASTER_ANALYSIS_REGISTRY.json",
    "python3 skills/internal/analyze/scripts/cohort_flow.py --project .",
    "git log --oneline -10",
    "git show HEAD",
    "git diff HEAD~1",
    "git status",
    "cat a.csv | grep foo | sort | uniq -c",
    "python3 tools/claim_audit.py --registry Reports/MASTER_ANALYSIS_REGISTRY.json && git status",
]


def test_allowed():
    for cmd in ALLOWED_COMMANDS:
        proc = run_bash(cmd)
        check(
            proc.returncode == 0,
            f"allowed: `{cmd}` -> exit {proc.returncode} (expected 0); stderr={proc.stderr.strip()!r}",
        )


# ---------------------------------------------------------------------- blocked (RED->GREEN)

BLOCKED_COMMANDS = [
    "echo hi > out.txt",
    "grep foo file.txt >> results.txt",
    "cat secret.txt | tee copy.txt",
    "rm Reports/red_team_2026-09-28.md",
    "mv a.csv b.csv",
    "cp a.csv b.csv",
    "ln -s a.csv b.csv",
    "chmod 777 script.py",
    "touch new_file.txt",
    "mkdir Archives/new",
    "sed -i 's/foo/bar/' Reports/MASTER_ANALYSIS_REGISTRY.json",
    "python3 -c \"import os; os.remove('x')\"",
    "python3 << EOF\nimport os\nEOF",
    "curl https://example.com/data.csv -o data.csv",
    "wget https://example.com/data.csv",
    "git commit -am 'edit registry'",
    "git push origin main",
    "git checkout main -- Reports/MASTER_ANALYSIS_REGISTRY.json",
    "git reset --hard HEAD~1",
    "git stash",
    "cat file.txt && rm -rf /tmp/x",
    "cat file.txt&&rm -rf /tmp/x",
    "find . -name '*.tmp' -delete",
    "find . -name '*.py' -exec rm {} \\;",
    "cat 'unterminated",  # unparseable command content from a confirmed cra-red-team call
]


def test_blocked():
    for cmd in BLOCKED_COMMANDS:
        proc = run_bash(cmd)
        check(
            proc.returncode == 2 and proc.stderr.strip() != "",
            f"blocked: `{cmd}` -> exit {proc.returncode} (expected 2 with stderr reason); "
            f"stderr={proc.stderr.strip()!r}",
        )


# --------------------------------------------------------------- non-red-team never blocked

def test_non_red_team_never_blocked():
    # The hook is plugin-wide (PreToolUse has no way to register a hook that only fires for
    # one named subagent's frontmatter), so it must be a complete no-op for anyone whose
    # agent_type isn't cra-red-team -- including commands that WOULD be blocked for
    # cra-red-team itself.
    dangerous_for_red_team = [
        "rm -rf /tmp/whatever",
        "git commit -am 'wip'",
        "echo hi > out.txt",
        "curl https://example.com",
    ]
    for agent_type in [None, "general-purpose", "cra-manuscript-qc", "main"]:
        for cmd in dangerous_for_red_team:
            proc = run_bash(cmd, agent_type=agent_type)
            label = agent_type if agent_type is not None else "<missing agent_type>"
            check(
                proc.returncode == 0,
                f"non-red-team ({label}): `{cmd}` -> exit {proc.returncode} (expected 0, "
                f"hook must be a no-op); stderr={proc.stderr.strip()!r}",
            )


def test_missing_agent_type_field():
    payload = {
        "session_id": "test-session",
        "cwd": HERE,
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "rm -rf /"},
        "tool_use_id": "x",
    }
    proc = run_hook(json.dumps(payload))
    check(
        proc.returncode == 0,
        f"stdin with no agent_type at all -> exit {proc.returncode} (expected 0, fail open)",
    )


def test_non_bash_tool_ignored():
    payload = {
        "session_id": "test-session",
        "cwd": HERE,
        "agent_type": "cra-red-team",
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "/tmp/x", "content": "y"},
        "tool_use_id": "x",
    }
    proc = run_hook(json.dumps(payload))
    check(
        proc.returncode == 0,
        f"non-Bash tool_name for cra-red-team -> exit {proc.returncode} (expected 0; a "
        "Write call is refused by the agent's tools: allowlist, not this hook)",
    )


# --------------------------------------------------------------------------- malformed stdin

MALFORMED_STDIN_CASES = [
    "",
    "not json at all",
    "{",
    "null",
    "42",
    '["a","b"]',
    '{"agent_type": "cra-red-team"}',  # missing tool_name/tool_input entirely
    '{"agent_type": "cra-red-team", "tool_name": "Bash"}',  # missing tool_input
    '{"agent_type": "cra-red-team", "tool_name": "Bash", "tool_input": {}}',  # missing command
    '{"agent_type": "cra-red-team", "tool_name": "Bash", "tool_input": {"command": 5}}',
    '{"agent_type": "cra-red-team", "tool_name": "Bash", "tool_input": "not-a-dict"}',
]


def test_malformed_stdin_exits_zero():
    for stdin_text in MALFORMED_STDIN_CASES:
        proc = run_hook(stdin_text)
        check(
            proc.returncode == 0,
            f"malformed stdin {stdin_text!r} -> exit {proc.returncode} (expected 0, fail "
            "open/refuse-safely, never crash)",
        )


def main():
    test_allowed()
    test_blocked()
    test_non_red_team_never_blocked()
    test_missing_agent_type_field()
    test_non_bash_tool_ignored()
    test_malformed_stdin_exits_zero()

    print()
    if FAILS:
        print(f"{len(FAILS)} FAILURE(S):")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
