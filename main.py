import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")  # Бот берёт токен из Render переменной окружения
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь ссылку на видео.")

# Обработка обновлений от Telegram через webhook
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

# Установка webhook и запуск Flask-сервера
if name == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://video-bot-jzdg.onrender.com/{TOKEN}")  # Это твой адрес на Render
    port = int(os.environ.get('PORT', 5000))  # Render передаёт PORT, на котором нужно слушать
    app.run(host='0.0.0.0', port=port)
