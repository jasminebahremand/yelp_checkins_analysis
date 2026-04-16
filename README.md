# Yelp Check-Ins Analysis
Marketplace Analytics · Count Modeling · Business Operations

## Overview
Modeled Yelp check-ins to evaluate whether operating hours meaningfully impact customer engagement across businesses.

## Methods
- Data merging and feature engineering
- Exploratory Data Analysis
- Negative Binomial Regression
- Controlled and interaction models

## Key Findings
- Operating hours have a statistically significant but minimal impact on check-ins
- Reviews, ratings, and business type are stronger drivers of engagement
- Model performance improves significantly with controls

## Tech Stack
Python · Pandas · Statsmodels · Matplotlib · Seaborn

## Files
- yelp_checkins_analysis.py — main analysis script
- requirements.txt — project dependencies

## Plots
- hours_distribution.png
- checkins_distribution.png
- hours_vs_checkins.png
- nb_model_fit.png
- region_comparison.png

## How to Run
pip install -r requirements.txt  
python yelp_checkins_analysis.py
