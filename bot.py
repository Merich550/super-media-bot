from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp
import os

TOKEN = "8705691968:AAFsg3UVE1YRWQl7RlIhRP7v-R_Een7kBYw"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = """
🤖 Super Media Bot

📥 TikTok / YouTube / Instagram video yuklaydi

Buyruqlar:
/tiktok
/youtube
/instagram
"""
    await message.answer(text)


@dp.message_handler(commands=["tiktok"])
async def tiktok_cmd(message: types.Message):
    await message.answer("📥 TikTok link yuboring")


@dp.message_handler(commands=["youtube"])
async def youtube_cmd(message: types.Message):
    await message.answer("📥 YouTube link yuboring")


@dp.message_handler(commands=["instagram"])
async def instagram_cmd(message: types.Message):
    await message.answer("📥 Instagram link yuboring")


@dp.message_handler(lambda message: message.text and (
        "tiktok.com" in message.text or
        "youtube.com" in message.text or
        "youtu.be" in message.text or
        "instagram.com" in message.text))
async def download_video(message: types.Message):

    url = message.text
    await message.answer("⏳ Video yuklanmoqda...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("video"):
            await message.answer_video(open(file, "rb"))
            os.remove(file)
            break


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
