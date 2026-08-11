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

# Number of leagues displayed per page
LEAGUES_PER_PAGE = 8

# Maximum matches predicted at once
MAX_MATCHES = 8


# ==================================================
# START
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/predict - Get football predictions\n"
        "/help - Show help"
    )


# ==================================================
# HELP
# ==================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 AI Match Predictor Bot\n\n"
        "/predict - Choose Today, Tomorrow or Weekend "
        "and then select a league."
    )


# ==================================================
# PREDICT
# ==================================================

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==================================================
# GET DATES
# ==================================================

def get_dates(date_type):

    today = datetime.now().date()

    if date_type == "today":

        return [today]

    if date_type == "tomorrow":

        return [
            today + timedelta(days=1)
        ]

    # Weekend
    days_until_saturday = (
        5 - today.weekday()
    ) % 7

    saturday = today + timedelta(
        days=days_until_saturday
    )

    sunday = saturday + timedelta(
        days=1
    )

    return [
        saturday,
        sunday
    ]


# ==================================================
# DATE SELECTED
# ==================================================

async def date_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    date_type = query.data.replace(
        "date_",
        ""
    )

    try:

        await query.edit_message_text(
            "🔎 Finding matches...\n\n"
            "⏳ Please wait."
        )

        api = FootballAPI()

        dates = get_dates(
            date_type
        )

        fixtures = []

        for date in dates:

            date_string = date.strftime(
                "%Y-%m-%d"
            )

            data = api.get_fixtures_by_date(
                date_string
            )

            fixtures.extend(
                data.get(
                    "response",
                    []
                )
            )

        if not fixtures:

            await query.edit_message_text(
                "⚠️ No matches found."
            )

            return

        # Store fixtures
        context.user_data[
            "selected_fixtures"
        ] = fixtures

        context.user_data[
            "selected_date_type"
        ] = date_type

        # Build league dictionary
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

            country = league.get(
                "country",
                ""
            )

            if league_id is not None:

                if league_id not in leagues:

                    leagues[league_id] = {
                        "name": league_name,
                        "country": country,
                        "matches": 0
                    }

                leagues[
                    league_id
                ][
                    "matches"
                ] += 1

        # Sort leagues by number of matches
        league_list = sorted(
            leagues.items(),
            key=lambda x: (
                -x[1]["matches"],
                x[1]["name"]
            )
        )

        context.user_data[
            "league_list"
        ] = league_list

        context.user_data[
            "league_page"
        ] = 0

        await show_league_page(
            query,
            context
        )

    except Exception as e:

        logging.exception(e)

        await query.edit_message_text(
            f"❌ Could not load matches:\n{e}"
        )


# ==================================================
# SHOW LEAGUE PAGE
# ==================================================

async def show_league_page(
    query,
    context
):

    league_list = context.user_data.get(
        "league_list",
        []
    )

    page = context.user_data.get(
        "league_page",
        0
    )

    if not league_list:

        await query.edit_message_text(
            "⚠️ No leagues found."
        )

        return

    total_pages = (
        len(league_list)
        + LEAGUES_PER_PAGE
        - 1
    ) // LEAGUES_PER_PAGE

    start_index = (
        page * LEAGUES_PER_PAGE
    )

    end_index = (
        start_index
        + LEAGUES_PER_PAGE
    )

    current_leagues = league_list[
        start_index:end_index
    ]

    keyboard = []

    for league_id, info in current_leagues:

        name = info["name"]
        matches = info["matches"]
        country = info["country"]

        if country:

            button_text = (
                f"🏆 {name} "
                f"({matches})"
            )

        else:

            button_text = (
                f"🏆 {name} "
                f"({matches})"
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    button_text,
                    callback_data=(
                        f"league_{league_id}"
                    )
                )
            ]
        )

    # Navigation buttons
    navigation = []

    if page > 0:

        navigation.append(
            InlineKeyboardButton(
                "⬅️ Previous",
                callback_data="league_prev"
            )
        )

    if page < total_pages - 1:

        navigation.append(
            InlineKeyboardButton(
                "Next ➡️",
                callback_data="league_next"
            )
        )

    if navigation:

        keyboard.append(
            navigation
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 Back to Dates",
                callback_data="back_dates"
            )
        ]
    )

    date_type = context.user_data.get(
        "selected_date_type",
        "today"
    )

    if date_type == "today":
        title = "Today's"

    elif date_type == "tomorrow":
        title = "Tomorrow's"

    else:
        title = "Weekend"

    await query.edit_message_text(
        f"🏆 {title} Matches\n\n"
        f"⚽ {len(context.user_data['selected_fixtures'])} "
        f"total matches\n\n"
        f"Choose a league:\n\n"
        f"📄 Page {page + 1} of {total_pages}",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# ==================================================
# LEAGUE NAVIGATION
# ==================================================

async def league_navigation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    page = context.user_data.get(
        "league_page",
        0
    )

    if query.data == "league_next":

        page += 1

    elif query.data == "league_prev":

        page -= 1

    page = max(
        0,
        page
    )

    context.user_data[
        "league_page"
    ] = page

    await show_league_page(
        query,
        context
    )


# ==================================================
# BACK TO DATES
# ==================================================

async def back_to_dates(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

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

    await query.edit_message_text(
        "📅 Choose when you want predictions:",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# ==================================================
# LEAGUE SELECTED
# ==================================================

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
            ).get("id") == league_id
        ]

        if not selected:

            await query.edit_message_text(
                "⚠️ No matches found "
                "for this league."
            )

            return

        league_name = selected[0][
            "league"
        ][
            "name"
        ]

        # Protect the Free API quota
        prediction_fixtures = selected[
            :MAX_MATCHES
        ]

        await query.edit_message_text(
            f"🏆 {league_name}\n\n"
            f"⚽ {len(selected)} matches found.\n\n"
            f"🧠 Predicting up to "
            f"{len(prediction_fixtures)} "
            f"matches...\n\n"
            f"⏳ Please wait."
        )

        api = FootballAPI()

        results = []

        for fixture in prediction_fixtures:

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

                winner_name = (
                    "No clear winner"
                )

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
                    "for fixture %s: %s",
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

        if len(selected) > MAX_MATCHES:

            message += (
                f"ℹ️ This league has "
                f"{len(selected)} matches.\n"
                f"Showing the first "
                f"{MAX_MATCHES} for now.\n\n"
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


# ==================================================
# MAIN
# ==================================================

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

    # Date buttons
    app.add_handler(
        CallbackQueryHandler(
            date_selected,
            pattern="^date_"
        )
    )

    # League navigation
    app.add_handler(
        CallbackQueryHandler(
            league_navigation,
            pattern="^league_(next|prev)$"
        )
    )

    # Back button
    app.add_handler(
        CallbackQueryHandler(
            back_to_dates,
            pattern="^back_dates$"
        )
    )

    # League selection
    app.add_handler(
        CallbackQueryHandler(
            league_selected,
            pattern="^league_[0-9]+$"
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
