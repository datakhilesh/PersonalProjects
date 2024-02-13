import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import sqlite3
from datetime import datetime

def get_weather(api_key, city, country='US'):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': f'{city},{country}', 'appid': api_key, 'units': 'imperial'}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        st.error(f'Error fetching weather data for {city}.')
        return None

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0/9.0

def store_weather_data(api_key, city, country='US'):
    weather_data = get_weather(api_key, city, country)
    
    if weather_data:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temperature_fahrenheit = weather_data['main']['temp']
        temperature_celsius = fahrenheit_to_celsius(temperature_fahrenheit)

        conn = sqlite3.connect('weather_database.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT,
                temperature_celsius REAL,
                description TEXT,
                timestamp TEXT
            )
        ''')

        cursor.execute("INSERT INTO weather_data (city, temperature_celsius, description, timestamp) VALUES (?, ?, ?, ?)",
                       (city, temperature_celsius, weather_data['weather'][0]['description'], timestamp))

        conn.commit()
        conn.close()
        #st.success(f'Successfully stored weather data for {city} in the database.')

def display_database_preview():
    conn = sqlite3.connect('weather_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM weather_data ORDER BY timestamp DESC')
    rows = cursor.fetchall()

    st.title('Database Preview')
    if not rows:
        st.info('No data found in the database.')
    else:
        st.table(rows)

    conn.close()

def display_weather_map(api_key, cities):
    st.title('Real-Time Weather Map for USA Cities')

    # Create a folium map centered around the USA
    usa_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4)

    for city in cities:
        weather_data = get_weather(api_key, city)
        if weather_data:
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']

            # Add a marker for each city with weather information
            folium.Marker(
                location=[lat, lon],
                popup=f'{city}\nTemperature: {temperature} °F\nDescription: {description}',
                icon=folium.Icon(color='blue')
            ).add_to(usa_map)

    # Display the map using Streamlit
    folium_static(usa_map)

    # Add a refresh button to fetch and store the latest weather data
    if st.button('Refresh Weather Data'):
        for city in cities:
            store_weather_data(api_key, city)

    # Add a preview button to show all entries in the database
    if st.button('Preview Database'):
        display_database_preview()

# Replace 'YOUR_API_KEY' with your actual OpenWeather API key
api_key = '148d1eda096dc439cc28be67d2bb30b4'

# List of cities in the USA
us_cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']

# Run the Streamlit app
if __name__ == "__main__":
    display_weather_map(api_key, us_cities)
