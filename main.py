
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "வணக்கம்! 👋\n"
        "எனது Telegram Bot-க்கு வரவேற்கிறேன்!\n"
        "உங்கள் செய்தியை அனுப்புங்கள்."
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "உங்கள் செய்தி கிடைத்தது! 😊"
    )

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is missing")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
    
    
