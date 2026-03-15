import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga qo‘shiq nomini yuboring.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        filename = ydl.prepare_filename(info)

    await update.message.reply_audio(audio=open(filename, 'rb'), title=info['title'])

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
