import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

results_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Qo‘shiq nomini yuboring")

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.message.chat_id

    await update.message.reply_text("⏳ Qidirilmoqda...")

    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)

    videos = info["entries"]
    results_store[chat_id] = videos

    text = f"🔎 Natijalar: {query}\n\n"
    keyboard = []
    row = []

    for i, video in enumerate(videos):
        title = video["title"]
        duration = video.get("duration", 0)

        m = duration // 60
        s = duration % 60

        text += f"{i+1}. {title} {m}:{s:02d}\n"

        row.append(InlineKeyboardButton(str(i+1), callback_data=str(i)))

        if len(row) == 5:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    index = int(query.data)

    video = results_store[chat_id][index]
    url = video["webpage_url"]
    title = video["title"]

    await query.message.reply_audio(
        audio=url,
        title=title
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))
app.add_handler(CallbackQueryHandler(download_music))

app.run_polling()
