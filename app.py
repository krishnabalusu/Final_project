import os
import pickle

import streamlit as st
from dotenv import load_dotenv
import pandas as pd
#import matplotlib.pyplot as plt



# from utils.b2 import B2


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'coffee_analysis_w_sentiment.csv'


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# # load Backblaze connection
# b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
#         key_id=os.environ['B2_KEYID'],
#         secret_key=os.environ['B2_APPKEY'])


# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df_coffee = b2.get_df(REMOTE_DATA)

    # average sentiment scores for the whole dataset
    benchmarks = df_coffee[['neg', 'neu', 'pos', 'compound']] \
                    .agg(['mean', 'median'])
    
    return df_coffee, benchmarks


@st.cache_resource
def get_model():
    with open('./model.pickle', 'rb') as f:
        analyzer = pickle.load(f)
    
    return analyzer

# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 0 : Overview
# ------------------------------


# df_coffee, benchmarks = get_data()
# analyzer = get_model()

df_coffee = pd.read_csv("Cleaned.csv")

# ------------------------------
# PART 1 : Filter Data
# ------------------------------

# Main title
st.title('Online Retail Store Analysis')

# Sidebar for user input
st.sidebar.title('Select Options')

# Provide option to select a country
selected_country = st.sidebar.selectbox('Select Country', df_coffee['Country'].unique())

# Filter data based on selected country
filtered_data = df_coffee[df_coffee['Country'] == selected_country]

# Display sales data for the selected country
st.subheader(f'Sales Data for {selected_country}')
st.write('Total Sales:', filtered_data['Quantity'].sum())

# Additional analytics or visualizations for the selected country can be added here
# For example, you could display a bar chart showing sales trend over time for the selected country

# Calculate and display sales trend over time for the selected country
sales_over_time = filtered_data.groupby('InvoiceDate')['Quantity'].sum().reset_index()
st.subheader('Sales Trend Over Time')
st.line_chart(sales_over_time.set_index('InvoiceDate'))

st.write('''
    The application filters the dataset accordingly, extracting sales information relevant to the chosen country. It then computes and displays key metrics, such as the total sales volume, providing users with a snapshot of the retail activity within their selected region.

Furthermore, the application goes beyond simple data presentation by incorporating interactive visualizations. For instance, it generates a dynamic line chart illustrating the sales trend over time for the selected country. This visual representation allows users to discern patterns, fluctuations, and seasonal variations in sales activity, facilitating deeper insights into market dynamics
''')
st.header('Issues')
st.write("""
 One issue we've encountered is ensuring data quality and handling missing values or outliers. To mitigate this, we plan to carefully inspect the dataset, identify any inconsistencies or anomalies, and implement appropriate data cleaning techniques.
 """)
st.header('Next Steps')
st.write("""
1. Enhance user interface with better styling and interactivity. We aim to improve the visual appeal and usability of the web app by incorporating modern design principles and interactive elements such as dropdown menus, sliders, and buttons.

2. Add more advanced analytics and visualizations. In addition to basic sales data, we plan to integrate more sophisticated analytics techniques such as predictive modeling, clustering, and time series forecasting to provide deeper insights into the online retail store's performance.
""")

