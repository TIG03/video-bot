import os
from dotenv import load_dotenv
from flask import Flask, request
import telebot
import requests

# Загрузка токена из .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Flask приложение
app = Flask(__name__)

# Проверка сервера
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

# Вебхук от Telegram
@app.route(f"/{API_TOKEN}", methods=["POST"])
def getMessage():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

# Обработка входящих сообщений
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    if any(domain in url for domain in ["tiktok.com", "instagram.com", "youtube.com", "youtu.be"]):
        bot.send_message(message.chat.id, "⏳ Обрабатываю ссылку...")
        try:
            api_url = f"https://api.dl-x.com/dl?url={url}"
            response = requests.get(api_url).json()
            if "url" in response:
                bot.send_video(message.chat.id, response["url"])
            else:
                bot.send_message(message.chat.id, "❌ Видео не найдено. Попробуйте другую ссылку.")
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Ошибка: {e}")
    else:
        bot.send_message(message.chat.id, "❌ Отправь ссылку на TikTok / Instagram / Shorts")

# Запуск сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
