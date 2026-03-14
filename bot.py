import yt_dlp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8705691968:AAE24pVc2UOeBDvl2sXsz639xTwhxeWRypU"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

mode = {}

# ---------- KEYBOARD ----------
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    KeyboardButton("📥 TikTok"),
    KeyboardButton("📥 Instagram")
)
keyboard.add(
    KeyboardButton("🎵 Musiqa"),
    KeyboardButton("🎬 Kino qidirish")
)

# ---------- START ----------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🤖 SUPER MEDIA BOT\nTanlang:", reply_markup=keyboard)


# ---------- TIKTOK ----------
@dp.message_handler(lambda m: m.text == "📥 TikTok")
async def tiktok_mode(message: types.Message):
    mode[message.from_user.id] = "tiktok"
    await message.answer("📥 TikTok link yuboring")

@dp.message_handler(lambda m: "tiktok.com" in m.text)
async def tiktok_download(message: types.Message):

    if mode.get(message.from_user.id) != "tiktok":
        return

    url = message.text

    ydl_opts = {
        'outtmpl': 'tiktok.mp4'
    }

    await message.answer("⏳ Video yuklanmoqda...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await message.answer_video(open("tiktok.mp4", "rb"))


# ---------- INSTAGRAM ----------
@dp.message_handler(lambda m: m.text == "📥 Instagram")
async def insta_mode(message: types.Message):
    mode[message.from_user.id] = "instagram"
    await message.answer("📥 Instagram link yuboring")

@dp.message_handler(lambda m: "instagram.com" in m.text)
async def insta_download(message: types.Message):

    if mode.get(message.from_user.id) != "instagram":
        return

    url = message.text

    ydl_opts = {
        'outtmpl': 'insta.mp4'
    }

    await message.answer("⏳ Video yuklanmoqda...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await message.answer_video(open("insta.mp4", "rb"))


# ---------- MUSIQA ----------
@dp.message_handler(lambda m: m.text == "🎵 Musiqa")
async def music_mode(message: types.Message):
    mode[message.from_user.id] = "music"
    await message.answer("🎵 Musiqa nomini yozing")

@dp.message_handler(lambda m: mode.get(m.from_user.id) == "music")
async def music_download(message: types.Message):

    query = message.text

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'music.%(ext)s'
    }

    await message.answer("⏳ Musiqa yuklanmoqda...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]

    await message.answer_audio(open("music.webm", "rb"))


# ---------- KINO ----------
@dp.message_handler(lambda m: m.text == "🎬 Kino qidirish")
async def kino_mode(message: types.Message):
    mode[message.from_user.id] = "kino"
    await message.answer("🎬 Kino nomini yozing")

@dp.message_handler(lambda m: mode.get(m.from_user.id) == "kino")
async def kino_search(message: types.Message):

    q = message.text
    link = f"https://www.youtube.com/results?search_query={q}+kino"

    await message.answer("🎬 Kino topildi:\n" + link)


# ---------- RUN ----------
if __name__ == "__main__":
    executor.start_polling(dp)
