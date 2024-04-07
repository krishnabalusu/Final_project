import os

import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2
import pandas as pd
import matplotlib.pyplot as plt

REMOTE_DATA = 'Cleaned.csv'

load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_keyID'],
        secret_key=os.environ['B2_applicationKey'])

def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df = b2.get_df(REMOTE_DATA)
    
    return df

df = get_data()
st.write("Display the frequency of different price ranges, helping to understand the pricing structure of the products.")

fig = plt.figure(figsize=(10, 6))
plt.hist(df['UnitPrice'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Unit Prices')
plt.xlabel('Unit Price')
plt.ylabel('Frequency')
plt.grid(True)

st.plotly_chart(fig)

st.dataframe(df)
