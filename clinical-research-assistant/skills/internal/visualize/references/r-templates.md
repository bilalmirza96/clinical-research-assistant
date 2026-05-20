# R Templates — Override Backend

Preserved R code patterns from the v2 `/visualize`. Used when:

- User explicitly requests R for a specific figure (`figure_specs.json::backend_override: "R"`)
- A specialized R package produces a better result than Python equivalent (e.g., `survminer` for KM with at-risk table, `forestploter` for forest plots, `rms` for spline plots)
- Journal explicitly requests R-rendered figures

The CRA aesthetic standards in `aesthetic-standards.md` apply identically when using R.

---

## Required R packages

```r
# Core
library(tidyplots)     # high-level plotting grammar
library(ggplot2)       # underlying engine
library(dplyr)         # data manipulation
library(patchwork)     # multi-panel composition

# Specialized
library(survminer)     # Kaplan-Meier with at-risk tables
library(forestploter)  # forest plots with table layout
library(pROC)          # ROC curves
library(tidycmprsk)    # competing risks
library(ggrepel)       # label placement
library(DiagrammeR)    # flow diagrams
library(rms)           # spline plots
library(scales)        # axis formatting
```

---

## Output convention

```r
# PDF (vector, primary)
ggsave("Figure_<N>_<slug>.pdf", width = W, height = H, units = "in")

# PNG (raster, secondary)
ggsave("Figure_<N>_<slug>.png", width = W, height = H, units = "in", dpi = 600)

# tidyplots shortcut
save_plot("Figure_<N>_<slug>.pdf", width = W, height = H)
```

Dimensions: 3.5 in (single column), 7 in (double column).

---

## tidyplots — group comparison (bar + beeswarm + P-value)

```r
library(tidyplots)

tidyplot(data, x = group, y = il6_pod1, color = group) |>
  add_mean_bar(alpha = 0.7) |>
  add_sem_errorbar() |>
  add_data_points_beeswarm(alpha = 0.5, size = 1.5) |>
  add_test_pvalue() |>
  adjust_colors(new_colors = c("#2C3E50", "#C0392B")) |>
  adjust_y_axis_label("IL-6 POD1 (pg/mL)") |>
  remove_x_axis_label() |>
  theme_tidyplot() |>
  save_plot("Figure_3_il6_comparison.pdf", width = 3.5, height = 4)
```

---

## ggplot2 — forest plot

```r
library(ggplot2)
library(dplyr)

results <- tibble(
  variable = c("IL-6 POD1", "TNF-α POD1", "IL-10 POD1"),
  or = c(2.34, 1.89, 0.72),
  ci_lower = c(1.56, 1.12, 0.45),
  ci_upper = c(3.52, 3.19, 1.15)
) |>
  mutate(variable = factor(variable, levels = rev(variable)))

ggplot(results, aes(x = or, y = variable)) +
  geom_vline(xintercept = 1.0, linetype = "dashed", color = "gray60", linewidth = 0.5) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0, linewidth = 0.8, color = "#2C3E50") +
  geom_point(size = 3, shape = 15, color = "#2C3E50") +
  scale_x_log10() +
  labs(x = "Adjusted Odds Ratio (95% CI)", y = NULL) +
  theme_classic(base_family = "Arial", base_size = 11) +
  theme(
    axis.line.y = element_blank(),
    axis.ticks.y = element_blank(),
    panel.grid.major.y = element_line(color = "#F0F0F0", linewidth = 0.3)
  )

ggsave("Figure_2_forest_plot.pdf", width = 7, height = 4, units = "in", dpi = 600)
ggsave("Figure_2_forest_plot.png", width = 7, height = 4, units = "in", dpi = 600)
```

---

## survminer — Kaplan-Meier with at-risk table

```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, event) ~ group, data = df)

ggsurvplot(
  fit,
  data = df,
  conf.int = TRUE,
  pval = TRUE,
  pval.method = TRUE,
  risk.table = TRUE,
  risk.table.height = 0.25,
  palette = c("#2C3E50", "#C0392B"),
  xlab = "Time (months)",
  ylab = "Overall survival probability",
  legend.title = "Group",
  legend.labs = c("Group A", "Group B"),
  ggtheme = theme_classic(base_family = "Arial", base_size = 11)
)
# Then save the composite via ggsave or via the survminer print method
```

---

## tidycmprsk — cumulative incidence with competing risks

```r
library(tidycmprsk)
library(ggsurvfit)

cuminc(Surv(time, event) ~ group, data = df) |>
  ggcuminc(outcome = "1") +
  add_confidence_interval() +
  add_risktable() +
  scale_color_manual(values = c("#2C3E50", "#C0392B")) +
  labs(x = "Time (months)", y = "Cumulative incidence") +
  theme_classic(base_family = "Arial", base_size = 11)
```

---

## pROC + ggplot2 — ROC curve

```r
library(pROC)
library(ggplot2)

roc_obj <- roc(outcome ~ predictor, data = df, ci = TRUE)
auc_value <- auc(roc_obj)
auc_ci <- ci.auc(roc_obj)

ggroc(roc_obj, color = "#2C3E50", size = 1) +
  geom_abline(slope = 1, intercept = 1, linetype = "dashed", color = "gray60") +
  annotate("text", x = 0.4, y = 0.2,
           label = sprintf("AUC = %.2f (95%% CI %.2f-%.2f)",
                           auc_value, auc_ci[1], auc_ci[3]),
           family = "Arial", size = 4) +
  labs(x = "1 - Specificity", y = "Sensitivity") +
  theme_classic(base_family = "Arial", base_size = 11)
```

---

## ggplot2 — Love plot (PSM balance)

```r
library(ggplot2)

balance <- tibble(
  covariate = c("Age", "BMI", "ASA III+", "Female", "Diabetes"),
  smd_unmatched = c(0.42, 0.31, 0.55, 0.18, 0.27),
  smd_matched = c(0.05, 0.04, 0.07, 0.02, 0.06)
)

balance_long <- balance |>
  tidyr::pivot_longer(cols = starts_with("smd"),
                      names_to = "match_status",
                      values_to = "smd") |>
  mutate(match_status = recode(match_status,
                               smd_unmatched = "Before matching",
                               smd_matched = "After matching"))

ggplot(balance_long, aes(x = smd, y = covariate, color = match_status)) +
  geom_vline(xintercept = c(-0.1, 0.1), linetype = "dashed", color = "gray60") +
  geom_vline(xintercept = 0, color = "black", linewidth = 0.3) +
  geom_point(size = 3) +
  scale_color_manual(values = c("Before matching" = "#C0392B",
                                "After matching" = "#2C3E50")) +
  labs(x = "Standardized Mean Difference",
       y = NULL,
       color = NULL) +
  theme_classic(base_family = "Arial", base_size = 11) +
  theme(legend.position = "bottom")
```

---

## rms — spline plot (RCS)

```r
library(rms)
library(ggplot2)

dd <- datadist(df); options(datadist = "dd")
fit <- lrm(outcome ~ rcs(age, 4) + sex + bmi, data = df)
pred <- Predict(fit, age, fun = exp)  # OR scale

ggplot(pred) +
  geom_hline(yintercept = 1, linetype = "dashed", color = "gray60") +
  geom_line(aes(x = age, y = yhat), color = "#2C3E50", linewidth = 0.8) +
  geom_ribbon(aes(x = age, ymin = lower, ymax = upper),
              alpha = 0.2, fill = "#2C3E50") +
  scale_y_log10() +
  labs(x = "Age (years)", y = "Adjusted OR (95% CI)") +
  theme_classic(base_family = "Arial", base_size = 11)
```

---

## patchwork — multi-panel composition

```r
library(patchwork)

p1 <- # ... first plot
p2 <- # ... second plot
p3 <- # ... third plot

(p1 | p2) / p3 +
  plot_annotation(tag_levels = "A",
                  theme = theme(plot.tag = element_text(face = "bold",
                                                        family = "Arial",
                                                        size = 14)))
ggsave("Figure_5_multipanel.pdf", width = 7, height = 8, units = "in")
```

---

## Universal theme override

If using ggplot2 directly without tidyplots, apply this theme to enforce CRA aesthetic standards:

```r
cra_theme <- function() {
  theme_classic(base_family = "Arial", base_size = 11) +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(linewidth = 0.4),
      axis.ticks = element_line(linewidth = 0.4),
      axis.title = element_text(size = 11),
      axis.text = element_text(size = 10),
      legend.title = element_blank(),
      legend.text = element_text(size = 10),
      plot.title = element_text(size = 12, face = "bold")
    )
}

# Use:
ggplot(...) + ... + cra_theme()
```
