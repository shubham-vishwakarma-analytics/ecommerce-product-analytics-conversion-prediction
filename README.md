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

The analysis focuses on sales performance, website sessions, marketing sources, product profitability, refunds, customer behavior, device performance, repeat sessions, and conversion prediction.

Business Objectives
#	Objective
1	Analyze overall e-commerce sales performance
2	Measure revenue, orders, AOV, gross profit, and gross margin
3	Analyze website session and conversion performance
4	Compare conversion performance across devices
5	Evaluate marketing source and campaign performance
6	Analyze product revenue and profitability
7	Identify refund concentration and refund risk
8	Compare repeat and new-session behavior
9	Analyze changes in sessions and orders over time
10	Build a machine-learning model for conversion prediction
11	Develop interactive Power BI dashboards
12	Translate analytical findings into business recommendations
Project at a Glance
KPI	Result
Gross Revenue	$1.94M
Net Revenue	$1.85M
Total Orders	32,313
Total Sessions	472,871
Conversion Rate	6.83%
Average Order Value	$59.99
Gross Margin	62.74%
Refund % of Revenue	4.40%
End-to-End Workflow
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
Data Model

The project uses six core source tables:

products
website_sessions
website_pageviews
orders
order_items
order_item_refunds
Entity Relationship Diagram

The analytical workflow keeps raw source tables separate from the final analytical views.

dbo Raw Tables
      ↓
Cleaning & Validation
      ↓
analytics.vw_* Views
      ↓
Python + Power BI
SQL Server Analysis

SQL Server forms the foundation of the analytical workflow.

Main Activities
Source-table auditing
Row-count validation
Missing-value checks
Duplicate checks
Invalid-value checks
Primary-key validation
Relationship validation
Data cleaning
Data transformation
KPI development
Executive sales analysis
Website and marketing analysis
Product and refund analysis
Customer/session analysis
Diagnostic analysis
KPI reconciliation
SQL Analytical Layer
Raw dbo Tables
      ↓
Cleaning & Validation
      ↓
analytics.vw_* Views
      ↓
Python + Power BI
SQL Analysis Modules
SQL Module	Purpose
Final SQL Master	Complete SQL workflow
Final Audit Revalidation	Final data-quality and relationship checks
Data Cleaning & Transformation	Cleaning and analytical preparation
KPI Definitions	Standardized business metrics
Executive Sales Analysis	Revenue, orders, profit, and sales trends
Website & Marketing Analysis	Sessions, conversion, devices, and marketing
Product & Refund Analysis	Product performance and refunds
Customer Analysis	Customer and session behavior
Diagnostic Analysis	Cross-dimensional business analysis
KPI Reconciliation	Final KPI consistency checks
KPI Snapshot	Final business KPI output
KPI Framework
Gross Revenue

Sum of order-line selling prices.

Gross Revenue = SUM(Order Item Selling Price)
Gross Profit
Gross Profit = Revenue - COGS
Gross Margin
Gross Margin % = (Revenue - COGS) / Revenue × 100
Average Order Value
AOV = Revenue / Number of Orders
Net Revenue
Net Revenue = Gross Revenue - Refunds
Conversion Rate
Conversion Rate = Converted Sessions / Total Sessions × 100
Revenue per Session
Revenue per Session = Revenue / Sessions
Refund Rate
Refund Rate = Refund Amount / Revenue × 100
Power BI Dashboards

Four Power BI dashboards were developed for interactive business analysis.

01. Executive Overview

Provides a high-level view of:

Revenue
Net revenue
Orders
Sessions
Conversion rate
Average order value
Gross profit
Gross margin
Overall business performance
02. Marketing & Session Funnel

Analyzes:

Marketing sources
Session volume
Conversion performance
Device performance
Repeat vs new sessions
Session trends
Marketing efficiency
03. Product & Refunds

Analyzes:

Product revenue
Gross profit
Gross margin
Product sales
Refund amounts
Refund rates
Product-level refund concentration
04. Sales & Profitability

Analyzes:

Sales trends
Revenue
Orders
Profitability
Gross margin
Supporting business KPIs
Python EDA & Business Analysis

Python was used after the SQL analytical layer to perform exploratory, diagnostic, and business analysis.

Analysis Areas
SQL Server data extraction
Data validation
Missing-value analysis
Duplicate analysis
Descriptive statistics
Time-series analysis
Marketing analysis
Device analysis
Product analysis
Refund analysis
Customer/session analysis
Repeat vs new-session analysis
Business rankings
KPI analysis
Business findings
Main Libraries
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
PyODBC
Jupyter
Machine Learning — Conversion Prediction

A first-pass Logistic Regression model was developed to predict whether a website session converts.

Target Variable
converted_session

0 = Not Converted
1 = Converted
Features

The model uses session-level attributes including:

Device type
UTM source
UTM campaign
UTM content
HTTP referrer
Repeat-session flag
Session hour
Day
Month
Year
Leakage Control

The following outcome-related variables were intentionally excluded:

order_count
session_revenue

These variables can directly reveal conversion outcomes and therefore could introduce data leakage into the prediction model.

Machine Learning Pipeline
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

The preprocessing workflow uses a ColumnTransformer and pipeline-based modeling to keep feature preparation consistent between training and prediction.

Model Evaluation
Metric	Score
Accuracy	93.17%
Precision	0.00
Recall	0.00
F1 Score	0.00
ROC-AUC	0.632
Model Interpretation

Approximately 6.8% of website sessions convert, resulting in a highly imbalanced target variable.

Because of this imbalance, accuracy alone is not a sufficient measure of model quality.

A model can achieve high accuracy by predicting the majority class while failing to correctly identify converting sessions.

The model achieved:

ROC-AUC = 0.632

This indicates some ability to distinguish converting sessions from non-converting sessions, but the current model has limited positive-class performance.

The Logistic Regression model is therefore treated as a first-pass analytical baseline rather than a production-ready prediction system.

Potential Improvements
Class weighting
SMOTE / oversampling
Decision-threshold tuning
Precision-recall analysis
Additional feature engineering
Tree-based model comparison
Cross-validation
Hyperparameter tuning
Key Business Insights
Revenue Concentration

The Original Mr. Fuzzy contributes approximately 62% of total revenue.

This creates strong dependence on a single high-performing product and makes product-level monitoring important.

Mobile Conversion Gap
Mobile   = 3.09%
Desktop  = 8.50%

Desktop sessions convert substantially more frequently than mobile sessions.

This indicates an area for investigation across:

Mobile user experience
Navigation
Page performance
Product discovery
Checkout experience
Mobile payment flow
Marketing Efficiency

gsearch generates high traffic volume, but traffic volume alone does not represent business value.

Marketing channels should be evaluated using:

Conversion rate
Revenue per session
Revenue
Orders
Profitability
Repeat Session Performance
Repeat Sessions = 7.83%
New Sessions    = 6.64%

Repeat sessions show stronger conversion performance than new sessions.

This supports further analysis of:

Customer retention
Remarketing
Returning visitors
Loyalty initiatives
Product and Refund Risk

Refund dollars are concentrated in the highest-volume product.

Therefore, product monitoring should consider both:

Absolute Refund Amount
+
Refund Rate

rather than evaluating refund performance using only one metric.

Session Decline

Session volume has declined since late 2014, contributing to lower order volume.

This represents an area for further investigation across:

Marketing acquisition
Website traffic
Customer retention
Device performance
Channel performance
Business Recommendations
Area	Recommendation	Expected Direction
Mobile Experience	Audit and improve the mobile conversion funnel	Improve mobile conversion
Marketing	Evaluate channels using conversion and revenue per session instead of traffic alone	Improve marketing efficiency
Product Mix	Protect high-revenue products and promote strong-margin, low-refund products	Improve profitability
Product Quality	Investigate products with high refund exposure	Reduce refund leakage
Customer Retention	Develop strategies for repeat visitors	Increase repeat-session contribution
Conversion Model	Address class imbalance and tune the prediction threshold	Improve useful predictive performance
Project Visual Gallery
Business Recommendations

Conversion Analysis

Device Analysis

Customer Analysis

Gross Profit by Product

Gross Profit Trend

Machine Learning

SQL KPI Analysis

Repository Structure
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
│
├── data/
│
├── requirements.txt
│
├── .gitignore
│
├── LICENSE
│
└── README.md
How to Run
SQL Server
Create a SQL Server database.
CREATE DATABASE PRP_Ecommerce_Analytics;
Import the six source CSV files into the appropriate dbo tables.
Run:
01_SQL_Codes/FINAL_SQL_MASTER.sql
Verify the generated analytical views.
Run the individual SQL analysis scripts when required.
Python / Jupyter

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Open:

03_Python_Analysis_ML/ECommerce_Analytics_Python_ML_Analysis.ipynb

The notebook connects to SQL Server using pyodbc.

Update the database connection variables according to your local SQL Server environment before running the notebook.

Power BI

Open:

02_PowerBI_Dashboard/PRP_Ecommerce_Digital_Analytics_Dashboard.pbix

Configure the SQL Server connection for your environment and refresh the data model.

Project Deliverables
Deliverable	Location
SQL Analysis & Data Quality Scripts	01_SQL_Codes/
Power BI Dashboard	02_PowerBI_Dashboard/
Python EDA & ML Notebook	03_Python_Analysis_ML/
Saved ML Model	03_Python_Analysis_ML/conversion_prediction_model.pkl
Python Business Outputs	03_Python_Analysis_ML/outputs/
Final Presentation	04_Presentation/
Project Visuals	screenshots/
Project Documentation	README.md
Data Availability

The project uses six raw CSV datasets:

products.csv
website_sessions.csv
website_pageviews.csv
orders.csv
order_items.csv
order_item_refunds.csv

Large raw files may be excluded from the public GitHub repository to keep the repository lightweight.

If the datasets are hosted separately, the approved data-access link can be added below:

Data Access: <ADD DATA LINK HERE>

Do not commit confidential, restricted, or sensitive business data to a public repository.

Security & Data Handling

The project should not contain confidential credentials or restricted business information.

Never commit:

Database Passwords
API Keys
Connection Strings
Private Credentials
Sensitive Business Data

Recommended .gitignore entries:

.env
*.env
__pycache__/
*.pyc
.ipynb_checkpoints/
Skills Demonstrated
SQL / Data Analytics
SQL Server
T-SQL
Data cleaning
Data validation
Data-quality analysis
Joins
CTEs
Aggregations
Window functions
CASE expressions
Date functions
Analytical views
KPI development
Descriptive analysis
Diagnostic analysis
Business analysis
Python
Pandas
NumPy
Matplotlib
Seaborn
Jupyter Notebook
Data manipulation
Data validation
Exploratory data analysis
Visualization
Business analysis
Machine Learning
Binary classification
Logistic Regression
Train/test split
Feature preprocessing
One-Hot Encoding
Pipeline
ColumnTransformer
Probability prediction
Confusion matrix
Classification report
ROC curve
ROC-AUC
Class imbalance
Data leakage prevention
Power BI
Power Query
Data modeling
DAX
KPI cards
Interactive filters
Time-series analysis
Product analysis
Marketing analysis
Sales analysis
Profitability analysis
Business dashboards
Tools
SQL Server
Jupyter
Python
Power BI
Git
GitHub
Analytical Limitations
Limitation	Explanation
Conversion imbalance	Only approximately 6.8% of sessions convert
Model performance	Current Logistic Regression is a baseline model
Positive-class performance	Precision, recall, and F1 are currently 0
Accuracy	High accuracy is influenced by class imbalance
Causality	Diagnostic analysis identifies relationships but does not prove causation
Historical data	Session and order trends reflect the available historical period
Product concentration	Revenue is heavily concentrated in The Original Mr. Fuzzy
Final Conclusion

This project demonstrates how raw e-commerce data can be transformed into a structured analytical solution using SQL Server, Python, Machine Learning, and Power BI.

The project provides a complete workflow for:

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

The analysis highlights important business areas including:

Mobile conversion performance
Marketing efficiency
Product revenue concentration
Refund exposure
Repeat-session performance
Session trends
Product profitability
Conversion prediction

The Logistic Regression model provides an initial baseline for conversion prediction. However, the highly imbalanced target and weak positive-class metrics indicate that additional feature engineering, class-imbalance handling, threshold tuning, and model experimentation would be required before considering a production-ready prediction system.

Author

Shubham Vishwakarma

Data Analyst | SQL | Python | Power BI | Machine Learning

GitHub: shubham-vishwakarma-analytics
