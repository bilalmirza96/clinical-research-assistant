#!/usr/bin/env python3
"""
Visual verification for a PowerPoint deck: PPTX -> PDF -> PNG.

You cannot trust a deck edit you have not looked at. python-pptx will happily
write geometry that PowerPoint renders wrong (clipped text, stray hairlines,
shapes behind other shapes), and it reports success either way.

Usage:
    python3 render_deck.py DECK.pptx OUTDIR [--match "Slide Title"] [--all]

Notes
  - PowerPoint must be QUIT before exporting. A running instance serves a
    cached copy of an already-open file, so you render the PREVIOUS version and
    conclude your edit failed (or, worse, that it worked).
  - Hidden slides (show="0") are excluded from the PDF, so PDF page numbers do
    not equal deck slide numbers. Match on title text, not on index.
"""
import subprocess, sys, time
from pathlib import Path

APPLESCRIPT = '''
tell application "Microsoft PowerPoint"
  open POSIX file "{deck}"
  save active presentation in POSIX file "{pdf}" as save as PDF
  close active presentation saving no
end tell
'''


def quit_powerpoint():
    subprocess.run(["osascript", "-e",
                    'tell application "Microsoft PowerPoint" to quit saving no'],
                   capture_output=True)
    time.sleep(3)


def export_pdf(deck: Path, pdf: Path) -> Path:
    quit_powerpoint()
    pdf.parent.mkdir(parents=True, exist_ok=True)   # PowerPoint will not create it
    pdf.unlink(missing_ok=True)
    r = subprocess.run(["osascript", "-e",
                        APPLESCRIPT.format(deck=deck.resolve(), pdf=pdf.resolve())],
                       capture_output=True, text=True)
    if not pdf.exists():
        sys.exit("PDF export failed: %s" % (r.stderr.strip() or "no output"))
    return pdf


def render(pdf: Path, outdir: Path, match=None, scale=2.0, render_all=False):
    import fitz
    d = fitz.open(str(pdf))
    outdir.mkdir(parents=True, exist_ok=True)
    hits = []
    for i in range(len(d)):
        text = d[i].get_text()
        if render_all or (match and match.lower() in text.lower()):
            out = outdir / ("page%02d.png" % i)
            d[i].get_pixmap(matrix=fitz.Matrix(scale, scale)).save(str(out))
            hits.append((i, out))
            if match and not render_all:
                break
    if not hits:
        print("no page matched %r; deck has %d rendered pages" % (match, len(d)))
    for i, out in hits:
        print("page %d -> %s" % (i, out))
    return hits


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    deck, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    match = None
    if "--match" in sys.argv:
        match = sys.argv[sys.argv.index("--match") + 1]
    pdf = export_pdf(deck, outdir / "deck.pdf")
    render(pdf, outdir, match=match, render_all="--all" in sys.argv)
