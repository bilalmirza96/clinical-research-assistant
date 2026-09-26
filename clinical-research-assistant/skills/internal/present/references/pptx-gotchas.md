# python-pptx gotchas

Every entry below is a bug that reached a real deck. Read before your first write.

## 1. `drop_rel()` corrupts the deck — absolute prohibition

`drop_rel()` frees relationship IDs, and `add_slide()` then **reuses** them. The
file saves without error and opens wrong. Never call it.

To delete a slide, remove its `sldId` from `p:sldIdLst` and leave the part in
place. To reorder, move the `sldId` element. Use
`deck_style.insert_slide_after()`.

## 2. Reading `shape.line.color` mutates the shape

The property getter calls `_get_or_add_ln()`, which inserts an empty
`<a:ln><a:solidFill/></a:ln>`. PowerPoint renders that as a **black hairline**.
A single colour-audit pass once put 285 stray outlines across 41 slides this way,
and the author saw them before the audit did.

Read outlines from XML (`deck_style.line_hex`). Repair with
`deck_style.strip_empty_outlines`.

## 3. Shape identity: `is` is always False

python-pptx builds a fresh wrapper object on every shape access, so
`shape_a is not shape_b` is true even for the same shape. A filter written as
`[sh for sh in slide.shapes if sh is not header]` excludes nothing — it once
overwrote a slide's eyebrow label instead of its body text.

Compare `._element`. Use `deck_style.same_shape()`.

## 4. Table border tags

The element is `a:lnT`, not `a:ln` + `"lnT"`. String-concatenating the prefix
yields `<a:lnlnT>`, which PowerPoint silently ignores — borders simply do not
appear, with no error anywhere.

Edges must also appear in schema order (L, R, T, B) and **before** the fill
element, so rebuild the whole `tcPr` child list rather than appending. Use
`deck_style.cell_borders()`.

## 5. Table row heights are minimums

PowerPoint grows a row to fit its content. A table laid out to a computed total
height will be taller than you asked. Set the top, let the bottom fall where it
falls, and verify in the render.

## 6. `word_wrap=False` clips text off the slide

A pre-existing box with `word_wrap=False`, 3.89 in wide, holding ~9 in of text,
put a panel's statistics past the slide edge where they were invisible in
PowerPoint and absent from the PDF. Check `word_wrap` on any box you inherit.

## 7. Hidden slides are excluded from PDF export

`show="0"` slides do not render, so **PDF page number ≠ deck slide number**.
Match rendered pages on title text.

## 8. PowerPoint serves cached copies

If the app is running with the file open, `open` returns the in-memory version and
you export the **previous** state. Quit PowerPoint before every export.
`render_deck.py` does this automatically.

## 9. `notes_text_frame` can be None

Programmatically built slides may have no notes placeholder; writing notes crashes
before the save. Inject a body placeholder into the notes-slide XML first.

## 10. Transform by element type, not by size

A rule that classified "anything ≤ 0.15 in wide" as a data marker treated 43
trend-line segments (0.14 in wide, `p:cxnSp` connectors) as markers and would have
shattered the line. Key on `sh._element.tag == qn('p:cxnSp')`.

## 11. Tolerance bands need slack

A tick label whose bottom edge sat at 8.2529 in fell outside a band bound of
8.25 in and was left behind by a group transform, so a curve appeared to drop
below zero. Widen bounds past the measured extremes.

## 12. Label-match windows

Value labels sit above their bars — often 0.42 in above. A 0.35 in match window
finds zero bars and the script reports success on an empty plan. Always print the
match count in a dry run and sanity-check it against the expected number.

## 13. matplotlib `Circle` in figure coordinates draws ellipses

Figure fractions are not square. Icon arrays must be drawn in a dedicated axes
with `set_aspect("equal")`.

## 14. matplotlib does not wrap text

`ax.text` overflows silently past the axes and off the canvas. Wrap with
`textwrap.wrap()` and place lines yourself, or measure first.

## 15. `normAutofit` silently shrinks text

A box carrying `<a:normAutofit fontScale="62500"/>` renders 28 pt text at ~17 pt; the run still
*says* 28 pt, so an audit of run sizes passes. Build boxes with `<a:noAutofit/>` (deck_style `_tx`
does) and let `deck_lint.py` S10 report any `fontScale`.

## 16. Never drive the author's live PowerPoint session

If PowerPoint has the author's file open (check `~$<deck>.pptx`, or ask PowerPoint for its open
presentations), do not open your render copies through it: the AppleScript export can hang behind
a dialog while the author is working, and a stuck app blocks both of you. Use
`scripts/preview_deck.py` for layout checks and do the final PDF export when PowerPoint is idle.
Keynote can export PDF too, but its first launch shows a modal that also hangs automation.

## 17. The sandbox blocks AppleScript and Desktop writes

In a sandboxed shell, `osascript` to PowerPoint fails with "Application isn't running" and writes
to `~/Desktop` fail with `PermissionError: Operation not permitted`. Both need the command re-run
outside the sandbox. Check the deck is byte-identical to its backup after a failed write before
retrying (`cmp`).

## 18. Write only when the deck is closed

Before saving over the author's deck, check for the lock file `~$<deck>.pptx`; re-check immediately
before `prs.save()`. If it appears, stop and build a preview or a one-slide file instead.

## 19. Titles are often split across runs

Setting `runs[0].text` leaves the old year range in `runs[1]` ("…: 1975–2021: 1975–2022").
Write the full text into the first run and blank the rest.

## 20. Rotated text boxes: width is the long side

For `rotation = 270`, python-pptx `width` is the text direction (the long side) and `height` the
thickness. Position by the centre; visual extent is (height × width). Offset a rotated y-axis title
from the axis by a FIXED distance, never by scaling it with the panel.

## 21. Cloning a slide drags its invisible residue along

Deep-copying a two-panel slide and deleting "everything right of x = 9.6" left panel B's rotated
y-axis title behind (its box started left of the cut), and a later remap parked it off the slide.
Delete by panel membership (text, role) and lint S9 (off-slide) before saving.

## 22. Hidden slides shift PDF page numbers

(See 7.) A hidden slide 15 made "page 16" show slide 17. Map pages to slides by title text.

## 23. Legend swatches: use `roundRect`, not flat rectangles

The house swatch is a 0.41 in `roundRect` (adj 0.25). Flat 0.27 × 0.17 in rectangles from the older
module read as spreadsheet chrome and were replaced deck-wide.
