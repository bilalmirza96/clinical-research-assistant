#!/usr/bin/env python3
"""PreToolUse hook: keep the cra-red-team subagent read-only by mechanism, not prose.

Contract (Claude Code PreToolUse event, matcher "Bash"):
  stdin:  JSON {"session_id": ..., "transcript_path": ..., "cwd": ..., "permission_mode": ...,
                "agent_id": ..., "agent_type": ..., "hook_event_name": "PreToolUse",
                "tool_name": "Bash", "tool_input": {"command": "...", ...}, "tool_use_id": ...}
  As of Claude Code 2.1.270, PreToolUse hook input carries `agent_type`: the name of the
  subagent definition that is currently making the tool call (e.g. "cra-red-team"), or the
  main thread's agent type when the call is not from a named subagent. This is what lets a
  single plugin-wide hook act "as if" it were scoped to one agent, without any cooperation
  from that agent's own prompt.

  To block: print a short reason to stderr, exit 2 (Claude Code shows stderr to the model
  and blocks the tool call).
  To allow: exit 0, print nothing.
  Fail open on anything that isn't a clear, confident block: malformed stdin, a caller that
  isn't cra-red-team, an unparseable command -> exit 0. This hook must never be the reason a
  legitimate command from a different agent or the main session fails.

WHAT THIS ENFORCES (only when agent_type == "cra-red-team")
-------------------------------------------------------------
cra-red-team's job (agents/cra-red-team.md) is to re-derive numbers from CSVs/the registry
and run the project's own linters -- never to write, edit, or delete a project file. The
agent's frontmatter still grants the Bash tool (it has to run python3, git log, grep, etc.),
so "read-only" has to be enforced at the command level:

ALLOWED (read-only re-derivation and linting):
  - `python3 <path under this plugin's tools/ or skills/**/scripts/> [args...]`
  - cat, head, tail, wc, ls, grep, rg, find (without -delete/-exec/-ok), jq, sort, uniq,
    diff, awk (without output redirection), git log/show/diff/status

BLOCKED:
  - Any redirect (`>`, `>>`), `tee`
  - rm, mv, cp, ln, chmod, touch, mkdir, `sed -i`
  - `python3 -c ...` / `python -c ...` / heredoc-delivered code (python3 <<EOF ...)
  - curl, wget
  - git commit/push/checkout/reset/stash
  - Command chaining (&&, ||, ;, |, backticks, $(...)) where ANY segment is itself blocked
  - find -delete / -exec / -ok
  - awk with output redirection

Everything not explicitly recognized as safe is refused (default deny for this agent only),
since a prompt-injected instruction inside a reviewed deliverable only has to find one
uninspected command shape to escape a blocklist.
"""
from __future__ import annotations

import json
import re
import shlex
import sys

TARGET_AGENT_TYPE = "cra-red-team"

# Commands cra-red-team may run at all. `python3`/`python` are handled separately (path +
# args must be a script under tools/ or skills/**/scripts/, never -c or a bare stdin script).
READ_ONLY_COMMANDS = {
    "cat", "head", "tail", "wc", "ls", "grep", "rg", "find",
    "jq", "sort", "uniq", "diff", "awk",
}
PYTHON_COMMANDS = {"python3", "python"}
GIT_READ_SUBCOMMANDS = {"log", "show", "diff", "status"}

# Never allowed regardless of position in a pipeline/chain.
BLOCKED_COMMANDS = {
    "tee", "rm", "mv", "cp", "ln", "chmod", "touch", "mkdir",
    "curl", "wget", "sed", "dd", "kill", "killall", "eval", "exec",
    "nc", "ncat", "ssh", "scp", "rsync", "install", "shred", "truncate",
    "chown", "chgrp", "npm", "pip", "pip3", "cargo",
}
BLOCKED_GIT_SUBCOMMANDS = {"commit", "push", "checkout", "reset", "stash", "add", "rm", "clean", "restore", "apply", "am", "merge", "rebase", "tag", "branch"}

REASON_PREFIX = "cra-red-team is read-only: "


def _fail_open():
    sys.exit(0)


def _block(reason: str):
    sys.stderr.write(REASON_PREFIX + reason + "\n")
    sys.exit(2)


def _split_top_level(command: str):
    """Split a shell command string into segments on &&, ||, ;, | and $(...)/`...`
    substitutions, returning (segments, has_unparseable_substitution).

    This is intentionally conservative: any `$(...)` or backtick substitution is treated as
    a nested command and extracted as its own segment (so it goes through the same
    allow/deny check), and anything shlex can't tokenize at all is reported as unparseable
    so the caller can refuse rather than guess.
    """
    segments = []
    unparseable = False

    # Pull out $(...) and `...` substitutions as their own segments first, replacing them
    # with a neutral placeholder in the outer command so shlex doesn't choke on them.
    sub_pattern = re.compile(r"\$\(([^()]*(?:\([^()]*\)[^()]*)*)\)|`([^`]*)`")
    outer = command
    subs = []

    def _capture(m):
        inner = m.group(1) if m.group(1) is not None else m.group(2)
        subs.append(inner)
        return " __SUBSHELL__ "

    outer = sub_pattern.sub(_capture, outer)
    segments.extend(subs)

    # Now split the outer command on chain/pipe operators. shlex.split() alone only breaks
    # tokens on whitespace, so `cat x&&rm -rf /` (no spaces around &&) would NOT split and
    # would slip through as a single opaque token. Using shlex.shlex with punctuation_chars
    # enabled makes the lexer treat ();<>|& as their own tokens regardless of spacing, and
    # groups repeats of the same punctuation into one token (&&, ||, >>, <<) -- this is the
    # documented behavior that exists specifically for parsing shell command lines.
    try:
        lex = shlex.shlex(outer, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        return segments, True

    CHAIN_OPS = {"&&", "||", ";", "|", "&"}
    current = []
    for tok in tokens:
        if tok in CHAIN_OPS:
            if current:
                segments.append(" ".join(current))
                current = []
            continue
        # Redirect/heredoc tokens (>, >>, <<, <<<) are NOT chain boundaries -- they stay in
        # the current segment so _has_redirect() still sees them when the segment is checked.
        current.append(tok)
    if current:
        segments.append(" ".join(current))

    return segments, unparseable


_REDIRECT_RE = re.compile(r">>?(?!&)|<<<?")


def _has_redirect(command: str) -> bool:
    # `>`, `>>`, an optional leading fd number (`2>file`) all match `>>?(?!&)`; `>&1`/`2>&1`
    # (fd duplication, not a file write) are excluded via the negative lookahead. `<<`/`<<<`
    # (heredoc / herestring, a way to deliver arbitrary "code" as stdin) are always blocked.
    # A single `<` (plain input redirection from a file) is left alone -- it only reads.
    return bool(_REDIRECT_RE.search(command))


def _check_git(args):
    if not args:
        _block("bare `git` with no subcommand is not recognized as read-only")
    sub = args[0]
    if sub in BLOCKED_GIT_SUBCOMMANDS:
        _block(f"`git {sub}` is a write/history-mutating subcommand")
    if sub not in GIT_READ_SUBCOMMANDS:
        _block(f"`git {sub}` is not on the read-only allowlist (log/show/diff/status only)")


def _check_python(cmd, args):
    for a in args:
        if a in ("-c", "-m"):
            _block(f"`{cmd} {a}` (inline/module code) is blocked; run a script file instead")
    if not args:
        _block(f"bare `{cmd}` with no script path (heredoc/stdin code) is blocked")
    script = args[0]
    if script.startswith("-"):
        _block(f"`{cmd} {script}` (flag before a script path) is not recognized as read-only")
    if not script.endswith(".py"):
        _block(f"`{cmd} {script}` is not a .py script path")
    parts = script.replace("\\", "/").split("/")
    if ".." in parts:
        _block(f"`{cmd} {script}` contains a `..` path segment")
    # Accept a relative or absolute path as long as one of its directory components is
    # literally "tools" or "scripts" (covers tools/foo.py, skills/internal/x/scripts/foo.py,
    # ./tools/foo.py, /abs/path/.../tools/foo.py). Not merely a substring check, so a path
    # like "toolsmith/foo.py" does not slip through.
    dirs = parts[:-1]
    if "tools" not in dirs and "scripts" not in dirs:
        _block(
            f"`{cmd} {script}` must be a script under this plugin's tools/ or "
            "skills/**/scripts/, not an arbitrary path"
        )


def _check_find(args):
    for bad in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprintf", "-fprint"):
        if bad in args:
            _block(f"`find ... {bad}` can modify the filesystem or run arbitrary commands")


def _check_awk(command_segment: str):
    if _has_redirect(command_segment):
        _block("`awk` with output redirection is blocked")


def _check_segment(segment: str):
    segment = segment.strip()
    if not segment:
        return
    if _has_redirect(segment):
        _block("redirect (`>`, `>>`, `<<`) is blocked")
    try:
        parts = shlex.split(segment, posix=True)
    except ValueError:
        _block("could not safely parse this command segment")
        return
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    # Strip a leading path (e.g. /usr/bin/cat) down to the basename for matching.
    base = cmd.rsplit("/", 1)[-1]

    if base in BLOCKED_COMMANDS:
        _block(f"`{base}` is not a read-only command")
    if base == "git":
        _check_git(args)
        return
    if base in PYTHON_COMMANDS:
        _check_python(base, args)
        return
    if base == "find":
        if base not in READ_ONLY_COMMANDS:
            _block(f"`{base}` is not on the read-only allowlist")
        _check_find(args)
        return
    if base == "awk":
        _check_awk(segment)
        if base not in READ_ONLY_COMMANDS:
            _block(f"`{base}` is not on the read-only allowlist")
        return
    if base not in READ_ONLY_COMMANDS:
        _block(f"`{base}` is not on the read-only allowlist")


def _read_payload():
    """Read and parse stdin exactly once. Returns a dict, or None on any malformed input."""
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw)
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def main():
    payload = _read_payload()
    if payload is None:
        _fail_open()
        return

    agent_type = payload.get("agent_type")
    is_red_team = agent_type == TARGET_AGENT_TYPE

    if not is_red_team:
        # Not cra-red-team (main session, another subagent, or agent_type missing/unknown on
        # an older Claude Code build without this field) -- never our business.
        _fail_open()
        return

    tool_name = payload.get("tool_name")
    if tool_name != "Bash":
        # Not a Bash call (e.g. Read/Grep/Glob) -- those are already governed by the agent's
        # own tools: allowlist in its frontmatter, not this hook.
        _fail_open()
        return

    # A malformed/unexpected shape for tool_input or tool_input.command is treated as a
    # protocol-level surprise (e.g. a future Claude Code version renaming a field), not as a
    # command to evaluate -- fail open per the hook's own contract, same as any other
    # malformed-stdin case. Only once we have an actual, well-typed command string do we
    # start refusing on ambiguity.
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        _fail_open()
        return

    command = tool_input.get("command")
    if not isinstance(command, str) or not command.strip():
        _fail_open()
        return

    # From here on we have a real command string from a confirmed cra-red-team Bash call:
    # any error tokenizing or checking it should refuse rather than silently allow an
    # unexamined command through.
    try:
        segments, unparseable = _split_top_level(command)
        if unparseable or not segments:
            _block("command could not be safely parsed (possible chaining bypass attempt)")
            return

        for segment in segments:
            _check_segment(segment)

        # Every segment passed -- allow.
        sys.exit(0)
    except SystemExit:
        raise
    except Exception:
        _block("internal guard error; refusing rather than allowing un-narrowed")


if __name__ == "__main__":
    main()
