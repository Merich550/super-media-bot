from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import os
import logging
import yt_dlp
import requests
from aiogram import Bot, Dispatcher, executor, types
from youtubesearchpython import VideosSearch

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboard.add("📥 TikTok","📥 Instagram")
keyboard.add("▶️ YouTube","🎵 Musiqa")
keyboard.add("🎬 Kino","☀️ Ob-havo")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🤖 Super Media Bot", reply_markup=keyboard)


# TikTok tugma
@dp.message_handler(lambda m: m.text == "📥 TikTok")
async def tiktok_btn(message: types.Message):
    await message.answer("TikTok link yuboring")


# TikTok yuklash
@dp.message_handler(lambda m: m.text and "tiktok.com" in m.text)
async def tiktok_download(message: types.Message):

    url = message.text

    ydl_opts = {
        'outtmpl': 'tiktok.mp4',
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("tiktok.mp4","rb")
    await message.answer_video(video)


# Instagram tugma
@dp.message_handler(lambda m: m.text == "📥 Instagram")
async def insta_btn(message: types.Message):
    await message.answer("Instagram link yuboring")


# Instagram yuklash
@dp.message_handler(lambda m: m.text and "instagram.com" in m.text)
async def insta_download(message: types.Message):

    url = message.text

    ydl_opts = {
        'outtmpl': 'insta.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("insta.mp4","rb")
    await message.answer_video(video)


# YouTube tugma
@dp.message_handler(lambda m: m.text == "▶️ YouTube")
async def yt_btn(message: types.Message):
    await message.answer("YouTube link yuboring")


# YouTube yuklash
@dp.message_handler(lambda m: m.text and ("youtube.com" in m.text or "youtu.be" in m.text))
async def yt_download(message: types.Message):

    url = message.text

    ydl_opts = {
        'outtmpl': 'youtube.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video = open("youtube.mp4","rb")
    await message.answer_video(video)


# Musiqa tugma
@dp.message_handler(lambda m: m.text == "🎵 Musiqa")
async def music_btn(message: types.Message):
    await message.answer("Musiqa nomini yozing")



    

        
        

        

        
            
            
        

        
            

        
        

    
    


# Kino
@dp.message_handler(lambda m: m.text == "🎬 Kino")
async def kino(message: types.Message):
    await message.answer("Kino funksiyasi tez orada qo‘shiladi")


# Ob-havo



   # Musiqa qidirish
@dp.message_handler(lambda m: m.text and "http" not in m.text and m.text not in ["📥 TikTok","📥 Instagram","▶️ YouTube","🎵 Musiqa","🎬 Kino","☀️ Ob-havo"])
async def music_search(message: types.Message):

    try:
        search = VideosSearch(message.text, limit=1)
        result = search.result()

        url = result["result"][0]["link"]

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'music.mp3'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio = open("music.mp3","rb")
        await message.answer_audio(audio)

    except:
        await message.answer("Musiqa topilmadi")

        
        result = search.result()

        url = result["result"][0]["link"]

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'music.mp3'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio = open("music.mp3","rb")
        await message.answer_audio(audio)

    except:
        await message.answer("Musiqa topilmadi")
  # Ob-havo
@dp.message_handler(lambda m: m.text == "☀️ Ob-havo")
async def weather(message: types.Message):

    city = "Tashkent"
    url = f"https://wttr.in/{city}?format=3"

    r = requests.get(url)

    await message.answer(r.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
