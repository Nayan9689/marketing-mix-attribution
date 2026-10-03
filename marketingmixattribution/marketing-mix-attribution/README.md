# Marketing Mix Attribution

**Problem:** A B2B SaaS company spends across multiple outreach channels. Which channels
are actually driving conversions, and how should budget be reallocated?

See `reports/README.md` for the findings and business recommendation.

## Structure
```
marketing-mix-attribution/
├── data/                  # touchpoints.csv, spend.csv
├── notebooks/              # EDA -> attribution models -> comparison -> recommendation
├── src/                     # generate_data.py, build_notebook.py
├── reports/                 # findings & recommendation (see README.md there)
├── requirements.txt
└── .gitignore
```

## Methods
Last-touch -> first-touch -> linear/position-based -> logistic regression -> Shapley-value
(computed per lead over that lead's own touched channels, to avoid requiring an unobserved
"all 7 channels at once" coalition).

## Status
- [x] Dataset generated and sanity-checked
- [x] Notebook built, executed end-to-end, recommendation written
- [x] reports/README.md written
- [ ] Optional: Streamlit page (channel attribution bar chart + ROI/CAC table)
