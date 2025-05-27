# 🧠 AI Smart Assistant

A multi-feature Streamlit app combining Chatbot, Object Detection, and Image Detection — powered by LLMs (via OpenRouter) and HuggingFace Transformers.

---

## ✨ Features

### 💬 Chat Mind (AI Chatbot)
- Multiple OpenRouter-compatible models (LLaMA, DeepSeek, etc.)
- Chat history persistence (local JSON)
- Rename & delete chat sessions
- Notification sound support
- ✅ **Attach & analyze files** (.txt, .pdf, .docx, .xlsx)
- ✅ **Auto-clear file uploader after chat**
- ✅ **Validates file content (warns if unreadable like scanned PDFs)**

### 👁️ Vision Track (Webcam Object Detection)
- Uses `facebook/detr-resnet-50` from HuggingFace
- Real-time detection with bounding boxes
- Adjustable confidence, resolution, and FPS skip
- (💡 Note: may not be supported on Streamlit Cloud)

### 🖼️ Image Lens (Image Upload Detection)
- Upload `.jpg/.png` images
- Visualize object detection bounding boxes
- Powered by the same DETR model

---

## 🗂️ Project Structure

```
.
├── app.py                            # Main entry file with mode selector
├── chatbot_main.py                   # Chatbot logic and UI
├── components/
│   └── file_uploader_display.py      # Enhanced file uploader state control
├── object_detection/
│   └── detect.py                     # Real-time webcam detection
├── image_detection/
│   └── detect.py                     # Image upload detection
├── chat_manager.py                   # Chat session management
├── llm_handler.py                    # API calls to OpenRouter
├── config.py                         # Settings and model config
├── storage.py                        # JSON file save/load
├── utils.py                          # Helper functions + file content extractor
├── state.py                          # Streamlit session state init
├── chat_history.json                 # Local chat history data
├── .streamlit/
│   └── secrets.toml                  # (DO NOT COMMIT) OpenRouter API key
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started (Local)

### 1. Clone this repo
```bash
git clone https://github.com/axlfbnt/ai-smart-assistant.git
cd ai-smart-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your OpenRouter API key
Create `.streamlit/secrets.toml` with:
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deployment on Streamlit Cloud

1. Push your code to a public GitHub repo
2. Go to https://streamlit.io/cloud → New App
3. Set `app.py` as main entry point
4. Add `OPENROUTER_API_KEY` in the **Secrets** section on Streamlit Cloud

---

## 📦 Requirements

Make sure this is in your `requirements.txt`:

```txt
streamlit
requests
pytz
watchdog
torch
transformers
timm
opencv-python
Pillow
numpy
pandas
python-docx
pdfplumber
openpyxl
```

---

## 📸 Example Use

- Switch between modes from sidebar
- In **Chatbot**, type messages and attach documents to ask questions about them
- In **Vision Track**, detect objects live via webcam
- In **Image Lens**, upload an image and auto-detect objects

---

## 🛠️ Powered By

- [OpenRouter.ai](https://openrouter.ai/)
- [Hugging Face Transformers](https://huggingface.co/facebook/detr-resnet-50)
- [Streamlit](https://streamlit.io/)
- [pdfplumber / docx / openpyxl / pandas] for file parsing

---

## ⚠️ Notes

- Webcam features may not work on Streamlit Cloud due to browser security
- `chat_history.json` stores chat state locally
- Never commit `.streamlit/secrets.toml` to public repos
- File attachments are cleared after chat is sent

---

## 📃 License

MIT License — free to use & modify.