import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval

# Load the CSV data
df = pd.read_csv('moviesdataset_2023.csv')

# Convert the genre column to a list
df['genre'] = df['genre'].apply(literal_eval)

# Convert the list of genres to a space-separated string
df['genre'] = df['genre'].apply(lambda x: ' '.join(x))

# Streamlit app
st.title("Movie Recommendation System")

# Prompt the user to choose between entering a movie or selecting a genre
option = st.radio("Choose an option:", ["Enter a movie", "Choose a genre"])

if option == "Enter a movie":
    # User enters a movie
    user_preference = st.text_input("Enter a movie:")

else:
    # User chooses a genre
    unique_genres = df['genre'].explode().unique()
    selected_genre_index = st.selectbox("Choose a genre:", range(1, len(unique_genres) + 1), format_func=lambda x: unique_genres[x - 1])
    selected_genre = unique_genres[selected_genre_index - 1]

    # Filter movies by the selected genre
    genre_filtered_df = df[df['genre'].str.contains(selected_genre)]

    if genre_filtered_df.empty:
        st.warning(f"No movies found for the '{selected_genre}' genre. Please try another genre.")
        st.stop()

    # Sort movies by vote count in descending order
    sorted_df = genre_filtered_df.sort_values(by='votes', ascending=False)

    # Display movies with the highest vote count in the selected genre
    st.subheader(f"Top movies in the '{selected_genre}' genre based on vote count:")
    st.table(sorted_df[['name', 'votes']].head())

    # Ask the user to choose a movie from the displayed list
    user_preference = st.text_input("Choose a movie from the list above:")

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Create a TF-IDF matrix based on combined features
tfidf_matrix = tfidf_vectorizer.fit_transform(df['genre'] + ' ' + df['description'])

# Calculate weighted cosine similarity
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations
def get_recommendations(movie_title, cosine_similarities=cosine_similarities, df=df):
    try:
        movie_index = df[df['name'] == movie_title].index[0]
    except IndexError:
        st.warning(f"No movie found with the title '{movie_title}'. Please try another movie.")
        st.stop()

    similarity_scores = list(enumerate(cosine_similarities[movie_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similar_movies = similarity_scores[1:6]  # Exclude the movie itself, and get top 5
    recommended_movies = df.loc[[index[0] for index in similar_movies], 'name'].tolist()
    return recommended_movies

# Get recommendations based on user's choice
recommendations = get_recommendations(user_preference)

# Display recommended movies
if recommendations:
    st.subheader(f"Recommended movies for '{user_preference}':")
    st.write(recommendations)
else:
    st.warning(f"No recommendations found for '{user_preference}'. Please try another movie or genre.")
