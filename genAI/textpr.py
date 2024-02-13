# Import necessary libraries
import streamlit as st
from langchain.llms import GooglePalm

# Initialize GooglePalm
api_key = "AIzaSyDj-QAjpa9hHlTV7iBCN45Z5mwXWTk7y3Y"
llm = GooglePalm(google_api_key=api_key, temperature=0.7)

# Streamlit app
def main():
    st.title("GooglePalm Text Generation App")
    
    # User input for prompt
    user_input = st.text_area("Enter a text prompt:", height=100)
    
    # Temperature control slider
    temperature = st.slider("Temperature (Controls randomness):", min_value=0.1, max_value=1.0, value=0.7, step=0.1)

    # Generate text using GooglePalm
    if st.button("Generate Text"):
        if user_input:
            generated_text = llm(user_input, temperature=temperature)
            st.success("Generated Text:")
            st.write(generated_text)
        else:
            st.warning("Please enter a text prompt.")

# Run the app
if __name__ == "__main__":
    main()
