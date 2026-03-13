import os
import yt_dlp
import openai

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# =========================
# TOKENS
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
    await message.answer(
        "🤖 Super Media Bot\n\n"
        "Kerakli tugmani tanlang 👇",
        reply_markup=menu
    )

# =========================
# BUTTON HANDLERS
# =========================
@dp.message_handler(lambda m: m.text == "📥 TikTok")
async def ask_tiktok(message: types.Message):
    await message.answer("📥 TikTok link yuboring")

@dp.message_handler(lambda m: m.text == "📥 Instagram")
async def ask_instagram(message: types.Message):
    await message.answer("📥 Instagram link yuboring")

@dp.message_handler(lambda m: m.text == "🔎 Kino qidirish")
async def ask_movie(message: types.Message):
    await message.answer("🎬 Kino nomini yozing")

@dp.message_handler(lambda m: m.text == "🤖 AI Chat")
async def ask_ai(message: types.Message):
    await message.answer("🤖 Savolingizni yozing")

# =========================
# VIDEO DOWNLOAD
# =========================
@dp.message_handler(lambda m: ("tiktok.com" in m.text) or ("instagram.com" in m.text))
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Video yuklanmoqda...")

    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "best",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None
        for f in os.listdir():
            if f.startswith("video"):
                video_file = f
                break

        if video_file:
            with open(video_file, "rb") as vf:
                await message.answer_video(vf)
            os.remove(video_file)
        else:
            await message.answer("❌ Video topilmadi")

    except Exception as e:
        await message.answer("❌ Video yuklab bo‘lmadi")

# =========================
# KINO SEARCH
# =========================
@dp.message_handler()
async def movie_or_ai(message: types.Message):
    text = message.text.strip()

    # Tugmalar matnini o'tkazib yuboramiz
    if text in ["📥 TikTok", "📥 Instagram", "🔎 Kino qidirish", "🤖 AI Chat"]:
        return

    # Agar link bo'lmasa -> kino qidiruv
    if not ("tiktok.com" in text or "instagram.com" in text):
        # Agar foydalanuvchi oldin "🔎 Kino qidirish" ni bosgan bo‘lsa
        if "kino" not in text.lower():
            search_url = f"https://www.google.com/search?q={text}+kino"
            await message.answer(f"🔎 Kino qidiruv natijasi:\n{search_url}")
            return

    # =========================
    # AI CHAT
    # =========================
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=300
        )

        answer = response.choices[0].message.content.strip()
        await message.answer(answer)

    except Exception:
        await message.answer("❌ AI javob bera olmadi")

# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
