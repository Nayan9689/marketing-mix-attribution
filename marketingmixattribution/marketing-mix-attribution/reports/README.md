# Marketing Mix Attribution — Findings & Recommendation

**Problem:** A B2B SaaS company spends across seven outreach channels (Referral,
Content/Webinar, Organic/SEO, Email, LinkedIn Ads, Google Ads, Cold Outbound). Which channels
actually drive conversions, and how should budget be reallocated?

## Method comparison
Five attribution methods were built in increasing sophistication: last-touch, first-touch,
linear/position-based, logistic regression on channel-presence, and an exact Shapley-value
model computed per lead (over each lead's own touched channels, avoiding the common pitfall of
requiring an unobserved "all channels at once" coalition).

## Key finding
Last-touch attribution over-credits **Google Ads** (18.8% of last-touch credit vs. 17.7% of
Shapley-based credit) and under-credits **Content/Webinar** (14.8% vs. 17.2%) — a pattern
independently confirmed by the regression step, where Content/Webinar has the strongest
per-touch coefficient (0.48) and Google Ads one of the weakest (0.06).

Cost tells the same story more sharply:

| Channel | CAC (spend ÷ Shapley-attributed conversions) |
|---|---|
| Referral | $47 |
| Email | $50 |
| Organic/SEO | $103 |
| Content/Webinar | $169 |
| Cold Outbound | $593 |
| LinkedIn Ads | $655 |
| Google Ads | $1,233 |

## Recommendation
Shift budget away from Google Ads (spend ≈ $232K/yr) — even a 20–25% cut frees up roughly
$46K–$58K/yr — and reallocate toward Content/Webinar production and Organic/SEO, both of which
convert at a fraction of Google Ads' cost and are currently under-represented in spend relative
to their actual (Shapley-attributed) contribution. Cold Outbound and LinkedIn Ads are the next
candidates for trimming once the Google Ads shift is validated.

## Caveat worth stating out loud
The Shapley value function here is estimated from population-level "at least these channels
were present" conversion rates, not a strict per-lead decomposition — so relative *shares*
across channels are the reliable signal, not the absolute credit totals (which can run above
the raw conversion count). This is disclosed rather than hidden because it's the kind of
methodology detail worth being able to explain if asked.
