import os
import yt_dlp
import requests
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8705691968:AAE24pVc2UOeBDvl2sXsz639xTwhxeWRypU"
openai.api_key = "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"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    KeyboardButton("📥 TikTok"),
    KeyboardButton("📥 Instagram")
)
keyboard.add(
    KeyboardButton("🎵 Musiqa"),
    KeyboardButton("🔎 Kino qidirish")
)
keyboard.add(
    KeyboardButton("🤖 AI Chat")
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "🚀 SUPER MEDIA BOT\n\nTanlang:",
        reply_markup=keyboard
    )

# TikTok
@dp.message_handler(lambda m: m.text == "📥 TikTok")
async def tiktok(message: types.Message):
    await message.answer("📥 TikTok link yuboring")

@dp.message_handler(lambda m: "tiktok.com" in m.text)
async def download_tiktok(message: types.Message):
    url = message.text

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'mp4'
    }

    await message.answer("⏳ Video yuklanmoqda...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await message.answer_video(open("video.mp4", "rb"))

# Instagram
@dp.message_handler(lambda m: m.text == "📥 Instagram")
async def insta(message: types.Message):
    await message.answer("📥 Instagram link yuboring")

@dp.message_handler(lambda m: "instagram.com" in m.text)
async def insta_download(message: types.Message):

    url = message.text

    ydl_opts = {
        'outtmpl': 'insta.mp4'
    }

    await message.answer("⏳ Video yuklanmoqda...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await message.answer_video(open("insta.mp4", "rb"))

# Musiqa
@dp.message_handler(lambda m: m.text == "🎵 Musiqa")
async def music(message: types.Message):
    await message.answer("🎵 Musiqa nomini yozing")

@dp.message_handler()
async def music_download(message: types.Message):

    if message.text.startswith("🎵"):
        return

    query = message.text

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'music.%(ext)s'
    }

    await message.answer("⏳ Musiqa yuklanmoqda...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]

    await message.answer_audio(open("music.webm", "rb"))

# Kino
@dp.message_handler(lambda m: m.text == "🔎 Kino qidirish")
async def kino(message: types.Message):
    q = message.text
    link = f"https://www.youtube.com/results?search_query={q}+kino"
    await message.answer("🎬 Kino topildi:\n"+link)

# AI
@dp.message_handler(lambda m: m.text == "🤖 AI Chat")
async def ai(message: types.Message):
    await message.answer("Savol yozing")

@dp.message_handler()
async def ai_chat(message: types.Message):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":message.text}]
    )

    await message.answer(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    executor.start_polling(dp)
