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



class SalesAnalysis:
    def __init__(self, df_coffee):
        self.df = df_coffee

    def calculate_sales_performance(self, country):
        country_df = self.df[self.df['Country'] == country]
        sales_performance = country_df.groupby('Country')['Quantity'].sum()
        return sales_performance

    def plot_sales_performance(self, sales_performance, country):
        st.subheader(f"Sales Performance for {country}")
        fig = px.bar(sales_performance, x=sales_performance.index, y='Quantity',
                     labels={'x': 'Country', 'Sales': 'Total Sales'},
                     title=f"Sales Performance for {country}")
        st.plotly_chart(fig)

    def plot_product_distribution(self, country, top_n=15):
        # Group by category and sum quantities
        df_coffee = self.df.groupby('Description')['Quantity'].sum().reset_index()

        # Sort categories by quantity and select top N categories
        df_coffee = df_coffee.sort_values(by='Quantity', ascending=False).head(top_n)

        # Plot pie chart
        fig = px.pie(df_coffee, values='Quantity', names='Description',
                     title=f"Top {top_n} Product Categories for {country}",
                     width=800, height=500)
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(showlegend=True)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig)

    def plot_sales_trend(self, country):
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], format='%Y-%m-%d %H:%M:%S')
        sales_trend = self.df.resample('M', on='InvoiceDate')['Quantity'].sum().reset_index()
        fig = px.line(sales_trend, x='InvoiceDate', y='Quantity',
                      labels={'InvoiceDate': 'Date', 'Quantity': 'Total Sales'},
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

    # Create instance of SalesAnalysis class
    sales_analysis = SalesAnalysis(df_coffee)

    # Perform analysis based on user input
    if st.sidebar.button("Analyze"):
        sales_performance = sales_analysis.calculate_sales_performance(country)
        sales_analysis.plot_sales_performance(sales_performance, country)
        sales_analysis.plot_product_distribution(country)
        sales_analysis.plot_sales_trend(country)

if __name__ == "__main__":
    main()
