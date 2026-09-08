# Week 1 — Data Acquisition, Cleaning & Preprocessing

Task submitted for the **YuvaIntern Virtual Data Science with Python Trainee** internship (Week 1).

## Objective
Acquire a publicly available dataset, explore its structure and quality, and apply systematic
cleaning and preprocessing using Python — documenting missing values, inconsistencies, and
outlier handling along the way.

## Dataset
**Palmer Archipelago (Antarctica) Penguin Data** — raw version
Source: [palmerpenguins by Allison Horst](https://github.com/allisonhorst/palmerpenguins)

344 records of three penguin species (Adelie, Chinstrap, Gentoo) collected by the Palmer Station
Long Term Ecological Research (LTER) Program. Chosen because it has real missing values,
inconsistent text formatting, and genuine outliers — a realistic cleaning exercise rather than an
already-clean toy dataset.

## Repo structure
```
├── Week1_Data_Cleaning_Report.docx   # Full report: process, code, screenshots, findings
├── data/
│   ├── penguins_raw.csv              # Original unmodified dataset
│   └── penguins_cleaned.csv          # Final cleaned dataset
├── scripts/
│   ├── 01_explore.py                 # Initial data exploration
│   ├── 02_clean.py                   # Missing value handling + cleaning
│   └── 03_outliers_per_species.py    # Per-species outlier detection
├── screenshots/                      # Charts generated during analysis
└── requirements.txt
```

## What was done
- Explored dataset shape, dtypes, and missing values
- Standardized inconsistent category casing (`Species` column)
- Handled missing values column-by-column based on what the missingness meant
  (dropped fully-empty rows, explicit "Unknown" category for `Sex`, per-species median
  imputation for isotope columns)
- Detected outliers using the IQR method — first pooled (found none), then per-species
  (found 6 legitimate outliers masked by pooling species with different size profiles)
- Parsed `Date Egg` into a proper datetime type
- Documented every decision and its downstream impact on later analysis

## How to run
```bash
pip install -r requirements.txt
cd scripts
python 01_explore.py
python 02_clean.py
python 03_outliers_per_species.py
```

## Full report
See [`Week1_Data_Cleaning_Report.docx`](./Week1_Data_Cleaning_Report.docx) for the complete
write-up with code snippets, narrative reasoning, and all visualizations.
