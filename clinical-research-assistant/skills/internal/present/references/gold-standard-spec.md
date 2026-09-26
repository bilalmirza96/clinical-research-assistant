# Gold-standard presentation spec

**Source:** the author's ITSOS 2026 podium deck (`~/Desktop/ITSOS_Mirza.pptx`, 22 slides, 20
visible, 20.00 × 11.25 in), measured slide-by-slide on 2026-09-25 after the author's own declutter
passes. The author named it the gold standard for every future study presentation.

Everything here is **measured**, not invented. `scripts/deck_style.py` implements these tokens and
`scripts/deck_lint.py` enforces them. When this file and a script disagree, the script is the bug.

---

## 1. Canvas and furniture

| Element | Value (inches unless noted) | Notes |
|---|---|---|
| Slide | 20.00 × 11.25 (16:9) | Never 13.33 × 7.5; figures sized for 13.33 in come out a third too small |
| Title box | left 0.938, top 0.729, w 19.938, h 0.706 | top-anchored, `noAutofit`, one line |
| Header rule | 0.938, 1.623, w 18.125, h 0.01, fill `E1E6ED` | under every content-slide title |
| Footer rule | 0.938, 10.286, w 18.125, h 0.01, fill `E1E6ED` | identical on every content slide |
| Content band | y 1.95 → 10.05 | nothing but furniture outside it |
| Side margins | 0.938 left, content right edge 19.063 | |
| Footer legend | first swatch x 0.92, top 10.47; swatch 0.41 × 0.41 `roundRect` adj 0.25 | labels 32 pt, top 10.391, h 0.539 |
| Legend spacing | swatch → label 0.15; label end → next swatch 0.60 | label width = measured text advance |
| Slide numbers | **none** | removed by the author |
| Source line | **none** | provenance lives in the notes archive |

The footer must be **pixel-identical** across slides so it does not jump when advancing. Race legends
and category legends use the same geometry.

## 2. Type

| Role | Size | Weight | Colour |
|---|---|---|---|
| Slide title | 43.5 pt | bold | black `000000` |
| **Everything in the body** (labels, ticks, axis titles, values, estimates, P values, annotations) | **28 pt** | regular | black |
| Footer legend labels | 32 pt | regular | black |
| Numbered conclusions / disclosures body | 32–36 pt | regular | black |
| Title-slide title | 66 pt | bold | white on navy |
| Title-slide authors / affiliation | 32 pt | regular | white |
| Closing "Thank you" | 148 pt | regular | navy `1A3255` |

- **Times New Roman on every run.** No other face anywhere.
- **Floor: 28 pt.** No annotation, footnote, interaction P or axis tick goes below it. The author's
  words: *"text size bigger to 28 … plots in the center … as little text as possible."*
- **Black text only.** No grey text (author: *"do not use grey color for text, replace all that
  grey with black"*). Grey is for lines: gridlines `E9ECF0`, rules `E1E6ED`, axis baselines and
  arrow shafts `6B7280`.
- **White text** only on a dark fill (bars, the last analytic step, the title slide).
- **Bold** only for titles and for structural labels: table row/column headers, step headings
  on the analytic-approach ladder, forest group headings. These structural labels may be navy
  `1A3255`. Never bold a value, estimate, P value, axis label or legend.
- En dash for ranges and CIs (`0.57 (0.53–0.62)`, `2010–2023`). No em dashes on slides.
- P values: `P<.001`, `P=.02` (no leading zero, no space).

## 3. Colour tokens (semantic, one meaning each)

| Token | Hex | Meaning |
|---|---|---|
| NHW | `123057` | non-Hispanic White (reference group), everywhere |
| NHB | `801819` | non-Hispanic Black, **reserved**: red never encodes a category |
| NAVY_TXT | `1A3255` | title-slide background, structural labels, closing text |
| MARKER | `000000` | forest points and CI bars (author: *"instead of light blue, just make it black"*) |
| GRID | `E9ECF0` | gridlines |
| RULE | `E1E6ED` | header/footer rules |
| AXIS | `6B7280` | baselines, arrow shafts (lines only) |
| BAND | `D9E0EF` | CI band behind a trend line |
| POINT | `4B5563` | observed yearly points on a trend chart (a fill, not text) |
| ACCENT | `007AD1` | single-series accent (E-value curve and markers) |
| STEP_RAMP | `EDF1F7 → DCE5F0 → C9D6E8 → 123057` | analytic-approach ladder; last step inverted |
| PAL_MODALITY | `0D1A2C, 2C4E74, 54121C, C4A2A8` | 4-level treatment modality |
| PAL_BLUES | `1B263B, 415A77, 778DA9, E0E1DD` | 4-level category (reason for no surgery) |
| PAL_GREYS | `C5CDD8, 63666A` | two-level non-race comparison (adjusted gap vs mediated part) |

Category palettes are the author's picks from supplied swatches. When the author supplies a palette,
sample the exact hexes, drop a shade that is indistinguishable from its neighbour (tell the author
which and why), and keep the darkest shade for the dominant category.

## 4. Slide archetypes (the 20 slides, in talk order)

| # | Archetype | Build rule |
|---|---|---|
| 1 | **Title** | full-bleed navy `1A3255` background with institutional watermark art at right; 66 pt bold white title centred; authors 32 pt white; department / institution 32 pt white. Pictures allowed (branding). |
| 2 | **Disclosures** | title + two plain lines, 36 pt. Nothing else. |
| 3 | **Trend** | yearly points (0.10 in `4B5563` dots), 95% CI band (`D9E0EF` polygon), modelled trend (navy segments), rotated y title, decade x ticks. Same time horizon as the rest of the talk (two-year survival here, to match the KM slides). |
| 4 | **Data sources table** | column heads = registries (navy bold), row heads = Design and era / Patients / Outcomes analyzed (navy bold), values black 28 pt centred, hairline row rules. No borders, no fills. |
| 5 | **Analytic approach ladder** | four full-width rounded boxes (h 1.22, pitch 2.22) on a light → dark ramp; number + bold heading + one plain line; small dark triangles between; final (primary) step inverted navy with white text. |
| 6 | **Two-panel KM** | native step polylines (open custGeom), NCDB OS left / SEER CSS right; grey landmark line at 24 months with a filled dot on each curve; "Log-rank P<.001" top-right; panel headers plain 28 pt; legend in footer; no at-risk table on the podium version. |
| 7 | **Estimator forest** | two outcome groups (navy bold headings), rows Unadjusted / Adjusted / Propensity matched; black markers; dotted null; log-symmetric ticks (0.67, 0.8, 1, 1.25, 1.5); estimates right; two-sided arrow labels below ("Black patients have better survival ← | → worse survival"). |
| 8 | **Grouped bars by stage** | race pair per stage, top-rounded bars; one statistic per pair above it ("HR 1.33, P<.001"); interaction P top-right; legend in footer. |
| 9–12 | **Bars + forest two-panel** | left: race bars with one P above each pair; right: forest with header ("Odds ratio, Black vs White"), estimate + P on two lines at right, "← Less likely in Black patients" below. Both panels share one baseline y. |
| 13 | **Stacked composition (2 rows)** | 1.93 in rows, rounded outer ends, in-segment labels where they fit (white on dark, black on light), tick + callout below small segments, splayed apart when adjacent; chi-square P top-right; category legend in footer. |
| 14 | **Stacked composition (4 rows)** | same grammar, stage × race rows. |
| 15 | **Single-panel KM** | one wide panel (x 4.55 → 16.55); statistic top-right is the ADJUSTED HR when that is the claim. |
| 16 | **Mediation bars** | two-level grey bars (total adjusted gap vs part through surgery) with error bars; "51% mediated (36–65%), P<.001" above each pair. |
| 17 | **E-value** | left: bias curve with shaded region and the labelled E-value point; right: E-value forest by registry and model (navy bold group labels). |
| 18 | **Conclusions** | numbered list, 32 pt, three items, faint watermark art; title in navy. |
| 19 | **Thank you** | 148 pt navy centred; institutional logos. |

Backup slides are **hidden** (`show="0"`) at the end, never deleted: the author keeps them for Q&A.

## 5. Chart grammar

- **Bars**: `round2SameRect` (top corners rounded, adj 0.08), no outline, race colours, pair gap
  0.10 in. **No per-bar value labels** when a pair statistic is shown: one number per comparison.
- **Forest**: point 0.20 in black oval; CI 0.035 in black bar; null line **dotted** black
  (`ROUND_DOT`), faint vertical gridlines; log scale; estimate text right of the plot, P on the
  next line; header text above; arrow label below. The y "spine" of a forest is dotted, never solid.
- **Two-panel alignment**: when bars and a forest share a slide, align their x baselines on one y
  and centre the forest header over its plot. Panel B starts at x 10.43.
- **KM**: 2.5 pt step lines, landmark 1 pt `B8C0CC`, 0.15 in dots at the landmark, 0–100 in 20s,
  months 0–60 in 12s, statistic top-right, legend in footer (never inside the plot).
- **Stacked**: segment labels `%.1f%%`; do not print a label into a segment it cannot fit.
- **Annotations** ("Chi-square P<.001", "Race × stage interaction P<.001") are 28 pt black
  one-liners, right-aligned to the content edge under the header rule, or in the footer band right
  of the legend.
- **Tick labels** vertically centred on their gridline (middle anchor), never hanging below it.

## 6. Presenter-note style (measured)

- 20–100 words per slide; ~130 words per talk minute (7-minute talk ≈ 800–950 words).
- 1–3 short paragraphs, blank line between.
- The first sentence is a transition or question that hands off from the previous slide
  ("We then asked…", "To understand why…", "To quantify this…", "Having observed…").
- Whole-number percentages; differences in **percentage points**; no decimals.
- Full detail is in `references/story-and-notes.md`.

## 7. Known deviations in the gold deck itself (2026-09-25 lint)

`deck_lint.py` on the gold deck reports five FAILs. They are author decisions to confirm, not
patterns to copy:

1. Slide 7 "All P<.001" at 24 pt (floor is 28).
2. Slide 12 "Race × stage interaction P=.01" at 24 pt.
3. Slide 4 note calls NCDB "population database" (NCDB is hospital-based).
4. Slide 8 note opens with "Furthermore" (banned transition).
5. Slide 15 carries a leftover rotated "Cancer-specific survival (%)" label parked off the right
   edge (residue of cloning the two-panel KM slide into a one-panel slide).

When you build from this spec, none of these may appear.
