#!/usr/bin/env python3
"""
Generate NJ public golf course rankings from ratings + price curve.

Usage (from repo root):

    python src/generate_rankings.py

This will:
- Read:  data/nj_public_courses_ratings.csv
- Read:  data/price_lookup_curve.csv
- Compute scores & rankings
- Write: data/nj_public_courses_ranked.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ==============================
# Configuration
# ==============================

# Paths (relative to repo root)
DATA_DIR = Path("data")
RATINGS_CSV = DATA_DIR / "nj_public_courses_ratings.csv"
PRICE_CURVE_CSV = DATA_DIR / "price_lookup_curve.csv"
OUTPUT_CSV = DATA_DIR / "nj_public_courses_ranked.csv"

# Column names (adjust here if your sheet uses different ones)
COL_COURSE = "course"
COL_PRICE = "sat_noon_price"
COL_LAYOUT = "layout_score"
COL_DIFFICULTY = "difficulty_score"
COL_CONDITIONS = "conditions_score"

COL_GOLF_QUALITY = "golf_quality"
COL_VALUE_SCORE = "value_score"
COL_VALUE_QUALITY = "value_quality"
COL_COMPOSITE = "composite_score"
COL_RANK = "rank_position"

# How to weight golf quality vs pure value when computing value_quality/composite
WEIGHT_GOLF_QUALITY = 0.7
WEIGHT_VALUE_SCORE = 0.3


# ==============================
# Core functions
# ==============================

def load_data(
    ratings_path: Path = RATINGS_CSV,
    price_curve_path: Path = PRICE_CURVE_CSV,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the ratings CSV and the price→value curve CSV."""
    if not ratings_path.exists():
        raise FileNotFoundError(f"Ratings file not found: {ratings_path}")
    if not price_curve_path.exists():
        raise FileNotFoundError(f"Price curve file not found: {price_curve_path}")

    ratings_df = pd.read_csv(ratings_path)
    price_curve_df = pd.read_csv(price_curve_path)

    return ratings_df, price_curve_df


def compute_golf_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Compute golf_quality = mean of layout, difficulty, and conditions."""
    for col in [COL_LAYOUT, COL_DIFFICULTY, COL_CONDITIONS]:
        if col not in df.columns:
            raise KeyError(f"Missing column in ratings data: '{col}'")

    df[COL_GOLF_QUALITY] = (
        df[[COL_LAYOUT, COL_DIFFICULTY, COL_CONDITIONS]]
        .astype(float)
        .mean(axis=1)
    )
    return df


def compute_value_score(
    df: pd.DataFrame,
    price_curve_df: pd.DataFrame,
    price_col: str = COL_PRICE,
    output_col: str = COL_VALUE_SCORE,
) -> pd.DataFrame:
    """
    Compute value_score for each course using the price curve.

    - price_curve_df must have:
        'sat_noon_price_usd', 'value_score'
    - Uses 1D interpolation so prices between curve points get smooth values.
    """
    required_cols = {"sat_noon_price_usd", "value_score"}
    if not required_cols.issubset(price_curve_df.columns):
        raise KeyError(
            f"Price curve CSV must contain columns: {required_cols} "
            f"but has {set(price_curve_df.columns)}"
        )

    if price_col not in df.columns:
        raise KeyError(f"Missing price column '{price_col}' in ratings data")

    # Drop rows with missing prices
    if df[price_col].isna().any():
        print("⚠️ Warning: Some rows have missing prices; value_score will be NaN for those.")

    # Sort curve by price for interpolation
    curve_sorted = price_curve_df.sort_values("sat_noon_price_usd")
    xp = curve_sorted["sat_noon_price_usd"].astype(float).values
    fp = curve_sorted["value_score"].astype(float).values

    prices = df[price_col].astype(float).values

    # Use np.interp for 1D linear interpolation, extrapolating flat at ends
    interpolated_values = np.interp(prices, xp, fp)

    df[output_col] = interpolated_values
    return df


def compute_composite_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute:
    - value_quality = blend of golf_quality and value_score
    - composite_score = same blend (you can change this if you want another formula)
    """
    for col in [COL_GOLF_QUALITY, COL_VALUE_SCORE]:
        if col not in df.columns:
            raise KeyError(f"Missing required column for scoring: '{col}'")

    gq = df[COL_GOLF_QUALITY].astype(float)
    vs = df[COL_VALUE_SCORE].astype(float)

    df[COL_VALUE_QUALITY] = (
        WEIGHT_GOLF_QUALITY * gq + WEIGHT_VALUE_SCORE * vs
    )

    # For now, composite_score is the same blend.
    # If you want a more complex formula (e.g., different weights, bonuses, penalties),
    # you can change this block.
    df[COL_COMPOSITE] = df[COL_VALUE_QUALITY]

    return df


def rank_courses(df: pd.DataFrame) -> pd.DataFrame:
    """Assign rank_position based on composite_score (1 = best)."""
    if COL_COMPOSITE not in df.columns:
        raise KeyError(f"Missing '{COL_COMPOSITE}' column; cannot rank courses.")

    # Higher composite_score = better
    df = df.sort_values(COL_COMPOSITE, ascending=False).reset_index(drop=True)
    df[COL_RANK] = df.index + 1
    return df


def save_results(df: pd.DataFrame, output_path: Path = OUTPUT_CSV) -> None:
    """Save ranked courses to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved ranked courses to: {output_path}")


def main():
    ratings_df, price_curve_df = load_data()

    print("➡️ Computing golf_quality...")
    ratings_df = compute_golf_quality(ratings_df)

    print("➡️ Computing value_score from price curve...")
    ratings_df = compute_value_score(ratings_df, price_curve_df)

    print("➡️ Computing composite scores...")
    ratings_df = compute_composite_scores(ratings_df)

    print("➡️ Ranking courses...")
    ratings_df = rank_courses(ratings_df)

    # Optional: round numeric score columns for neatness
    for col in [COL_GOLF_QUALITY, COL_VALUE_SCORE, COL_VALUE_QUALITY, COL_COMPOSITE]:
        if col in ratings_df.columns:
            ratings_df[col] = ratings_df[col].round(3)

    save_results(ratings_df, OUTPUT_CSV)


if __name__ == "__main__":
    main()
