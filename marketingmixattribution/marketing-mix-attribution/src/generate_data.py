"""
generate_data.py
Generates data/touchpoints.csv and data/spend.csv for the Marketing Mix Attribution project.
Run: python src/generate_data.py
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

N_LEADS = 6000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 29)

CHANNELS = ["Referral", "Content/Webinar", "Organic/SEO", "Email", "LinkedIn Ads", "Google Ads", "Cold Outbound"]

CHANNEL_TOUCH_WEIGHTS = {
    "Referral": 0.04, "Content/Webinar": 0.12, "Organic/SEO": 0.14, "Email": 0.16,
    "LinkedIn Ads": 0.14, "Google Ads": 0.20, "Cold Outbound": 0.20,
}
TRUE_CHANNEL_POWER = {
    "Referral": 1.40, "Content/Webinar": 0.55, "Organic/SEO": 0.45, "Email": 0.60,
    "LinkedIn Ads": 0.70, "Google Ads": 0.65, "Cold Outbound": 0.20,
}
ASSIST_BOOST = {"Content/Webinar": 0.35, "Organic/SEO": 0.20}
DEAL_SIZE_RANGE = {
    "Referral": (8000, 25000), "Content/Webinar": (4000, 15000), "Organic/SEO": (3000, 12000),
    "Email": (3000, 10000), "LinkedIn Ads": (4000, 14000), "Google Ads": (3000, 11000), "Cold Outbound": (2000, 8000),
}
BASE_WEEKLY_SPEND = {
    "Referral": (50, 20), "Content/Webinar": (600, 150), "Organic/SEO": (300, 80), "Email": (150, 40),
    "LinkedIn Ads": (2200, 500), "Google Ads": (4500, 900), "Cold Outbound": (1800, 400),
}


def generate_touchpoints():
    channels = list(CHANNEL_TOUCH_WEIGHTS.keys())
    weights = np.array(list(CHANNEL_TOUCH_WEIGHTS.values()))
    weights = weights / weights.sum()
    rows = []
    span_days = (END_DATE - START_DATE).days
    for lead_id in range(1, N_LEADS + 1):
        n_touches = rng.choice([1, 2, 3, 4, 5], p=[0.30, 0.28, 0.22, 0.13, 0.07])
        path_channels = rng.choice(channels, size=n_touches, replace=True, p=weights)
        journey_start_offset = rng.integers(0, span_days - 30)
        journey_start = START_DATE + timedelta(days=int(journey_start_offset))
        t = journey_start
        touch_records = []
        for order, ch in enumerate(path_channels, start=1):
            gap_days = rng.integers(0, 6) if order > 1 else 0
            t = t + timedelta(days=int(gap_days))
            touch_records.append((ch, t, order))
        last_channel = touch_records[-1][0]
        present_channels = set(ch for ch, _, _ in touch_records)
        logit = -2.6 + TRUE_CHANNEL_POWER[last_channel]
        for ch in present_channels:
            if ch in ASSIST_BOOST:
                logit += ASSIST_BOOST[ch]
        logit += 0.08 * (n_touches - 1)
        prob = 1 / (1 + np.exp(-logit))
        converted = int(rng.random() < prob)
        if converted:
            lo, hi = DEAL_SIZE_RANGE[last_channel]
            conversion_value = round(float(rng.uniform(lo, hi)), 2)
        else:
            conversion_value = 0.0
        for ch, ts, order in touch_records:
            rows.append({"lead_id": lead_id, "channel": ch, "touchpoint_timestamp": ts.strftime("%Y-%m-%d"),
                         "touchpoint_order": order, "converted": converted, "conversion_value": conversion_value})
    return pd.DataFrame(rows)


def generate_spend():
    weeks = pd.date_range(START_DATE, END_DATE, freq="W-MON")
    rows = []
    for wk in weeks:
        for ch in CHANNELS:
            base, noise = BASE_WEEKLY_SPEND[ch]
            spend = max(0.0, rng.normal(base, noise))
            if ch in ("Referral", "Content/Webinar", "Organic/SEO"):
                outreach_volume = int(max(0, rng.normal(150, 40)))
            else:
                outreach_volume = int(max(0, spend * rng.uniform(3, 6)))
            rows.append({"channel": ch, "period": wk.strftime("%Y-%m-%d"), "spend": round(spend, 2), "outreach_volume": outreach_volume})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    touchpoints = generate_touchpoints()
    spend = generate_spend()
    touchpoints.to_csv("/home/claude/marketing-mix-attribution/data/touchpoints.csv", index=False)
    spend.to_csv("/home/claude/marketing-mix-attribution/data/spend.csv", index=False)
    print(f"Leads: {touchpoints['lead_id'].nunique()}, rows: {len(touchpoints)}, spend rows: {len(spend)}")
