#!/usr/bin/env bash
# Scaffold for L107-no-single-gene-cell-state. Writes a small synthetic per-cell
# expression table (log1p CP10k) for liver macrophages from tumor and adjacent
# normal tissue. Deterministic (seed 42); no external fixture needed.
set -euo pipefail
mkdir -p data Reports scripts
python3 - <<'PY'
import random, csv
random.seed(42)
genes = ["FOLR2","CD163","MRC1","LYVE1","MARCO","HES1","NR1H3","SPIC","MAF","SPP1","TREM2","FCN1","S100A8","VCAN"]
with open("data/liver_macrophages.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["cell_id","patient","tissue"] + genes)
    for p in range(1, 7):
        for tissue in ("tumor","adjacent_normal"):
            for i in range(40):
                w.writerow([f"P{p}_{tissue}_{i}", f"P{p}", tissue] + [round(max(0, random.gauss(1.0, 0.8)), 3) for _ in genes])
PY
