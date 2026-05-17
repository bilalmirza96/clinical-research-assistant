#!/usr/bin/env python3
"""
analysis_registry.py — Single Consolidated Analysis Registry (SCAR) manager.

PURPOSE (project-agnostic, reusable across all projects):
One living registry file per project holds EVERY still-valid analysis result.
Each result entry carries its current authoritative value AND the full history
of superseded prior values *with it* — so no one ever has to hunt across
V36/V44/V50/... scattered output files again. New analyses UPDATE this file
in place (current value moves into history[], new value becomes current);
nothing is lost; the registry is always the single lookup surface.

FILES (per project, at the project's Reports/ root):
  MASTER_ANALYSIS_REGISTRY.json   machine source of truth (update in place)
  MASTER_ANALYSIS_REGISTRY.md     auto-generated human index (never hand-edit)

USAGE:
  # add/update one result (auto-supersedes prior, preserving it in history[])
  python analysis_registry.py upsert --registry PATH \
      --id SEER.surgery.matched_OR --domain SEER \
      --label "SEER Loc+Reg curative surgery 1:1 PSM matched OR (NHB vs NHW)" \
      --value 0.633 --ci 0.553,0.725 --p "<.001" --n "1,887 pairs" \
      --analysis-id V50 --script V50_SEER_comprehensive_5quantity.py \
      --source-file Reports/V50_..._2026-05-17.json --source-key surgery.psm \
      --date 2026-05-17 --reason "latest SEER comprehensive recomputation"

  # mark a quantity unsourced (no analysis file computes it — flag, never guess)
  python analysis_registry.py flag --registry PATH --id X --note "..."

  # record a consolidation/archive event
  python analysis_registry.py log --registry PATH --analysis-id V50 \
      --script ... --action initial_consolidation \
      --archived-to "Archives/Analysis_consolidated_2026-05-17/"

  # (re)generate the human-readable MD index from the JSON
  python analysis_registry.py render --registry PATH

  # initialize an empty registry for a new project
  python analysis_registry.py init --registry PATH --project "Name"
"""
import argparse
import datetime
import json
import os
import sys


def _now():
    return datetime.date.today().isoformat()


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, data):
    data["registry_meta"]["last_updated"] = _now()
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init(path, project):
    reg = {
        "registry_meta": {
            "project": project,
            "schema_version": "1.0",
            "standard": ("Single Consolidated Analysis Registry (SCAR). "
                         "One file per project; update in place; prior valid "
                         "results carried forward in each entry's history[]. "
                         "Rule: ~/Claude/00_Context/working-rules.md."),
            "created": _now(),
            "last_updated": _now(),
            "current_analysis_vintages": {},
            "update_log": [],
        },
        "results": {},
        "flags": [],
        "archived_sources": [],
    }
    save(path, reg)
    return reg


def _parse_ci(ci):
    if ci in (None, "", "NA"):
        return None
    parts = [p.strip() for p in str(ci).replace("[", "").replace("]", "")
             .split(",")]
    try:
        return [float(parts[0]), float(parts[1])]
    except (ValueError, IndexError):
        return ci  # keep as-is if non-numeric (e.g., "see note")


def upsert(reg, qid, domain, label, value, ci, p, n, analysis_id, script,
           source_file, source_key, date, reason, status="current"):
    new_current = {
        "value": value, "ci": _parse_ci(ci), "p": p, "n": n,
        "analysis_id": analysis_id, "script": script,
        "source_file": source_file, "source_key": source_key,
        "date": date or _now(), "status": status,
    }
    entry = reg["results"].get(qid)
    if entry is None:
        reg["results"][qid] = {
            "domain": domain, "label": label,
            "current": new_current, "history": [],
        }
        return "added"
    # supersession: only archive prior if the value/ci/p actually changed
    cur = entry.get("current") or {}
    if not cur:
        entry["current"] = new_current
        if label:
            entry["label"] = label
        if domain:
            entry["domain"] = domain
        return "added"
    changed = (str(cur.get("value")) != str(value)
               or str(cur.get("ci")) != str(_parse_ci(ci))
               or str(cur.get("p")) != str(p))
    if changed:
        prior = dict(cur)
        prior["status"] = "superseded"
        prior["superseded_by"] = analysis_id
        prior["superseded_on"] = date or _now()
        prior["reason"] = reason or "updated by newer analysis"
        entry["history"].insert(0, prior)
        entry["current"] = new_current
        if label:
            entry["label"] = label
        if domain:
            entry["domain"] = domain
        return "superseded"
    # no change → just refresh provenance pointer
    entry["current"].update({"analysis_id": analysis_id, "script": script,
                             "source_file": source_file,
                             "source_key": source_key,
                             "date": date or _now()})
    return "confirmed"


def flag(reg, qid, note):
    reg.setdefault("flags", [])
    reg["flags"] = [f for f in reg["flags"] if f.get("quantity_id") != qid]
    reg["flags"].append({"quantity_id": qid, "status": "UNSOURCED",
                         "note": note, "flagged_on": _now()})


def log(reg, analysis_id, script, action, archived_to=None, sources=None,
        added=0, superseded=0):
    reg["registry_meta"]["update_log"].append({
        "date": _now(), "analysis_id": analysis_id, "script": script,
        "action": action, "entries_added": added,
        "entries_superseded": superseded,
        "sources_folded": sources or [],
        "sources_archived_to": archived_to,
    })


def render_md(reg, md_path):
    m = reg["registry_meta"]
    lines = [
        f"# MASTER ANALYSIS REGISTRY — {m.get('project','')}",
        "",
        "> AUTO-GENERATED from `MASTER_ANALYSIS_REGISTRY.json` by "
        "`analysis_registry.py render`. **Do not hand-edit this file.**",
        "> Single source of truth for every still-valid analysis result in "
        "this project. Each row is the *current* authoritative value; prior "
        "superseded values are preserved in the JSON `history[]` of that "
        "entry (and summarized below).",
        "",
        f"- **Schema:** {m.get('schema_version')}  |  **Created:** "
        f"{m.get('created')}  |  **Last updated:** {m.get('last_updated')}",
        f"- **Standard:** {m.get('standard','')}",
        "",
        "## Current analysis vintages",
        "",
    ]
    for k, v in (m.get("current_analysis_vintages") or {}).items():
        lines.append(f"- **{k}:** {v}")
    lines += ["", "## Results (current authoritative values)", "",
              "| ID | Domain | Value | 95% CI | P | n | Source | Date |",
              "|---|---|---|---|---|---|---|---|"]
    for qid, e in sorted(reg.get("results", {}).items()):
        c = e.get("current") or {}
        if not c:
            lines.append(
                f"| `{qid}` | {e.get('domain','')} | _UNSOURCED_ |  |  |  "
                f"|  |  |")
            continue
        ci = c.get("ci")
        ci_s = (f"{ci[0]}–{ci[1]}" if isinstance(ci, list) and len(ci) == 2
                else (ci or ""))
        lines.append(
            f"| `{qid}` | {e.get('domain','')} | {c.get('value','')} | "
            f"{ci_s} | {c.get('p','')} | {c.get('n','')} | "
            f"{c.get('analysis_id','')} | {c.get('date','')} |")
    # superseded history
    hist = [(qid, h) for qid, e in reg.get("results", {}).items()
            for h in e.get("history", [])]
    if hist:
        lines += ["", "## Superseded values (carried with their entry)", "",
                  "| ID | Old value | Old CI | Superseded by | On | Reason |",
                  "|---|---|---|---|---|---|"]
        for qid, h in sorted(hist, key=lambda x: x[0]):
            ci = h.get("ci")
            ci_s = (f"{ci[0]}–{ci[1]}" if isinstance(ci, list)
                    and len(ci) == 2 else (ci or ""))
            lines.append(
                f"| `{qid}` | {h.get('value','')} | {ci_s} | "
                f"{h.get('superseded_by','')} | {h.get('superseded_on','')} "
                f"| {h.get('reason','')} |")
    flags = reg.get("flags", [])
    if flags:
        lines += ["", "## UNSOURCED / FLAGGED (no analysis file computes "
                  "this — never guessed)", ""]
        for f in flags:
            lines.append(f"- `{f.get('quantity_id')}` — {f.get('note')}")
    arch = reg.get("archived_sources", [])
    if arch:
        lines += ["", "## Archived source files (folded into this registry)",
                  ""]
        for a in arch:
            lines.append(f"- `{a.get('file')}` → `{a.get('archived_to')}` "
                         f"({a.get('date')})")
    lines += ["", "## Update log", "",
              "| Date | Analysis | Action | +added | superseded | "
              "archived to |", "|---|---|---|---|---|---|"]
    for u in reg["registry_meta"].get("update_log", []):
        lines.append(
            f"| {u.get('date')} | {u.get('analysis_id')} | "
            f"{u.get('action')} | {u.get('entries_added')} | "
            f"{u.get('entries_superseded')} | "
            f"{u.get('sources_archived_to') or ''} |")
    with open(md_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def _md_path(registry_path):
    base = registry_path.rsplit(".json", 1)[0]
    return base + ".md"


def main():
    ap = argparse.ArgumentParser(description="Single Consolidated Analysis "
                                 "Registry manager")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init")
    pi.add_argument("--registry", required=True)
    pi.add_argument("--project", required=True)

    pu = sub.add_parser("upsert")
    for a in ("registry", "id", "domain", "label", "value", "analysis-id",
              "script", "source-file", "source-key", "date", "reason"):
        pu.add_argument(f"--{a}", required=(a in ("registry", "id", "value")))
    pu.add_argument("--ci", default=None)
    pu.add_argument("--p", default=None)
    pu.add_argument("--n", default=None)

    pf = sub.add_parser("flag")
    pf.add_argument("--registry", required=True)
    pf.add_argument("--id", required=True)
    pf.add_argument("--note", required=True)

    pl = sub.add_parser("log")
    pl.add_argument("--registry", required=True)
    pl.add_argument("--analysis-id", required=True)
    pl.add_argument("--script", default="")
    pl.add_argument("--action", required=True)
    pl.add_argument("--archived-to", default=None)

    pr = sub.add_parser("render")
    pr.add_argument("--registry", required=True)

    args = ap.parse_args()

    if args.cmd == "init":
        reg = init(args.registry, args.project)
        render_md(reg, _md_path(args.registry))
        print(f"[init] {args.registry}")
        return

    reg = load(args.registry)
    if args.cmd == "upsert":
        r = upsert(reg, args.id, args.domain, args.label, args.value,
                   args.ci, args.p, args.n, getattr(args, "analysis_id"),
                   args.script, getattr(args, "source_file"),
                   getattr(args, "source_key"), args.date, args.reason)
        save(args.registry, reg)
        render_md(reg, _md_path(args.registry))
        print(f"[upsert:{r}] {args.id}")
    elif args.cmd == "flag":
        flag(reg, args.id, args.note)
        save(args.registry, reg)
        render_md(reg, _md_path(args.registry))
        print(f"[flag] {args.id}")
    elif args.cmd == "log":
        log(reg, getattr(args, "analysis_id"), args.script, args.action,
            getattr(args, "archived_to"))
        save(args.registry, reg)
        render_md(reg, _md_path(args.registry))
        print("[log] recorded")
    elif args.cmd == "render":
        render_md(reg, _md_path(args.registry))
        print(f"[render] {_md_path(args.registry)}")


if __name__ == "__main__":
    sys.exit(main())
