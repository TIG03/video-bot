from flask import Flask, request
from pyrogram import Client
import requests
import os

app = Flask(__name__)

TOKEN = "7713277915:AAEFzFI7qvMFGg5ys35Y6K8ApQhJMFblE-Y"
API_ID = 12345678  # заменим позже
API_HASH = "abcdef1234567890abcdef1234567890"  # заменим позже

bot = Client("bot", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    update = request.get_json()
    print("UPDATE:", update)
    
    # Простейшая логика: если прислали сообщение — ответить "Привет"
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        if text.startswith("http"):
            # Здесь можно скачать видео и отправить — пока просто ответим
            requests.get(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                params={"chat_id": chat_id, "text": "Видео получено, сейчас скачаю!"},
            )
    
    return {"ok": True}

if name == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
