import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import PyPDF2
import docx2txt
import pandas as pd

# Set title and description
st.title("Datar's Word Cloud App")
st.write("This app allows you to generate a word cloud from your document.")

# Allow user to upload single or multiple files
uploaded_files = st.file_uploader("Upload your file(s)", accept_multiple_files=True)

# Sidebar to adjust word cloud width and height
width = st.sidebar.slider("Width", 100, 1000, 500)
height = st.sidebar.slider("Height", 100, 1000, 500)

# Checkbox to remove stopwords
remove_stopwords = st.sidebar.checkbox("Remove Stopwords")

# Function to generate word cloud
def generate_word_cloud(text, width, height, remove_stopwords):
    if remove_stopwords:
        wordcloud = WordCloud(width=width, height=height, stopwords=STOPWORDS).generate(text)
    else:
        wordcloud = WordCloud(width=width, height=height).generate(text)
    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return plt, wordcloud

# Process and display word cloud for each uploaded file
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        file_label = f"Word Cloud for {uploaded_file.name}"
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page_number in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_number].extract_text()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")

        if text:  # Check if the text is not empty
            fig, word_cloud = generate_word_cloud(text, width, height, remove_stopwords)
            st.subheader(file_label)
            st.pyplot(fig)

            # Display the top 50 words
            word_freq = pd.Series(word_cloud.process_text(text.lower())).value_counts()[:50]
            st.write("Top 50 Words:")
            st.write(list(word_freq.index))

            # Allow user to download the word cloud as JPG or PNG
            def get_image_download_link(img, format, filename):
                buffered = BytesIO()
                img.savefig(buffered, format=format)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                href = f'<a href="data:image/{format};base64,{img_str}" download="{filename}.{format}">Download {filename}.{format.upper()}</a>'
                return href

            st.markdown(get_image_download_link(fig, "jpg", f"wordcloud_{uploaded_file.name}"), unsafe_allow_html=True)
            st.markdown(get_image_download_link(fig, "png", f"wordcloud_{uploaded_file.name}"), unsafe_allow_html=True)
        else:
            st.write(f"The text in {uploaded_file.name} is empty. Unable to generate a word cloud.")