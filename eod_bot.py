# ADVANCED PREMIUM INSTITUTIONAL DASHBOARD
# PRICE ACTION TELUGU — TELEGRAM EOD REPORT (2 IMAGE STYLE)

import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@priceactionoptions"

DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID", "1100484167")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

WIDTH = 1080
HEIGHT = 1900

# =========================================================
# COLORS (PREMIUM LIGHT THEME)
# =========================================================

NAVY = (12, 28, 92)
YELLOW = (255, 196, 0)
GREEN = (0, 170, 90)
RED = (220, 45, 45)
CYAN = (0, 190, 220)
PURPLE = (130, 90, 255)
LIGHT_BG = (248, 249, 252)
WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
GRAY = (110, 110, 110)
BORDER = (225, 230, 240)

# =========================================================
# FONT LOADER
# =========================================================

def font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

TITLE = font(42, True)
HEAD = font(30, True)
SUB = font(24, True)
TXT = font(22)
BOLD = font(22, True)
SMALL = font(18)

# =========================================================
# SAMPLE DATA (replace later with live Dhan API)
# =========================================================

def get_data():
    return {
        "date": datetime.now().strftime("%d %B %Y"),

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
            ("24700 CE", "95 L"),
        ],

        "put_oi": [
            ("24000 PE", "2.10 Cr"),
            ("24100 PE", "1.64 Cr"),
            ("24200 PE", "1.12 Cr"),
        ],

        "bulk_deals": [
            ("RELIANCE", "Institutional Buy"),
            ("INFY", "Fund Activity"),
            ("BEL", "Large Accumulation"),
            ("LT", "Bulk Buying"),
            ("HDFCLIFE", "Promoter Activity"),
        ],

        "fii": "+₹2,350 Cr",
        "dii": "-₹1,120 Cr",

        "summary":
        "Institutions accumulating Defence & PSU stocks. "
        "FII net buyers in IT. Watch BEL & HAL for continuation tomorrow.",

        "bias":
        "Buy on dips near 24,150 | Resistance near 24,500"
    }

# =========================================================
# SECTION BLOCK
# =========================================================

def section(draw, y, title, strip_color):
    draw.rounded_rectangle((30, y, 1050, y + 60), radius=14, fill=NAVY)
    draw.rectangle((30, y, 45, y + 60), fill=strip_color)
    draw.text((65, y + 14), title, font=HEAD, fill=WHITE)
    return y + 80

# =========================================================
# SIMPLE ROW
# =========================================================

def row(draw, y, left, right, color=BLACK):
    draw.text((60, y), left, font=BOLD, fill=BLACK)
    draw.text((820, y), right, font=BOLD, fill=color)
    return y + 42

# =========================================================
# IMAGE 1
# =========================================================

def create_page_1(data):
    img = Image.new("RGB", (WIDTH, HEIGHT), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    # HEADER
    draw.rounded_rectangle((20, 20, 1060, 100), radius=20, fill=YELLOW)
    draw.text((250, 38), "PRICE ACTION TELUGU", font=TITLE, fill=NAVY)

    draw.text((40, 135), "Institutional Smart Money Report", font=HEAD, fill=BLACK)
    draw.text((40, 180), f"Date: {data['date']}", font=TXT, fill=BLACK)

    y = 250

    # INDEX
    y = section(draw, y, "INDEX SNAPSHOT", CYAN)
    y = row(draw, y, "NIFTY 50", data["nifty"], GREEN)
    y = row(draw, y, "BANK NIFTY", data["banknifty"], GREEN)
    y = row(draw, y, "SENSEX", data["sensex"], GREEN)

    y += 30

    # TOP VOLUME
    y = section(draw, y, "TOP 5 HIGHEST VOLUME", YELLOW)
    for s, v in data["top_volume"]:
        y = row(draw, y, s, v, NAVY)

    y += 20

    # DELIVERY
    y = section(draw, y, "TOP 5 HIGHEST DELIVERY %", GREEN)
    for s, v in data["delivery"]:
        y = row(draw, y, s, v, GREEN)

    y += 20

    # CALL OI
    y = section(draw, y, "CALL OI — RESISTANCE ZONE", RED)
    for s, v in data["call_oi"]:
        y = row(draw, y, s, v, RED)

    y += 20

    # PUT OI
    y = section(draw, y, "PUT OI — SUPPORT ZONE", GREEN)
    for s, v in data["put_oi"]:
        y = row(draw, y, s, v, GREEN)

    img.save("report_page_1.png")
    return "report_page_1.png"

# =========================================================
# IMAGE 2
# =========================================================

def create_page_2(data):
    img = Image.new("RGB", (WIDTH, HEIGHT), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((20, 20, 1060, 100), radius=20, fill=YELLOW)
    draw.text((250, 38), "PRICE ACTION TELUGU", font=TITLE, fill=NAVY)

    draw.text((40, 135), "Institutional Smart Money Report", font=HEAD, fill=BLACK)
    draw.text((40, 180), f"Date: {data['date']}", font=TXT, fill=BLACK)

    y = 250

    # BULK DEALS
    y = section(draw, y, "TOP BULK / BLOCK DEALS", PURPLE)
    for s, v in data["bulk_deals"]:
        y = row(draw, y, s, v, NAVY)

    y += 30

    # FII DII
    y = section(draw, y, "FII / DII DATA", YELLOW)
    y = row(draw, y, "FII Net Buy / Sell", data["fii"], GREEN)
    y = row(draw, y, "DII Net Buy / Sell", data["dii"], RED)

    y += 40

    # SUMMARY
    y = section(draw, y, "SMART MONEY SUMMARY", CYAN)

    draw.rounded_rectangle((50, y, 1030, y + 180), radius=16, fill=WHITE)
    draw.text((80, y + 30), data["summary"], font=TXT, fill=BLACK)
    y += 220

    # TOMORROW BIAS
    y = section(draw, y, "TOMORROW'S BIAS", GREEN)

    draw.rounded_rectangle((50, y, 1030, y + 130), radius=16, fill=WHITE)
    draw.text((80, y + 40), data["bias"], font=SUB, fill=NAVY)
    y += 180

    # FOOTER
    draw.line((60, y, 1020, y), fill=BORDER, width=2)
    draw.text(
        (150, y + 40),
        "Follow @PriceActionTelugu | For Educational Purposes Only",
        font=TXT,
        fill=NAVY
    )

    img.save("report_page_2.png")
    return "report_page_2.png"

# =========================================================
# TELEGRAM POST
# =========================================================

def send_photo(path, caption=""):
    try:
        with open(path, "rb") as f:
            response = requests.post(
                TELEGRAM_URL,
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption
                },
                files={
                    "photo": f
                },
                timeout=30
            )

        print(response.text)

    except Exception as e:
        print("Telegram Error:", str(e))

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    data = get_data()

    page1 = create_page_1(data)
    page2 = create_page_2(data)

    send_photo(page1, "📊 Institutional Smart Money Report — Part 1")
    send_photo(page2, "📊 Institutional Smart Money Report — Part 2")
