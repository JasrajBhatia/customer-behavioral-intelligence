import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIGURATION
# -------------------------------------------
st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
# -------------------------------------------
@st.cache_data
def load_data():
    rfm = pd.read_parquet("rfm.parquet")
    churn_scores = pd.read_parquet("churn_scores.parquet")
    df_profiling = pd.read_parquet("df_profiling.parquet")
    return rfm, churn_scores, df_profiling

rfm, churn_scores, df_profiling = load_data()


# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #2c5f8a 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
    }
    
    /* KPI metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a2e;
        color: white;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 15px;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: white !important;
    }
    
    /* Divider */
    hr {
        border-color: #e0e0e0;
    }
    
    /* Cards */
    .insight-card {
        background: white;
        border-left: 4px solid #2c5f8a;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
# -------------------------------------------
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <div style='font-size: 3rem;'>📊</div>
    <div style='color: white; font-size: 1.2rem; font-weight: bold;'>
        Customer Intelligence
    </div>
    <div style='color: #a0b0c0; font-size: 0.8rem;'>
        Analytics Platform
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("**Project:** Customer Behavioral Intelligence")
st.sidebar.markdown("**Data:** 1M+ E-Commerce Transactions")
st.sidebar.markdown("**Period:** Dec 2009 — Dec 2011")
st.sidebar.markdown("**Built on:** Databricks · Python · XGBoost")

st.sidebar.divider()
page = st.sidebar.radio("Go to", [
    "📋 Project Overview",
    "📊 Business KPIs",
    "👥 Customer Segments",
    "🌍 Audience Profiling",
    "⚠️ Churn Prediction",
    "💡 Recommendations"
])


# PAGE 1: PROJECT OVERVIEW
# -------------------------------------------
if page == "📋 Project Overview":
    st.title("📋 Project Overview")
    st.markdown("### Why this project was built")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 🎯 The Business Problem
        A UK-based online gift retailer had over **1 million transactions**
        across 2 years but no clear understanding of:
        - Who their most valuable customers were
        - Which customers were at risk of leaving
        - What drove customer behaviour and spending

        Without this knowledge the business was:
        - Spending marketing budget on the wrong customers
        - Missing early warning signs of customer churn
        - Unable to personalise retention strategies
        """)

    with col2:
        st.markdown("""
        #### 🔍 What We Set Out to Find
        1. **Segment** customers by buying behaviour using RFM analysis
        2. **Profile** each segment — who they are, what they buy, when they buy
        3. **Predict** which customers are likely to churn before they leave
        4. **Quantify** the revenue at risk from churning customers
        5. **Recommend** targeted retention strategies per segment
        """)

    st.divider()

    st.markdown("### 📌 Key Findings at a Glance")

    col1, col2, col3, col4 = st.columns(4)
    col1.info("**22% of customers** (Champions) generate **68% of all revenue**")
    col2.warning("**40.85% churn rate** — 4 in 10 customers have gone inactive")
    col3.error("**£2.1M revenue** at risk from Medium Risk customers alone")
    col4.success("**Customer Lifespan** is the #1 predictor of churn")

    st.divider()

    st.markdown("### 🛠️ How We Built It")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown("**Step 1**\n\nData Loading & Cleaning\n\n1M+ rows cleaned and validated")
    col2.markdown("**Step 2**\n\nEDA & KPIs\n\nRevenue trends, top products, countries")
    col3.markdown("**Step 3**\n\nRFM Segmentation\n\n5,878 customers scored and segmented")
    col4.markdown("**Step 4**\n\nAudience Profiling\n\nGeographic, product and timing analysis")
    col5.markdown("**Step 5**\n\nChurn Prediction\n\nXGBoost model with 82% AUC score")

# PAGE 2: BUSINESS KPIs
# -------------------------------------------
elif page == "📊 Business KPIs":
    st.title("📊 Business KPIs")
    st.markdown("High level performance metrics across the entire customer base")
    st.divider()

    # KPI Row 1
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Customers", f"{len(rfm):,}")
    col2.metric("Total Revenue", f"£{rfm['TotalSpend'].sum():,.0f}")
    col3.metric("Avg Revenue/Customer", f"£{rfm['TotalSpend'].mean():,.0f}")
    col4.metric("Median Revenue/Customer", f"£{rfm['TotalSpend'].median():,.0f}")
    col5.metric("Churn Rate", "40.85%", delta="-40.85%", delta_color="inverse")

    st.divider()

    col1, col2 = st.columns(2)

    # Revenue by segment
    with col1:
        st.markdown("#### Revenue Distribution by Segment")
        st.caption("Champions generate 68% of all revenue despite being only 22% of customers")
        segment_revenue = rfm.groupby('Segment')['TotalSpend'].sum().reset_index()
        segment_revenue.columns = ['Segment', 'Revenue']
        segment_revenue['Revenue_Pct'] = (
            segment_revenue['Revenue'] / segment_revenue['Revenue'].sum() * 100
        ).round(1)
        fig = px.pie(
            segment_revenue,
            values='Revenue',
            names='Segment',
            title='Revenue Share by Segment',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # Customer distribution
    with col2:
        st.markdown("#### Customer Distribution by Segment")
        st.caption("Lost and Champion segments are almost equal in size but generate vastly different revenue")
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        fig2 = px.pie(
            segment_counts,
            values='Count',
            names='Segment',
            title='Customer Share by Segment',
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # RFM Summary Stats
    st.markdown("#### RFM Summary Statistics")
    st.caption("Understanding the typical customer across recency, frequency and spend")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📅 Recency")
        st.caption("""
        **How many days ago did each customer last buy?**
        Lower = better. A customer who bought 5 days ago 
        is far more engaged than one who bought 300 days ago.
        Most active customers cluster near 0.
        """)
        fig = px.histogram(rfm, x='Recency', nbins=50,
            title='Days Since Last Purchase',
            color_discrete_sequence=['#4C72B0'])
        fig.update_layout(xaxis_title="Days Since Last Purchase",
            yaxis_title="Number of Customers")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🔁 Frequency")
        st.caption("""
        **How many orders has each customer placed in total?**
        Higher = more loyal. Most customers placed 1-5 orders.
        A small group of highly loyal customers placed 
        50-400 orders — these are your wholesale Champions.
        """)
        fig = px.histogram(rfm, x='Frequency', nbins=50,
            title='Number of Orders Placed',
            color_discrete_sequence=['#2ecc71'])
        fig.update_layout(xaxis_title="Number of Orders",
            yaxis_title="Number of Customers")
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("#### 💰 Total Spend")
        st.caption("""
        **How much has each customer spent in total?**
        Most customers spent under £5,000. A small group 
        of high value customers spent significantly more —
        up to £608,000. These outliers drive the 
        average spend up significantly.
        """)
        fig = px.histogram(rfm, x='TotalSpend', nbins=50,
            title='Total Revenue per Customer (£)',
            color_discrete_sequence=['#e74c3c'])
        fig.update_layout(xaxis_title="Total Spend (£)",
            yaxis_title="Number of Customers")
        st.plotly_chart(fig, use_container_width=True)

# PAGE 3: CUSTOMER SEGMENTS
# -------------------------------------------
elif page == "👥 Customer Segments":
    st.title("👥 Customer Segments")
    st.markdown("Customers segmented using **RFM Analysis** — Recency, Frequency and Monetary value")
    st.divider()

    # Segment filter
    selected_segment = st.selectbox(
        "Select a segment to explore:",
        ["All Segments"] + list(rfm['Segment'].unique())
    )

    if selected_segment != "All Segments":
        filtered_rfm = rfm[rfm['Segment'] == selected_segment]
    else:
        filtered_rfm = rfm

    # Segment metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers", f"{len(filtered_rfm):,}")
    col2.metric("Total Revenue", f"£{filtered_rfm['TotalSpend'].sum():,.0f}")
    col3.metric("Avg Recency", f"{filtered_rfm['Recency'].mean():.0f} days")
    col4.metric("Avg Frequency", f"{filtered_rfm['Frequency'].mean():.1f} orders")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Customer Count per Segment")
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        fig = px.bar(segment_counts, x='Segment', y='Count',
            color='Segment', text='Count',
            title='How many customers in each segment?')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Revenue per Segment")
        segment_revenue = rfm.groupby('Segment')['TotalSpend'].sum().reset_index()
        segment_revenue.columns = ['Segment', 'Revenue']
        segment_revenue = segment_revenue.sort_values('Revenue', ascending=False)
        fig2 = px.bar(segment_revenue, x='Segment', y='Revenue',
            color='Segment',
            text=segment_revenue['Revenue'].apply(lambda x: f'£{x:,.0f}'),
            title='How much revenue does each segment generate?')
        fig2.update_traces(textposition='outside')
        fig2.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # RFM Scatter
    st.markdown("#### RFM Scatter Plot — Frequency vs Total Spend")
    st.caption("Each dot is one customer — colour shows their segment")
    fig3 = px.scatter(
        rfm,
        x='Frequency',
        y='TotalSpend',
        color='Segment',
        size='TotalSpend',
        hover_data=['Customer ID', 'Recency'],
        title='Customer Frequency vs Total Spend by Segment',
        size_max=30
    )
    st.plotly_chart(fig3, use_container_width=True)

# PAGE 4: AUDIENCE PROFILING
# -------------------------------------------
elif page == "🌍 Audience Profiling":
    st.title("🌍 Audience Profiling")
    st.markdown("Understanding **who customers are, where they come from and how they buy**")
    st.divider()

    # Segment filter
    selected_segment = st.selectbox(
        "Filter by segment:",
        ["All Segments"] + list(rfm['Segment'].unique())
    )

    if selected_segment != "All Segments":
        filtered_profiling = df_profiling[df_profiling['Segment'] == selected_segment]
    else:
        filtered_profiling = df_profiling

    col1, col2 = st.columns(2)

    # Geographic distribution
    with col1:
        st.markdown("#### Top 10 Countries by Revenue")
        st.caption("Where does revenue come from geographically?")
        country_rev = filtered_profiling.groupby('Country')['TotalRevenue'].sum().reset_index()
        country_rev = country_rev.sort_values('TotalRevenue', ascending=False).head(10)
        fig = px.bar(country_rev, x='TotalRevenue', y='Country',
            orientation='h',
            title='Revenue by Country',
            color='TotalRevenue',
            color_continuous_scale='Blues')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # Purchase timing
    with col2:
        st.markdown("#### Orders by Day of Week")
        st.caption("When do customers place orders?")
        df_profiling['DayOfWeek'] = pd.to_datetime(
            df_profiling['InvoiceDate']).dt.day_name()
        day_order = ['Monday','Tuesday','Wednesday',
                     'Thursday','Friday','Saturday','Sunday']
        day_counts = filtered_profiling.copy()
        day_counts['DayOfWeek'] = pd.to_datetime(
            day_counts['InvoiceDate']).dt.day_name()
        day_counts = day_counts.groupby('DayOfWeek')['Invoice'].nunique().reset_index()
        day_counts.columns = ['DayOfWeek', 'Orders']
        day_counts['DayOfWeek'] = pd.Categorical(
            day_counts['DayOfWeek'], categories=day_order, ordered=True)
        day_counts = day_counts.sort_values('DayOfWeek')
        fig2 = px.bar(day_counts, x='DayOfWeek', y='Orders',
            title='Order Volume by Day of Week',
            color='Orders', color_continuous_scale='Greens')
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Top products
    st.markdown("#### Top 10 Products by Revenue")
    st.caption("Which products generate the most revenue for the selected segment?")
    product_rev = filtered_profiling.groupby(
        'Description')['TotalRevenue'].sum().reset_index()
    product_rev = product_rev.sort_values('TotalRevenue', ascending=False).head(10)
    fig3 = px.bar(product_rev, x='TotalRevenue', y='Description',
        orientation='h',
        title='Top 10 Products by Revenue',
        color='TotalRevenue',
        color_continuous_scale='Purples')
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

    # Purchase timing
    st.divider()
    st.markdown("#### Peak ordering day across all segments")
    st.caption("Thursday is consistently the highest ordering day regardless of customer segment")

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    all_day_counts = df_profiling.copy()
    all_day_counts['DayOfWeek'] = pd.to_datetime(
        all_day_counts['InvoiceDate']).dt.day_name()
    all_day_counts = all_day_counts.groupby(
        'DayOfWeek')['Invoice'].nunique().reset_index()
    all_day_counts.columns = ['DayOfWeek', 'Orders']
    all_day_counts['DayOfWeek'] = pd.Categorical(
        all_day_counts['DayOfWeek'], categories=day_order, ordered=True)
    all_day_counts = all_day_counts.sort_values('DayOfWeek')

    fig_day = px.bar(
        all_day_counts,
        x='DayOfWeek',
        y='Orders',
        title='Total Orders by Day of Week — All Customers',
        color='Orders',
        color_continuous_scale='Blues',
        text='Orders'
    )
    fig_day.update_traces(textposition='outside')
    fig_day.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_day, use_container_width=True)

    st.info("Thursday is peak ordering day across every customer segment — promotional campaigns sent on Tuesday or Wednesday would catch customers before their peak buying day.")

# PAGE 5: CHURN PREDICTION
# -------------------------------------------
elif page == "⚠️ Churn Prediction":
    st.title("⚠️ Churn Prediction")
    st.markdown("Using **XGBoost Machine Learning** to identify customers at risk of leaving")
    st.divider()

    # Model performance
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Model AUC Score", "0.82", help="How well the model separates churned from active customers. 1.0 = perfect")
    col2.metric("Overall Accuracy", "74%")
    col3.metric("Churn Recall", "94%", help="Of all customers who actually churned, the model caught 94%")
    col4.metric("Churn Threshold", "0.3", help="Optimised from default 0.5 to catch more at-risk customers")

    st.divider()

    # Risk tier overview
    st.markdown("#### Churn Risk Tier Summary")
    st.caption("Every customer scored with a churn probability and grouped into risk tiers")

    col1, col2, col3 = st.columns(3)

    high_risk = churn_scores[churn_scores['Risk_Tier'] == 'High Risk']
    med_risk = churn_scores[churn_scores['Risk_Tier'] == 'Medium Risk']
    low_risk = churn_scores[churn_scores['Risk_Tier'] == 'Low Risk']

    col1.error(f"🔴 High Risk\n\n**{len(high_risk):,} customers**\n\n£{high_risk['TotalSpend'].sum():,.0f} revenue at risk")
    col2.warning(f"🟡 Medium Risk\n\n**{len(med_risk):,} customers**\n\n£{med_risk['TotalSpend'].sum():,.0f} revenue at risk")
    col3.success(f"🟢 Low Risk\n\n**{len(low_risk):,} customers**\n\n£{low_risk['TotalSpend'].sum():,.0f} revenue at risk")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Customers per Risk Tier")
        risk_counts = churn_scores['Risk_Tier'].value_counts().reset_index()
        risk_counts.columns = ['Risk_Tier', 'Count']
        colors = {'High Risk': '#e74c3c',
                  'Medium Risk': '#f39c12',
                  'Low Risk': '#2ecc71'}
        fig = px.bar(risk_counts, x='Risk_Tier', y='Count',
            color='Risk_Tier',
            color_discrete_map=colors,
            text='Count',
            title='How many customers in each risk tier?')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Revenue at Risk per Tier")
        risk_revenue = churn_scores.groupby(
            'Risk_Tier')['TotalSpend'].sum().reset_index()
        fig2 = px.bar(risk_revenue, x='Risk_Tier', y='TotalSpend',
            color='Risk_Tier',
            color_discrete_map=colors,
            text=risk_revenue['TotalSpend'].apply(lambda x: f'£{x:,.0f}'),
            title='How much revenue is at risk in each tier?')
        fig2.update_traces(textposition='outside')
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # High risk customers table
    st.markdown("#### High Risk Customers — Priority Retention List")
    st.caption("These customers have the highest probability of churning — contact them first")

    risk_filter = st.selectbox(
        "Filter by risk tier:",
        ["High Risk", "Medium Risk", "Low Risk"]
    )

    filtered_churn = churn_scores[
        churn_scores['Risk_Tier'] == risk_filter
    ].sort_values('Churn_Probability', ascending=False)

    st.dataframe(
        filtered_churn[[
            'Customer ID', 'Segment',
            'Churn_Probability', 'Risk_Tier', 'TotalSpend'
        ]].head(20).style.format({
            'Churn_Probability': '{:.1%}',
            'TotalSpend': '£{:,.2f}'
        }),
        use_container_width=True
    )

    # SHAP Insight
    st.divider()
    st.markdown("#### What drives churn the most?")
    st.caption("Based on SHAP values from the XGBoost model — features ranked by their impact on churn predictions")

    shap_data = pd.DataFrame({
        'Feature': [
            'Customer Lifespan',
            'Avg Quantity',
            'Unique Products',
            'Avg Order Value',
            'Frequency',
            'Total Spend',
            'F Score',
            'Unique Countries',
            'S Score'
        ],
        'Importance': [1.95, 0.28, 0.22, 0.20, 0.12, 0.10, 0.04, 0.01, 0.01]
    })

    fig = px.bar(
        shap_data.sort_values('Importance'),
        x='Importance',
        y='Feature',
        orientation='h',
        title='Feature Importance — What predicts churn?',
        color='Importance',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("Customer Lifespan is by far the strongest predictor — customers with a short history between their first and last purchase are significantly more likely to churn.")

# PAGE 6: RECOMMENDATIONS
# -------------------------------------------
elif page == "💡 Recommendations":
    st.title("💡 Business Recommendations")
    st.markdown("Actionable strategies based on the analysis — **what to do with each segment**")
    st.divider()

    st.markdown("### 🏆 Champions — 1,294 customers | £12.1M revenue")
    st.success("""
    **Strategy: Reward and Retain**
    - Launch a VIP loyalty programme exclusively for Champions
    - Give early access to new products before general release
    - Send personalised thank you communications
    - Ask for reviews and referrals — they're your best brand ambassadors
    - **Campaign timing:** Send offers on Tuesday/Wednesday before their Thursday peak ordering day
    """)

    st.markdown("### ⚠️ At Risk — 612 customers | £1.5M revenue")
    st.warning("""
    **Strategy: Re-engagement Campaign**
    - These customers used to buy regularly but have gone quiet
    - Send a personalised "We miss you" campaign with a targeted discount
    - Highlight new products in categories they previously bought
    - Set up automated alerts when an At Risk customer hasn't ordered in 60 days
    - **Urgency:** Act before they cross into the Lost segment
    """)

    st.markdown("### 🚨 Cannot Lose Them — 248 customers | £339K revenue")
    st.error("""
    **Strategy: White Glove Retention**
    - These are premium buyers (avg £94 per unit) going inactive
    - Assign a dedicated account manager to each one
    - Offer exclusive pricing or bulk order incentives
    - Personal phone call outreach — not just email
    - **Priority:** Despite small numbers these customers spend the most per order
    """)

    st.markdown("### 🌱 New Customers — 441 customers | £394K revenue")
    st.info("""
    **Strategy: Onboarding to Loyalty**
    - Most new customers only appear in November/December — seasonal buyers
    - Send a welcome series immediately after first order
    - Offer a January incentive to convert seasonal buyers into year-round customers
    - Introduce them to the full product catalogue — they typically buy only one category
    - **Goal:** Convert seasonal buyers into Loyal Customers within 90 days
    """)

    st.divider()

    st.markdown("### 📊 Revenue Impact Summary")
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue Protected if 10% of At Risk retained",
        f"£{1545073 * 0.1:,.0f}"
    )
    col2.metric(
        "Revenue Protected if 10% of Cannot Lose Them retained",
        f"£{339478 * 0.1:,.0f}"
    )
    col3.metric(
        "Total Medium Risk Revenue at Stake",
        "£2,127,037"
    )