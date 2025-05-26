# chat_manager.py

import datetime
import streamlit as st
from config import TARGET_TZ
from utils import get_current_time, update_chat_title

def generate_chat_id():
    return f"chat_{get_current_time().strftime('%Y%m%d_%H%M%S_%f')}"

def create_chat(title_prefix="Chat Baru", initial_messages=None, switch_to=True, pinned=False, fixed_title=False, uploaded_filename=None):
    chat_id = generate_chat_id()
    timestamp = get_current_time()

    if uploaded_filename:
        base_name = uploaded_filename.rsplit('.', 1)[0] if '.' in uploaded_filename else uploaded_filename
        title = f"Upload: {base_name[:25]}"
        fixed_title = True
    else:
        title = f"{title_prefix} ({timestamp.strftime('%H:%M:%S')})"

    if initial_messages is None:
        initial_messages = [{
            "role": "assistant",
            "content_text": f"Sesi '{title}' dimulai. Siap membantu!",
            "timestamp": timestamp,
            "feedback": None
        }]
    else:
        for msg in initial_messages:
            if msg.get("role") == "assistant" and "feedback" not in msg:
                msg["feedback"] = None

    st.session_state.all_chats[chat_id] = {
        "title": title,
        "created_at": timestamp,
        "messages": initial_messages,
        "is_pinned": pinned,
        "title_is_fixed": fixed_title,
        "pinned_at": timestamp if pinned else None
    }

    if switch_to:
        st.session_state.current_chat_id = chat_id

    if initial_messages and not fixed_title and not uploaded_filename:
        first_user_msg = next((msg for msg in initial_messages if msg["role"] == "user"), None)
        if first_user_msg:
            update_chat_title(chat_id, first_user_msg["content_text"])

    return chat_id

def switch_chat(chat_id):
    if chat_id in st.session_state.all_chats:
        st.session_state.current_chat_id = chat_id
    else:
        st.error("Chat ID tidak ditemukan.")
        if st.session_state.all_chats:
            recent_chat = max(
                st.session_state.all_chats.items(),
                key=lambda x: (x[1].get("is_pinned", False), x[1].get("pinned_at") or x[1]["created_at"])
            )
            st.session_state.current_chat_id = recent_chat[0]
        else:
            create_chat("Chat Awal")

def reset_chats():
    st.session_state.all_chats = {}
    st.session_state.current_chat_id = None
    st.session_state.renaming_chat_id = None
    st.session_state.active_chat_search_query = ""
    create_chat("Chat Awal Baru")
    st.toast("Semua riwayat chat telah dihapus!", icon="🗑️")

def get_chat_messages():
    chat_id = st.session_state.current_chat_id
    if chat_id and chat_id in st.session_state.all_chats:
        return st.session_state.all_chats[chat_id]["messages"]
    return []

def add_message_to_chat(role, content_text, timestamp=None, feedback=None):
    chat_id = st.session_state.current_chat_id
    if not chat_id or chat_id not in st.session_state.all_chats:
        return
    msg_time = timestamp or get_current_time()
    msg_data = {"role": role, "content_text": content_text, "timestamp": msg_time}
    if role == "assistant":
        msg_data["feedback"] = feedback

    st.session_state.all_chats[chat_id]["messages"].append(msg_data)

    if role == "user":
        update_chat_title(chat_id, content_text)