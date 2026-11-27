
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
import os

PATTERN_1 = [
    "SMALL", "SMALL", "SMALL",
    "BIG", "BIG", "BIG"
]

PATTERN_2 = [
    "SMALL", "BIG", "SMALL",
    "BIG", "SMALL"
]

PREDICTIONS = PATTERN_1 + PATTERN_2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if not jobs:
        context.job_queue.run_repeating(
            prediction,
            interval=30,
            first=0,
            chat_id=chat_id,
            name=str(chat_id)
        )

    await update.message.reply_text(
        "வணக்கம்! 👋\n\n"
        "உன்னுடைய இரண்டு Patterns சேர்க்கப்பட்டுள்ளன.\n"
        "⏱️ ஒவ்வொரு 30 விநாடிக்கும் அடுத்த Prediction வரும்.\n\n"
        "🟢 Auto Prediction STARTED!"
    )


async def prediction(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    indices = context.application.bot_data
    index = indices.get(str(chat_id), 0)

    result = PREDICTIONS[index]

    pattern_name = (
        "Pattern 1" if index < len(PATTERN_1)
        else "Pattern 2"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🔮 AUTO PREDICTION\n\n"
            f"📌 {pattern_name}\n"
            f"🎯 Prediction: {result}\n"
            f"🔢 Step: {index + 1}\n"
            "⏱️ Next Prediction: 30 Seconds"
        )
    )

    indices[str(chat_id)] = (
        index + 1
    ) % len(PREDICTIONS)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    for job in jobs:
        job.schedule_removal()

    await update.message.reply_text(
        "🛑 Auto Prediction STOPPED!"
    )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is missing")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()


if __name__ == "__main__":
    main()

