#!/usr/bin/env python3
"""
Analysis script for NJ Public Golf Course Rankings.

You can:
- Run this as a script from the repo root:
    python notebooks/analysis.py
- Or copy/paste cells into a Jupyter notebook.

It expects:
- data/nj_public_courses_ranked.csv  (output of src/generate_rankings.py)
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# Configuration
# ==============================

# Resolve repo root as the parent of this file's directory
THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[1]

DATA_CSV = REPO_ROOT / "data" / "nj_public_courses_ranked.csv"

COL_COURSE = "course"
COL_COUNTY = "county"
COL_PRICE = "sat_noon_price"
COL_GOLF_QUALITY = "golf_quality"
COL_VALUE_SCORE = "value_score"
COL_VALUE_QUALITY = "value_quality"
COL_COMPOSITE = "composite_score"
COL_RANK = "rank_position"


# ==============================
# Data loading
# ==============================

def load_ranked_courses(csv_path: Path = DATA_CSV) -> pd.DataFrame:
    """Load the ranked courses CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Ranked courses file not found at {csv_path}. "
            "Make sure you've run src/generate_rankings.py first."
        )

    df = pd.read_csv(csv_path)

    # Basic sanity checks
    required_cols = [
        COL_COURSE,
        COL_PRICE,
        COL_GOLF_QUALITY,
        COL_VALUE_SCORE,
        COL_VALUE_QUALITY,
        COL_COMPOSITE,
        COL_RANK,
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns in data: {missing}")

    return df


# ==============================
# Plots
# ==============================

def plot_top_n_courses(df: pd.DataFrame, n: int = 10) -> None:
    """Horizontal bar chart for top N courses by composite_score."""
    top = df.sort_values(COL_COMPOSITE, ascending=False).head(n).copy()
    top = top.iloc[::-1]  # reverse for nicer barh ordering

    plt.figure()
    plt.barh(top[COL_COURSE], top[COL_COMPOSITE])
    plt.xlabel("Composite Score")
    plt.title(f"Top {n} NJ Public Courses by Composite Score")
    plt.tight_layout()
    plt.show()


def plot_price_vs_composite(df: pd.DataFrame) -> None:
    """Scatter plot of price vs composite_score."""
    plt.figure()
    plt.scatter(df[COL_PRICE], df[COL_COMPOSITE])
    plt.xlabel("Saturday 12–2 PM Price (USD)")
    plt.ylabel("Composite Score")
    plt.title("Price vs Composite Score")
    plt.tight_layout()
    plt.show()


def plot_distributions(df: pd.DataFrame) -> None:
    """Histograms for price, golf_quality, and composite_score."""
    # Price distribution
    plt.figure()
    plt.hist(df[COL_PRICE].dropna(), bins=15)
    plt.xlabel("Saturday 12–2 PM Price (USD)")
    plt.ylabel("Number of Courses")
    plt.title("Price Distribution")
    plt.tight_layout()
    plt.show()

    # Golf quality distribution
    plt.figure()
    plt.hist(df[COL_GOLF_QUALITY].dropna(), bins=10)
    plt.xlabel("Golf Quality Score")
    plt.ylabel("Number of Courses")
    plt.title("Golf Quality Distribution")
    plt.tight_layout()
    plt.show()

    # Composite score distribution
    plt.figure()
    plt.hist(df[COL_COMPOSITE].dropna(), bins=10)
    plt.xlabel("Composite Score")
    plt.ylabel("Number of Courses")
    plt.title("Composite Score Distribution")
    plt.tight_layout()
    plt.show()


# ==============================
# Tabular insights
# ==============================

def get_most_undervalued(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return courses that look most 'undervalued'.

    Here, 'undervalued' is approximated as:
    - High value_score (you feel you get a lot for the price)
    - Then sorted by composite_score as a tiebreaker.
    """
    subset_cols = [
        COL_COURSE,
        COL_COUNTY if COL_COUNTY in df.columns else COL_PRICE,
        COL_PRICE,
        COL_GOLF_QUALITY,
        COL_VALUE_SCORE,
        COL_COMPOSITE,
        COL_RANK,
    ]
    subset_cols = [c for c in subset_cols if c in df.columns]

    undervalued = (
        df.sort_values([COL_VALUE_SCORE, COL_COMPOSITE], ascending=[False, False])
        .head(top_n)
        .loc[:, subset_cols]
    )
    return undervalued


def get_most_overpriced(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return courses that look most 'overpriced'.

    Here, 'overpriced' is approximated as:
    - Low value_score (you feel you get less for the price)
    - Then sorted by price descending as a tiebreaker.
    """
    subset_cols = [
        COL_COURSE,
        COL_COUNTY if COL_COUNTY in df.columns else COL_PRICE,
        COL_PRICE,
        COL_GOLF_QUALITY,
        COL_VALUE_SCORE,
        COL_COMPOSITE,
        COL_RANK,
    ]
    subset_cols = [c for c in subset_cols if c in df.columns]

    overpriced = (
        df.sort_values([COL_VALUE_SCORE, COL_PRICE], ascending=[True, False])
        .head(top_n)
        .loc[:, subset_cols]
    )
    return overpriced


def print_summary(df: pd.DataFrame) -> None:
    """Print some high-level summary stats to the console."""
    num_courses = len(df)
    avg_price = df[COL_PRICE].mean()
    avg_gq = df[COL_GOLF_QUALITY].mean()
    avg_comp = df[COL_COMPOSITE].mean()

    print("===== Summary =====")
    print(f"Number of courses: {num_courses}")
    print(f"Average Saturday noon price: ${avg_price:,.2f}")
    print(f"Average golf quality score: {avg_gq:.2f}")
    print(f"Average composite score: {avg_comp:.2f}")
    print()

    print("Top 5 courses by composite_score:")
    top5 = (
        df.sort_values(COL_COMPOSITE, ascending=False)
        .head(5)[[COL_RANK, COL_COURSE, COL_COMPOSITE, COL_PRICE]]
    )
    print(top5.to_string(index=False))
    print()


# ==============================
# Main
# ==============================

def main():
    df = load_ranked_courses()

    # Console summary
    print_summary(df)

    # Plots
    plot_top_n_courses(df, n=10)
    plot_price_vs_composite(df)
    plot_distributions(df)

    # Tabular undervalued / overpriced views
    undervalued = get_most_undervalued(df, top_n=10)
    overpriced = get_most_overpriced(df, top_n=10)

    print("===== Most Undervalued Courses (by value_score) =====")
    print(undervalued.to_string(index=False))
    print()

    print("===== Most Overpriced Courses (by value_score) =====")
    print(overpriced.to_string(index=False))
    print()


if __name__ == "__main__":
    main()
