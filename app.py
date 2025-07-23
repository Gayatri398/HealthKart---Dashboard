import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HealthKart Influencer Dashboard", layout="wide")
st.title("📊 HealthKart Influencer Campaign Dashboard")

# File upload section
st.sidebar.header("Upload Your Data")
influencers_file = st.sidebar.file_uploader("Upload influencers.csv", type="csv")
posts_file = st.sidebar.file_uploader("Upload posts.csv", type="csv")
tracking_file = st.sidebar.file_uploader("Upload tracking_data.csv", type="csv")
payouts_file = st.sidebar.file_uploader("Upload payouts.csv", type="csv")

# Load datasets
if influencers_file and posts_file and tracking_file and payouts_file:
    influencers = pd.read_csv(influencers_file)
    posts = pd.read_csv(posts_file)
    tracking = pd.read_csv(tracking_file)
    payouts = pd.read_csv(payouts_file)

    # Merge Data
    # merged = tracking.merge(influencers, on='influencer_id')
    # merged = merged.merge(payouts, on='influencer_id')
    merged = tracking.merge(influencers, on='influencer_id')
    payouts_filtered = payouts[['influencer_id', 'basis', 'rate', 'total_payout']]  # Exclude 'orders'
    merged = merged.merge(payouts_filtered, on='influencer_id')


    st.header("🔍 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"₹{merged['revenue'].sum():,.0f}")
    with col2:
        st.metric("Total Orders", int(merged['orders'].sum()))
    with col3:
        st.metric("Total Payout", f"₹{merged['total_payout'].sum():,.0f}")
    with col4:
        roas = merged['revenue'].sum() / merged['total_payout'].sum()
        st.metric("ROAS", f"{roas:.2f}")

    # ROAS per Influencer
    st.subheader("📈 ROAS by Influencer")
    merged['ROAS'] = merged['revenue'] / merged['total_payout']
    roas_chart = px.bar(merged.groupby('name')['ROAS'].mean().sort_values(ascending=False).reset_index(),
                        x='name', y='ROAS', title="ROAS per Influencer")
    st.plotly_chart(roas_chart, use_container_width=True)

    # Revenue by Platform
    st.subheader("💰 Revenue by Platform")
    platform_chart = px.pie(merged, names='platform', values='revenue', title="Revenue Distribution")
    st.plotly_chart(platform_chart, use_container_width=True)

    # Payout vs Revenue Table
    st.subheader("📋 Payout vs Revenue Table")
    summary = merged.groupby(['name', 'platform']).agg({
        'revenue': 'sum',
        'total_payout': 'sum',
        'orders': 'sum'
    }).reset_index()
    summary['ROAS'] = summary['revenue'] / summary['total_payout']
    st.dataframe(summary)

    # Filter Section
    st.sidebar.header("🔎 Filters")
    selected_platform = st.sidebar.selectbox("Filter by Platform", options=["All"] + list(influencers['platform'].unique()))
    if selected_platform != "All":
        merged = merged[merged['platform'] == selected_platform]

    # Downloadable Insights
    st.subheader("⬇️ Export Data")
    csv = summary.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Summary CSV",
        data=csv,
        file_name='campaign_summary.csv',
        mime='text/csv'
    )
else:
    st.info("Please upload all required CSV files from the sidebar to proceed.")
