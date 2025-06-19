import streamlit as st
from PIL import Image

def introduction():

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

    # --- Main Content ---
    st.title("🚀 SalesBoost Dashboard")
    st.markdown("""
    SalesBoost is a project aimed at increasing sales by addressing a declining trend through accurate forecasting.
    It combines **customer behavior clustering** to uncover actionable segments for more effective promotions.

    This app delivers two key features:
    - 📈 **Sales Forecast Deployment**
    - 👥 **Interactive Customer Dashboard**
    """)

    st.write("---")

    # --- Team ---
    st.title("Let's Meet Our Team")
    st.image("Team.jpg", caption="Group 2", use_column_width=True)

    # # Fungsi untuk membuka dan merotasi gambar 270 derajat
    # def load_and_rotate(image_path):
    #     img = Image.open(image_path)
    #     size = img.resize((300,300))
    #     rotated = img.rotate(90, expand=True)

    #     return rotated

    # # Layout 2 kolom
    # col1, col2 = st.columns(2)

    # with col1:
    #     st.image(load_and_rotate('Sesil.JPG'), caption='Sesil as Data Scientist', use_column_width=True)
    #     st.image(load_and_rotate('Avisa.JPG'), caption='Avisa as Data Scientist', use_column_width=True)

    # with col2:
    #     st.image(load_and_rotate('Ka Nei.JPG'), caption='Neila as Data Analyst', use_column_width=True)
    #     st.image(load_and_rotate('Farhan.JPG'), caption='Farhan as Data Engineer', use_column_width=True)


    # --- Sales Forecast Section ---
    st.header("📈 Predict Sales for the Next N Days")
    st.markdown("Upload external model & input demand variables to generate sales forecasts.")
    # st.image("forecast_example.png", caption="Forecast Output Example", use_column_width=True)

    st.write("---")

    # --- Customer Segmentation Section ---
    st.header("👥 Interactive Customer Clustering Dashboard")
    st.markdown("Explore customer behavior and segment patterns through clustering.")

    st.image("Dashboard Example.png", caption="Example of Dashboard", use_column_width=True)

    # Tombol untuk membuka Tableau
    tableau_url = "https://public.tableau.com/views/P0M1_MuhammadFarhanHendriyanto/MainDashboard?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
    st.markdown(f"[🔗 Click here to open the dashboard in a new tab]({tableau_url})")

    st.info("Note: Due to Tableau Public's restrictions, this dashboard cannot be displayed directly in Streamlit.")
    st.write("---")

    # --- About Section ---
    st.header("ℹ️ About SalesBoost")
    st.markdown("""
    **Objective:**
    - Reverse the declining sales trend using intelligent forecasting and segmentation.

    **Methodology:**
    - Time Series Forecasting (SARIMAX)
    - Customer Clustering (K-Prototypes)
    - Dashboarding using Streamlit & Tableau

    **Deliverables:**
    - Forecast Deployment Page
    - Customer Segmentation Dashboard

    ---
    #BismillahSuksesSelalu
    """)
if __name__ == "__main__":
    introduction()