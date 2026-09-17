# Slide patterns

Layouts proven on a real podium deck (20 × 11.25 in). Geometry in inches.
Figure panels are rendered at 13.33 × 7.5 in (same 16:9) and placed full-bleed.

Common furniture: title at (0.94, 0.73), title rule at y = 1.62, footer rule at
y = 10.31, footer caption at y = 10.46, page number right-aligned at x ≈ 19.06.
Body lives between the rules.

---

## Data-sources table

Native PowerPoint table, one column per cohort, rows for design/era, N, outcomes,
role. Label column ~3.3 in; data columns split the rest. Accent bar (1.25 × 0.06)
in the registry colour above each column header; hairline `RULE` under the header
and between rows; no fills, no banding.

Better than side-by-side cards: the reader compares *across* cohorts on one row
instead of re-reading three parallel blocks. Use `deck_style.plain_table()`.

## Era / category blocks

Equal-width rounded rectangles with a shading ramp that darkens into the era of
interest, year range inside, one-word descriptor beneath, and a caret callout
above the emphasised block.

Equal width reads as a categorical split; width-proportional-to-duration reads as
a timeline. Pick deliberately and say which in the footer, because equal blocks
silently discard the duration information.

## Estimator ladder

Stacked full-width rows, one per estimator (unadjusted → clinical → socioeconomic
→ propensity matched), shading escalating into the last, caret between rows.
Row height 1.38, pitch 1.70, number at x + 0.20, label at x + 1.31, gloss below.

Strong because it becomes the legend for every forest plot that follows — the
audience learns three or four rows once and reads them repeatedly.

Name estimators in plain language. Avoid "Model A / Model B"; the SAP framing for
the socioeconomic layer is usually mediation ("does the gap shrink?"), not a
second adjustment.

## Forest plot, log-symmetric axis

Measured axis from a real deck: null at x = 11.05 in, 7.40 in per log unit, so
`X(v) = 11.05 + 7.40 * log(v)`. Ticks at 0.67 / 0.8 / 1 / 1.25 / 1.5.

Direction arrows: a rectangle shaft plus a triangle head, filled in the chart's
own null-rule colour at the null rule's weight — connector arrowheads never match
the rest of the figure. Interior vs edge nulls need different arrow logic:

```python
interior = (gl + 0.35 < nx < gr - 0.35)
```

One shared lead line for the BETTER/WORSE labels. Per-arrow lead lines overflow:
a 4.0 in label box on a 2 in axis half collides with its neighbour.

Hollow markers carry colour on the **outline**, filled markers on the **fill** —
a recolour pass must handle both, plus text runs.

## Kaplan-Meier, hero treatment

Single panel, curve on the left ~55%, a number rail on the right separated by
hairlines: absolute difference as the hero figure, the two survival percentages
with colour chips, the adjusted HR, then the replication cohort at footnote
weight.

The gap between curves is filled with a **vertical gradient wedge** (imshow
clipped to the polygon between the curves) so the disparity is an object rather
than an inference. Nothing is written over the data; the axis is quieter than the
curves (no left spine, 8% grey gridlines, muted labels).

Day resolution: if follow-up is day-resolved, step at every event time rather than
a monthly grid. Sampling resolution does not move the estimate — verify that the
landmark values are unchanged before and after.

## Kaplan-Meier, survminer idiom

When the author wants the familiar `ggsurvplot` look: top-centre legend with `+`
glyphs, confidence ribbons, censoring ticks, dashed median drop-lines, log-rank
annotation inside the panel, survival probability on 0.0–1.0, and a
"Number at risk (number censored)" table with colour swatches.

**Censoring ticks cannot be one-per-patient at registry scale** — thousands of
distinct censoring times merge into a solid band. Place one tick per month in
which censoring occurred and say so in the footnote, or the figure implies 60
censored patients when the truth is thousands.

Confidence ribbons are invisible at n ≈ 90,000 and visible at n ≈ 8,700. That
asymmetry is honest but earns little; mention it rather than letting it read as a
rendering failure.

## Icon array

Two 10 × 10 grids of circles, filled to the rounded percentage. Draw in an axes
with `set_aspect("equal")`. Footnote must state that icons are proportions
rounded to whole patients, not individual patients — the real denominators are
orders of magnitude larger.

Best audience comprehension of any survival display; weakest technically. Works
for one or two outcomes side by side.

## Dumbbell

Two dots joined by a line, one row per cohort, value printed inside each dot.
Makes the gap a physical length. Loses the time axis entirely — pair it with a
spoken "at two years".

## Gap-over-time

Plot the difference (reference minus comparison) against time, one line per
cohort. The gap *is* the line.

Check the shape before titling it. A gap that rises and then narrows must not be
captioned "never closes" — that convergence is partly the mechanical effect of
both curves approaching zero, and someone in the audience will notice.

## Study-question divider

Eyebrow label, one large question, two supporting lines beneath. Works on white
or on a navy ground; to convert, drop the slide-level `<p:bg>` override and remap
every run (`deck_style.set_white_background`).
