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
async def tiktok(message: types.Message):
    await message.answer("📥 TikTok link yuboring")


@dp.message_handler(commands=["youtube"])
async def youtube(message: types.Message):
    await message.answer("📥 YouTube link yuboring")


@dp.message_handler(commands=["instagram"])
async def instagram(message: types.Message):
    await message.answer("📥 Instagram link yuboring")


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

        file = None

        for f in os.listdir():
            if f.startswith("video"):
                file = f
                break

        if file:
            await message.answer_video(open(file, "rb"))
            os.remove(file)

    except:
        await message.answer("❌ Video yuklab bo‘lmadi")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
