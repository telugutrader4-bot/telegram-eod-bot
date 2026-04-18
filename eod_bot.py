import os
import time
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =====================================================
# PRICE ACTION TELUGU — CLEAN WORKING EOD IMAGE BOT
# =====================================================

# -----------------------------
# CONFIG
# -----------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@priceactionoptions"

DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID", "1100484167")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# -----------------------------
# FALLBACK SAMPLE DATA
# (safe starter version)
# -----------------------------

def get_report_data():
    today = datetime.now().strftime("%d %B %Y")

    return {
        "date": today,
        "nifty": "24,315",
        "banknifty": "52,840",
        "sensex": "80,218",

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
            ("56000 CE", "95 L"),
        ],

        "put_oi": [
            ("24000 PE", "2.10 Cr"),
            ("24100 PE", "1.64 Cr"),
            ("55000 PE", "1.12 Cr"),
        ],

        "fii": "+₹2,350 Cr",
        "dii": "-₹1,120 Cr",
    }

# -----------------------------
# FONT
# -----------------------------

def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

TITLE_FONT = load_font(40, True)
SUB_FONT = load_font(28, True)
TEXT_FONT = load_font(22)
BOLD_FONT = load_font(22, True)

# -----------------------------
# IMAGE GENERATOR
# -----------------------------

def create_dashboard_image(data):
    width = 1080
    height = 1700

    bg = (248, 249, 252)
    navy = (10, 25, 90)
    yellow = (255, 196, 0)
    green = (0, 160, 80)
    red = (210, 45, 45)
    white = (255, 255, 255)
    black = (20, 20, 20)
    border = (220, 225, 235)

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rounded_rectangle((20, 20, 1060, 110), radius=20, fill=yellow)
    draw.text((250, 40), "PRICE ACTION TELUGU", font=TITLE_FONT, fill=navy)

    draw.text((40, 140), "Institutional Smart Money Report", font=SUB_FONT, fill=black)
    draw.text((40, 185), f"Date: {data['date']}", font=TEXT_FONT, fill=black)

    y = 250

    def section(title, color):
        nonlocal y
        draw.rounded_rectangle((30, y, 1050, y + 55), radius=12, fill=navy)
        draw.rectangle((30, y, 45, y + 55), fill=color)
        draw.text((65, y + 13), title, font=SUB_FONT, fill=white)
        y += 75

    def row(left, right, right_color=black):
        nonlocal y
        draw.text((60, y), left, font=BOLD_FONT, fill=black)
        draw.text((850, y), right, font=BOLD_FONT, fill=right_color)
        y += 38

    # Index
    section("INDEX SNAPSHOT", yellow)
    row("NIFTY 50", data["nifty"], green)
    row("BANK NIFTY", data["banknifty"], green)
    row("SENSEX", data["sensex"], green)

    y += 20

    # Volume
    section("TOP 5 HIGHEST VOLUME", yellow)
    for stock, vol in data["top_volume"]:
        row(stock, vol, navy)

    y += 20

    # Delivery
    section("TOP 5 HIGHEST DELIVERY %", green)
    for stock, val in data["delivery"]:
        row(stock, val, green)

    y += 20

    # Call OI
    section("CALL OI RESISTANCE", red)
    for strike, oi in data["call_oi"]:
        row(strike, oi, red)

    y += 20

    # Put OI
    section("PUT OI SUPPORT", green)
    for strike, oi in data["put_oi"]:
        row(strike, oi, green)

    y += 20

    # FII DII
    section("FII / DII DATA", yellow)
    row("FII Net", data["fii"], green)
    row("DII Net", data["dii"], red)

    # Footer
    draw.line((40, 1560, 1040, 1560), fill=border, width=2)
    draw.text(
        (180, 1600),
        "Follow @PriceActionTelugu | For Educational Purposes Only",
        font=TEXT_FONT,
        fill=navy
    )

    file_name = "eod_report.png"
    img.save(file_name)
    return file_name

# -----------------------------
# TELEGRAM SENDER
# -----------------------------

def send_photo(image_path):
    try:
        with open(image_path, "rb") as photo:
            response = requests.post(
                TELEGRAM_URL,
                data={
                    "chat_id": CHAT_ID,
                    "caption": "📊 PRICE ACTION TELUGU — Institutional Smart Money Report"
                },
                files={
                    "photo": photo
                },
                timeout=30
            )

        print(response.text)

    except Exception as e:
        print("Telegram Error:", str(e))

# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    data = get_report_data()
    image_path = create_dashboard_image(data)
    send_photo(image_path)
