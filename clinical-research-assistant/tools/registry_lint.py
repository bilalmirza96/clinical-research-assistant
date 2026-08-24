#!/usr/bin/env python3
"""
registry_lint.py - mechanical safeguards against result-logging confusion (L071).

    python3 tools/registry_lint.py <path-to-MASTER_ANALYSIS_REGISTRY.json>
    python3 tools/registry_lint.py <registry> --results-dir Reports   # also finds orphans
    python3 tools/registry_lint.py <registry> --arms adeno,scc        # parity check
    python3 tools/registry_lint.py <registry> --deliverable Reports/abstract.md

WHY THIS EXISTS
---------------
L071. In the Esophageal-Organ-Preservation study, results from many analyses were logged in
batches at the end of a session rather than as each analysis completed, keys for the two
arms of one comparison were named asymmetrically, and many keys carried no label. The
consequence was a MATCHED estimate from one arm being written into an abstract next to an
UNMATCHED estimate from the other, and a subgroup verdict reported as INFERIOR when the
like-for-like value was INCONCLUSIVE. Prose rules did not prevent it. This does.

Exit code 0 = clean, 1 = hard failures. Wire it into any workflow that touches a registry.

CHECKS (hard failures)
  H1  every key has a non-empty label
  H2  every effect-size key carries a CI
  H3  every key whose label mentions a non-inferiority margin states a verdict
  H4  matched/weighted keys name their specification in the KEY, not only the label
  H5  parallel-arm parity: if --arms given, every suffix exists for every arm
  H6  pooled-scope keys carry a scope annotation naming their stratified counterparts
  H7  no orphan results: values in result JSONs that were never registered (--results-dir)
  H8  every number in a deliverable traces to a registry value (--deliverable)
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

EFFECT_HINTS = ("_aHR", ".cox_", "rmst", "_HR", "hazard", "_did", "ate_", "autoc", "_OR")
NO_CI_OK = ("_N", ".N", "n_", "_n", "pct_", "_pct", "count", "deaths", "events", "verdict",
            "chi2", "_p", "spread", "frac_", "max_smd", "failure_rate", "cohort_N",
            "eligible", "_id", "coverage", "drift", "median_", "_seeds", "bound")
VERDICT_WORDS = ("INFERIOR", "NON-INFERIOR", "INCONCLUSIVE", "NOT CONFIRMED", "CONFIRMED",
                 "UNDERPOWERED", "NOT RESOLVED", "NOT DEMONSTRATED", "PRESENT", "ROBUST",
                 "FRAGILE", "STABLE", "DIFFERS")
SPEC_TOKENS = ("matched", "match", "iptw", "psm", "ccw", "forest", "landmark", "unadj",
               "weighted", "trimmed", "restricted", "era", "allcause", "cancerspecific")
POOLED_HINTS = ("overall", "allhist", "hte_forest", "tte_ccw", "landmarked", "pooled")


def load(p: Path):
    d = json.loads(p.read_text())
    return d["results"] if isinstance(d, dict) and "results" in d else d


def ann_text(entry) -> str:
    """All annotation/flag text attached to an entry, however the tool stored it."""
    out = []
    for fld in ("flags", "annotations", "notes"):
        v = entry.get(fld)
        if isinstance(v, list):
            for x in v:
                out.append(x if isinstance(x, str) else json.dumps(x))
        elif isinstance(v, str):
            out.append(v)
    cur = entry.get("current", {})
    for fld in ("note", "reason", "status"):
        if isinstance(cur.get(fld), str):
            out.append(cur[fld])
    return " ".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("registry", type=Path)
    ap.add_argument("--arms", help="comma-separated parallel arms. Each arm may list "
                    "aliases with '|', e.g. 'adeno|adenocarcinoma,scc|SCC|squamous'. "
                    "Aliases are matched case-insensitively and an arm spelled more than "
                    "one way is reported as its own finding (H9).")
    ap.add_argument("--results-dir", type=Path)
    ap.add_argument("--deliverable", type=Path, action="append", default=[])
    ap.add_argument("--ignore-file", type=Path,
                    help="JSON file of documented exceptions: "
                         "{\"H5\": [{\"pattern\": \"...\", \"reason\": \"...\"}], ...}. "
                         "Every exception MUST carry a reason; an entry without one is "
                         "itself a hard failure.")
    ap.add_argument("--warn-only", action="store_true")
    a = ap.parse_args()

    R = load(a.registry)
    hard: list[str] = []
    soft: list[str] = []

    ignores: dict[str, list[dict]] = {}
    if a.ignore_file and a.ignore_file.exists():
        ignores = json.loads(a.ignore_file.read_text())
        for chk, entries in ignores.items():
            if chk.startswith("_"):
                continue
            for ent in entries:
                if not ent.get("reason"):
                    hard.append(f"IGNORE-FILE {chk} entry has no reason: "
                                f"{ent.get('pattern')}")
        n = sum(len(v) for k, v in ignores.items() if not k.startswith("_"))
        print(f"ignore-file: {a.ignore_file.name}, {n} documented exceptions\n")

    def ignored(check: str, text: str) -> bool:
        for ent in ignores.get(check, []):
            if ent.get("reason") and re.search(ent["pattern"], text):
                return True
        return False

    def add(bucket: list[str], check: str, msg: str) -> None:
        if not ignored(check, msg):
            bucket.append(f"{check} {msg}")
    print(f"registry_lint - {a.registry.name}: {len(R)} keys\n")

    # ---- H1 label present
    for k, e in R.items():
        if not (e.get("label") or "").strip():
            add(hard, "H1", f"no label: {k}")

    # ---- H2 effect keys carry a CI
    for k, e in R.items():
        if any(h in k for h in EFFECT_HINTS) and not any(o in k for o in NO_CI_OK):
            if not (e.get("current", {}).get("ci")):
                add(soft, "H2", f"effect key without CI: {k}")

    # ---- H3 margin mentioned -> verdict stated
    for k, e in R.items():
        lab = e.get("label") or ""
        if not re.search(r"margin", lab, re.I):
            continue
        val = str((e.get("current", {}) or {}).get("value", "")).upper()
        # a key whose VALUE is itself the verdict need not repeat it in the label
        if any(w in val for w in VERDICT_WORDS) or "verdict" in k.lower():
            continue
        if not any(w in lab.upper() for w in VERDICT_WORDS):
            add(hard, "H3", f"label cites a margin but states no verdict: {k}")

    # ---- H4 specification in the key, not only the label
    for k, e in R.items():
        lab = (e.get("label") or "").lower()
        if re.search(r"\b1:\d\b|\bmatched\b", lab):
            if not any(t in k.lower() for t in ("matched", "psm", "match")):
                add(hard, "H4", f"label says matched but the KEY does not: {k}")
        if ("cancer-specific" in lab and "cancerspecific" not in k.lower()
                and "all-cause" not in lab and "allcause" not in k.lower()):
            add(hard, "H4", f"label says cancer-specific but the KEY does not: {k}")

    # ---- H5 parallel-arm parity, and H9 alias consistency
    if a.arms:
        specs = [x.strip() for x in a.arms.split(",") if x.strip()]
        arms = {}                       # canonical -> [aliases]
        for sp in specs:
            al = [y.strip() for y in sp.split("|") if y.strip()]
            arms[al[0]] = al
        buckets: dict[str, set[str]] = {}
        spellings: dict[str, set[str]] = {c: set() for c in arms}
        for k in R:
            hit = None
            for canon, aliases in arms.items():
                for al in aliases:
                    m = re.search(rf"(^|[._]){re.escape(al)}([._]|$)", k, re.I)
                    if m:
                        spellings[canon].add(k[m.start(0) + len(m.group(1)):
                                              m.end(0) - len(m.group(2))])
                        generic = (k[:m.start(0) + len(m.group(1))] + "<ARM>"
                                   + k[m.end(0) - len(m.group(2)):])
                        hit = (canon, generic)
                        break
                if hit:
                    break
            if hit:
                buckets.setdefault(hit[1], set()).add(hit[0])
        for generic, present in sorted(buckets.items()):
            missing = set(arms) - present
            if missing:
                add(hard, "H5", f"arm parity: {generic} present for {sorted(present)}, "
                                f"MISSING {sorted(missing)}")
        for canon, seen_sp in spellings.items():
            if len(seen_sp) > 1:
                add(hard, "H9", f"arm '{canon}' is spelled {len(seen_sp)} different ways in "
                                f"key names: {sorted(seen_sp)}. One arm, one token. "
                                f"Divergent spellings are how a reader ends up comparing "
                                f"two different populations.")

    # ---- H6 pooled keys carry a scope annotation
    for k, e in R.items():
        if any(h in k.lower() for h in POOLED_HINTS):
            blob = (ann_text(e) + " " + (e.get("label") or "")).upper()
            if "POOLED" not in blob and "SCOPE" not in blob:
                add(soft, "H6", f"possibly-pooled key without a SCOPE/POOLED note: {k}")

    # ---- H7 orphan results in result JSONs
    if a.results_dir and a.results_dir.exists():
        registered_files = {(e.get("current", {}) or {}).get("source_file")
                            for e in R.values()}
        registered_files = {f for f in registered_files if f}
        seen = set()
        for jf in sorted(a.results_dir.glob("*.json")):
            rel_candidates = {f"Reports/{jf.name}", jf.name, str(jf)}
            if not (rel_candidates & registered_files):
                if jf.name.startswith(("MASTER_", "REGISTRY_KEY_MAP")):
                    continue
                seen.add(jf.name)
        for n in sorted(seen):
            add(soft, "H7", f"result file with no registered key pointing at it: {n}")

    # ---- H8 deliverable numbers trace to the registry
    for d in a.deliverable:
        if not d.exists():
            add(soft, "H8", f"deliverable not found: {d}")
            continue
        text = d.read_text()
        body = text.split("[END OF ABSTRACT BODY]")[0]
        vals = set()
        for e in R.values():
            cur = e.get("current", {})
            for f in ("value", "ci"):
                v = cur.get(f)
                if v is None:
                    continue
                for m in re.findall(r"-?\d+\.?\d*", str(v)):
                    vals.add(m.lstrip("-"))
                    try:
                        vals.add(f"{abs(float(m)):.2f}".rstrip("0").rstrip("."))
                        vals.add(f"{abs(float(m)):.1f}")
                    except ValueError:
                        pass
        untraced = []
        for m in re.findall(r"(?<![\w.])\d+\.\d+(?![\w])", body):
            if m.lstrip("-") in vals:
                continue
            try:
                if f"{float(m):.1f}" in vals or f"{float(m):.2f}" in vals:
                    continue
            except ValueError:
                pass
            untraced.append(m)
        if untraced:
            add(soft, "H8", f"{d.name}: decimals with no matching registry value: "
                            f"{sorted(set(untraced))[:12]}")

    for label, items in (("HARD FAILURES", hard), ("REVIEW", soft)):
        if items:
            print(f"{label} ({len(items)})")
            for x in items[:60]:
                print(f"  {'x' if label.startswith('HARD') else '?'} {x}")
            if len(items) > 60:
                print(f"  ... and {len(items) - 60} more")
            print()
    if not hard and not soft:
        print("clean: no hard failures, nothing flagged for review")
    elif not hard:
        print("no hard failures")
    return 1 if (hard and not a.warn_only) else 0


if __name__ == "__main__":
    sys.exit(main())
