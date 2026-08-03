import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "Welcome!\n\n"
        "Available commands:\n"
        "/today - Today's predictions\n"
        "/tomorrow - Tomorrow's predictions\n"
        "/weekend - Weekend predictions\n"
        "/help - Help menu"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Commands\n\n"
        "/today - Today's predictions\n"
        "/tomorrow - Tomorrow's predictions\n"
        "/weekend - Weekend predictions\n"
        "/help - Show this message"
    )


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Today's AI Predictions\n\n"
        "No predictions available yet.\n"
        "Live football analysis will be added in the next update."
    )


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 Tomorrow's AI Predictions\n\n"
        "No predictions available yet."
    )


async def weekend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 Weekend AI Predictions\n\n"
        "No predictions available yet."
    )


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("weekend", weekend))

    print("✅ Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
