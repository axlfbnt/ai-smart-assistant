# app.py

import streamlit as st

# ✅ HARUS paling atas
st.set_page_config(page_title="AI Multi Tool", layout="wide")

st.title("🧠 AI Smart Assistant")

# Dropdown dengan label unik
mode = st.sidebar.selectbox(
    "🧩 Pilih Mode Aplikasi",
    ["💬 Chat Mind", "🎥 Vision Track", "🖼️ Image Lens"]
)

# Jalankan modul sesuai pilihan
if mode == "💬 Chat Mind":
    from chatbot_main import run_chatbot
    run_chatbot()

elif mode == "🎥 Vision Track":
    from object_detection.detect import run_webcam_detection
    run_webcam_detection()

elif mode == "🖼️ Image Lens":
    from image_detection.detect import run_image_detection
    run_image_detection()