# NJ Public Golf Course Rankings

This project ranks public golf courses in New Jersey using a custom model that blends on-course quality with real-world pricing.

As a scratch golfer who has played most of these courses, I built a structured scoring system that:
- Rates **layout**, **difficulty**, and **conditions** on a 1–10 scale
- Collects **Saturday 12–2 PM prices** from course websites
- Converts prices into a **value score** using a calibrated price → value curve
- Combines golf quality and value into a final **composite score** and ranking

The goal is to turn personal golf knowledge into a reproducible, data-driven analytics project.

---

## Data

All data lives in the `data/` folder:

### `nj_public_courses_ratings.csv`

One row per course with:

- `course` – course name  
- `county` – county in New Jersey  
- `layout_score` – 1–10 rating of routing/design  
- `difficulty_score` – 1–10 rating of challenge for a scratch golfer  
- `conditions_score` – 1–10 rating of maintenance  
- `sat_noon_price` – Saturday 12–2 PM green fee (USD) from the course website  
- `value_score` – 1–10 value metric derived from the price/value curve  
- `golf_quality` – average of layout, difficulty, and conditions  
- `value_quality` – blend of golf_quality and value_score  
- `composite_score` – final overall score used for ranking  
- `rank_position` – rank (1 = best)  
- `notes` – free-text notes about the course  

### `price_lookup_curve.csv`

A manual price → value mapping:

- `sat_noon_price_usd` – representative weekend price  
- `value_score` – perceived value (1–10)

I built this curve by looking at prices on course websites and calibrating how much “value” each price point represents for NJ public golf.

---

## Methodology

1. **Golf Quality**

For each course I assign:

```text
golf_quality = (layout_score + difficulty_score + conditions_score) / 3

2. Price → Value Curve

Saturday 12–2 PM prices are mapped to a 1–10 value scale using price_lookup_curve.csv.
This same mapping is used both in Excel (via XLOOKUP) and in Python.

3. Final Rankings

value_score is combined with golf_quality to compute:

value_quality – price-adjusted quality

composite_score – overall score

rank_position – final ordering of courses

All metrics are formula-driven: if prices or scores change, rankings update automatically.


Analysis

The notebooks/ folder (coming soon) will contain Jupyter notebooks to:

Explore the distribution of scores and prices

Compare price vs. composite_score

Show the top/bottom courses by different metrics

(Optional) plot courses on a map using folium

Tech Stack

Python – analysis + future scraping

pandas – data wrangling

matplotlib – basic visualizations

folium – interactive course map (planned)

Future Work

Scrape updated pricing from course or county sites where allowed

Add additional regions/states

Incorporate online review scores and basic sentiment

Build a small web dashboard or API for querying the rankings

