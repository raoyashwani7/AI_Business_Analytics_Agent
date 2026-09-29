import streamlit as st
import requests

st.set_page_config(
    page_title="AI Business Analytics",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("🤖 AI Business Analytics Dashboard")
st.caption("AI-powered business intelligence and decision support")



st.divider()
st.subheader("📂 Select Dataset")

dataset_response = requests.get(f"{API_URL}/datasets")

if dataset_response.status_code == 200:

    datasets = dataset_response.json()["datasets"]

    selected_dataset = st.selectbox(
        "Choose the dataset you want to analyze:",
        datasets
    )

else:
    st.error("Could not load datasets.")
    selected_dataset = None
# -----------------------------
# KPI SECTION
# -----------------------------

st.subheader("📊 Business Overview")

response = requests.get(f"{API_URL}/sales/summary")

if response.status_code == 200:
    data = response.json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", data["total_orders"])
    col2.metric("Total Revenue", f"₹ {data['total_revenue']:,.0f}")
    col3.metric("Total Profit", f"₹ {data['total_profit']:,.0f}")
    col4.metric("Average Revenue", f"₹ {data['average_revenue']:,.2f}")

else:
    st.error("Could not connect to FastAPI.")


# -----------------------------
# AI BUSINESS ANALYST
# -----------------------------

st.divider()

st.subheader("🤖 Ask AI Business Analyst")

question = st.text_input(
    "Ask a business question",
    placeholder="Example: Which category generated the highest revenue?"
)

if st.button("Ask AI"):

    if not question:
        st.warning("Please enter a question.")

    else:
        with st.spinner("Analyzing business data..."):

            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question}
            )

        if response.status_code == 200:
            result = response.json()

            st.markdown("### AI Analysis")
            st.write(result["answer"])

        else:
            st.error("AI agent request failed.")


# -----------------------------
# REVENUE BY CATEGORY
# -----------------------------

st.divider()

st.subheader("📦 Revenue by Category")

from database import run_query

category_rows = run_query("""
    SELECT
        category,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY category
    ORDER BY total_revenue DESC;
""")

category_data = {
    row[0]: float(row[1])
    for row in category_rows
}

st.bar_chart(category_data)
# -----------------------------
# REVENUE BY REGION
# -----------------------------

st.subheader("🌎 Revenue by Region")

region_rows = run_query("""
    SELECT
        region,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC;
""")

region_data = {
    row[0]: float(row[1])
    for row in region_rows
}

st.bar_chart(region_data)
# -----------------------------
# MONTHLY REVENUE & PROFIT TREND
# -----------------------------

st.divider()
st.subheader("📈 Monthly Revenue & Profit Trend")

monthly_rows = run_query("""
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit
    FROM sales
    GROUP BY month
    ORDER BY month;
""")

monthly_data = {
    str(row[0])[:7]: {
        "Revenue": float(row[1]),
        "Profit": float(row[2])
    }
    for row in monthly_rows
}

st.line_chart(monthly_data)
# -----------------------------
# SALES ANOMALY ANALYSIS
# -----------------------------

st.divider()
st.subheader("🚨 Sales Anomaly Analysis")

anomaly_rows = run_query("""
    SELECT
        anomaly_flag,
        COUNT(*) AS total_orders,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY anomaly_flag
    ORDER BY total_orders DESC;
""")

anomaly_data = {
    str(row[0]): int(row[1])
    for row in anomaly_rows
}

st.bar_chart(anomaly_data)

st.write("Anomaly summary:")

for row in anomaly_rows:
    st.write(
        f"**{row[0]}** — "
        f"{row[1]} orders, "
        f"₹ {float(row[2]):,.0f} revenue"
    )

# -----------------------------
# TOP PRODUCTS
# -----------------------------

st.divider()
st.subheader("🏆 Top 10 Products by Revenue")

top_product_rows = run_query("""
    SELECT
        product,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
    LIMIT 10;
""")

top_product_data = {
    row[0]: float(row[1])
    for row in top_product_rows
}

st.bar_chart(top_product_data)

# -----------------------------
# CSV DATA UPLOAD
# -----------------------------

st.divider()
st.subheader("📤 Upload Sales CSV")

uploaded_file = st.file_uploader(
    "Upload a sales CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Upload CSV"):

        with st.spinner("Uploading CSV..."):

            response = requests.post(
                f"{API_URL}/upload-csv",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )
                }
            )

        if response.status_code == 200:
            st.success("CSV uploaded successfully!")

            result = response.json()

            st.write("**Upload Details:**")
            st.json(result)

        else:
            st.error("CSV upload failed.")
            st.write(response.text)