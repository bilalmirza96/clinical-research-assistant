# Registry-Specific Cautions

Key coding issues and outcome limitations for commonly used surgical and clinical registries.

## ACS-NSQIP (National Surgical Quality Improvement Program)

- **Outcome window**: 30-day postoperative outcomes ONLY — do not analyze 60-day or 90-day outcomes
- **Procedure targeting**: Not all procedures captured at all sites — verify procedure inclusion
- **CPT-based identification**: Use CPT codes for cohort selection; ICD codes are secondary
- **Missing variables**: Some variables (e.g., specific lab values) have high missingness — check before including as covariates
- **Risk calculator variables**: Many sites only collect risk calculator variables; extended variables may have significant missingness
- **No cause-specific mortality**: Deaths are all-cause; cannot distinguish surgical from non-surgical mortality
- **Readmission data**: Available only for targeted procedures since 2011

## NCDB (National Cancer Database)

- **No cause-specific survival**: Only overall survival is available — do NOT report disease-specific or cancer-specific survival
- **Facility-level clustering**: Patients nested within facilities — consider GEE or mixed models
- **Treatment intent**: Cannot reliably distinguish curative from palliative intent
- **Chemotherapy coding**: Regimen details are limited; specific agents often not captured
- **Survival follow-up**: Variable by facility and year; check completeness
- **Selection bias**: Commission on Cancer-accredited hospitals only (~70% of cancer cases)

## SEER (Surveillance, Epidemiology, and End Results)

- **Population-based**: Covers ~35% of US population
- **No treatment details**: Surgery and radiation captured; systemic therapy NOT reliably captured
- **Medicare linkage**: SEER-Medicare provides claims data for patients ≥65 years
- **Cause-specific survival**: Available (unlike NCDB)
- **Staging changes**: AJCC staging edition changes over time — harmonize or restrict time periods

## UNOS/OPTN (United Network for Organ Sharing)

- **Allocation policy changes**: Analyze within consistent allocation policy eras
- **Waitlist dynamics**: Distinguish waitlist outcomes from post-transplant outcomes
- **Living vs deceased donor**: Always stratify or restrict
- **Cold ischemia time**: Critical confounder in graft survival analyses
- **Center volume**: Consider as confounder or effect modifier

## NTDB (National Trauma Data Bank)

- **Voluntary reporting**: Not population-based; selection bias exists
- **ISS calculation**: Verify ISS is correctly calculated from AIS codes
- **Missing GCS**: High missingness for intubated/sedated patients
- **Mortality definition**: In-hospital mortality; no post-discharge follow-up
- **Transfer patients**: May appear in both sending and receiving facility data

## MBSAQIP (Metabolic and Bariatric Surgery Accreditation and Quality Improvement Program)

- **Outcome window**: 30-day outcomes only
- **Weight outcomes**: %EWL and %TWL — report both; define excess weight from BMI 25
- **Comorbidity resolution**: Requires follow-up data beyond 30 days for meaningful analysis
- **Procedure codes**: Distinguish primary vs. revisional procedures
- **Concurrent procedures**: Hiatal hernia repair may confound operative time analyses

## General Cautions for All Registries

- **Coding accuracy**: Registry data is abstracted by trained registrars but errors exist — validate implausible values
- **Temporal trends**: Practice patterns change — consider time-period adjustment or restriction
- **Missing data patterns**: Missingness is rarely MCAR in registries — investigate and address
- **Immortal time bias**: Common in registry studies with time-dependent exposures — use landmark analysis or time-varying covariates
- **Selection bias**: Understand who is captured and who is excluded from the registry
