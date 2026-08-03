from telegram import Update
from telegram.ext import ContextTypes

from prediction.predictor import get_predictions
from utils.formatter import format_predictions


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = get_predictions("today")
    await update.message.reply_text(format_predictions(matches))


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = get_predictions("tomorrow")
    await update.message.reply_text(format_predictions(matches))


async def weekend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = get_predictions("weekend")
    await update.message.reply_text(format_predictions(matches))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
Available commands:

/today
/tomorrow
/weekend
/help
"""
  )
