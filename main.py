

import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

PATTERN_1 = [
    "SMALL", "SMALL", "SMALL",
    "BIG", "BIG", "BIG"
]

PATTERN_2 = [
    "SMALL", "BIG", "SMALL",
    "BIG", "SMALL"
]

# இரண்டு Patterns-ஐ வரிசையாக இணைக்கிறோம்
PREDICTIONS = PATTERN_1 + PATTERN_2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # ஏற்கனவே இயங்கினால் மீண்டும் தொடங்க வேண்டாம்
    existing = context.job_queue.get_jobs_by_name(str(chat_id))

    if existing:
        await update.message.reply_text(
            "உங்கள் Automatic Pattern Bot ஏற்கனவே இயங்குகிறது!"
        )
        return

    context.job_queue.run_repeating(
        auto_prediction,
        interval=30,
        first=0,
        chat_id=chat_id,
        name=str(chat_id),
    )

    await update.message.reply_text(
        "வணக்கம்! 👋\n\n"
        "உங்கள் Pattern Bot தொடங்கிவிட்டது!\n"
        "30 விநாடிகளுக்கு ஒருமுறை Pattern Message வரும்.\n\n"
        "Pattern 1: SMALL SMALL SMALL BIG BIG BIG\n"
        "Pattern 2: SMALL BIG SMALL BIG SMALL\n\n"
        "/stop - நிறுத்த"
    )


async def auto_prediction(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    index = job.data.get("index", 0) if job.data else 0

    prediction = PREDICTIONS[index % len(PREDICTIONS)]
    pattern_name = (
        "Pattern 1"
        if index % len(PREDICTIONS) < len(PATTERN_1)
        else "Pattern 2"
    )

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=(
            "🤖 AUTOMATIC PATTERN UPDATE\n\n"
            f"📌 {pattern_name}\n"
            f"🎯 Pattern Result: {prediction}\n"
            f"🔢 Step: {index + 1}\n\n"
            "⏱ அடுத்த Message: 30 Seconds"
        ),
    )

    job.data = {"index": index + 1}


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    for job in jobs:
        job.schedule_removal()

    await update.message.reply_text(
        "⛔ Automatic Pattern Bot நிறுத்தப்பட்டது."
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()


if __name__ == "__main__":
    main()
