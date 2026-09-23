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
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        model = joblib.load(MODEL_PATH)
        return model

    except Exception as e:
        st.error(
            f"Unable to load ML model: {e}"
        )
        return None


# ============================================================
# LOAD ALL DATA
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

    """Return a metric value from business_summary.csv."""

    if business_summary.empty:
        return 0

    metric_column = business_summary["Metric"].astype(str).str.strip().str.lower()

    matches = business_summary.loc[
        metric_column == metric_name.strip().lower(),
        "Value"
    ]

    if matches.empty:
        return 0

    try:
        return float(
            pd.to_numeric(
                matches.iloc[0],
                errors="coerce"
            )
        )

    except Exception:
        return 0


# ============================================================
# BUSINESS KPI CALCULATIONS
# ============================================================

# Total Sessions
total_sessions = int(
    pd.to_numeric(
        repeat_session_analysis["sessions"],
        errors="coerce"
    ).sum()
)


# Converted Sessions / Orders
total_orders = int(
    get_business_metric(
        "Converted Sessions"
    )
)


# Conversion Rate
conversion_rate = (
    total_orders / total_sessions * 100
    if total_sessions > 0
    else 0
)


# Revenue per Session
revenue_per_session = get_business_metric(
    "Revenue per Session"
)


# ------------------------------------------------------------
# IMPORTANT REVENUE FIX
# ------------------------------------------------------------
#
# business_summary.csv does NOT contain a "Total Revenue"
# row.
#
# Therefore:
#
# Total Revenue =
# Total Sessions × Revenue per Session
#
# ------------------------------------------------------------

total_revenue = (
    total_sessions * revenue_per_session
)


# ============================================================
# SIDEBAR
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
# HEADER
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

    display_business_summary = business_summary.copy()

    st.dataframe(
        display_business_summary,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # IMPORTANT BUSINESS METRICS
    # --------------------------------------------------------

    st.subheader(
        "Key Business Metrics"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        average_order_value = get_business_metric(
            "Average Order Value"
        )

        st.metric(
            "Average Order Value",
            f"${average_order_value:,.2f}"
        )

    with col2:

        total_cogs = get_business_metric(
            "Total COGS"
        )

        st.metric(
            "Total COGS",
            f"${total_cogs:,.2f}"
        )

    with col3:

        gross_profit = get_business_metric(
            "Gross Profit"
        )

        st.metric(
            "Gross Profit",
            f"${gross_profit:,.2f}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        gross_margin = get_business_metric(
            "Gross Margin (%)"
        )

        st.metric(
            "Gross Margin",
            f"{gross_margin:.2f}%"
        )

    with col2:

        refund_amount = get_business_metric(
            "Total Refund Amount"
        )

        st.metric(
            "Total Refund Amount",
            f"${refund_amount:,.2f}"
        )

    with col3:

        refund_percentage = get_business_metric(
            "Refund % of Revenue"
        )

        st.metric(
            "Refund % of Revenue",
            f"{refund_percentage:.2f}%"
        )


# ============================================================
# PAGE 2 — PRODUCT PERFORMANCE
# ============================================================

elif page == "🛍️ Product Performance":

    st.header(
        "🛍️ Product Performance"
    )

    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

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
    # REVENUE BY PRODUCT
    # --------------------------------------------------------

    fig = px.bar(
        product_analysis,
        x="product_name",
        y="revenue",
        title="Revenue by Product",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Revenue",
        showlegend=False
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
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Units Sold",
        showlegend=False
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
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Gross Profit",
        showlegend=False
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

    # --------------------------------------------------------
    # REFUND TABLE
    # --------------------------------------------------------

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
    # REFUND AMOUNT
    # --------------------------------------------------------

    fig = px.bar(
        refund_analysis,
        x="product_name",
        y="refund_amount",
        title="Refund Amount by Product",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Refund Amount",
        showlegend=False
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
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Refund Rate (%)",
        showlegend=False
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

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

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
    # REVENUE BY SOURCE
    # --------------------------------------------------------

    fig = px.bar(
        marketing_analysis,
        x="reporting_utm_source",
        y="revenue",
        title="Revenue by Marketing Source",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Marketing Source",
        yaxis_title="Revenue",
        showlegend=False
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
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Marketing Source",
        yaxis_title="Conversion Rate (%)",
        showlegend=False
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

    # --------------------------------------------------------
    # DEVICE TABLE
    # --------------------------------------------------------

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
    # SESSIONS BY DEVICE
    # --------------------------------------------------------

    fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="sessions",
        title="Sessions by Device",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Device",
        yaxis_title="Sessions",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CONVERSION RATE BY DEVICE
    # --------------------------------------------------------

    fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="conversion_rate_pct",
        title="Conversion Rate by Device",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Device",
        yaxis_title="Conversion Rate (%)",
        showlegend=False
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

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

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
    # SESSION DISTRIBUTION
    # --------------------------------------------------------

    fig = px.bar(
        repeat_session_analysis,
        x="is_repeat_session",
        y="sessions",
        title="Sessions by Customer Type",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Repeat Session",
        yaxis_title="Sessions",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CONVERSION RATE
    # --------------------------------------------------------

    fig = px.bar(
        repeat_session_analysis,
        x="is_repeat_session",
        y="conversion_rate_pct",
        title="Conversion Rate by Customer Type",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Repeat Session",
        yaxis_title="Conversion Rate (%)",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REVENUE PER SESSION
    # --------------------------------------------------------

    fig = px.bar(
        repeat_session_analysis,
        x="is_repeat_session",
        y="revenue_per_session",
        title="Revenue per Session",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Repeat Session",
        yaxis_title="Revenue per Session",
        showlegend=False
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
    # HISTORICAL PREDICTION RESULTS
    # --------------------------------------------------------

    st.subheader(
        "Historical Prediction Results"
    )

    col1, col2 = st.columns(2)

    with col1:

        actual_count = (
            prediction_results["actual_conversion"]
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
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        predicted_count = (
            prediction_results["predicted_conversion"]
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
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # PREDICTION PROBABILITY
    # --------------------------------------------------------

    st.subheader(
        "Conversion Probability Distribution"
    )

    fig = px.histogram(
        prediction_results,
        x="conversion_probability",
        nbins=30,
        title="Predicted Conversion Probability"
    )

    fig.update_layout(
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
            "Live prediction is unavailable because the model could not be loaded."
        )

    else:

        st.markdown(
            "Enter session information to predict the probability of conversion."
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
        # PREDICTION BUTTON
        # ----------------------------------------------------

        if st.button(
            "🚀 Predict Conversion",
            use_container_width=True
        ):

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

                st.divider()

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
                    f"{probability * 100:.2f}%"
                )

                # =================================================
                # SPEEDOMETER / GAUGE CHART
                # =================================================

                st.subheader(
                    "🎯 Conversion Probability"
                )

                probability_percentage = (
                    probability * 100
                )

                gauge_fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=probability_percentage,
                        number={
                            "suffix": "%",
                            "font": {
                                "size": 36
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

            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Digital Analytics | "
    "SQL • Python • Power BI • Machine Learning • Streamlit"
)
