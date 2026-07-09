ApexPlanet Data Analytics Internship — Superstore Sales Analysis

Dataset: Superstore Sales (2014–2017) — 9,994 orders, 21 columns

Overview
End-to-end data analytics project covering the full pipeline: data cleaning, exploratory
analysis, SQL-based extraction, interactive dashboards, statistical testing, predictive
modeling, and a fully automated reporting pipeline.

Project Structure

├── Task_1.ipynb                          # EDA: cleaning, distributions, correlations
├── Task_2.ipynb                          # SQL extraction via SQLAlchemy + Python
├── Task2_queries.sql                     # Standalone SQL query file
├── Task_3.ipynb                          # Dashboards: Matplotlib, Seaborn, Plotly
├── dashboards/                           # Exported charts (PNG/HTML) + Power BI file
├── Task_4.ipynb                          # Hypothesis testing, clustering, regression
├── Task-5.py                  # Automated ETL + KPI + Excel export script
├── requirements.txt
├── ApexPlanet_Executive_Summary_Report.pdf
└── README.md

Key Findings

Total Revenue: $2,272,449.85 across 9,694 orders | Total Profit: $282,857.75
Top Category: Technology ($835.9K) | Top Region (Profit): West ($106K)
Top State: California ($450.6K) | YoY Growth 2014→2017: +50.5%
Discounts above 20% turn average profit negative (–$9.15), while low/no-discount
orders stay solidly profitable ($68–72 avg profit).
No statistically significant difference in Sales between West/East regions (t-test,
p=0.426) or in Category–Region association (chi-square, p=0.722).
K-Means clustering (k=4) segmented customers by Sales, Profit, and Quantity; a Linear
Regression baseline for Sales prediction achieved R²=-0.15, indicating these features
alone are weak predictors — a direction for future modeling work.

Tech Stack

Python (Pandas, NumPy, Matplotlib, Seaborn, Plotly, Scikit-learn, SciPy) · MySQL/SQLite +
SQLAlchemy · Power BI · Jupyter Notebook
Running the Automation Script
Bash
This loads the raw CSV, cleans it (missing values, duplicates, outlier capping via IQR),
and exports:
reports/processed_superstore.csv — cleaned dataset
reports/ApexPlanet_KPI_Report.xlsx — KPI summary + Category/Region/Monthly breakdowns

for the complete executive summary with visuals and business recommendations.
Submitted as part of the ApexPlanet Software Pvt. Ltd. Data Analytics Internship — Task 5 (Final).