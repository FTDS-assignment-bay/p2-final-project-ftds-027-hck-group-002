# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pickle

# Load model
with open('D:\Hacktiv8\Z_deployment_finpro\model_finpro.pkl', 'rb') as file:
    model = pickle.load(file)

# Load test data
with open('D:\Hacktiv8\Z_deployment_finpro\data_test_finpro.pkl', 'rb') as file:
    test = pickle.load(file)

# Pastikan date dalam datetime format
test.index = pd.to_datetime(test.index)

# Forecasting function
def forecast_sales(n_days, qty_sum_input):   
    # Future qty_sum sebagai eksogen variabel
    future_exog_vars = pd.DataFrame(qty_sum_input, columns=['qty_sum'])

    # Buat index tanggal untuk prediksi
    forecast_index = pd.date_range(start=test.index[-1] + pd.Timedelta(days=1), 
                                   periods=n_days, freq='D')

    # Forecast
    forecast = model.get_forecast(steps=n_days, exog=future_exog_vars)
    forecast_mean = forecast.predicted_mean

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(forecast_index, forecast_mean, label='Forecasted Total Sales', color='red', linestyle='--')
    ax.set_title('Forecast of Total Sales Over the Next Days')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Sales')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig, forecast_index, forecast_mean


# Streamlit app
def run():

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

    st.title("Inventory Demand Forecast")
    st.write("---")
    # st.image("mc_inv.jpg", caption="Inventory Management and Demand Forecasting")
    st.write("---")
    st.write("# Forecast Future Demand")
    
    n_days = st.slider("Number of Days to Forecast", 1, 30, 10)
    
    qty_sum_input = []
    for i in range(n_days):
        val = st.number_input(f"Day {i+1} Total Quantity", value=100, step=1)
        qty_sum_input.append(val)
    
    if st.button("Generate Forecast"):
        fig, forecast_index, forecast_mean = forecast_sales(n_days, qty_sum_input)
        
        # Tampilkan plot
        st.pyplot(fig)
        
        # Tampilkan tabel hasil
        forecast_df = pd.DataFrame({
            'Date': forecast_index.strftime('%d-%m-%Y'),  # Format jadi dd-mm-yyyy
            'Forecasted Total Sales': forecast_mean
        }).reset_index(drop=True)
        
        st.write("### Forecast Table")
        st.write(forecast_df)

if __name__ == "__main__":
    run()