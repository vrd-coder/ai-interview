import streamlit as st
import openai
import tempfile

# Set OpenAI API key
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
    st.audio(uploaded_file, format="audio/wav")

    with st.spinner("🔍 Transcribing your question..."):
        try:
            # Save to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name

            # Transcribe using Whisper
            with open(tmp_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
            question = transcript["text"]

            st.subheader("📝 Transcribed Question:")
            st.write(question)

        except Exception as e:
            st.error(f"❌ Failed to transcribe audio: {e}")
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
            st.error(f"❌ Failed to generate answer: {e}")
