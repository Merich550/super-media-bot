import os
import yt_dlp
import openai

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# =========================
# TOKENLAR
# =========================

TOKEN = "8705691968:AAGPoBPIpPc3JTJd6NZ-diKI0kE3eV7SZKQ"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# =========================
# MENU
# =========================

menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.add(
    KeyboardButton("📥 TikTok"),
    KeyboardButton("📥 Instagram")
)

menu.add(
    KeyboardButton("🔎 Kino qidirish"),
    KeyboardButton("🤖 AI Chat")
)

# =========================
# START
# =========================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    text = """
🚀 Super Media Bot

Bu bot nima qila oladi?

📥 TikTok video yuklash
📥 Instagram video yuklash
🔎 Kino qidirish
🤖 AI Chat

Kerakli tugmani tanlang 👇
"""

    await message.answer(text, reply_markup=menu)

# =========================
# TIKTOK TUGMA
# =========================

@dp.message_handler(lambda message: message.text == "📥 TikTok")
async def tiktok_button(message: types.Message):
    await message.answer("📥 TikTok link yuboring")

# =========================
# INSTAGRAM TUGMA
# =========================

@dp.message_handler(lambda message: message.text == "📥 Instagram")
async def instagram_button(message: types.Message):
    await message.answer("📥 Instagram link yuboring")

# =========================
# VIDEO YUKLASH
# =========================

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

# =========================
# KINO QIDIRISH
# =========================

kino_mode = {}

@dp.message_handler(lambda message: message.text == "🔎 Kino qidirish")
async def kino_start(message: types.Message):

    kino_mode[message.from_user.id] = True

    await message.answer("🎬 Kino nomini yozing")

@dp.message_handler()
async def kino_search(message: types.Message):

    if kino_mode.get(message.from_user.id):

        kino_mode[message.from_user.id] = False

        link = f"https://www.google.com/search?q={message.text}+kino"

        await message.answer(f"🔎 Kino qidiruv natijasi:\n{link}")

# =========================
# AI CHAT
# =========================

ai_mode = {}

@dp.message_handler(lambda message: message.text == "🤖 AI Chat")
async def ai_start(message: types.Message):

    ai_mode[message.from_user.id] = True

    await message.answer("🤖 AI Chat yoqildi.\nSavolingizni yozing.")

@dp.message_handler()
async def ai_chat(message: types.Message):

    if ai_mode.get(message.from_user.id):

        try:

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Sen aqlli AI yordamchisan. O'zbek tilida aniq va tushunarli javob ber."
                    },
                    {
                        "role": "user",
                        "content": message.text
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )

            reply = response.choices[0].message.content

            await message.answer(reply)

        except:
            await message.answer("❌ AI javob bera olmadi")

# =========================
# BOTNI ISHGA TUSHIRISH
# =========================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
