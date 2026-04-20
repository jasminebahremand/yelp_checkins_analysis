# Does Staying Open Longer Drive More Customers?
**Regression Analysis · Consumer Behavior · Yelp Data**

## Overview
Analyzed Yelp business data to evaluate whether longer operating hours meaningfully increase customer traffic. Built a fully reproducible pipeline from raw JSON data to modeling, controlling for business type, region, ratings, and review volume.

> Full write-up coming soon

---

## Methods
- Data cleaning, merging, and feature engineering from raw Yelp dataset  
- Exploratory Data Analysis (EDA)  
- Negative Binomial Regression (chosen due to highly skewed count data)  
- Model comparison across three specifications (baseline, controlled, interaction model)  

---

## Key Findings
- **Operating hours have a statistically significant but weak effect** on customer traffic — increasing hours alone does not meaningfully drive more visits  
- **Model performance improves substantially after adding business context variables**, showing that factors like business type and reviews explain far more variation  
- **Being a restaurant is a strong predictor of customer traffic**, outweighing the impact of operating hours  
- **Regional differences are more important than hours**, with Western-region businesses consistently outperforming others  

---

## Tech Stack
Python · Pandas · Statsmodels · Matplotlib · Seaborn  

---

## Files
- `yelp_checkins_analysis.py` — main analysis script  
- `requirements.txt` — project dependencies  
- `plots/` — generated visualizations  

---

## Key Visual Insights

### Most Businesses Operate Within a Similar Weekly Hour Range
![Operating Hours Distribution](plots/hours_distribution.png)  
Most businesses cluster within a mid-range of weekly operating hours, with relatively few operating at very low or very high extremes.

---

### Most Businesses Receive Low Customer Traffic
![Check-Ins Distribution](plots/checkins_distribution.png)  
Customer traffic is highly uneven — most businesses receive relatively few visits, while a small number capture a disproportionately large share.

---

### Longer Operating Hours Do Not Strongly Increase Customer Traffic
![Hours vs Check-Ins](plots/hours_vs_checkins.png)  
While there is a slight positive relationship between hours and traffic, the effect is weak, indicating that simply staying open longer does not significantly increase customer visits.

---

### Customer Traffic Varies More by Region Than by Hours
![Region Comparison](plots/region_comparison.png)  
Regional differences in performance are more pronounced than the effect of operating hours, highlighting the importance of location-based factors.

---

### Model Captures Overall Trends but Not Exact Outcomes
![Model Fit](plots/model_fit.png)  
The model captures general patterns in customer traffic but cannot precisely predict individual business performance, reinforcing that unobserved factors also play a role.

---

## How to Run
```bash
pip install -r requirements.txt
python yelp_checkins_analysis.py
