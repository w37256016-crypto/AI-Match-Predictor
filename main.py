"""
AI Match Predictor Bot
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
    await update.message.reply_text(
        "Use /predict to generate a football match prediction."
    )


async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        predictor = MatchPredictor()

        result = predictor.predict(
    league_id=39,
    season=2024,
    fixture_id=12345,
    home_team_id=33,
    away_team_id=40
        )

        prediction = result["prediction"]

        await update.message.reply_text(
            f"🏆 AI Match Prediction\n\n"
            f"🏠 Home Win: {prediction['home_win']}%\n"
            f"🤝 Draw: {prediction['draw']}%\n"
            f"✈️ Away Win: {prediction['away_win']}%\n\n"
            f"🎯 Confidence: {prediction['confidence']}%\n"
            f"⚠️ Risk: {prediction['risk']}\n\n"
            f"🥇 Predicted Winner: {result['winner']}"
        )

    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(
            f"❌ Prediction failed:\n{e}"
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
