# `visualize` — CHANGELOG / Lessons Learned

**Load trigger:** only when auditing the history of this skill. Never needed to run the skill; `SKILL.md` holds enforcement. Newest first.

---

- **2026-09-06 (v1.2 exemplar devices).** Author adopted a two-panel JAMA-style exemplar as the
  target look (declarative panel headers that state the finding, on-data value labels, effect
  brackets, at-risk tables, dense sourced footnotes). `scripts/fig_style.py` gained
  `panel_header`, `effect_bracket`, `at_risk_table`, `dist_strip`, `endpoint_label`. First deck:
  ITSOS 2026 REPEAT DISPARITIES (21 figures). Gotchas: anchor forest right-hand labels in axes x,
  not data x (they clip otherwise); serif is the house default (L070), not sans as older text
  here says; external national statistics are declared as sourced constants in the figure
  script and never written to the registry. Lessons-log L074.
