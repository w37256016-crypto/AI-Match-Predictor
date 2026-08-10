"""
AI Match Predictor Bot
"""

import logging
import os
from datetime import datetime

from api.football_api import FootballAPI

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


# --------------------------------------------------
# START
# --------------------------------------------------

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


# --------------------------------------------------
# HELP
# --------------------------------------------------

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "/predict - Automatically find and "
        "predict today's football matches."
    )


# --------------------------------------------------
# GET API-FOOTBALL PREDICTION
# --------------------------------------------------

def get_prediction(api, fixture_id):

    data = api.get_prediction(
        fixture_id
    )

    response = data.get(
        "response",
        []
    )

    if not response:
        return None

    prediction_data = response[0]

    predictions = prediction_data.get(
        "predictions",
        {}
    )

    percentages = predictions.get(
        "percent",
        {}
    )

    home = percentages.get(
        "home"
    )

    draw = percentages.get(
        "draw"
    )

    away = percentages.get(
        "away"
    )

    # If API has no percentages,
    # don't pretend we have a prediction.
    if home is None or draw is None or away is None:
        return None

    winner = predictions.get(
        "winner"
    )

    winner_name = None

    if isinstance(winner, dict):
        winner_name = winner.get(
            "name"
        )

    advice = predictions.get(
        "advice"
    )

    goals = predictions.get(
        "goals",
        {}
    )

    home_goals = goals.get(
        "home"
    )

    away_goals = goals.get(
        "away"
    )

    return {
        "home": home,
        "draw": draw,
        "away": away,
        "winner": winner_name,
        "advice": advice,
        "home_goals": home_goals,
        "away_goals": away_goals
    }


# --------------------------------------------------
# CONVERT PERCENTAGE TO NUMBER
# --------------------------------------------------

def percentage_to_number(value):

    try:
        return float(
            str(value).replace(
                "%",
                ""
            )
        )

    except (
        ValueError,
        TypeError
    ):
        return None


# --------------------------------------------------
# CONFIDENCE
# --------------------------------------------------

def calculate_confidence(
    home,
    draw,
    away
):

    values = [
        percentage_to_number(home),
        percentage_to_number(draw),
        percentage_to_number(away)
    ]

    values = [
        value
        for value in values
        if value is not None
    ]

    if not values:
        return 0

    return round(
        max(values),
        2
    )


# --------------------------------------------------
# RISK
# --------------------------------------------------

def calculate_risk(confidence):

    if confidence >= 70:
        return "Low"

    if confidence >= 55:
        return "Medium"

    return "High"


# --------------------------------------------------
# FORMAT GOAL RANGE
# --------------------------------------------------

def format_goal_range(
    home_goals,
    away_goals
):

    if (
        home_goals is None
        or away_goals is None
    ):
        return None

    return (
        f"{home_goals} - "
        f"{away_goals}"
    )


# --------------------------------------------------
# PREDICT
# --------------------------------------------------

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

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        # Get today's fixtures.
        fixture_data = api.get_fixtures_by_date(
            today
        )

        fixtures = fixture_data.get(
            "response",
            []
        )

        if not fixtures:

            await update.message.reply_text(
                f"⚠️ No football matches found "
                f"for {today}."
            )

            return

        # --------------------------------------------------
        # FREE PLAN PROTECTION
        # --------------------------------------------------

        # We deliberately start with 8 matches.
        # We can increase this later after optimization.
        fixtures = fixtures[:8]

        await update.message.reply_text(
            f"⚽ Found {len(fixtures)} matches.\n\n"
            f"🧠 Generating predictions..."
        )

        results = []

        for fixture in fixtures:

            fixture_id = fixture[
                "fixture"
            ][
                "id"
            ]

            home_team = fixture[
                "teams"
            ][
                "home"
            ]

            away_team = fixture[
                "teams"
            ][
                "away"
            ]

            home_name = home_team[
                "name"
            ]

            away_name = away_team[
                "name"
            ]

            league = fixture[
                "league"
            ]

            league_name = league[
                "name"
            ]

            try:

                prediction = get_prediction(
                    api,
                    fixture_id
                )

                if not prediction:

                    results.append(
                        f"🏆 {league_name}\n\n"
                        f"⚽ {home_name} vs "
                        f"{away_name}\n\n"
                        f"⚠️ Prediction unavailable."
                    )

                    continue

                home = prediction[
                    "home"
                ]

                draw = prediction[
                    "draw"
                ]

                away = prediction[
                    "away"
                ]

                confidence = calculate_confidence(
                    home,
                    draw,
                    away
                )

                risk = calculate_risk(
                    confidence
                )

                winner = prediction[
                    "winner"
                ]

                advice = prediction[
                    "advice"
                ]

                goal_range = format_goal_range(
                    prediction[
                        "home_goals"
                    ],
                    prediction[
                        "away_goals"
                    ]
                )

                message = (
                    f"🏆 {league_name}\n\n"
                    f"⚽ {home_name} vs "
                    f"{away_name}\n\n"
                    f"📊 Prediction\n\n"
                    f"🏠 Home Win: {home}\n"
                    f"🤝 Draw: {draw}\n"
                    f"✈️ Away Win: {away}\n\n"
                    f"🎯 Confidence: "
                    f"{confidence}%\n"
                    f"⚠️ Risk: {risk}\n\n"
                    f"🥇 Predicted: "
                    f"{winner or 'No clear winner'}"
                )

                if advice:

                    message += (
                        f"\n\n"
                        f"💡 Advice: {advice}"
                    )

                if goal_range:

                    message += (
                        f"\n\n"
                        f"⚽ Goal Range: "
                        f"{goal_range}"
                    )

                results.append(
                    message
                )

            except Exception as match_error:

                logging.warning(
                    "Prediction failed for "
                    "fixture %s: %s",
                    fixture_id,
                    match_error
                )

                results.append(
                    f"⚽ {home_name} vs "
                    f"{away_name}\n\n"
                    f"❌ Prediction unavailable."
                )

        # --------------------------------------------------
        # SEND RESULTS
        # --------------------------------------------------

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


# --------------------------------------------------
# MAIN
# --------------------------------------------------

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
