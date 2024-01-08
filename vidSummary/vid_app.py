import streamlit as st
from transformers import BartForConditionalGeneration, BartTokenizer
from youtube_transcript_api import YouTubeTranscriptApi

st.title("📹 YouTube Video Summarization App")

# Text input for the user to provide the YouTube link
youtube_link = st.text_input("Enter the YouTube video link:")

# Button to fetch transcript and generate the video summary
if st.button("Generate Summary"):
    try:
        # Fetch video transcript using YouTubeTranscriptApi
        video_id = youtube_link.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Extract text from transcript
        video_description = " ".join([entry["text"] for entry in transcript])

        # Using BART model for summarization
        model_name = "facebook/bart-large-cnn"
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)

        # Tokenize and generate summary
        inputs = tokenizer(video_description, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs["input_ids"], max_length=150, num_beams=4, length_penalty=2.0)

        # Decode summary and display
        video_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        st.subheader("Generated Video Summary:")
        st.write(video_summary)

    except Exception as e:
        st.error(f"Error: {e}")
