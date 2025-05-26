# storage.py

import os
import json
import datetime
import streamlit as st
from config import TARGET_TZ
from utils import get_current_time

CHAT_FILE = "chat_history.json"

def save_all_chats():
    try:
        serializable_data = {}
        for chat_id, chat in st.session_state.all_chats.items():
            serializable_data[chat_id] = {
                "title": chat["title"],
                "title_is_fixed": chat.get("title_is_fixed", False),
                "is_pinned": chat.get("is_pinned", False),
                "pinned_at": chat.get("pinned_at").isoformat() if chat.get("pinned_at") else None,
                "created_at": chat["created_at"].isoformat(),
                "messages": [
                    {
                        "role": msg["role"],
                        "content_text": msg["content_text"],
                        "timestamp": msg["timestamp"].isoformat(),
                        "feedback": msg.get("feedback")
                    }
                    for msg in chat.get("messages", [])
                ]
            }

        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.warning(f"Gagal menyimpan chat: {e}")

def load_all_chats():
    if not os.path.exists(CHAT_FILE):
        return

    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        st.session_state.all_chats = {}
        for chat_id, chat in raw_data.items():
            created_at = parse_ts(chat.get("created_at"))
            pinned_at = parse_ts(chat.get("pinned_at")) if chat.get("is_pinned") else None

            st.session_state.all_chats[chat_id] = {
                "title": chat["title"],
                "title_is_fixed": chat.get("title_is_fixed", False),
                "is_pinned": chat.get("is_pinned", False),
                "pinned_at": pinned_at,
                "created_at": created_at,
                "messages": [
                    {
                        "role": msg["role"],
                        "content_text": msg["content_text"],
                        "timestamp": parse_ts(msg.get("timestamp")),
                        "feedback": msg.get("feedback")
                    }
                    for msg in chat.get("messages", [])
                ]
            }
    except Exception as e:
        st.error(f"Gagal memuat riwayat chat: {e}")

def parse_ts(ts):
    if not ts:
        return get_current_time()
    try:
        return TARGET_TZ.localize(datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")))
    except Exception:
        return get_current_time()