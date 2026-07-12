import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Forecasting Dashboard", layout="wide")

st.title("📈 Sales Forecasting Dashboard")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Demand Segments"
    ]
)
if page == "Sales Overview":

    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d/%m/%Y"
)

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%d/%m/%Y"
)
    

    yearly = (
        df.groupby(df["Order Date"].dt.year)["Sales"]
        .sum()
        .reset_index(name="Sales")
    )

    st.subheader("Total Sales by Year")

    fig = px.bar(
        yearly,
        x="Order Date",
        y="Sales"
    )

    st.plotly_chart(fig, use_container_width=True)

    monthly = (
        df.set_index("Order Date")
        .resample("ME")["Sales"]
        .sum()
        .reset_index()
    )

    st.subheader("Monthly Sales Trend")

    fig = px.line(
        monthly,
        x="Order Date",
        y="Sales"
    )

    st.plotly_chart(fig, use_container_width=True)
elif page == "Forecast Explorer":

    forecast = pd.read_csv("forecast_table.csv")

    choice = st.selectbox(
        "Select Forecast",
        [
            "Furniture",
            "Technology",
            "Office Supplies",
            "West",
            "East"
        ]
    )

    fig = px.line(
        forecast,
        x="Month",
        y=choice,
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric("Best Model", "XGBoost")
    st.metric("MAE", "15101.82")
    st.metric("RMSE", "19347.99")
elif page == "Anomaly Report":

    weekly = pd.read_csv("weekly_sales.csv")

    fig = px.line(
        weekly,
        x="Order Date",
        y="Sales"
    )

    anomaly = weekly[weekly["Anomaly"] == True]

    fig.add_scatter(
        x=anomaly["Order Date"],
        y=anomaly["Sales"],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Anomaly"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detected Anomalies")

    st.dataframe(
        anomaly[["Order Date","Sales"]]
    )
elif page == "Demand Segments":

    cluster = pd.read_csv("cluster_results.csv")

    fig = px.scatter(
        cluster,
        x="PC1",
        y="PC2",
        color="Cluster",
        hover_name="Sub-Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cluster Membership")

    st.dataframe(
        cluster[["Sub-Category","Cluster"]]
    )
