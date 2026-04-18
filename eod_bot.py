import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =====================================
# CONFIG
# =====================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@priceactiontelugu"

TELEGRAM_PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

OUTPUT_IMAGE = "eod_report.png"

# =====================================
# SAMPLE DATA (replace later with Dhan API)
# =====================================

report_data = {
    "date": datetime.now().strftime("%d %B %Y"),
    "nifty": "24,315",
    "banknifty": "52,840",
    "sensex": "80,218",
    "call_oi": [
        "24500 CE",
        "24600 CE",
        "24700 CE"
    ],
    "put_oi": [
        "24000 PE",
        "24100 PE",
        "24200 PE"
    ],
    "top_volume": [
        "RELIANCE",
        "SBIN",
        "BEL",
        "TATA MOTORS",
        "IRFC"
    ],
    "fii": "FII Net Buy 🟢",
    "dii": "DII Net Sell 🔴"
}

# =====================================
# IMAGE GENERATOR
# =====================================

def create_dashboard_image(data):
    width = 1080
    height = 1350

    bg_color = (245, 247, 252)
    navy = (12, 25, 82)
    yellow = (255, 204, 0)
    green = (0, 153, 76)
    red = (220, 53, 69)
    black = (20, 20, 20)

    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        section_font = ImageFont.truetype("arial.ttf", 34)
        text_font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        section_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Header
    draw.rectangle((0, 0, width, 110), fill=navy)
    draw.text((40, 25), "PRICE ACTION TELUGU", fill=yellow, font=title_font)

    # Date
    draw.text((40, 140), f"Institutional Smart Money Report", fill=black, font=section_font)
    draw.text((40, 190), f"Date: {data['date']}", fill=black, font=text_font)

    y = 270

    # Index Snapshot
    draw.text((40, y), "INDEX SNAPSHOT", fill=navy, font=section_font)
    y += 60

    draw.text((60, y), f"NIFTY 50 → {data['nifty']} 🟢", fill=green, font=text_font)
    y += 45
    draw.text((60, y), f"BANK NIFTY → {data['banknifty']} 🟢", fill=green, font=text_font)
    y += 45
    draw.text((60, y), f"SENSEX → {data['sensex']} 🟢", fill=green, font=text_font)

    y += 90

    # Call OI
    draw.text((40, y), "CALL OI RESISTANCE", fill=red, font=section_font)
    y += 55

    for item in data["call_oi"]:
        draw.text((60, y), item, fill=black, font=text_font)
        y += 40

    y += 40

    # Put OI
    draw.text((40, y), "PUT OI SUPPORT", fill=green, font=section_font)
    y += 55

    for item in data["put_oi"]:
        draw.text((60, y), item, fill=black, font=text_font)
        y += 40

    y += 40

    # Top Volume
    draw.text((40, y), "TOP VOLUME STOCKS", fill=navy, font=section_font)
    y += 55

    for item in data["top_volume"]:
        draw.text((60, y), item, fill=black, font=text_font)
        y += 40

    y += 50

    # FII DII
    draw.text((40, y), "FII / DII DATA", fill=navy, font=section_font)
    y += 60

    draw.text((60, y), data["fii"], fill=green, font=text_font)
    y += 45
    draw.text((60, y), data["dii"], fill=red, font=text_font)

    y += 80

    draw.line((40, y, 1040, y), fill=navy, width=3)
    y += 30

    draw.text((40, y), "Follow @PriceActionTelugu for Daily Institutional Reports", fill=navy, font=small_font)

    image.save(OUTPUT_IMAGE)
    print("Image created successfully")


# =====================================
# TELEGRAM PHOTO SENDER
# =====================================

def send_photo_to_telegram():
    with open(OUTPUT_IMAGE, "rb") as photo:
        files = {
            "photo": photo
        }

        data = {
            "chat_id": CHAT_ID,
            "caption": "📊 Institutional Smart Money Report"
        }

        response = requests.post(
            TELEGRAM_PHOTO_URL,
            data=data,
            files=files
        )

        print(response.text)


# =====================================
# RUN
# =====================================

if __name__ == "__main__":
    create_dashboard_image(report_data)
    send_photo_to_telegram()
