import snowflake.connector as sf
from snowflake.connector import DictCursor
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

connection = sf.connect(user = 'GayathriM',
                        password = 'Raasi123$',
                        account = 'PVQJPLS-AM90580',
                        warehouse = 'COMPUTE_WH',
                        database = 'BOOKS',
                        schema = 'PUBLIC',
                        role = 'ACCOUNTADMIN')

cur=connection.cursor(DictCursor)

# Retrieve data from the Snowflake database
query = 'SELECT * FROM SCRAPED_DATA'  # Replace with your actual table name
df = pd.read_sql(query, con=connection) 


# Layout setup
st.title('Bookstore Analysis Dashboard')

# KPIs at the top
st.markdown('<h2 style="text-align: center;">KPIs</h2>', unsafe_allow_html=True)

# Total number of books
total_books = df.shape[0]
average_price = int(df['PRICE'].mean())
average_rating = int(df['RATING'].mean())

kpi_html = f"""
    <div style="display: flex; justify-content: space-between; text-align: center;">
        <div>
            <h4>Total Books:</h4>
            <p>{total_books}</p>
        </div>
        <div>
            <h4>Average Price:</h4>
            <p>{average_price}</p>
        </div>
        <div>
            <h4>Average Rating:</h4>
            <p>{average_rating}</p>
        </div>
    </div>
"""

# Display KPIs
st.markdown(kpi_html, unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.title('Filters')

# Price filter
min_price = st.sidebar.slider('Minimum Price', float(df['PRICE'].min()), float(df['PRICE'].max()), float(df['PRICE'].min()))
filtered_price_df = df[df['PRICE'] >= min_price]

# Rating filter as multi-select
selected_ratings = st.sidebar.multiselect('Select Ratings:', sorted(df['RATING'].unique(), reverse=True))

# Filter the dataframe based on the selected ratings
filtered_df = filtered_price_df[filtered_price_df['RATING'].isin(selected_ratings)]

# Additional filters
top_n = st.sidebar.slider('Select Top N Books:', 1, 10, 1)

# Create columns for side-by-side layout
col1, col2 = st.columns(2)

# Distribution of Ratings (Pie chart)
with col1:
    st.subheader('Distribution of Ratings:')
    fig1, ax1 = plt.subplots()
    rating_counts = df['RATING'].value_counts()
    ax1.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# Distribution of Price (Histogram with 10 bins)
with col2:
    st.subheader('Distribution of Price:')
    fig2, ax2 = plt.subplots()
    sns.histplot(df['PRICE'], bins=10, kde=False, ax=ax2)
    st.pyplot(fig2)

# Display the top N books in a table
st.subheader(f'Top {top_n} Books')
top_books_table = filtered_df.nlargest(top_n, 'RATING')
st.table(top_books_table[['TITLE', 'PRICE', 'RATING', 'AVAILABILITY']])
