import os
import yt_dlp
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("📥 TikTok"), KeyboardButton("📥 Instagram"))
keyboard.add(KeyboardButton("▶️ YouTube"), KeyboardButton("🎵 Musiqa"))
keyboard.add(KeyboardButton("🎬 Kino"), KeyboardButton("🌤 Ob-havo"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Super Media Bot", reply_markup=keyboard)

# TikTok
@dp.message_handler(lambda m: m.text == "📥 TikTok")
async def tiktok(message: types.Message):
    await message.answer("TikTok link yuboring")

@dp.message_handler(lambda m: "tiktok.com" in m.text)
async def tiktok_download(message: types.Message):
    url = message.text
    ydl_opts = {"outtmpl": "tiktok.mp4"}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("tiktok.mp4", "rb")
    await message.answer_video(video)

# Instagram
@dp.message_handler(lambda m: m.text == "📥 Instagram")
async def insta(message: types.Message):
    await message.answer("Instagram link yuboring")

@dp.message_handler(lambda m: "instagram.com" in m.text)
async def insta_download(message: types.Message):
    url = message.text
    ydl_opts = {"outtmpl": "insta.mp4"}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("insta.mp4", "rb")
    await message.answer_video(video)

# YouTube
@dp.message_handler(lambda m: m.text == "▶️ YouTube")
async def youtube(message: types.Message):
    await message.answer("YouTube link yuboring")

@dp.message_handler(lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
async def yt_download(message: types.Message):
    url = message.text
    ydl_opts = {"outtmpl": "youtube.mp4"}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("youtube.mp4", "rb")
    await message.answer_video(video)

# Musiqa
@dp.message_handler(lambda m: m.text == "🎵 Musiqa")
async def music(message: types.Message):
    await message.answer("Musiqa nomini yozing")

@dp.message_handler(lambda m: not m.text.startswith("http"))
async def search_music(message: types.Message):
    query = message.text

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.mp3'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{query}"])

    audio = open("music.mp3", "rb")
    await message.answer_audio(audio)

# Kino
@dp.message_handler(lambda m: m.text == "🎬 Kino")
async def kino(message: types.Message):
    await message.answer("Kino nomini yozing")

# Ob-havo
@dp.message_handler(lambda m: m.text == "🌤 Ob-havo")
async def weather(message: types.Message):
    await message.answer("Shahar nomini yozing")

executor.start_polling(dp)
