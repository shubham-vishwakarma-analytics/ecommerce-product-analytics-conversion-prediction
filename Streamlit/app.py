import streamlit as st
import pandas as pd
import plotly.express as px
import joblib


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-Commerce Digital Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    business_summary = pd.read_csv(
        "data/business_summary.csv"
    )

    device_analysis = pd.read_csv(
        "data/device_analysis.csv"
    )

    marketing_analysis = pd.read_csv(
        "data/marketing_analysis.csv"
    )

    model_performance = pd.read_csv(
        "data/model_performance.csv"
    )

    prediction_results = pd.read_csv(
        "data/prediction_results.csv"
    )

    product_analysis = pd.read_csv(
        "data/product_analysis.csv"
    )

    refund_analysis = pd.read_csv(
        "data/refund_analysis.csv"
    )

    repeat_session_analysis = pd.read_csv(
        "data/repeat_session_analysis.csv"
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


# =========================================================
# LOAD ML MODEL
# =========================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "models/conversion_prediction_model.pkl"
    )

    return model


try:

    model = load_model()

    model_loaded = True

except Exception as e:

    model = None
    model_loaded = False
    model_error = str(e)


# =========================================================
# BUSINESS METRICS
# =========================================================

business_metrics = dict(
    zip(
        business_summary["Metric"],
        business_summary["Value"]
    )
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛒 E-Commerce Analytics")

st.sidebar.markdown(
    "### Dashboard Navigation"
)

page = st.sidebar.radio(
    "Select Section",
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

st.sidebar.divider()

st.sidebar.caption(
    "E-Commerce Digital Analytics"
)

st.sidebar.caption(
    "Built with Python, Pandas, Plotly & Streamlit"
)


# =========================================================
# MAIN HEADER
# =========================================================

st.title("🛒 E-Commerce Digital Analytics")

st.caption(
    "Interactive analytics dashboard for sales, products, "
    "marketing, customers, refunds and conversion performance."
)


# =========================================================
# PAGE 1 — BUSINESS OVERVIEW
# =========================================================

if page == "📊 Business Overview":

    st.header("📊 Business Overview")

    st.markdown(
        "A high-level view of e-commerce business performance."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Sessions",
            f"{business_metrics.get('Total Sessions', 0):,.0f}"
        )

    with col2:

        st.metric(
            "Converted Sessions",
            f"{business_metrics.get('Converted Sessions', 0):,.0f}"
        )

    with col3:

        st.metric(
            "Conversion Rate",
            f"{business_metrics.get('Conversion Rate (%)', 0):.2f}%"
        )

    with col4:

        st.metric(
            "Revenue",
            f"${business_metrics.get('Revenue', 0):,.2f}"
        )


    col5, col6, col7, col8 = st.columns(4)

    with col5:

        st.metric(
            "COGS",
            f"${business_metrics.get('COGS', 0):,.2f}"
        )

    with col6:

        st.metric(
            "Gross Profit",
            f"${business_metrics.get('Gross Profit', 0):,.2f}"
        )

    with col7:

        st.metric(
            "Gross Margin",
            f"{business_metrics.get('Gross Margin (%)', 0):.2f}%"
        )

    with col8:

        st.metric(
            "Refund Amount",
            f"${business_metrics.get('Total Refund Amount', 0):,.2f}"
        )


    st.divider()

    st.subheader("Business Summary")

    st.dataframe(
        business_summary,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 2 — PRODUCT PERFORMANCE
# =========================================================

elif page == "🛍️ Product Performance":

    st.header("🛍️ Product Performance")

    st.markdown(
        "Analyze product revenue, units sold, gross profit and margins."
    )

    st.divider()

    product_list = product_analysis[
        "product_name"
    ].unique().tolist()

    selected_products = st.multiselect(
        "Select Products",
        product_list,
        default=product_list
    )

    filtered_products = product_analysis[
        product_analysis["product_name"].isin(
            selected_products
        )
    ]


    col1, col2 = st.columns(2)

    with col1:

        revenue_fig = px.bar(
            filtered_products,
            x="product_name",
            y="revenue",
            title="Revenue by Product",
            labels={
                "product_name": "Product",
                "revenue": "Revenue"
            },
            text_auto=".2s"
        )

        revenue_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue",
            hovermode="x unified"
        )

        st.plotly_chart(
            revenue_fig,
            use_container_width=True
        )


    with col2:

        profit_fig = px.bar(
            filtered_products,
            x="product_name",
            y="gross_profit",
            title="Gross Profit by Product",
            labels={
                "product_name": "Product",
                "gross_profit": "Gross Profit"
            },
            text_auto=".2s"
        )

        profit_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Gross Profit",
            hovermode="x unified"
        )

        st.plotly_chart(
            profit_fig,
            use_container_width=True
        )


    margin_fig = px.bar(
        filtered_products,
        x="product_name",
        y="gross_margin_pct",
        title="Gross Margin by Product",
        labels={
            "product_name": "Product",
            "gross_margin_pct": "Gross Margin (%)"
        },
        text_auto=".2f"
    )

    margin_fig.update_layout(
        xaxis_title=None,
        yaxis_title="Gross Margin (%)"
    )

    st.plotly_chart(
        margin_fig,
        use_container_width=True
    )


    st.subheader("Product Performance Details")

    st.dataframe(
        filtered_products,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 3 — REFUND ANALYSIS
# =========================================================

elif page == "💰 Refund Analysis":

    st.header("💰 Refund Analysis")

    st.markdown(
        "Analyze refund amount, refund count and refund rate by product."
    )

    st.divider()

    refund_products = refund_analysis[
        "product_name"
    ].unique().tolist()

    selected_refund_products = st.multiselect(
        "Select Products",
        refund_products,
        default=refund_products
    )

    filtered_refunds = refund_analysis[
        refund_analysis["product_name"].isin(
            selected_refund_products
        )
    ]


    col1, col2 = st.columns(2)

    with col1:

        refund_amount_fig = px.bar(
            filtered_refunds,
            x="product_name",
            y="refund_amount",
            title="Refund Amount by Product",
            labels={
                "product_name": "Product",
                "refund_amount": "Refund Amount"
            },
            text_auto=".2s"
        )

        refund_amount_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Refund Amount"
        )

        st.plotly_chart(
            refund_amount_fig,
            use_container_width=True
        )


    with col2:

        refund_rate_fig = px.bar(
            filtered_refunds,
            x="product_name",
            y="refund_rate_pct",
            title="Refund Rate by Product",
            labels={
                "product_name": "Product",
                "refund_rate_pct": "Refund Rate (%)"
            },
            text_auto=".2f"
        )

        refund_rate_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Refund Rate (%)"
        )

        st.plotly_chart(
            refund_rate_fig,
            use_container_width=True
        )


    refund_count_fig = px.bar(
        filtered_refunds,
        x="product_name",
        y="refund_count",
        title="Refund Count by Product",
        labels={
            "product_name": "Product",
            "refund_count": "Refund Count"
        },
        text_auto=True
    )

    refund_count_fig.update_layout(
        xaxis_title=None,
        yaxis_title="Refund Count"
    )

    st.plotly_chart(
        refund_count_fig,
        use_container_width=True
    )


    st.subheader("Refund Details")

    st.dataframe(
        filtered_refunds,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 4 — MARKETING PERFORMANCE
# =========================================================

elif page == "📢 Marketing Performance":

    st.header("📢 Marketing Performance")

    st.markdown(
        "Compare marketing sources based on sessions, revenue "
        "and conversion performance."
    )

    st.divider()

    marketing_sources = marketing_analysis[
        "reporting_utm_source"
    ].unique().tolist()

    selected_sources = st.multiselect(
        "Select Marketing Sources",
        marketing_sources,
        default=marketing_sources
    )

    filtered_marketing = marketing_analysis[
        marketing_analysis["reporting_utm_source"].isin(
            selected_sources
        )
    ]


    col1, col2 = st.columns(2)

    with col1:

        marketing_revenue_fig = px.bar(
            filtered_marketing,
            x="reporting_utm_source",
            y="revenue",
            title="Revenue by Marketing Source",
            labels={
                "reporting_utm_source": "Marketing Source",
                "revenue": "Revenue"
            },
            text_auto=".2s"
        )

        marketing_revenue_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            marketing_revenue_fig,
            use_container_width=True
        )


    with col2:

        marketing_conversion_fig = px.bar(
            filtered_marketing,
            x="reporting_utm_source",
            y="conversion_rate_pct",
            title="Conversion Rate by Marketing Source",
            labels={
                "reporting_utm_source": "Marketing Source",
                "conversion_rate_pct": "Conversion Rate (%)"
            },
            text_auto=".2f"
        )

        marketing_conversion_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Conversion Rate (%)"
        )

        st.plotly_chart(
            marketing_conversion_fig,
            use_container_width=True
        )


    sessions_fig = px.bar(
        filtered_marketing,
        x="reporting_utm_source",
        y="sessions",
        title="Sessions by Marketing Source",
        labels={
            "reporting_utm_source": "Marketing Source",
            "sessions": "Sessions"
        },
        text_auto=".2s"
    )

    sessions_fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sessions"
    )

    st.plotly_chart(
        sessions_fig,
        use_container_width=True
    )


    st.subheader("Marketing Details")

    st.dataframe(
        filtered_marketing,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 5 — DEVICE PERFORMANCE
# =========================================================

elif page == "📱 Device Performance":

    st.header("📱 Device Performance")

    st.markdown(
        "Compare customer sessions and conversion performance "
        "across devices."
    )

    st.divider()


    col1, col2 = st.columns(2)

    with col1:

        device_sessions_fig = px.bar(
            device_analysis,
            x="reporting_device_type",
            y="sessions",
            title="Sessions by Device",
            labels={
                "reporting_device_type": "Device",
                "sessions": "Sessions"
            },
            text_auto=".2s"
        )

        device_sessions_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Sessions"
        )

        st.plotly_chart(
            device_sessions_fig,
            use_container_width=True
        )


    with col2:

        device_conversion_fig = px.bar(
            device_analysis,
            x="reporting_device_type",
            y="conversion_rate_pct",
            title="Conversion Rate by Device",
            labels={
                "reporting_device_type": "Device",
                "conversion_rate_pct": "Conversion Rate (%)"
            },
            text_auto=".2f"
        )

        device_conversion_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Conversion Rate (%)"
        )

        st.plotly_chart(
            device_conversion_fig,
            use_container_width=True
        )


    revenue_session_fig = px.bar(
        device_analysis,
        x="reporting_device_type",
        y="revenue_per_session",
        title="Revenue per Session by Device",
        labels={
            "reporting_device_type": "Device",
            "revenue_per_session": "Revenue per Session"
        },
        text_auto=".2f"
    )

    revenue_session_fig.update_layout(
        xaxis_title=None,
        yaxis_title="Revenue per Session"
    )

    st.plotly_chart(
        revenue_session_fig,
        use_container_width=True
    )


    st.subheader("Device Details")

    st.dataframe(
        device_analysis,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 6 — CUSTOMER SESSIONS
# =========================================================

elif page == "🔁 Customer Sessions":

    st.header("🔁 Repeat vs New Sessions")

    st.markdown(
        "Compare repeat sessions with new sessions based on "
        "sessions, conversion and revenue."
    )

    st.divider()


    col1, col2 = st.columns(2)

    with col1:

        repeat_conversion_fig = px.bar(
            repeat_session_analysis,
            x="is_repeat_session",
            y="conversion_rate_pct",
            title="Conversion Rate",
            labels={
                "is_repeat_session": "Session Type",
                "conversion_rate_pct": "Conversion Rate (%)"
            },
            text_auto=".2f"
        )

        repeat_conversion_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Conversion Rate (%)"
        )

        st.plotly_chart(
            repeat_conversion_fig,
            use_container_width=True
        )


    with col2:

        repeat_revenue_fig = px.bar(
            repeat_session_analysis,
            x="is_repeat_session",
            y="revenue",
            title="Revenue",
            labels={
                "is_repeat_session": "Session Type",
                "revenue": "Revenue"
            },
            text_auto=".2s"
        )

        repeat_revenue_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            repeat_revenue_fig,
            use_container_width=True
        )


    sessions_fig = px.bar(
        repeat_session_analysis,
        x="is_repeat_session",
        y="sessions",
        title="Sessions by Customer Type",
        labels={
            "is_repeat_session": "Session Type",
            "sessions": "Sessions"
        },
        text_auto=".2s"
    )

    sessions_fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sessions"
    )

    st.plotly_chart(
        sessions_fig,
        use_container_width=True
    )


    st.subheader("Customer Session Details")

    st.dataframe(
        repeat_session_analysis,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 7 — MACHINE LEARNING MODEL
# =========================================================

elif page == "🤖 ML Model":

    st.header("🤖 Machine Learning Model")

    st.markdown(
        "Conversion prediction model performance, "
        "historical predictions and live prediction."
    )

    st.divider()


    # =====================================================
    # MODEL STATUS
    # =====================================================

    st.subheader("Model Status")

    if model_loaded:

        st.success(
            "✅ Conversion prediction model loaded successfully."
        )

    else:

        st.error(
            "❌ The prediction model could not be loaded."
        )

        st.code(
            model_error
        )


    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    st.subheader("Model Performance")

    st.dataframe(
        model_performance,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # HISTORICAL PREDICTION SUMMARY
    # =====================================================

    st.subheader("Historical Prediction Summary")

    total_predictions = len(
        prediction_results
    )

    converted_predictions = prediction_results[
        "predicted_conversion"
    ].sum()

    average_probability = prediction_results[
        "conversion_probability"
    ].mean()


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Predictions",
            f"{total_predictions:,}"
        )

    with col2:

        st.metric(
            "Predicted Conversions",
            f"{converted_predictions:,.0f}"
        )

    with col3:

        st.metric(
            "Average Conversion Probability",
            f"{average_probability:.2%}"
        )


    # =====================================================
    # ACTUAL VS PREDICTED
    # =====================================================

    st.subheader("Actual vs Predicted Conversion")

    comparison = pd.DataFrame(
        {
            "Conversion Type": [
                "Actual Conversion",
                "Predicted Conversion"
            ],
            "Count": [
                prediction_results[
                    "actual_conversion"
                ].sum(),

                prediction_results[
                    "predicted_conversion"
                ].sum()
            ]
        }
    )


    comparison_fig = px.bar(
        comparison,
        x="Conversion Type",
        y="Count",
        title="Actual vs Predicted Conversions",
        text_auto=True
    )

    comparison_fig.update_layout(
        xaxis_title=None,
        yaxis_title="Count"
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True
    )


    # =====================================================
    # PROBABILITY DISTRIBUTION
    # =====================================================

    st.subheader(
        "Conversion Probability Distribution"
    )

    probability_fig = px.histogram(
        prediction_results,
        x="conversion_probability",
        nbins=30,
        title="Distribution of Conversion Probability",
        labels={
            "conversion_probability":
            "Conversion Probability"
        }
    )

    probability_fig.update_layout(
        xaxis_title="Conversion Probability",
        yaxis_title="Number of Sessions"
    )

    st.plotly_chart(
        probability_fig,
        use_container_width=True
    )


    # =====================================================
    # LIVE PREDICTION
    # =====================================================

    st.divider()

    st.header("🔮 Live Conversion Prediction")

    st.markdown(
        "Enter session information below to estimate the "
        "probability that the session will convert."
    )


    if not model_loaded:

        st.warning(
            "Live prediction is unavailable because "
            "the ML model could not be loaded."
        )

    else:

        # -------------------------------------------------
        # INPUT SECTION
        # -------------------------------------------------

        st.subheader("Session Information")

        col1, col2 = st.columns(2)


        with col1:

            repeat_session = st.selectbox(
                "Is Repeat Session?",
                options=[0, 1],
                format_func=lambda x:
                    "Yes" if x == 1 else "No"
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
                options=utm_source_options
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
                options=device_options
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
                value=2,
                help=(
                    "0 = Monday, 1 = Tuesday, "
                    "2 = Wednesday, ..., 6 = Sunday"
                )
            )


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

            campaign_options = [
                "None"
            ] + campaign_options

            utm_campaign = st.selectbox(
                "UTM Campaign",
                options=campaign_options
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

            content_options = [
                "None"
            ] + content_options

            utm_content = st.selectbox(
                "UTM Content",
                options=content_options
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

            referer_options = [
                "None"
            ] + referer_options

            http_referer = st.selectbox(
                "HTTP Referer",
                options=referer_options
            )


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
                value=2015,
                step=1
            )


        st.divider()


        # -------------------------------------------------
        # PREDICTION BUTTON
        # -------------------------------------------------

        predict_button = st.button(
            "🔮 Predict Conversion",
            type="primary",
            use_container_width=True
        )


        if predict_button:

            live_input = pd.DataFrame(
                {
                    "is_repeat_session": [
                        repeat_session
                    ],

                    "reporting_utm_source": [
                        utm_source
                    ],

                    "utm_campaign": [
                        None
                        if utm_campaign == "None"
                        else utm_campaign
                    ],

                    "utm_content": [
                        None
                        if utm_content == "None"
                        else utm_content
                    ],

                    "reporting_device_type": [
                        device_type
                    ],

                    "http_referer": [
                        None
                        if http_referer == "None"
                        else http_referer
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
                    live_input
                )[0]

                probability = model.predict_proba(
                    live_input
                )[0][1]


                st.divider()

                st.subheader(
                    "Prediction Result"
                )


                result_col1, result_col2 = st.columns(2)


                with result_col1:

                    if prediction == 1:

                        st.success(
                            "🟢 Predicted: Conversion"
                        )

                    else:

                        st.info(
                            "🔵 Predicted: No Conversion"
                        )


                with result_col2:

                    st.metric(
                        "Conversion Probability",
                        f"{probability:.2%}"
                    )


                st.progress(
                    float(probability)
                )


                st.caption(
                    "The probability is produced by the "
                    "trained Logistic Regression pipeline."
                )


                with st.expander(
                    "View Input Sent to Model"
                ):

                    st.dataframe(
                        live_input,
                        use_container_width=True,
                        hide_index=True
                    )


            except Exception as e:

                st.error(
                    "Prediction failed."
                )

                st.code(
                    str(e)
                )


    # =====================================================
    # HISTORICAL PREDICTION RESULTS
    # =====================================================

    st.divider()

    st.subheader("Historical Prediction Results")

    st.write(
        f"Showing first 100 records out of "
        f"{len(prediction_results):,} predictions."
    )

    st.dataframe(
        prediction_results.head(100),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "E-Commerce Digital Analytics | "
    "Python • Pandas • Plotly • Scikit-learn • Streamlit"
)
