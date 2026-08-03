"""
AI Match Predictor Bot - Part 1
This is the starter structure.
The full project will be built in later parts.
"""

import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "Commands:\n"
        "/start\n"
        "/predict\n"
        "/help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /predict to begin.")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Part 1 installed successfully!\n"
        "Interactive day and league menus will be added in the next version."
    )

def main():
    if not TOKEN:
        raise ValueError("Missing TELEGRAM_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("predict", predict))
    app.run_polling()

if __name__ == "__main__":
    main()
