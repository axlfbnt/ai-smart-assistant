# llm_handler.py

import json
import requests
import streamlit as st
from config import AVAILABLE_MODELS, DEFAULT_MODEL_NAME, APP_VERSION
from utils import get_current_time


def build_headers():
    return {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "HTTP-Referer": st.session_state.get("http_referer", "http://localhost:8501"),
        "X-Title": f"Ai Chatbot ({st.session_state.get('app_version', APP_VERSION)})"
    }


def get_response_stream(messages, model_id):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model_id,
        "messages": messages,
        "stream": True,
        "temperature": 0.7  # fixed default
    }

    try:
        response = requests.post(url, headers=build_headers(), json=payload, stream=True, timeout=180)
        response.raise_for_status()
        for line in response.iter_lines():
            if st.session_state.get("stop_generating", False):
                yield "🛑 Generasi dihentikan pengguna."
                break
            if line:
                line = line.decode('utf-8')
                if line.startswith("data: "):
                    json_str = line[len("data: "):]
                    if json_str.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(json_str)
                        delta = data.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        pass
    except requests.exceptions.HTTPError as err:
        detail = getattr(err.response, "text", str(err))[:100]
        yield f"🛑 HTTP error: {err}. Detail: {detail}"
    except Exception as e:
        yield f"🛑 Kesalahan: {str(e)[:100]}"


def prepare_messages(messages, system_prompt):
    msgs = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        msgs.append({"role": msg["role"], "content": msg.get("content_text", "")})
    return msgs


def handle_command(cmd, model_info, chat_messages):
    cmd = cmd.strip().lower()
    if cmd in ["!help", "!bantuan"]:
        return "**Perintah:**\n- `!help`: Bantuan\n- `!info_model`: Info model\n- `!waktu`: Waktu\n- `!summarize_chat`: Ringkasan"
    elif cmd == "!info_model":
        return f"**Model:** {st.session_state.selected_model_name}\n- ID: `{model_info.get('id')}`\n- Max Tokens: {model_info.get('max_tokens')}"
    elif cmd == "!waktu":
        return f"Waktu saat ini (GMT+7): {get_current_time().strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    elif cmd == "!summarize_chat":
        if not chat_messages:
            return "Tidak ada riwayat untuk dirangkum."
        full_text = "\n".join(
            [f"{m['role']}: {m['content_text']}" for m in chat_messages if not str(m.get('content_text','')).startswith("🛑")]
        )
        prompt = [
            {"role": "system", "content": "Summarize this conversation concisely:"},
            {"role": "user", "content": full_text}
        ]
        st.session_state.pending_llm_automation = {
            "messages": prompt,
            "model_id": model_info.get("id", AVAILABLE_MODELS[DEFAULT_MODEL_NAME]["id"]),
            "is_summary_for_current_chat": True
        }
        return None
    return f"Perintah '{cmd}' tidak dikenali. Gunakan `!help` untuk melihat perintah yang tersedia."