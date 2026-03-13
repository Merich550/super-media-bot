import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "8705691968:AAFsg3UVE1YRWQl7RlIhRP7v-R_Een7kBYw"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message(commands=["start"])
async def start(msg: types.Message):

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

    await msg.answer(text)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
