#!/usr/bin/env python3
"""Regenerate the Clinical Research Assistant skill registry.

Scans first-party internal skills plus user-pasted external skills and writes:
- skills/references/skill-registry.yaml
- skills/references/external-skills.md

External skills may be either:
- skills/external/<skill-name>/SKILL.md
- skills/external/<skill-name>.skill  (zip package containing SKILL.md)
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PLUGIN_ROOT / "skills"
INTERNAL_DIR = SKILLS_DIR / "internal"
EXTERNAL_DIR = SKILLS_DIR / "external"
REFERENCES_DIR = SKILLS_DIR / "references"
REGISTRY_PATH = REFERENCES_DIR / "skill-registry.yaml"
EXTERNAL_INDEX_PATH = REFERENCES_DIR / "external-skills.md"


INTERNAL_OVERRIDES = {
    "project-init": {
        "role": "primary-workflow",
        "triggers": ["project init", "new project", "study setup", "scaffold", "IRB", "study specification"],
    },
    "resume-project": {
        "role": "primary-workflow",
        "triggers": ["resume", "continue project", "project state", "pick up", "checkpoint"],
    },
    "analyze": {
        "role": "primary-workflow",
        "triggers": ["analysis", "analyze", "regression", "survival", "Cox", "logistic", "NCDB", "SEER", "NSQIP", "cohort", "hazard ratio", "odds ratio"],
    },
    "data-analysis": {
        "role": "support-policy",
        "triggers": ["methods", "diagnostics", "registry cautions", "statistical policy", "assumptions"],
    },
    "clinical-analysis-policy": {
        "role": "support-policy",
        "triggers": ["methods", "diagnostics", "registry cautions", "statistical policy", "assumptions"],
    },
    "literature-review": {
        "role": "primary-workflow",
        "triggers": ["literature review", "PubMed", "evidence", "gap analysis", "citation", "references", "bibliography"],
    },
    "visualize": {
        "role": "primary-workflow",
        "triggers": ["figure", "visualize", "plot", "forest plot", "Kaplan-Meier", "ROC", "publication figure"],
    },
    "write-abstract": {
        "role": "primary-workflow",
        "triggers": ["abstract", "structured abstract", "AATS", "ITSOS", "JAMA", "revise abstract", "audit abstract"],
    },
    "write-discussion": {
        "role": "primary-workflow",
        "triggers": ["discussion", "conclusion", "limitations", "interpretation", "RPTH"],
    },
    "write-introduction": {
        "role": "primary-workflow",
        "triggers": ["introduction", "background", "gap statement", "study objective"],
    },
    "write-manuscript": {
        "role": "primary-workflow",
        "triggers": ["manuscript", "full draft", "assemble manuscript", "final audit", "submission"],
    },
    "write-methods-results": {
        "role": "primary-workflow",
        "triggers": ["methods", "results", "statistical methods", "results section", "Table 1"],
    },
    "biomedagent": {
        "role": "delegated-engine",
        "triggers": ["omics", "scRNA-seq", "RNA-seq", "genomics", "transcriptomics", "VCF", "BAM", "FASTQ", "h5ad", "machine learning", "differential expression", "pathway enrichment"],
    },
}

KEYWORD_HINTS = [
    "abstract",
    "analysis",
    "anndata",
    "bibliography",
    "citation",
    "clinical",
    "differential expression",
    "figure",
    "gene",
    "genomics",
    "geo",
    "h5ad",
    "literature",
    "machine learning",
    "manuscript",
    "omics",
    "PMID",
    "PubMed",
    "RNA-seq",
    "scRNA-seq",
    "single-cell",
    "survival",
    "VCF",
    "visualization",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    data: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []
    for line in block.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            if current_key is not None:
                data[current_key] = " ".join(current_value).strip().strip('"').strip("'")
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_value = [value.strip().strip(">")]
        elif current_key is not None:
            current_value.append(line.strip())
    if current_key is not None:
        data[current_key] = " ".join(current_value).strip().strip('"').strip("'")
    return data


def skill_text_from_package(path: Path) -> str | None:
    try:
        with zipfile.ZipFile(path) as zf:
            with zf.open("SKILL.md") as f:
                return f.read().decode("utf-8", errors="replace")
    except (KeyError, zipfile.BadZipFile, OSError):
        return None


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(values: list[str]) -> str:
    if not values:
        return "[]"
    return "[" + ", ".join(yaml_scalar(v) for v in values) + "]"


def write_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8", errors="replace") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def infer_external_triggers(name: str, description: str) -> list[str]:
    text = f"{name} {description}".lower()
    triggers = {name}
    for hint in KEYWORD_HINTS:
        if hint.lower() in text:
            triggers.add(hint)
    for token in re.split(r"[^A-Za-z0-9.+#-]+", name):
        if len(token) >= 3:
            triggers.add(token)
    return sorted(triggers, key=str.lower)


def load_skill_entry(skill_path: Path, source: str, package_path: Path | None = None) -> dict[str, object] | None:
    if package_path is not None:
        text = skill_text_from_package(package_path)
        if text is None:
            return None
        rel_path = package_path.relative_to(PLUGIN_ROOT).as_posix()
        source_type = "external-package"
    else:
        text = read_text(skill_path)
        rel_path = skill_path.relative_to(PLUGIN_ROOT).as_posix()
        source_type = source

    frontmatter = parse_frontmatter(text)
    name = frontmatter.get("name") or skill_path.parent.name
    description = frontmatter.get("description", "").strip()

    if source == "internal":
        override = INTERNAL_OVERRIDES.get(name, {})
        role = str(override.get("role", "primary-workflow"))
        triggers = list(override.get("triggers", infer_external_triggers(name, description)))
    else:
        role = "external-support"
        triggers = infer_external_triggers(name, description)

    return {
        "id": name,
        "name": name,
        "source": source,
        "source_type": source_type,
        "role": role,
        "path": rel_path,
        "description": description,
        "triggers": triggers,
    }


def discover_internal() -> list[dict[str, object]]:
    entries = []
    for skill_md in sorted(INTERNAL_DIR.glob("*/SKILL.md")):
        entry = load_skill_entry(skill_md, "internal")
        if entry:
            entries.append(entry)
    return entries


def discover_external() -> list[dict[str, object]]:
    entries_by_id: dict[str, dict[str, object]] = {}

    for skill_md in sorted(EXTERNAL_DIR.glob("*/SKILL.md")):
        entry = load_skill_entry(skill_md, "external")
        if entry:
            entries_by_id[str(entry["id"])] = entry

    for package in sorted(EXTERNAL_DIR.glob("*.skill")):
        # Prefer an extracted folder with the same stem when both exist.
        if (EXTERNAL_DIR / package.stem / "SKILL.md").exists():
            continue
        placeholder = EXTERNAL_DIR / package.stem / "SKILL.md"
        entry = load_skill_entry(placeholder, "external", package_path=package)
        if entry:
            entries_by_id[str(entry["id"])] = entry

    return [entries_by_id[k] for k in sorted(entries_by_id, key=str.lower)]


def write_registry(entries: list[dict[str, object]]) -> None:
    lines = [
        "# Generated by tools/update_skill_registry.py. Do not edit by hand.",
        "# Deterministic output: rerunning without skill changes should produce no diff.",
        "router: " + yaml_scalar("skills/clinical-research-assistant/SKILL.md"),
        "skills:",
    ]
    for entry in entries:
        lines.extend(
            [
                f"  - id: {yaml_scalar(str(entry['id']))}",
                f"    name: {yaml_scalar(str(entry['name']))}",
                f"    source: {yaml_scalar(str(entry['source']))}",
                f"    source_type: {yaml_scalar(str(entry['source_type']))}",
                f"    role: {yaml_scalar(str(entry['role']))}",
                f"    path: {yaml_scalar(str(entry['path']))}",
                f"    description: {yaml_scalar(str(entry['description']))}",
                f"    triggers: {yaml_list([str(v) for v in entry['triggers']])}",
            ]
        )
    changed = write_if_changed(REGISTRY_PATH, "\n".join(lines) + "\n")
    status = "updated" if changed else "unchanged"
    print(f"{status}: {REGISTRY_PATH.relative_to(PLUGIN_ROOT)}")


def write_external_index(entries: list[dict[str, object]]) -> None:
    external_entries = [e for e in entries if e["source"] == "external"]
    lines = [
        "# External Skill Index",
        "",
        "Generated by `tools/update_skill_registry.py`.",
        "",
        "Deterministic output: rerunning without skill changes should produce no diff.",
        "",
        "Paste external skills into `skills/external/` as either a folder containing `SKILL.md` or a `.skill` package, then rerun the updater.",
        "",
        "| Skill | Type | Path | Description |",
        "|---|---|---|---|",
    ]
    if not external_entries:
        lines.append("| _None registered_ |  |  |  |")
    for entry in external_entries:
        desc = str(entry["description"]).replace("|", "\\|")
        lines.append(f"| `{entry['id']}` | `{entry['source_type']}` | `{entry['path']}` | {desc} |")
    changed = write_if_changed(EXTERNAL_INDEX_PATH, "\n".join(lines) + "\n")
    status = "updated" if changed else "unchanged"
    print(f"{status}: {EXTERNAL_INDEX_PATH.relative_to(PLUGIN_ROOT)}")


def main() -> int:
    missing = [p for p in [SKILLS_DIR, INTERNAL_DIR, EXTERNAL_DIR, REFERENCES_DIR] if not p.exists()]
    if missing:
        for path in missing:
            print(f"Missing required directory: {path}", file=sys.stderr)
        return 1

    entries = discover_internal() + discover_external()
    entries = sorted(entries, key=lambda e: (str(e["source"]) != "internal", str(e["id"]).lower()))
    write_registry(entries)
    write_external_index(entries)
    print(f"indexed skills: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
