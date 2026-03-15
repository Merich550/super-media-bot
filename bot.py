import logging
import yt_dlp
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from youtubesearchpython import VideosSearch

TOKEN = "8705691968:AAHuPJ78OrUxz8dQ2LPi6Oge7zVg7YDFTUM"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

search_results = {}

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add("📥 TikTok","📥 Instagram")
keyboard.add("▶️ YouTube","🎵 Musiqa")
keyboard.add("🎬 Kino","☀️ Ob-havo")

# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    text = """
🤖 Super Media Bot

📥 TikTok video yuklash
📥 Instagram video yuklash
▶️ YouTube video yuklash
🎵 Musiqa topish
🎬 Kino qidirish
☀️ Ob-havo
"""

    await message.answer(text, reply_markup=keyboard)

# TIKTOK TUGMA
@dp.message_handler(lambda m: m.text == "📥 TikTok")
async def tiktok_btn(message: types.Message):

    await message.answer("TikTok link yuboring")

# INSTAGRAM TUGMA
@dp.message_handler(lambda m: m.text == "📥 Instagram")
async def insta_btn(message: types.Message):

    await message.answer("Instagram link yuboring")

# YOUTUBE TUGMA
@dp.message_handler(lambda m: m.text == "▶️ YouTube")
async def yt_btn(message: types.Message):

    await message.answer("YouTube link yuboring")

# MUSIQA TUGMA
@dp.message_handler(lambda m: m.text == "🎵 Musiqa")
async def music_btn(message: types.Message):

    await message.answer("Musiqa nomini yozing")

# TIKTOK DOWNLOAD
@dp.message_handler(lambda m: m.text and "tiktok.com" in m.text)
async def tiktok_download(message: types.Message):

    url = message.text.strip()

    ydl_opts = {
        'outtmpl': 'tiktok.mp4',
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("tiktok.mp4","rb")
    await message.answer_video(video)

# INSTAGRAM DOWNLOAD
@dp.message_handler(lambda m: m.text and "instagram.com" in m.text)
async def insta_download(message: types.Message):

    url = message.text.strip()

    ydl_opts = {
        'outtmpl': 'insta.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("insta.mp4","rb")
    await message.answer_video(video)

# YOUTUBE DOWNLOAD
@dp.message_handler(lambda m: m.text and ("youtube.com" in m.text or "youtu.be" in m.text))
async def yt_download(message: types.Message):

    url = message.text.strip()

    ydl_opts = {
        'outtmpl': 'youtube.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("youtube.mp4","rb")
    await message.answer_video(video)

# MUSIQA QIDIRISH
@dp.message_handler(lambda m: m.text 
and "http" not in m.text
and m.text not in ["📥 TikTok","📥 Instagram","▶️ YouTube","🎵 Musiqa","🎬 Kino","☀️ Ob-havo"])
async def music_search(message: types.Message):

    search = VideosSearch(message.text, limit=10)
    result = search.result()["result"]

    search_results[message.from_user.id] = result

    text = f"🔎 {message.text}\n\n"

    keyboard = InlineKeyboardMarkup(row_width=5)

    buttons = []

    for i, video in enumerate(result, start=1):

        title = video["title"]
        duration = video["duration"]

        text += f"{i}. {title} {duration}\n"

        buttons.append(
            InlineKeyboardButton(str(i), callback_data=f"music_{i}")
        )

    keyboard.add(*buttons)

    await message.answer(text, reply_markup=keyboard)

# MUSIQA TANLASH
@dp.callback_query_handler(lambda c: c.data.startswith("music_"))
async def send_music(call: types.CallbackQuery):

    index = int(call.data.split("_")[1]) - 1
    video = search_results[call.from_user.id][index]

    url = video["link"]

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'music.mp3'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    audio = open("music.mp3","rb")

    await call.message.answer_audio(
        audio,
        title=video["title"]
    )

# KINO
@dp.message_handler(lambda m: m.text == "🎬 Kino")
async def kino(message: types.Message):

    await message.answer("Kino qidirish funksiyasi tez orada qo‘shiladi")

# OB HAVO
@dp.message_handler(lambda m: m.text == "☀️ Ob-havo")
async def weather(message: types.Message):

    city = "Tashkent"

    url = f"https://wttr.in/{city}?format=3"

    r = requests.get(url)

    await message.answer(r.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
