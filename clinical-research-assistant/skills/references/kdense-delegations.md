# K-Dense Delegation Map — Citation, Peer Review, Scholar Eval, Zotero, Systematic Review

Single source of truth for how CRA internal skills delegate to vendored K-Dense
skills for citation integrity, formal peer-review-style auditing, quantitative
quality scoring, Zotero library sync, and formal systematic-review workflows.

Read this file when any of the following are about to happen:

- A reference is being added to `citation_bank.json` or inserted into manuscript prose
- `/literature-review` is running a systematic search
- `/manuscript-qc` is running its checklist
- `/write-manuscript` Phase 8 is auditing citation integrity
- A user mentions Zotero, BibTeX export, or library sync

The K-Dense skills referenced here are vendored under
`skills/external/scientific-agent-skills/scientific-skills/`. They are loaded
as **expert reference** at runtime (the same pattern `/analyze` uses with
`scientific-visualization`) — read their `SKILL.md` before invoking their tools.

---

## 1. Citation integrity — `scientific-skills:citation-management`

**When:** every time a citation is added to `citation_bank.json`, inserted into
manuscript prose, or audited in `/manuscript-qc`.

**Role in CRA:** primary citation-verification engine. Closes L041
(Citation Integrity Audit).

**Skill path:** `skills/external/scientific-agent-skills/scientific-skills/citation-management/SKILL.md`

**Capabilities used:**

- Google Scholar + PubMed metadata lookup
- DOI → BibTeX conversion
- Verify (author, year, journal, volume, pages, DOI, PMID) tuple consistency
- Generate properly formatted BibTeX entries

### Hard gate — non-negotiable per L041

Every citation added during a CRA session must pass this gate before it can
enter `citation_bank.json` with `.verified = true` or appear in any drafted
prose:

```
For each candidate citation (author, year, title, journal, doi or pmid):
  1. Load citation-management SKILL.md as expert reference
  2. Run the skill's verify_citation tool against PubMed (preferred) or Crossref
  3. Compare returned metadata to the candidate fields
  4. PASS if (title fuzzy-match ≥ 0.9) AND (year matches) AND (doi or pmid resolves):
       → write entry with .verified = true
       → store doi + pmid + canonical title in citation_bank
  5. AMBIGUOUS if title matches but multiple papers returned:
       → halt, present candidates to user, require disambiguation
  6. FAIL if not found OR metadata mismatch:
       → DO NOT write to citation_bank
       → DO NOT use the citation in prose
       → log to decision_log.md with reason
       → halt and tell the user explicitly
```

No silent fallback. No "PMID: pending verification" placeholders. No citing
from memory. If the user wants to override (e.g., a brand-new preprint without
a stable PMID yet), require a written exception in `decision_log.md` and tag
the citation entry with `.verified = false, .exception_reason = "..."`.

### Where this gate is enforced

- `/literature-review` STEP 2 + STEP 5 citation verification passes
- `/write-introduction` every reference before paragraph approval
- `/write-discussion` every concordant/discordant comparison reference
- `/write-methods-results` any newly added references (rare)
- `/write-manuscript` Phase 8 Part B.5 (final pre-submission audit)
- `/manuscript-qc` Check on References (run as audit, not as gate)

---

## 2. Formal peer-review-style audit — `scientific-skills:peer-review`

**When:** `/manuscript-qc` final pass; optional `/write-manuscript` Phase 8 pre-delivery.

**Role in CRA:** structured checklist-based peer-review simulation. Catches
issues a journal reviewer would catch before submission.

**Skill path:** `skills/external/scientific-agent-skills/scientific-skills/peer-review/SKILL.md`

**Capabilities used:**

- Methodology assessment (study design appropriateness, sample size, statistical validity)
- Reporting-standards compliance (CONSORT, STROBE, PRISMA, TRIPOD, STARD, SPIRIT, SQUIRE)
- Constructive feedback structure (Major Comments / Minor Comments / Editor Comments)

### Pattern

```
At manuscript-qc final review OR write-manuscript Phase 8:
  1. Load peer-review SKILL.md as expert reference
  2. Provide manuscript + study design + target journal
  3. Run the skill's structured review pass
  4. Capture output as Reports/peer_review_simulation_<date>.md
  5. Surface MAJOR comments to the user before delivery
```

The CRA-native `manuscript-qc/references/checks.md` 12-check list stays as the
primary audit. peer-review is layered on top as a Check 13: "Reviewer-perspective
simulation." Its output complements the deterministic checks with reviewer-style
narrative feedback.

---

## 3. Quantitative quality scoring — `scientific-skills:scholar-evaluation`

**When:** `/manuscript-qc` (post-checklist scoring); `/literature-review` (per-evidence quality scoring).

**Role in CRA:** numeric ScholarEval scores across research-quality dimensions —
problem formulation, methodology, analysis, writing. Use to triage which papers
in the evidence bank are highest-quality, and to put a number on the manuscript's
own quality before submission.

**Skill path:** `skills/external/scientific-agent-skills/scientific-skills/scholar-evaluation/SKILL.md`

**Capabilities used:**

- ScholarEval rubric (4 dimensions, each scored 1–5 with justification)
- Cross-dimension weighted total
- Identifies the weakest dimension to prioritize for revision

### Two CRA touch points

**In `/literature-review`:** as part of the STEP 5 deep-dive, score the top
15–25 verified papers using ScholarEval. Store the scores in
`evidence_bank.json` per-entry as `.scholar_eval = {problem, method, analysis, writing, total, weakest_dimension}`.
The Discussion-discordant tag should be biased toward papers with `total ≥ 16`
(out of 20) — comparison to weak prior work is itself a weakness.

**In `/manuscript-qc`:** as a final check before "ready to submit?" verdict.
Run ScholarEval against the manuscript's own draft. If `total < 14`, halt and
surface the weakest dimension — that is what to revise before submission.

```
For literature-review STEP 5:
  1. Load scholar-evaluation SKILL.md as expert reference
  2. For each verified evidence entry:
       a. Pass the paper (or its abstract + design) through the rubric
       b. Capture 4 dimension scores + justification
       c. Write to evidence_bank.json[.scholar_eval]
  3. Sort the evidence table by total score descending

For manuscript-qc:
  1. Load scholar-evaluation SKILL.md as expert reference
  2. Pass the full assembled manuscript through the rubric
  3. Write Reports/scholar_evaluation_<date>.md
  4. If total < 14, set verdict = NOT READY and surface weakest dimension
```

---

## 4. Zotero library sync — `scientific-skills:pyzotero`

**When:** end of `/literature-review`; optional start of `/write-manuscript`.

**Role in CRA:** sync the verified `citation_bank.json` to a Zotero library.
Optional but **auto-enables** when a Zotero config is detected.

**Skill path:** `skills/external/scientific-agent-skills/scientific-skills/pyzotero/SKILL.md`

**Capabilities used:**

- Zotero Web API v3 read/write
- Create items, attach PDFs, tag by collection
- Export from existing Zotero collection into the CRA citation bank

### Detection rule — auto-on

At the end of `/literature-review` and at the start of `/write-manuscript`:

```
zotero_api_key   = os.environ.get("ZOTERO_API_KEY")
zotero_user_id   = os.environ.get("ZOTERO_USER_ID")
zotero_group_id  = os.environ.get("ZOTERO_GROUP_ID")

if zotero_api_key AND (zotero_user_id OR zotero_group_id):
    # Zotero config detected — sync automatically
    1. Load pyzotero SKILL.md as expert reference
    2. For each entry in citation_bank.json:
         - if .verified = true AND no .zotero_key:
             - create Zotero item via pyzotero
             - store returned .zotero_key in citation_bank entry
             - tag with project name + "CRA" tag
    3. Log sync result to decision_log.md
else:
    # No config — skip silently
    # User can opt in later by exporting ZOTERO_API_KEY + ZOTERO_USER_ID
```

Failure mode: if sync fails (network, auth, rate limit), do NOT halt the workflow.
Log the failure, leave citation_bank unchanged, and proceed. Zotero is convenience,
not a gate.

### Reverse sync (Zotero → CRA)

If the user starts a manuscript with an existing Zotero collection, allow the
reverse: `/write-manuscript` Phase 1 can pull a Zotero collection into
`citation_bank.json`. Each pulled item still has to pass the citation-management
hard gate before `.verified = true`.

---

## 4b. Phase 0 Pre-Design Literature Recon — `/analyze` HARD GATE (per L048)

**When:** automatically, every time `/analyze` is invoked. Phase 1 INTAKE cannot fire without Phase 0 sign-off. Implemented as auto-invocation of `/literature-review` Mode 0 (see `internal/literature-review/SKILL.md` §State-Management).

**Role in CRA:** prevents the "I-analyzed-it-but-someone-already-published-this" failure mode. Per L048 (added 2026-05-24 after Esophageal-Organ-Preservation v2 vs Sakowitz 2025 JTCVS discovery), running Phase 1+ without lit recon is the canonical bug.

### Phase 0 K-Dense delegation chain

| Step | K-Dense skill | Why this skill |
|---|---|---|
| Initial ideation (broad question) | `scientific-skills:scientific-brainstorming` | Cast wider net before narrowing — surface adjacent literatures the user may not have considered |
| Multi-database systematic sweep | `scientific-skills:literature-review` | PRISMA-quality search across PubMed + bioRxiv + OpenAlex + Semantic Scholar |
| Direct DB query (targeted) | `scientific-skills:pubmed-database`, `scientific-skills:openalex-database` | When a specific landmark trial / author / dataset needs to be confirmed |
| Quality scoring of nearest comparators | `scientific-skills:scholar-evaluation` | Rank top 5–10 prior papers by ScholarEval rubric — drives the "nearest_comparators" entries with `.scholar_eval_score` |
| Critical assessment of prior evidence | `scientific-skills:scientific-critical-thinking` | Identify limitations / biases / generalizability gaps in prior work that justify our study |
| Research-question refinement (if pivot needed) | `scientific-skills:hypothesis-generation` | Sharpen the question if Phase 0 reveals it should be modified |
| Citation verification | `scientific-skills:citation-management` | L041 hard gate — every entry in citation_bank verified before lock |

### Required outputs at Phase 0 close

| Artifact | Purpose | Schema |
|---|---|---|
| `evidence_bank.json` | Broad prior-work inventory | `templates/state/evidence_bank.template.json` (existing) |
| `citation_bank.json` | L041-verified citations only | `templates/state/citation_bank.template.json` (existing) |
| `novelty_assessment.json` | Structured differentiation analysis | `templates/state/novelty_assessment.template.json` (added 2026-05-24) |
| `differentiation_brief.md` | PI-facing narrative for HALT 0 sign-off | `templates/state/differentiation_brief.template.md` (added 2026-05-24) |

### HALT 0 — non-skippable

After Phase 0 produces the four artifacts, `/analyze` presents differentiation_brief.md to the PI and requires one of:

- `(a) Novel` — proceed to Phase 1
- `(b) Replication with extension` — proceed; differentiation_brief becomes Discussion scaffolding
- `(c) Pivot scope` — research question modified, re-hash, re-enter Phase 0
- `(d) Abandon` — archive project, stop

PI signature is required; rationale text is required. SHA256 of the signed differentiation_brief is locked into `novelty_assessment.lock_hash`. Valid for 30 days; auto-re-fires if research_question changes.

### Failure mode this gate prevents

The Esophageal-Organ-Preservation project (Bilal Mirza, May 2026) ran a full Standing-Rule-A analysis with 5 rungs of methodological rigor on N=53,389 NCDB patients comparing trimodality vs definitive CRT — only to discover at write-up planning that **Sakowitz et al. 2025 (J Thorac Cardiovasc Surg)** had published a 3,786-patient NCDB SCC analysis with essentially identical headline finding (HR 1.75) earlier the same year. The analysis is not wasted (HTE quantification + adenocarcinoma inclusion + methodological extensions are genuinely novel) but the framing now requires "replication with extension" repositioning that should have been the design choice from day one. Phase 0 prevents this in all future CRA projects.

---

## 5. Formal systematic-review workflow — K-Dense `literature-review`

**When:** `/literature-review` when the user wants a PRISMA-quality systematic review
or meta-analysis, not just an evidence landscape.

**Role in CRA:** primary execution backbone for systematic searches.
CRA `/literature-review` stays as the **orchestrator** (PRISMA framing, gap
analysis, evidence bank schema, novelty assessment, journal-fit). K-Dense's
literature-review handles the **execution** (multi-database parallel search,
deduplication, PRISMA flow tracking, formatted output).

**Skill path:** `skills/external/scientific-agent-skills/scientific-skills/literature-review/SKILL.md`

**Capabilities used:**

- Multi-database search (PubMed, arXiv, bioRxiv, Semantic Scholar, openalex)
- PRISMA flow tracking (identified / screened / eligible / included)
- Multi-format output (APA, Nature, Vancouver, Markdown, PDF)
- Built-in deduplication

### Orchestration pattern

```
CRA /literature-review owns:
  - STEP 1 (research scope)
  - STEP 3 (gap analysis + novelty)
  - STEP 4 (research question recommendations)
  - STEP 5 (deep dive synthesis)
  - evidence_bank.json + citation_bank.json schemas
  - decision_log.md writes

K-Dense literature-review executes:
  - STEP 2 multi-database search + initial 20–40 paper sweep
  - STEP 5 deep-dive 20–30 paper expanded search
  - PRISMA flow if formal systematic review requested

Bridge:
  - CRA passes structured search criteria → K-Dense
  - K-Dense returns ranked, deduplicated paper list with DOIs
  - CRA writes them into evidence_bank.json
  - CRA runs each through citation-management gate before promoting to citation_bank
```

This is the same orchestrator-contract pattern `/analyze` uses with
`scientific-visualization`. CRA stays in control of state files, schemas, and
decision points; K-Dense does the heavy lift.

---

## Combined invocation order at runtime

When `/literature-review` runs:

```
1. Load this file (kdense-delegations.md) at PREREQUISITE
2. STEP 1: scope (CRA-native)
3. STEP 2: search → delegate to K-Dense literature-review
4. STEP 2 verification pass: every paper → citation-management gate
5. STEP 3: gap analysis (CRA-native)
6. STEP 4: research question recommendations (CRA-native)
7. STEP 5: deep dive → delegate to K-Dense literature-review again
8. STEP 5 verification: citation-management gate
9. STEP 5 scoring: scholar-evaluation per verified entry
10. End of session: pyzotero sync if env detected
```

When `/write-*` skills run:

```
1. Load this file at PREREQUISITE (read once per session)
2. Drafting proceeds normally
3. For every new citation that is not already in citation_bank with .verified=true:
     → citation-management hard gate (halt on FAIL)
4. End of session: pyzotero sync if env detected
```

When `/manuscript-qc` runs:

```
1. Load this file at PREREQUISITE
2. Run the 12 native CRA checks per references/checks.md
3. Check 13: peer-review structured pass (delegated to K-Dense peer-review)
4. Check 14: ScholarEval quantitative scoring (delegated to K-Dense scholar-evaluation)
5. Check 15: citation-management batch audit of every reference (re-verify all DOIs/PMIDs)
6. Verdict: NOT READY if any CRITICAL native check fails, OR Check 14 total < 14
```

---

## File-write contract — what gets logged

| Event | Logged where |
|---|---|
| Citation passes gate | `citation_bank.json[entry].verified = true` + sha256 of metadata |
| Citation fails gate | `decision_log.md` append + `citation_bank.json` NOT updated |
| ScholarEval scores added | `evidence_bank.json[entry].scholar_eval` OR `Reports/scholar_evaluation_<date>.md` |
| Peer-review simulation | `Reports/peer_review_simulation_<date>.md` |
| Zotero sync result | `citation_bank.json[entry].zotero_key` + `decision_log.md` append |
| K-Dense literature-review search | `evidence_bank.json[entry]` per paper + `.search_queries` log |

All writes follow the same conventions used elsewhere in CRA (ISO 8601 timestamps,
sequential IDs, `json.dump indent=2`, never overwrite fields you are not updating).

---

## Versioning

If any K-Dense skill updates change its interface, update this file's section for
the affected skill. Track changes in the file header `last_updated` if needed.
The vendored copy under `skills/external/` is the canonical reference — refresh
it by re-running `tools/update_skill_registry.py` after pulling upstream.
