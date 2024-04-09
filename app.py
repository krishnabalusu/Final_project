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

# df_filtered = df_coffee.groupby("Country").agg({'UnitPrice': 'sum'})

#st.write(
'''
**Your filtered data:**


#st.dataframe(df_filtered)
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
sales_over_time = filtered_data.groupby('InvoiceDate')['Quantity'].sum()
st.subheader('Sales Trend Over Time')
st.line_chart(sales_over_time)

# Issues section
st.sidebar.header('Issues')
st.sidebar.write('1. Ensure data quality and handle missing values or outliers.')
st.sidebar.write('2. Handle user input validation to prevent errors.')

# Next steps section
st.sidebar.header('Next Steps')
st.sidebar.write('1. Enhance user interface with better styling and interactivity.')
st.sidebar.write('2. Add more advanced analytics and visualizations.')
st.sidebar.write('3. Deploy the Streamlit app for public access.')


# ------------------------------
# PART 2 : Plot
# ------------------------------

#st.write(
'''
## Visualize
#Compare this subset of reviews with the rest of the data.
'''
)

#st.bar_chart(df_filtered)

# fig = plot_sentiment(df_filtered, benchmarks)
# st.plotly_chart(fig)

# ------------------------------
# PART 3 : Analyze Input Sentiment
# ------------------------------

st.write(
'''
## Custom Sentiment Check

# Compare these results with the sentiment scores of your own input.



# text = st.text_input("Write a paragraph, if you like.", 
#                      "Your text here.")

# df_sentiment = get_sentence_sentiment(text, analyzer)

# st.dataframe(df_sentiment)
