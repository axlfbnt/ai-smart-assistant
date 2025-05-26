# state.py

import streamlit as st
from config import APP_VERSION, DEFAULT_MODEL_NAME

DEFAULT_SYSTEM_PROMPT = "Anda adalah asisten AI yang siap membantu dengan jawaban jelas dan ringkas."

def init_session_state():
    if "app_version" not in st.session_state:
        st.session_state.app_version = APP_VERSION

    if "all_chats" not in st.session_state:
        st.session_state.all_chats = {}

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None

    if "rename_chat_id" not in st.session_state:
        st.session_state.rename_chat_id = None

    if "selected_model_name" not in st.session_state:
        st.session_state.selected_model_name = DEFAULT_MODEL_NAME

    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

    if "generating" not in st.session_state:
        st.session_state.generating = False

    if "play_sound_once" not in st.session_state:
        st.session_state.play_sound_once = False