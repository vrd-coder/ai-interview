import streamlit as st
import openai
import speech_recognition as sr
import tempfile
import os

# Set up page
st.set_page_config(page_title="🎤 AI Interview Assistant", layout="centered")
st.title("🎤 AI Interview Assistant")

# Use secret for API key (set in Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.markdown("""
Upload a short **WAV audio** of the interviewer asking a question.

The AI will transcribe it and suggest a professional answer.
""")

# Upload the audio file
audio_file = st.file_uploader("🎙️ Upload WAV file", type=["wav"])

if audio_file:
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_path = temp_file.name

    # Use SpeechRecognition to transcribe
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_path) as source:
        audio_data = recognizer.record(source)

    try:
        # Transcribe the question
        question = recognizer.recognize_google(audio_data)
        st.success(f"Transcribed: {question}")

        # Send to GPT-4
        with st.spinner("Generating answer..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant helping a job candidate."},
                    {"role": "user", "content": f"In a job interview, the interviewer asks: '{question}'. Suggest a smart, confident answer."}
                ],
                temperature=0.6
            )
            answer = response["choices"][0]["message"]["content"]

        st.markdown("### ✅ Suggested Answer:")
        st.write(answer)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

    finally:
        os.remove(temp_path)
