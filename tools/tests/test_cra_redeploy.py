#!/usr/bin/env python3
"""Tests for tools/cra-redeploy.sh's version-bump path (run: python3 tools/tests/test_cra_redeploy.py).

Same dependency-free RED/GREEN style as tools/tests/test_gates.py: print PASS/FAIL, exit 1 if
anything failed. Every scenario runs the real script as a subprocess against a synthetic
temp HOME that mimics ~/.claude/plugins/ layout - the real ~/.claude is never touched.

WHY THIS EXISTS
---------------
The `python3 - ... <<'PYEOF' ... PYEOF` heredoc that edits installed_plugins.json during a
version bump had its exit status ignored: a failure inside the heredoc (e.g. the plugin key
missing from installed_plugins.json) still fell through to `CACHE="$NEW_CACHE"` and printed
"stood up ... and updated installed_plugins.json" - success output for a run that changed
nothing useful and left a half-created version dir behind. This pins the fix: the heredoc's
exit status must be checked, the installed_plugins.json backup restored, the half-created
version dir removed (only if this run created it), an error printed, and the script must
exit non-zero.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../tools/tests
REPO_ROOT = HERE.parent.parent                   # repo root (contains clinical-research-assistant/)
SCRIPT = REPO_ROOT / "tools" / "cra-redeploy.sh"
PLUGIN_JSON = REPO_ROOT / "clinical-research-assistant" / ".claude-plugin" / "plugin.json"

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def real_version() -> str:
    return json.loads(PLUGIN_JSON.read_text())["version"]


def make_fake_home(old_version: str, marketplace: str, installed_plugins: dict) -> Path:
    """A temp HOME with a ~/.claude/plugins layout: an OLD_VERSION cache dir (so cra-redeploy.sh
    detects a version bump against the repo's real, newer plugin.json version) and an
    installed_plugins.json with the given content."""
    home = Path(tempfile.mkdtemp(prefix="cra_redeploy_test_home_"))
    old_cache = home / ".claude" / "plugins" / "cache" / marketplace / "clinical-research-assistant" / old_version
    old_cache.mkdir(parents=True, exist_ok=True)
    (old_cache / "marker.txt").write_text("old version cache marker\n")
    plugins_dir = home / ".claude" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    (plugins_dir / "installed_plugins.json").write_text(json.dumps(installed_plugins, indent=2))
    return home


def run_script(home: Path, extra_args: "list[str] | None" = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["HOME"] = str(home)
    args = ["bash", str(SCRIPT), *(extra_args or [])]
    return subprocess.run(args, capture_output=True, text=True, env=env, timeout=60)


def new_cache_dir(home: Path, version: str, marketplace: str) -> Path:
    return home / ".claude" / "plugins" / "cache" / marketplace / "clinical-research-assistant" / version


def main() -> int:
    version = real_version()
    old_version = "0.0.1-test-old"
    marketplace = "test-marketplace"

    # ------------------------------------------------------------ case 1
    # installed_plugins.json is missing the plugin key entirely -> the heredoc's own
    # `sys.exit("plugin key not found ...")` must be caught, not ignored.
    home1 = make_fake_home(old_version, marketplace, {"plugins": {}})
    try:
        original_installed = (home1 / ".claude" / "plugins" / "installed_plugins.json").read_text()
        proc = run_script(home1)

        check(proc.returncode != 0,
              f"case1 (missing plugin key): script exits non-zero (got {proc.returncode})")
        combined = proc.stdout + proc.stderr
        check("✗" in combined, "case1: an error marker is printed")
        check("✓ stood up" not in combined,
              "case1: success message is NOT printed when the heredoc actually failed")

        installed_after = (home1 / ".claude" / "plugins" / "installed_plugins.json").read_text()
        check(installed_after == original_installed,
              "case1: installed_plugins.json is restored to its pre-run content")

        ncd = new_cache_dir(home1, version, marketplace)
        check(not ncd.exists(),
              "case1: the half-created version cache dir is removed on failure")
    finally:
        shutil.rmtree(home1, ignore_errors=True)

    # ------------------------------------------------------------ case 2
    # a valid plugin key -> the version bump succeeds (regression check on the happy path).
    plugin_key = f"clinical-research-assistant@{marketplace}"
    good_installed = {"plugins": {plugin_key: [{"version": old_version,
                                                "installPath": f".../cache/{marketplace}/"
                                                                f"clinical-research-assistant/{old_version}"}]}}
    home2 = make_fake_home(old_version, marketplace, good_installed)
    try:
        proc = run_script(home2)
        combined = proc.stdout + proc.stderr
        check("✓ stood up" in combined,
              f"case2 (valid plugin key): success message is printed (rc={proc.returncode})\n{combined[-800:]}")

        ncd = new_cache_dir(home2, version, marketplace)
        check(ncd.is_dir(), "case2: the new version cache dir was created")

        installed_after = json.loads((home2 / ".claude" / "plugins" / "installed_plugins.json").read_text())
        entry = installed_after["plugins"][plugin_key][0]
        check(entry["version"] == version,
              f"case2: installed_plugins.json version is bumped to {version} (got {entry['version']})")
    finally:
        shutil.rmtree(home2, ignore_errors=True)

    # ------------------------------------------------------------ case 3
    # --dry-run must still write nothing, even against the same missing-plugin-key fixture.
    home3 = make_fake_home(old_version, marketplace, {"plugins": {}})
    try:
        original_installed = (home3 / ".claude" / "plugins" / "installed_plugins.json").read_text()
        proc = run_script(home3, ["--dry-run"])

        installed_after = (home3 / ".claude" / "plugins" / "installed_plugins.json").read_text()
        check(installed_after == original_installed,
              "case3 (--dry-run): installed_plugins.json is untouched")

        ncd = new_cache_dir(home3, version, marketplace)
        check(not ncd.exists(), "case3 (--dry-run): no new version cache dir is created")

        combined = proc.stdout + proc.stderr
        check("dry run" in combined.lower(), "case3 (--dry-run): output says it is a dry run")
    finally:
        shutil.rmtree(home3, ignore_errors=True)

    print()
    print(f"{len(FAILS)} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
