import streamlit as st
from gtts import gTTS
import os
import tempfile

def run_text_to_speech():
    st.markdown("Masukkan teks di bawah ini untuk diubah menjadi suara.")

    text = st.text_area("Teks:", placeholder="Ketik sesuatu untuk dibacakan...")

    if st.button("🔈 Convert & Play"):
        if not text.strip():
            st.warning("Mohon masukkan teks terlebih dahulu.")
            return

        tts = gTTS(text, lang="id")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")
            
            with open(fp.name, "rb") as f:
                audio_data = f.read()
                st.download_button(
                    label="Download MP3",
                    data=audio_data,
                    file_name="text_to_speech.mp3",
                    mime="audio/mp3"
                )
