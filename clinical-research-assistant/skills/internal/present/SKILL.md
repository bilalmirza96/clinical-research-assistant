---
name: present
description: Builds and edits conference presentation decks for abstract presentations — podium talks, oral abstracts, invited sessions. Produces native PowerPoint slides in a consistent academic design system, sources every number from the project's MASTER_ANALYSIS_REGISTRY.json, renders figures that fill a slide, and verifies each edit by exporting the deck to PDF and looking at it. Use whenever the user asks for a presentation, a deck, slides, a talk, or wants existing slides redesigned, simplified, or re-figured.
argument-hint: "[abstract/project path, slide numbers, or the slide change requested]"
allowed-tools: Read Write Edit Bash Task
---

# /present — Conference Presentation Builder

## Role

You build and edit the slide deck for an abstract presentation. The deck is a
*deliverable*, not a scratch artifact: it goes on a projector in front of an
audience that can do arithmetic, and every number on it must trace to the
project's registry.

Two distinct modes, and you must know which you are in before writing anything:

| Mode | When | Rule |
|---|---|---|
| **BUILD** | No deck exists yet | Generate the full deck from the abstract + registry |
| **EDIT** | A deck exists | Change only the slides named. The author edits the same file in parallel. |

**EDIT is the common case and the dangerous one.** See "Editing a live deck".

---

## PREREQUISITE — read before anything else

1. The project's `Reports/MASTER_ANALYSIS_REGISTRY.json` — the **only** authoritative
   numbers surface (L045). Re-derive, never transcribe.
2. The project's `CLAUDE.md` — palette conventions, DUA restrictions, standing rules.
3. `references/aesthetic-principles.md` — the house look for national surgical and
   oncology meetings, and the patterns the author has already rejected.
4. `references/slide-patterns.md` — the layouts that work, with measured geometry.
5. `references/pptx-gotchas.md` — read this before your first python-pptx write.
   It is not optional; each entry is a bug that shipped.

---

## Hard rules

**Numbers.** Every value on a slide comes from the registry or is re-derived from
the locked cohort by a script you wrote in this session. Never copy a number off
an earlier slide, an earlier draft, or your own previous message.

**Registry arithmetic must survive the audience.** If a slide shows 40.0%, 30.2%
and "9.9-point difference", someone will subtract. Before shipping any slide that
displays both components and their difference, check that they agree. When they
do not, find out why before changing either — a registry value computed as
`round(a,1) - round(b,1)` differs from `round(a-b,1)`, and the registry is locked,
so you report the discrepancy and let the author decide. Do not silently "fix" a
locked value, and do not silently display one that contradicts the slide.

**Suppression.** NCDB PUF DUA: suppress any cell with 0 < n < 11. Never describe
NCDB as "population-based" (it is hospital-based). Carry the verbatim disclaimer.

**Native shapes are the deliverable. A finished deck contains zero images.**
Every slide the author will present — data slides included — is real PowerPoint
geometry: rectangles, rounded rectangles, ovals, lines, textboxes. The author
edits decks between your runs, and a rendered PNG is a dead end for them: they
cannot fix a typo, renumber a value, or recolour a series without coming back to
you. Render matplotlib **only** for marks a plotting engine genuinely owns —
survival curves, densities, gradient fills, kernel estimates — and say in the
manifest why that slide is an exception. Assert it at build time:

```python
n_pic = sum(1 for sl in prs.slides for sh in sl.shapes if sh.shape_type == 13)
assert n_pic == 0, "a slide still contains a rendered image"
```

Matplotlib still earns its place in **Phase 3**: a mockup PNG is the cheapest way
to settle a design before you build it. Mockups are for the decision; the deck is
built natively afterwards. Keep the mockup scripts, and record in the manifest
that they no longer feed the deck.

**Bind every colour to one meaning, once, before drawing anything.** Declare the
deck's semantic tokens in the drawing module and draw *through the token names*,
never through a raw `NAVY`/`RED`:

```python
OPEN_C = NAVY    # the open/reference arm, everywhere
MIS_C  = RED     # the minimally invasive arm, everywhere
NS_C   = SLATE   # not statistically significant
```

The failure this prevents is specific and easy to walk into: a cohort slide binds
navy to the reference arm, then a forest two slides later colours "favours the
other arm" navy because navy reads as the primary hue. Now navy means two things
in one deck and the audience is silently misled. **Colour a forest marker by
which arm the effect favours**, so the arm colours established on the cohort and
unadjusted slides carry straight through. Where a race series is present, red is
reserved for the disadvantaged group named in the project CLAUDE.md and may not
be reused for a registry or category series. Recolour by *label and region*,
never by hex — the same hex often carries two meanings in one deck.

**Uniformity is a hard requirement, not a preference.** Pin the furniture as
module constants and use them on every content slide, so nothing drifts by a
tenth of an inch between slides:

| Constant | What it fixes |
|---|---|
| `TITLE_Y`, `MARGIN_L/R` | title origin and side margins |
| `BODY_TOP`, `BODY_BOTTOM` | the band content may occupy |
| `FOOT_Y` | footnote origin |
| `SZ_*` | the type scale, one size per role |

One P-value format, one en-dash convention, one footnote size, one eyebrow size
across the whole deck. A registry that stores `"<0.001"` as a string will print
`P <0.001` beside `P = .432` unless the formatter normalises it.

**Audit before you ship.** Walk every run on every slide and fail on anything off
-contract — it catches what a render does not:

```python
# 0 pictures, 0 off-palette runs, 0 off-font runs, identical title/footnote origins
```

**No editorial voice.** Slide text states findings; it does not characterise them.
"The largest modifiable step identified here is receipt of curative-intent surgery"
is a finding. "The highest-leverage intervention in this disease" is an editorial.
Strip the second kind on sight.

---

## Workflow

```
Phase 1 INTAKE     read abstract, registry, project CLAUDE.md, existing deck
Phase 2 OUTLINE    slide-by-slide plan: title, claim, evidence, source key
   HALT 1          author approves the outline (BUILD mode only)
Phase 3 MOCKUP     render candidate layouts as PNG, before touching the deck
   HALT 2          author picks a direction
Phase 4 BUILD      write slides; back up the deck first
Phase 5 VERIFY     export PDF, render PNG, LOOK at it
Phase 6 NOTES      presenter notes, narrative only
```

**Phase 3 is not skippable for any new figure or layout.** Rendering a mockup PNG
costs one tool call; rebuilding a deck the author rejects costs the session. The
author will routinely reject two or three directions before one lands — that is
the process working, not failing.

---

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
   to a scratch directory, never beside the deck. Author directive 2026-09-16:
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

## Verification — non-negotiable

A deck edit is not done until you have looked at the rendered slide.

```bash
python3 scripts/render_deck.py DECK.pptx /tmp/out --match "Slide Title"
```

**Quit PowerPoint before exporting.** A running instance serves a cached copy of an
open file, so you render the previous version. This produces the most confusing
failure mode available: an edit that is correct on disk and absent from the render.
If a render disagrees with what you just wrote, quit PowerPoint and re-export
before concluding anything.

Then Read the PNG. Look for: text clipped at the slide edge, labels written over
data, stray black hairlines, collisions between a label and a rule, numbers that
do not add up.

Dry-run first for any bulk operation. `DRY=1` should print the plan and write
nothing. Dry runs on one deck caught four destructive mistakes before they landed,
including a recolour that would have turned 99 person-icons yellow.

---

## Figures

Text and simple geometry are **native PowerPoint shapes** — editable by the author,
crisp at projector resolution. Charts that need a plotting engine (Kaplan-Meier,
distributions, gradient fills) are rendered with matplotlib at the deck's aspect
ratio (13.33 × 7.5 in = 16:9) and placed full-bleed.

Figure scripts read locked values and restyle them. A figure script never
recomputes an effect estimate. It may re-derive a display quantity the registry
does not store (medians, censored counts) — say so in the script docstring and
print the derived values on every run so they are checkable.

See `references/slide-patterns.md` for the catalogue: estimator ladder, era blocks,
data-source table, forest plot with a log-symmetric axis, KM hero with a gradient
gap wedge, survminer-idiom KM, icon array, dumbbell, gap-over-time.

---

## Presenter notes

Narrative only — what the presenter says, in order, telling a story across slides.
No "Reference" blocks, no registry keys, no model specifications in the notes: they
sit in the speaker's eyeline during the talk. Provenance belongs in an archive file
beside the deck, not in the notes pane.

Notes attach by slide title, not index. Some programmatically built slides have no
notes placeholder — inject one into the notes-slide XML rather than crashing.

---

## Deliverables

| File | Contents |
|---|---|
| `<deck>.pptx` | the deck — exactly one, no dated copies |
| `Presentations/<venue>/.<deck>.prev.pptx` | hidden rolling backup, previous state only |
| `Presentations/<venue>/presenter_notes_<date>.md` | exported notes |
| `Scripts/build_slide*.py` | one pinned script per slide built |
| `Scripts/make_*_mockup.py` | mockup generators, kept for re-runs |

One script per slide, named for the slide. They are the record of how the deck was
built and the only way to rebuild it after the author edits around you.
