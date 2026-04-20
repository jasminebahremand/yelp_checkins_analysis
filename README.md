# Your Hours Aren't the Problem
**Negative Binomial Regression · Yelp Open Dataset · 103,907 businesses**

---

## Overview
The assumption was simple: businesses that stay open longer get more customers. The data said otherwise.

This project analyzes Yelp check-in data across 103,907 businesses to test whether operating hours meaningfully predict customer traffic. Built a fully reproducible pipeline from raw JSON to modeling, controlling for business type, region, ratings, and review volume.

---

## What I Found
Operating hours have a statistically significant but weak effect on traffic. The real drivers are business type, review volume, and region — factors that longer hours cannot compensate for.

Specifically:
- Being a restaurant predicts traffic far more than any number of additional hours open
- Western-region businesses consistently outperform other regions regardless of hours
- Model fit jumped from Pseudo R²=0.21 to 0.88 after adding business context variables — hours alone explain almost nothing

The practical takeaway: if a business wants more foot traffic, staying open later is the least efficient lever available.

---

## Methods
- Data cleaning, merging, and feature engineering from raw Yelp JSON
- Exploratory Data Analysis
- Negative Binomial Regression — chosen for highly skewed count data where OLS breaks down
- Three model specifications: baseline, controlled, and interaction

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
- `yelp_checkins_analysis.py` — main analysis script
- `requirements.txt` — dependencies
- `plots/` — generated visualizations
