"""
Yelp Check-Ins Analysis
Marketplace Analytics · Count Modeling · Business Operations
"""

import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

warnings.filterwarnings("ignore")

# -----------------------------
# Config
# -----------------------------
BUSINESS_PATH = "yelp_business.csv"
HOURS_PATH = "yelp_business_hours.csv"
CHECKIN_PATH = "yelp_checkin.csv"
PLOTS_DIR = "plots"

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)


# -----------------------------
# Helpers
# -----------------------------
def save_plot(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename), dpi=300, bbox_inches="tight")
    plt.close()


def calculate_hours(time_range: str) -> float:
    if pd.isna(time_range) or str(time_range).strip().lower() in {"none", "", "nan"}:
        return 0.0

    try:
        open_time, close_time = str(time_range).split("-")
        open_hour, open_minute = map(int, open_time.split(":"))
        close_hour, close_minute = map(int, close_time.split(":"))

        open_total = open_hour * 60 + open_minute
        close_total = close_hour * 60 + close_minute

        if close_total < open_total:
            close_total += 24 * 60

        return (close_total - open_total) / 60.0
    except Exception:
        return 0.0


def map_region(state: str) -> str:
    state = str(state).strip().upper()

    west_states = {"AZ", "NV", "CA", "WA", "OR", "HI", "AK"}
    middle_states = {"OH", "WI", "IL", "MI", "IN", "MN", "MO", "IA", "KS", "NE", "ND", "SD"}
    east_states = {"PA", "NC", "SC", "NY", "NJ", "MA", "FL", "GA", "VA", "MD", "DC", "DE", "CT", "RI", "VT", "NH", "ME"}
    canada_east = {"ON", "QC"}

    if state in west_states:
        return "West"
    if state in middle_states:
        return "Middle"
    if state in east_states or state in canada_east:
        return "East"
    return "Other"


# -----------------------------
# Load and prepare data
# -----------------------------
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    business = pd.read_csv(BUSINESS_PATH)
    business_hours = pd.read_csv(HOURS_PATH)
    checkin = pd.read_csv(CHECKIN_PATH)
    return business, business_hours, checkin


def prepare_data(
    business: pd.DataFrame,
    business_hours: pd.DataFrame,
    checkin: pd.DataFrame,
) -> pd.DataFrame:
    days_of_week = [
        "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"
    ]

    for day in days_of_week:
        business_hours[day] = business_hours[day].apply(calculate_hours)

    business_hours["total_hours_per_week"] = business_hours[days_of_week].sum(axis=1)
    business_hours = business_hours[["business_id", "total_hours_per_week"]].copy()

    checkin_summary = (
        checkin.groupby("business_id", as_index=False)["checkins"]
        .sum()
    )

    df = business.merge(business_hours, on="business_id", how="left")
    df = df.merge(checkin_summary, on="business_id", how="left")

    df["total_hours_per_week"] = df["total_hours_per_week"].fillna(0)
    df["checkins"] = df["checkins"].fillna(0)

    if "stars" in df.columns:
        df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
        df["stars"] = df["stars"].fillna(df["stars"].median())

    if "review_count" in df.columns:
        df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
        df["review_count"] = df["review_count"].fillna(0)

    if "categories" in df.columns:
        df["categories"] = df["categories"].fillna("")
        df["is_restaurant"] = df["categories"].str.contains("Restaurant", case=False, na=False).astype(int)
    else:
        df["is_restaurant"] = 0

    df["region"] = df["state"].apply(map_region)
    df = df[df["region"].isin(["West", "Middle", "East"])].copy()

    df = df[(df["total_hours_per_week"] > 0) & (df["checkins"] >= 0)].copy()

    df["hours_stars"] = df["total_hours_per_week"] * df["stars"]
    df["hours_reviews"] = df["total_hours_per_week"] * df["review_count"]

    df["region"] = pd.Categorical(df["region"], categories=["West", "Middle", "East"])

    return df


# -----------------------------
# Plot 1: Hours distribution
# -----------------------------
def plot_hours_distribution(df: pd.DataFrame) -> None:
    plt.figure()
    sns.histplot(df["total_hours_per_week"], bins=50)
    plt.title("Distribution of Weekly Operating Hours")
    plt.xlabel("Total Hours Per Week")
    plt.ylabel("Frequency")
    save_plot("hours_distribution.png")


# -----------------------------
# Plot 2: Check-ins distribution
# -----------------------------
def plot_checkins_distribution(df: pd.DataFrame) -> None:
    plt.figure()
    sns.histplot(df["checkins"], bins=60)
    plt.title("Distribution of Yelp Check-Ins")
    plt.xlabel("Check-Ins")
    plt.ylabel("Frequency")
    plt.xlim(0, min(300, int(df["checkins"].max())))
    save_plot("checkins_distribution.png")


# -----------------------------
# Plot 3: Hours vs check-ins
# -----------------------------
def plot_hours_vs_checkins(df: pd.DataFrame) -> None:
    plt.figure()
    plt.scatter(df["total_hours_per_week"], df["checkins"], alpha=0.2)
    plt.title("Operating Hours vs Check-Ins")
    plt.xlabel("Total Hours Per Week")
    plt.ylabel("Check-Ins")
    save_plot("hours_vs_checkins.png")


# -----------------------------
# Models
# -----------------------------
def fit_models(df: pd.DataFrame):
    formula_1 = "checkins ~ total_hours_per_week"

    formula_2 = """
    checkins ~ total_hours_per_week + stars + review_count + is_restaurant + C(region)
    """

    formula_3 = """
    checkins ~ total_hours_per_week + stars + review_count + is_restaurant + C(region)
             + hours_stars + hours_reviews
    """

    model_1 = sm.GLM.from_formula(
        formula=formula_1,
        data=df,
        family=sm.families.NegativeBinomial()
    ).fit()

    model_2 = sm.GLM.from_formula(
        formula=formula_2,
        data=df,
        family=sm.families.NegativeBinomial()
    ).fit()

    model_3 = sm.GLM.from_formula(
        formula=formula_3,
        data=df,
        family=sm.families.NegativeBinomial()
    ).fit()

    print("\nModel 1 Summary")
    print(model_1.summary())

    print("\nModel 2 Summary")
    print(model_2.summary())

    print("\nModel 3 Summary")
    print(model_3.summary())

    return model_1, model_2, model_3


# -----------------------------
# Plot 4: Final model fit
# -----------------------------
def plot_model_fit(df: pd.DataFrame, model) -> None:
    fitted = model.predict(df)

    plt.figure()
    plt.scatter(df["total_hours_per_week"], df["checkins"], alpha=0.2, label="Observed")
    plt.scatter(df["total_hours_per_week"], fitted, alpha=0.2, label="Predicted")
    plt.title("Negative Binomial Model Fit")
    plt.xlabel("Total Hours Per Week")
    plt.ylabel("Check-Ins")
    plt.legend()
    save_plot("nb_model_fit.png")


# -----------------------------
# Plot 5: Region comparison
# -----------------------------
def plot_region_comparison(df: pd.DataFrame) -> None:
    summary = (
        df.groupby("region", observed=False)["checkins"]
        .mean()
        .reset_index()
    )

    plt.figure()
    sns.barplot(data=summary, x="region", y="checkins")
    plt.title("Average Check-Ins by Region")
    plt.xlabel("Region")
    plt.ylabel("Average Check-Ins")
    save_plot("region_comparison.png")


# -----------------------------
# Run analysis
# -----------------------------
def main() -> None:
    os.makedirs(PLOTS_DIR, exist_ok=True)

    business, business_hours, checkin = load_data()
    df = prepare_data(business, business_hours, checkin)

    print("Dataset shape:", df.shape)

    plot_hours_distribution(df)
    plot_checkins_distribution(df)
    plot_hours_vs_checkins(df)

    _, _, final_model = fit_models(df)

    plot_model_fit(df, final_model)
    plot_region_comparison(df)

    print("\nDone. Plots saved to:", PLOTS_DIR)


if __name__ == "__main__":
    main()
