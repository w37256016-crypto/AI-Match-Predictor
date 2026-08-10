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
        "/predict - Automatically find and predict "
        "today's football matches."
    )


def get_api_prediction(api, fixture_id):

    data = api.get_prediction(fixture_id)

    response = data.get("response", [])

    if not response:
        raise ValueError(
            "No API-Football prediction available."
        )

    prediction_data = response[0]

    predictions = prediction_data.get(
        "predictions",
        {}
    )

    percentages = predictions.get(
        "percent",
        {}
    )

    home_percent = percentages.get(
        "home",
        "N/A"
    )

    draw_percent = percentages.get(
        "draw",
        "N/A"
    )

    away_percent = percentages.get(
        "away",
        "N/A"
    )

    winner = predictions.get(
        "winner",
        {}
    )

    winner_name = winner.get(
        "name",
        "Unknown"
    )

    advice = predictions.get(
        "advice",
        "No advice available"
    )

    goals = predictions.get(
        "goals",
        {}
    )

    home_goals = goals.get(
        "home",
        "N/A"
    )

    away_goals = goals.get(
        "away",
        "N/A"
    )

    return {
        "home_win": home_percent,
        "draw": draw_percent,
        "away_win": away_percent,
        "winner": winner_name,
        "advice": advice,
        "home_goals": home_goals,
        "away_goals": away_goals
    }


async def predict(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        await update.message.reply_text(
            "🔎 Finding today's football matches...\n\n"
            "⏳ Analyzing available matches..."
        )

        api = FootballAPI()

        predictor = MatchPredictor()

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        data = api.get_fixtures_by_date(
            today
        )

        fixtures = data.get(
            "response",
            []
        )

        if not fixtures:

            await update.message.reply_text(
                f"⚠️ No football matches found for "
                f"{today}."
            )

            return

        # Protect the Free API quota for now.
        fixtures = fixtures[:10]

        results = []

        for fixture in fixtures:

            fixture_id = fixture["fixture"]["id"]

            home = fixture["teams"]["home"]
            away = fixture["teams"]["away"]

            home_id = home["id"]
            away_id = away["id"]

            home_name = home["name"]
            away_name = away["name"]

            league = fixture["league"]

            league_id = league["id"]
            league_name = league["name"]
            season = league["season"]

            # ---------------------------------------
            # TRY OUR OWN AI MODEL
            # ---------------------------------------

            try:

                result = predictor.predict(
                    league_id=league_id,
                    season=season,
                    fixture_id=fixture_id,
                    home_team_id=home_id,
                    away_team_id=away_id
                )

                prediction = result["prediction"]

                results.append(
                    f"🏆 {league_name}\n\n"
                    f"⚽ {home_name} vs {away_name}\n\n"
                    f"🧠 Our AI Model\n\n"
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

                continue

            except Exception as model_error:

                logging.warning(
                    "Our AI failed for fixture %s: %s",
                    fixture_id,
                    model_error
                )

            # ---------------------------------------
            # FALLBACK TO API-FOOTBALL PREDICTION
            # ---------------------------------------

            try:

                api_prediction = get_api_prediction(
                    api,
                    fixture_id
                )

                results.append(
                    f"🏆 {league_name}\n\n"
                    f"⚽ {home_name} vs {away_name}\n\n"
                    f"📊 API-Football Prediction\n\n"
                    f"🏠 Home Win: "
                    f"{api_prediction['home_win']}\n"
                    f"🤝 Draw: "
                    f"{api_prediction['draw']}\n"
                    f"✈️ Away Win: "
                    f"{api_prediction['away_win']}\n\n"
                    f"🥇 Predicted: "
                    f"{api_prediction['winner']}\n\n"
                    f"💡 Advice: "
                    f"{api_prediction['advice']}\n\n"
                    f"⚽ Expected Goals: "
                    f"{api_prediction['home_goals']} - "
                    f"{api_prediction['away_goals']}"
                )

            except Exception as api_error:

                logging.exception(api_error)

                results.append(
                    f"⚽ {home_name} vs {away_name}\n\n"
                    f"❌ Prediction unavailable\n"
                    f"Reason: {api_error}"
                )

        # ---------------------------------------
        # SEND RESULTS
        # ---------------------------------------

        message = ""

        for result in results:

            if len(message) + len(result) > 3800:

                await update.message.reply_text(
                    message
                )

                message = ""

            message += result
            message += "\n\n"

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
