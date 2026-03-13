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
    KeyboardButton("📥 YouTube")
)
menu.add(
    KeyboardButton("📥 Instagram"),
    KeyboardButton("🎵 MP3")
)

# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "🤖 Super Media Bot\n\n"
        "Bot nimalar qila oladi?\n"
        "📥 TikTok video yuklash\n"
        "📥 Instagram video yuklash\n"
        "📥 YouTube video yuklash\n"
        "🎵 YouTube MP3 yuklash\n\n"
        "Pastdagi tugmani tanlang 👇",
        reply_markup=menu
    )

# BUTTONS
@dp.message_handler(lambda message: message.text == "📥 TikTok")
async def tiktok(message: types.Message):
    await message.answer("📥 TikTok link yuboring")

@dp.message_handler(lambda message: message.text == "📥 YouTube")
async def youtube(message: types.Message):
    await message.answer("📥 YouTube link yuboring")

@dp.message_handler(lambda message: message.text == "📥 Instagram")
async def instagram(message: types.Message):
    await message.answer("📥 Instagram link yuboring")

@dp.message_handler(lambda message: message.text == "🎵 MP3")
async def mp3(message: types.Message):
    await message.answer("🎵 YouTube link yuboring")

# DOWNLOAD
@dp.message_handler()
async def downloader(message: types.Message):

    url = message.text

    if not any(x in url for x in ["tiktok.com","youtube.com","youtu.be","instagram.com"]):
        return

    await message.answer("⏳ Yuklanmoqda...")

    ydl_opts = {
        "outtmpl": "media.%(ext)s",
        "format": "best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file_name = None

        for file in os.listdir():
            if file.startswith("media"):
                file_name = file
                break

        if file_name:
            if "mp3" in file_name or "m4a" in file_name:
                await message.answer_audio(open(file_name, "rb"))
            else:
                await message.answer_video(open(file_name, "rb"))

            os.remove(file_name)

    except:
        await message.answer("❌ Yuklab bo‘lmadi")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
