# pip install -U streamlit
# streamlit run app.py

import streamlit as st
import pickle

model_filepath = "sentiment/sentiment_analysis.pkl"

try:
    with open(model_filepath, 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_filepath}.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")

# create title
st.title('Sentiment Analysis Model')

review = st.text_input('Enter your review:')

submit = st.button('Predict')

if submit:
    prediction = model.predict([review])

    # print(prediction)
    # st.write(prediction)

    if prediction[0] == 'positive':
        st.success('Positive Review')
    else:
        st.warning('Negative Review')
