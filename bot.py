from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import yt_dlp
import os

TOKEN = "8705691968:AAFsg3UVE1YRWQl7RlIhRP7v-R_Een7kBYw"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("📥 TikTok"),
    KeyboardButton("📥 YouTube")
)
menu.add(
    KeyboardButton("📥 Instagram")
)

# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "🤖 Super Media Bot\n\n"
        "Video yuklash uchun tugmani tanlang:",
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


# DOWNLOAD
@dp.message_handler()
async def downloader(message: types.Message):

    url = message.text

    if not any(x in url for x in ["tiktok.com","youtube.com","youtu.be","instagram.com"]):
        return

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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
