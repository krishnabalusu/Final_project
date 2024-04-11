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
st.write(
'''
# Review Sentiment Analysis
We pull data from our Backblaze storage bucket, and render it in Streamlit.
''')

# df_coffee, benchmarks = get_data()
# analyzer = get_model()

df_coffee = pd.read_csv("Cleaned.csv")

# ------------------------------
# PART 1 : Filter Data
# ------------------------------

# Extract unique countries from the dataset
countries = df_coffee['Country'].unique()

# Create a dropdown menu for selecting countries
selected_country = st.selectbox('Select a country', countries)

# Display the selected country
st.write('You selected:', selected_country)
# Filter sales data based on the selected country
filtered_sales = df[df['Country'] == selected_country]

# Display the filtered sales data
st.write('Sales data for', selected_country)
st.write(filtered_sales)
