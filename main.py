
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID")

# Newest result first: Period, Number
history = [
    ("50374", 2), ("50373", 9), ("50372", 2),
    ("50371", 1), ("50370", 9), ("50369", 2),
    ("50368", 6), ("50367", 5), ("50366", 8),
    ("50365", 6), ("50364", 6), ("50363", 8),
    ("50362", 2), ("50361", 4), ("50360", 0),
    ("50359", 9), ("50358", 2), ("50357", 2),
    ("50356", 1), ("50355", 9), ("50354", 3),
    ("50353", 5), ("50352", 0), ("50351", 8),
    ("50350", 7), ("50349", 3), ("50348", 1),
    ("50347", 0), ("50346", 1), ("50345", 8)
]

def size(n):
    return "Big" if n >= 5 else "Small"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Kathir Wingo Bot!\n\n"
        "/history - Last 30 results\n"
        "/stats - Number statistics\n"
        "/bigsmall - Big/Small count\n"
        "/id - Your Telegram ID\n"
        "/add PERIOD NUMBER - Add result (admin only)\n\n"
        "Note: Results are historical, not predictions."
    )

async def history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["📋 LAST 30 WINGO RESULTS\n"]
    for period, n in history[:30]:
        lines.append(f"{period} | {n} | {size(n)}")
    await update.message.reply_text("\n".join(lines))

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    counts = [sum(1 for _, n in history[:30] if n == i)
              for i in range(10)]
    msg = "📊 NUMBER STATISTICS\n\n"
    msg += "\n".join(f"{i}: {counts[i]}" for i in range(10))
    await update.message.reply_text(msg)

async def bigsmall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    big = sum(1 for _, n in history[:30] if n >= 5)
    small = min(30, len(history)) - big
    await update.message.reply_text(
        f"📊 BIG: {big}\n📊 SMALL: {small}\n"
        "Past results do not predict future results."
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Telegram ID: {update.effective_user.id}"
    )

async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_ID or str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("⛔ Admin only.")
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Use: /add PERIOD NUMBER\nExample: /add 50375 4"
        )
        return

    period, number_text = context.args
    if not period.isdigit() or not number_text.isdigit():
        await update.message.reply_text("Period and number must be digits.")
        return

    number = int(number_text)
    if not 0 <= number <= 9:
        await update.message.reply_text("Number must be 0 to 9.")
        return

    history.insert(0, (period, number))
    del history[30:]
    await update.message.reply_text(
        f"✅ Added: {period} | {number} | {size(number)}"
    )

def main():
    if not TOKEN:
        raise RuntimeError("Set BOT_TOKEN in Railway Variables")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history_cmd))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("bigsmall", bigsmall))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("add", add_result))
    print("Kathir Wingo Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
          
