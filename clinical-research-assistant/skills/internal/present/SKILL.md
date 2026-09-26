---
name: present
description: Use when the user asks for a presentation, podium or oral-abstract talk, slide deck, slides, invited session, discussant or audience Q&A preparation, or presenter notes for a study, or wants existing slides redesigned, restyled, decluttered, recoloured or re-figured.
argument-hint: "[abstract/project path, slide numbers, or the slide change requested]"
allowed-tools: Read Write Edit Bash Task
---

# /present: Study Presentation Builder

## Overview

Build and edit conference decks that look like the author's **gold-standard ITSOS 2026 deck**:
native PowerPoint geometry, Times New Roman, 28 pt minimum, black text, one statistic per
comparison, an identical footer legend on every slide, and a story told slide by slide in the
presenter notes. Every number traces to the project's `MASTER_ANALYSIS_REGISTRY.json`.

The design is measured, not remembered. `scripts/deck_style.py` draws it, `scripts/deck_lint.py`
fails anything that drifts from it, and `tests/test_gold_standard.py` proves both still agree.

| Mode | When | Rule |
|---|---|---|
| **BUILD** | No deck exists yet | Story first, then build every slide with `deck_style` |
| **EDIT** | A deck exists | Change only the slides named. The author edits the same file in parallel. |

**EDIT is the common case and the dangerous one.** See "Editing a live deck".

## Read first

1. The project's `Reports/MASTER_ANALYSIS_REGISTRY.json`, the **only** source of numbers (L045).
2. The project's `CLAUDE.md`: palette conventions, DUA limits, standing rules.
3. `references/gold-standard-spec.md`: every size, colour and position, and the 20 slide archetypes.
4. `references/story-and-notes.md`: the arc, the notes contract, modest conclusions, the Q&A pack.
5. `references/content-lessons.md`: claims a slide can and cannot make (denominators, registry
   codes, measures). Read it before writing a single conclusion.
6. `references/pptx-gotchas.md`: every entry is a bug that shipped. Read before the first write.
7. `references/aesthetic-principles.md` and `references/slide-patterns.md`: the taste behind it,
   and the catalogue of figure ideas.

## The house standard on one screen

| | Rule |
|---|---|
| Canvas | 20 × 11.25 in; title at (0.938, 0.729); rules at y 1.623 and 10.286, x 0.938, w 18.125 |
| Type | Times New Roman only. Body **28 pt minimum**; legend 32; title 43.5 bold; conclusions 32 |
| Colour of text | Black. White only on dark fills. Navy `1A3255` only for structural labels |
| Bold | Titles and structural labels (table heads, step headings, forest group headings) only |
| Grey | Lines only: grid `E9ECF0`, rules `E1E6ED`, axis/arrows `6B7280`. Never text |
| Race colours | NHW `123057`, NHB `801819` (red reserved; never a category colour) |
| Legend | Footer only: 0.41 in rounded squares at x 0.92, y 10.47; 32 pt labels; identical on every slide |
| Bars | Top-rounded; one statistic per pair above it (P or HR); no per-bar values alongside it |
| Forest | Black 0.20 in markers, 0.035 in CI, **dotted** null, log ticks, estimate + P at right, arrow label below |
| KM | Native step polylines, 24-month landmark line + dots, statistic top-right, legend in footer |
| Furniture | No slide numbers. No source line. No in-plot legends. Pictures only for branding |
| Density | Plots centred, as little text as possible; detail goes in notes and hidden backup slides |

## Hard rules

**Numbers.** Every value comes from the registry or is re-derived by a script written in this
session. Never copy a number off an earlier slide, draft, or message. When a slide shows two values
and their difference, check the subtraction (40.0 − 30.2 = 9.8, not a registry 9.9).

**Claims.** Follow `references/content-lessons.md`. Compare groups on the all-patient denominator,
never on within-subgroup shares. Name registry codes by their dictionary definition. Never assign
a decision to clinicians or patients when the registry cannot. NCDB is hospital-based.

**Suppression.** NCDB PUF: suppress 0 < n < 11, and suppress a second cell when a single suppressed
cell could be recovered by subtraction.

**Native shapes.** Data slides contain zero pictures (curves are open custGeom polylines via
`deck_style.polyline` / `km_panel`). Pictures are allowed only for branding: title-slide art,
logos, the conclusions watermark.

**Colour binds to one meaning, once.** Declare tokens before drawing; recolour by label and
region, never by hex. When the author supplies a palette, sample the exact hexes, drop a shade that
cannot be told apart from its neighbour, and say which one you dropped.

**Uniformity.** Draw through `deck_style` tokens only (`frame`, `legend`, `grouped_bars`, `forest`,
`stacked_rows`, `km_panel`, `steps`, `numbered_list`, `note`). Never hand-place furniture.

**No editorial voice** on slides. State the finding, not its importance.

## Workflow

```
1 INTAKE   abstract, registry, project CLAUDE.md, existing deck, venue time limit
2 STORY    slide list: the question each slide answers (story-and-notes.md §1)   -> HALT 1 (BUILD)
3 MOCKUP   any NEW figure type: one preview PNG before touching the deck         -> HALT 2
4 BUILD    deck_style only; one pinned script per slide; back up first (single rolling backup)
5 LINT     python3 scripts/deck_lint.py DECK.pptx --minutes N    -> zero FAIL before delivery
6 VERIFY   render and LOOK (PowerPoint export when idle; preview_deck.py otherwise)
7 NOTES    notes contract: hand-off sentence, finding, rounded numbers
8 Q&A      qa_prep_<date>.md: discussant questions in order, adjusted/matched numbers only
```

The lint gate is not optional: a deck with any FAIL is not delivered. WARN lines are read one by one
and either fixed or explicitly accepted (e.g. a bold structural label).

## Editing a live deck

The author has the deck open and is editing it between your runs. Every
assumption you cached is stale.

**A full-rebuild script is incompatible with a co-edited deck.** This is the
trap, and it is invisible until it has already destroyed work: a
`build_deck.py` that regenerates every slide from source is correct on the first
build and catastrophic on the second. The author fixes a title in PowerPoint, you
are asked to change one number on another slide, you re-run the builder, and
their fix is gone with no error and nothing in the diff to notice. Rebuilding is
*the same class of destructive act as editing a slide you were not asked to
touch* — it just does it to all of them at once.

So from the moment the author has the file, the builder is no longer the way you
change the deck:

- **Fingerprint what you wrote.** On every build, record the deck's SHA-256
  beside it (`.build_fingerprint.json`). On the next run, hash the deck first. If
  it does not match, the author has edited it.
- **A changed fingerprint means STOP, not `--force`.** Do not rebuild. Switch to
  a targeted in-place edit of the named slides: open the existing deck, find the
  slide by title, change only what was asked, save. `clear_slide()` +
  redraw on that one slide is the largest acceptable blast radius.
- **Never pass a force flag on your own initiative.** Only the author can
  authorise discarding their edits, and only for that one run.
- **Regenerating "just to pick up the new style" is not a reason.** If a
  contract change needs to reach every slide, say so and let the author decide
  whether to re-export or hand-apply.

1. **ONE working deck, and back it up without cloning it.** The venue folder
   holds exactly one `.pptx` and one `.pdf` — no dated copies, no `_v2`, no
   `_final`, no `_pre_<change>`. A folder of near-identical decks is its own
   hazard: the author opens the wrong one, edits it for an hour, and the work is
   stranded in a file nobody is publishing from. Recovery comes from a **single
   hidden rolling backup** (`.<deck>.prev.pptx`) overwritten on every write, so
   only the immediately previous state is recoverable — that is the trade, and
   it is the right one, because a visible copy the author might open is more
   dangerous than a lost intermediate. Render intermediates (PDF pages, PNGs) go
   to a scratch directory, never beside the deck. Author directive 2026-09-16 (re-violated 2026-09-23..25, when ~30 `_pre_<change>` copies piled up beside the ITSOS deck; do not repeat it):
   *"have one working ppt, dont save multiple copies."*
2. **Re-read the deck at the start of every task.** Slide count, indices, and
   contents all change. During one session a deck went 51 → 52 → 49 → 48 → 47 → 48.
3. **Locate slides by title text, never by index** (`deck_style.find_slide_by_title`).
4. **Locate furniture geometrically, never by shape index**
   (`deck_style.keep_furniture`) — anything above the title rule or below the
   footer rule is furniture; everything between is body.
5. **Change only what was asked.** The author's standing instruction, restated
   2026-09-16: *"we are both making edits at the same time, do not change the
   edits I make."* Earlier form: *"only make changes to slides I ask you to,
   leave others as they are, I am also making edits on my own."* This binds the
   builder as much as the editor — see the rebuild trap above.
6. **Report what you overwrote.** If you replaced the author's own text, quote the
   old text in your reply and name the backup. They may have wanted both.
7. **When in doubt, diff before you write.** Comparing the on-disk deck against
   your last build costs one hash and is the only thing standing between a
   routine edit and silently reverting an afternoon of the author's work.

---

## Verification

A slide is not done until you have looked at it.

1. `python3 scripts/deck_lint.py DECK.pptx --minutes 7`: zero FAIL.
2. Render:
   - **PowerPoint idle and deck closed:** `python3 scripts/render_deck.py DECK.pptx OUT --match "Title"`
     (copy to scratch first; hidden slides shift PDF pages, so match by title).
   - **Author working in PowerPoint, or automation blocked:** `python3 scripts/preview_deck.py
     DECK.pptx OUT --slides 3,5 --sheet`. It draws shapes and text offline, which is enough for
     collisions, overflow and alignment; do the final PDF check when PowerPoint is free.
   - Never open your files through the author's live PowerPoint session (gotcha 16).
3. Read the PNG. Look for clipped text, labels over data, collisions with rules, a legend that
   moved, numbers that do not add up.

Dry-run first for any bulk operation (`DRY=1` prints the plan and writes nothing).

## Presenter notes and Q&A

Notes follow `references/story-and-notes.md` §2: 20–100 words, a hand-off first sentence, whole
percentages, percentage points for differences, ~130 words per talk minute. `deck_lint.py` checks
banned openers, "population-based" NCDB, decimal percentages and the word budget. Notes attach by
slide title; inject a notes placeholder where python-pptx returns None.

For a discussant, write `qa_prep_<date>.md`: questions in the order received, 2–4 spoken sentences
each, adjusted or matched numbers labelled as such, one honest limit per answer, plus a tiered
audience list (basic → complex) and a corrections list if the abstract said something the final
analysis revised.

## Deliverables

| File | Contents |
|---|---|
| `<deck>.pptx` | the deck: exactly one, no dated copies |
| `.<deck>.prev.pptx` | hidden rolling backup, previous state only |
| `presenter_notes_<date>.md` | notes exported in slide order |
| `qa_prep_<date>.md` | discussant answers + audience questions |
| `Scripts/build_slide_*.py` | one pinned script per slide built |

## Common mistakes

| Mistake | Fix |
|---|---|
| 18–24 pt axis ticks or "All P<.001" annotations | 28 pt floor; `deck_lint` S2 |
| Grey labels, bold values, coloured forest markers | black text, bold only structural, black markers |
| Slide numbers / source line in the footer | remove; the footer holds the legend only |
| Legend redrawn per slide by hand | `deck_style.legend()`; `deck_lint` S8 |
| "Black patients refused less" from within-subgroup shares | all-patient denominator + adjusted model |
| "Not offered" / "not recommended" for NAACCR 1340 code 1 | "not part of the planned first course" |
| Decimal percentages and "percent" for differences in notes | whole numbers; "percentage points" |
| Conclusions that assign blame or overstate mediation | `story-and-notes.md` §3 modesty contract |
| Re-running a full-deck builder after the author edited | fingerprint, then targeted in-place edit |
| Rendering through the author's open PowerPoint | `preview_deck.py`; export later |
| `_pre_<change>` copies next to the deck | single hidden rolling backup |

## Changelog / Lessons learned

- **2026-09-25 (L085): gold standard v2.** Measured the author's ITSOS 2026 deck and rebuilt the
  module on it: 28 pt floor, black text, no slide numbers or source line, footer legend with rounded
  swatches, black forests with dotted null, native KM helpers, conclusions and notes contracts,
  content lessons (denominators, NAACCR 1340, time horizons), `deck_lint.py`, `preview_deck.py`,
  and a red/green test (`tests/test_gold_standard.py`).
