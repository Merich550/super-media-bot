import os
import yt_dlp
import openai

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "8705691968:AAE24pVc2UOeBDvl2sXsz639xTwhxeWRypU"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_mode = {}

menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.add(
KeyboardButton("📥 TikTok"),
KeyboardButton("📥 Instagram")
)

menu.add(
KeyboardButton("🎵 Musiqa"),
KeyboardButton("🔎 Kino qidirish")
)

menu.add(
KeyboardButton("🤖 AI Chat")
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.answer(
        "🚀 SUPER MEDIA BOT\n\n"
        "📥 TikTok yuklash\n"
        "📥 Instagram yuklash\n"
        "🎵 Musiqa yuklash\n"
        "🔎 Kino qidirish\n"
        "🤖 AI Chat",
        reply_markup=menu
    )

@dp.message_handler(lambda message: message.text == "📥 TikTok")
async def tiktok(message: types.Message):

    user_mode[message.from_user.id] = "tiktok"
    await message.answer("📥 TikTok link yuboring")

@dp.message_handler(lambda message: message.text == "📥 Instagram")
async def instagram(message: types.Message):

    user_mode[message.from_user.id] = "instagram"
    await message.answer("📥 Instagram link yuboring")

@dp.message_handler(lambda message: message.text == "🎵 Musiqa")
async def music(message: types.Message):

    user_mode[message.from_user.id] = "music"
    await message.answer("🎵 Musiqa nomini yozing")

@dp.message_handler(lambda message: message.text == "🔎 Kino qidirish")
async def kino(message: types.Message):

    user_mode[message.from_user.id] = "kino"
    await message.answer("🎬 Kino nomini yozing")

@dp.message_handler(lambda message: message.text == "🤖 AI Chat")
async def ai(message: types.Message):

    user_mode[message.from_user.id] = "ai"
    await message.answer("🤖 Savol yozing")

@dp.message_handler()
async def handler(message: types.Message):

    mode = user_mode.get(message.from_user.id)

    if mode == "tiktok":

        await message.answer("⏳ Video yuklanmoqda...")

        ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'tiktok.mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])

        await bot.send_video(message.chat.id, open("tiktok.mp4","rb"))

        os.remove("tiktok.mp4")

    elif mode == "instagram":

        await message.answer("⏳ Video yuklanmoqda...")

        ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'insta.mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])

        await bot.send_video(message.chat.id, open("insta.mp4","rb"))

        os.remove("insta.mp4")

    elif mode == "music":

        await message.answer("⏳ Musiqa yuklanmoqda...")

        ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'music.mp3'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{message.text}"])

        await bot.send_audio(message.chat.id, open("music.mp3","rb"))

        os.remove("music.mp3")

    elif mode == "kino":

        await message.answer("🎬 Kino topildi")

        url = f"https://www.youtube.com/results?search_query={message.text}+kino"

        await message.answer(url)

    elif mode == "ai":

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":message.text}]
        )

        text = response['choices'][0]['message']['content']

        await message.answer(text)

if __name__ == "__main__":
    executor.start_polling(dp)
