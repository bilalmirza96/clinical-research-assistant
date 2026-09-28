#!/usr/bin/env python3
"""Tests pinning seven lessons-log entries to the linters/tools that enforce them
(run: python3 tools/tests/test_linters.py).

Same dependency-free style as skills/internal/analyze/tests/test_study_design_tools.py:
print PASS/FAIL/SKIP per assertion, exit 1 if anything failed. Fixtures are built at
runtime in a temp dir (tempfile) - nothing is written into the repo.

Lessons covered (skills/references/lessons-log.json):
  L045  single consolidated analysis registry; upsert with history[]; nothing lost
        -> skills/internal/analyze/scripts/analysis_registry.py (upsert/flag/render)
           + tools/registry_lint.py H7 (scattered result files never folded into the registry)
  L071  real-time, self-describing, symmetric result logging
        -> tools/registry_lint.py (H1 label, H4 spec-in-key, H5 arm parity, H9 alias spelling)
  L021  Results must be the largest abstract section by word/character count
        -> tools/voice_check.py --sections
  L062  house academic voice: no em dashes, no banned transitions, no AI-tell phrases
        -> tools/voice_check.py
  L087  analysis ladder order; two adjusted models only (crude/modelA/modelB, ...)
        -> skills/internal/analyze/scripts/ladder_table.py
           ALREADY COVERED by skills/internal/analyze/tests/test_study_design_tools.py
           (rung order, N drift, direction flip, skipped-rung reasons, two-adjusted-models-
           only via "Unknown rung 'ses'"). Gap filled here only: the survival=True path,
           which requires an explicit adjusted-KM ("adjsurv") rung or a stated skip reason,
           and is never exercised by that file (its rungs list never passes survival=True).
  L088  cohort inclusion/exclusion curated once, counted by group, reconciled exactly
        -> skills/internal/analyze/scripts/cohort_flow.py
           ALREADY COVERED by test_study_design_tools.py (differential-exclusion flagging,
           filter_operations.json n_in/n_out by group, assert_n / assert_same_cohort exact
           reconciliation). Gap filled here only: the two guardrails on the cohort's identity
           itself (duplicated cohort-unit id at construction; a mask with unresolved missing
           values) that that file never exercises.
  L089  data dictionary dossier read before any variable is used
        -> skills/internal/analyze/scripts/dictionary_audit.py
           check_recode_map/audit_frame ALREADY COVERED by test_study_design_tools.py (via
           direct import). Gap filled here: dictionary_audit.py also ships a CLI
           (--dossier/--map/--var/--data) that no existing test invokes as a session would;
           this file pins that real interface with subprocess.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent            # .../clinical-research-assistant/tools/tests
ROOT = HERE.parent.parent                          # .../clinical-research-assistant (plugin root)
TOOLS = ROOT / "tools"
SCRIPTS = ROOT / "skills" / "internal" / "analyze" / "scripts"

sys.path.insert(0, str(SCRIPTS))
import cohort_flow as CF          # noqa: E402  (L088 gap-fill, imported like test_study_design_tools.py)
import ladder_table as LT         # noqa: E402  (L087 gap-fill, imported like test_study_design_tools.py)
import numpy as np                # noqa: E402
import pandas as pd               # noqa: E402

FAILS: list[str] = []
SKIPS: list[str] = []


def check(cond: bool, msg: str, lesson: str) -> None:
    print(("PASS " if cond else "FAIL ") + f"[{lesson}] {msg}")
    if not cond:
        FAILS.append(f"[{lesson}] {msg}")


def skip(msg: str, lesson: str) -> None:
    print(f"SKIP [{lesson}] {msg}")
    SKIPS.append(f"[{lesson}] {msg}")


def run_cli(script: Path, args: list[str]) -> subprocess.CompletedProcess:
    """Invoke a tool's CLI exactly the way a session would: `python3 <script> <args>`."""
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True)


def write(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, str):
        path.write_text(obj)
    else:
        path.write_text(json.dumps(obj, indent=2))
    return path


# =====================================================================================
# L045 - Single Consolidated Analysis Registry: upsert/history preservation, UNSOURCED
#        never guessed, and (via registry_lint H7) no scattered result files left outside
#        the one registry.
# =====================================================================================
def test_L045_single_consolidated_registry():
    tmp = Path(tempfile.mkdtemp())
    reg = tmp / "MASTER_ANALYSIS_REGISTRY.json"
    script = SCRIPTS / "analysis_registry.py"
    qid = "NCDB.os.crude_HR"

    r = run_cli(script, ["init", "--registry", str(reg), "--project", "TestProj"])
    check(r.returncode == 0 and reg.exists(), "init creates a single registry file", "L045")

    r = run_cli(script, ["upsert", "--registry", str(reg), "--id", qid, "--domain", "NCDB",
                        "--label", "Crude OS HR", "--value", "1.30", "--ci", "1.20,1.41",
                        "--p", "<.001", "--n", "1000", "--analysis-id", "V1",
                        "--source-file", "Reports/V1_os.json", "--reason", "initial"])
    check("[upsert:added]" in r.stdout, "negative: first upsert of a new quantity is added", "L045")

    # re-running with the identical value must not fabricate history noise (nothing "lost"
    # cuts both ways: nothing spurious gets recorded either)
    r = run_cli(script, ["upsert", "--registry", str(reg), "--id", qid, "--domain", "NCDB",
                        "--label", "Crude OS HR", "--value", "1.30", "--ci", "1.20,1.41",
                        "--p", "<.001", "--n", "1000", "--analysis-id", "V1",
                        "--source-file", "Reports/V1_os.json", "--reason", "initial"])
    check("[upsert:confirmed]" in r.stdout,
          "negative: an unchanged re-run is a no-op confirm, not a new history entry", "L045")
    entry = json.loads(reg.read_text())["results"][qid]
    check(entry["history"] == [], "negative: confirming an unchanged value adds no history noise", "L045")

    # a changed value must supersede: old value preserved in history[], nothing lost
    r = run_cli(script, ["upsert", "--registry", str(reg), "--id", qid, "--domain", "NCDB",
                        "--label", "Crude OS HR (V2)", "--value", "1.14", "--ci", "1.11,1.17",
                        "--p", "<.001", "--n", "1050", "--analysis-id", "V2",
                        "--source-file", "Reports/V2_os.json", "--reason", "recomputed"])
    check("[upsert:superseded]" in r.stdout, "positive: a changed value triggers supersession", "L045")
    entry = json.loads(reg.read_text())["results"][qid]
    check(entry["current"]["value"] == "1.14", "current holds the newest value", "L045")
    check(len(entry["history"]) == 1 and entry["history"][0]["value"] == "1.30",
          "the superseded prior value is preserved in history[], nothing lost", "L045")

    # a quantity no analysis computes must be flag-able as UNSOURCED, never guessed
    run_cli(script, ["flag", "--registry", str(reg), "--id", "NCDB.tmb_high_OR",
                    "--note", "no analysis file computes this quantity"])
    md = (tmp / "MASTER_ANALYSIS_REGISTRY.md").read_text()
    check("UNSOURCED" in md and "NCDB.tmb_high_OR" in md,
          "negative: a flagged UNSOURCED quantity surfaces under its own heading, not silently omitted", "L045")

    # positive: a scattered result file the registry never points at (the L045 failure mode -
    # "scattered date-stamped analysis outputs") is caught by registry_lint H7
    results_dir = tmp / "Reports"
    results_dir.mkdir(exist_ok=True)
    write(results_dir / "V1_os.json", {"os_hr": 1.30})          # registered via source_file above
    write(results_dir / "V9_side_channel.json", {"orphan": True})  # never referenced by any key

    lint = TOOLS / "registry_lint.py"
    r = run_cli(lint, [str(reg), "--results-dir", str(results_dir)])
    check("V9_side_channel.json" in r.stdout,
          "positive: an un-registered result file outside the one registry is flagged (H7)", "L045")

    (results_dir / "V9_side_channel.json").unlink()
    r = run_cli(lint, [str(reg), "--results-dir", str(results_dir)])
    check("V9_side_channel.json" not in r.stdout,
          "negative: once every result file is registered, nothing is flagged as orphaned", "L045")


# =====================================================================================
# L071 - real-time, self-describing, symmetric result logging: every key has a label,
#        matched/weighted specs live in the KEY not just the label, parallel arms are
#        present for every generic key and are spelled one way.
# =====================================================================================
def test_L071_self_describing_symmetric_keys():
    lint = TOOLS / "registry_lint.py"
    arms = "adeno,scc|SCC|squamous"

    bad = {
        "H1.nolabel_key": {"label": "", "current": {"value": 1.0}},
        # H5: adeno has a matched-pairs key; scc has no equivalent -> arm parity fails
        "NCDB.adeno.matched.pairs_N": {"label": "Adeno 1:1 matched pairs, N", "current": {"value": 900}},
        # H4: label says "1:1 matched" but the KEY carries no matched/psm/match token
        "NCDB.adeno.channel_HR": {"label": "Adeno 1:1 matched channel-specific HR",
                                  "current": {"value": 1.2, "ci": [1.1, 1.3]}},
        # H9: the same "scc" arm spelled three different ways across keys
        "NCDB.scc.endpoint_HR": {"label": "SCC endpoint HR", "current": {"value": 0.9, "ci": [0.8, 1.0]}},
        "NCDB.SCC.other_HR": {"label": "SCC other HR", "current": {"value": 0.95, "ci": [0.85, 1.05]}},
        "NCDB.squamous.third_HR": {"label": "Squamous third HR", "current": {"value": 0.99, "ci": [0.9, 1.1]}},
    }
    good = {
        "NCDB.adeno.matched.pairs_N": {"label": "Adeno 1:1 matched pairs, N", "current": {"value": 900}},
        "NCDB.scc.matched.pairs_N": {"label": "SCC 1:1 matched pairs, N", "current": {"value": 850}},
        "NCDB.adeno.matched.channel_HR": {"label": "Adeno 1:1 matched channel-specific HR",
                                          "current": {"value": 1.2, "ci": [1.1, 1.3]}},
        "NCDB.scc.matched.channel_HR": {"label": "SCC 1:1 matched channel-specific HR",
                                        "current": {"value": 0.9, "ci": [0.8, 1.0]}},
        "NCDB.adeno.endpoint_HR": {"label": "Adeno endpoint HR", "current": {"value": 1.1, "ci": [1.0, 1.2]}},
        "NCDB.scc.endpoint_HR": {"label": "SCC endpoint HR", "current": {"value": 0.9, "ci": [0.8, 1.0]}},
    }
    tmp = Path(tempfile.mkdtemp())
    bad_path = write(tmp / "bad_registry.json", bad)
    good_path = write(tmp / "good_registry.json", good)

    r = run_cli(lint, [str(bad_path), "--arms", arms])
    check(r.returncode == 1, "positive: an asymmetric, unlabeled, key-vs-label registry is a hard failure", "L071")
    check("H1" in r.stdout and "H1.nolabel_key" in r.stdout,
          "positive: a key with no label is flagged (H1)", "L071")
    check("H4" in r.stdout and "channel_HR" in r.stdout,
          "positive: 'matched' stated only in the label, not the key, is flagged (H4)", "L071")
    check("H5" in r.stdout and "MISSING" in r.stdout and "'scc'" in r.stdout,
          "positive: a key present for one arm with no counterpart for the other is flagged (H5)", "L071")
    check("H9" in r.stdout and "spelled" in r.stdout,
          "positive: one arm spelled 'scc' / 'SCC' / 'squamous' across keys is flagged (H9)", "L071")

    r = run_cli(lint, [str(good_path), "--arms", arms])
    check(r.returncode == 0, "negative: a labeled, symmetric, one-spelling-per-arm registry passes clean", "L071")
    check("HARD FAILURES" not in r.stdout, "negative: no hard failures reported for the compliant registry", "L071")


# =====================================================================================
# L021 - Results must be the largest structured-abstract section by character count,
#        at least 2x Methods and 2x Conclusions.
# =====================================================================================
def test_L021_results_largest_section():
    voice = TOOLS / "voice_check.py"
    tmp = Path(tempfile.mkdtemp())

    # positive: Methods is padded out until it approaches/exceeds Results - mis-weighted
    bad_text = (
        "Introduction: Short background sentence on the clinical relevance of this question.\n\n"
        "Methods: We used a large retrospective national registry cohort with propensity score "
        "matching across many pre-specified covariates, sensitivity analyses stratified by stage, "
        "age and comorbidity burden, multiple imputation for missing covariates, E-value "
        "quantification of unmeasured confounding across the full study period, and additional "
        "bootstrap resampling used throughout for confidence interval estimation and robustness.\n\n"
        "Results: Of 1,000 patients, 400 (40%) received treatment and outcomes differed by group.\n\n"
        "Conclusions: Treatment was associated with improved outcomes in this cohort.\n"
    )
    bad_path = write(tmp / "bad_abstract.md", bad_text)
    r = run_cli(voice, [str(bad_path), "--sections"])
    check(r.returncode == 1, "positive: a mis-weighted abstract (Methods approaching Results) is a hard failure", "L021")
    check("section weight" in r.stdout, "positive: the section-weight rule names the violation", "L021")

    # negative: Results is comfortably >= 2x both Methods and Conclusions, and the largest overall
    good_text = (
        "Introduction: Brief background statement.\n\n"
        "Methods: Retrospective cohort study with adjusted regression.\n\n"
        "Results: Of 1,000 patients (mean age 64 years), 400 (40%) received treatment. "
        "Treated patients had improved overall survival (adjusted hazard ratio 0.75, "
        "95% CI 0.65 to 0.87, P < .001) and improved recurrence-free survival (adjusted "
        "hazard ratio 0.80, 95% CI 0.70 to 0.92, P = .002) compared with untreated patients, "
        "with consistent effects across pre-specified age and stage subgroups.\n\n"
        "Conclusions: Treatment was associated with better outcomes in this cohort.\n"
    )
    good_path = write(tmp / "good_abstract.md", good_text)
    r = run_cli(voice, [str(good_path), "--sections"])
    check(r.returncode == 0, "negative: a Results-weighted abstract passes the section-weight check", "L021")
    check("section weight" not in r.stdout, "negative: no section-weight violation is reported", "L021")


# =====================================================================================
# L062 - House Academic Voice: no em dashes (still a hard failure).
# L103 - the banned-transition and AI-tell word lists were removed 2026-09-28, so
#        Furthermore/Moreover/Additionally/Interestingly and words such as "robust",
#        "highlight" or "utilizing" must NOT fail the gate.
# =====================================================================================
def test_L062_house_academic_voice():
    voice = TOOLS / "voice_check.py"
    tmp = Path(tempfile.mkdtemp())

    bad_text = ("The study examined the mechanism"
                "\u2014which remained unclear before this analysis.\n")
    bad_path = write(tmp / "bad_voice.md", bad_text)
    r = run_cli(voice, [str(bad_path)])
    check(r.returncode == 1, "positive: an em dash is a hard failure", "L062")
    check("em dash" in r.stdout, "positive: the em dash is flagged", "L062")

    good_text = ("The study examined the mechanism, which remained unclear before this analysis. "
                "Patients were followed for two years, and outcomes were recorded prospectively.\n")
    good_path = write(tmp / "good_voice.md", good_text)
    r = run_cli(voice, [str(good_path)])
    check(r.returncode == 0, "negative: plain compliant prose passes with no hard failures", "L062")
    check("HARD FAILURES" not in r.stdout, "negative: no hard-failure section is printed", "L062")


def test_L103_no_word_bans():
    voice = TOOLS / "voice_check.py"
    tmp = Path(tempfile.mkdtemp())
    text = ("Furthermore, the robust association persisted. Moreover, utilizing a second cohort, "
            "the findings highlight a consistent pattern. Additionally, rates were similar. "
            "Interestingly, the effect was larger in older patients, which sheds light on selection.\n")
    path = write(tmp / "formerly_banned.md", text)
    r = run_cli(voice, [str(path)])
    check(r.returncode == 0, "negative: formerly banned transitions and AI-tell words no longer fail", "L103")
    check("banned transition" not in r.stdout and "AI-tell" not in r.stdout,
          "negative: no word-ban message is printed", "L103")
    check("robust" not in r.stdout, "negative: 'robust' is not flagged as vague praise", "L103")


def test_L103_voice_guide_wired():
    refs = ROOT / "skills" / "references"
    check((refs / "manuscript-voice.md").is_file(), "positive: manuscript-voice.md is installed", "L103")
    style = (refs / "writing-style.md").read_text()
    check("manuscript-voice.md" in style, "positive: writing-style.md points to manuscript-voice.md", "L103")
    check("Banned transitions" not in style and "Banned AI-tell" not in style,
          "negative: writing-style.md carries no word-ban rows", "L103")
    for sk in ("write-introduction", "write-methods-results", "write-discussion", "write-abstract"):
        t = (ROOT / "skills" / "internal" / sk / "SKILL.md").read_text()
        check("manuscript-voice.md" in t, f"positive: {sk} points to manuscript-voice.md", "L103")
        check('never use "Furthermore' not in t and 'never "Furthermore' not in t,
              f"negative: {sk} carries no transition ban", "L103")


# =====================================================================================
# L087 GAP-FILL ONLY (full ladder coverage already lives in test_study_design_tools.py -
# rung order, N drift across rungs 1-3, direction flips, skip-reason bookkeeping, and
# "two adjusted models only" via the Unknown-rung-'ses' assertion). What that file never
# exercises: the survival=True path, which additionally requires an adjusted-KM ("adjsurv")
# rung, run or explicitly skipped with a reason.
# =====================================================================================
def test_L087_analysis_ladder_survival_rung():
    rungs = [dict(rung="crude", est=1.2, lo=1.1, hi=1.3, n=500),
             dict(rung="modelA", est=1.15, lo=1.05, hi=1.25, n=500),
             dict(rung="modelB", est=1.10, lo=1.00, hi=1.20, n=500)]

    _, flags = LT.ladder_table(rungs, measure="HR", common=True, survival=True,
                               skipped={"iptw": "x", "mediation": "x", "ml": "x"})
    check(any("'adjsurv'" in fl and "missing" in fl.lower() for fl in flags),
          "positive: survival=True requires an adjusted-KM (adjsurv) rung, run or skipped with a reason", "L087")

    _, flags2 = LT.ladder_table(rungs, measure="HR", common=True, survival=True,
                                skipped={"iptw": "x", "mediation": "x", "ml": "x",
                                        "adjsurv": "no KM curve requested for this endpoint"})
    check(not any("adjsurv" in fl for fl in flags2),
          "negative: a stated reason clears the adjsurv requirement", "L087")


# =====================================================================================
# L088 GAP-FILL ONLY (full cohort-flow coverage already lives in test_study_design_tools.py -
# differential-exclusion flagging by group, filter_operations.json n_in/n_out, exact-N
# reconciliation via assert_n / assert_same_cohort). What that file never exercises: the two
# guardrails on the cohort's identity itself before any step is even recorded.
# =====================================================================================
def test_L088_cohort_identity_guardrails():
    dup = pd.DataFrame({"id": [1, 1, 2], "race": ["A", "A", "B"]})
    try:
        CF.CohortFlow(dup, id_col="id", group_col="race")
        check(False, "positive: a duplicated cohort-unit id is a hard failure at construction", "L088")
    except ValueError as e:
        check("duplicate" in str(e).lower(),
              "positive: a duplicated cohort-unit id is a hard failure at construction", "L088")

    clean = pd.DataFrame({"id": [1, 2, 3], "race": ["A", "A", "B"]})
    try:
        flow = CF.CohortFlow(clean, id_col="id", group_col="race")
        check(True, "negative: unique cohort-unit ids construct without error", "L088")
    except ValueError:
        check(False, "negative: unique cohort-unit ids construct without error", "L088")
        return

    mask_with_na = pd.Series([True, np.nan, False], index=clean.index)
    try:
        flow.include("has data", mask_with_na, rationale="x", ref="x")
        check(False, "positive: a mask with unresolved missing values is a hard failure, not a silent default", "L088")
    except ValueError as e:
        check("missing" in str(e).lower(),
              "positive: a mask with unresolved missing values is a hard failure, not a silent default", "L088")

    clean_mask = pd.Series([True, True, False], index=clean.index)
    try:
        out = flow.include("has data", clean_mask, rationale="x", ref="x")
        check(len(out) == 2, "negative: a fully-resolved mask is accepted and applied", "L088")
    except ValueError:
        check(False, "negative: a fully-resolved mask is accepted and applied", "L088")


# =====================================================================================
# L089 GAP-FILL ONLY (check_recode_map / audit_frame direct-import coverage already lives
# in test_study_design_tools.py, replaying the exact REPEAT DISPARITIES NAACCR 1340 defects).
# What that file never exercises: dictionary_audit.py also ships a CLI
# (--dossier/--map/--var), and no existing test invokes it the way a session actually would.
# =====================================================================================
def test_L089_dictionary_audit_cli():
    script = SCRIPTS / "dictionary_audit.py"
    tmp = Path(tempfile.mkdtemp())

    dossier = {
        "source": "SYNTHETIC test dossier",
        "variables": {
            "REASON": {
                "item": "TEST 0001",
                "storage": "numeric",
                "codes": {"0": "Surgery performed", "1": "Not part of planned first course"},
                "missing_codes": ["9"],
                "forbidden_labels": {"1": ["not recommended"]},
            }
        },
    }
    dossier_path = write(tmp / "dossier.json", dossier)

    bad_map = {"0": "Surgery performed", "1": "Not recommended", "3": "Refused"}
    bad_map_path = write(tmp / "bad_map.json", bad_map)
    r = run_cli(script, ["--dossier", str(dossier_path), "--map", str(bad_map_path), "--var", "REASON"])
    check(r.returncode == 1,
          "positive: an out-of-dictionary code and a forbidden label is a hard failure via the CLI", "L089")
    check("M1" in r.stdout and "code 3" in r.stdout,
          "positive: a code the dictionary does not allow is flagged (M1)", "L089")
    check("M3" in r.stdout and "not recommended" in r.stdout.lower(),
          "positive: a label contradicting the code's definition is flagged (M3)", "L089")

    good_map = {"0": "Surgery performed", "1": "Not part of planned first course", "9": "Unknown"}
    good_map_path = write(tmp / "good_map.json", good_map)
    r = run_cli(script, ["--dossier", str(dossier_path), "--map", str(good_map_path), "--var", "REASON"])
    check(r.returncode == 0,
          "negative: a complete, dictionary-consistent recode map passes clean via the CLI", "L089")


# =====================================================================================
# JSON CONTRACT - all four linters (voice_check, claim_audit, registry_lint, house_style)
# share one --json machine-readable contract: stdout is EXACTLY one JSON object
# {"hard": [...], "soft": [...], "error": null | "<message>"} and nothing else, with exit
# code 0 (no hard findings), 1 (hard findings) or 2 (tool error - missing dependency,
# unreadable/missing path, corrupt document, malformed registry JSON; "error" is set).
# Per linter: clean input -> exit 0, hard empty; violating input -> exit 1; missing path
# -> exit 2, error set, stdout still valid single-object JSON. hooks/exit_gates.py's
# check_json_linter() classifies purely from this contract (see hooks/tests/test_exit_gates.py
# for the HARD FAIL vs. TOOL ERROR wiring through the Stop hook).
# =====================================================================================

def parse_json_stdout(stdout: str):
    """The --json contract requires stdout to be exactly one JSON object and nothing
    else - a strict (not tolerant) parse pins that, independent of exit_gates.py's own
    fallback recovery for stray text."""
    return json.loads(stdout.strip())


def test_json_contract_voice_check():
    voice = TOOLS / "voice_check.py"
    tmp = Path(tempfile.mkdtemp())

    clean_path = write(tmp / "clean.md", "Plain compliant prose with nothing flagged at all.\n")
    r = run_cli(voice, [str(clean_path), "--json"])
    check(r.returncode == 0, "positive: clean input exits 0 under --json", "JSON-voice_check")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and data["error"] is None,
          "positive: clean input has hard=[] and error=null", "JSON-voice_check")

    bad_path = write(tmp / "bad.md", "An em dash—right here is a hard failure.\n")
    r = run_cli(voice, [str(bad_path), "--json"])
    check(r.returncode == 1, "positive: violating input exits 1 under --json", "JSON-voice_check")
    data = parse_json_stdout(r.stdout)
    check(bool(data["hard"]) and data["error"] is None,
          "positive: violating input has a non-empty hard list and error=null", "JSON-voice_check")

    r = run_cli(voice, [str(tmp / "does_not_exist.md"), "--json"])
    check(r.returncode == 2, "positive: missing path exits 2 under --json", "JSON-voice_check")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and isinstance(data["error"], str) and data["error"],
          "positive: missing path sets a non-empty error string, hard stays empty", "JSON-voice_check")


def test_json_contract_claim_audit():
    audit = TOOLS / "claim_audit.py"
    tmp = Path(tempfile.mkdtemp())
    registry = write(tmp / "registry.json", {
        "NCDB.sano_tte.histology_interaction_E1_diff_pp": {
            "label": "histology interaction diff",
            "current": {"value": 7.23, "ci": [1.77, 13.38]},
        }
    })

    clean_path = write(tmp / "clean.md", "Patients were followed prospectively for two years.\n")
    r = run_cli(audit, [str(clean_path), "--registry", str(registry), "--json"])
    check(r.returncode == 0, "positive: clean input exits 0 under --json", "JSON-claim_audit")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and data["error"] is None,
          "positive: clean input has hard=[] and error=null", "JSON-claim_audit")

    bad_path = write(tmp / "bad.md",
                     "The two histologies were not formally compared on this endpoint.\n")
    r = run_cli(audit, [str(bad_path), "--registry", str(registry), "--json"])
    check(r.returncode == 1, "positive: violating input exits 1 under --json", "JSON-claim_audit")
    data = parse_json_stdout(r.stdout)
    check(bool(data["hard"]) and data["error"] is None,
          "positive: a claim the registry contradicts has a non-empty hard list", "JSON-claim_audit")

    r = run_cli(audit, [str(tmp / "does_not_exist.md"), "--registry", str(registry), "--json"])
    check(r.returncode == 2, "positive: missing path exits 2 under --json", "JSON-claim_audit")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and isinstance(data["error"], str) and data["error"],
          "positive: missing path sets a non-empty error string, hard stays empty", "JSON-claim_audit")


def test_json_contract_registry_lint():
    lint = TOOLS / "registry_lint.py"
    tmp = Path(tempfile.mkdtemp())

    clean_reg = write(tmp / "clean_registry.json", {
        "NCDB.os.crude_HR": {"label": "Crude OS HR", "current": {"value": 1.1, "ci": [1.0, 1.2]}},
    })
    r = run_cli(lint, [str(clean_reg), "--json"])
    check(r.returncode == 0, "positive: clean registry exits 0 under --json", "JSON-registry_lint")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and data["error"] is None,
          "positive: clean registry has hard=[] and error=null", "JSON-registry_lint")

    bad_reg = write(tmp / "bad_registry.json", {
        "NCDB.os.crude_HR": {"label": "", "current": {"value": 1.1, "ci": [1.0, 1.2]}},
    })
    r = run_cli(lint, [str(bad_reg), "--json"])
    check(r.returncode == 1, "positive: an unlabeled key exits 1 under --json", "JSON-registry_lint")
    data = parse_json_stdout(r.stdout)
    check(bool(data["hard"]) and data["error"] is None,
          "positive: an unlabeled key (H1) has a non-empty hard list", "JSON-registry_lint")

    r = run_cli(lint, [str(tmp / "does_not_exist.json"), "--json"])
    check(r.returncode == 2, "positive: missing path exits 2 under --json", "JSON-registry_lint")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and isinstance(data["error"], str) and data["error"],
          "positive: missing path sets a non-empty error string, hard stays empty", "JSON-registry_lint")

    malformed = write(tmp / "malformed.json", "not valid json{{{")
    r = run_cli(lint, [str(malformed), "--json"])
    check(r.returncode == 2, "positive: malformed registry JSON exits 2 under --json", "JSON-registry_lint")
    data = parse_json_stdout(r.stdout)
    check(isinstance(data["error"], str) and data["error"],
          "positive: malformed registry JSON sets a non-empty error string", "JSON-registry_lint")


def test_json_contract_house_style():
    house = TOOLS / "house_style.py"
    tmp = Path(tempfile.mkdtemp())
    from docx import Document  # already a hard dependency of house_style.py itself

    # A truly clean fixture is built by letting house_style FIX a fresh document (check=False)
    # in a private import, then verifying --json reports it clean - avoids hand-tracking every
    # default-template font/colour the House Style standard also flags.
    sys.path.insert(0, str(TOOLS))
    import house_style as HS  # noqa: E402
    clean_path = tmp / "clean.docx"
    d = Document()
    d.add_paragraph("Hello world").runs[0].font.name = "Times New Roman"
    d.save(str(clean_path))
    HS.enforce_docx(str(clean_path), check=False)

    r = run_cli(house, [str(clean_path), "--json"])
    check(r.returncode == 0, "positive: clean docx exits 0 under --json", "JSON-house_style")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and data["error"] is None,
          "positive: clean docx has hard=[] and error=null", "JSON-house_style")
    check(Document(str(clean_path)).paragraphs[0].runs[0].font.name == "Times New Roman",
          "positive: --json never mutates the file it checks", "JSON-house_style")

    bad_path = tmp / "bad.docx"
    d2 = Document()
    d2.add_paragraph("Hello world").runs[0].font.name = "Arial"
    d2.save(str(bad_path))
    r = run_cli(house, [str(bad_path), "--json"])
    check(r.returncode == 1, "positive: wrong-font docx exits 1 under --json", "JSON-house_style")
    data = parse_json_stdout(r.stdout)
    check(bool(data["hard"]) and data["error"] is None,
          "positive: wrong-font docx has a non-empty hard list", "JSON-house_style")
    check(Document(str(bad_path)).paragraphs[0].runs[0].font.name == "Arial",
          "positive: --json never mutates the violating file either (report-only, even "
          "without --check)", "JSON-house_style")

    r = run_cli(house, [str(tmp / "does_not_exist.docx"), "--json"])
    check(r.returncode == 2, "positive: missing path exits 2 under --json", "JSON-house_style")
    data = parse_json_stdout(r.stdout)
    check(data["hard"] == [] and isinstance(data["error"], str) and data["error"],
          "positive: missing path sets a non-empty error string, hard stays empty", "JSON-house_style")


def main() -> int:
    tests = [
        test_L045_single_consolidated_registry,
        test_L071_self_describing_symmetric_keys,
        test_L021_results_largest_section,
        test_L062_house_academic_voice,
        test_L103_no_word_bans,
        test_L103_voice_guide_wired,
        test_L087_analysis_ladder_survival_rung,
        test_L088_cohort_identity_guardrails,
        test_L089_dictionary_audit_cli,
        test_json_contract_voice_check,
        test_json_contract_claim_audit,
        test_json_contract_registry_lint,
        test_json_contract_house_style,
    ]
    for t in tests:
        print(f"\n--- {t.__name__} ---")
        t()

    print()
    print(f"{len(FAILS)} failure(s), {len(SKIPS)} skip(s)")
    for s in SKIPS:
        print(f"  SKIP: {s}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
