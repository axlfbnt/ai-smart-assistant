# chatbot_main.py

def run_chatbot():
    import streamlit as st
    import os
    from config import AVAILABLE_MODELS
    from state import init_session_state
    from chat_manager import create_chat, reset_chats, get_chat_messages, add_message_to_chat, switch_chat
    from llm_handler import prepare_messages, get_response_stream, handle_command
    from utils import play_notification_sound, format_time_display, extract_text_from_file
    from storage import save_all_chats, load_all_chats
    from components.file_uploader_display import init_uploader_state, render_file_uploader, reset_uploader

    init_session_state()
    init_uploader_state()
    load_all_chats()

    if not st.session_state.all_chats:
        create_chat("Chat Awal")

    if not st.session_state.current_chat_id:
        st.session_state.current_chat_id = next(iter(st.session_state.all_chats))

    chat_title = "Chatbot"
    if st.session_state.current_chat_id:
        chat_data = st.session_state.all_chats.get(st.session_state.current_chat_id, {})
        chat_title = chat_data.get("title", chat_title)

    st.title("🤖 AI Chatbot Streamlit")

    with st.sidebar:
        st.header("💬 Navigasi Chat")
        if st.button("+ Chat Baru"):
            create_chat()
            save_all_chats()
            st.rerun()

        if st.button("🗑️ Hapus Semua Chat"):
            reset_chats()
            save_all_chats()
            st.rerun()

        st.markdown("---")
        rename_chat_id = st.session_state.get("rename_chat_id")

        for chat_id, chat in list(st.session_state.all_chats.items())[::-1]:
            is_active = chat_id == st.session_state.current_chat_id
            row = st.columns([0.6, 0.2, 0.2])
            with row[0]:
                if rename_chat_id == chat_id:
                    new_title = st.text_input("", value=chat["title"], key=f"input_{chat_id}", label_visibility="collapsed")
                else:
                    if st.button(chat['title'], key=f"switch_{chat_id}", use_container_width=True):
                        switch_chat(chat_id)
                        st.rerun()
            with row[1]:
                if rename_chat_id == chat_id:
                    if st.button("📏", key=f"save_{chat_id}"):
                        new_val = st.session_state.get(f"input_{chat_id}", "").strip()
                        if new_val:
                            st.session_state.all_chats[chat_id]["title"] = new_val
                            st.session_state.all_chats[chat_id]["title_is_fixed"] = True
                            st.session_state.rename_chat_id = None
                            save_all_chats()
                            st.rerun()
                else:
                    if st.button("✏️", key=f"rename_{chat_id}"):
                        st.session_state.rename_chat_id = chat_id
                        st.rerun()
            with row[2]:
                if st.button("🗑️", key=f"delete_{chat_id}", help="Hapus", use_container_width=True):
                    del st.session_state.all_chats[chat_id]
                    if st.session_state.current_chat_id == chat_id:
                        st.session_state.current_chat_id = None
                    st.session_state.rename_chat_id = None
                    save_all_chats()
                    st.rerun()

        st.markdown("---")
        st.subheader("Pengaturan")
        model_names = list(AVAILABLE_MODELS.keys())
        st.session_state.selected_model_name = st.selectbox("Model AI", model_names, index=model_names.index(st.session_state.selected_model_name))

    chat_messages = get_chat_messages()
    if not chat_messages:
        st.markdown("### 💬 Mulai percakapan baru...")
    for msg in chat_messages:
        with st.chat_message(msg['role'], avatar="👤" if msg['role'] == "user" else "🤖"):
            st.markdown(msg['content_text'])
            st.caption(format_time_display(msg['timestamp']))

    uploaded_file = render_file_uploader()
    user_prompt = st.chat_input("Ketik pesan...")

    if user_prompt and not st.session_state.generating:
        st.session_state.generating = True
        model_info = AVAILABLE_MODELS[st.session_state.selected_model_name]

        extracted_text = ""
        filename_note = ""

        if uploaded_file:
            extracted_text = extract_text_from_file(uploaded_file)
            filename_note = f"(berkas: `{uploaded_file.name}`)"
            if not extracted_text.strip():
                add_message_to_chat("user", user_prompt)
                add_message_to_chat("assistant", "⚠️ File tidak berisi teks yang dapat dibaca.")
                st.session_state.generating = False
                reset_uploader()
                st.rerun()

        full_prompt = f"{user_prompt}\n\n---\n\U0001F4C4 File terlampir: `{uploaded_file.name}`" if uploaded_file else user_prompt

        if user_prompt.startswith("!"):
            response = handle_command(user_prompt, model_info, chat_messages)
            add_message_to_chat("user", user_prompt)
            if response:
                add_message_to_chat("assistant", response)
            save_all_chats()
            st.session_state.generating = False
            reset_uploader()
            st.rerun()
        else:
            add_message_to_chat("user", full_prompt)
            prompt_messages = prepare_messages(
                get_chat_messages(),
                st.session_state.get("system_prompt", "Halo, saya siap membantu.")
            )
            if extracted_text:
                prompt_messages.append({"role": "user", "content": extracted_text})

            with st.chat_message("assistant", avatar="🤖"):
                placeholder = st.empty()
                full_response = ""
                for chunk in get_response_stream(prompt_messages, model_info['id']):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                add_message_to_chat("assistant", full_response)
                st.session_state.play_sound_once = True
                save_all_chats()

            st.session_state.generating = False
            if st.session_state.play_sound_once:
                play_notification_sound()
            reset_uploader()
            st.rerun()