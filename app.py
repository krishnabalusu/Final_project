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

import streamlit as st
import pandas as pd
import plotly.express as px

class SalesAnalysis:
    def __init__(self, df_coffee):
        self.df_coffee = df_coffee

    def calculate_sales_performance(self, country):
        country_df = self.df_coffee[self.df_coffee['Country'] == country]
        sales_performance = country_df.groupby('Country')['Quantity'].sum()
        return sales_performance

    def plot_sales_performance(self, sales_performance, country):
        st.subheader(f"Sales Performance for {country}")
        st.write(sales_performance)
        st.write('The bar chart depicts information about the distribution of product categories based on quantities sold in a specific country. By filtering the dataset and grouping the data by product categories, the method identifies the top 15 product categories with the highest sales volumes. The resulting bar chart visualizes this information, with each bar representing a product category and its height indicating the total quantity sold. This visualization enables businesses to identify popular product categories, understand market preferences, and make strategic decisions regarding inventory management and marketing strategies tailored to meet customer demands.')

    def plot_product_distribution_bar(self, country, top_n=15):
        country_df = self.df_coffee[self.df_coffee['Country'] == country]
        df_product = country_df.groupby('Description')['Quantity'].sum().reset_index()
        df_product = df_product.sort_values(by='Quantity', ascending=False).head(top_n)
        fig = px.bar(df_product, x='Description', y='Quantity', 
                     title=f"Top {top_n} Product Categories for {country}",
                     labels={'Description': 'Product Category', 'Quantity': 'Quantity'})
        st.plotly_chart(fig)
        st.write('kittu')

    def plot_product_distribution_pie(self, country, top_n=15):
        country_df = self.df_coffee[self.df_coffee['Country'] == country]
        df_product = country_df.groupby('Description')['Quantity'].sum().reset_index()
        df_product = df_product.sort_values(by='Quantity', ascending=False).head(top_n)
        fig = px.pie(df_product, values='Quantity', names='Description',
                     title=f"Top {top_n} Product Categories for {country}")
        st.plotly_chart(fig)

    def plot_sales_trend(self, country):
        country_df = self.df_coffee[self.df_coffee['Country'] == country]
        country_df['InvoiceDate'] = pd.to_datetime(country_df['InvoiceDate'], format='%Y-%m-%d %H:%M:%S')
        sales_trend = country_df.resample('M', on='InvoiceDate')['Quantity'].sum().reset_index()
        fig = px.line(sales_trend, x='InvoiceDate', y='Quantity',
                      labels={'InvoiceDate': 'Date', 'Quantity': 'Total Sales'},
                      title=f"Sales Trend over Time for {country}")
        st.plotly_chart(fig)

    def plot_geographical_distribution(self):
        st.subheader("Geographical Distribution of Sales")
        sales_by_country = self.df_coffee.groupby('Country')['Quantity'].sum().reset_index()
        fig = px.choropleth(sales_by_country, 
                            locations='Country', 
                            locationmode='country names',
                            color='Quantity', 
                            hover_name='Country', 
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title='Sales by Country')
        fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
        st.plotly_chart(fig)




def main():
    st.title("Sales Performance Analysis")

    # Load the dataset


    # Display dataset
    st.subheader("Dataset")
    st.dataframe(df_coffee)

    # Create instance of SalesAnalysis class
    sales_analysis = SalesAnalysis(df_coffee)

    # Sidebar options
    st.sidebar.header("Options")
    
    country = st.sidebar.selectbox("Select Country", df_coffee['Country'].unique())

    # Perform analysis based on user input
    if st.sidebar.button("Analyze"):
         sales_performance = sales_analysis.calculate_sales_performance(country)
         sales_analysis.plot_sales_performance(sales_performance, country)
         sales_analysis.plot_product_distribution_bar(country)
         sales_analysis.plot_product_distribution_pie(country)
         sales_analysis.plot_sales_trend(country)
         sales_analysis.plot_geographical_distribution()
        

if __name__ == "__main__":
    main()


   
       
