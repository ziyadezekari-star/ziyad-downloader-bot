import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

TOKEN = "8539570428:AAHvPp2gpkezhp-bv_xBHVrfNjrBRU7JtRA"
bot = telebot.TeleBot(TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Live"

def run_web(): app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(message): bot.reply_to(message, "🎬 أهلاً بك! أرسل الرابط للتحميل.")

@bot.message_handler(func=lambda message: "http" in message.text)
def download(message):
    url = message.text
    bot.reply_to(message, "⏳ جاري التحميل...")
    file_name = f"v_{message.chat.id}.mp4"
    try:
        with yt_dlp.YoutubeDL({'format':'best','outtmpl':file_name}) as ydl: ydl.download([url])
        with open(file_name, 'rb') as f: bot.send_video(message.chat.id, f)
        os.remove(file_name)
    except Exception as e: bot.reply_to(message, f"❌ خطأ: {e}")

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.polling(none_stop=True)

