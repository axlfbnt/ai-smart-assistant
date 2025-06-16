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

        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")