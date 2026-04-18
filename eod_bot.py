# eod_bot.py
# PRICE ACTION TELUGU — Efficient Production EOD Bot
# Real structure ready for Dhan + Telegram + Premium Dashboard

import os
import time
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =====================================================
# CONFIG
# =====================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@priceactionoptions"   # safer later: use numeric channel ID

DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID", "1100484167")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN missing in GitHub Secrets")

if not DHAN_ACCESS_TOKEN:
    raise Exception("DHAN_ACCESS_TOKEN missing in GitHub Secrets")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

DHAN_HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id": DHAN_CLIENT_ID,
    "Content-Type": "application/json"
}

# =====================================================
# SAFE API FETCH (REAL DATA PLACEHOLDER)
# Replace endpoint URLs with your exact Dhan endpoints
# =====================================================

def safe_get(url):
    try:
        r = requests.get(url, headers=DHAN_HEADERS, timeout=20)
        print("API:", r.status_code, url)

        if r.status_code == 200:
            return r.json()

        print("API Failed:", r.text)
        return None

    except Exception as e:
        print("API Error:", str(e))
        return None


def get_report_data():
    """
    Replace below URLs with actual Dhan endpoints
    """

    today = datetime.now().strftime("%d %B %Y")

    # Example structure
    # index_data = safe_get("https://api.dhan.co/market/index")
    # oi_data = safe_get("https://api.dhan.co/options/oi")
    # volume_data = safe_get("https://api.dhan.co/market/volume")

    # Temporary production-safe fallback
    return {
        "date": today,

        "indices": [
            ("NIFTY 50", "24,315", "+0.82%"),
            ("BANK NIFTY", "52,840", "+1.14%"),
            ("SENSEX", "80,218", "+0.79%"),
        ],

        "top_volume": [
            ("RELIANCE", "4.2 Cr"),
            ("SBIN", "3.8 Cr"),
            ("BEL", "3.1 Cr"),
            ("TATA MOTORS", "2.9 Cr"),
            ("IRFC", "2.6 Cr"),
        ],

        "delivery": [
            ("BEL", "78%"),
            ("IRCTC", "74%"),
            ("HAL", "71%"),
            ("BHEL", "69%"),
            ("COAL INDIA", "67%"),
        ],

        "call_oi": [
            ("24500 CE", "1.82 Cr"),
            ("24600 CE", "1.35 Cr"),
            ("24700 CE", "95 L"),
        ],

        "put_oi": [
            ("24000 PE", "2.10 Cr"),
            ("24100 PE", "1.64 Cr"),
            ("24200 PE", "1.12 Cr"),
        ],

        "fii": "+₹2,350 Cr",
        "dii": "-₹1,120 Cr"
    }

# =====================================================
# FONT
# =====================================================

def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

TITLE = load_font(38, True)
HEAD = load_font(26, True)
TEXT = load_font(20)
BOLD = load_font(20, True)

# =====================================================
# IMAGE BUILDER (Professional Clean)
# =====================================================

def create_dashboard(data):
    width = 1080
    height = 1500

    WHITE = (248, 249, 252)
    NAVY = (10, 25, 90)
    YELLOW = (255, 196, 0)
    GREEN = (0, 160, 80)
    RED = (210, 40, 40)
    BLACK = (20, 20, 20)

    img = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rounded_rectangle((20, 20, 1060, 100), radius=20, fill=YELLOW)
    draw.text((230, 38), "PRICE ACTION TELUGU", font=TITLE, fill=NAVY)

    draw.text((40, 130), "Institutional Smart Money Report", font=HEAD, fill=BLACK)
    draw.text((40, 170), f"Date: {data['date']}", font=TEXT, fill=BLACK)

    y = 240

    def section(title):
        nonlocal y
        draw.rounded_rectangle((30, y, 1050, y + 50), radius=10, fill=NAVY)
        draw.text((60, y + 12), title, font=HEAD, fill=(255,255,255))
        y += 70

    def row(left, right):
        nonlocal y
        draw.text((60, y), left, font=BOLD, fill=BLACK)
        draw.text((820, y), right, font=BOLD, fill=NAVY)
        y += 36

    section("INDEX SNAPSHOT")
    for name, value, chg in data["indices"]:
        row(name, f"{value}  {chg}")

    y += 20

    section("TOP 5 HIGHEST VOLUME")
    for s, v in data["top_volume"]:
        row(s, v)

    y += 20

    section("TOP 5 DELIVERY %")
    for s, v in data["delivery"]:
        row(s, v)

    y += 20

    section("CALL OI RESISTANCE")
    for s, v in data["call_oi"]:
        row(s, v)

    y += 20

    section("PUT OI SUPPORT")
    for s, v in data["put_oi"]:
        row(s, v)

    y += 20

    section("FII / DII DATA")
    row("FII Net", data["fii"])
    row("DII Net", data["dii"])

    file_name = "eod_report.png"
    img.save(file_name, "PNG", optimize=True)
    return file_name

# =====================================================
# TELEGRAM SEND
# =====================================================

def send_photo(path):
    try:
        with open(path, "rb") as f:
            r = requests.post(
                TELEGRAM_URL,
                data={
                    "chat_id": CHAT_ID,
                    "caption": "📊 PRICE ACTION TELUGU — EOD Institutional Dashboard"
                },
                files={
                    "photo": f
                },
                timeout=30
            )

        print("Telegram:", r.status_code, r.text)

    except Exception as e:
        print("Telegram Error:", str(e))

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("Starting EOD Bot...")

    data = get_report_data()
    image_path = create_dashboard(data)
    send_photo(image_path)

    print("Done.")
