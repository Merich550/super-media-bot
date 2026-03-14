import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("8705691968:AAE24pVc2UOeBDvl2sXsz639xTwhxeWRypU")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("📥 TikTok"), KeyboardButton("📥 Instagram"))
keyboard.add(KeyboardButton("🎵 Musiqa"), KeyboardButton("🔎 Kino qidirish"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = """Super Media Bot

🎬 Kino qidirish
🎵 Musiqa topish
📥 TikTok / Instagram yuklash
"""
    await message.answer(text, reply_markup=keyboard)

# TikTok tugma
@dp.message_handler(lambda message: message.text == "📥 TikTok")
async def tiktok(message: types.Message):
    await message.answer("TikTok link yuboring")

# TikTok video yuklash
@dp.message_handler(lambda message: "tiktok.com" in message.text)
async def download_tiktok(message: types.Message):
    url = message.text

    ydl_opts = {
        "format": "mp4",
        "outtmpl": "video.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open("video.mp4", "rb") as video:
        await message.answer_video(video)

# Instagram
@dp.message_handler(lambda message: message.text == "📥 Instagram")
async def instagram(message: types.Message):
    await message.answer("Instagram link yuboring")

# Musiqa
@dp.message_handler(lambda message: message.text == "🎵 Musiqa")
async def music(message: types.Message):
    await message.answer("Musiqa nomini yozing")

# Kino
@dp.message_handler(lambda message: message.text == "🔎 Kino qidirish")
async def kino(message: types.Message):
    await message.answer("Qaysi kinoni qidiryapsiz?")

executor.start_polling(dp)
