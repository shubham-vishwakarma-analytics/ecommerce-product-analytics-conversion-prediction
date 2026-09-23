import os
import joblib
import numpy as np
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
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    business_summary = pd.read_csv(
        os.path.join(DATA_DIR, "business_summary.csv")
    )

    device_analysis = pd.read_csv(
        os.path.join(DATA_DIR, "device_analysis.csv")
    )

    marketing_analysis = pd.read_csv(
        os.path.join(DATA_DIR, "marketing_analysis.csv")
    )

    model_performance = pd.read_csv(
        os.path.join(DATA_DIR, "model_performance.csv")
    )

    prediction_results = pd.read_csv(
        os.path.join(DATA_DIR, "prediction_results.csv")
    )

    product_analysis = pd.read_csv(
        os.path.join(DATA_DIR, "product_analysis.csv")
    )

    refund_analysis = pd.read_csv(
        os.path.join(DATA_DIR, "refund_analysis.csv")
    )

    repeat_session_analysis = pd.read_csv(
        os.path.join(DATA_DIR, "repeat_session_analysis.csv")
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

    model_path = os.path.join(
        MODEL_DIR,
        "conversion_prediction_model.pkl"
    )

    return joblib.load(model_path)


# ============================================================
# LOAD DATA
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

    st.error("Unable to load project data.")

    st.exception(e)

    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = load_model()

    model_loaded = True

except Exception as e:

    model = None

    model_loaded = False

    st.warning(
        "ML model could not be loaded. "
        "The dashboard will still work, but live prediction will be unavailable."
    )

    st.exception(e)


# ============================================================
# TITLE
# ============================================================

st.title("🛒 E-Commerce Digital Analytics Dashboard")

st.markdown(
    """
    **Business Analytics • Customer Behavior • Marketing • Product Performance • Machine Learning**
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Analysis",
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
# BUSINESS OVERVIEW
# ============================================================

if page == "📊 Business Overview":

    st.header("📊 Business Overview")


    # --------------------------------------------------------
    # Prepare metric dictionary
    # --------------------------------------------------------

    metrics = {}

    for _, row in business_summary.iterrows():

        metric_name = str(row["Metric"]).strip().lower()

        metric_value = row["Value"]

        metrics[metric_name] = metric_value


    # --------------------------------------------------------
    # Helper function
    # --------------------------------------------------------

    def get_metric_value(possible_names, default=0):

        for name in possible_names:

            normalized_name = name.strip().lower()

            if normalized_name in metrics:

                value = metrics[normalized_name]

                try:

                    if pd.isna(value):
                        return default

                except TypeError:
                    pass

                try:

                    value_string = (
                        str(value)
                        .replace(",", "")
                        .replace("$", "")
                        .replace("₹", "")
                        .replace("%", "")
                        .strip()
                    )

                    return float(value_string)

                except (ValueError, TypeError):

                    return value

        return default


    # --------------------------------------------------------
    # KPI Values
    # --------------------------------------------------------

    total_sessions = get_metric_value(
        [
            "total sessions",
            "sessions",
            "total session"
        ]
    )

    total_revenue = get_metric_value(
        [
            "total revenue",
            "revenue",
            "total revenue ($)",
            "total revenue usd",
            "revenue ($)"
        ]
    )

    total_orders = get_metric_value(
        [
            "total orders",
            "orders",
            "total order"
        ]
    )

    conversion_rate = get_metric_value(
        [
            "conversion rate",
            "conversion rate (%)",
            "conversion rate %",
            "conversion rate percent"
        ]
    )


    # --------------------------------------------------------
    # KPI Cards
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        if isinstance(total_sessions, (int, float, np.number)):

            st.metric(
                "Total Sessions",
                f"{total_sessions:,.0f}"
            )

        else:

            st.metric(
                "Total Sessions",
                total_sessions
            )


    with col2:

        if isinstance(total_revenue, (int, float, np.number)):

            st.metric(
                "Total Revenue",
                f"${total_revenue:,.2f}"
            )

        else:

            st.metric(
                "Total Revenue",
                total_revenue
            )


    with col3:

        if isinstance(total_orders, (int, float, np.number)):

            st.metric(
                "Total Orders",
                f"{total_orders:,.0f}"
            )

        else:

            st.metric(
                "Total Orders",
                total_orders
            )


    with col4:

        if isinstance(conversion_rate, (int, float, np.number)):

            st.metric(
                "Conversion Rate",
                f"{conversion_rate:.2f}%"
            )

        else:

            st.metric(
                "Conversion Rate",
                conversion_rate
            )


    # --------------------------------------------------------
    # Business Summary Table
    # --------------------------------------------------------

    st.subheader("Business Summary")

    st.dataframe(
        business_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

elif page == "🛍️ Product Performance":

    st.header("🛍️ Product Performance")


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            product_analysis,
            x="product_name",
            y="revenue",
            title="Revenue by Product",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            product_analysis,
            x="product_name",
            y="gross_profit",
            title="Gross Profit by Product",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    fig = px.bar(
        product_analysis,
        x="product_name",
        y="units_sold",
        title="Units Sold by Product",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("Product Analysis")

    st.dataframe(
        product_analysis,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# REFUND ANALYSIS
# ============================================================

elif page == "💰 Refund Analysis":

    st.header("💰 Refund Analysis")


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            refund_analysis,
            x="product_name",
            y="refund_amount",
            title="Refund Amount by Product",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            refund_analysis,
            x="product_name",
            y="refund_rate_pct",
            title="Refund Rate by Product",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader("Refund Details")

    st.dataframe(
        refund_analysis,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MARKETING PERFORMANCE
# ============================================================

elif page == "📢 Marketing Performance":

    st.header("📢 Marketing Performance")


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            marketing_analysis,
            x="reporting_utm_source",
            y="sessions",
            title="Sessions by Marketing Source",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            marketing_analysis,
            x="reporting_utm_source",
            y="conversion_rate_pct",
            title="Conversion Rate by Marketing Source",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    fig = px.bar(
        marketing_analysis,
        x="reporting_utm_source",
        y="revenue",
        title="Revenue by Marketing Source",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("Marketing Analysis")

    st.dataframe(
        marketing_analysis,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DEVICE PERFORMANCE
# ============================================================

elif page == "📱 Device Performance":

    st.header("📱 Device Performance")


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            device_analysis,
            x="reporting_device_type",
            y="sessions",
            title="Sessions by Device",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            device_analysis,
            x="reporting_device_type",
            y="conversion_rate_pct",
            title="Conversion Rate by Device",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="revenue",
        title="Revenue by Device",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("Device Analysis")

    st.dataframe(
        device_analysis,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CUSTOMER SESSIONS
# ============================================================

elif page == "🔁 Customer Sessions":

    st.header("🔁 Customer Session Analysis")


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            repeat_session_analysis,
            x="is_repeat_session",
            y="sessions",
            title="Sessions: New vs Repeat",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            repeat_session_analysis,
            x="is_repeat_session",
            y="conversion_rate_pct",
            title="Conversion Rate: New vs Repeat",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    fig = px.bar(
        repeat_session_analysis,
        x="is_repeat_session",
        y="revenue",
        title="Revenue: New vs Repeat",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("Session Analysis")

    st.dataframe(
        repeat_session_analysis,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MACHINE LEARNING
# ============================================================

elif page == "🤖 ML Model":

    st.header("🤖 Conversion Prediction Model")


    # --------------------------------------------------------
    # Model Status
    # --------------------------------------------------------

    if model_loaded:

        st.success(
            "✅ Conversion prediction model loaded successfully."
        )

    else:

        st.error(
            "❌ Conversion prediction model is unavailable."
        )


    # --------------------------------------------------------
    # Model Performance
    # --------------------------------------------------------

    st.subheader("📈 Model Performance")

    st.dataframe(
        model_performance,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Historical Prediction Results
    # --------------------------------------------------------

    st.subheader("📊 Historical Prediction Results")


    col1, col2 = st.columns(2)


    with col1:

        actual_counts = (
            prediction_results["actual_conversion"]
            .value_counts()
            .reset_index()
        )

        actual_counts.columns = [
            "Conversion",
            "Count"
        ]

        fig = px.bar(
            actual_counts,
            x="Conversion",
            y="Count",
            title="Actual Conversion Distribution",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        predicted_counts = (
            prediction_results["predicted_conversion"]
            .value_counts()
            .reset_index()
        )

        predicted_counts.columns = [
            "Conversion",
            "Count"
        ]

        fig = px.bar(
            predicted_counts,
            x="Conversion",
            y="Count",
            title="Predicted Conversion Distribution",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Conversion Probability
    # --------------------------------------------------------

    fig = px.histogram(
        prediction_results,
        x="conversion_probability",
        nbins=30,
        title="Conversion Probability Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # LIVE PREDICTION
    # --------------------------------------------------------

    st.divider()

    st.subheader("🔮 Live Conversion Prediction")


    if not model_loaded:

        st.warning(
            "Live prediction is unavailable because the ML model could not be loaded."
        )


    else:

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # INPUT COLUMN 1
        # ----------------------------------------------------

        with col1:

            repeat_session = st.selectbox(
                "Repeat Session",
                ["No", "Yes"]
            )


            utm_source_options = sorted(
                prediction_results[
                    "reporting_utm_source"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            utm_source = st.selectbox(
                "UTM Source",
                utm_source_options
            )


            device_options = sorted(
                prediction_results[
                    "reporting_device_type"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            device_type = st.selectbox(
                "Device Type",
                device_options
            )


            session_hour = st.number_input(
                "Session Hour",
                min_value=0,
                max_value=23,
                value=12
            )


            day_of_week = st.number_input(
                "Day of Week",
                min_value=0,
                max_value=6,
                value=0
            )


        # ----------------------------------------------------
        # INPUT COLUMN 2
        # ----------------------------------------------------

        with col2:

            campaign_options = sorted(
                prediction_results[
                    "utm_campaign"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            campaign = st.selectbox(
                "UTM Campaign",
                ["None"] + campaign_options
            )


            content_options = sorted(
                prediction_results[
                    "utm_content"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            content = st.selectbox(
                "UTM Content",
                ["None"] + content_options
            )


            referer_options = sorted(
                prediction_results[
                    "http_referer"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            referer = st.selectbox(
                "HTTP Referer",
                ["None"] + referer_options
            )


            session_month = st.number_input(
                "Session Month",
                min_value=1,
                max_value=12,
                value=1
            )


            session_year = st.number_input(
                "Session Year",
                min_value=2000,
                max_value=2100,
                value=2026
            )


        # ----------------------------------------------------
        # PREPARE INPUT DATA
        # ----------------------------------------------------

        input_data = pd.DataFrame(
            {
                "is_repeat_session": [
                    1 if repeat_session == "Yes" else 0
                ],

                "reporting_utm_source": [
                    utm_source
                ],

                "utm_campaign": [
                    None if campaign == "None" else campaign
                ],

                "utm_content": [
                    None if content == "None" else content
                ],

                "reporting_device_type": [
                    device_type
                ],

                "http_referer": [
                    None if referer == "None" else referer
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


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        if st.button(
            "🔮 Predict Conversion",
            use_container_width=True
        ):

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
                        "✅ Prediction: Customer is likely to convert."
                    )

                else:

                    st.warning(
                        "⚠️ Prediction: Customer is unlikely to convert."
                    )


                st.metric(
                    "Conversion Probability",
                    f"{probability * 100:.2f}%"
                )


                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=probability * 100,
                        title={
                            "text": "Conversion Probability (%)"
                        },
                        gauge={
                            "axis": {
                                "range": [0, 100]
                            }
                        }
                    )
                )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            except Exception as e:

                st.error(
                    "Prediction failed."
                )

                st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Digital Analytics | SQL • Python • Excel • Power BI • Machine Learning • Streamlit"
)
