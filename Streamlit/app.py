import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Digital Analytics",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")


# ============================================================
# DATA FILE PATHS
# ============================================================

BUSINESS_SUMMARY_PATH = os.path.join(
    DATA_DIR,
    "business_summary.csv"
)

DEVICE_ANALYSIS_PATH = os.path.join(
    DATA_DIR,
    "device_analysis.csv"
)

MARKETING_ANALYSIS_PATH = os.path.join(
    DATA_DIR,
    "marketing_analysis.csv"
)

MODEL_PERFORMANCE_PATH = os.path.join(
    DATA_DIR,
    "model_performance.csv"
)

PREDICTION_RESULTS_PATH = os.path.join(
    DATA_DIR,
    "prediction_results.csv"
)

PRODUCT_ANALYSIS_PATH = os.path.join(
    DATA_DIR,
    "product_analysis.csv"
)

REFUND_ANALYSIS_PATH = os.path.join(
    DATA_DIR,
    "refund_analysis.csv"
)

REPEAT_SESSION_ANALYSIS_PATH = os.path.join(
    DATA_DIR,
    "repeat_session_analysis.csv"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "conversion_prediction_model.pkl"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    business_summary = pd.read_csv(
        BUSINESS_SUMMARY_PATH
    )

    device_analysis = pd.read_csv(
        DEVICE_ANALYSIS_PATH
    )

    marketing_analysis = pd.read_csv(
        MARKETING_ANALYSIS_PATH
    )

    model_performance = pd.read_csv(
        MODEL_PERFORMANCE_PATH
    )

    prediction_results = pd.read_csv(
        PREDICTION_RESULTS_PATH
    )

    product_analysis = pd.read_csv(
        PRODUCT_ANALYSIS_PATH
    )

    refund_analysis = pd.read_csv(
        REFUND_ANALYSIS_PATH
    )

    repeat_session_analysis = pd.read_csv(
        REPEAT_SESSION_ANALYSIS_PATH
    )

    return (
        business_summary,
        device_analysis,
        marketing_analysis,
        model_performance,
        prediction_results,
        product_analysis,
        refund_analysis,
        repeat_session_analysis
    )


# ============================================================
# LOAD ML MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)

    except Exception as e:

        st.error(
            f"Unable to load ML model: {e}"
        )

        return None


# ============================================================
# LOAD PROJECT DATA
# ============================================================

try:

    (
        business_summary,
        device_analysis,
        marketing_analysis,
        model_performance,
        prediction_results,
        product_analysis,
        refund_analysis,
        repeat_session_analysis
    ) = load_data()

except Exception as e:

    st.error(
        f"Error loading project data: {e}"
    )

    st.stop()


model = load_model()


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_business_metric(metric_name):

    if business_summary.empty:
        return 0

    metric_column = (
        business_summary["Metric"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    matches = business_summary.loc[
        metric_column == metric_name.strip().lower(),
        "Value"
    ]

    if matches.empty:
        return 0

    value = pd.to_numeric(
        matches.iloc[0],
        errors="coerce"
    )

    if pd.isna(value):
        return 0

    return float(value)


# ============================================================
# BUSINESS KPI CALCULATIONS
# ============================================================

total_sessions = int(
    pd.to_numeric(
        repeat_session_analysis["sessions"],
        errors="coerce"
    ).sum()
)


total_orders = int(
    get_business_metric(
        "Converted Sessions"
    )
)


conversion_rate = (
    total_orders / total_sessions * 100
    if total_sessions > 0
    else 0
)


revenue_per_session = get_business_metric(
    "Revenue per Session"
)


# IMPORTANT:
# business_summary.csv does not contain a direct
# "Total Revenue" row.
#
# Therefore:
#
# Total Revenue =
# Total Sessions × Revenue per Session

total_revenue = (
    total_sessions * revenue_per_session
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title(
    "🛒 E-Commerce Analytics"
)

st.sidebar.markdown(
    "### Navigation"
)

page = st.sidebar.radio(
    "Go to",
    [
        "📊 Business Overview",
        "🛍️ Product Performance",
        "💰 Refund Analysis",
        "📢 Marketing Performance",
        "📱 Device Performance",
        "🔁 Customer Sessions",
        "🤖 ML Model"
    ]
)


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title(
    "🛒 E-Commerce Digital Analytics"
)

st.markdown(
    """
    **End-to-End E-Commerce Analytics Dashboard**

    Explore business performance, product sales, refunds,
    marketing channels, device behavior, customer sessions,
    and machine learning conversion predictions.
    """
)

st.divider()


# ============================================================
# PAGE 1 — BUSINESS OVERVIEW
# ============================================================

if page == "📊 Business Overview":

    st.header(
        "Business Overview"
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Sessions",
            f"{total_sessions:,}"
        )

    with col2:

        st.metric(
            "Total Revenue",
            f"${total_revenue:,.2f}"
        )

    with col3:

        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

    with col4:

        st.metric(
            "Conversion Rate",
            f"{conversion_rate:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # BUSINESS SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "Business Summary"
    )

    st.dataframe(
        business_summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # BUSINESS METRICS
    # --------------------------------------------------------

    st.subheader(
        "Key Business Metrics"
    )

    average_order_value = get_business_metric(
        "Average Order Value"
    )

    total_cogs = get_business_metric(
        "Total COGS"
    )

    gross_profit = get_business_metric(
        "Gross Profit"
    )

    gross_margin = get_business_metric(
        "Gross Margin (%)"
    )

    refund_amount = get_business_metric(
        "Total Refund Amount"
    )

    refund_percentage = get_business_metric(
        "Refund % of Revenue"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average Order Value",
            f"${average_order_value:,.2f}"
        )

    with col2:

        st.metric(
            "Total COGS",
            f"${total_cogs:,.2f}"
        )

    with col3:

        st.metric(
            "Gross Profit",
            f"${gross_profit:,.2f}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Gross Margin",
            f"{gross_margin:.2f}%"
        )

    with col2:

        st.metric(
            "Total Refund Amount",
            f"${refund_amount:,.2f}"
        )

    with col3:

        st.metric(
            "Refund % of Revenue",
            f"{refund_percentage:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # BUSINESS KPI VISUAL
    # --------------------------------------------------------

    business_chart = pd.DataFrame(
        {
            "Metric": [
                "Sessions",
                "Orders"
            ],
            "Value": [
                total_sessions,
                total_orders
            ]
        }
    )

    fig = px.bar(
        business_chart,
        x="Metric",
        y="Value",
        title="Sessions vs Converted Sessions",
        text_auto=True
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Metric",
        yaxis_title="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 2 — PRODUCT PERFORMANCE
# ============================================================

elif page == "🛍️ Product Performance":

    st.header(
        "🛍️ Product Performance"
    )

    st.subheader(
        "Product Performance Summary"
    )

    st.dataframe(
        product_analysis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # PRODUCT SELECTOR
    # --------------------------------------------------------

    selected_product = st.selectbox(
        "Select a product",
        options=product_analysis["product_name"].tolist()
    )

    selected_product_data = product_analysis[
        product_analysis["product_name"] == selected_product
    ].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Units Sold",
            f"{int(selected_product_data['units_sold']):,}"
        )

    with col2:

        st.metric(
            "Revenue",
            f"${selected_product_data['revenue']:,.2f}"
        )

    with col3:

        st.metric(
            "Gross Profit",
            f"${selected_product_data['gross_profit']:,.2f}"
        )

    with col4:

        st.metric(
            "Gross Margin",
            f"{selected_product_data['gross_margin_pct']:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    fig = px.bar(
        product_analysis,
        x="product_name",
        y="revenue",
        title="Revenue by Product",
        text_auto=".2s",
        hover_data=[
            "units_sold",
            "cogs",
            "gross_profit",
            "gross_margin_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # UNITS SOLD
    # --------------------------------------------------------

    fig = px.bar(
        product_analysis,
        x="product_name",
        y="units_sold",
        title="Units Sold by Product",
        text_auto=True,
        hover_data=[
            "revenue",
            "gross_profit",
            "gross_margin_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Units Sold"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # GROSS PROFIT
    # --------------------------------------------------------

    fig = px.bar(
        product_analysis,
        x="product_name",
        y="gross_profit",
        title="Gross Profit by Product",
        text_auto=".2s",
        hover_data=[
            "revenue",
            "cogs",
            "gross_margin_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Gross Profit"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # GROSS MARGIN
    # --------------------------------------------------------

    fig = px.bar(
        product_analysis,
        x="product_name",
        y="gross_margin_pct",
        title="Gross Margin by Product",
        text_auto=".2f",
        hover_data=[
            "revenue",
            "gross_profit"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Gross Margin (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 3 — REFUND ANALYSIS
# ============================================================

elif page == "💰 Refund Analysis":

    st.header(
        "💰 Refund Analysis"
    )

    st.subheader(
        "Refund Summary"
    )

    st.dataframe(
        refund_analysis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # PRODUCT FILTER
    # --------------------------------------------------------

    selected_product = st.selectbox(
        "Select product",
        options=refund_analysis["product_name"].tolist()
    )

    selected_refund = refund_analysis[
        refund_analysis["product_name"] == selected_product
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Revenue",
            f"${selected_refund['revenue']:,.2f}"
        )

    with col2:

        st.metric(
            "Refund Amount",
            f"${selected_refund['refund_amount']:,.2f}"
        )

    with col3:

        st.metric(
            "Refund Rate",
            f"{selected_refund['refund_rate_pct']:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # REFUND AMOUNT
    # --------------------------------------------------------

    fig = px.bar(
        refund_analysis,
        x="product_name",
        y="refund_amount",
        title="Refund Amount by Product",
        text_auto=".2s",
        hover_data=[
            "revenue",
            "refund_count",
            "refund_rate_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Refund Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REFUND RATE
    # --------------------------------------------------------

    fig = px.bar(
        refund_analysis,
        x="product_name",
        y="refund_rate_pct",
        title="Refund Rate by Product",
        text_auto=".2f",
        hover_data=[
            "revenue",
            "refund_amount",
            "refund_count"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Refund Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REFUND COUNT
    # --------------------------------------------------------

    fig = px.bar(
        refund_analysis,
        x="product_name",
        y="refund_count",
        title="Refund Count by Product",
        text_auto=True,
        hover_data=[
            "refund_amount",
            "refund_rate_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Product",
        yaxis_title="Refund Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 4 — MARKETING PERFORMANCE
# ============================================================

elif page == "📢 Marketing Performance":

    st.header(
        "📢 Marketing Performance"
    )

    st.subheader(
        "Marketing Channel Performance"
    )

    st.dataframe(
        marketing_analysis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # SOURCE FILTER
    # --------------------------------------------------------

    selected_source = st.selectbox(
        "Select marketing source",
        options=marketing_analysis[
            "reporting_utm_source"
        ].tolist()
    )

    selected_marketing = marketing_analysis[
        marketing_analysis["reporting_utm_source"]
        == selected_source
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Sessions",
            f"{int(selected_marketing['sessions']):,}"
        )

    with col2:

        st.metric(
            "Revenue",
            f"${selected_marketing['revenue']:,.2f}"
        )

    with col3:

        st.metric(
            "Conversion Rate",
            f"{selected_marketing['conversion_rate_pct']:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    fig = px.bar(
        marketing_analysis,
        x="reporting_utm_source",
        y="revenue",
        title="Revenue by Marketing Source",
        text_auto=".2s",
        hover_data=[
            "sessions",
            "converted_sessions",
            "conversion_rate_pct",
            "revenue_per_session"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Marketing Source",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CONVERSION RATE
    # --------------------------------------------------------

    fig = px.bar(
        marketing_analysis,
        x="reporting_utm_source",
        y="conversion_rate_pct",
        title="Conversion Rate by Marketing Source",
        text_auto=".2f",
        hover_data=[
            "sessions",
            "converted_sessions",
            "revenue",
            "revenue_per_session"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Marketing Source",
        yaxis_title="Conversion Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REVENUE PER SESSION
    # --------------------------------------------------------

    fig = px.bar(
        marketing_analysis,
        x="reporting_utm_source",
        y="revenue_per_session",
        title="Revenue per Session by Marketing Source",
        text_auto=".2f",
        hover_data=[
            "sessions",
            "revenue",
            "conversion_rate_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Marketing Source",
        yaxis_title="Revenue per Session"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 5 — DEVICE PERFORMANCE
# ============================================================

elif page == "📱 Device Performance":

    st.header(
        "📱 Device Performance"
    )

    st.subheader(
        "Device Performance Summary"
    )

    st.dataframe(
        device_analysis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # DEVICE FILTER
    # --------------------------------------------------------

    selected_device = st.selectbox(
        "Select device",
        options=device_analysis[
            "reporting_device_type"
        ].tolist()
    )

    selected_device_data = device_analysis[
        device_analysis["reporting_device_type"]
        == selected_device
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Sessions",
            f"{int(selected_device_data['sessions']):,}"
        )

    with col2:

        st.metric(
            "Revenue",
            f"${selected_device_data['revenue']:,.2f}"
        )

    with col3:

        st.metric(
            "Conversion Rate",
            f"{selected_device_data['conversion_rate_pct']:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # SESSIONS
    # --------------------------------------------------------

    fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="sessions",
        title="Sessions by Device",
        text_auto=True,
        hover_data=[
            "converted_sessions",
            "revenue",
            "conversion_rate_pct",
            "revenue_per_session"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Device",
        yaxis_title="Sessions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CONVERSION RATE
    # --------------------------------------------------------

    fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="conversion_rate_pct",
        title="Conversion Rate by Device",
        text_auto=".2f",
        hover_data=[
            "sessions",
            "converted_sessions",
            "revenue"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Device",
        yaxis_title="Conversion Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="revenue",
        title="Revenue by Device",
        text_auto=".2s",
        hover_data=[
            "sessions",
            "conversion_rate_pct",
            "revenue_per_session"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Device",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 6 — CUSTOMER SESSIONS
# ============================================================

elif page == "🔁 Customer Sessions":

    st.header(
        "🔁 Customer Session Analysis"
    )

    st.subheader(
        "Repeat vs Non-Repeat Sessions"
    )

    st.dataframe(
        repeat_session_analysis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # SESSION TYPE FILTER
    # --------------------------------------------------------

    selected_session_type = st.selectbox(
        "Select session type",
        options=repeat_session_analysis[
            "is_repeat_session"
        ].tolist(),
        format_func=lambda x: (
            "Repeat Session"
            if x == 1
            else "New Session"
        )
    )

    selected_session = repeat_session_analysis[
        repeat_session_analysis["is_repeat_session"]
        == selected_session_type
    ].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Sessions",
            f"{int(selected_session['sessions']):,}"
        )

    with col2:

        st.metric(
            "Converted Sessions",
            f"{int(selected_session['converted_sessions']):,}"
        )

    with col3:

        st.metric(
            "Conversion Rate",
            f"{selected_session['conversion_rate_pct']:.2f}%"
        )

    with col4:

        st.metric(
            "Revenue / Session",
            f"${selected_session['revenue_per_session']:.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # SESSION DISTRIBUTION
    # --------------------------------------------------------

    session_chart = repeat_session_analysis.copy()

    session_chart["Session Type"] = session_chart[
        "is_repeat_session"
    ].map(
        {
            0: "New Session",
            1: "Repeat Session"
        }
    )

    fig = px.bar(
        session_chart,
        x="Session Type",
        y="sessions",
        title="Sessions by Customer Type",
        text_auto=True,
        hover_data=[
            "converted_sessions",
            "conversion_rate_pct",
            "revenue",
            "revenue_per_session"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Customer Type",
        yaxis_title="Sessions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CONVERSION RATE
    # --------------------------------------------------------

    fig = px.bar(
        session_chart,
        x="Session Type",
        y="conversion_rate_pct",
        title="Conversion Rate by Customer Type",
        text_auto=".2f",
        hover_data=[
            "sessions",
            "converted_sessions",
            "revenue"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Customer Type",
        yaxis_title="Conversion Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REVENUE PER SESSION
    # --------------------------------------------------------

    fig = px.bar(
        session_chart,
        x="Session Type",
        y="revenue_per_session",
        title="Revenue per Session by Customer Type",
        text_auto=".2f",
        hover_data=[
            "sessions",
            "revenue",
            "conversion_rate_pct"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Customer Type",
        yaxis_title="Revenue per Session"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 7 — MACHINE LEARNING MODEL
# ============================================================

elif page == "🤖 ML Model":

    st.header(
        "🤖 Conversion Prediction Model"
    )

    # --------------------------------------------------------
    # MODEL STATUS
    # --------------------------------------------------------

    if model is not None:

        st.success(
            "✅ Machine Learning model loaded successfully."
        )

    else:

        st.error(
            "❌ Machine Learning model could not be loaded."
        )

    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    st.subheader(
        "Model Performance"
    )

    st.dataframe(
        model_performance,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # MODEL PERFORMANCE CHART
    # --------------------------------------------------------

    performance_chart = model_performance.copy()

    performance_chart["Score"] = pd.to_numeric(
        performance_chart["Score"],
        errors="coerce"
    )

    fig = px.bar(
        performance_chart,
        x="Metric",
        y="Score",
        title="Model Performance Metrics",
        text_auto=".3f",
        hover_data=["Score"]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Metric",
        yaxis_title="Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # HISTORICAL PREDICTION RESULTS
    # --------------------------------------------------------

    st.subheader(
        "Historical Prediction Results"
    )

    col1, col2 = st.columns(2)

    with col1:

        actual_count = (
            prediction_results[
                "actual_conversion"
            ]
            .value_counts()
            .reset_index()
        )

        actual_count.columns = [
            "conversion",
            "count"
        ]

        fig = px.bar(
            actual_count,
            x="conversion",
            y="count",
            title="Actual Conversion Distribution",
            text_auto=True,
            hover_data=["count"]
        )

        fig.update_layout(
            hovermode="x unified",
            xaxis_title="Conversion",
            yaxis_title="Sessions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        predicted_count = (
            prediction_results[
                "predicted_conversion"
            ]
            .value_counts()
            .reset_index()
        )

        predicted_count.columns = [
            "conversion",
            "count"
        ]

        fig = px.bar(
            predicted_count,
            x="conversion",
            y="count",
            title="Predicted Conversion Distribution",
            text_auto=True,
            hover_data=["count"]
        )

        fig.update_layout(
            hovermode="x unified",
            xaxis_title="Conversion",
            yaxis_title="Sessions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # PROBABILITY DISTRIBUTION
    # --------------------------------------------------------

    st.subheader(
        "Conversion Probability Distribution"
    )

    fig = px.histogram(
        prediction_results,
        x="conversion_probability",
        nbins=30,
        title="Predicted Conversion Probability",
        marginal="box",
        hover_data=[
            "conversion_probability"
        ]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Conversion Probability",
        yaxis_title="Number of Sessions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # LIVE PREDICTION
    # ========================================================

    st.subheader(
        "🔮 Live Conversion Prediction"
    )

    if model is None:

        st.warning(
            "Live prediction is unavailable because "
            "the model could not be loaded."
        )

    else:

        st.markdown(
            """
            Enter session information below and the trained
            machine learning model will predict the probability
            that the session will convert.
            """
        )

        col1, col2 = st.columns(2)

        with col1:

            is_repeat_session = st.selectbox(
                "Repeat Session",
                options=[0, 1],
                format_func=lambda x: (
                    "Yes" if x == 1 else "No"
                )
            )

            reporting_utm_source = st.selectbox(
                "UTM Source",
                options=sorted(
                    prediction_results[
                        "reporting_utm_source"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            reporting_device_type = st.selectbox(
                "Device Type",
                options=sorted(
                    prediction_results[
                        "reporting_device_type"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            session_hour = st.slider(
                "Session Hour",
                min_value=0,
                max_value=23,
                value=12
            )

            day_of_week = st.slider(
                "Day of Week",
                min_value=0,
                max_value=6,
                value=2
            )

        with col2:

            session_month = st.slider(
                "Session Month",
                min_value=1,
                max_value=12,
                value=6
            )

            session_year = st.number_input(
                "Session Year",
                min_value=2000,
                max_value=2100,
                value=2026
            )

            utm_campaign = st.selectbox(
                "UTM Campaign",
                options=sorted(
                    prediction_results[
                        "utm_campaign"
                    ]
                    .fillna("Unknown")
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            utm_content = st.selectbox(
                "UTM Content",
                options=sorted(
                    prediction_results[
                        "utm_content"
                    ]
                    .fillna("Unknown")
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            http_referer = st.selectbox(
                "HTTP Referer",
                options=sorted(
                    prediction_results[
                        "http_referer"
                    ]
                    .fillna("Unknown")
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

        # ----------------------------------------------------
        # PREDICT BUTTON
        # ----------------------------------------------------

        predict_clicked = st.button(
            "🚀 Predict Conversion",
            use_container_width=True
        )

        if predict_clicked:

            input_data = pd.DataFrame(
                {
                    "is_repeat_session": [
                        is_repeat_session
                    ],

                    "reporting_utm_source": [
                        reporting_utm_source
                    ],

                    "utm_campaign": [
                        utm_campaign
                    ],

                    "utm_content": [
                        utm_content
                    ],

                    "reporting_device_type": [
                        reporting_device_type
                    ],

                    "http_referer": [
                        http_referer
                    ],

                    "session_hour": [
                        session_hour
                    ],

                    "day_of_week": [
                        day_of_week
                    ],

                    "session_month": [
                        session_month
                    ],

                    "session_year": [
                        session_year
                    ]
                }
            )

            try:

                prediction = model.predict(
                    input_data
                )[0]

                probability = model.predict_proba(
                    input_data
                )[0][1]

                probability_percentage = (
                    probability * 100
                )

                st.session_state[
                    "last_prediction"
                ] = int(prediction)

                st.session_state[
                    "last_probability"
                ] = probability_percentage

            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
                )

        # ----------------------------------------------------
        # SHOW PREDICTION RESULT
        # ----------------------------------------------------

        if "last_prediction" in st.session_state:

            prediction = st.session_state[
                "last_prediction"
            ]

            probability_percentage = (
                st.session_state[
                    "last_probability"
                ]
            )

            st.divider()

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            if prediction == 1:

                st.success(
                    "🎉 Prediction: Session is likely to CONVERT"
                )

            else:

                st.warning(
                    "Prediction: Session is unlikely to convert"
                )

            st.metric(
                "Conversion Probability",
                f"{probability_percentage:.2f}%"
            )

            st.divider()

            # =================================================
            # SPEEDOMETER / GAUGE
            # =================================================

            st.subheader(
                "🎯 Conversion Probability Speedometer"
            )

            gauge_fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=probability_percentage,
                    number={
                        "suffix": "%",
                        "font": {
                            "size": 42
                        }
                    },
                    title={
                        "text": "Predicted Conversion Probability"
                    },
                    gauge={
                        "axis": {
                            "range": [
                                0,
                                100
                            ],
                            "ticksuffix": "%"
                        },

                        "bar": {
                            "color": "#2563EB"
                        },

                        "steps": [
                            {
                                "range": [
                                    0,
                                    30
                                ],
                                "color": "#FEE2E2"
                            },
                            {
                                "range": [
                                    30,
                                    70
                                ],
                                "color": "#FEF3C7"
                            },
                            {
                                "range": [
                                    70,
                                    100
                                ],
                                "color": "#DCFCE7"
                            }
                        ],

                        "threshold": {
                            "line": {
                                "color": "#111827",
                                "width": 4
                            },
                            "thickness": 0.75,
                            "value": probability_percentage
                        }
                    }
                )
            )

            gauge_fig.update_layout(
                height=400,
                margin=dict(
                    l=40,
                    r=40,
                    t=80,
                    b=20
                )
            )

            st.plotly_chart(
                gauge_fig,
                use_container_width=True
            )

            # ------------------------------------------------
            # INTERPRETATION
            # ------------------------------------------------

            if probability_percentage < 30:

                st.info(
                    "📉 Low predicted conversion probability."
                )

            elif probability_percentage < 70:

                st.info(
                    "📊 Moderate predicted conversion probability."
                )

            else:

                st.success(
                    "📈 High predicted conversion probability."
                )

            # ------------------------------------------------
            # INPUT SUMMARY
            # ------------------------------------------------

            st.subheader(
                "Prediction Input Summary"
            )

            input_summary = pd.DataFrame(
                {
                    "Feature": [
                        "Repeat Session",
                        "UTM Source",
                        "UTM Campaign",
                        "UTM Content",
                        "Device Type",
                        "HTTP Referer",
                        "Session Hour",
                        "Day of Week",
                        "Session Month",
                        "Session Year"
                    ],

                    "Value": [
                        (
                            "Yes"
                            if is_repeat_session == 1
                            else "No"
                        ),
                        reporting_utm_source,
                        utm_campaign,
                        utm_content,
                        reporting_device_type,
                        http_referer,
                        session_hour,
                        day_of_week,
                        session_month,
                        session_year
                    ]
                }
            )

            st.dataframe(
                input_summary,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Digital Analytics | "
    "SQL • Python • Power BI • Machine Learning • Streamlit"
)
