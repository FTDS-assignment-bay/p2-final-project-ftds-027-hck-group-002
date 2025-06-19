# Judul Project
SalesBoost

## Repository Outline

```
p2-final-project-ftds-027-hck-group-002/
├── Amazon_sales.csv
├── Cleaning_DAG.py
├── README.md
├── exploratory_data_analysis.ipynb
├── customer_clustering/
│   ├── .gitignore
│   └── clustering.ipynb
├── main_model_timeseries/
│   ├── data_test.pkl
│   ├── forecasting_model.ipynb
│   └── inference.ipynb
├── other_model_timeseries/
│   ├── ar_sar_holt.ipynb
│   ├── prophet.ipynb
│   └── LSTM.ipynb
```

## Problem Background

1. The company is experiencing a downward trend in sales.
2. which poses a risk to long-term profitability.
3. The current promotional strategies are considered ineffective and poorly targeted.
4. This is mainly due to a lack of deep understanding of customer behavior.


## Project Output

Performed Exploratory Data Analysis before and after clustering, visualized using Tableau, and deployed the Time Series Machine Learning model as an interactive application on Hugging Face.


## Data

Data Source : https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data
The dataset used is "Amazon Sale Report.csv".

Number of columns : 24

Number of rows : 128.975

Data raw (before cleaning) :

1. index
2. Order ID
3. Date
4. Status
5. Fulfilment
6. Sales Channel
7. ship-service-level
8. Style
9. SKU
10. Category
11. Size
12. ASIN
13. Courier Status
14. Qty
15. currency
16. Amount
17. ship-city
18. ship-state
19. ship-postal-code
20. ship-country
21. promotion-ids
22. B2B
23. fulfilled-by
24. Unnamed: 22

Data used (after cleaning):

Number of Columns : 13
1. date
2. status
3. fulfilment
4. sales_channel
5. ship-service-level
6. category
7. size
8. amazon_standard_id (column name changed from ASIN)
9. qty
10. currency
11. sales
12. clean_ship_state
13. promotion_used


## Method
This project applies unsupervised learning models, specifically time series forecasting and clustering. For the time series analysis, six models were evaluated: ARIMA, SARIMA, Holt-Winters, LSTM, Prophet, and SARIMAX. Among them, SARIMAX was selected as the best-performing model.
For the clustering task, two models were tested: K-Prototype and Gower distance-based clustering, with K-Prototype chosen as the most suitable model.


## Stacks
Programming language:
1. Python

Libraries:
1. Matplotlib
2. Numpy
3. Pandas
4. Pylab
5. Scikit-learn
6. Seaborn
7. Statsmodels

Tools:
1. Airflow
2. Docker
3. Hugging Face
4. Streamlit
5. Tableau


## Reference
Dataset:
[E-Commerce Sales Dataset] (https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data)

Dashboard Tableau: 
https://public.tableau.com/app/profile/muhammad.farhan.hendriyanto/viz/finalproject_17503214545810/DashboardSalesBoostAfterClustering?publish=yes

Deployment Hugging Face:
https://huggingface.co/spaces/farhanpaul21/Final_Project
