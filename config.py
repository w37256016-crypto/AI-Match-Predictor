import os

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# API-Football Key
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# API Base URL
API_BASE_URL = "https://v3.football.api-sports.io"

# Check required variables
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is missing.")

if not API_FOOTBALL_KEY:
    raise ValueError("API_FOOTBALL_KEY environment variable is missing.")
