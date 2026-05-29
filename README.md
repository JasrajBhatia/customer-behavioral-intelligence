# 📊 Customer Behavioral Intelligence

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://customer-behavioral-intelligence.streamlit.app)

A end-to-end customer analytics project built on Databricks, analysing 1M+ real e-commerce transactions to uncover customer behaviour patterns, predict churn and generate actionable business insights.

🔗 **[View Live Dashboard](https://customer-behavioral-intelligence.streamlit.app)**

---

## 🎯 The Business Problem

A UK-based online gift retailer had over 1 million transactions across 2 years but no clear understanding of:
- Who their most valuable customers were
- Which customers were at risk of leaving
- What drove customer behaviour and spending

Without this knowledge the business was spending marketing budget on the wrong customers and missing early warning signs of churn.

---

## 🔍 Key Findings

| Insight | Finding |
|---------|---------|
| Champion customers | 22% of customers generate 68% of all revenue |
| Churn rate | 40.85% of customers have gone inactive |
| Revenue at risk | £2.1M at risk from Medium Risk customers alone |
| Top churn predictor | Customer Lifespan is the #1 predictor of churn |
| Peak ordering day | Thursday across all customer segments |
| Seasonal pattern | Q4 revenue spike driven by Christmas wholesale buying |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data processing and machine learning |
| Databricks | Cloud analytics platform |
| Apache Spark | Large scale data processing |
| Pandas | Data manipulation and analysis |
| XGBoost | Churn prediction model |
| SHAP | Model explainability |
| Matplotlib / Seaborn | Static visualisations |
| Plotly | Interactive charts |
| Streamlit | Live dashboard deployment |
| Parquet | Efficient data storage |
| GitHub | Version control |

---

## 📁 Project Structure
customer-behavioral-intelligence/
├── 01_data_loading_and_cleaning.ipynb   # Data ingestion, cleaning, member vs guest split
├── 02_eda_and_kpis.ipynb                # Revenue trends, KPIs, top products and countries
├── 03_rfm_segmentation.ipynb            # RFM scoring and customer segmentation
├── 04_audience_profiling.ipynb          # Geographic, product and timing analysis
├── 05_churn_prediction.ipynb            # XGBoost churn model with SHAP explainability
├── app.py                               # Streamlit dashboard
├── requirements.txt                     # Python dependencies
└── README.md

---

## 📊 Project Notebooks

### Notebook 1 — Data Loading & Cleaning
- Loaded 1M+ transactions from two Excel sheets covering 2009-2011
- Separated loyalty members from guest customers
- Removed cancelled orders, invalid quantities and missing data
- Saved cleaned datasets as Parquet files for efficient loading

### Notebook 2 — EDA & KPIs
- Analysed monthly revenue trends — identified November as peak month
- Mapped revenue by country — UK accounts for 83% of total revenue
- Identified top products by revenue
- Analysed customer purchase frequency and spend distribution

### Notebook 3 — RFM Segmentation
- Calculated Recency, Frequency and Total Spend per customer
- Scored every customer 1-5 on each RFM dimension
- Segmented 5,878 customers into 8 behavioural groups
- Built segment visualisations and RFM heatmap

### Notebook 4 — Audience Profiling
- Geographic profiling — top countries per segment
- Product price tier classification — Budget, Mid Range, Premium, Luxury
- Buying behaviour analysis — bulk buyers vs premium buyers
- Purchase timing analysis — day of week and monthly patterns

### Notebook 5 — Churn Prediction
- Defined churn as 180 days of inactivity — 40.85% churn rate
- Built 12 behavioural features per customer
- Identified and fixed data leakage issue
- Trained XGBoost model — AUC 0.82, 74% accuracy
- Optimised prediction threshold from 0.5 to 0.3 — improved churn recall to 94%
- Used SHAP values to identify Customer Lifespan as top churn predictor
- Scored all 5,878 customers with churn probability and risk tiers

---

## 🚀 Running Locally

```bash
# Clone the repo
git clone https://github.com/JasrajBhatia/customer-behavioral-intelligence.git

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## 💡 Business Recommendations

- **Champions** — Launch VIP loyalty programme, send offers Tuesday/Wednesday before Thursday peak
- **At Risk** — Re-engagement campaign with personalised discount before they cross into Lost
- **Cannot Lose Them** — White glove retention — dedicated account manager and exclusive pricing
- **New Customers** — January onboarding campaign to convert seasonal buyers into year-round customers

---

## 👤 Author

**Jasraj Bhatia** — Data Analyst | Dubai, UAE

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/jasrajb2727)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/JasrajBhatia)
