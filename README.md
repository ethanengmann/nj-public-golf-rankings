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

### **`nj_public_courses_ratings.csv`**

One row per course with:


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

### **`nj_public_courses_ratings.csv`**

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

---

### **`price_lookup_curve.csv`**

A manually constructed price → value mapping:

- `sat_noon_price_usd` – representative weekend price  
- `value_score` – perceived value (1–10)

This curve was built by observing NJ public golf pricing and calibrating how much “value” each price point represents.

---

## Methodology

### **1. Golf Quality**

For each course:

```text
golf_quality = (layout_score + difficulty_score + conditions_score) / 3

**1. Golf Quality**

Saturday 12–2 PM prices are mapped to a 1–10 value scale using price_lookup_curve.csv.

This same mapping is applied:

In Excel using XLOOKUP

In Python for reproducibility

3. Final Rankings

value_score is combined with golf_quality to compute:

value_quality – price-adjusted quality

composite_score – overall score used to rank courses

rank_position – final ranking (1 = best)

All scoring is formula-driven.
Changing any course’s price or rating automatically updates rankings.

Analysis (Coming Soon)

The notebooks/ folder will include Jupyter notebooks such as:

Score and price distribution analysis

Price vs. composite score scatter plots

Top/bottom courses by individual metrics

(Optional) interactive folium map

Tech Stack

Python – analysis + potential scraping

pandas – data wrangling

matplotlib – visualization

folium – mapping (planned)

Future Work

Scrape updated pricing from course websites (where permitted)

Add additional states/regions

Incorporate online review sentiment
