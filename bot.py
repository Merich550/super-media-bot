from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
