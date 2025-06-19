import EDA_finpro
import Predict_finpro
from Introduction import introduction
import streamlit as st

st.set_page_config(
    page_title="SalesBoost | Sales Forecast & Customer Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Halaman Navigasi ---
page = st.sidebar.selectbox('Pilih Halaman', ('📊 Introduction', '📈 Predict', '📉 EDA'))

# --- Routing berdasarkan pilihan user ---
if page == '📉 EDA':
    EDA_finpro.run()
elif page == '📈 Predict':
    Predict_finpro.run()
else:
    introduction()