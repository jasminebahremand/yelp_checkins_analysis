# Your Hours Aren't the Problem
**Negative Binomial Regression · Yelp Open Dataset · 103,907 businesses**

---

## Overview
The assumption was simple: businesses that stay open longer get more customers. The data said otherwise.

This project analyzes Yelp check-in data across 103,907 businesses to test whether operating hours meaningfully predict customer traffic. Built a fully reproducible pipeline from raw JSON to modeling, controlling for business type, region, ratings, and review volume.

> Full write-up available at [portfolio URL]

---

## Key Findings
- **Operating hours had a statistically significant but weak effect** on check-ins (β=0.0146, p<.001)
- **Adding controls improved model fit from 21% to 88%** (Pseudo R²: 0.21 → 0.88) — business type, region, and review count were far stronger drivers
- **Being a restaurant was the strongest predictor** (β=0.6352) — business type matters more than hours
- **Western region businesses outperformed** East and Midwest across all models

---

## Key Visuals

### Customer Traffic Varies More by Region Than by Hours
![Region Comparison](plots/region_comparison.png)

### Longer Operating Hours Do Not Strongly Increase Customer Traffic
![Hours vs Check-Ins](plots/hours_vs_checkins.png)

### Why Standard Regression Doesn't Work Here
![Check-Ins Distribution](plots/checkins_distribution.png)

Check-ins are highly skewed — a small number of businesses capture a disproportionate share of traffic. This overdispersion is why Negative Binomial Regression was used instead of OLS.

---

## Methods
- Data merging and feature engineering from raw Yelp JSON
- Exploratory Data Analysis
- Negative Binomial Regression — chosen over OLS due to count data overdispersion
- Three iterative models: simple GLM, multiple GLM with controls, interaction term model

---

## Tech Stack
Python · Pandas · Statsmodels · Matplotlib · Seaborn

---

## How to Run

```bash
pip install -r requirements.txt
python yelp_checkins_analysis.py
```

---

## Data

**Yelp Open Dataset:** https://www.yelp.com/dataset  
**Kaggle Mirror:** https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset

Download and place the following in your working directory:
- `yelp_academic_dataset_business.json`
- `yelp_academic_dataset_checkin.json`

> Dataset not included in this repo due to file size.

---

## Files
- `yelp_checkins_analysis.ipynb` — full analysis notebook
- `plots/` — generated visualizations
