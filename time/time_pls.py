# sentiment_analysis_app.py
import streamlit as st
from textblob import TextBlob
import pandas as pd

# Streamlit app
def main():
    st.title("Sentiment Analysis App")

    # CSV URL input
    csv_url = st.text_input("Enter the CSV URL:", "https://raw.githubusercontent.com/datasets/sentiment140/master/data/training.1600000.processed.noemoticon.csv")

    if csv_url:
        try:
            # Load data from CSV URL
            data = pd.read_csv(csv_url, encoding='latin-1', header=None, names=['target', 'ids', 'date', 'flag', 'user', 'text'])
            st.subheader("Data Loaded from CSV URL:")
            st.write(data.head())

            # Sentiment Analysis
            st.subheader("Sentiment Analysis:")
            text_input = st.text_area("Enter text for sentiment analysis:")
            if st.button("Analyze Sentiment"):
                if text_input:
                    # Perform sentiment analysis using TextBlob
                    blob = TextBlob(text_input)
                    sentiment_score = blob.sentiment.polarity

                    # Display result
                    st.write(f"Sentiment Score: {sentiment_score}")

                    # Categorize sentiment
                    if sentiment_score > 0:
                        st.success("Positive Sentiment")
                    elif sentiment_score < 0:
                        st.error("Negative Sentiment")
                    else:
                        st.info("Neutral Sentiment")
                else:
                    st.warning("Please enter text for sentiment analysis.")
        except Exception as e:
            st.error(f"Error loading data from CSV URL: {e}")

if __name__ == "__main__":
    main()
