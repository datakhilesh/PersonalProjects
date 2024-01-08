import streamlit as st
import openai
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

        # Using GPT-3.5-turbo from OpenAI Playground API
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use "gpt-3.5-turbo" as well
            prompt=f"Summarize the following video: {video_description}",
            temperature=0.5,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # Display the generated summary
        video_summary = response.choices[0].text.strip()
        st.subheader("Generated Video Summary:")
        st.write(video_summary)

    except Exception as e:
        st.error(f"Error: {e}")
