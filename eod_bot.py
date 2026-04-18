import os
import requests
from datetime import datetime

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@priceactionoptions"   # replace with your Telegram channel username if needed

DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id": DHAN_CLIENT_ID,
    "Content-Type": "application/json"
}

# =========================
# TELEGRAM SEND FUNCTION
# =========================

def send_telegram_message(message):
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(TELEGRAM_URL, json=payload)
    print(response.text)


# =========================
# SAMPLE DATA FETCH
# (Starter version using stable structure)
# =========================

def get_market_report():
    today = datetime.now().strftime("%d %B %Y")

    # Initial production-safe starter report
    # We will connect deeper Dhan endpoints next step

    message = f"""
📊 <b>PRICE ACTION TELUGU</b>

🏛 <b>Institutional Smart Money Report</b>
📅 {today}

━━━━━━━━━━━━━━━

📌 <b>INDEX SNAPSHOT</b>

NIFTY 50 → 24,315 🟢
BANK NIFTY → 52,840 🟢
SENSEX → 80,218 🟢

━━━━━━━━━━━━━━━

🔴 <b>CALL OI RESISTANCE</b>

24500 CE
24600 CE
24700 CE

━━━━━━━━━━━━━━━

🟢 <b>PUT OI SUPPORT</b>

24000 PE
24100 PE
24200 PE

━━━━━━━━━━━━━━━

📈 <b>TOP VOLUME STOCKS</b>

RELIANCE
SBIN
BEL
TATA MOTORS
IRFC

━━━━━━━━━━━━━━━

💰 <b>FII / DII DATA</b>

FII Net Buy 🟢
DII Net Sell 🔴

━━━━━━━━━━━━━━━

⚡ <b>TOMORROW BIAS</b>

Buy on Dips near Support

━━━━━━━━━━━━━━━

Follow @PriceActionTelugu
"""

    return message


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    report = get_market_report()
    send_telegram_message(report)
