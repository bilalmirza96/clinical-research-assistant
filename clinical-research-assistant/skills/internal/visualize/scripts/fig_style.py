"""
fig_style.py — Bilal Mirza house figure style (v1, 2026-07-13): one coherent,
restrained editorial style for clinical / genomic research figures.

The palette is swappable (edit the "palette" block) but the SEMANTIC ROLES and the
structural language (rounded bars/CI capsules, card frame, clean sans typography,
short titles with stats in the caption, 300 DPI) are the house standard. For journal
submission omit titles() and let the caption carry the title (see aesthetic-standards.md).

Design goals (per author request 2026-07-13):
  * one coherent color palette across every figure
  * rounded corners on bars / CI capsules ("rounded borders of graphs and charts")
  * clean typography, short left-aligned titles, stats moved to a light subtitle
  * a subtle rounded "card" frame so each figure reads as a tidy panel in the Word doc

Public API
----------
setup()                          -> apply global rcParams
new_fig(w, h)                    -> (fig, ax) at fixed dpi with a rounded card
titles(fig, title, subtitle)     -> left-aligned title + light subtitle in figure coords
rbar(ax, x0, y0, w, h, color, ...) -> rounded-corner rectangle in DATA coords (pixel radius)
capsule(ax, x0, x1, y, thick_px, color, ...) -> rounded CI capsule (forest plots)
despine(ax) / grid(ax)           -> consistent spines + gridlines
legend(ax, ...)                  -> rounded, frameless-ish legend
finish(fig, path)                -> add card, save at 200 dpi

Colors are semantic and reused everywhere:
  TEAL  = primary / DIRECT (anatomic) effect / development (internal) cohort
  CORAL = secondary / MEDIATED via molecular (APC) axis
  PLUM  = external / replication cohort contrast
  GREEN = FDR-significant highlight (forest)
  AMBER = nominal significance (p<.05, q>=.05)
  SLATE = non-significant / neutral / reference lines
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, FancyBboxPatch
from matplotlib.lines import Line2D

# ---------------------------------------------------------------- palette
INK    = "#22333F"   # primary text / axes
MUTE   = "#5E6B78"   # secondary text / annotations
FAINT  = "#93A0AC"   # tertiary text
GRID   = "#E9ECF0"   # gridlines
SPINE  = "#C4CCD4"   # kept spines
CARD_FC = "#FCFDFE"  # card fill (barely off-white)
CARD_EC = "#E1E7ED"  # card border
PAGE_FC = "#FFFFFF"  # figure background outside card

# Palette swap 2026-08-06 (author directive: red/blue contrast pair).
# The SEMANTIC ROLES are unchanged, per the House Figure Style Standard: hexes are
# swappable, roles are not. TEAL still means primary/direct, CORAL still means
# mediated/molecular; only the hues moved. Names kept so existing scripts import
# unchanged; use the BLUE/RED or PRIMARY/MEDIATED aliases below in new code.
#
# The blue is a deep navy rather than the original medium blue (#2F6FB0) because
# grayscale luminance separation is a hard constraint for print venues: medium blue
# and this red both land near gray 96-99 of 255, a separation of 3, which makes the
# two series indistinguishable when a journal or meeting prints in grayscale.
# Navy #123E66 sits at gray 53 against the red at 96, a separation of 43.
# If you change these hexes, re-check that separation before shipping.
TEAL   = "#123E66"   # primary / direct / internal   (navy;  grayscale 53)
TEAL_D = "#0B2A45"
CORAL  = "#C0392B"   # mediated / molecular          (red;   grayscale 96)
CORAL_D = "#96271C"

# Role-named aliases: prefer these over the colour names, which are now historical.
BLUE = PRIMARY = TEAL
BLUE_D = PRIMARY_D = TEAL_D
RED = MEDIATED = CORAL
RED_D = MEDIATED_D = CORAL_D
PLUM   = "#6C5B9E"   # external / replication
PLUM_D = "#4E4276"
GREEN  = "#3C9A73"   # FDR-significant
AMBER  = "#D9A441"   # nominal significance
SLATE  = "#AEBAC5"   # non-significant / neutral

DPI = 300            # manuscript-grade; review renders can drop to 200
R_PX = round(DPI * 0.03)   # default corner radius in px, DPI-relative so the
                           # physical roundness is constant across DPI settings
_K = 0.5522847498    # cubic-bezier circle constant


# ---------------------------------------------------------------- global style
def setup():
    plt.rcParams.update({
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "figure.facecolor": PAGE_FC,
        "savefig.facecolor": PAGE_FC,
        "font.family": "sans-serif",
        # Arial leads deliberately. Helvetica Neue ships on macOS as a .ttc that
        # matplotlib registers at weight 400 ONLY, so every fontweight="bold"
        # request silently resolved to the regular face and nothing in any house
        # figure ever rendered bold. Arial carries real 400 and 700 faces and is
        # metrically close to Helvetica. Verified 2026-08-06.
        "font.sans-serif": ["Arial", "Helvetica Neue", "Helvetica", "DejaVu Sans"],
        "font.size": 11,
        "text.color": INK,
        "axes.edgecolor": SPINE,
        "axes.linewidth": 1.0,
        "axes.labelcolor": INK,
        "axes.labelsize": 11.5,
        "axes.titlesize": 12,
        "axes.facecolor": "none",
        "axes.grid": False,
        "xtick.color": MUTE,
        "ytick.color": MUTE,
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 10.5,
        "legend.fontsize": 9.5,
        "legend.frameon": False,
        "axes.unicode_minus": True,
    })


# ---------------------------------------------------------------- figure scaffold
def new_fig(w, h, left=0.13, right=0.97, bottom=0.14, top=0.80):
    """Fixed-geometry figure (no tight_layout) so pixel-radius rounding is stable.

    Generous top margin holds the title/subtitle placed via titles()."""
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    ax = fig.add_axes([left, bottom, right - left, top - bottom])
    return fig, ax


def new_fig_axes(w, h, rects):
    """Multi-panel variant: pass a list of [l,b,w,h] axes rects (figure fraction)."""
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    axes = [fig.add_axes(r) for r in rects]
    return fig, axes


def titles(fig, title, subtitle=None, x=0.035, y=0.945):
    fig.text(x, y, title, ha="left", va="top", color=INK,
             fontsize=13.5, fontweight="bold")
    if subtitle:
        fig.text(x, y - 0.075, subtitle, ha="left", va="top", color=MUTE,
                 fontsize=10.2)


def badge(fig, text, x=0.035, y=0.945, fontsize=9.5, fc=None, tc="white"):
    """Dark rounded pill in the top-left, e.g. badge(fig, "FIGURE 1").

    Sits above titles(); call titles() with a lower y (0.86 works) when using it."""
    return fig.text(x, y, text.upper(), ha="left", va="center", color=tc,
                    fontsize=fontsize, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.55", facecolor=fc or INK,
                              edgecolor="none"))


def footnote(fig, text, x=0.035, y=0.045, rule=True, fontsize=8.6, width=0.93):
    """Small faint source/method note, optionally over a dashed hairline rule."""
    if rule:
        fig.add_artist(Line2D([x, x + width], [y + 0.055, y + 0.055],
                              transform=fig.transFigure, color=CARD_EC,
                              linewidth=1.0, linestyle=(0, (4, 4)), zorder=1))
    return fig.text(x, y, text, ha="left", va="bottom", color=FAINT,
                    fontsize=fontsize)


def swatch_legend(fig, items, x=0.035, y=0.125, fontsize=10.2, gap=0.30,
                  size=0.016):
    """Frameless inline legend: [(color, label), ...] laid out left to right.

    Matches the house reference figures, which carry square swatches under the
    axes rather than a boxed legend."""
    for i, (color, label) in enumerate(items):
        cx = x + i * gap
        fig.add_artist(FancyBboxPatch((cx, y - size / 2), size, size,
                                      transform=fig.transFigure,
                                      boxstyle="round,pad=0,rounding_size=0.004",
                                      facecolor=color, edgecolor="none", zorder=4))
        fig.text(cx + size * 1.75, y, label, ha="left", va="center",
                 color=INK, fontsize=fontsize)


def despine(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)
    ax.tick_params(length=3.5, width=1.0, color=SPINE)


def grid(ax, axis="y"):
    ax.set_axisbelow(True)
    ax.grid(True, axis=axis, color=GRID, linewidth=1.0, zorder=0)


def legend(ax, **kw):
    lg = ax.legend(frameon=True, framealpha=1.0, edgecolor=CARD_EC,
                   facecolor="white", borderpad=0.7, labelspacing=0.55,
                   handlelength=1.3, handletextpad=0.7, **kw)
    lg.get_frame().set_linewidth(1.0)
    fr = lg.get_frame()
    fr.set_boxstyle("round,pad=0.4,rounding_size=0.5")
    for t in lg.get_texts():
        t.set_color(INK)
    return lg


# ---------------------------------------------------------------- rounded shapes
def _rounded_path(x0, y0, w, h, rx, ry, corners):
    """Rounded rectangle Path; `corners` subset of {'tl','tr','br','bl'}."""
    x1, y1 = x0 + w, y0 + h
    rx = min(rx, abs(w) / 2.0)
    ry = min(ry, abs(h) / 2.0)

    def rr(c):
        return (rx if c in corners else 0.0, ry if c in corners else 0.0)

    tlx, tly = rr("tl")
    trx, try_ = rr("tr")
    brx, bry = rr("br")
    blx, bly = rr("bl")
    V, C = [], []
    # start just right of bottom-left corner, travel CCW
    V.append((x0 + blx, y0)); C.append(Path.MOVETO)
    V.append((x1 - brx, y0)); C.append(Path.LINETO)          # bottom edge
    if brx > 0:                                              # bottom-right corner
        V += [(x1 - brx + _K * brx, y0), (x1, y0 + bry - _K * bry), (x1, y0 + bry)]
        C += [Path.CURVE4] * 3
    V.append((x1, y1 - try_)); C.append(Path.LINETO)         # right edge
    if trx > 0:                                              # top-right corner
        V += [(x1, y1 - try_ + _K * try_), (x1 - trx + _K * trx, y1), (x1 - trx, y1)]
        C += [Path.CURVE4] * 3
    V.append((x0 + tlx, y1)); C.append(Path.LINETO)          # top edge
    if tlx > 0:                                              # top-left corner
        V += [(x0 + tlx - _K * tlx, y1), (x0, y1 - tly + _K * tly), (x0, y1 - tly)]
        C += [Path.CURVE4] * 3
    V.append((x0, y0 + bly)); C.append(Path.LINETO)          # left edge
    if blx > 0:                                              # bottom-left corner
        V += [(x0, y0 + bly - _K * bly), (x0 + blx - _K * blx, y0), (x0 + blx, y0)]
        C += [Path.CURVE4] * 3
    V.append((x0 + blx, y0)); C.append(Path.CLOSEPOLY)
    return Path(V, C)


def _px_per_data(ax):
    ax.figure.canvas.draw()
    bb = ax.get_window_extent()
    xl, yl = ax.get_xlim(), ax.get_ylim()
    return bb.width / abs(xl[1] - xl[0]), bb.height / abs(yl[1] - yl[0])


def rbar(ax, x0, y0, w, h, color, radius_px=None, corners=("tl", "tr", "br", "bl"),
         ec="white", lw=1.0, z=3, alpha=1.0):
    """Rounded rectangle in data coords with true pixel-radius corners.

    radius_px defaults to R_PX (DPI-relative) so roundness looks constant across DPI.
    Limits must be set before calling (radius is derived from the axes geometry)."""
    if radius_px is None:
        radius_px = R_PX
    ppx, ppy = _px_per_data(ax)
    p = _rounded_path(x0, y0, w, h, radius_px / ppx, radius_px / ppy, set(corners))
    ax.add_patch(PathPatch(p, facecolor=color, edgecolor=ec, linewidth=lw,
                           zorder=z, alpha=alpha, antialiased=True))


def capsule(ax, x0, x1, y, thick_px, color, z=3, alpha=1.0):
    """A horizontal rounded capsule from x0..x1 at height y (forest CI)."""
    ppx, ppy = _px_per_data(ax)
    h = thick_px / ppy
    p = _rounded_path(min(x0, x1), y - h / 2, abs(x1 - x0), h,
                      (thick_px / 2) / ppx, (thick_px / 2) / ppy,
                      {"tl", "tr", "br", "bl"})
    ax.add_patch(PathPatch(p, facecolor=color, edgecolor="none",
                           zorder=z, alpha=alpha, antialiased=True))


# ---------------------------------------------------------------- card + save
def _card(fig):
    ar = fig.get_figwidth() / fig.get_figheight()
    card = FancyBboxPatch(
        (0.012, 0.012), 0.976, 0.976, transform=fig.transFigure,
        boxstyle="round,pad=0,rounding_size=0.022",
        mutation_aspect=ar, facecolor=CARD_FC, edgecolor=CARD_EC,
        linewidth=1.2, zorder=-100, clip_on=False)
    fig.patches.insert(0, card)


def finish(fig, path):
    _card(fig)
    fig.savefig(path, dpi=DPI, facecolor=PAGE_FC)
    plt.close(fig)
    return path
