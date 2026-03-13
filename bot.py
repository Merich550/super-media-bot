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

🎬 /kino - Kino qidirish
🎬 /kod - Kino kodi
🎵 /music - Musiqa topish
📥 /tiktok - TikTok video yuklash
📥 /instagram - Instagram video yuklash
📥 /youtube - YouTube video yuklash
🤖 /ai - AI chat
📞 /help - Yordam
"""
    await message.answer(text)


@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    text = """
📞 Yordam menyusi

/kino - Kino qidirish
/kod - Kino kodi
/music - Musiqa topish
/tiktok - TikTok video yuklash
/instagram - Instagram video yuklash
/youtube - YouTube video yuklash
/ai - AI chat
"""
    await message.answer(text)


@dp.message_handler(commands=["tiktok"])
async def tiktok_cmd(message: types.Message):
    await message.answer("📥 TikTok link yuboring")


@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text

    if "tiktok.com" in url:
        await message.answer("⏳ Video yuklanmoqda...")

        ydl_opts = {
            'outtmpl': 'video.%(ext)s'
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
