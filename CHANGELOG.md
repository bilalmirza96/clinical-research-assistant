# Changelog

All notable changes to the clinical-research-assistant plugin will be documented in this file.

## [3.9.3] - 2026-07-02

### Fixed — delegation namespace resolution + deploy-version discipline (L058)

- **Namespace resolver.** Added a "Namespace resolution" section to `skills/internal/analyze/references/delegation-matrix.md` documenting that every `scientific-skills:<name>` reference is a delegation *label* that resolves to the **natively-installed** `claude-scientific-skills` skill `<name>` (bare invokable name; 173-skill superset), with the vendored `skills/external/scientific-agent-skills/` copy as an offline/Codex fallback only. One authoritative table resolves all ~141 `scientific-skills:` occurrences across 18 files without touching each one. Fixes the latent fragility that the prefixed label was never `Skill()`-invokable as written.
- **Version-bump discipline.** Bumped `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (both `metadata.version` and the plugin-entry version) 3.9.2 → 3.9.3. Content had been shipping under a frozen 3.9.2 label, so the version-keyed install cache never pulled it. Policy going forward: bump the patch version on every content change, however small.
- **Drift-check hook.** Wired `tools/cra-cache-drift-check.sh` into a non-blocking `SessionStart` hook (`~/.claude/settings.json`) so cache-vs-repo drift is surfaced automatically each session (extends L056).

### Added — `/analyze --quick` exploratory tier (L058)

- New lightweight `/analyze --quick` path for exploratory analyses: keeps the seeded run and inline `verifying-results-before-claiming` verification, but drops the halt ladder, Master Excel scaffolding, pre-registration, red-team, SCAR registration, and the 16-section report. **Abstract-exclusion is structural, not advisory:** quick results are written only to a separate `Reports/exploratory_quick_log.md`/`.json` and **never** to `MASTER_ANALYSIS_REGISTRY.json`/SCAR — since L045 makes SCAR the sole source for every manuscript/abstract number, a quick result is thereby structurally ineligible for a manuscript (artifact firewall, not a banner). Labeled `EXPLORATORY-UNGATED` (an orthogonal provenance class, explicitly **not** an L035 Tier 1–4, which are a post-audit multiple-testing partition undefined for a single-contrast run). Single-contrast only; adjustment requests refuse and redirect to full `/analyze`. Purpose: remove the incentive to hand-run analyses outside the plugin (the manual-execution reliability gap surfaced in the 2026-07-02 audit). *(Design corrected after an adversarial review caught that an earlier draft wrote quick results into SCAR with a `mode`/tier tag the registry script cannot store — a laundering path; the firewall replaces it.)*

### Staged — de-vendoring migration (NOT executed)

- Added `tools/cra-devendor.sh` (dry-run by default): would drop the 128 vendored scientific-skills that have a native namesake and retain the 10 CRA-local ones that do not (`autoskill, bids, database-lookup, exa-search, hugging-science, optimize-for-gpu, paper-lookup, paperzilla, polars-bio, primekg`). Not run — the script **refuses `--apply`** until two coupled prerequisites are cleared: (1) rewire the vendored-path references in `skills/references/kdense-delegations.md` to native, and (2) update `tools/cra-sanity-check.sh` (which hardcodes `EXPECTED_KDENSE_COUNT=138` and `check_file`s five vendored delegation-target paths — the count would warn and the five path checks would hard-fail post-devendor). Set the count to the retained total and repoint those checks to native before execution.

## [3.9.2] - 2026-05-30

### Fixed — Codex skill loader compatibility

- Shortened the frontmatter descriptions for vendored `biomedagent` and `hugging-science` skills so they stay under Codex's 1024-character skill-description limit.
- Regenerated `skills/references/skill-registry.yaml` and `skills/references/external-skills.md` so CRA routing metadata matches the fixed skill frontmatter.

## [3.9.1] - 2026-05-30

### Added — Codex packaging layer + version alignment

- New `clinical-research-assistant/.codex-plugin/plugin.json` (mirrors the K-Dense science-superpowers Codex manifest schema; `skills: "./skills/"`) so CRA installs as a Codex plugin alongside the existing Claude (`.claude-plugin`) packaging.
- Aligned version fields: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` bumped 3.4.0 -> 3.9.1 to match the CHANGELOG (they had drifted behind through v3.5-v3.9).

## [3.9.0] - 2026-05-30

### Added — claude-scientific-writer skills wired as delegated references (no duplicate vendoring)

- Evaluated `K-Dense-AI/claude-scientific-writer`; found it a curated subset of the already-vendored `scientific-agent-skills`. Chose NOT to vendor it (would duplicate ~20 skills) — wired the useful pieces by reference instead.
- New `DELEGATION_RULES.md` §F maps `scientific-skills:*` execution helpers to CRA `write-*`/`visualize`: `research-lookup`, `scientific-schematics`, `venue-templates`, `scientific-slides`, `latex-posters`/`pptx-posters`, `research-grants`, `paper-2-web`, `markitdown`. `citation-management` / `peer-review` / `scholar-evaluation` already wired (§D).
- Pointer blocks appended to `write-introduction`, `write-methods-results`, `write-discussion`, `write-abstract`, `write-manuscript`, `visualize`. CRA `write-*` + house standards remain authoritative over any generic writing skill. Lessons-log L054; working-rules updated.

## [3.8.0] - 2026-05-30

### Changed — checkpoint phase-flow + science-superpowers audits replace the 9-agent panels (Stages 2-4)

#### Stage 2 — checkpoint phase flow
- `/analyze` Phase 4 PRIMARY now ends with **Checkpoint A** (inline verify). Phase 5 split into **5A SECONDARY (adjusted)** + **Checkpoint B** + new **5B SENSITIVITY & SUBGROUPS**. Sensitivity no longer runs inside the secondary phase — it is gated on Checkpoint B passing. New **HALT 2B** between adjusted results and sensitivity.

#### Stage 3 — audits via science-superpowers (token reduction)
- Phase 3's 4-agent plan critique now runs **INLINE** (escalates to one reviewer only on a CRITICAL plan flaw) and locks the pre-registration via `science-superpowers:preregistering-analysis`.
- Phase 6's 5-agent audit panel is replaced by **ONE** `science-superpowers:requesting-red-team-review` subagent briefed with new `analyze/references/red-team-brief.md`. Numerical / reproducibility / completeness are done **inline** at Checkpoints A/B via `science-superpowers:verifying-results-before-claiming`. ~32K tokens of panels -> ~3-5K.

#### Stage 4 — three-layer delegation codified
- New `analyze/references/sp-integration.md` (SP-skill -> phase map + bootstrap precedence). `DELEGATION_RULES.md` §E + `00_Context/working-rules.md` ratify the three layers — **science-superpowers (rigor) + CRA (orchestration/brain) + K-Dense scientific-skills & BioMedAgent (validated execution)** — with maximal delegation to the validated layers and a bootstrap-precedence rule so the competing session-starts don't fight.
- `references/audit-agents.md` and `references/critique-panel.md` superseded/repurposed (retained for reference). Lessons-log L053.

## [3.7.0] - 2026-05-30

### Changed — `data-analysis` merged into `/analyze`; lazy reference loading (token reduction)

Refactor (Bilal Mirza, Cowork session) consolidating the analysis layer and ratifying the three-layer delegation architecture.

#### Stage 1 (this entry) — skill merge

- The standalone `data-analysis` (clinical-analysis-policy) skill is merged into `/analyze`. Its policy body now lives at `skills/internal/analyze/references/clinical-analysis-policy.md`; its four reference files (`method-selection-guide`, `diagnostics-checklist`, `registry-cautions`, `variable-collapse-defaults`) + `settings-template` moved under `analyze/references/`.
- `/analyze` PREREQUISITE switched from bulk-reading all 6 prerequisite files every run to **lazy on-demand loading** (read `lessons-log.json` up front; read each policy reference only at the phase that needs it). Token reduction.
- Consumers repointed: `write-methods-results`, `project-init`, router `clinical-research-assistant/SKILL.md`, `skill-registry.yaml`, `OWNERSHIP_MAP.md`, `AGENTS.md`, `README.md`, `skills/internal/README.md`.
- `skills/internal/data-analysis/SKILL.md` left as a **deprecation stub**; original `data-analysis/references/` retained as backup pending Bilal's confirmation to delete the folder. Nothing deleted.

#### Architecture ratified (Stages 2-4 pending)

- **Three layers:** science-superpowers (rigor — pre-registration, verify, red-team) + CRA (clinical orchestration / brain) + K-Dense scientific-skills & BioMedAgent (validated execution). Maximal delegation to the specialized/validated layers; CRA stays the orchestrator.
- **Pending:** Stage 2 phase-flow checkpoints (sanity at end of PRIMARY and SECONDARY, sensitivity split out); Stage 3+4 replace the 9-agent critique+audit panels with inline `verifying-results-before-claiming` at checkpoints + one clinically-augmented `requesting-red-team-review`, codify delegation in `DELEGATION_RULES.md`, add bootstrap-precedence rule.

## [3.6.0] - 2026-05-24

### Added — Registry-specific inclusion/exclusion checklist HARD GATE at Phase 1.1 (per L050)

This release closes the **silent-default-filter** failure mode. The trigger was the **Esophageal Organ-Preservation HTE SEER replication** (Bilal Mirza, 2026-05-24) — NCDB Phase 1 silently defaulted "all primaries" while SEER Phase 1 silently defaulted "first primary only," producing a 16,000-patient methodological gap between cohorts that the PI caught only post-hoc. Neither default was an explicit PI decision; both were assistant choices the PI could not audit because no checklist forced explicit review.

#### Phase 1.1 hard gate

- **`skills/internal/analyze/SKILL.md`** — new §1.1.a inserted before `dataset_spec.json` is written. Requires the assistant to load the registry-appropriate checklist, present a structured table (filter | common defaults | proposed value + rationale | PI checkbox) for every conventional filter, and obtain explicit PI attestation that no filter is silently defaulted. Cross-registry studies require a side-by-side comparison with §HALT/AMBIGUITY notation for every divergence.
- **`skills/references/registry-cohort-checklists.md`** — new 6-registry reference file (NCDB 26 items, SEER 26, NSQIP 10, UNOS 10, TriNetX 7, generic 5) + cross-registry consistency rule. Each item lists common literature defaults and prompts the assistant to surface a specific recommendation with rationale.
- **L050 added** to `lessons-log.json` — full worked-example failure-mode narrative. Last 3 lessons (L048/L049/L050) all originated in the Esophageal Organ-Preservation HTE project; this represents the most concentrated CRA hardening sprint to date.

#### What this prevents

Silent-default-filter failures across registries: future projects cannot have NCDB and SEER cohorts diverge on a filter the PI never consciously decided. Every filter that any common registry analysis would conventionally apply is surfaced for explicit yes/no/custom. The completed checklist (including rejected items) is appended to the Phase 1 CONSORT report as a permanent audit record — answering "what filters were even considered?" after the fact.

---

## [3.5.0] - 2026-05-24

### Added — Phase 0 PRE-DESIGN LITERATURE RECON as hard gate in `/analyze` (per L048)

This release closes the canonical "I-analyzed-it-but-someone-already-published-this" failure mode by making `/literature-review` a non-skippable prerequisite for `/analyze`. The trigger was the **Esophageal Organ-Preservation HTE** project (Bilal Mirza, 2026-05-23) — a full Standing-Rule-A analysis (5 rungs, multi-estimator concordance, N=53,389 NCDB) was completed before discovering that **Sakowitz et al. 2025 (J Thorac Cardiovasc Surg, N=3,786)** had published essentially the same NCDB analysis 4 months prior with the same headline HR 1.75. The work was not wasted (HTE quantification, adenocarcinoma inclusion, and methodological extensions are genuinely novel) but the framing had to reposition from "first NCDB evidence" to "replication with extension" — a decision that should have been made at Phase 1 not at Phase 7.

#### Phase 0 hard gate

- **`skills/internal/analyze/SKILL.md`** — new **PHASE 0 — PRE-DESIGN LITERATURE RECON** section inserted before Phase 1 INTAKE. Workflow header updated (now four halts). Phase 0 auto-invokes `/literature-review` Mode 0 via Task() if any of {`evidence_bank.json`, `citation_bank.json`, `novelty_assessment.json`, `differentiation_brief.md`} are missing, stale (>30 days), or research-question-mismatched (SHA256 differs from `study_spec.research_question`). State files table expanded to include the four Phase 0 prerequisites. New §0.6 Resume behavior — skips Phase 0 if artifacts are fresh + matched + signed.
- **HALT 0** — PI must select one of: `(a) Novel`, `(b) Replication with extension`, `(c) Pivot scope`, `(d) Abandon`, with required free-text rationale. PI sign-off SHA256-locks `differentiation_brief.md` and writes hash to `novelty_assessment.lock_hash`. Without sign-off, `/analyze` cannot proceed to Phase 1 INTAKE.
- **`skills/internal/literature-review/SKILL.md`** — State-management section now lists three modes (was two): **Mode 0 Phase 0 Pre-Design Gate** (auto-invoked by /analyze; produces `novelty_assessment.json` and `differentiation_brief.md` in addition to evidence + citation banks), Mode A Stateful, Mode B Standalone.
- **`skills/internal/project-init/SKILL.md`** — STEP 4 next-steps language now leads with "**Required next step: `/literature-review`**" and explicitly explains the Phase 0 prerequisite. Existing alternatives (upload dataset, /analyze, /resume-project) retained but framed correctly.
- **`skills/references/kdense-delegations.md`** — new §4b documenting the Phase 0 delegation chain: `scientific-brainstorming` (initial ideation), `literature-review` (systematic sweep), `pubmed-database` + `openalex-database` (direct queries), `scholar-evaluation` (quantitative ranking), `scientific-critical-thinking` (assess prior-work limitations), `hypothesis-generation` (refine if pivot needed), `citation-management` (L041 verification). Includes worked-example failure-mode narrative for L048.

#### New templates

- **`templates/state/novelty_assessment.template.json`** — structured differentiation analysis (search metadata, ranked nearest comparators with ScholarEval scores, evidence landscape, differentiation statement, PI sign-off block, staleness window).
- **`templates/state/differentiation_brief.template.md`** — 8-section PI-facing narrative (what is known / uncertain / unknown, comparators table, what we replicate vs extend vs make novel, anticipated reviewer critique, PI sign-off block with required rationale, audit trail).

#### Lessons log

- **L048 added** to `skills/references/lessons-log.json` — "Pre-design literature recon as non-skippable gate before analysis design lock." Originating session and worked-example narrative documented in detail. `_meta.last_updated` bumped to 2026-05-24; promotion summary updated (48/48 lessons with audit trail).

#### What this prevents

The Phase 0 gate prevents future projects from discovering high-overlap published comparators only at the Discussion-writing stage. Auto-invocation makes the gate friction-free for the PI; SHA256 lock + 30-day staleness window prevents stale assessments from carrying forward without re-check. The differentiation brief becomes Discussion scaffolding regardless of verdict — even a "novel" determination produces a structured rationale that strengthens the manuscript framing.

#### Outstanding follow-up

- `00_Context/working-rules.md` should be updated with the corresponding session-wide rule: "Pre-design literature recon (Phase 0) is required before /analyze locks any specs; PI must sign the differentiation brief; sign-off is valid for 30 days or until research_question changes." This file is not in the CRA repo and must be edited by the user.

---

## [3.4.0] - 2026-05-20

### Added — K-Dense delegation layer + Phase A/B doc refresh

This release wires five K-Dense scientific-skills as runtime delegated executors and refreshes every top-level doc to reflect the current architecture. The K-Dense delegations are a real new feature surface — citation integrity, peer-review-style audits, quantitative quality scoring, Zotero sync, and systematic-search execution — so this is a minor bump rather than a patch.

#### K-Dense delegation layer

- **`skills/references/kdense-delegations.md`** — new single source of truth (319 lines) defining how CRA delegates to K-Dense skills at runtime. Five delegations are formally wired:
  - `scientific-skills:citation-management` — **hard gate** for L041 across `/literature-review` + all `/write-*` + `/manuscript-qc`. PASS / AMBIGUOUS / FAIL routing; no silent fallback; no "PMID: pending verification" placeholders.
  - `scientific-skills:peer-review` — `/manuscript-qc` Check 13 (reviewer-perspective structured pass).
  - `scientific-skills:scholar-evaluation` — `/manuscript-qc` Check 14 (ScholarEval scoring; verdict = NOT READY if total < 14/20) + `/literature-review` STEP 5 per-evidence scoring.
  - `scientific-skills:pyzotero` — auto-on if `ZOTERO_API_KEY` env detected; sync at end of `/literature-review` and `/write-manuscript` Phase 8.
  - `scientific-skills:literature-review` (K-Dense) — primary execution backbone for CRA `/literature-review` STEP 2 + STEP 5 multi-database searches.
- **`/manuscript-qc`** — added Checks 13–15 as delegated K-Dense passes; VERDICT now considers ScholarEval total and citation audit FAIL count.
- **L041 promotion expanded** — `lessons-log.json` `promoted_to` now references 7 files (was 2); covers literature-review, all write-* skills, manuscript-qc, and kdense-delegations.md.

#### Indexer fix

- **`tools/update_skill_registry.py`** — `EXTERNAL_SKIP_SUFFIXES` was matching `-evaluation` recursively, silently filtering `scholar-evaluation/SKILL.md` from the registry even though it's a legitimate nested skill. Fixed to only skip top-level external bundles whose directory name matches. Indexed skill count went from 145 → 151.

#### Top-level doc refresh (Phase A + B)

- **`README.md`** — K-Dense Python is now the default visualize backend (was R + tidyplots/ggplot2); `/write-abstract` and `/manuscript-qc` added to commands table; K-Dense delegation layer noted in Key Features; recommended workflow ends with `/manuscript-qc`.
- **`ARCHITECTURE.md`** — new Design Principle 8a (K-Dense delegations); new System Overview Section B' (K-Dense as runtime expert references); Manuscript Layer table includes `/write-abstract` and `/manuscript-qc`; Audit Layer expanded to native 12 checks + Checks 13–15 K-Dense delegations.
- **`COMMAND_CONTRACTS.md`** — moved to `skills/references/command-contracts.md`. Added `/write-abstract` contract; replaced the planned `/audit-manuscript` with the actual `/manuscript-qc` contract (Checks 13–15 + workflow + verdict rules).
- **`DELEGATION_RULES.md`** — new Section D documenting all 5 K-Dense delegations with mandatory/auto-on flags; cross-links to `kdense-delegations.md`.
- **`ROADMAP.md`** — Phase 0–6 marked complete; Phase 7 (write-* refactor) expanded with concrete target sizes; new Phase 8 (audit tooling); Phase 9 reframed as real-world stress test.
- **`STATE_SCHEMA.md`** — moved to `skills/references/state-schema.md`. Root now a 5-line pointer stub.
- **Outer `CLAUDE.md`** — refreshed v2.0.0 → v3.4.x; documents 12 internal skills + router + 151 vendored externals.

#### Archive

- **`PHASE0_CLEANUP_AUDIT.md`** → `docs/archive/` (obsolete since 2026-04-01).
- **`append_hnscc_lessons.py`** → `clinical-research-assistant/tools/archive/` (one-shot from 2026-05-03).
- Leaked `.DS_Store` files removed from tree.

### Changed

- Plugin metadata version bumped to `3.4.0`.
- `marketplace.json` metadata version bumped to `3.4.0`.

### Migration note

If you have CRA installed as a Claude Code plugin and your installed copy is older than 3.4.0, refresh it from the marketplace to pick up the K-Dense delegation references. If your `~/.claude/plugins/clinical-research-assistant` is a symlink to a dev checkout (the recommended setup), no action is required.

## [3.0.0] - 2026-05-17

### Added — Router-first CRA architecture

This release makes Clinical Research Assistant the single user-facing front door. The user can invoke CRA once, and the router selects the best internal workflow, delegated engine, or pasted external skill.

- **`clinical-research-assistant/skills/clinical-research-assistant/SKILL.md`** — new router skill. It reads the generated skill registry, classifies each request, selects the best primary route, and normalizes delegated/external outputs back into CRA state.
- **`clinical-research-assistant/skills/internal/`** — new home for first-party CRA skills. The original native CRA skills now live here: project-init, resume-project, analyze, data-analysis, literature-review, visualize, write-introduction, write-methods-results, write-discussion, write-abstract, and write-manuscript.
- **`clinical-research-assistant/skills/external/`** — new paste-in folder for borrowed or third-party skills. Supports both `<skill-name>/SKILL.md` folders and `.skill` package archives.
- **`clinical-research-assistant/tools/update_skill_registry.py`** — deterministic registry updater. It scans internal and external skills, parses frontmatter, and regenerates `skills/references/skill-registry.yaml` and `skills/references/external-skills.md`. Rerunning without skill changes should produce no diff.
- **`clinical-research-assistant/skills/references/skill-registry.yaml`** — generated routing map used by the CRA router.
- **`clinical-research-assistant/skills/references/external-skills.md`** — generated human-readable index of pasted external skills.

### Changed

- BioMedAgent is now packaged under the installable plugin's external skills path as `skills/external/biomedagent/`, preserving its third-party provenance while making it CRA's canonical delegated execution engine rather than a parallel outer skill.
- `CLAUDE.md`, `README.md`, and `OWNERSHIP_MAP.md` now describe the router-first layout and internal/external skill boundaries.
- Plugin metadata version bumped to `3.0.0`.

### Migration note

Legacy top-level skill folders under `clinical-research-assistant/skills/<skill-name>/` have moved to `clinical-research-assistant/skills/internal/<skill-name>/`. Use `skills/clinical-research-assistant/SKILL.md` as the preferred entry point.

## [2.5.1] - 2026-05-06

### Added — V4-audit lessons (L038, L040; finalises L039)

This release groups the three V4-audit lessons captured during the Esophageal-IO V4 methodological audit and the V4_22 within-ICI PSM follow-up. Two are added by this commit (L038, L040); L039 was added directly by the 30-min auto-sync (commit `6b76b7b`) before this commit was prepared, and is documented here so the three V4-audit lessons are described together.

- **L038 — headline-claim audit tagging + comparator-aligned reporting.** Every audit step that involves an A × B interaction must be tagged with both `outcome` and `dataset` fields, and the audit-report prose must repeat that tagging; a P value computed on one outcome must never be interpreted as if it spoke to a different outcome. For comparator-aligned reporting, match the closest published comparator paper's reporting practice in the same subfield and journal tier; cites Miller S et al, *Lancet Oncol* 2024 (PMID 39551068; DOI 10.1016/S1470-2045(24)00528-X) as the field-standard precedent for descriptive within-race subgroup reporting in disparity research.
- **L039 — within-recipient propensity matching for effectiveness comparators** *(added by auto-sync `6b76b7b` from the V4_22 P1–P5 working tree; entry id `L039-within-recipient-propensity-matching-for-effectiveness-comparators`).* When a multi-stage access-disparity manuscript reports a within-treatment-recipient hazard ratio (e.g., NHB vs NHW within ICI recipients), an unmatched within-recipient HR is not a sufficient anchor — measured access factors at the moment of treatment receipt (timing from diagnosis to treatment, prior multimodal therapy, comorbidity, facility type, insurance) confound the within-recipient effectiveness estimate. The within-recipient HR must come from a 1:1 propensity-matched analysis on those access factors, with a complementary IPTW sensitivity (logistic vs flexible-ML / gradient-boosted-tree PS), a propensity-weighted KM figure, a histology-stratified version (EAC vs ESCC), and an explicit time-to-treatment Cox sensitivity. Empirical anchor: V4 NCDB Stage IV ICI 2018+ matched HR 1.25 (95% CI 1.03–1.53; P=.03), Δ(GBT-IPTW vs logistic-IPTW) = 0.02 HR units, ΔHR after time-to-ICI adjustment = +0.03.
- **L040 — PSM caliper-binding diagnostic.** For every PSM analysis, run an extended caliper sweep at 0.01 / 0.05 / 0.10 / 0.20 / 0.25 / 0.50 / 1.00 × pooled SD logit-PS plus an unbounded sweep, and for each caliper report matched-pair count, % treated matched, median match distance, maximum match distance, and an explicit Yes/No binding flag. (Originally drafted with id `L027-psm-caliper-binding-diagnostic`; rebadged to L040 to avoid collision with the v2.5.0 batch's `L027-five-agent-self-audit-before-manuscript`.)

### Maintenance

- **`.gitignore`** — added pattern `/PUSH_*_INSTRUCTIONS.md` under the existing "Local dev navigation note" section. Per-batch push-instruction docs (e.g., `PUSH_v2.5.0_INSTRUCTIONS.md`) are local meta-content for handing the working tree off between sessions; they are not part of the skill source and should not flow upstream.

### Why this is v2.5.1 and not part of v2.5.0

The three V4-audit lessons were drafted in a different work session from the v2.5.0 HNSCC-TAM rigor remediation batch (L027–L037). They are additive (not breaking), they originate from a different empirical session (Esophageal-IO V4 audit + V4_22 within-ICI PSM, both Bilal Mirza / U Arizona, May 2026), and they live cleanly on top of v2.5.0 without amending it. The v2.5.0 commit (`21fbfc5`) is preserved unchanged.

## [2.4.0] - 2026-04-26

### Added — Mandatory analysis-report rule

Every analysis must end with a date-stamped, structured markdown report. The report is the durable deliverable that the manuscript Methods and Results sections are drafted from, that co-authors audit, and that future sessions read first before re-deriving anything. No analysis is considered complete without it.

- **`skills/analyze/SKILL.md`** — added new `Step 9 — Generate the Analysis Report (MANDATORY)` section between `/visualize` reminder and `Reporting Standards`. Defines filename pattern (`analysis_report_<short-question-slug>_YYYY-MM-DD.md`), required-section template (16 sections in fixed order), per-claim requirements (effect size + 95% CI + P + BH-FDR Q + numerator/denominator), versioning rule (re-generate on re-run; archive prior), and a compliance checklist that must pass before the report is declared complete.
- **`skills/data-analysis/SKILL.md`** — added `<mandatory_analysis_report>` block summarising the 16-section template and pointing to `analyze/SKILL.md` Step 9 for the full template and compliance rules.
- **`skills/references/lessons-log.json`** — added entry `L026-mandatory-analysis-report` so the rule is machine-readable and trigger-pattern-routable for future sessions.

The report is the single source of truth for what was done; future sessions read it first before re-deriving findings, and the manuscript-writing skills (`/write-methods-results`, `/write-discussion`, `/write-abstract`) draw their Methods/Results/Limitations content from the report rather than from chat history.

## [2.3.0] - 2026-04-26

### Added — `write-abstract` sub-skill (Bilal Mirza editorial rubric)

A new sub-skill at `skills/write-abstract/SKILL.md` codifies a 12-principle editorial philosophy for writing and auditing abstracts, with a 12-point gate that runs explicitly before any draft is declared submission-ready.

**The 12 principles:** (1) coherence as primary editing criterion, (2) hypothesis-falsification narratives in three places, (3) calibrated language tracking epistemic standing, (4) race terminology matching what was measured, (5) audience calibration leaning biologist for translational, (6) Results as largest section, (7) therapeutic implications at the level data supports, (8) confounders in manuscript not abstract, (9) honesty over impact, (10) compliance as final pass, (11) four-criterion rigor gate (BH-FDR + bootstrap BCa + permutation + jackknife) before any claim earns abstract space, (12) prose over bullets.

**Priority order for use:** principles 3, 7, 9 for active editing; principles 1, 2, 6 for narrative architecture; principle 10 for compliance; principle 11 for rigor.

**Includes** a venue cheat-sheet (AATS / ITSOS / Summit; JTCVS; JAMA Oncology; JCO; ASCO; AHA / ACC; NEJM; Lancet; Annals of Surgery), workflows for both drafting and auditing, and a worked example applying the gate to the ITSOS 2026 esophageal disparity abstract.

**Wired into** `write-manuscript/SKILL.md` Phase 7 (Abstract) — the orchestrator now delegates abstract drafting to the new sub-skill.

**Lessons log additions** (`skills/references/lessons-log.json`): 9 new entries (L017–L025) covering coherence, falsification arc, calibrated language, race terminology, section weight, therapeutic implications, honesty-over-impact, four-criterion rigor gate, and the 12-point final-pass gate.

## [2.2.0] - 2026-04-25

### Added — BioMedAgent-adapted methodology (the *ideas*, not the tool catalog)

Inspired by Bu et al., *Empowering AI data scientists using a multi-agent LLM framework with self-evolving capabilities for autonomous, tool-aware biomedical data analyses*, Nat Biomed Eng 2026 (https://github.com/BOBQWERA/BioMedAgent.git).

- **`skills/references/biomedagent-methodology.md`** — new cross-cutting reference for clinical research that distils the four transferable BioMedAgent ideas: (1) three-phase pipeline (Plan → Execute → Verify with self-correcting feedback loops), (2) task classification before method selection (six-way routing table for clinical research), (3) memory retrieval before re-deriving (read the lessons log first), and (4) anti-misclassification rules (Cox-PH violation, complete-case bias, immortal-time bias, causal language for observational data, NCDB DUA cell-N≥11, etc.).
- **`skills/references/lessons-log.json`** — new machine-readable memory log seeded with 16 entries from real sessions: 10 from the V3 Esophageal Cancer Disparity analysis (Simpson's-paradox prevention, time-stratified Cox, multiple-imputation sensitivity, E-value reporting, master significance with BH-FDR, NCDB DUA compliance, stage decomposition, subgroup-power justification, provider-vs-patient-side gating), 3 from the V4 cross-cohort harmonization and JAMA-table rebuild (cohort harmonization before cross-cohort comparison, JAMA table-formatting discipline, JAMA P-value formatting), and 3 from the BioMedAgent methodology adaptation itself (three-phase pipeline, task classification, memory retrieval).
- **`skills/analyze/SKILL.md`** — added `<biomedagent_adapted_methodology>` block at the top instructing every analysis to read `lessons-log.json` and `biomedagent-methodology.md` first, classify the task before method selection, and append a new lesson at session end.
- **`skills/data-analysis/SKILL.md`** — same pointer block (shorter form).
- **`skills/write-manuscript/SKILL.md`** — same pointer block, framing the existing 9-phase manuscript orchestrator as an instance of the BioMedAgent three-phase pipeline (Plan = Phase 0–1, Execute = Phases 2–7, Verify = Phase 8).

### Maintenance philosophy
The lessons log is append-only. Mark superseded entries `"deprecated": true` rather than deleting them; the audit trail matters. Each new clinical-research session that surfaces a new pattern (pitfall, default sensitivity, classification trap) should append an entry. This is the self-evolution mechanism BioMedAgent uses; here it is the explicit clinical-research analogue.

### What this is NOT
- Not a port of BioMedAgent's 65-tool catalog (those are bioinformatics tools, mostly duplicated by the existing `bio-research`, `scientific-skills`, and `pyhealth` plugins).
- Not a new top-level skill — the four ideas are integrated into the three existing analytic/manuscript skills.
- Not a replacement for the standalone `biomedagent` Cowork plugin if you have it installed; this just brings the *ideas* into clinical-research-assistant so the two plugins can coexist or you can choose to uninstall the standalone one.

## [2.1.0] - 2026-03-10

### Added
- **Research connector integration**: Each skill now declares exactly which research tools it needs via `allowed-tools` in frontmatter
- PubMed connector (search articles, get metadata, find related, full text, citation lookup)
- bioRxiv/medRxiv connector (search preprints, get details, track publications)
- Scholar Gateway connector (semantic search across academic literature)
- ClinicalTrials.gov connector (search trials, trial details, sponsor search, endpoint analysis)
- BioRender connector (search icons and templates for scientific figures)
- CONNECTOR-SETUP.md guide for enabling all required research connectors

### Changed
- `/literature-review` now has access to PubMed, bioRxiv, Scholar Gateway, Clinical Trials, and web search
- `/write-manuscript` (orchestrator) has access to all connectors since it coordinates all phases
- `/write-introduction` and `/write-discussion` have PubMed + Scholar Gateway for finding additional references
- `/visualize` has BioRender access for scientific icons and templates
- `/analyze` and `/write-methods-results` are scoped to local tools only (data crunching, no web access needed)

## [2.0.0] - 2026-03-08

### Added
- Migrated all 7 commands from `commands/` to `skills/` directory structure (preferred by Anthropic)
- Each command is now an independent skill with proper frontmatter (`name`, `description`, `argument-hint`)
- `argument-hint` support for `/analyze`, `/literature-review`, and `/visualize`
- Plugin settings template (`settings-template.md`) for configurable defaults (target journal, citation style, voice, etc.)
- MIT LICENSE file
- `user-invocable: false` on data-analysis skill (knowledge base, not directly invoked)

### Changed
- **BREAKING**: Commands directory removed — all commands are now skills under `skills/`
- Version bump to 2.0.0 (major structural change)
- Updated plugin.json description and author name

### Removed
- `commands/` directory (replaced by `skills/`)

## [1.4.0] - 2026-03-08

### Added
- XML tags (`<role>`, `<rules>`, `<interaction_rules>`, `<examples>`, etc.) across all command files for improved prompt structure
- Concrete examples in 6 command files (Introduction paragraph, Results paragraph, Toggle Rule, Table 1 format, forest plot code, evidence summary table)
- Anti-hallucination guardrails (`<citation_integrity>`) in literature-review command
- Parallel search guidance for literature-review (PubMed, bioRxiv, Scholar Gateway simultaneously)
- JSON-based state persistence (`manuscript_state.json`, `manuscript_context.json`) in write-manuscript
- Context window refresh recovery in write-manuscript
- "Why" context for key rules (funnel structure, association language, loop-closing)
- Reference files: `method-selection-guide.md`, `registry-cautions.md`, `diagnostics-checklist.md`
- CHANGELOG.md

### Changed
- Shortened plugin description in plugin.json for cleaner display
- Fixed "HTML table" references to "formatted markdown table" in analyze command
- Consolidated domain expertise to SKILL.md as single source of truth (removed duplicates from analyze.md and literature-review.md)
- Compressed 14 less-common figure types into compact reference table in visualize command
- Cleaned SKILL.md frontmatter to use only recognized fields (`name`, `description`)

### Removed
- Duplicated domain expertise sections from analyze.md and literature-review.md
- Redundant Excel formatting specifications in analyze.md
- Non-standard frontmatter fields (`metadata`, `category`) from SKILL.md

## [1.3.0] - 2025-12-01

### Added
- Initial plugin release with 7 slash commands
- /analyze — Full statistical analysis workflow
- /visualize — Publication-quality figure generation
- /write-manuscript — Full manuscript orchestrator
- /write-introduction — Introduction section writer
- /write-methods-results — Methods and Results writer
- /write-discussion — Discussion and Conclusion writer
- /literature-review — Evidence synthesis and search strategy
- Clinical statistical analyst skill (SKILL.md)
