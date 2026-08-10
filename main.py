"""
AI Match Predictor Bot
"""

import logging
import os
from datetime import datetime, timedelta

from api.football_api import FootballAPI

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)


logging.basicConfig(level=logging.INFO)

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
        "/predict - Get football predictions\n"
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
        "Use /predict to choose a date "
        "and league for predictions."
    )


# --------------------------------------------------
# PREDICT COMMAND
# --------------------------------------------------

async def predict(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        [
            InlineKeyboardButton(
                "📅 Today",
                callback_data="date_today"
            )
        ],
        [
            InlineKeyboardButton(
                "📅 Tomorrow",
                callback_data="date_tomorrow"
            )
        ],
        [
            InlineKeyboardButton(
                "📅 Weekend",
                callback_data="date_weekend"
            )
        ]
    ]

    await update.message.reply_text(
        "📅 Choose when you want predictions:",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# --------------------------------------------------
# DATE BUTTON
# --------------------------------------------------

async def date_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    today = datetime.now().date()

    if query.data == "date_today":

        dates = [
            today
        ]

        title = "📅 Today's"

    elif query.data == "date_tomorrow":

        dates = [
            today + timedelta(days=1)
        ]

        title = "📅 Tomorrow's"

    else:

        # Saturday and Sunday
        days_until_saturday = (
            5 - today.weekday()
        ) % 7

        saturday = (
            today +
            timedelta(
                days=days_until_saturday
            )
        )

        sunday = (
            saturday +
            timedelta(days=1)
        )

        dates = [
            saturday,
            sunday
        ]

        title = "📅 Weekend"

    try:

        api = FootballAPI()

        fixtures = []

        for date in dates:

            date_string = date.strftime(
                "%Y-%m-%d"
            )

            data = api.get_fixtures_by_date(
                date_string
            )

            response = data.get(
                "response",
                []
            )

            fixtures.extend(response)

        if not fixtures:

            await query.edit_message_text(
                f"⚠️ No matches found for "
                f"{title.lower()}."
            )

            return

        # Store fixtures for the next step.
        context.user_data[
            "selected_fixtures"
        ] = fixtures

        # --------------------------------------------------
        # FIND LEAGUES
        # --------------------------------------------------

        leagues = {}

        for fixture in fixtures:

            league = fixture.get(
                "league",
                {}
            )

            league_id = league.get(
                "id"
            )

            league_name = league.get(
                "name",
                "Unknown League"
            )

            if league_id is not None:

                leagues[
                    league_id
                ] = league_name

        if not leagues:

            await query.edit_message_text(
                "⚠️ No leagues found."
            )

            return

        keyboard = []

        for league_id, league_name in list(
            leagues.items()
        )[:20]:

            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"🏆 {league_name}",
                        callback_data=(
                            f"league_{league_id}"
                        )
                    )
                ]
            )

        context.user_data[
            "selected_title"
        ] = title

        await query.edit_message_text(
            f"{title} matches found: "
            f"{len(fixtures)}\n\n"
            f"🏆 Choose a league:",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    except Exception as e:

        logging.exception(e)

        await query.edit_message_text(
            f"❌ Could not load matches:\n{e}"
        )


# --------------------------------------------------
# LEAGUE SELECTED
# --------------------------------------------------

async def league_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        league_id = int(
            query.data.replace(
                "league_",
                ""
            )
        )

        fixtures = context.user_data.get(
            "selected_fixtures",
            []
        )

        selected = [
            fixture
            for fixture in fixtures
            if fixture.get(
                "league",
                {}
            ).get(
                "id"
            ) == league_id
        ]

        if not selected:

            await query.edit_message_text(
                "⚠️ No matches found for "
                "this league."
            )

            return

        league_name = selected[0][
            "league"
        ][
            "name"
        ]

        await query.edit_message_text(
            f"🏆 {league_name}\n\n"
            f"⚽ Found {len(selected)} "
            f"matches.\n\n"
            f"🧠 Generating predictions..."
        )

        api = FootballAPI()

        results = []

        # Free-plan protection.
        selected = selected[:8]

        for fixture in selected:

            fixture_id = fixture[
                "fixture"
            ][
                "id"
            ]

            home_name = fixture[
                "teams"
            ][
                "home"
            ][
                "name"
            ]

            away_name = fixture[
                "teams"
            ][
                "away"
            ][
                "name"
            ]

            try:

                data = api.get_prediction(
                    fixture_id
                )

                response = data.get(
                    "response",
                    []
                )

                if not response:

                    results.append(
                        f"⚽ {home_name} vs "
                        f"{away_name}\n\n"
                        f"⚠️ Prediction unavailable."
                    )

                    continue

                prediction_data = response[0]

                predictions = (
                    prediction_data.get(
                        "predictions",
                        {}
                    )
                )

                percentages = (
                    predictions.get(
                        "percent",
                        {}
                    )
                )

                home = percentages.get(
                    "home",
                    "N/A"
                )

                draw = percentages.get(
                    "draw",
                    "N/A"
                )

                away = percentages.get(
                    "away",
                    "N/A"
                )

                winner = predictions.get(
                    "winner"
                )

                winner_name = "No clear winner"

                if isinstance(
                    winner,
                    dict
                ):

                    winner_name = (
                        winner.get(
                            "name"
                        )
                        or
                        "No clear winner"
                    )

                advice = predictions.get(
                    "advice"
                )

                results.append(
                    f"⚽ {home_name} vs "
                    f"{away_name}\n\n"
                    f"🏠 Home: {home}\n"
                    f"🤝 Draw: {draw}\n"
                    f"✈️ Away: {away}\n\n"
                    f"🥇 Predicted: "
                    f"{winner_name}\n"
                    f"💡 Advice: "
                    f"{advice or 'None'}"
                )

            except Exception as e:

                logging.warning(
                    "Prediction failed "
                    "for %s: %s",
                    fixture_id,
                    e
                )

                results.append(
                    f"⚽ {home_name} vs "
                    f"{away_name}\n\n"
                    f"❌ Prediction unavailable."
                )

        # --------------------------------------------------
        # SEND RESULTS
        # --------------------------------------------------

        message = (
            f"🏆 {league_name}\n\n"
        )

        for result in results:

            if len(
                message
            ) + len(result) > 3800:

                await query.message.reply_text(
                    message
                )

                message = ""

            message += (
                result +
                "\n\n"
            )

        if message:

            await query.message.reply_text(
                message
            )

    except Exception as e:

        logging.exception(e)

        await query.edit_message_text(
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

    app.add_handler(
        CallbackQueryHandler(
            date_selected,
            pattern="^date_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            league_selected,
            pattern="^league_"
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
