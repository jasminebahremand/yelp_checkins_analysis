# Does Staying Open Longer Drive More Customers?
**Regression Analysis · Consumer Behavior · Yelp Data**

## Overview
Modeled Yelp check-ins across 103,907 businesses to evaluate whether operating hours meaningfully impact customer engagement, controlling for region, business type, star rating, and review count.

> Full write-up coming soon

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
![Operating Hours Distribution](plots/hours_distribution.png)
Most businesses cluster between 40–100 weekly hours, with the distribution peaking around 50 hours. Very few operate at extremes, which informed the decision to model hours as a continuous predictor rather than a categorical one.

### Distribution of Yelp Check-Ins
![Check-Ins Distribution](plots/checkins_distribution.png)
Check-ins are heavily right-skewed — the vast majority of businesses receive under 50 check-ins while a small number capture tens of thousands. This overdispersion is exactly why Negative Binomial Regression was chosen over standard OLS.

### Operating Hours vs. Check-Ins
![Hours vs Check-Ins](plots/hours_vs_checkins.png)
The scatter shows a positive but non-linear relationship between hours and check-ins, with high-checkin outliers concentrated around 75–100 weekly hours. The flat baseline confirms hours alone explain very little variance — context factors dominate.

## How to Run
```bash
pip install -r requirements.txt
python yelp_checkins_analysis.py
```

> Dataset:[ Yelp Open Dataset]([url](https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset?resource=download))
