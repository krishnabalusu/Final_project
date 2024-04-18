import os
import pickle



import streamlit as st
from dotenv import load_dotenv
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px



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

def load_data(df_coffee):
    try:
        return df_coffee
    except FileNotFoundError:
        print("File not found.")
        return None

# Analysis function
def calculate_sales_performance(df_coffee):
    sales_performance = df_coffee.groupby('Country')['Quantity'].sum()
    return sales_performance

# Visualization functions
def plot_sales_performance(sales_performance, country):
    st.subheader(f"Sales Performance for {country}")
    st.write(sales_performance)

def plot_sales_performance(sales_performance, country):
    st.subheader(f"Sales Performance for {country}")
    fig = px.bar(sales_performance, x=sales_performance.index, y='Quantity',
                 labels={'x': 'Country', 'Sales': 'Total Sales'},
                 title=f"Sales Performance for {country}")
    st.plotly_chart(fig)

def plot_product_distribution(df_coffee, country):
    product_distribution = df_coffee.groupby('Description')['Quantity'].sum().reset_index()
    fig = px.pie(product_distribution, values='Quantity', names='Description',
                 title=f"Product Category Distribution for {country}")
    st.plotly_chart(fig)

def plot_sales_trend(df_coffee, country):
    df['InvoiceDate'] = pd.to_datetime(df_coffee['InvoiceDate'], format='%Y-%m-%d %H:%M:%S')
    sales_trend = df_coffee.resample('M', on='InvoiceDate')['Quantity'].sum().reset_index()
    fig = px.line(sales_trend, x='InvoiceDate', y='Quantity',
                  labels={'InvoiceDate': 'Date', 'Sales': 'Total Sales'},
                  title=f"Sales Trend over Time for {country}")
    st.plotly_chart(fig)

def main():
    st.title("Sales Performance Analysis")
    
    # Load the dataset
    
    
    # Display dataset
    st.subheader("Dataset")
    st.dataframe(df_coffee)
    
    # Sidebar options
    st.sidebar.header("Options")
    country = st.sidebar.selectbox("Select Country", df_coffee['Country'].unique())
    
    # Perform analysis based on user input
    if st.sidebar.button("Analyze"):
        country_df = df_coffee[df_coffee['Country'] == country]
        sales_performance = calculate_sales_performance(country_df)
        plot_sales_performance(sales_performance, country)
        plot_product_distribution(country_df, country)
        plot_sales_trend(country_df, country)

if __name__ == "__main__":
    main()
