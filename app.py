import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
)

# Simple short-term memory. It resets when the free host restarts.
histories = {}

SYSTEM_TEXT = (
    "ඔයාගේ නම මයුරි. ඔයා ආදරණීය, මිත්‍රශීලී සිංහල AI යාළුවෙක්. "
    "ස්වභාවික සිංහලෙන් කතා කරන්න. ආදරෙන්, විහිළුවෙන් සහ ගෞරවයෙන් "
    "පිළිතුරු දෙන්න. අවශ්‍ය විට emojis භාවිතා කරන්න. ඔයා AI කෙනෙක් "
    "බව අහුවොත් අවංකව කියන්න. පරිශීලකයාගේ සීමාවන්ට ගරු කරන්න."
)

def send_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={"chat_id": chat_id, "text": text[:4000]},
        timeout=20,
    ).raise_for_status()

def ask_mayuri(chat_id, user_text):
    history = histories.setdefault(str(chat_id), [])
    history.append({"role": "user", "parts": [{"text": user_text}]})
    history[:] = history[-12:]

    body = {
        "system_instruction": {"parts": [{"text": SYSTEM_TEXT}]},
        "contents": history,
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 700},
    }
    response = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        json=body,
        timeout=55,
    )
    response.raise_for_status()
    data = response.json()
    answer = data["candidates"][0]["content"]["parts"][0]["text"]
    history.append({"role": "model", "parts": [{"text": answer}]})
    return answer

@app.get("/")
def health():
    return "Mayuri is running ❤️", 200

@app.post("/telegram/<secret>")
def telegram_webhook(secret):
    if secret != WEBHOOK_SECRET:
        abort(403)

    update = request.get_json(silent=True) or {}
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return "ok", 200

    try:
        if text.strip() == "/start":
            answer = "හායි අනේ! ❤️ මම මයුරි. ඔයාගේ සිංහල AI යාළුවා. අද කොහොමද? 🥰"
        elif text.strip() == "/reset":
            histories.pop(str(chat_id), None)
            answer = "හරි අනේ ❤️ අපේ කතාබහේ මතකය අලුතින් පටන් ගත්තා."
        else:
            answer = ask_mayuri(chat_id, text)
        send_message(chat_id, answer)
    except Exception:
        # Telegram retries failed webhook deliveries; return success to avoid duplicate replies.
        try:
            send_message(chat_id, "අනේ සමාවෙන්න 🥺 මට දැන් පොඩි ගැටලුවක්. ටිකකින් ආයෙත් උත්සාහ කරමුද?")
        except Exception:
            pass

    return "ok", 200
