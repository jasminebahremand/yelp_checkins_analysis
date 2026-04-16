import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# ----------------------------
# 1. Load data
# ----------------------------
business = pd.read_csv("yelp_business.csv")
business_hours = pd.read_csv("yelp_business_hours.csv")
checkin_raw = pd.read_csv("yelp_checkin.csv")

sns.set_theme(style="whitegrid")

# ----------------------------
# 2. Summarize check-ins
# ----------------------------
# If the file is already aggregated to one row per business, this still works
checkin_summary = (
    checkin_raw.groupby("business_id", as_index=False)["checkins"]
    .sum()
)

# ----------------------------
# 3. Convert business hours to total weekly hours
# ----------------------------
def calculate_hours(time_range: str) -> float:
    if pd.isna(time_range) or str(time_range).strip().lower() in {"none", "", "nan"}:
        return 0.0
    try:
        open_time, close_time = str(time_range).split("-")
        open_hour, open_minute = map(int, open_time.split(":"))
        close_hour, close_minute = map(int, close_time.split(":"))

        open_total = open_hour * 60 + open_minute
        close_total = close_hour * 60 + close_minute

        # handle overnight closing
        if close_total < open_total:
            close_total += 24 * 60

        return (close_total - open_total) / 60.0
    except Exception:
        return 0.0

days_of_week = [
    "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday"
]

for day in days_of_week:
    business_hours[day] = business_hours[day].apply(calculate_hours)

business_hours["total_hours_per_week"] = business_hours[days_of_week].sum(axis=1)

# keep only needed columns from hours table
business_hours_summary = business_hours[["business_id", "total_hours_per_week"]].copy()

# ----------------------------
# 4. Merge data
# ----------------------------
df = business.merge(business_hours_summary, on="business_id", how="left")
df = df.merge(checkin_summary, on="business_id", how="left")

# ----------------------------
# 5. Clean only relevant columns
# ----------------------------
# Do NOT fill every column in the whole dataframe with 0
df["checkins"] = df["checkins"].fillna(0)
df["total_hours_per_week"] = df["total_hours_per_week"].fillna(0)

# expected business fields in Yelp dataset
for col in ["stars", "review_count"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["stars"] = df["stars"].fillna(df["stars"].median())
df["review_count"] = df["review_count"].fillna(0)

# ----------------------------
# 6. Filter usable observations
# ----------------------------
# mirrors your project logic: exclude zero-hour businesses
# keep nonnegative check-ins
df = df[
    (df["total_hours_per_week"] > 0) &
    (df["checkins"] >= 0)
].copy()

# ----------------------------
# 7. Feature engineering
# ----------------------------
# Restaurant flag
if "categories" in df.columns:
    df["categories"] = df["categories"].fillna("")
    df["is_restaurant"] = df["categories"].str.contains("Restaurant", case=False, na=False).astype(int)
else:
    df["is_restaurant"] = 0

# Region mapping
# IMPORTANT: adjust this mapping if your class used a different one
west_states = {"AZ", "NV", "CA", "WA", "OR", "HI", "AK"}
middle_states = {"OH", "WI", "IL", "MI", "IN", "MN", "MO", "IA", "KS", "NE", "ND", "SD"}
east_states = {"PA", "NC", "SC", "NY", "NJ", "MA", "FL", "GA", "VA", "MD", "DC", "DE", "CT", "RI", "VT", "NH", "ME"}
canada_east = {"ON", "QC"}

def map_region(state: str) -> str:
    state = str(state).strip().upper()
    if state in west_states:
        return "West"
    if state in middle_states:
        return "Middle"
    if state in east_states or state in canada_east:
        return "East"
    return "Other"

df["region"] = df["state"].apply(map_region)

# drop "Other" so final model matches your West / Middle / East framing more closely
df = df[df["region"].isin(["West", "Middle", "East"])].copy()

# Set West as baseline
df["region"] = pd.Categorical(df["region"], categories=["West", "Middle", "East"])

# interaction terms
df["hours_stars"] = df["total_hours_per_week"] * df["stars"]
df["hours_reviews"] = df["total_hours_per_week"] * df["review_count"]

# optional: keep reviews on a smaller scale for stability
# comment out if you want raw review_count
# df["review_count"] = df["review_count"] / 100
# df["hours_reviews"] = df["total_hours_per_week"] * df["review_count"]

# ----------------------------
# 8. EDA visuals used in slides
# ----------------------------
plt.figure(figsize=(10, 5))
sns.histplot(df["total_hours_per_week"], bins=60, color="salmon")
plt.title("Frequency Distribution of Total Hours Per Week")
plt.xlabel("Total Hours Per Week")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(df["checkins"], bins=80, color="steelblue")
plt.title("Frequency Distribution of Check-Ins")
plt.xlabel("Check-Ins")
plt.ylabel("Frequency")
plt.xlim(0, min(300, df["checkins"].max()))
plt.tight_layout()
plt.show()

# ----------------------------
# 9. Model 1: simple Negative Binomial
# ----------------------------
formula_simple = "checkins ~ total_hours_per_week"

model_simple = sm.GLM.from_formula(
    formula=formula_simple,
    data=df,
    family=sm.families.NegativeBinomial()
).fit()

print("\n=== SIMPLE NEGATIVE BINOMIAL MODEL ===")
print(model_simple.summary())

# ----------------------------
# 10. Model 2: controls added
# ----------------------------
formula_controls = """
checkins ~ total_hours_per_week + stars + review_count + is_restaurant + C(region)
"""

model_controls = sm.GLM.from_formula(
    formula=formula_controls,
    data=df,
    family=sm.families.NegativeBinomial()
).fit()

print("\n=== NEGATIVE BINOMIAL MODEL WITH CONTROLS ===")
print(model_controls.summary())

# ----------------------------
# 11. Model 3: final model with interactions
# ----------------------------
formula_final = """
checkins ~ total_hours_per_week + stars + review_count + is_restaurant + C(region)
         + hours_stars + hours_reviews
"""

model_final = sm.GLM.from_formula(
    formula=formula_final,
    data=df,
    family=sm.families.NegativeBinomial()
).fit()

print("\n=== FINAL NEGATIVE BINOMIAL MODEL WITH INTERACTIONS ===")
print(model_final.summary())

# ----------------------------
# 12. Quick coefficient table
# ----------------------------
coef_table = pd.DataFrame({
    "coefficient": model_final.params,
    "p_value": model_final.pvalues,
    "ci_lower": model_final.conf_int()[0],
    "ci_upper": model_final.conf_int()[1]
}).sort_index()

print("\n=== FINAL MODEL COEFFICIENT TABLE ===")
print(coef_table)

# ----------------------------
# 13. Predicted vs observed plot
# ----------------------------
df["predicted_checkins"] = model_final.predict(df)

plt.figure(figsize=(8, 6))
plt.scatter(
    df["total_hours_per_week"],
    df["checkins"],
    alpha=0.25,
    label="Observed"
)
plt.scatter(
    df["total_hours_per_week"],
    df["predicted_checkins"],
    alpha=0.25,
    label="Predicted"
)
plt.xlabel("Total Hours Per Week")
plt.ylabel("Check-Ins")
plt.title("Negative Binomial Regression: Predicted vs Observed Check-Ins")
plt.legend()
plt.tight_layout()
plt.show()

# ----------------------------
# 14. Pull final numbers for portfolio / slides
# ----------------------------
hours_coef = model_final.params.get("total_hours_per_week", np.nan)
hours_p = model_final.pvalues.get("total_hours_per_week", np.nan)

print("\n=== FINAL TAKEAWAY ===")
print(f"Coefficient for total_hours_per_week: {hours_coef:.4f}")
print(f"P-value for total_hours_per_week: {hours_p:.6g}")

if hours_p < 0.05:
    print("Operating hours are statistically significant in the final model.")
else:
    print("Operating hours are NOT statistically significant in the final model.")

print(
    "Interpretation: the effect is positive if the coefficient is above 0, "
    "but practical impact is small if the coefficient is close to zero."
)
