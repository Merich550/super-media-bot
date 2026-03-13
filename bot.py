from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import yt_dlp
import os

TOKEN = "8705691968:AAGPoBPIpPc3JTJd6NZ-diKI0kE3eV7SZKQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("📥 TikTok"),
    KeyboardButton("📥 Instagram")
)
menu.add(
    KeyboardButton("🔎 Kino qidirish")
)

# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "🤖 Super Media Bot\n\n"
        "Tugmani tanlang 👇",
        reply_markup=menu
    )

# TIKTOK
@dp.message_handler(lambda message: message.text == "📥 TikTok")
async def tiktok(message: types.Message):
    await message.answer("📥 TikTok link yuboring")

# INSTAGRAM
@dp.message_handler(lambda message: message.text == "📥 Instagram")
async def instagram(message: types.Message):
    await message.answer("📥 Instagram link yuboring")

# KINO SEARCH BUTTON
@dp.message_handler(lambda message: message.text == "🔎 Kino qidirish")
async def kino(message: types.Message):
    await message.answer("🎬 Kino nomini yozing")

# VIDEO DOWNLOAD
@dp.message_handler(lambda message: "tiktok.com" in message.text or "instagram.com" in message.text)
async def downloader(message: types.Message):

    url = message.text

    await message.answer("⏳ Video yuklanmoqda...")

    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None

        for file in os.listdir():
            if file.startswith("video"):
                video_file = file
                break

        if video_file:
            await message.answer_video(open(video_file, "rb"))
            os.remove(video_file)

    except:
        await message.answer("❌ Video yuklab bo‘lmadi")

# KINO SEARCH
@dp.message_handler()
async def kino_search(message: types.Message):

    if message.text.startswith("📥") or message.text.startswith("🔎"):
        return

    movie = message.text

    search_url = f"https://www.google.com/search?q={movie}+kino"

    await message.answer(
        f"🔎 Kino qidiruv natijasi:\n{search_url}"
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
