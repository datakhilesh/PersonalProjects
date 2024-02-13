# Import necessary libraries
import streamlit as st
from langchain.llms import GooglePalm
from langchain.document_loaders.csv_loader import CSVLoader
from sentence_transformers import SentenceTransformer
from InstructorEmbedding import INSTRUCTOR

# Load data from CSV
loader = CSVLoader(file_path='codebasics_faqs.csv', source_column='prompt', encoding='latin1')
data = loader.load()

# Initialize GooglePalm
api_key = "AIzaSyDj-QAjpa9hHlTV7iBCN45Z5mwXWTk7y3Y"
llm = GooglePalm(google_api_key=api_key, temperature=0.7)

# Initialize InstructorEmbedding
model = INSTRUCTOR('hkunlp/instructor-large')

# Streamlit app
def main():
    st.title("Text Generation and Embedding App")
    
    # User input for haiku generation
    user_input = st.text_input("Enter a prompt for haiku generation:")
    
    # Generate haiku using GooglePalm
    if st.button("Generate Haiku"):
        if user_input:
            haiku = llm(user_input)
            st.success("Generated Haiku:")
            st.write(haiku)
        else:
            st.warning("Please enter a prompt.")

    # User input for sentence embedding
    sentence_input = st.text_input("Enter a sentence for embedding:")
    
    # Embed sentence using InstructorEmbedding
    if st.button("Embed Sentence"):
        if sentence_input:
            embeddings = model.encode([[sentence_input]])
            st.success("Sentence Embedding:")
            st.write(embeddings)
        else:
            st.warning("Please enter a sentence.")

# Run the app
if __name__ == "__main__":
    main()
