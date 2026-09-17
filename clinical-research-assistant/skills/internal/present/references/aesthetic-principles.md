# Aesthetic principles

Derived from what the author accepted and rejected building a podium deck for a
national surgical/oncology meeting. The audience is surgeons and clinical
researchers; the register is a peer-reviewed journal figure, not a corporate deck.

The single test: **would this figure survive review at JAMA Surgery / Annals of
Surgery?** If it would look out of place there, it is wrong here.

---

## Form

**Rounded borders on bars, always.** Rounded bar ends and forest CI capsules are
the house signature. Square-cornered bars read as spreadsheet output.

**Native shapes for text and geometry; matplotlib only for real charts.** Native
shapes stay editable and re-render crisply on any projector. Reach for a rendered
image when the content genuinely needs a plotting engine — survival curves,
distributions, gradient fills.

**Direct-label the data.** Label curves at their ends, values on their bars. A
legend box inside the plot is four lines of chrome that the eye must reconcile
with the data; direct labels cost nothing.

**The axis is quieter than the data.** Drop the top and right spines; drop the
left spine where a gridline already carries the baseline. Gridlines at ~8% grey,
axis labels muted, tick marks short or absent. The data series should be the
darkest thing in the panel.

**One emphasis point per figure.** A dashed landmark line with a labelled dot, or
a shaded region, or a bracket — one of these, not three.

**Whitespace is not wasted space.** A single large panel beats two cramped ones.
Dropping a co-primary panel to a one-line replication statement is usually a gain:
the surviving panel doubles in size and the replication reads as confirmation
rather than as a second thing to parse.

---

## Typography

Times New Roman throughout, matching the manuscript. Titles black and bold; body
ink `#22333F`; secondary text muted; footnotes at footer grey.

One title per figure, left-aligned, no subtitle block competing with it. A short
subtitle naming the cohort and years is fine; a second declarative sentence is not.

Type scale is coarse on purpose: a hero number can be 40–64 pt while its label sits
at 13–15 pt. Timid contrast reads as indecision.

---

## Colour

Semantic, never decorative. Every hue means one thing in the whole deck.

- Race series follow the project convention (navy = non-Hispanic White,
  red = non-Hispanic Black). **Red is reserved for the disadvantaged group** and may
  not be reused for a registry or category series anywhere a race series appears.
- Registry series: NCDB blue `#007AD1`, SEER orange `#D15600`.
- Sequential emphasis (eras, estimator ladders) uses a tint ramp of one hue that
  darkens into the group of interest.

Recolour by label and region, never by hex — the same hex routinely carries two
meanings in one deck.

Check grayscale luminance separation before changing any pair; these decks get
printed.

---

## Density

**Cut annotation, not data.** When a slide is crowded, the first things to go are
duplicated numbers, in-plot legends, per-panel footnotes, and anything the title
already said. The curves, the at-risk table, and the effect estimate stay.

Numbers belong in one place. If the two-year survival is stated in a panel header,
it does not also belong on the curve and in the caption.

A number rail — hero figure, component values with colour chips, effect estimate,
replication, separated by hairlines — carries more information than an in-plot
annotation block and crowds nothing.

Reviewer-facing detail (caliper widths, FDR method, weighting variants) belongs in
presenter notes and backup slides, not on the slide.

---

## Language

**No editorial voice.** State the finding; do not characterise its importance.

- Yes: "The largest modifiable step identified here is receipt of curative-intent surgery."
- No: "The highest-leverage intervention in this disease."

**No jargon the audience has to decode.** "Model A / Model B" means nothing to a
room of surgeons. Name what was held constant: "clinical factors",
"socioeconomic factors", "propensity matched". Avoid "adjustment" where the
analysis is framed as mediation — ask whether the gap shrinks.

**Titles are declarative and literal.** "Absolute Survival Difference by Race at
Two Years" is right. Anything that sounds like a headline is wrong — and a
declarative title must be *true of the plotted data*: a gap that rises then
narrows cannot be titled "never closes".

Plain words over register vocabulary: "alive at two years", not "achieved the
two-year survival endpoint".

---

## Rejected patterns

Each of these was built, shown, and turned down. Do not re-propose them.

**Box-and-arrow hub diagrams.** A central contrast with explanatory boxes feeding
in reads as a consulting slide. Rejected on sight. For objectives, prefer one
large question, or a PICO table, or both stacked.

**Two co-equal panels where one will do.** The two-panel KM was the most crowded
slide in the deck.

**Censoring ticks drawn per patient at registry scale.** Thousands of distinct
censoring times merge into a solid band along the curve.

**Anything that makes the reader do arithmetic that fails.** 40.0%, 30.2%, and
"9.9-point difference" on one slide invites subtraction and loses.

**Ornament without meaning** — drop shadows, 3-D bars, gradients that encode
nothing, icons as decoration. The one gradient that earned its place encoded the
size of a gap.
