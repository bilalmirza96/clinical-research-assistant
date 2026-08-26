#!/usr/bin/env python3
"""
claim_audit.py - catch negative-existence claims that the registry contradicts (L073).

    python3 tools/claim_audit.py <deliverable> --registry <MASTER_ANALYSIS_REGISTRY.json>
    python3 tools/claim_audit.py draft.md --registry Reports/MASTER_ANALYSIS_REGISTRY.json --json

Exit code 0 = clean, 1 = hard failures.

WHY THIS EXISTS
---------------
L073. In the Esophageal-Organ-Preservation study an abstract draft carried the sentence
"the two histologies were not formally compared on this endpoint". That sentence was a
cautious hedge written by the agent, not a finding. It was then read back out of the draft
in a later turn and treated as evidence about the state of the analysis, and a real result
was nearly cut from the abstract on the strength of it.

The registry said otherwise, and had for two days:
    NCDB.sano_tte.histology_interaction_E1_diff_pp  7.23 pp (1.77 to 13.38), bootstrap p=0.013
    NCDB.histology_interaction.overall.HR_ratio     0.889 (0.839 to 0.943), LRT p=9.0e-05
    NCDB.clustered.interaction_arm_x_histology      p=7.1e-05, facility-cluster-robust
    FDR.interaction.arm_x_histology                 q=0.000185
    SEER.histology_interaction.allcause.lrt_chi2    p=0.0025  (independent replication)

registry_lint H8 checks that numbers PRESENT in a deliverable trace to the registry. It
cannot see a claim whose whole content is that a number is ABSENT. That is the gap this
fills: assertions of absence are claims about the registry and must be answered by it.

TWO RULES THIS ENFORCES
    R1  Never assert a negative about the analysis state from memory. "X was never tested",
        "there is no key for Y", "Z is unavailable" are claims ABOUT the registry.
    R2  Generated prose is never a source. Abstracts, reports, emails and summaries are
        downstream artifacts. Only registry keys and source JSONs are evidence.

R1 is mechanical and lives here. R2 is behavioural and lives in working-rules.md, but this
script is what makes an R2 violation visible: a hedge that survived into a deliverable and
is contradicted by the registry is exactly the artifact an R2 failure leaves behind.

CHECKS
  C1  an assertion that something was not tested / not compared, where the registry holds a
      plausibly matching interaction, comparison or test key            [HARD]
  C2  an assertion that data are unavailable / not recorded, where the registry holds a
      plausibly matching key                                            [HARD]
  C3  an assertion of a null or absent effect that carries no number, and for which the
      registry holds a matching effect key                              [SOFT]

LIMITS
  This is a lexical screen, not an adjudicator. It reports CANDIDATE keys whose names
  overlap the claim's subject; a human or agent still has to open them and decide. It is
  tuned to over-report rather than under-report, because the failure it exists to prevent
  is a confident claim of absence going unchecked. A flagged sentence that survives
  verification is fine - record why in the deliverable or the registry, and move on.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------------------
# Assertion patterns. Each is a claim whose content is that something does NOT exist.
# Edit these here, not in the skills - the skills point at this file.
# --------------------------------------------------------------------------------------

C1_UNTESTED = [
    r"\bnot\s+(?:be\s+)?formally\s+(?:compared|tested|assessed|evaluated)\b",
    r"\bwere\s+not\s+(?:directly\s+|formally\s+)?compared\b",
    r"\bwas\s+not\s+(?:directly\s+|formally\s+)?(?:compared|tested)\b",
    r"\bno\s+(?:formal\s+)?(?:test|comparison|interaction\s+test)\b",
    r"\b(?:never|not)\s+(?:been\s+)?tested\b",
    r"\bdid\s+not\s+(?:formally\s+)?(?:test|compare)\b",
    r"\bwe\s+did\s+not\s+(?:examine|assess|evaluate|test)\b",
    r"\bnot\s+(?:been\s+)?(?:examined|assessed|evaluated)\b",
    r"\bcannot\s+be\s+(?:compared|tested|assessed)\b",
    r"\bno\s+interaction\s+(?:was\s+)?(?:test|tested|performed|assessed)\b",
]

C2_UNAVAILABLE = [
    r"\b(?:is|are|was|were)\s+not\s+(?:available|recorded|captured|collected|ascertain\w*)\b",
    r"\bdoes\s+not\s+(?:record|capture|contain|include|report)\b",
    r"\bdo\s+not\s+(?:record|capture|contain|include|report)\b",
    r"\bno\s+(?:data|information|measure|record)s?\s+(?:on|for|about|regarding)\b",
    r"\b(?:unavailable|unrecorded|uncaptured)\b",
    r"\black(?:s|ed|ing)?\s+(?:data|information)\b",
    r"\bnot\s+(?:be\s+)?ascertain(?:ed|able)\b",
]

C3_NULL = [
    r"\bno\s+(?:significant|detectable|measurable|apparent)\s+\w+\b",
    r"\b(?:did|does)\s+not\s+differ\b",
    r"\bno\s+(?:evidence|indication)\s+of\b",
    r"\bshowed\s+no\s+\w+\b",
]

# Sentence-side term -> registry-side tokens it should make us look for.
SYNONYMS = {
    "compare": {"interaction", "did", "diff", "difference", "ratio", "contrast"},
    "compared": {"interaction", "did", "diff", "difference", "ratio", "contrast"},
    "comparison": {"interaction", "did", "diff", "difference", "ratio"},
    "test": {"interaction", "lrt", "chi2", "p", "bootstrap", "permutation"},
    "tested": {"interaction", "lrt", "chi2", "p", "bootstrap", "permutation"},
    "interaction": {"interaction", "lrt", "chi2", "did", "ratio", "modification"},
    "modifier": {"interaction", "modification", "hte", "subgroup"},
    "histology": {"histology", "adeno", "adenocarcinoma", "scc", "squamous"},
    "histologies": {"histology", "adeno", "adenocarcinoma", "scc", "squamous"},
    "histologic": {"histology", "adeno", "adenocarcinoma", "scc", "squamous"},
    "squamous": {"scc", "squamous"},
    "adenocarcinoma": {"adeno", "adenocarcinoma"},
    "subgroup": {"subgroup", "stratum", "strata", "hte"},
    "survival": {"survival", "os", "rmst", "km", "hr"},
    "mortality": {"mortality", "death", "os", "cancerspecific"},
    "response": {"response", "ccr", "pcr", "cr"},
    "era": {"era", "year", "period", "temporal"},
    "facility": {"facility", "cluster", "clustered", "hospital", "volume"},
    "missing": {"missing", "missingness", "imputation", "selwt", "ipcw"},
    "sensitivity": {"sensitivity", "sens", "s1", "s2", "s3", "s4", "s5", "s6"},
    "nodal": {"nodal", "cn", "node", "npos"},
    "endpoint": {"endpoint", "os", "rmst", "survival", "pp"},
}

STOPWORDS = {
    "the", "two", "this", "that", "these", "those", "was", "were", "not", "and", "but",
    "for", "with", "from", "into", "onto", "our", "their", "its", "his", "her", "them",
    "have", "has", "had", "been", "being", "are", "is", "be", "on", "in", "of", "at",
    "to", "by", "we", "us", "it", "a", "an", "as", "or", "no", "any", "all", "both",
    "formally", "directly", "never", "did", "does", "do", "cannot", "can", "could",
    "would", "should", "may", "might", "must", "so", "than", "then", "there", "here",
    "which", "who", "whom", "whose", "what", "when", "where", "why", "how", "study",
    "analysis", "data", "patients", "patient", "cohort", "however", "although", "though",
    "because", "since", "while", "also", "only", "one", "other", "same", "such", "own",
}

# Words that carry the ASSERTION itself rather than its subject. They may expand through
# SYNONYMS, but they can never be the literal token that proves a key is on-topic - otherwise
# any sentence containing "compared" matches every key containing "interaction".
ASSERTION_WORDS = {
    "compare", "compared", "comparison", "test", "tested", "testing", "assess", "assessed",
    "evaluate", "evaluated", "examine", "examined", "record", "recorded", "records",
    "available", "capture", "captured", "collect", "collected", "ascertain", "ascertained",
    "ascertainable", "show", "showed", "shown", "significant", "evidence", "indication",
    "differ", "differed", "detectable", "measurable", "apparent", "database", "registry",
    "performed", "reported", "conducted", "undertaken",
}

BODY_END_SENTINEL = "[END OF ABSTRACT BODY]"

# Match quality thresholds. A candidate must clear MIN_HITS distinct substantive tokens.
MIN_HITS = 2
MIN_STEM = 5
MAX_CANDIDATES = 4


# --------------------------------------------------------------------------------------
# IO
# --------------------------------------------------------------------------------------

def read_text(path: Path, stop_at: str | None) -> str:
    if path.suffix.lower() == ".docx":
        try:
            import docx  # type: ignore
        except ImportError:
            sys.exit("python-docx is required to read .docx files: pip install python-docx")
        text = "\n".join(p.text for p in docx.Document(str(path)).paragraphs)
    else:
        text = path.read_text(encoding="utf-8")
    if stop_at and stop_at in text:
        text = text.split(stop_at, 1)[0]
    return text


def load_registry(path: Path) -> dict:
    """Return {key: label_text}. Tolerates the three registry shapes in use."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    for container in ("results", "entries"):
        if isinstance(raw.get(container), dict):
            block = raw[container]
            break
    else:
        block = raw
    out = {}
    for k, v in block.items():
        if not isinstance(k, str) or k.startswith("_"):
            continue
        bits = []
        if isinstance(v, dict):
            cur = v.get("current", v)
            for field in ("label", "note", "annotation", "n", "verdict"):
                for src in (v, cur if isinstance(cur, dict) else {}):
                    val = src.get(field)
                    if isinstance(val, str):
                        bits.append(val)
        out[k] = " ".join(bits)
    return out


# --------------------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------------------

def tokenise(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2}


def key_tokens(key: str) -> set[str]:
    return tokenise(key.replace(".", " ").replace("_", " "))


def key_bag(key: str, label: str) -> set[str]:
    return key_tokens(key) | tokenise(label)


def sentence_terms(sentence: str) -> tuple[set[str], set[str]]:
    """Return (literal_subject_tokens, expanded_tokens).

    literal tokens are what the sentence is ABOUT and must appear in a key for it to be a
    candidate. expanded tokens add synonyms and are used only to rank.
    """
    raw = tokenise(sentence)
    literal = {t for t in raw if t not in STOPWORDS and t not in ASSERTION_WORDS}
    expanded = {t for t in raw if t not in STOPWORDS}
    for t in raw:
        expanded |= SYNONYMS.get(t, set())
        expanded |= SYNONYMS.get(t.rstrip("s"), set())
    return literal, expanded


def literal_hits(literal: set[str], bag: set[str]) -> set[str]:
    """Exact match, or a shared prefix of at least MIN_STEM chars (histologies/histology)."""
    out = set()
    for term in literal:
        for tok in bag:
            if term == tok or (
                len(term) >= MIN_STEM and len(tok) >= MIN_STEM
                and (term.startswith(tok[:MIN_STEM]) or tok.startswith(term[:MIN_STEM]))
            ):
                out.add(term)
                break
    return out


def split_sentences(text: str) -> list[tuple[int, str]]:
    """Return (line_no, sentence). Line numbers are 1-indexed and approximate."""
    out = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        for sent in re.split(r"(?<=[.;:])\s+", stripped):
            if sent.strip():
                out.append((lineno, sent.strip()))
    return out


def find_candidates(sentence: str, registry: dict[str, str]) -> list[tuple[int, str]]:
    literal, expanded = sentence_terms(sentence)
    if not literal:
        return []
    scored = []
    for key, label in registry.items():
        bag = key_bag(key, label)
        # The claim's subject must appear in the KEY itself, not merely in label prose.
        # L071/S2 already requires keys to name their population and specification, so a key
        # that is genuinely about this subject will say so in its name. Matching label text
        # alone produces lexical coincidences ("operating room" hitting an "operative" label).
        lit = literal_hits(literal, key_tokens(key))
        if not lit:
            continue
        score = len((expanded & bag) | lit)
        if score >= MIN_HITS:
            scored.append((score, key))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[:MAX_CANDIDATES]


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------

CHECKS = [
    ("C1", "asserts something was not tested or compared", C1_UNTESTED, True),
    ("C2", "asserts data are unavailable or not recorded", C2_UNAVAILABLE, True),
    ("C3", "asserts a null or absent effect without a number", C3_NULL, False),
]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Audit a deliverable for negative-existence claims the registry contradicts.")
    ap.add_argument("path", type=Path)
    ap.add_argument("--registry", type=Path, required=True)
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--stop-at", default=BODY_END_SENTINEL,
                    help="ignore everything after this sentinel line")
    args = ap.parse_args()

    if not args.path.exists():
        sys.exit(f"no such file: {args.path}")
    if not args.registry.exists():
        sys.exit(f"no such registry: {args.registry}")

    text = read_text(args.path, args.stop_at)
    registry = load_registry(args.registry)

    hard, soft = [], []
    for lineno, sent in split_sentences(text):
        for code, why, patterns, is_hard in CHECKS:
            if not any(re.search(p, sent, re.I) for p in patterns):
                continue
            cands = find_candidates(sent, registry)
            if not cands:
                continue
            finding = {
                "check": code,
                "line": lineno,
                "why": why,
                "sentence": sent,
                "contradicting_keys": [k for _, k in cands],
            }
            (hard if is_hard else soft).append(finding)
            break

    if args.json:
        print(json.dumps({"hard": hard, "soft": soft,
                          "registry_keys": len(registry)}, indent=1))
        return 1 if hard else 0

    print(f"claim_audit: {args.path.name}  ({len(registry)} registry keys)")
    if not hard and not soft:
        print("  clean - no unverified negative-existence claims found.")
        return 0
    for bucket, title in ((hard, "HARD FAILURES"), (soft, "SOFT FINDINGS")):
        if not bucket:
            continue
        print(f"\n{title}")
        for f in bucket:
            print(f"  [{f['check']}] line {f['line']}: {f['why']}")
            print(f"      \"{f['sentence']}\"")
            print("      candidate contradicting keys - verify each:")
            for k in f["contradicting_keys"]:
                print(f"        - {k}")
    if hard:
        print("\nEach HARD failure is a claim of absence that the registry appears to "
              "contradict.\nVerify against the named keys before this deliverable ships.")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
