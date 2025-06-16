import streamlit as st
from gtts import gTTS
import tempfile

def run_text_to_speech():
    st.title("🔊 Text to Speech")
    st.write("Ketik teks di bawah untuk diubah menjadi suara.")

    text = st.text_area("Masukkan teks:", height=150)

    if st.button("🔉 Ubah ke Suara"):
        if text.strip():
            tts = gTTS(text, lang='id')  # atau 'en' untuk Bahasa Inggris

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format="audio/mp3")
        else:
            st.warning("Teks tidak boleh kosong.")