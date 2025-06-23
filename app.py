import streamlit as st
import openai
import speech_recognition as sr
import tempfile
import os

openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.title("🎙️ AI Interview Assistant (Live Speech to Text)")

st.markdown(\"\"\"
This tool listens to the interviewer's voice, transcribes the question, and generates a text-based answer using GPT-4.
\"\"\")

audio_bytes = st.audio(label="🎤 Speak your question", format="audio/wav")

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes.read())
        audio_path = temp_audio.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        question = recognizer.recognize_google(audio_data)
        st.success(f"Transcribed Question: {question}")

        with st.spinner("Generating answer..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"You are in a job interview. The interviewer asks: '{question}'. Respond professionally and concisely."}
                ],
                temperature=0.6
            )
            answer = response["choices"][0]["message"]["content"]

        st.markdown("### ✅ AI's Suggested Answer:")
        st.write(answer)

    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Request Error: {e}")
    finally:
        os.remove(audio_path)
else:
    st.info("Please speak or upload a question to begin.")
