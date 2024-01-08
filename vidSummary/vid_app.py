import streamlit as st
import openai

st.title("📹 Video Summarization App")

# Text input for the user to provide details about the video
video_description = st.text_area("Enter details about the video:", height=100)

# Button to generate the video summary
if st.button("Generate Summary"):
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
