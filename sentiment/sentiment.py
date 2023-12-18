import streamlit as st
import pickle

model_filepath = "sentiment/sentiment_analysis.pkl"

try:
    with open(model_filepath, 'rb') as model_file:
        model = pickle.load(model_file)
        st.title('Sentiment Analysis Model')
        review = st.text_input('Enter your review:')
        submit = st.button('Predict')

        if submit and review:
            prediction = model.predict([review])
            if prediction[0] == 'positive':
                st.success('Positive Review')
            else:
                st.warning('Negative Review')
        elif submit:
            st.warning('Please enter a review before predicting.')

        st.text("Model loaded successfully.")
except FileNotFoundError:
    st.error(f"Error: Model file not found at {model_filepath}. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
