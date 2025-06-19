import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

def run():
    # Page title
    st.title('📊 SalesBoost - Exploratory Data Analysis')
    st.markdown('### Amazon Sales Report Dataset')

    # --- Sidebar ---
    st.sidebar.image("Amazon.png", use_column_width=True)
    st.sidebar.title("SalesBoost")
    st.sidebar.markdown("""
    **Team Members**
    - 👩‍🔬 Avisa Rahma Benedicta (Data Scientist)
    - 👨‍💻 Muhammad Farhan Hendriyanto (Data Engineer)
    - 👩‍🔬 Neila Ismahunnisa (Data Analyst)
    - 👩‍🔬 Sesilia Virdha Kezia (Data Scientist)            
    """)
    st.sidebar.markdown("""
    **Batch HCK-027** """)

    # Display team and project image
    col1, col2 = st.columns([1, 3])
    with col1:
        image1 = Image.open('D:/Hacktiv8/Z_deployment_finpro/Amazon.png')
        st.image(image1, caption='Amazon')
    with col2:
        st.markdown("""
        **Column Description:**
        - **Date**              : Date of the sale
        - **Status**            : Status of the sale (e.g., Shipped, Cancelled)
        - **Fulfilment**        : Method of fulfilment (Amazon or Merchant)
        - **Sales Channel**     : Platform used (e.g., Amazon.in)
        - **Ship Service Level**: Shipping speed (Standard, Expedited)
        - **Category**          : Product category (e.g., Set, Kurta)
        - **Size**              : Size of the product (e.g., M, L, XL)
        - **Amazon Standard Id**: Unique product identifier
        - **Qty**               : Quantity sold
        - **Currency**          : Currency used (e.g., INR)
        - **Sales**             : Revenue from the sale
        - **Clean Ship State**  : Normalized shipping state name
        - **Promotion Used**    : Whether a promo code was applied
        """)

    # Load dataset
    data = pd.read_csv("D:/Hacktiv8/Z_deployment_finpro/data_for_modelling.csv", 
                       index_col=False, parse_dates=['date'])
    st.write('### Dataset Preview')
    st.dataframe(data)
    st.write("---")

    # 1. Sales Trend
    data_trend = data.groupby('date')['sales'].sum()

    # Create a figure and a set of subplots
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(data_trend.index, data_trend, color='red', linewidth=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Sales Trend')
    st.write('The chart shows a decreasing trend in sales over time.')
    st.write("---")

    # 2. Seasonal Decomposition
    st.subheader("2. Time Series Decomposition")
    plt.rcParams['figure.figsize'] = (14, 9)

    # dekomposisi
    res = seasonal_decompose(data_trend, model='multiplicative', period=45)

    # Plot dan simpan figure yang dihasilkan
    fig = res.plot()
    
    st.pyplot(fig)
    st.markdown(''' 
             As mentioned earlier, the trend is decreasing. There appears to be a seasonal pattern occurring approximately every 1.5 months or 45 days (March 31st and May 15th).

            From the residual plot, we can see that the residual values are centered around 1, rather than zero. This suggests that there are components in the data that are not explained by the identified trend and seasonality. In other words, the decomposition leaves behind some unexplained variation, which could be noise or other hidden patterns not captured in the current decomposition.
             ''')
    st.write("---")

    # 3. Top Sales by Category
    st.subheader("3. Top Sales by Category")
    data_category = data[['category', 'sales']].groupby('category').sum().sort_values('sales', ascending=False)
    data_category = data_category.reset_index()

    fig = plt.figure(figsize=(15, 10))
    plt.bar(data_category['category'], data_category['sales'])
    plt.xlabel('Category')
    plt.ylabel('Sales')
    plt.title('Top Sales by Category')
    st.pyplot(fig)

    st.write('The Set category is the top-selling product category, followed by Kurta and Western Dress. On the other hand, Dupatta is the least popular category.')
    st.write("---")

    # 4. Product Distribution by Size & Category
    st.subheader("4. Product Distribution by Category and Size")
    # Step 1: Count product based on its category and size jumlah produk berdasarkan category dan size
    data_cat_size = data.groupby(['category', 'size'])['amazon_standard_id'].count().unstack(fill_value=0)

    # Step 2: Buat plot
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(data_cat_size.values)

    # Step 3: Set ticks dan label-nya
    ax.set_xticks(range(len(data_cat_size.columns)))
    ax.set_xticklabels(data_cat_size.columns, rotation=45, ha="right")

    ax.set_yticks(range(len(data_cat_size.index)))
    ax.set_yticklabels(data_cat_size.index)

    # Step 4: Tambahkan label di tiap sel
    for i in range(len(data_cat_size.index)):
        for j in range(len(data_cat_size.columns)):
            text = ax.text(j, i, data_cat_size.values[i, j],
                        ha="center", va="center", color="w")

    # Step 5: Judul dan layout
    ax.set_title("Distribution of Products Sold by Category and Size")
    fig.tight_layout()
    st.pyplot(fig)
    st.write('Set as the top-selling product category sold the most at size M, followed by L and S. There is no free size in this product category. Kurta sold the most at L, followed by M and XL and similar with Set, there is no free size in this product category. Dupatta only sold at 3 in free size.')
    st.write("---")

    # 5. Promotion Use Pie Chart
    data_pie = data['promotion_used'].value_counts()
    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.pie(data_pie, labels=data_pie.index.map({True: 'Use Promotion Code', False: 'Not Use Promotion Code'}), autopct='%.0f%%', colors=['#ff9999', '#66b3ff'])
    plt.title('Distribution of Promotion Used')
    # show plot
    st.pyplot(fig)
    st.write('Most of our customers tends to use promotion code when buying our products, while only 40% decided to not use promotion code.')
    st.write("---")

    # 6. Top 5 High-Spending Customers
    st.subheader("6. Top 5 High-Spending Customers")
    data_spend = data.groupby(['amazon_standard_id', 'category'])['sales'].sum().unstack(fill_value=0)

    top5_spender = data_spend.loc[
        data_spend.sum(axis=1).sort_values(ascending=False).head(5).index
    ]

    # Buat figure dan axes secara eksplisit
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot ke objek axes
    top5_spender.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title('Top 5 High Spender Customers - Stacked by Category')
    ax.set_xlabel('Amazon Standard ID')
    ax.set_ylabel('Total Sales')
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Tampilkan di Streamlit
    st.pyplot(fig)
    st.markdown("""
    Based on the chart above, even when displayed as a stacked bar chart, only one color (brown, representing the 'Set' category) is visible. 
    This could indicate two things: 
                
    (1) the 'Set' category is either the most expensive or the most preferred product, or 
                
    (2) high-spending customers tend to favor the 'Set' category.
    """)  
    st.markdown("---")
    st.markdown("### 🙏 Athenk kemayu pening kurus \
                \
                Thank you for exploring with us! 🙏")

if __name__ == '__main__':
    run()
