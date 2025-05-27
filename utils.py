# utils.py

import datetime
import pytz
import re
import streamlit as st
import base64
import os
from config import TARGET_TZ, SOUND_NOTIFICATION_FILE

# Regex patterns
TXT_PATTERN_FULL_TS = re.compile(r"\[(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]\s*(User|Assistant|System|Bot):\s*([\s\S]*)", re.IGNORECASE)
TXT_PATTERN_TIME_ONLY_TS = re.compile(r"\[(\d{2}:\d{2}:\d{2})\]\s*(User|Assistant|System|Bot):\s*([\s\S]*)", re.IGNORECASE)

# Timestamp helpers
def get_current_time():
    return datetime.datetime.now(TARGET_TZ)

def convert_to_local(dt_obj):
    if not isinstance(dt_obj, datetime.datetime):
        try:
            dt_obj = datetime.datetime.fromisoformat(str(dt_obj).replace("Z", "+00:00"))
        except ValueError:
            try:
                dt_obj = datetime.datetime.strptime(str(dt_obj), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return get_current_time()
    if dt_obj.tzinfo is None:
        return TARGET_TZ.localize(dt_obj)
    return dt_obj.astimezone(TARGET_TZ)

def format_time_display(ts):
    return convert_to_local(ts).strftime("%H:%M:%S") if isinstance(ts, datetime.datetime) else str(ts)

def format_time_export(ts):
    return convert_to_local(ts).strftime("%Y-%m-%d %H:%M:%S %Z%z") if isinstance(ts, datetime.datetime) else str(ts)

# Chat title auto-update
def update_chat_title(chat_id, prompt):
    if not chat_id in st.session_state.all_chats:
        return
    chat = st.session_state.all_chats[chat_id]
    if chat.get("title_is_fixed"):
        return
    cleaned = prompt.strip()
    if cleaned.startswith("!"):
        return

    words = cleaned.split()
    if len(words) < 2:
        if any(chat['title'].startswith(p) for p in ["Chat Baru", "Upload:", "Chat Awal", "Diskusi"]):
            chat['title'] = f"Diskusi ({chat['created_at'].astimezone(TARGET_TZ).strftime('%H:%M')})"
        return

    title = " ".join(words[:5]) + ("..." if len(words) > 5 else "")
    chat['title'] = title

# Notification sound
def play_notification_sound(sound_path=SOUND_NOTIFICATION_FILE):
    if not st.session_state.get("play_sound_once", False):
        return
    st.session_state.play_sound_once = False

    if os.path.exists(sound_path):
        try:
            with open(sound_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                mime = "audio/mp3"
                if sound_path.lower().endswith(".wav"):
                    mime = "audio/wav"
                elif sound_path.lower().endswith(".ogg"):
                    mime = "audio/ogg"

                html = f"""
                    <audio autoplay>
                        <source src="data:{mime};base64,{b64}" type="{mime}">
                        Browser Anda tidak mendukung elemen audio.
                    </audio>
                    <script>
                        var audio = document.querySelector("audio");
                        if (audio) {{ audio.play().catch(err => console.log("Autoplay dicegah:", err)); }}
                    </script>
                """
                st.components.v1.html(html, height=0, width=0)
        except Exception as e:
            st.warning(f"Gagal memutar suara notifikasi: {e}", icon="🔊")
    else:
        st.warning(f"File suara tidak ditemukan: {sound_path}", icon="🔊")

# File content extraction
def extract_text_from_file(file):
    import io
    import pandas as pd

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        import pdfplumber
        try:
            with pdfplumber.open(file) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                return text.strip()
        except Exception:
            return "PDF tidak dapat dibaca."

    elif file_name.endswith(".docx"):
        try:
            from docx import Document
            document = Document(file)
            return "\n".join([para.text for para in document.paragraphs]).strip()
        except Exception:
            return "DOCX tidak dapat dibaca."

    elif file_name.endswith(".csv"):
        try:
            df = pd.read_csv(file)
            return df.to_string(index=False)
        except Exception:
            return "CSV tidak dapat dibaca."

    elif file_name.endswith(".xlsx"):
        try:
            df = pd.read_excel(file)
            return df.to_string(index=False)
        except Exception:
            return "XLSX tidak dapat dibaca."

    elif file_name.endswith(".txt"):
        try:
            return file.read().decode("utf-8").strip()
        except Exception:
            return "TXT tidak dapat dibaca."

    return "Format file tidak dikenali."