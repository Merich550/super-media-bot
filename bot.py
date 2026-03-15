import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Qo‘shiq nomini yuboring")

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("⏳ Qidirilmoqda...")

    try:
        ydl_opts = {
            "quiet": True,
            "default_search": "ytsearch1"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            video = info["entries"][0]

        title = video["title"]
        url = video["url"]

        await update.message.reply_audio(audio=url, title=title)

    except Exception as e:
        await update.message.reply_text("❌ Qo‘shiq topilmadi")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))

app.run_polling()
