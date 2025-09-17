from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp as youtube_dl
import os

BOT_TOKEN = "8020894234:AAGrwLt95H6C_4d_PZ38U3wvIXrGYi0Kg1s"

CHANNELS = [
    "https://t.me/AI_SI_II",
    "https://t.me/magick_AI_PRO",
    "https://t.me/web_saites"
]

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("1-Kanal", url=CHANNELS[2])],
        [InlineKeyboardButton("2-Kanal", url=CHANNELS[1])],
        [InlineKeyboardButton("3-Kanal", url=CHANNELS[0])],
        [InlineKeyboardButton("Obuna bo‘ldim ✅", callback_data="sub_done")]
    ]
    await update.message.reply_text(
        "Salom! Videoni olish uchun 3 ta kanalga obuna bo‘lishingiz shart.\n\n"
        "Barcha kanallarga obuna bo‘lgandan so‘ng 'Obuna bo‘ldim' tugmasini bosing.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Tugma bosilganda obuna qilingan deb qabul qilamiz
async def sub_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text("Rahmat! Endi YouTube linkini yuboring.")
    
# YouTube videoni yuklash
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("Video yoki playlist yuklanmoqda, biroz kuting...")

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': False
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if 'entries' in info_dict:
                videos = info_dict['entries']
            else:
                videos = [info_dict]

            for video in videos:
                file_path = ydl.prepare_filename(video)
                await context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'))
                os.remove(file_path)
        await msg.edit_text("Barcha videolar jo‘natildi ✅")
    except Exception as e:
        await msg.edit_text(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(sub_done, pattern="sub_done"))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))

    app.run_polling()