# ═════════════════════════════════════
# CONFIG
# ═════════════════════════════════════

import os

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# Your PUBLIC Telegram Channel Username
# Your real channel is:
CHAT_ID = os.getenv("CHAT_ID", "@priceactionoptions")

# Dhan API Details
DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID", "1100484167")

DHAN_ACCESS_TOKEN = os.getenv(
    "DHAN_ACCESS_TOKEN",
    "YOUR_DHAN_ACCESS_TOKEN"
)

# Telegram API URL
TELEGRAM_PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# Dhan Headers
DHAN_HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id": DHAN_CLIENT_ID,
    "Content-Type": "application/json"
}
