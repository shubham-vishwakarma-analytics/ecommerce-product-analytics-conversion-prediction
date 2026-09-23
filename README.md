# E-Commerce Product Analytics & Conversion Prediction

> End-to-end e-commerce analytics project using SQL Server, T-SQL, Python, Machine Learning, Power BI, and GitHub.

![E-Commerce Analytics Overview](screenshots/business_reconmedation.png)

**Author:** Shubham Vishwakarma  
**Project Type:** End-to-End Data Analytics & Machine Learning  
**Domain:** E-Commerce / Digital Analytics

---

## Project Overview

E-Commerce Product Analytics & Conversion Prediction is an end-to-end analytics project that transforms raw e-commerce data into validated business KPIs, analytical datasets, interactive Power BI dashboards, and a machine-learning model for website session conversion prediction.

The project covers the complete analytics lifecycle:

```text
Raw E-Commerce Data
        ↓
Data Audit & Validation
        ↓
SQL Cleaning & Transformation
        ↓
Analytical Views
        ↓
Python EDA
        ↓
Diagnostic Analysis
        ↓
Machine Learning
        ↓
Power BI Dashboards
        ↓
Business Insights
        ↓
Recommendations
```

The analysis focuses on sales performance, website sessions, marketing sources, product profitability, refunds, customer behavior, device performance, repeat sessions, and conversion prediction.

---

## Business Objectives

| # | Objective |
|---|---|
| 1 | Analyze overall e-commerce sales performance |
| 2 | Measure revenue, orders, AOV, gross profit, and gross margin |
| 3 | Analyze website session and conversion performance |
| 4 | Compare conversion performance across devices |
| 5 | Evaluate marketing source and campaign performance |
| 6 | Analyze product revenue and profitability |
| 7 | Identify refund concentration and refund risk |
| 8 | Compare repeat and new-session behavior |
| 9 | Analyze changes in sessions and orders over time |
| 10 | Build a machine-learning model for conversion prediction |
| 11 | Develop interactive Power BI dashboards |
| 12 | Translate analytical findings into business recommendations |

---

## Project at a Glance

| KPI | Result |
|---|---:|
| Gross Revenue | $1.94M |
| Net Revenue | $1.85M |
| Total Orders | 32,313 |
| Total Sessions | 472,871 |
| Conversion Rate | 6.83% |
| Average Order Value | $59.99 |
| Gross Margin | 62.74% |
| Refund % of Revenue | 4.40% |

---

## End-to-End Workflow

```text
Raw E-Commerce Data
        ↓
SQL Server
        ↓
Data Audit
        ↓
Data Cleaning
        ↓
Data Validation
        ↓
KPI Definitions
        ↓
Analytical Views
        ↓
Python
    ├── EDA
    ├── Diagnostic Analysis
    └── Business Analysis
        ↓
Machine Learning
    └── Logistic Regression
        ↓
Power BI
    ├── Executive Overview
    ├── Marketing & Session Funnel
    ├── Product & Refunds
    └── Sales & Profitability
        ↓
Business Insights
        ↓
Recommendations
```

---

# Data Model

The project uses six core source tables:

- `products`
- `website_sessions`
- `website_pageviews`
- `orders`
- `order_items`
- `order_item_refunds`

## Entity Relationship Diagram

![Entity Relationship Diagram](screenshots/ER-Diagram.png)

The analytical workflow keeps raw source tables separate from the final analytical views.

```text
dbo Raw Tables
      ↓
Cleaning & Validation
      ↓
analytics.vw_* Views
      ↓
Python + Power BI
```

---

# SQL Server Analysis

SQL Server forms the foundation of the analytical workflow.

## Main Activities

- Source-table auditing
- Row-count validation
- Missing-value checks
- Duplicate checks
- Invalid-value checks
- Primary-key validation
- Relationship validation
- Data cleaning
- Data transformation
- KPI development
- Executive sales analysis
- Website and marketing analysis
- Product and refund analysis
- Customer/session analysis
- Diagnostic analysis
- KPI reconciliation

## SQL Analysis Modules

| SQL Module | Purpose |
|---|---|
| `FINAL_SQL_MASTER.sql` | Complete SQL workflow |
| `01_Final_Audit_Revalidation.sql` | Final data-quality and relationship checks |
| `02_Data_Cleaning_and_Transformation.sql` | Cleaning and analytical preparation |
| `03_KPI_Definitions.sql` | Standardized business metrics |
| `04_EDA_Executive_Sales.sql` | Revenue, orders, profit, and sales trends |
| `05_EDA_Website_Marketing.sql` | Sessions, conversion, devices, and marketing |
| `06_EDA_Product_Refund.sql` | Product performance and refunds |
| `07_EDA_Customer.sql` | Customer and session behavior |
| `08_Diagnostic_Analysis.sql` | Cross-dimensional business analysis |
| `09_Final_Data_Quality_Reconciliation.sql` | Final KPI and data-quality reconciliation |
| `10_Final_KPI_Snapshot.sql` | Final business KPI output |

## SQL Analysis Visuals

### Table Inventory and Row Count

![Table Inventory Row Count](screenshots/Table_Inventory_Row_Count_By_SQL.png)

### SQL KPI Analysis

![SQL KPI](screenshots/SQL_KPI.png)

### SQL KPI Summary

![SQL KPIs](screenshots/SQL_KPIs.png)

### Product Sales, Profit and Margin

![Product Sales Profit Margin](screenshots/Produt_sales_profit_margin_By_SQL.png)

### Refund by Product

![Refund by Product](screenshots/Refund_by_product_By_SQL.png)

### Customer Order Frequency

![Customer Order Frequency](screenshots/customer_order_frequency_By_SQL.png)

---

# KPI Framework

## Gross Revenue

Sum of order-line selling prices.

```text
Gross Revenue = SUM(Order Item Selling Price)
```

## Gross Profit

```text
Gross Profit = Revenue - COGS
```

## Gross Margin

```text
Gross Margin % = (Revenue - COGS) / Revenue × 100
```

## Average Order Value

```text
AOV = Revenue / Number of Orders
```

## Net Revenue

```text
Net Revenue = Gross Revenue - Refunds
```

## Conversion Rate

```text
Conversion Rate = Converted Sessions / Total Sessions × 100
```

## Revenue per Session

```text
Revenue per Session = Revenue / Sessions
```

## Refund Rate

```text
Refund Rate = Refund Amount / Revenue × 100
```

---

# Power BI Dashboards

Four Power BI dashboards were developed for interactive business analysis.

## 01. Executive Overview

![Executive Overview](screenshots/Executive-Overview.png)

Provides a high-level view of:

- Revenue
- Net revenue
- Orders
- Sessions
- Conversion rate
- Average order value
- Gross profit
- Gross margin
- Overall business performance

## 02. Marketing & Session Funnel

![Marketing and Sessions](screenshots/Maketing&Sessions.png)

Analyzes:

- Marketing sources
- Session volume
- Conversion performance
- Device performance
- Repeat vs new sessions
- Session trends
- Marketing efficiency

## 03. Product & Refunds

![Products and Refunds](screenshots/Products&Refunds.png)

Analyzes:

- Product revenue
- Gross profit
- Gross margin
- Product sales
- Refund amounts
- Refund rates
- Product-level refund concentration

## 04. Sales & Profitability

![Sales and Profitability](screenshots/Sales&Profitability.png)

Analyzes:

- Sales trends
- Revenue
- Orders
- Profitability
- Gross margin
- Supporting business KPIs

---

# Python EDA & Business Analysis

Python was used after the SQL analytical layer to perform exploratory, diagnostic, and business analysis.

## Analysis Areas

- SQL Server data extraction
- Data validation
- Missing-value analysis
- Duplicate analysis
- Descriptive statistics
- Time-series analysis
- Marketing analysis
- Device analysis
- Product analysis
- Refund analysis
- Customer/session analysis
- Repeat vs new-session analysis
- Business rankings
- KPI analysis
- Business findings

## Main Libraries

```text
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
PyODBC
Jupyter
```

## Python Analysis Visuals

### Revenue by Product

![Revenue by Product](screenshots/Revenue_By_Product_Python_Visualization.png)

### Gross Profit by Product

![Gross Profit by Product](screenshots/Gross_Profit_by_Product_Python_Visualization.png)

### Gross Profit Trend

![Gross Profit Trend](screenshots/Gross_Profit_Trend_Pthon_Visualization.png)

### Orders by Year

![Orders by Year](screenshots/Order_By_Year_Python_Visualization.png)

### Sessions by Marketing Source

![Sessions by Marketing Source](screenshots/Session_BY_Marketing_Source_Python_Visualization.png)

### Sessions by Device

![Sessions by Device](screenshots/Session_by_Deivce_Python_Visualization.png)

### Conversion Rate by Device

![Conversion Rate by Device](screenshots/Conversion_rate_by_device_Python_Visualization.png)

### Refund Rate by Device

![Refund Rate by Device](screenshots/Refund_Rate_By_device_Python_Visualization.png)

---

# Machine Learning — Conversion Prediction

A first-pass Logistic Regression model was developed to predict whether a website session converts.

## Target Variable

```text
converted_session

0 = Not Converted
1 = Converted
```

## Features

The model uses session-level attributes including:

- Device type
- UTM source
- UTM campaign
- UTM content
- HTTP referrer
- Repeat-session flag
- Session hour
- Day
- Month
- Year

## Leakage Control

The following outcome-related variables were intentionally excluded:

```text
order_count
session_revenue
```

These variables can directly reveal conversion outcomes and therefore could introduce data leakage into the prediction model.

---

## Machine Learning Pipeline

```text
Session Data
      ↓
Feature Selection
      ↓
Train / Test Split
      ↓
Numerical + Categorical Preprocessing
      ↓
One-Hot Encoding
      ↓
Logistic Regression
      ↓
Probability Prediction
      ↓
Model Evaluation
```

The preprocessing workflow uses a `ColumnTransformer` and pipeline-based modeling to keep feature preparation consistent between training and prediction.

## Train-Test Splitting and Preprocessing

![Train Test Splitting and Preprocessing](screenshots/Train_test_spiliting_and_preprocessing_python_code.png)

## Model Prediction

![Model Prediction](screenshots/Model_prediction.png)

---

## Model Evaluation

| Metric | Score |
|---|---:|
| Accuracy | 93.17% |
| Precision | 0.00 |
| Recall | 0.00 |
| F1 Score | 0.00 |
| ROC-AUC | 0.632 |

Approximately 6.8% of website sessions convert, resulting in a highly imbalanced target variable.

Because of this imbalance, accuracy alone is not a sufficient measure of model quality.

The Logistic Regression model is treated as a first-pass analytical baseline rather than a production-ready prediction system.

### Potential Improvements

- Class weighting
- SMOTE / oversampling
- Decision-threshold tuning
- Precision-recall analysis
- Additional feature engineering
- Tree-based model comparison
- Cross-validation
- Hyperparameter tuning

---

# Key Business Insights

## Revenue Concentration

**The Original Mr. Fuzzy** contributes approximately **62% of total revenue**.

This creates strong dependence on a single high-performing product and makes product-level monitoring important.

## Mobile Conversion Gap

```text
Mobile   = 3.09%
Desktop  = 8.50%
```

Desktop sessions convert substantially more frequently than mobile sessions.

![Conversion Gap by Device and Repeat Status](screenshots/conversiongap_by_device_and_repeat_status.png)

This indicates an area for investigation across:

- Mobile user experience
- Navigation
- Page performance
- Product discovery
- Checkout experience
- Mobile payment flow

## Marketing Efficiency

`gsearch` generates high traffic volume, but traffic volume alone does not represent business value.

Marketing channels should be evaluated using:

- Conversion rate
- Revenue per session
- Revenue
- Orders
- Profitability

![Marketing Analysis](screenshots/Marketing_Analysis_Python_Code.png)

## Repeat Session Performance

```text
Repeat Sessions = 7.83%
New Sessions    = 6.64%
```

Repeat sessions show stronger conversion performance than new sessions.

![Repeat vs New Session Analysis](screenshots/Repeat_vs_New_Session_Python_code.png)

This supports further analysis of:

- Customer retention
- Remarketing
- Returning visitors
- Loyalty initiatives

## Product and Refund Risk

Refund dollars are concentrated in the highest-volume product.

Therefore, product monitoring should consider both:

```text
Absolute Refund Amount
+
Refund Rate
```

![Refund Analysis](screenshots/Refund_Analysis_Python_Code.png)

rather than evaluating refund performance using only one metric.

## Session Decline

Session volume has declined since late 2014, contributing to lower order volume.

This represents an area for further investigation across:

- Marketing acquisition
- Website traffic
- Customer retention
- Device performance
- Channel performance

---

# Business Recommendations

| Area | Recommendation |
|---|---|
| Mobile Experience | Audit and improve the mobile conversion funnel |
| Marketing | Evaluate channels using conversion and revenue per session instead of traffic alone |
| Product Mix | Protect high-revenue products and promote strong-margin, low-refund products |
| Product Quality | Investigate products with high refund exposure |
| Customer Retention | Develop strategies for repeat visitors |
| Conversion Model | Address class imbalance and tune the prediction threshold |

---

# Project Visual Gallery

## Business Recommendations

![Business Recommendations](screenshots/business_reconmedation.png)

## Conversion Analysis

![Conversion Gap by Device and Repeat Status](screenshots/conversiongap_by_device_and_repeat_status.png)

## Device Analysis

![Conversion Rate by Device](screenshots/Conversion_rate_by_device_Python_Visualization.png)

## Customer Analysis

![Customer Order Frequency](screenshots/customer_order_frequency_By_SQL.png)

## Revenue by Product

![Revenue by Product](screenshots/Revenue_By_Product_Python_Visualization.png)

## Gross Profit by Product

![Gross Profit by Product](screenshots/Gross_Profit_by_Product_Python_Visualization.png)

## Gross Profit Trend

![Gross Profit Trend](screenshots/Gross_Profit_Trend_Pthon_Visualization.png)

## Orders by Year

![Orders by Year](screenshots/Order_By_Year_Python_Visualization.png)

## Sessions by Marketing Source

![Sessions by Marketing Source](screenshots/Session_BY_Marketing_Source_Python_Visualization.png)

## Sessions by Device

![Sessions by Device](screenshots/Session_by_Deivce_Python_Visualization.png)

## Refund Rate by Device

![Refund Rate by Device](screenshots/Refund_Rate_By_device_Python_Visualization.png)

## Product Sales, Profit and Margin

![Product Sales Profit Margin](screenshots/Produt_sales_profit_margin_By_SQL.png)

## Refund by Product

![Refund by Product](screenshots/Refund_by_product_By_SQL.png)

## Machine Learning Prediction

![Model Prediction](screenshots/Model_prediction.png)

## SQL KPI Analysis

![SQL KPI](screenshots/SQL_KPI.png)

---

# Repository Structure

```text
ecommerce-product-analytics/
│
├── 01_SQL_Codes/
│   ├── FINAL_SQL_MASTER.sql
│   ├── 01_Final_Audit_Revalidation.sql
│   ├── 02_Data_Cleaning_and_Transformation.sql
│   ├── 03_KPI_Definitions.sql
│   ├── 04_EDA_Executive_Sales.sql
│   ├── 05_EDA_Website_Marketing.sql
│   ├── 06_EDA_Product_Refund.sql
│   ├── 07_EDA_Customer.sql
│   ├── 08_Diagnostic_Analysis.sql
│   ├── 09_Final_Data_Quality_Reconciliation.sql
│   ├── 10_Final_KPI_Snapshot.sql
│   └── ER-Diagram.png
│
├── 02_PowerBI_Dashboard/
│   ├── PRP_Ecommerce_Digital_Analytics_Dashboard.pbix
│   └── Power BI Dashboards.pdf
│
├── 03_Python_Analysis_ML/
│   ├── ECommerce_Analytics_Python_ML_Analysis.ipynb
│   ├── conversion_prediction_model.pkl
│   └── outputs/
│
├── 04_Presentation/
│   ├── PRP_Ecommerce_Digital_Analytics_Final_Presentation.pptx
│   └── PRP_Ecommerce_Digital_Analytics_Final_Presentation.pdf
│
├── screenshots/
├── data/
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

# How to Run

## SQL Server

Create the database:

```sql
CREATE DATABASE PRP_Ecommerce_Analytics;
```

Import the six source CSV files into the appropriate `dbo` tables.

Run:

```text
01_SQL_Codes/FINAL_SQL_MASTER.sql
```

Verify the generated analytical views and then run the individual SQL analysis scripts as required.

## Python / Jupyter

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Open:

```text
03_Python_Analysis_ML/ECommerce_Analytics_Python_ML_Analysis.ipynb
```

Update the SQL Server connection variables according to your local environment before running the notebook.

## Power BI

Open:

```text
02_PowerBI_Dashboard/PRP_Ecommerce_Digital_Analytics_Dashboard.pbix
```

Configure the SQL Server connection and refresh the data model.

---

# Project Deliverables

| Deliverable | Location |
|---|---|
| SQL Analysis & Data Quality Scripts | `01_SQL_Codes/` |
| Power BI Dashboard | `02_PowerBI_Dashboard/` |
| Python EDA & ML Notebook | `03_Python_Analysis_ML/` |
| Saved ML Model | `03_Python_Analysis_ML/conversion_prediction_model.pkl` |
| Python Business Outputs | `03_Python_Analysis_ML/outputs/` |
| Final Presentation | `04_Presentation/` |
| Project Visuals | `screenshots/` |
| Project Documentation | `README.md` |

---

# Data Availability

The project uses six raw CSV datasets:

```text
products.csv
website_sessions.csv
website_pageviews.csv
orders.csv
order_items.csv
order_item_refunds.csv
```

Large raw files may be excluded from the public GitHub repository to keep the repository lightweight.

If the datasets are hosted separately, an approved data-access link can be added to the repository.

Do not commit confidential, restricted, or sensitive business data to a public repository.

---

# Security & Data Handling

Never commit:

```text
Database Passwords
API Keys
Connection Strings
Private Credentials
Sensitive Business Data
```

Recommended `.gitignore` entries:

```text
.env
*.env
__pycache__/
*.pyc
.ipynb_checkpoints/
```

---

# Skills Demonstrated

## SQL / Data Analytics

- SQL Server
- T-SQL
- Data cleaning
- Data validation
- Data-quality analysis
- Joins
- CTEs
- Aggregations
- Window functions
- CASE expressions
- Date functions
- Analytical views
- KPI development
- Descriptive analysis
- Diagnostic analysis
- Business analysis

## Python

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Data manipulation
- Data validation
- Exploratory data analysis
- Visualization
- Business analysis

## Machine Learning

- Binary classification
- Logistic Regression
- Train/test split
- Feature preprocessing
- One-Hot Encoding
- Pipeline
- ColumnTransformer
- Probability prediction
- Confusion matrix
- Classification report
- ROC curve
- ROC-AUC
- Class imbalance
- Data leakage prevention

## Power BI

- Power Query
- Data modeling
- DAX
- KPI cards
- Interactive filters
- Time-series analysis
- Product analysis
- Marketing analysis
- Sales analysis
- Profitability analysis
- Business dashboards

## Tools

- SQL Server
- Jupyter
- Python
- Power BI
- Git
- GitHub

---

# Analytical Limitations

| Limitation | Explanation |
|---|---|
| Conversion imbalance | Only approximately 6.8% of sessions convert |
| Model performance | Current Logistic Regression is a baseline model |
| Positive-class performance | Precision, recall, and F1 are currently 0 |
| Accuracy | High accuracy is influenced by class imbalance |
| Causality | Diagnostic analysis identifies relationships but does not prove causation |
| Historical data | Session and order trends reflect the available historical period |
| Product concentration | Revenue is heavily concentrated in The Original Mr. Fuzzy |

---

# Final Conclusion

This project demonstrates how raw e-commerce data can be transformed into a structured analytical solution using SQL Server, Python, Machine Learning, and Power BI.

The project provides a complete workflow for:

```text
DATA
 ↓
AUDIT
 ↓
CLEAN
 ↓
VALIDATE
 ↓
TRANSFORM
 ↓
ANALYZE
 ↓
VISUALIZE
 ↓
MODEL
 ↓
EVALUATE
 ↓
RECOMMEND
```

The analysis highlights important business areas including:

- Mobile conversion performance
- Marketing efficiency
- Product revenue concentration
- Refund exposure
- Repeat-session performance
- Session trends
- Product profitability
- Conversion prediction

The Logistic Regression model provides an initial baseline for conversion prediction. However, the highly imbalanced target and weak positive-class metrics indicate that additional feature engineering, class-imbalance handling, threshold tuning, and model experimentation would be required before considering a production-ready prediction system.

---

# Author

**Shubham Vishwakarma**

**Data Analyst | SQL | Python | Power BI | Machine Learning**

GitHub: `shubham-vishwakarma-analytics`
