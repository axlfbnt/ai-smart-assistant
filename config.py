# config.py

import pytz

APP_VERSION = "Chatbot AI"
DEFAULT_MODEL_NAME = "DeepSeek Chat V3 0324 (free)"
DEFAULT_SYSTEM_PROMPT = "Anda adalah asisten AI yang siap membantu dengan jawaban jelas dan ringkas."

# Timezone configuration
TARGET_TIMEZONE_STR = "Asia/Bangkok"
TARGET_TZ = pytz.timezone(TARGET_TIMEZONE_STR)

# Audio notification
SOUND_NOTIFICATION_FILE = "assets/notification.mp3"

# Available models
AVAILABLE_MODELS = {
    "DeepSeek Chat V3 0324 (free)": {
        "id": "deepseek/deepseek-chat-v3-0324:free",
        "vision": False,
        "max_tokens": 163840,
        "free": True,
    },
    "Meta Llama 3 8B Instruct": {
        "id": "meta-llama/llama-3-8b-instruct",
        "vision": False,
        "max_tokens": 8192,
        "free": True,
    },
    "Mistral 7B Instruct": {
        "id": "mistralai/mistral-7b-instruct:free",
        "vision": False,
        "max_tokens": 8192,
        "free": True,
    },
    "Claude 3 Haiku": {
        "id": "anthropic/claude-3-haiku:beta",
        "vision": False,
        "max_tokens": 200000,
        "free": True,
    },
    "GPT-3.5 Turbo": {
        "id": "openai/gpt-3.5-turbo",
        "vision": False,
        "max_tokens": 4096,
        "free": False,
    },
}