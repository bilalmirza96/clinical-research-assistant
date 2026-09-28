#!/usr/bin/env python3
"""Stop hook: run CRA's linters on deliverables touched during the session and refuse to
stop on a hard failure.

Contract (Claude Code Stop event):
  stdin:  JSON {"session_id": ..., "transcript_path": ..., "stop_hook_active": bool,
                "cwd": ..., "hook_event_name": "Stop"}
  To block stopping: print {"decision": "block", "reason": "<...>"} to stdout, exit 0.
  To allow: print nothing, exit 0.
  If stop_hook_active is true: exit 0 immediately (prevents loops).
  Fail open on any internal error: never raise, never print malformed output, always exit 0.

WHAT THIS DOES
--------------
1. Parses the session transcript (JSONL) and collects file paths the session actually wrote
   or edited: Write/Edit `file_path`, NotebookEdit `notebook_path`, and Bash commands only
   when a path is an obvious redirect target (`> file`, `>> file`, `tee file`).
2. Classifies each surviving path (must exist on disk, <= 5 MB):
     - basename MASTER_ANALYSIS_REGISTRY.json           -> registry_lint
     - .md / .docx under Abstracts/, Manuscripts/,
       Reports/, or named abstract*/manuscript*/
       analysis_report*                                  -> voice_check (+ --sections for
                                                             abstract-like files) and
                                                             claim_audit when a registry can
                                                             be found nearby
     - .docx / .xlsx (any deliverable)                    -> house_style --check
   Everything else (scripts, notes, CLAUDE.md, memory, unclassified files) is ignored.
3. Runs each linter as a subprocess, under a per-call timeout and a 25 s total budget.
   Anything left when the budget runs out is marked SKIPPED and does not block.
4. Writes a dated report under <cwd>/Reports/ (reusing an existing Reports/ dir, or
   creating one only if <cwd> already looks like a project root by way of a CLAUDE.md;
   otherwise the system temp dir) and blocks the Stop only when at least one HARD failure
   was found, naming the failing file(s) and the report path in the reason.

DISTINGUISHING HARD FAILURES FROM TOOL ERRORS
-----------------------------------------------
voice_check.py and claim_audit.py support --json and a clean {"hard": [...], "soft": [...]}
shape, but on a missing python-docx dependency (or a bad path) they call `sys.exit(<string>)`
BEFORE ever emitting JSON — same exit code (1) as a real hard failure. This hook treats a
non-JSON-parseable response as a TOOL ERROR (reported, never blocking), not a hard failure.

registry_lint.py and house_style.py expose no --json at all; their exit code conflates a
genuine hard failure with any unhandled exception (e.g. a malformed registry file, or
python-docx/openpyxl raising on a corrupt document — see house_style.py's traceback on a
missing file, which also exits 1). This hook cross-checks the exit code against each tool's
own success/failure text markers in stdout ("HARD FAILURES (" for registry_lint; "N
violations" for the specific file for house_style) and only blocks when that marker is
present, downgrading an ambiguous nonzero exit with no marker to a non-blocking TOOL ERROR.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------

HOOKS_DIR = Path(__file__).resolve().parent
TOOLS_DIR = HOOKS_DIR.parent / "tools"
VOICE_CHECK = TOOLS_DIR / "voice_check.py"
CLAIM_AUDIT = TOOLS_DIR / "claim_audit.py"
REGISTRY_LINT = TOOLS_DIR / "registry_lint.py"
HOUSE_STYLE = TOOLS_DIR / "house_style.py"

MAX_FILE_BYTES = 5 * 1024 * 1024
OVERALL_BUDGET_SEC = 25.0
PER_CALL_TIMEOUT_SEC = 8.0
MIN_CALL_TIMEOUT_SEC = 0.5

REGISTRY_BASENAME = "MASTER_ANALYSIS_REGISTRY.json"
PROSE_DIR_MARKERS = ("/abstracts/", "/manuscripts/", "/reports/")
PROSE_BASENAME_PREFIXES = ("abstract", "manuscript", "analysis_report")
PROSE_EXTS = {".md", ".docx"}
HOUSE_STYLE_EXTS = {".docx", ".xlsx"}
REGISTRY_SEARCH_DEPTH = 8

TOOL_NAMES_WITH_PATH = {"Write": "file_path", "Edit": "file_path", "NotebookEdit": "notebook_path"}

_REDIRECT_RE = re.compile(r'(?:^|[\s;|&])>{1,2}\s*([^\s|;&<>]+)')
_TEE_RE = re.compile(r'\btee\b(?:\s+-a)?\s+(?!-)([^\s|;&<>]+)')


# --------------------------------------------------------------------------------------
# Transcript parsing
# --------------------------------------------------------------------------------------

def extract_bash_redirect_targets(command: str) -> list[str]:
    """Obvious redirect targets only: `> file`, `>> file`, `tee [-a] file`."""
    if not isinstance(command, str) or not command:
        return []
    raw = [m.group(1) for m in _REDIRECT_RE.finditer(command)]
    raw += [m.group(1) for m in _TEE_RE.finditer(command)]
    out = []
    for t in raw:
        t = t.strip().strip("'\"")
        if not t or t.startswith("&") or t.startswith("-") or t.startswith("$"):
            continue
        if "$(" in t or "`" in t:
            continue
        if t in ("/dev/null", "/dev/stdout", "/dev/stderr"):
            continue
        out.append(t)
    return out


def resolve_path(raw: str, line_cwd: str) -> Path | None:
    if not raw or not isinstance(raw, str):
        return None
    p = Path(raw)
    if not p.is_absolute():
        p = Path(line_cwd) / p
    try:
        return p.resolve()
    except OSError:
        return None


def collect_deliverables(transcript_path: str, top_cwd: str) -> "dict[Path, None]":
    """Ordered set (dict keys) of resolved, existing, small-enough file paths touched."""
    seen: "dict[Path, None]" = {}
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if not isinstance(obj, dict):
                continue
            line_cwd = obj.get("cwd") if isinstance(obj.get("cwd"), str) else top_cwd
            message = obj.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name")
                tool_input = block.get("input")
                if not isinstance(tool_input, dict):
                    continue
                raw_paths: list[str] = []
                if name in TOOL_NAMES_WITH_PATH:
                    val = tool_input.get(TOOL_NAMES_WITH_PATH[name])
                    if isinstance(val, str):
                        raw_paths.append(val)
                elif name == "Bash":
                    raw_paths.extend(extract_bash_redirect_targets(tool_input.get("command", "")))
                for raw in raw_paths:
                    resolved = resolve_path(raw, line_cwd)
                    if resolved is None:
                        continue
                    if resolved in seen:
                        continue
                    try:
                        if not resolved.is_file():
                            continue
                        if resolved.stat().st_size > MAX_FILE_BYTES:
                            continue
                    except OSError:
                        continue
                    seen[resolved] = None
    return seen


# --------------------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------------------

def classify(paths: "dict[Path, None]") -> "dict[Path, list[str]]":
    plan: "dict[Path, list[str]]" = {}
    for p in paths:
        tags: list[str] = []
        ext = p.suffix.lower()
        stem_lower = p.stem.lower()
        posix_lower = (p.as_posix() + "/").lower()  # trailing slash lets a bare dir-name match

        if p.name == REGISTRY_BASENAME and ext == ".json":
            tags.append("registry")

        is_prose_location = (
            any(marker in posix_lower for marker in PROSE_DIR_MARKERS)
            or stem_lower.startswith(PROSE_BASENAME_PREFIXES)
        )
        if ext in PROSE_EXTS and is_prose_location:
            tags.append("prose")

        if ext in HOUSE_STYLE_EXTS:
            tags.append("house_style")

        if tags:
            plan[p] = tags
    return plan


def is_abstract_like(p: Path) -> bool:
    posix_lower = (p.as_posix() + "/").lower()
    return "abstract" in p.stem.lower() or "/abstracts/" in posix_lower


def find_nearby_registry(path: Path, known_registries: "list[Path]") -> Path | None:
    """Prefer a registry touched this session that shares ancestry with `path`; else walk
    upward looking for Reports/MASTER_ANALYSIS_REGISTRY.json or a sibling of the same name."""
    best: "tuple[int, Path] | None" = None
    for reg in known_registries:
        common = 0
        for a, b in zip(path.parts, reg.parts):
            if a != b:
                break
            common += 1
        if common >= 2 and (best is None or common > best[0]):
            best = (common, reg)
    if best is not None:
        return best[1]

    d = path.parent
    for _ in range(REGISTRY_SEARCH_DEPTH):
        for candidate in (d / "Reports" / REGISTRY_BASENAME, d / REGISTRY_BASENAME):
            if candidate.is_file():
                return candidate
        if d.parent == d:
            break
        d = d.parent
    return None


# --------------------------------------------------------------------------------------
# Running linters
# --------------------------------------------------------------------------------------

def run_linter(cmd: "list[str]", timeout: float) -> dict:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
                "timed_out": False, "launch_error": None}
    except subprocess.TimeoutExpired:
        return {"returncode": None, "stdout": "", "stderr": "", "timed_out": True, "launch_error": None}
    except Exception as exc:  # e.g. interpreter missing, permission error
        return {"returncode": None, "stdout": "", "stderr": "", "timed_out": False,
                "launch_error": str(exc)}


def make_result(path: Path, linter: str, status: str, detail: str, raw: str) -> dict:
    return {"path": path, "linter": linter, "status": status, "detail": detail, "raw": raw}


def _base_status(path: Path, linter: str, run: dict) -> tuple[str, str] | None:
    """Returns (status, detail) for the universal non-happy paths, else None."""
    if run["timed_out"]:
        return "TIMEOUT", f"{linter} exceeded its {PER_CALL_TIMEOUT_SEC:.0f}s per-call timeout"
    if run["launch_error"]:
        return "TOOL ERROR", f"failed to launch {linter}: {run['launch_error']}"
    return None


def check_json_linter(path: Path, linter: str, script: Path, cmd: "list[str]", timeout: float) -> dict:
    if not script.is_file():
        return make_result(path, linter, "TOOL ERROR", f"linter script not found: {script}", "")
    run = run_linter(cmd, timeout)
    early = _base_status(path, linter, run)
    if early:
        return make_result(path, linter, *early, run["stderr"] or run["stdout"])
    try:
        data = json.loads(run["stdout"].strip())
    except (json.JSONDecodeError, ValueError):
        # Non-JSON output despite --json: e.g. a missing python-docx dependency or a bad
        # path calls sys.exit(<string>) before any JSON is emitted. Same exit code as a real
        # hard failure — ambiguous, so this downgrades to a non-blocking tool error.
        note = (run["stderr"].strip() or run["stdout"].strip()
                or f"exit {run['returncode']}, no parseable JSON output")
        return make_result(path, linter, "TOOL ERROR", note, run["stdout"] + run["stderr"])
    hard = data.get("hard") or []
    soft = data.get("soft") or []
    raw = json.dumps(data, indent=2)
    if hard:
        detail_items = [h if isinstance(h, str) else json.dumps(h) for h in hard[:6]]
        return make_result(path, linter, "HARD FAIL", " | ".join(detail_items), raw)
    if soft:
        detail_items = [s if isinstance(s, str) else json.dumps(s) for s in soft[:6]]
        return make_result(path, linter, "PASS (warnings)", " | ".join(detail_items), raw)
    return make_result(path, linter, "PASS", "clean", raw)


def check_voice(path: Path, timeout: float) -> dict:
    cmd = [sys.executable, str(VOICE_CHECK), str(path), "--json"]
    if is_abstract_like(path):
        cmd.append("--sections")
    return check_json_linter(path, "voice_check", VOICE_CHECK, cmd, timeout)


def check_claim_audit(path: Path, registry: Path, timeout: float) -> dict:
    cmd = [sys.executable, str(CLAIM_AUDIT), str(path), "--registry", str(registry), "--json"]
    return check_json_linter(path, "claim_audit", CLAIM_AUDIT, cmd, timeout)


def check_registry_lint(path: Path, timeout: float) -> dict:
    linter = "registry_lint"
    if not REGISTRY_LINT.is_file():
        return make_result(path, linter, "TOOL ERROR", f"linter script not found: {REGISTRY_LINT}", "")
    cmd = [sys.executable, str(REGISTRY_LINT), str(path)]
    run = run_linter(cmd, timeout)
    early = _base_status(path, linter, run)
    if early:
        return make_result(path, linter, *early, run["stderr"] or run["stdout"])
    stdout = run["stdout"]
    # registry_lint has no --json; its exit code alone cannot distinguish a genuine H1-H9
    # hard failure from any unhandled exception (e.g. malformed registry JSON). Its own
    # "HARD FAILURES (" marker is a more reliable signal than the exit code.
    if "HARD FAILURES (" in stdout:
        lines = [ln.strip() for ln in stdout.splitlines() if ln.strip().startswith("x ")]
        return make_result(path, linter, "HARD FAIL", " | ".join(lines[:6]), stdout)
    if run["returncode"] not in (0, 1):
        return make_result(path, linter, "TOOL ERROR",
                            f"exit {run['returncode']} with no HARD FAILURES marker (ambiguous)",
                            stdout + run["stderr"])
    if run["returncode"] == 1 and "HARD FAILURES (" not in stdout:
        return make_result(path, linter, "TOOL ERROR",
                            "exit 1 but no HARD FAILURES marker in stdout (likely an unhandled "
                            "exception rather than a genuine lint failure)", stdout + run["stderr"])
    if "REVIEW (" in stdout:
        lines = [ln.strip() for ln in stdout.splitlines() if ln.strip().startswith("?")]
        return make_result(path, linter, "PASS (warnings)", " | ".join(lines[:6]), stdout)
    return make_result(path, linter, "PASS", "clean", stdout)


def check_house_style(path: Path, timeout: float) -> dict:
    linter = "house_style"
    if not HOUSE_STYLE.is_file():
        return make_result(path, linter, "TOOL ERROR", f"linter script not found: {HOUSE_STYLE}", "")
    cmd = [sys.executable, str(HOUSE_STYLE), "--check", str(path)]
    run = run_linter(cmd, timeout)
    early = _base_status(path, linter, run)
    if early:
        return make_result(path, linter, *early, run["stderr"] or run["stdout"])
    stdout = run["stdout"]
    if f"skip (unsupported): {path}" in stdout:
        return make_result(path, linter, "SKIPPED (unsupported type)", "house_style does not "
                            "accept this file type", stdout)
    # No --json here either; house_style crashes with an unhandled traceback (exit 1, empty
    # stdout) on e.g. a corrupt .docx/.xlsx, which is the same exit code as a real violation
    # count. Only trust an exit code of 1 when this file's own "N violations" line is present.
    m = re.search(re.escape(path.name) + r": (\d+) violations", stdout)
    if m:
        n = int(m.group(1))
        if n > 0:
            return make_result(path, linter, "HARD FAIL", f"{n} house-style violation(s)", stdout)
        return make_result(path, linter, "PASS", "clean", stdout)
    if run["returncode"] not in (0, 1):
        return make_result(path, linter, "TOOL ERROR",
                            f"exit {run['returncode']} with no 'N violations' marker (ambiguous)",
                            stdout + run["stderr"])
    return make_result(path, linter, "TOOL ERROR",
                        "exit 1 but no 'N violations' marker in stdout (likely an unhandled "
                        "exception, e.g. a corrupt document, rather than a genuine violation)",
                        stdout + run["stderr"])


# --------------------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------------------

def build_tasks(plan: "dict[Path, list[str]]") -> "tuple[list[tuple], list[dict]]":
    """Returns (tasks, presched_results). tasks is [(path, linter_name, callable(timeout))]."""
    registries = [p for p, tags in plan.items() if "registry" in tags]
    tasks: list[tuple] = []
    presched: list[dict] = []

    for path, tags in plan.items():
        if "registry" in tags:
            tasks.append((path, "registry_lint",
                          lambda t, p=path: check_registry_lint(p, t)))
        if "prose" in tags:
            tasks.append((path, "voice_check",
                          lambda t, p=path: check_voice(p, t)))
            reg = find_nearby_registry(path, registries)
            if reg is not None:
                tasks.append((path, "claim_audit",
                              lambda t, p=path, r=reg: check_claim_audit(p, r, t)))
            else:
                presched.append(make_result(path, "claim_audit", "SKIPPED",
                                             "no MASTER_ANALYSIS_REGISTRY.json found nearby", ""))
        if "house_style" in tags:
            tasks.append((path, "house_style",
                          lambda t, p=path: check_house_style(p, t)))
    return tasks, presched


def run_all(plan: "dict[Path, list[str]]") -> "tuple[list[dict], list[dict]]":
    tasks, results = build_tasks(plan)
    start = time.monotonic()
    hard_failures: list[dict] = []

    for path, linter, run_fn in tasks:
        elapsed = time.monotonic() - start
        remaining = OVERALL_BUDGET_SEC - elapsed
        if remaining <= MIN_CALL_TIMEOUT_SEC:
            results.append(make_result(path, linter, "SKIPPED",
                                        "25s total exit-gate time budget exceeded before this "
                                        "check could run", ""))
            continue
        timeout = max(MIN_CALL_TIMEOUT_SEC, min(PER_CALL_TIMEOUT_SEC, remaining))
        res = run_fn(timeout)
        results.append(res)
        if res["status"] == "HARD FAIL":
            hard_failures.append(res)
    return results, hard_failures


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------

def report_output_dir(cwd: str) -> Path:
    cwd_path = Path(cwd) if cwd else Path.cwd()
    reports = cwd_path / "Reports"
    if reports.is_dir():
        return reports
    if (cwd_path / "CLAUDE.md").is_file():
        try:
            reports.mkdir(parents=True, exist_ok=True)
            return reports
        except OSError:
            pass
    return Path(tempfile.gettempdir())


def build_report(results: "list[dict]", plan: "dict[Path, list[str]]") -> str:
    now = datetime.now()
    lines = [
        "# Exit gates report",
        "",
        f"Generated: {now.isoformat(timespec='seconds')}",
        f"Files checked: {len(plan)}",
        "",
    ]
    by_path: "dict[Path, list[dict]]" = {}
    for r in results:
        by_path.setdefault(r["path"], []).append(r)

    for path in plan:
        lines.append(f"## {path}")
        lines.append("")
        for r in by_path.get(path, []):
            lines.append(f"- **{r['linter']}** — {r['status']}")
            if r["detail"]:
                lines.append(f"  - {r['detail']}")
            if r["raw"]:
                raw = r["raw"].strip()
                if len(raw) > 4000:
                    raw = raw[:4000] + "\n... (truncated)"
                lines.append("  - raw output:")
                lines.append("    ```")
                for raw_line in raw.splitlines():
                    lines.append(f"    {raw_line}")
                lines.append("    ```")
        lines.append("")

    hard = [r for r in results if r["status"] == "HARD FAIL"]
    lines.append("## Summary")
    lines.append("")
    if hard:
        lines.append(f"{len(hard)} hard failure(s) — Stop was blocked.")
        for r in hard:
            lines.append(f"- {r['path']} ({r['linter']}): {r['detail']}")
    else:
        lines.append("No hard failures. Stop was allowed.")
    lines.append("")
    return "\n".join(lines)


def write_report(text: str, cwd: str) -> Path:
    out_dir = report_output_dir(cwd)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out_path = out_dir / f"exit_gates_{stamp}.md"
    out_path.write_text(text, encoding="utf-8")
    return out_path


def format_block_reason(hard_failures: "list[dict]", report_path: Path) -> str:
    names = [f"{r['path'].name} ({r['linter']})" for r in hard_failures[:5]]
    more = "" if len(hard_failures) <= 5 else f", and {len(hard_failures) - 5} more"
    return (f"exit_gates: {len(hard_failures)} hard failure(s) in "
            f"{', '.join(names)}{more}. Full report: {report_path}")


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

def main() -> int:
    try:
        raw_stdin = sys.stdin.read()
    except Exception:
        return 0

    try:
        payload = json.loads(raw_stdin) if raw_stdin.strip() else {}
        if not isinstance(payload, dict):
            return 0
    except (json.JSONDecodeError, ValueError):
        return 0

    try:
        if payload.get("stop_hook_active"):
            return 0

        transcript_path = payload.get("transcript_path")
        top_cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else os.getcwd()

        if not isinstance(transcript_path, str) or not transcript_path or not os.path.isfile(transcript_path):
            return 0

        deliverables = collect_deliverables(transcript_path, top_cwd)
        if not deliverables:
            return 0

        plan = classify(deliverables)
        if not plan:
            return 0

        results, hard_failures = run_all(plan)
        report_text = build_report(results, plan)
        report_path = write_report(report_text, top_cwd)

        if hard_failures:
            reason = format_block_reason(hard_failures, report_path)
            sys.stdout.write(json.dumps({"decision": "block", "reason": reason}))
        return 0
    except Exception:
        # Fail open: an internal error in this hook must never block the user's Stop.
        return 0


if __name__ == "__main__":
    sys.exit(main())
