# Clinical Research Assistant — Settings Template

Copy this file to `.claude/clinical-research-assistant.local.md` in your project directory to configure default preferences. These settings are read automatically by all commands and avoid repetitive questions.

```yaml
---
target_journal: ""
# e.g., "Annals of Surgery", "JAMA Surgery", "Journal of Clinical Oncology"

citation_style: "AMA"
# Options: AMA, Vancouver, APA, Harvard

person_voice: "first"
# Options: "first" (we aimed to...) or "third" (this study aimed to...)

default_alpha: 0.05
# Significance level. Default: 0.05, two-sided

statistical_software: "Python"
# Options: Python, R, Stata, SAS

excel_font: "Times New Roman"
# Font for Excel table output

preferred_registry: ""
# e.g., "NSQIP", "NCDB", "SEER", "UNOS"

subspecialty: ""
# e.g., "surgical oncology", "transplant", "bariatric", "trauma"

institution_name: ""
# Used for IRB statement placeholders

irb_protocol: ""
# IRB protocol number if known
---
```

## How to Use

1. Copy this template to your project: `.claude/clinical-research-assistant.local.md`
2. Fill in your preferred values
3. All commands will read these defaults automatically
4. You can still override any setting during a session by telling Claude directly
