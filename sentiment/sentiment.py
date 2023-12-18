# Install required modules
try:
    import streamlit
except ModuleNotFoundError:
    !pip install streamlit
    import streamlit

import pickle

model_filepath = "sentiment/sentiment_analysis.pkl"

try:
    with open(model_filepath, 'rb') as model_file:
        model = pickle.load(model_file)
        st.title('Sentiment Analysis Model')
        review = st.text_input('Enter your review:')
        submit = st.button('Predict')
        if submit:
            prediction = model.predict([review])
        if prediction[0] == 'positive':
            st.success('Positive Review')
        else:
            st.warning('Negative Review')
        print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_filepath}.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
