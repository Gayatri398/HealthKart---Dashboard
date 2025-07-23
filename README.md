# HealthKart---Dashboard
# 📊 HealthKart Influencer Dashboard

This is a Streamlit-based dashboard to analyze HealthKart's influencer marketing data. The app visualizes key metrics like revenue, orders, payouts, and ROAS (Return on Ad Spend), and supports influencer-wise performance tracking.

---

## 🚀 Features

- Upload influencer data files (CSV)
- Track key metrics:
  - Total Revenue
  - Total Orders
  - Total Payout
  - ROAS
- View influencer-level analytics
- Download filtered results as CSV

---

## 🧠 Assumptions

- All CSVs (`influencers.csv`, `tracking_data.csv`, `payouts.csv`) contain clean, consistent, and valid data
- `influencer_id` is the common column used for merging datasets
- Revenue and order values are pre-aggregated per influencer in `tracking_data.csv`
- `posts.csv` is optional or unused in the current version but can be extended
- All currency is in INR (₹)

---

## 📂 Project Structure

