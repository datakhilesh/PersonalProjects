import streamlit as st
import requests
import sqlite3
import nltk  # Import nltk
nltk.download('all')
from textblob import TextBlob
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from itertools import combinations

# Replace 'YOUR_NEWS_API_KEY' with your actual News API key
NEWS_API_KEY = '59b27c1999d74180b359282e670b94f9'

# News API endpoint for top headlines
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'

# Function to fetch, analyze, and store news data
def fetch_analyze_and_store_news(api_key, country='us', category='technology', page_size=10):
    # Set up parameters for the API request
    params = {
        'country': country,
        'category': category,
        'pageSize': page_size,
        'apiKey': api_key,
    }

    # Make the API request
    response = requests.get(NEWS_API_ENDPOINT, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        news_data = response.json()['articles']

        # Connect to the SQLite database
        conn = sqlite3.connect('news_database.db')
        cursor = conn.cursor()

        # Create table if not exists (including the 'category' column)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_data (
                title TEXT,
                description TEXT,
                url TEXT,
                publishedAt TEXT,
                source TEXT,
                sentiment REAL,
                category TEXT
            )
        ''')

        # Delete articles with title containing "[Removed]"
        cursor.execute('DELETE FROM news_data WHERE title LIKE "%[Removed]%"')

        # Fetch existing titles from the database
        existing_titles = [row[0] for row in cursor.execute('SELECT title FROM news_data').fetchall()]

        # Iterate through news articles
        for article in news_data:
            title = article['title']

            # Check if the title is not in the database to avoid duplicates
            if title not in existing_titles:
                # Perform sentiment analysis
                description = article['description']
                if description:
                    analysis = TextBlob(description)
                    sentiment = analysis.sentiment.polarity
                else:
                    sentiment = 0.0

                # Insert data into the database (including the 'category' information)
                cursor.execute('''
                    INSERT INTO news_data (title, description, url, publishedAt, source, sentiment, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (title, description, article['url'], article['publishedAt'], article['source']['name'], sentiment, category))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        st.success('News data successfully fetched, analyzed, and stored in the database.')

    else:
        st.error(f'Error fetching news data. Status code: {response.status_code}')

# Function to display database preview
def display_database_preview():
    conn = sqlite3.connect('news_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM news_data ORDER BY publishedAt DESC')
    rows = cursor.fetchall()

    st.title('Database Preview')
    if not rows:
        st.info('No data found in the database.')
    else:
        st.table(rows)

    conn.close()

# Function to display sentiment analysis distribution
def display_sentiment_distribution():
    conn = sqlite3.connect('news_database.db')
    df = pd.read_sql_query('SELECT * FROM news_data', conn)
    conn.close()

    plt.figure(figsize=(8, 6))
    plt.hist(df['sentiment'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Sentiment Analysis Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    st.pyplot(plt)

# Function to display source-wise sentiment
def display_source_sentiment():
    conn = sqlite3.connect('news_database.db')
    df = pd.read_sql_query('SELECT * FROM news_data', conn)
    conn.close()

    plt.figure(figsize=(12, 6))
    df.groupby('source')['sentiment'].mean().sort_values().plot(kind='bar', color='lightcoral')
    plt.title('Average Sentiment by News Source')
    plt.xlabel('News Source')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

# Function to display most positive, negative, and neutral categories
def display_most_sentiments():
    conn = sqlite3.connect('news_database.db')
    df = pd.read_sql_query('SELECT * FROM news_data', conn)
    conn.close()

    # Get unique categories in the database
    categories = df['category'].unique()

    most_positive_category = None
    most_negative_category = None
    most_neutral_category = None
    max_positive_score = -1
    min_negative_score = 1
    min_neutral_score = 1

    for category in categories:
        category_df = df[df['category'] == category]

        if not category_df.empty:
            average_score = category_df['sentiment'].mean()

            # Update most positive category
            if average_score > max_positive_score:
                max_positive_score = average_score
                most_positive_category = category

            # Update most negative category
            if average_score < min_negative_score:
                min_negative_score = average_score
                most_negative_category = category

            # Update most neutral category
            if abs(average_score) < min_neutral_score:
                min_neutral_score = abs(average_score)
                most_neutral_category = category

    st.title('Most Sentiments by Category')
    if most_positive_category:
        st.code(f'Most Positive Category: {most_positive_category.capitalize()} (Average Score: {max_positive_score:.2f})')
    if most_negative_category:
        st.code(f'Most Negative Category: {most_negative_category.capitalize()} (Average Score: {min_negative_score:.2f})')
    if most_neutral_category:
        st.code(f'Most Neutral Category: {most_neutral_category.capitalize()} (Average Score: {min_neutral_score:.2f})')

# Function to display Keyword Co-occurrence Network Graph
def display_keyword_cooccurrence_network():
    conn = sqlite3.connect('news_database.db')
    df = pd.read_sql_query('SELECT * FROM news_data', conn)
    conn.close()

    # Create a graph
    G = nx.Graph()

    # Iterate through each article and extract keywords
    for _, article in df.iterrows():
        description = article['description']
        if description:
            analysis = TextBlob(description)
            keywords = [word.lower() for word, tag in analysis.tags if tag.startswith('NN')]
            G.add_nodes_from(keywords)
            for node1, node2 in combinations(keywords, 2):
                if G.has_edge(node1, node2):
                    G[node1][node2]['weight'] += 1
                else:
                    G.add_edge(node1, node2, weight=1)

    # Draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, width=[d['weight'] for u, v, d in G.edges(data=True)], edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title('Keyword Co-occurrence Network Graph')
    st.pyplot(plt)

# Streamlit app
if __name__ == "__main__":
    st.title('Real-Time News Data Processing')

    # Allow the user to select the news category in the sidebar
    category = st.sidebar.selectbox('Select News Category', ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'])

    # Fetch and store news data if the button is clicked
    if st.sidebar.button('Fetch and Store News Data'):
        fetch_analyze_and_store_news(api_key=NEWS_API_KEY, category=category)

    # Display most positive, negative, and neutral sentiment scores for each category
    display_most_sentiments()

    # Display the database preview if the checkbox is selected
    if st.sidebar.checkbox('Preview Database'):
        display_database_preview()

    # Display the sentiment analysis distribution if the checkbox is selected
    if st.sidebar.checkbox('Sentiment Analysis Distribution'):
        display_sentiment_distribution()

    # Display source-wise sentiment if the checkbox is selected
    if st.sidebar.checkbox('Source-wise Sentiment'):
        display_source_sentiment()

    # Display the Keyword Co-occurrence Network Graph if the checkbox is selected
    if st.sidebar.checkbox('Keyword Co-occurrence Network Graph'):
        display_keyword_cooccurrence_network()
