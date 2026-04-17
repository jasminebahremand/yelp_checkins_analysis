# Does Staying Open Longer Drive More Customers?
**Regression Analysis · Consumer Behavior · Yelp Data**

## Overview
Modeled Yelp check-ins across 103,907 businesses to evaluate whether operating hours meaningfully impact customer engagement, controlling for region, business type, star rating, and review count.

> Full write-up available at [portfolio URL]

## Methods
- Data merging and feature engineering
- Exploratory Data Analysis
- Negative Binomial Regression (chosen over OLS due to count data overdispersion)
- Three iterative models: simple GLM, multiple GLM with controls, interaction term model

## Key Findings
- **Operating hours had a statistically significant but weak effect** on check-ins (β=0.0146, p<.001)
- **Adding controls improved model fit from 21% to 88%** (Pseudo R²: 0.21 → 0.88) — business type, region, and review count were far stronger drivers
- **Being a restaurant was the strongest predictor** (β=0.6352) — business type matters more than hours
- **Western region businesses outperformed** East and Midwest across all models

## Tech Stack
Python · Pandas · Statsmodels · Matplotlib · Seaborn

## Files
- `yelp_checkins_analysis.py` — main analysis script
- `requirements.txt` — project dependencies

## Key Visual Insights

### Distribution of Weekly Operating Hours
![Hours Distribution](plots/hours_distribution.png)
Most businesses operate within a mid-range of weekly hours, with fewer operating at very low or very high extremes.

### Distribution of Yelp Check-Ins
![Check-Ins Distribution](plots/checkins_distribution.png)
Check-ins are highly skewed, with a small number of businesses capturing a disproportionate share of customer activity.

### Operating Hours vs. Check-Ins
![Hours vs Check-Ins](plots/hours_vs_checkins.png)
Operating hours show a positive but non-linear relationship with check-ins, supporting the use of count-based models (Negative Binomial).

## How to Run
```bash
pip install -r requirements.txt
python yelp_checkins_analysis.py
```

## Data
Dataset: [Yelp Open Dataset](https://www.yelp.com/dataset)
