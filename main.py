"""
AI Match Predictor Bot
"""

import logging
import os
from datetime import datetime

from api.football_api import FootballAPI
from prediction.predictor import MatchPredictor

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)


logging.basicConfig(
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/predict - Predict today's matches\n"
        "/help - Show help"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "/predict - Get predictions for today's matches.\n"
        "/start - Start the bot."
    )


async def predict(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        await update.message.reply_text(
            "🔎 Finding today's football matches...\n"
            "⏳ Please wait."
        )

        api = FootballAPI()

        predictor = MatchPredictor()

        # Cameroon time
        today = datetime.now().strftime("%Y-%m-%d")

        # Get today's fixtures
        data = api.get_fixtures_by_date(today)

        fixtures = data.get("response", [])

        if not fixtures:

            await update.message.reply_text(
                f"⚠️ No matches found for {today}."
            )

            return

        # Limit for now to protect the Free API quota
        fixtures = fixtures[:10]

        results = []

        for fixture in fixtures:

            fixture_id = fixture["fixture"]["id"]

            home_team = fixture["teams"]["home"]

            away_team = fixture["teams"]["away"]

            home_team_id = home_team["id"]

            away_team_id = away_team["id"]

            home_name = home_team["name"]

            away_name = away_team["name"]

            league = fixture["league"]

            league_id = league["id"]

            league_name = league["name"]

            # API-Football uses the starting year
            # of the competition season.
            season = league["season"]

            try:

                result = predictor.predict(
                    league_id=league_id,
                    season=season,
                    fixture_id=fixture_id,
                    home_team_id=home_team_id,
                    away_team_id=away_team_id
                )

                prediction = result["prediction"]

                results.append(
                    f"🏆 {league_name}\n\n"
                    f"⚽ {home_name} vs {away_name}\n\n"
                    f"🏠 Home Win: "
                    f"{prediction['home_win']}%\n"
                    f"🤝 Draw: "
                    f"{prediction['draw']}%\n"
                    f"✈️ Away Win: "
                    f"{prediction['away_win']}%\n\n"
                    f"🎯 Confidence: "
                    f"{prediction['confidence']}%\n"
                    f"⚠️ Risk: "
                    f"{prediction['risk']}\n\n"
                    f"🥇 Predicted: "
                    f"{result['winner']}"
                )

            except Exception as match_error:

                logging.exception(match_error)

                results.append(
                    f"⚽ {home_name} vs {away_name}\n"
                    f"❌ Prediction unavailable\n"
                    f"Reason: {match_error}"
                )

        # Send results in groups so Telegram
        # doesn't reject an oversized message.
        message = ""

        for result in results:

            if len(message) + len(result) + 5 > 4000:

                await update.message.reply_text(
                    message
                )

                message = ""

            message += result + "\n\n"

        if message:

            await update.message.reply_text(
                message
            )

    except Exception as e:

        logging.exception(e)

        await update.message.reply_text(
            f"❌ Prediction system error:\n{e}"
        )


def main():

    if not TOKEN:

        raise ValueError(
            "Missing TELEGRAM_TOKEN"
        )

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    app.add_handler(
        CommandHandler(
            "predict",
            predict
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
