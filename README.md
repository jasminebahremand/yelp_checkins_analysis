The Impact of Operating Hours on Yelp Check-Ins

Marketplace Analytics · Count Modeling · Business Operations

Overview

This project analyzes how a business’s total weekly operating hours relate to customer engagement, measured by Yelp check-ins. The goal was to determine whether extending hours meaningfully increases check-in activity or if other factors play a larger role.

Objective

For local businesses, increasing operating hours can be costly. This analysis evaluates whether longer hours are associated with higher check-in volume and whether this relationship holds after accounting for business characteristics.

Dataset

Yelp dataset including:
	•	Business information (location, ratings, categories)
	•	Operating hours by day of week
	•	Check-in counts

Methodology
	•	Merged business, hours, and check-in data at the business level
	•	Created total weekly operating hours as the primary independent variable
	•	Performed exploratory data analysis to understand distributions and skewness
	•	Modeled check-ins using Negative Binomial Regression (appropriate for overdispersed count data)
	•	Estimated three models:
	•	Baseline model (hours only)
	•	Controlled model (adding ratings, reviews, business type, and region)
	•	Final model with interaction terms

Key Findings
	•	Operating hours have a statistically significant but very small impact on check-ins
	•	Business characteristics (reviews, ratings, category) explain more variation than hours alone
	•	Model performance improves substantially after adding controls and interactions

Conclusion

Extending operating hours alone is unlikely to meaningfully increase customer engagement. Businesses may benefit more from improving visibility, increasing reviews, and optimizing customer experience rather than simply staying open longer.

Tech Stack

Python · Pandas · Statsmodels · Matplotlib · Seaborn

Repository Structure

yelp-checkins-analysis/
├── yelp_checkins_analysis.py
├── README.md
├── requirements.txt
├── plots/
└── data/ (optional)

How to Run
	1.	Install dependencies
pip install -r requirements.txt
	2.	Run the analysis
python yelp_checkins_analysis.py

Notes

This project analyzes relationships in observational data and identifies associations rather than causal effects.
