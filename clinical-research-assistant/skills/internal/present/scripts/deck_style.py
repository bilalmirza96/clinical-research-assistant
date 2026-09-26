"""
CRA conference-deck design system -- GOLD STANDARD v2 (2026-09-25).

Every token below was measured off the author's gold-standard deck
(ITSOS 2026, `ITSOS_Mirza.pptx`, 20 x 11.25 in, 16:9) after the author's own
declutter passes. Slides built with this module match that deck; `deck_lint.py`
fails any slide that drifts from it. Read references/gold-standard-spec.md for the
measured spec and the reasoning behind each rule.

Non-negotiables baked into the defaults (author directives, 2026-09-22..25):
  * Times New Roman everywhere; every run >= 28 pt (legends 32 pt, titles 43.5 pt bold).
  * Text is BLACK. No grey text anywhere (grey is for lines/gridlines only).
    White only on a dark fill. Navy 1A3255 only for structural labels (table
    headers, forest group labels) and title-slide / closing text.
  * No bold inside the slide body except structural labels; titles are bold.
  * No slide numbers, no source line, no in-plot legend boxes. The race legend
    lives in the footer band, identical on every slide (rounded 0.41 in swatches).
  * Native PowerPoint shapes; pictures only for branding (logos, watermark).

PALETTE NOTE: race series NHW = navy 123057, NHB = dark red 801819 (red is RESERVED
for the disadvantaged group). Category palettes below are author-chosen per slide
family; never reuse the race red for a category.
"""
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE
from lxml import etree
import copy, math, os

FONT = "Times New Roman"
_A = "http://schemas.openxmlformats.org/drawingml/2006/main"

# ---- palette (measured off the gold deck) -----------------------------------
BLACK    = RGBColor(0x00, 0x00, 0x00)   # ALL body text
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)   # text on dark fills only
NAVY_TXT = RGBColor(0x1A, 0x32, 0x55)   # structural labels, title-slide background, closing text
NHW      = RGBColor(0x12, 0x30, 0x57)   # race: non-Hispanic White (navy)
NHB      = RGBColor(0x80, 0x18, 0x19)   # race: non-Hispanic Black (dark red) -- RESERVED
GRID     = RGBColor(0xE9, 0xEC, 0xF0)   # gridlines
RULE     = RGBColor(0xE1, 0xE6, 0xED)   # header + footer rules
AXIS     = RGBColor(0x6B, 0x72, 0x80)   # axis baselines, arrow shafts (LINES ONLY, never text)
MARKER   = BLACK                        # forest point + CI (author: "make it black")
BAND     = RGBColor(0xD9, 0xE0, 0xEF)   # CI band behind a trend line
POINT    = RGBColor(0x4B, 0x55, 0x63)   # observed points on a trend chart (fill, not text)
ACCENT   = RGBColor(0x00, 0x7A, 0xD1)   # single-series accent (E-value slide)
# steps ramp (analytic approach): light -> dark, last step inverted
STEP_RAMP = [RGBColor(0xED, 0xF1, 0xF7), RGBColor(0xDC, 0xE5, 0xF0), RGBColor(0xC9, 0xD6, 0xE8), NHW]
# 4-level categorical palettes the author picked (keep the ROLE, swap hexes only on request)
PAL_MODALITY = [RGBColor(0x0D, 0x1A, 0x2C), RGBColor(0x2C, 0x4E, 0x74), RGBColor(0x54, 0x12, 0x1C), RGBColor(0xC4, 0xA2, 0xA8)]
PAL_BLUES    = [RGBColor(0x1B, 0x26, 0x3B), RGBColor(0x41, 0x5A, 0x77), RGBColor(0x77, 0x8D, 0xA9), RGBColor(0xE0, 0xE1, 0xDD)]
PAL_GREYS    = [RGBColor(0xC5, 0xCD, 0xD8), RGBColor(0x63, 0x66, 0x6A)]   # e.g. "adjusted gap" vs "through surgery"
# legacy names kept so older scripts import cleanly (all TEXT roles now resolve to black)
INK = BLACK; MUTED = BLACK; FOOT = BLACK
ALT = RGBColor(0x51, 0x80, 0xBF); NCDB_BLUE = ACCENT; SEER_ORANGE = RGBColor(0xD1, 0x56, 0x00)
PALE = RGBColor(0xC5, 0xCD, 0xD8)

# ---- type scale (measured) --------------------------------------------------
SZ_MIN = 28.0                       # hard floor, enforced by deck_lint.py
SZ_TITLE = 43.5                     # slide title, bold, black
SZ_BODY = 28.0                      # every label, tick, value, estimate, annotation
SZ_LEGEND = 32.0                    # footer legend labels
SZ_TS_TITLE = 66.0; SZ_TS_BODY = 32.0   # title slide
SZ_LIST = 32.0                      # numbered conclusions / disclosures body
SZ_CLOSING = 148.0                  # "Thank you"
# legacy aliases -> all at or above the floor
SZ_PANEL = SZ_VALUE = SZ_CAT = SZ_AXIS = SZ_EST = SZ_SUB = SZ_SRC = SZ_BODY
LINE_H = 0.50                       # height of a one-line 28 pt box (in)

# ---- canonical geometry (measured, inches) ----------------------------------
SLIDE_W, SLIDE_H = 20.0, 11.25
MARGIN_L = 0.938; CONTENT_W = 18.125; MARGIN_R = MARGIN_L + CONTENT_W      # 19.063
TITLE = (0.938, 0.729, 19.938, 0.706)          # top-anchored, noAutofit
TITLE_RULE = (0.938, 1.623, 18.125, 0.01)
FOOT_RULE = (0.938, 10.286, 18.125, 0.01)
BODY_TOP, BODY_BOTTOM = 1.95, 10.05            # content band between the rules
# footer legend (identical on every slide)
LEG_X0 = 0.92; LEG_SW = 0.41; LEG_SW_TOP = 10.47; LEG_TXT_TOP = 10.391; LEG_TXT_H = 0.539
LEG_GAP_S = 0.15; LEG_GAP_L = 0.60; LEG_ADJ = 0.25
# two-panel layout (bars left, forest right) -- panel B starts at the slide midline
PANEL_A_X = 0.938; PANEL_B_X = 10.43
# left bar panel / right forest panel defaults
BAR_X0 = 2.45; BAR_W = 6.1; BAR_BASE = 8.25; BAR_TOP = 3.60; BARW = 0.95
FOR_X0 = 12.25; FOR_X1 = 15.75; FOR_LBL = 16.35; FOR_TOP = 4.10; FOR_DY = 1.45
STK_X0 = 3.40; STK_W = 15.30; STK_H = 1.93
PGNUM = SRC = None                  # removed: no slide numbers, no source line


def _tx(slide, l, t, w, h, text, size=SZ_BODY, color=BLACK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, wrap=True, italic=False):
    """Text box: zero insets, explicit size, no autofit (normAutofit shrinks 28 pt to ~17 pt)."""
    b = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    bp = tf._txBody.find("{%s}bodyPr" % _A)
    for c in list(bp):
        if c.tag.endswith("Autofit") or c.tag.endswith("AutoFit"): bp.remove(c)
    etree.SubElement(bp, "{%s}noAutofit" % _A)
    for i, line in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
        f = r.font; f.name = FONT; f.size = Pt(max(size, SZ_MIN) if size < 40 else size)
        f.bold = bold; f.italic = italic; f.color.rgb = color
    return b


def _rect(slide, l, t, w, h, color, shape=MSO_SHAPE.RECTANGLE, adj=None, outline=False):
    s = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = color
    if not outline: s.line.fill.background()
    s.shadow.inherit = False
    if adj is not None:
        try: s.adjustments[0] = adj
        except Exception: pass
    return s


def _line(slide, x1, y1, x2, y2, color=AXIS, pt=1.0, dash=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(pt)
    if dash is not None: c.line.dash_style = dash
    return c


def text_width_in(text, size=SZ_BODY, typeface=FONT):
    """Advance width of `text` in inches (fontTools); falls back to 0.5 em per character."""
    try:
        from fontTools.ttLib import TTFont
        path = next((p for p in ("/System/Library/Fonts/Supplemental/%s.ttf" % typeface,
                                 "/Library/Fonts/%s.ttf" % typeface,
                                 os.path.expanduser("~/Library/Fonts/%s.ttf" % typeface)) if os.path.exists(p)), None)
        f = TTFont(path); cmap = f.getBestCmap(); hm = f["hmtx"]; upm = f["head"].unitsPerEm
        return sum(hm[cmap.get(ord(c), cmap[ord("n")])][0] for c in text) / upm * size / 72
    except Exception:
        return 0.5 * len(text) * size / 72


# ---- slide furniture ----------------------------------------------------------
def title(slide, text):
    return _tx(slide, *TITLE, text, SZ_TITLE, BLACK, bold=True)


def legend(slide, items, x0=LEG_X0):
    """Footer legend: [(label, RGBColor), ...]. Rounded 0.41 in swatches, 32 pt black labels,
    first swatch at x 0.92 in, 0.15 in swatch->label, 0.60 in label->next swatch.
    Identical geometry on every slide so the footer never jumps between slides."""
    x = x0
    for lab, col in items:
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(LEG_SW_TOP),
                                   Inches(LEG_SW), Inches(LEG_SW))
        s.adjustments[0] = LEG_ADJ; s.fill.solid(); s.fill.fore_color.rgb = col; s.shadow.inherit = False
        x += LEG_SW + LEG_GAP_S
        w = text_width_in(lab, SZ_LEGEND) + 0.04
        _tx(slide, x, LEG_TXT_TOP, w, LEG_TXT_H, lab, SZ_LEGEND, BLACK, wrap=False)
        x += w + LEG_GAP_L
    return x - LEG_GAP_L


RACE_LEGEND = [("Non-Hispanic White", NHW), ("Non-Hispanic Black", NHB)]
_draw_legend = legend   # frame() takes a `legend=` kwarg that shadows the function name


def frame(slide, title_text, source=None, pagenum=None, legend_items=None, legend=None):
    """Title + header rule + footer rule (+ optional footer legend).
    `source` / `pagenum` are accepted for old callers and IGNORED: the house deck carries no
    slide numbers and no source line (provenance lives in the notes archive)."""
    title(slide, title_text)
    _rect(slide, *TITLE_RULE, RULE)
    _rect(slide, *FOOT_RULE, RULE)
    items = legend_items or legend
    if items:
        _draw_legend(slide, items)
    return slide


def panel_header(slide, text, x, y=2.05, w=8.6, align=PP_ALIGN.CENTER):
    """Plain 28 pt black panel header ("Overall survival (NCDB)"), no letter, no bold."""
    return _tx(slide, x, y, w, LINE_H, text, SZ_BODY, BLACK, align=align)


# ---- bars -----------------------------------------------------------------------
def grouped_bars(slide, groups, ymax, ylab, x0=BAR_X0, w=BAR_W, base=BAR_BASE, top=BAR_TOP,
                 ticks=None, p_labels=None, value_fmt=None, k_gap=0.10, barw=BARW):
    """groups = [(label, [(value, color), ...]), ...]. Top-rounded bars (round2SameRect adj 0.08).
    p_labels: one string per group ("P<.001", "HR 1.33, P<.001") centred above the pair --
    the house replaces per-bar value labels with ONE comparison statistic per pair.
    value_fmt: optional per-bar value label (off by default)."""
    span = base - top; scale = span / ymax
    ticks = ticks if ticks is not None else [0, ymax / 4, ymax / 2, 3 * ymax / 4, ymax]
    for tv in ticks:
        y = base - tv * scale
        if tv: _rect(slide, x0, y, w, 0.01, GRID)
        _tx(slide, x0 - 0.95, y - 0.25, 0.80, LINE_H, "%g" % tv, SZ_BODY, BLACK,
            align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    _rect(slide, x0, base - 0.02, w, 0.03, AXIS)
    yl = _tx(slide, 0, 0, top - base + 2 * (base - top), LINE_H, ylab, SZ_BODY, BLACK,
             align=PP_ALIGN.CENTER, wrap=False)
    yl.width = Inches(base - top + 0.6); yl.rotation = 270
    yl.left = Inches(x0 - 1.30 - (base - top + 0.6) / 2); yl.top = Inches((top + base) / 2 - LINE_H / 2)
    n = len(groups); gw = w / n
    for gi, (glab, bars) in enumerate(groups):
        gc = x0 + gw * (gi + 0.5); k = len(bars)
        tot = k * barw + (k - 1) * k_gap; bx = gc - tot / 2; hmax = 0
        for val, col in bars:
            h = val * scale; hmax = max(hmax, h)
            _rect(slide, bx, base - h, barw, h, col, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, adj=0.08)
            if value_fmt:
                _tx(slide, bx + barw / 2 - 0.7, base - h - 0.55, 1.4, LINE_H, value_fmt.format(val),
                    SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
            bx += barw + k_gap
        if p_labels and p_labels[gi]:
            _tx(slide, gc - 1.6, base - hmax - (1.05 if value_fmt else 0.62), 3.2, LINE_H, p_labels[gi],
                SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
        _tx(slide, gc - gw / 2, base + 0.15, gw, LINE_H, glab, SZ_BODY, BLACK, align=PP_ALIGN.CENTER)


# ---- forest ---------------------------------------------------------------------
def forest(slide, rows, xmin, xmax, ticks, axis_label=None, x0=FOR_X0, x1=FOR_X1, top=FOR_TOP,
           dy=FOR_DY, null=1.0, lbl_x=FOR_LBL, lbl_w=3.6, cat_w=3.2, header=None, arrow_text=None,
           log=True, color=MARKER):
    """rows = [(label, point, lo, hi, estimate_text, sub_text), ...]  (a 7th colour item is accepted
    and ignored -- markers are black by house rule). Log-scaled x by default.
    Layout (measured): black 0.20 in marker, 0.035 in CI bar, DOTTED null line, faint gridlines,
    estimate "0.73 (0.65–0.81)" right of the plot with the P value on the line beneath it,
    optional header above ("Odds ratio, Black vs White") and a one-sided arrow label below
    ("← Less likely in Black patients"). Returns the y of the lowest element."""
    f = (lambda v: math.log(v)) if log else (lambda v: v)
    sc = (x1 - x0) / (f(xmax) - f(xmin)); px = lambda v: x0 + (f(v) - f(xmin)) * sc
    last = top + dy * (len(rows) - 1); gtop = top - 0.55; gbot = last + 0.65
    if header:
        _tx(slide, x0 - cat_w - 0.25, gtop - 0.75, (x1 - x0) + cat_w + 0.25 + 1.0, LINE_H, header,
            SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
    for tv in ticks:
        x = px(tv)
        if abs(tv - null) > 1e-9: _rect(slide, x, gtop, 0.01, gbot - gtop, GRID)
        _tx(slide, x - 0.45, gbot + 0.08, 0.90, LINE_H, "%g" % tv, SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
    if xmin <= null <= xmax:
        _line(slide, px(null), gtop, px(null), gbot, BLACK, 1.25, MSO_LINE.ROUND_DOT)
    for i, row in enumerate(rows):
        lab, pt, lo, hi, est, sub = row[:6]
        y = top + i * dy
        _tx(slide, x0 - cat_w - 0.25, y - 0.25, cat_w, LINE_H, lab, SZ_BODY, BLACK,
            align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
        xl, xh = px(max(lo, xmin)), px(min(hi, xmax))
        _rect(slide, xl, y - 0.0175, max(xh - xl, 0.02), 0.035, color)
        _rect(slide, px(pt) - 0.10, y - 0.10, 0.20, 0.20, color, MSO_SHAPE.OVAL)
        _tx(slide, lbl_x, y - 0.27, lbl_w, LINE_H, est, SZ_BODY, BLACK, wrap=False)
        if sub: _tx(slide, lbl_x, y + 0.20, lbl_w, LINE_H, sub, SZ_BODY, BLACK, wrap=False)
    low = gbot + 0.08 + LINE_H
    if axis_label:
        _tx(slide, x0, low, x1 - x0, LINE_H, axis_label, SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
        low += LINE_H
    if arrow_text:
        a = _line(slide, x0 + 0.05, low + 0.28, x0 + 0.75, low + 0.28, AXIS, 1.25)
        etree.SubElement(a.line._get_or_add_ln(), "{%s}headEnd" % _A).set("type", "triangle")   # arrow points left
        _tx(slide, x0 + 0.90, low + 0.03, 6.0, LINE_H, arrow_text, SZ_BODY, BLACK, wrap=False)
        low += LINE_H
    return low


def forest_log(slide, rows, axis_label, x0, x1, top, dy, lbl_x, lbl_w=3.6, cat_w=3.2, grid_top=None,
               note_text=None, tick_fmt=None):
    """Log-symmetric ratio forest (null centred, mirror ticks). Delegates to forest()."""
    vals = [v for r in rows for v in r[1:4]]
    lo_x, hi_x, ticks = sym_axis(vals)
    return forest(slide, rows, lo_x, hi_x, ticks, axis_label, x0=x0, x1=x1, top=top, dy=dy,
                  lbl_x=lbl_x, lbl_w=lbl_w, cat_w=cat_w, arrow_text=note_text)


# ---- stacked composition bars ---------------------------------------------------
def _readable_on(bg):
    lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
    return BLACK if lum > 150 else WHITE


def stacked_rows(slide, rows, segments, y0=2.81, dy=2.77, label_x=0.60, label_w=2.55,
                 x0=STK_X0, w=STK_W, h=STK_H, callout_min_w=1.10):
    """rows = [(label, [pct, ...]), ...] summing to 100; segments = [(name, RGBColor), ...].
    Measured on the gold 'Documented Reason' slide: two rows, 1.93 in tall, rounded outer ends.
    Values print INSIDE a segment when it is wide enough (white on dark, black on light);
    narrower segments get a tick + callout below the bar instead of being dropped."""
    for ri, (lab, vals) in enumerate(rows):
        y = y0 + ri * dy
        _tx(slide, label_x, y + h / 2 - LINE_H / 2, label_w, LINE_H, lab, SZ_BODY, BLACK,
            align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
        x = x0; calls = []
        for si, v in enumerate(vals):
            sw = w * v / 100.0; col = segments[si][1]
            shp = MSO_SHAPE.RECTANGLE if 0 < si < len(vals) - 1 else MSO_SHAPE.ROUNDED_RECTANGLE
            _rect(slide, x, y, max(sw - 0.02, 0.01), h, col, shp, adj=0.08 if shp != MSO_SHAPE.RECTANGLE else None)
            if sw >= callout_min_w:
                _tx(slide, x, y + h / 2 - LINE_H / 2, sw, LINE_H, "%.1f%%" % v, SZ_BODY, _readable_on(col),
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
            elif v >= 1.0:
                calls.append((x + sw / 2, v))
            x += sw
        # callouts: tick under the segment, label beneath. Neighbours closer than 1.4 in are
        # splayed apart (left one right-aligned to its tick, right one left-aligned) so two small
        # adjacent segments never print "5.0%5.8%".
        for k, (cx, v) in enumerate(calls):
            _line(slide, cx, y + h + 0.03, cx, y + h + 0.18, AXIS, 1.0)
            near_next = k + 1 < len(calls) and calls[k + 1][0] - cx < 1.4
            near_prev = k > 0 and cx - calls[k - 1][0] < 1.4
            if near_next:
                _tx(slide, cx + 0.15 - 1.4, y + h + 0.20, 1.4, LINE_H, "%.1f%%" % v, SZ_BODY, BLACK, align=PP_ALIGN.RIGHT, wrap=False)
            elif near_prev:
                _tx(slide, cx - 0.15, y + h + 0.20, 1.4, LINE_H, "%.1f%%" % v, SZ_BODY, BLACK, align=PP_ALIGN.LEFT, wrap=False)
            else:
                _tx(slide, cx - 0.7, y + h + 0.20, 1.4, LINE_H, "%.1f%%" % v, SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
    return y0 + dy * len(rows)


def segment_legend(slide, segments, y=None, x0=LEG_X0):
    """Category legend in the footer band -- same geometry as the race legend."""
    return legend(slide, segments, x0=x0)


def note(slide, text, l=10.43, t=8.38, w=8.6, h=LINE_H, color=BLACK, size=SZ_BODY, bold=False,
         align=PP_ALIGN.LEFT):
    """One-line annotation ("Chi-square P<.001", "Race × stage interaction P<.001"): 28 pt black."""
    return _tx(slide, l, t, w, h, text, max(size, SZ_MIN), color, bold=bold, align=align)


# ---- open polyline (KM curves, trend lines) ---------------------------------------
def polyline(slide, pts, color, pt=2.5, name="curve", dash=None):
    """ONE freeform shape carrying an OPEN custGeom path (fill="none", no <a:close/>).
    add_freeform closes and fills the path -- wrong for a survival curve."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0_, y0_ = min(xs), min(ys); w = max(max(xs) - x0_, 1e-4); h = max(max(ys) - y0_, 1e-4)
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0_), Inches(y0_), Inches(w), Inches(h))
    sh.name = name; sh.shadow.inherit = False
    spPr = sh._element.spPr
    for g in spPr.findall("{%s}prstGeom" % _A): spPr.remove(g)
    cust = etree.Element("{%s}custGeom" % _A)
    for t_ in ("avLst", "gdLst", "ahLst", "cxnLst"): etree.SubElement(cust, "{%s}%s" % (_A, t_))
    path = etree.SubElement(etree.SubElement(cust, "{%s}pathLst" % _A), "{%s}path" % _A,
                            {"w": str(int(Inches(w))), "h": str(int(Inches(h))), "fill": "none"})
    for i, (px_, py_) in enumerate(pts):
        n = etree.SubElement(path, "{%s}%s" % (_A, "moveTo" if i == 0 else "lnTo"))
        etree.SubElement(n, "{%s}pt" % _A, {"x": str(int(Inches(px_ - x0_))), "y": str(int(Inches(py_ - y0_)))})
    spPr.insert(list(spPr).index(spPr.find("{%s}xfrm" % _A)) + 1, cust)
    sh.fill.background(); sh.line.color.rgb = color; sh.line.width = Pt(pt)
    if dash is not None: sh.line.dash_style = dash
    return sh


def km_panel(slide, curves, x0, x1, top, bot, header=None, ylab="Overall survival (%)", tmax=60,
             tstep=12, landmark=24, stat_text=None):
    """Native Kaplan-Meier panel. curves = [(months_list, surv_frac_list, RGBColor), ...] (step data).
    House look: 0-100 y axis in steps of 20 (28 pt ticks), months 0..tmax in steps of 12, faint
    gridlines, thin vertical landmark line at 24 months with a filled dot on each curve,
    statistic (log-rank P or adjusted HR) at top-right, no in-plot legend (legend in footer)."""
    fx = lambda t: x0 + (x1 - x0) * t / tmax; fy = lambda s: bot - (bot - top) * s / 100.0
    for v in range(0, 101, 20):
        if v: _rect(slide, x0, fy(v), x1 - x0, 0.01, GRID)
        _tx(slide, x0 - 0.95, fy(v) - 0.25, 0.80, LINE_H, str(v), SZ_BODY, BLACK, align=PP_ALIGN.RIGHT,
            anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    _rect(slide, x0, bot - 0.01, x1 - x0, 0.02, AXIS); _rect(slide, x0 - 0.01, top, 0.02, bot - top, AXIS)
    for t in range(0, tmax + 1, tstep):
        _tx(slide, fx(t) - 0.6, bot + 0.10, 1.2, LINE_H, str(t), SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
    _tx(slide, x0, bot + 0.62, x1 - x0, LINE_H, "Months from diagnosis", SZ_BODY, BLACK, align=PP_ALIGN.CENTER)
    yl = _tx(slide, 0, 0, bot - top, LINE_H, ylab, SZ_BODY, BLACK, align=PP_ALIGN.CENTER, wrap=False)
    yl.rotation = 270; yl.left = Inches(x0 - 1.25 - (bot - top) / 2); yl.top = Inches((top + bot) / 2 - LINE_H / 2)
    if landmark: _line(slide, fx(landmark), top, fx(landmark), bot, RGBColor(0xB8, 0xC0, 0xCC), 1.0)
    for ts, ss, col in curves:
        S = [100 * s for s in ss]; pts = [(fx(ts[0]), fy(S[0]))]
        for i in range(1, len(ts)):
            if ts[i] > tmax: break
            pts += [(fx(ts[i]), fy(S[i - 1])), (fx(ts[i]), fy(S[i]))]
        polyline(slide, pts, col, 2.5)
        if landmark:
            k = max(i for i, t in enumerate(ts) if t <= landmark)
            _rect(slide, fx(landmark) - 0.075, fy(S[k]) - 0.075, 0.15, 0.15, col, MSO_SHAPE.OVAL)
    if header: panel_header(slide, header, x0 - 0.5, top - 0.95, x1 - x0 + 1.0)
    if stat_text: _tx(slide, x1 - 7.0, top + 0.35, 7.0, LINE_H, stat_text, SZ_BODY, BLACK, align=PP_ALIGN.RIGHT)


# ---- text-led slides -----------------------------------------------------------------
def numbered_list(slide, items, l=0.94, t=2.05, w=16.5, size=SZ_LIST, spacing=1.35):
    """Numbered conclusions/disclosures: 32 pt black, one idea per item, generous leading."""
    b = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(8.0))
    tf = b.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = spacing; p.space_after = Pt(18)
        r = p.add_run(); r.text = "%d.  %s" % (i + 1, it)
        r.font.name = FONT; r.font.size = Pt(size); r.font.color.rgb = BLACK
    return b


def steps(slide, items, top=2.05, left=0.94, width=18.125, box_h=1.22, pitch=2.22):
    """Analytic-approach ladder: rounded boxes on a light->dark ramp, the final (primary) step
    inverted (navy fill, white text), small dark triangles between steps. items=[(head, line), ...].
    Heads are the ONLY bold body text the house allows (structural labels)."""
    n = len(items); ramp = STEP_RAMP[-n:] if n <= len(STEP_RAMP) else STEP_RAMP
    for i, (head, line) in enumerate(items):
        y = top + i * pitch; col = ramp[min(i, len(ramp) - 1)]; txt = WHITE if i == n - 1 else BLACK
        _rect(slide, left, y, width, box_h, col, MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
        _tx(slide, left + 0.35, y + box_h / 2 - LINE_H / 2, 0.6, LINE_H, str(i + 1), SZ_BODY, txt, bold=True,
            anchor=MSO_ANCHOR.MIDDLE)
        _tx(slide, left + 1.15, y + 0.10, width - 1.5, LINE_H, head, SZ_BODY, txt, bold=True)
        _tx(slide, left + 1.15, y + 0.58, width - 1.5, LINE_H, line, SZ_BODY, txt)
        if i < n - 1:
            _rect(slide, left + width / 2 - 0.12, y + box_h + 0.33, 0.24, 0.20, RGBColor(0x40, 0x40, 0x40),
                  MSO_SHAPE.ISOSCELES_TRIANGLE).rotation = 180


def blank(prs, layout=None):
    """New slide on the deck's own layout, with any placeholders removed."""
    lay = layout if layout is not None else (
        prs.slides[19].slide_layout if len(prs.slides) > 19 else prs.slide_layouts[0])
    s=prs.slides.add_slide(lay)
    for ph in list(s.shapes):
        if ph.is_placeholder:
            ph._element.getparent().remove(ph._element)
    return s


def move_slide(prs,old_index,new_index):
    """Reorder by manipulating sldIdLst (python-pptx has no API for this)."""
    lst=prs.slides._sldIdLst
    ids=list(lst)
    lst.remove(ids[old_index])
    lst.insert(new_index,ids[old_index])


# ---- log-symmetric ratio axis ------------------------------------------------
# Exact reciprocal pairs, so the null sits dead centre and the tick labels mirror.
_LADDER = [(1.25, 1.6), (1.25, 1.5), (1.6, 2.5), (1.4, 2.0), (2.0, 4.0)]

def sym_axis(values):
    """Pick [1/k, k] and five mirror-symmetric ticks covering every value/CI bound."""
    import math
    ext = max(max(values), 1.0/min(values))
    for m, k in sorted(_LADDER, key=lambda t: t[1]):
        if ext <= k * 1.001:
            return 1.0/k, k, [round(1.0/k, 3), round(1.0/m, 3), 1.0, m, k]
    k = 4.0; m = 2.0
    return 1.0/k, k, [1.0/k, 1.0/m, 1.0, m, k]




def clear_slide(slide, keep=None):
    """Strip every shape from a slide so it can be redrawn in place.

    Rewriting a slide in place is the ONLY safe way to replace one: deleting a slide with
    part.drop_rel() frees its relationship id, and the next add_slide() reuses that id, which
    silently re-points earlier sldId entries at the new slide. That corrupted this deck once
    (four different slides all rendered as the last one built) -- never delete, always rewrite.
    """
    keep = keep or (lambda sh: False)
    for sh in list(slide.shapes):
        if not keep(sh):
            sh._element.getparent().remove(sh._element)
    return slide


def find_slide(prs, title_prefix):
    """Index of the first slide whose any text box starts with title_prefix, else None."""
    for i, sl in enumerate(prs.slides):
        for sh in sl.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip().startswith(title_prefix):
                return i
    return None


# =============================================================================
# SAFE DECK OPERATIONS
#
# Everything below was learned the hard way editing a live deck while the author
# edited it in parallel. Read references/pptx-gotchas.md before changing any of it.
# =============================================================================

from pptx.oxml.ns import qn


def find_slide_by_title(prs, title, exact=True):
    """Locate a slide by its title text. NEVER address slides by index.

    Indices move whenever the author adds or deletes a slide, which they do
    between your runs. Every write must re-locate its target by content.
    """
    for s in prs.slides:
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            t = sh.text_frame.text.strip()
            if (t == title) if exact else (title in t):
                return s
    return None


def keep_furniture(slide, title_rule_y=1.70, footer_rule_y=10.20):
    """Delete the slide body, keep the furniture. Returns shapes removed.

    Furniture is located GEOMETRICALLY -- anything above the title rule or below
    the footer rule -- not by shape index. Index-based retention breaks the first
    time the author edits the slide.
    """
    from pptx.util import Emu
    removed = 0
    for sh in list(slide.shapes):
        top = Emu(sh.top).inches if sh.top is not None else 0.0
        if top <= title_rule_y or top >= footer_rule_y:
            continue
        sh._element.getparent().remove(sh._element)
        removed += 1
    return removed


def insert_slide_after(prs, ref_slide, layout=None):
    """Add a slide and move it directly after ref_slide.

    add_slide() always appends; ordering is fixed by reordering p:sldIdLst.
    NEVER call drop_rel() -- it frees relationship IDs that add_slide() then
    reuses, silently corrupting the deck. That prohibition is absolute.
    """
    idx = list(prs.slides).index(ref_slide)
    new = prs.slides.add_slide(layout or ref_slide.slide_layout)
    for sh in list(new.shapes):              # strip layout placeholders
        sh._element.getparent().remove(sh._element)
    lst = prs.slides._sldIdLst
    moved = list(lst)[-1]
    lst.remove(moved)
    lst.insert(idx + 1, moved)
    return new


def full_bleed_picture(prs, slide, img_path):
    """Place a rendered figure edge to edge. The figure must be 16:9."""
    return slide.shapes.add_picture(str(img_path), 0, 0,
                                    width=prs.slide_width,
                                    height=prs.slide_height)


def set_white_background(slide):
    """Drop a slide-level background override so the layout's white shows."""
    cSld = slide._element.find(qn("p:cSld"))
    bg = cSld.find(qn("p:bg"))
    if bg is not None:
        cSld.remove(bg)
        return True
    return False


# ---- outline colour, read safely -------------------------------------------

def line_hex(shape):
    """Read a shape's outline colour from XML.

    Reading shape.line.color in python-pptx calls _get_or_add_ln(), which INSERTS
    an empty <a:ln><a:solidFill/></a:ln>. PowerPoint renders that as a black
    hairline. One audit pass once put 285 stray outlines across 41 slides this
    way. Always read outlines from the XML instead.
    """
    ln = shape._element.find(".//" + qn("a:ln"))
    if ln is None:
        return None
    clr = ln.find(".//" + qn("a:srgbClr"))
    return clr.get("val") if clr is not None else None


def strip_empty_outlines(prs):
    """Repair <a:ln><a:solidFill/></a:ln> stubs left by reading shape.line.color."""
    fixed = 0
    for s in prs.slides:
        for ln in s._element.iter(qn("a:ln")):
            kids = list(ln)
            if len(kids) == 1 and kids[0].tag == qn("a:solidFill") and not len(list(kids[0])):
                ln.getparent().remove(ln)
                fixed += 1
    return fixed


# ---- native tables ----------------------------------------------------------

_EDGES = ["lnL", "lnR", "lnT", "lnB"]


def cell_borders(cell, spec):
    """spec: {'lnT': (hex_or_None, pt), ...}; omitted edges are cleared.

    The edge elements must appear in schema order (L, R, T, B) and BEFORE the
    fill element, so the whole tcPr child list is rebuilt. Note the tag is
    'a:lnT', not 'a:ln' + 'lnT' -- getting that wrong produces <a:lnlnT>, which
    PowerPoint silently ignores.
    """
    tcPr = cell._tc.get_or_add_tcPr()
    for e in _EDGES:
        for old in tcPr.findall(qn("a:" + e)):
            tcPr.remove(old)
    rest = list(tcPr)
    for ch in rest:
        tcPr.remove(ch)
    for e in _EDGES:
        col, pt = spec.get(e, (None, 1.0))
        ln = tcPr.makeelement(qn("a:" + e), {"w": str(int(pt * 12700)),
                                             "cap": "flat", "cmpd": "sng",
                                             "algn": "ctr"})
        if col is None:
            ln.append(ln.makeelement(qn("a:noFill"), {}))
        else:
            fill = ln.makeelement(qn("a:solidFill"), {})
            fill.append(fill.makeelement(qn("a:srgbClr"), {"val": col}))
            ln.append(fill)
        tcPr.append(ln)
    for ch in rest:
        tcPr.append(ch)


def cell_no_fill(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    for t in ("a:solidFill", "a:noFill", "a:gradFill", "a:blipFill", "a:pattFill"):
        for old in tcPr.findall(qn(t)):
            tcPr.remove(old)
    tcPr.append(tcPr.makeelement(qn("a:noFill"), {}))


def plain_table(slide, rows, cols, l, t, w, h, col_widths=None, row_heights=None):
    """A table with the deck's own styling: no banding, no fills, hairlines only."""
    gf = slide.shapes.add_table(rows, cols, Inches(l), Inches(t), Inches(w), Inches(h))
    tbl = gf.table
    tblPr = tbl._tbl.find(qn("a:tblPr"))
    for a in ("firstRow", "bandRow", "firstCol", "bandCol", "lastRow", "lastCol"):
        tblPr.set(a, "0")
    if col_widths:
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = Inches(cw)
    if row_heights:
        for i, rh in enumerate(row_heights):
            tbl.rows[i].height = Inches(rh)
    for r in range(rows):
        for c in range(cols):
            cell_no_fill(tbl.cell(r, c))
            cell_borders(tbl.cell(r, c), {})
    return tbl


def same_shape(a, b):
    """python-pptx re-wraps shapes on every access, so `a is b` is ALWAYS False
    even for the same shape. Compare the underlying XML elements."""
    return a._element is b._element
