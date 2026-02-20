import telebot
import yt_dlp
import os

bot = telebot.TeleBot("7805387290:AAGqe_zlHN-ee1EWk5UHhmfsVbS5k60wPE0")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello, welcome to the music download bot, send me the link and I will convert it to mp3."
    )

@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def download_audio(message):
    url = message.text
    bot.send_message(message.chat.id, "please wait, audio is loading...")
    
    # Sozlamalar
    ydl_opts = {
        "extract_flat": "in_playlist",
        "noplaylist": True,
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Faylni yuborish
        with open("audio.mp3", "rb") as audio_file:
            bot.send_audio(message.chat.id, audio_file)
        
        # Faylni o'chirish
        os.remove("audio.mp3")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred! {e}")
        print(f"error: {e}")

bot.infinity_polling()
