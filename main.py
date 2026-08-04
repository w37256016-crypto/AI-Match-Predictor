"""
AI Match Predictor Bot - Part 1
This is the starter structure.
The full project will be built in later parts.
"""

import logging
import os

from prediction.predictor import MatchPredictor
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
    predictor = MatchPredictor()

    result = predictor.predict(
        league_id=39,
        season=2025,
        fixture_id=12345,
        home_team_id=33,
        away_team_id=40
    )

    await update.message.reply_text(
        f"🏆 Prediction\n\n"
        f"Home Win: {result['prediction']['home_win']}%\n"
        f"Draw: {result['prediction']['draw']}%\n"
        f"Away Win: {result['prediction']['away_win']}%\n\n"
        f"Predicted Winner: {result['winner']}"
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
