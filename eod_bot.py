from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# =========================================
# PROFESSIONAL IMAGE DASHBOARD — PART 1
# =========================================

WIDTH = 1080
HEIGHT = 1600

BG = (248, 249, 252)          # Premium light background
NAVY = (10, 25, 90)           # Brand dark blue
YELLOW = (255, 196, 0)        # Brand yellow
GREEN = (0, 170, 80)
RED = (220, 53, 69)
CYAN = (0, 180, 255)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)
BORDER = (220, 225, 235)

OUTPUT = "dashboard_part1.png"

# =========================================
# SAMPLE DATA
# =========================================

data = {
    "date": "18 April 2026",
    "nifty": "24,315",
    "banknifty": "52,840",
    "sensex": "80,218",

    "top_volume": [
        ("RELIANCE", "4.2 Cr"),
        ("SBIN", "3.8 Cr"),
        ("BEL", "3.1 Cr"),
        ("TATA MOTORS", "2.9 Cr"),
        ("IRFC", "2.6 Cr")
    ],

    "delivery": [
        ("BEL", "78%"),
        ("IRCTC", "74%"),
        ("HAL", "71%"),
        ("BHEL", "69%"),
        ("COAL INDIA", "67%")
    ],

    "call_oi": [
        ("24500 CE", "1.82 Cr"),
        ("24600 CE", "1.35 Cr"),
        ("24700 CE", "95 L")
    ],

    "put_oi": [
        ("24000 PE", "2.10 Cr"),
        ("24100 PE", "1.64 Cr"),
        ("24200 PE", "1.12 Cr")
    ],

    "fii": "+2,350 Cr",
    "dii": "-1,120 Cr"
}

# =========================================
# FONT LOADER
# =========================================

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

TITLE = get_font(42, True)
SUB = get_font(30, True)
TEXT = get_font(24)
TEXT_BOLD = get_font(24, True)
SMALL = get_font(20)

# =========================================
# BASE IMAGE
# =========================================

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

# =========================================
# HELPERS
# =========================================

def box(x, y, w, h, title, color):
    draw.rounded_rectangle(
        (x, y, x+w, y+h),
        radius=18,
        fill=WHITE,
        outline=BORDER,
        width=2
    )

    draw.rounded_rectangle(
        (x, y, x+w, y+60),
        radius=18,
        fill=NAVY
    )

    draw.rectangle((x, y+42, x+w, y+60), fill=NAVY)

    draw.rectangle((x, y, x+12, y+60), fill=color)

    draw.text(
        (x+30, y+14),
        title,
        font=SUB,
        fill=WHITE
    )


def row(y, left, right, right_color=BLACK):
    draw.text((60, y), left, font=TEXT_BOLD, fill=BLACK)
    draw.text((900, y), right, font=TEXT_BOLD, fill=right_color)


# =========================================
# HEADER
# =========================================

draw.rounded_rectangle(
    (20, 20, 1060, 110),
    radius=20,
    fill=YELLOW
)

draw.text(
    (250, 40),
    "PRICE ACTION TELUGU",
    font=TITLE,
    fill=NAVY
)

draw.text(
    (40, 140),
    "Institutional Smart Money Report",
    font=TEXT,
    fill=BLACK
)

draw.rounded_rectangle(
    (780, 130, 1040, 180),
    radius=12,
    fill=YELLOW
)

draw.text(
    (830, 142),
    data["date"],
    font=TEXT_BOLD,
    fill=NAVY
)

# =========================================
# INDEX SNAPSHOT
# =========================================

y = 220
box(20, y, 1040, 220, "INDEX SNAPSHOT", CYAN)

draw.text((70, y+90), f"NIFTY 50     {data['nifty']} 🟢", font=TEXT_BOLD, fill=GREEN)
draw.text((70, y+135), f"BANK NIFTY   {data['banknifty']} 🟢", font=TEXT_BOLD, fill=GREEN)
draw.text((70, y+180), f"SENSEX       {data['sensex']} 🟢", font=TEXT_BOLD, fill=GREEN)

# =========================================
# TOP VOLUME
# =========================================

y = 480
box(20, y, 1040, 300, "TOP 5 HIGHEST VOLUME", YELLOW)

yy = y + 90
for stock, vol in data["top_volume"]:
    row(yy, stock, vol, NAVY)
    yy += 42

# =========================================
# DELIVERY %
# =========================================

y = 820
box(20, y, 1040, 300, "TOP 5 HIGHEST DELIVERY %", GREEN)

yy = y + 90
for stock, val in data["delivery"]:
    row(yy, stock, val, GREEN)
    yy += 42

# =========================================
# OI LEVELS
# =========================================

y = 1160
box(20, y, 1040, 320, "OPEN INTEREST LEVELS", RED)

draw.text((60, y+90), "CALL OI — Resistance", font=TEXT_BOLD, fill=RED)
draw.text((580, y+90), "PUT OI — Support", font=TEXT_BOLD, fill=GREEN)

yy = y + 140
for i in range(3):
    draw.text((60, yy), f"{data['call_oi'][i][0]}   {data['call_oi'][i][1]}", font=TEXT, fill=BLACK)
    draw.text((580, yy), f"{data['put_oi'][i][0]}   {data['put_oi'][i][1]}", font=TEXT, fill=BLACK)
    yy += 45

# =========================================
# FOOTER
# =========================================

draw.rounded_rectangle(
    (0, 1520, WIDTH, 1600),
    radius=0,
    fill=NAVY
)

draw.text(
    (220, 1545),
    "Follow @PriceActionTelugu for Daily Updates",
    font=TEXT_BOLD,
    fill=YELLOW
)

# =========================================
# SAVE
# =========================================

img.save(OUTPUT)
print("Professional dashboard created:", OUTPUT)
