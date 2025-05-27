# components/file_uploader_display.py
import streamlit as st
import uuid

def init_uploader_state():
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = str(uuid.uuid4())

def reset_uploader():
    st.session_state.uploader_key = str(uuid.uuid4())

def render_file_uploader():
    return st.file_uploader(
        "\U0001F4CE Attach file (txt, pdf, docx, xlsx)",
        type=["txt", "pdf", "docx", "xlsx"],
        key=st.session_state.uploader_key,
        label_visibility="collapsed"
    )