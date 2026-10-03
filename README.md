# Marketing Mix Attribution

**TL;DR:** A B2B company's marketing team spends across 7 channels. The standard way companies
measure "what's working" (last-touch attribution) gives a misleading answer. This project
builds 5 increasingly rigorous attribution methods to find the true answer, and turns it into a
concrete budget-reallocation recommendation worth an estimated $46K–58K/year.

## The business problem

When a customer converts after touching Email, then LinkedIn Ads, then finally Google Ads —
who gets the credit? Most companies default to **last-touch attribution**: whichever channel
closed the deal gets 100% of the credit, and every channel that built the relationship earlier
in the journey gets none. That's the industry default because it's the easiest number to pull
from a CRM — not because it's correct.

The risk: budget keeps flowing to the channel that happens to close deals (often a cheap,
high-volume channel like cold outreach or paid search), while the channels that actually
generate interest and trust (content, webinars, organic search, referrals) look like they
"don't convert" and get their budget cut — even though removing them would tank the whole
funnel.

This project asks: **which channels are actually driving conversions, and how should budget be
reallocated?**

## The data

Since no public dataset combines multi-touch customer journeys *with* channel-level spend (the
two things you need to answer this), the dataset is synthetic — generated with a known,
realistic pattern baked in, so the attribution models have a real signal to recover instead of
noise. See [`src/generate_data.py`](src/generate_data.py) for exactly how.

- **`data/touchpoints.csv`** — 6,000 leads, 14,358 touchpoints (1–5 touches per lead) across 7
  channels: Referral, Content/Webinar, Organic/SEO, Email, LinkedIn Ads, Google Ads, Cold
  Outbound.
- **`data/spend.csv`** — weekly spend per channel across 2024 (52 weeks).

## The methods, in plain terms

Built in increasing order of sophistication, each fixing a blind spot in the one before it:

1. **Last-touch** — 100% of credit to the closing channel. (The flawed industry default.)
2. **First-touch** — 100% of credit to the channel that started the journey. (Equally flawed,
   opposite direction.)
3. **Linear / position-based** — credit split evenly across every channel a lead touched.
4. **Logistic regression** — fits conversion probability from which channels were present on a
   lead's path; each channel's regression coefficient becomes its "contribution" score.
5. **Shapley-value attribution** — borrowed from cooperative game theory. Treats each channel
   as a "player" and computes its average marginal contribution to conversion across every
   possible order those channels could have been touched in. This is the most rigorous method
   here, and the one that actually corrects for assist channels being underrated by last-touch.

**A real bug I hit and fixed:** a naive Shapley implementation needs a value for "all 7
channels touched together" — but no lead in this dataset ever has more than 5 touches, so that
combination never occurs in the data. The naive version silently returned near-zero, unstable
numbers because of this. The fix: compute Shapley values *per lead*, over only the channels
that lead actually touched, so the model never needs a coalition that doesn't exist. Details
and the corrected code are in the notebook.

## Key finding

Comparing last-touch credit share to Shapley credit share across channels:

| Channel | Last-touch share | Shapley share | Change |
|---|---|---|---|
| Google Ads | 18.8% | 17.7% | **-1.1pp (over-credited)** |
| Content/Webinar | 14.8% | 17.2% | **+2.5pp (under-credited)** |
| LinkedIn Ads | 16.6% | 17.2% | +0.6pp |
| Cold Outbound | 14.8% | 14.8% | ~flat |
| Email | 14.4% | 14.1% | -0.4pp |
| Organic/SEO | 14.4% | 13.4% | -1.0pp |
| Referral | 6.3% | 5.6% | -0.6pp |

The logistic regression step independently confirms this: Content/Webinar has the strongest
coefficient (0.48) of any channel; Google Ads one of the weakest (0.06).

Cost per attributed conversion (CAC) makes the case even sharper — Google Ads costs **~$1,233**
per conversion vs. **~$169** for Content/Webinar, a 7x gap:

| Channel | CAC |
|---|---|
| Referral | $47 |
| Email | $50 |
| Organic/SEO | $103 |
| Content/Webinar | $169 |
| Cold Outbound | $593 |
| LinkedIn Ads | $655 |
| Google Ads | $1,233 |

## Recommendation

Shift budget away from Google Ads (current spend ≈ $232K/yr) — even a 20–25% cut frees up
roughly **$46K–58K/yr** — and reallocate it toward Content/Webinar production and Organic/SEO,
both of which convert at a fraction of the cost and are currently under-funded relative to
their actual (Shapley-attributed) contribution. Full writeup: [`reports/README.md`](reports/README.md).

## How to run it

```bash
git clone <this-repo-url>
cd marketing-mix-attribution
pip install -r requirements.txt
jupyter notebook notebooks/marketing_mix_attribution.ipynb
```

The data is already generated and committed (`data/*.csv`), so the notebook runs immediately.
To regenerate it from scratch: `python src/generate_data.py`.

## Repo structure

```
marketing-mix-attribution/
├── data/                   # touchpoints.csv, spend.csv
├── notebooks/              # EDA -> 5 attribution methods -> comparison -> recommendation
├── src/
│   ├── generate_data.py    # reproducible synthetic data generator (seeded)
│   └── build_notebook.py   # rebuilds the notebook from scratch
├── reports/README.md       # findings & recommendation, standalone writeup
├── requirements.txt
└── README.md                # you are here
```

## Skills demonstrated

Synthetic dataset design with embedded ground truth · multi-touch attribution modeling ·
logistic regression · Shapley values / cooperative game theory · debugging a statistical
method's edge case · translating model output into a dollar-denominated business
recommendation.
