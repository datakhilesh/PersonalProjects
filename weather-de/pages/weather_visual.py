import streamlit as st
import pandas as pd
import sqlite3

# Streamlit App
st.title('Weather Data Explorer')

# Create a connection to the SQLite database
conn = sqlite3.connect('weather-de/weather_database.db')  # Update with your actual database file path

# Sidebar filters
cities = st.sidebar.multiselect(
    'Select Cities:',
    pd.read_sql_query('SELECT DISTINCT city FROM weather_data', conn)['city'].tolist(),
    default=[]  # Set an empty default list to handle the case where no cities are selected
)
start_date = st.sidebar.date_input('Select Start Date:', pd.to_datetime(pd.read_sql_query('SELECT MIN(timestamp) FROM weather_data', conn)['MIN(timestamp)'].iloc[0]))
end_date = st.sidebar.date_input('Select End Date:', pd.to_datetime(pd.read_sql_query('SELECT MAX(timestamp) FROM weather_data', conn)['MAX(timestamp)'].iloc[0]))

# Build the SQL query based on the selected filters
if len(cities) == 1:
    query = f"SELECT * FROM weather_data WHERE city = '{cities[0]}' AND timestamp BETWEEN '{start_date}' AND '{end_date}'"
else:
    query = f"SELECT * FROM weather_data WHERE city IN {tuple(cities)} AND timestamp BETWEEN '{start_date}' AND '{end_date}'"

# Execute the query and fetch the results into a DataFrame
filtered_df = pd.read_sql_query(query, conn)

# Display the filtered data
st.write(f"Showing data for {', '.join(cities)} from {start_date} to {end_date}")
st.dataframe(filtered_df)

# Line chart showing temperature trends
st.line_chart(filtered_df.set_index('timestamp')['temperature_celsius'])

# Bar chart showing weather description distribution
st.bar_chart(filtered_df['description'].value_counts())

# Map showing cities and their temperatures
st.map(filtered_df[['city', 'temperature_celsius', 'description', 'timestamp']])

# Close the connection
conn.close()
