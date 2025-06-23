import streamlit as st
import openai
import os

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.title("🎤 AI Interview Assistant")
st.markdown("""
Upload a short **WAV audio** of the interviewer asking a question.  
The AI will **transcribe it** and **suggest a professional answer**.
""")

uploaded_file = st.file_uploader("🎙️ Upload WAV file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    with st.spinner("🔍 Transcribing your question..."):
        # Save uploaded file temporarily
        with open("temp.wav", "wb") as f:
            f.write(uploaded_file.read())

        # Transcribe with OpenAI Whisper
        audio_file = open("temp.wav", "rb")
        try:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            question = transcript["text"]
            st.subheader("📝 Transcribed Question:")
            st.write(question)
        except Exception as e:
            st.error("❌ Failed to transcribe audio.")
            st.stop()

    with st.spinner("🤖 Generating interview answer..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional interview coach. Help job seekers answer interview questions effectively."},
                    {"role": "user", "content": f"How should I answer this interview question: '{question}'?"}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            st.subheader("✅ Suggested Answer:")
            st.write(answer)
        except Exception as e:
            st.error("❌ Failed to generate answer from AI.")
