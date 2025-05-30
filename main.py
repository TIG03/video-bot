import os
import telebot
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
        "👋 Привет! Отправь ссылку на видео из YouTube Shorts, Instagram или TikTok — я скачаю и пришлю тебе видео.")

@bot.message_handler(func=lambda m: True)
def handle_video_request(message):
    url = message.text.strip()
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Это не похоже на ссылку. Попробуй снова.")
        return

    msg = bot.send_message(message.chat.id, "⏳ Загружаю видео...")

    try:
        response = requests.post("https://co.wuk.sh/api/json", json={
            "url": url,
            "hd": True,
            "isAudioOnly": False
        }, timeout=30)

        result = response.json()
        video_url = result.get("url")

        if video_url:
            bot.send_video(message.chat.id, video=video_url, caption="✅ Готово!")
        else:
            bot.send_message(message.chat.id, "❌ Не удалось получить видео с сервиса.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка загрузки: {str(e)}")

bot.polling()