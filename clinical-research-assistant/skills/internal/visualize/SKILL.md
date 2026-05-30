---
name: visualize
description: Manuscript-rigor orchestrator for publication-quality figures. Reads figure intent and analysis results from /analyze, writes a figure plan, generates the full deck via delegation to K-Dense scientific-visualization and scientific-schematics, delivers a registered figure package. Use after /analyze has produced results_registry.json and figure_intent.md. Two approval halts — plan then deck.
argument-hint: "[figure number, figure type, or 'all']"
allowed-tools: Read Write Edit Bash Task
---

# /visualize — Figure Orchestrator

## Role

You orchestrate publication-quality figure generation for clinical research manuscripts. When invoked, **you generate the full figure deck end-to-end** — reading the planned figures from `/analyze`, writing a render plan, executing all figures, and delivering a registered package. You delegate execution to K-Dense scientific skills (primarily `scientific-skills:scientific-visualization` for charts and `scientific-skills:scientific-schematics` for diagrams), loading each as expert reference at runtime — the same pattern `/analyze` uses with statistical libraries. The user invokes `/visualize` once and receives the complete figure deck.

## What runs when you invoke `/visualize`

```
Phase 1 INTAKE      read figure_intent.md, results_registry.json, study_spec.json
Phase 2 PLAN        produce figure_specs.json (per-figure render spec)
   ✋ HALT 1        user approves the figure plan
Phase 3 GENERATE    delegate each figure to its K-Dense skill, render PDF + PNG
   ✋ HALT 2        user reviews the rendered deck; approve/regenerate
Phase 4 DELIVER     finalize figure_registry.json, save deck to figures/
```

Two halts. Plan first, then rendered-deck review. Figures are visceral — the plan is abstract, the deck is concrete.

---

## PREREQUISITE — read before anything else

Before any phase executes, read these files **in this order**:

1. `../../references/lessons-log.json` — relevant figure lessons (L013 P-value format, L020 race terminology, L038 comparator declaration, L042 manuscript formatting)
2. `references/aesthetic-standards.md` — non-negotiable visual standards (typography, color, dimensions, annotations)
3. `references/delegation-by-figure-type.md` — which K-Dense skill executes which figure type
4. `references/figure-specs-schema.md` — JSON schema for `figure_specs.json`

If `figure_intent.md` does NOT exist in the project's `specs/` folder, halt: **"No figure intent declared. Run `/analyze` first — Phase 1 produces `figure_intent.md`."**

---

## State files

| File | Read | Written |
|---|---|---|
| `specs/figure_intent.md` | yes (from /analyze) | no |
| `results_registry.json` | yes (data source for each figure) | no |
| `study_spec.json` | yes (target journal → style; subspecialty → conventions) | no |
| `specs/figure_specs.json` (+ `_v<n>.json` on revision) | yes | Phase 2 |
| `figure_registry.json` | yes (resume) | Phase 3–4 |
| `decision_log.md` | append | every halt + every regenerate |

Resume rule: if `figure_specs.json` exists from a prior session, restart from the first incomplete phase.

---

## PHASE 1 — INTAKE

Goal: gather everything needed to plan figures, without locking specs of our own (those come from `/analyze`).

1. Read `figure_intent.md` → list of planned figures with intent (number, type, what it shows, axes, strata)
2. Read `results_registry.json` → identify data sources for each figure (which model output, which derived table)
3. Read `study_spec.json` → target journal (drives dimensions + style), subspecialty (drives conventions)

Output: nothing locked at this phase. Phase 2 produces the locked artifact.

---

## PHASE 2 — PLAN (`figure_specs.json`)

For each figure in `figure_intent.md`, write a complete render spec:

| Field | Content |
|---|---|
| `figure_id` | e.g., "fig_001" |
| `manuscript_number` | e.g., 1, 2, "S1" (supplementary) |
| `title` | descriptive title for caption |
| `type` | KM / forest / ROC / bar+beeswarm / violin / heatmap / CONSORT / etc. |
| `delegation` | K-Dense skill path (per `references/delegation-by-figure-type.md`) |
| `data_source` | `results_registry::<key>` pointer to the data this figure plots |
| `dimensions` | width × height in inches (per journal column rules; default single 3.5×2.5, double 7×5) |
| `panels` | single or multi-panel composition spec |
| `annotations` | P-value format (per L013), comparator label (per L038), CI display, significance markers |
| `color_palette` | colorblind-safe default (Okabe-Ito / viridis); override per study type |
| `axis_labels` | with units; sentence case per aesthetic-standards |
| `legend` | position + content |
| `caption_draft` | one-paragraph caption stub for the manuscript |
| `export_formats` | PDF (primary, vector) + PNG 600 DPI (review) |

Each delegation field names the K-Dense skill that will execute. Common patterns from `references/delegation-by-figure-type.md`:

- Standard plot → `scientific-skills:scientific-visualization`
- Survival → `scientific-skills:scikit-survival` + `scientific-skills:scientific-visualization`
- Diagram → `scientific-skills:scientific-schematics`
- Interactive → `scientific-skills:plotly` (rare in manuscripts)

---

## ✋ HALT 1 — Approve the figure plan

Present:

1. The full `figure_specs.json` rendered as a readable table (one row per figure)
2. Manuscript figure list summary (e.g., "Figure 1 = KM by CR-POPF status; Figure 2 = forest plot of multivariable aORs; Figure 3 = CONSORT flow; Sup S1 = caliper-sensitivity love plot")
3. Cross-references to `results_registry` (every figure's data source verified to exist)

Ask the user how to approve:

- **Bundle (default):** single yes/no covering all figures
- **Section-by-section:** approve figure-by-figure

On `revise`: indicate which figures to revise (e.g., "change Figure 2 to a Cleveland dot plot"); analyze re-writes only those specs; re-presents.

On `reject`: archive `figure_specs.json` as `_v<n>.json` per Concern #8 versioning rule; restart Phase 2.

---

## PHASE 3 — GENERATE (autonomous, batch)

Generate all approved figures in sequence. Per figure:

1. **Load** the delegated K-Dense skill's `SKILL.md` as expert reference (do not write plotting code from memory)
2. **Read** the data source from `results_registry.json` per the `data_source` field
3. **Write code** following the K-Dense skill's documented patterns, applying the locked spec
4. **Apply aesthetic standards** from `references/aesthetic-standards.md`:
   - Typography (sans-serif, 9–10pt body, 10–12pt headers, units in axis labels)
   - Colorblind-safe palette (Okabe-Ito or viridis)
   - Comparator declaration (per L038) — every grouped plot states reference category in caption
   - P-value formatting (per L013) — JAMA convention
5. **Render** PDF (vector) + PNG (600 DPI) to `figures/`
6. **Register** in `figure_registry.json` with code path, data source pointer, sha256 of output, dimensions, captions

Quality gates (each failure → fix and continue; document in decision_log.md):

- ✓ Axis labels include units
- ✓ Multi-group plots state reference category in caption
- ✓ P-value formatted per L013
- ✓ Color palette colorblind-safe
- ✓ Dimensions match journal column rules
- ✓ Resolution ≥ 300 DPI for raster, vector for PDF
- ✓ **No text overlap — HARD GATE.** Visually inspect the rendered PNG (open and look at it) before declaring the figure complete. All axis labels, tick labels, bar value labels, legend, panel labels (A/B/C), and significance brackets must be non-overlapping and non-clipped. If any text overlaps another text element or covers data, re-layout per `references/aesthetic-standards.md` "Layout and overlap prevention" section (rotate labels 30° with `ha='right'` when >5 categorical positions or any label >8 chars; use horizontal bars; reposition legend; etc.) and re-render. Never declare a figure complete without this visual inspection.

R override: if the user explicitly requested R for a figure, use the templates and tidyplots patterns in `references/r-templates.md` instead of K-Dense Python delegation. The aesthetic standards (including the no-overlap hard gate) apply identically.

---

## ✋ HALT 2 — Review the rendered deck

Present:

1. Thumbnail grid of all generated figures (one card per figure with manuscript number + caption)
2. Compliance summary (passed gates per figure; any auto-fixes applied)
3. File paths to PDFs + PNGs

Halt presentation policy (consistent with `/analyze`): concise mode by default; verbose if any gate auto-fix triggered or if regeneration is needed.

User can:

- `approve all` → Phase 4 delivery
- `regenerate figure N with [change]` → re-render only that figure, return to HALT 2
- `add figure X` → write spec, generate, register, return to HALT 2
- `remove figure N` → mark deleted in figure_registry; return to HALT 2
- `abort` → preserve current state, exit

---

## PHASE 4 — DELIVER

Finalize the deck:

1. `figure_registry.json` — all approved figures with: id, manuscript_number, code_path, data_source pointer, file_paths (PDF + PNG), sha256, dimensions, caption, K-Dense skill used
2. `figures/` folder — all PDFs + PNGs with stable filenames (`Figure_N_<descriptive_slug>.pdf`)
3. Captions consolidated in `Reports/figure_captions_<date>.md` for direct paste into manuscript drafts
4. Cross-reference back to `results_registry.json` per L045 SCAR audit trail
5. Update `project_state.json` + append `decision_log.md`

Hand-off downstream:
- `/write-methods-results` reads `figure_registry.json` to reference figures in Methods/Results prose
- `/write-manuscript` assembles the final manuscript including figures
- `/manuscript-qc` audits figure compliance per `manuscript-qc/references/checks.md` Check 5 (Figure Quality)

---

## Aesthetic and policy enforcement

All visual standards (color, typography, dimensions, annotations) live in `references/aesthetic-standards.md` — read at PREREQUISITE. The K-Dense delegation step applies its own publication-quality standards layered on top. If they conflict (rare), the CRA aesthetic standards win — they encode your accumulated journal-specific preferences.

Lesson enforcement directly relevant to figures:

| Lesson | Enforcement |
|---|---|
| L013 (JAMA P-value format) | Applied in annotations; verified at quality gate |
| L020 (race terminology = source labels) | Caption labels match `variable_spec.json` source labels |
| L038 (comparator declaration) | Every grouped/stratified figure caption names the reference category |
| L042 (Georgia 12pt 1.5-spacing for documents) | Applies to caption text in the consolidated captions doc |

---

## After-figure-deck closure

1. Append entry to SCAR via `scripts/analysis_registry.py` (link figure deck to analysis registry)
2. Update `project_state.json` with figures completion timestamp
3. Append `decision_log.md` summary
4. Hand off to `/write-methods-results` if user requests next step


---

## Delegated helper (scientific-skills execution layer — see DELEGATION_RULES.md §F)

- `scientific-skills:scientific-schematics` — conceptual / mechanism diagrams + graphical abstracts (Nano-Banana). Use ONLY for non-data conceptual figures. Data figures stay in CRA's matplotlib/seaborn house pipeline (Poppins/Lora, five-color palette, no figure titles).
