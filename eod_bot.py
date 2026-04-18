"""
PRICE ACTION TELUGU — Professional EOD Report Bot
File: eod_bot.py
Run: python eod_bot.py
Install: pip install pillow requests pytz
"""

import os, time, requests, pytz
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ═══════════════════════════════════════════
# INDIA TIMEZONE
# ═══════════════════════════════════════════
IST = pytz.timezone("Asia/Kolkata")
def now_ist():
    return datetime.now(IST)

# ═══════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════
BOT_TOKEN         = os.getenv("BOT_TOKEN")
CHAT_ID           = "@priceactionoptions"
DHAN_CLIENT_ID    = os.getenv("DHAN_CLIENT_ID", "1100484167")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
TELEGRAM_URL      = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# ═══════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════
def get_report_data():
    today = now_ist().strftime("%d %B %Y")
    return {
        "date": today,
        "indices": [
            {"name": "NIFTY 50",   "value": "24,315", "chg": "+0.82%"},
            {"name": "BANK NIFTY", "value": "52,840", "chg": "+1.14%"},
            {"name": "SENSEX",     "value": "80,218", "chg": "+0.79%"},
        ],
        "vix": "13.45", "pcr": "1.18", "adv_dec": "3 : 1",
        "advances": 1820, "declines": 620, "unchanged": 110,
        "gainers": [
            ("BEL",        "+5.2%"), ("HAL",      "+4.1%"),
            ("IRFC",       "+3.8%"), ("RECLTD",   "+3.2%"),
            ("TATA POWER", "+2.9%"),
        ],
        "losers": [
            ("HINDUNILVR", "-2.1%"), ("NESTLEIND", "-1.8%"),
            ("WIPRO",      "-1.5%"), ("TECHM",     "-1.2%"),
            ("DABUR",      "-0.9%"),
        ],
        "sectors": [
            ("DEFENCE",   "+3.4%"), ("PSU BANKS", "+2.1%"),
            ("METAL",     "+1.8%"), ("IT",        "-1.2%"),
            ("FMCG",      "-0.8%"), ("PHARMA",    "+0.5%"),
        ],
        "week52_high": [
            ("BEL",        "310.50", "311.00"),
            ("HAL",        "4,820",  "4,850"),
            ("IRFC",       "229.40", "230.00"),
            ("RECLTD",     "498.70", "500.00"),
            ("TATA POWER", "415.20", "416.50"),
        ],
        "week52_low": [
            ("HINDUNILVR", "2,190",  "2,180"),
            ("NESTLEIND",  "2,050",  "2,040"),
            ("WIPRO",      "442.30", "440.00"),
            ("TECHM",      "1,315",  "1,310"),
            ("DABUR",      "488.60", "485.00"),
        ],
        "top_volume": [
            ("RELIANCE",    "4.2 Cr"), ("SBIN",        "3.8 Cr"),
            ("BEL",         "3.1 Cr"), ("TATA MOTORS", "2.9 Cr"),
            ("IRFC",        "2.6 Cr"),
        ],
        "delivery": [
            ("BEL",        "78%"), ("IRCTC",      "74%"),
            ("HAL",        "71%"), ("BHEL",       "69%"),
            ("COAL INDIA", "67%"),
        ],
        "long_buildup": [
            ("BEL",        "+5.2%", "OI +18%"),
            ("HAL",        "+4.1%", "OI +14%"),
            ("RECLTD",     "+3.2%", "OI +12%"),
            ("IRFC",       "+3.8%", "OI +11%"),
            ("TATA POWER", "+2.9%", "OI  +9%"),
        ],
        "short_buildup": [
            ("HINDUNILVR", "-2.1%", "OI +16%"),
            ("NESTLEIND",  "-1.8%", "OI +13%"),
            ("WIPRO",      "-1.5%", "OI +11%"),
            ("TECHM",      "-1.2%", "OI  +8%"),
            ("DABUR",      "-0.9%", "OI  +7%"),
        ],
        "call_oi": [
            ("NIFTY  24500 CE", "1.82 Cr"), ("NIFTY  24600 CE", "1.35 Cr"),
            ("BNIFTY 56000 CE", "95 L"),    ("BNIFTY 56200 CE", "72 L"),
        ],
        "put_oi": [
            ("NIFTY  24000 PE", "2.10 Cr"), ("NIFTY  24100 PE", "1.64 Cr"),
            ("BNIFTY 55000 PE", "1.12 Cr"), ("BNIFTY 54800 PE", "88 L"),
        ],
        "key_levels": {
            "strong_res": "24,600", "resistance": "24,450",
            "ltp": "24,315", "support": "24,150", "strong_sup": "24,000",
        },
        "bulk_deals": [
            ("RELIANCE",  "Institutional Buy"),  ("INFY",    "Fund Activity"),
            ("BEL",       "Large Accumulation"), ("LT",      "Bulk Buying"),
            ("HDFCLIFE",  "Promoter Activity"),
        ],
        "fii": "+2,350",
        "dii": "-1,120",
    }

# ═══════════════════════════════════════════
# COLOR SYSTEM
# ═══════════════════════════════════════════
C_PAGE    = (243, 244, 249)
C_CARD    = (255, 255, 255)
C_CARD2   = (238, 240, 250)
C_HEADER  = (6,  13,  52)
C_SECTION = (11, 20,  68)
C_GOLD    = (218, 163,   0)
C_GOLD2   = (255, 200,   0)
C_CYAN    = (0,  165, 185)
C_GREEN   = (0,  145,  65)
C_RED     = (185,  28,  48)
C_ORANGE  = (200, 105,   0)
C_BLUE    = (25,   95, 185)
C_PURPLE  = (90,   55, 175)
C_TEAL    = (0,  130, 150)
C_TEXT    = (8,  14,  46)
C_MID     = (58,  68, 108)
C_DIM     = (128, 138, 168)
C_BORDER  = (208, 212, 232)
C_SHADOW  = (220, 223, 240)
C_LINE    = (195, 200, 225)
C_WHITE   = (255, 255, 255)

ACC = {
    "cyan": C_CYAN, "green": C_GREEN, "red": C_RED,
    "gold": C_GOLD, "blue": C_BLUE,   "purple": C_PURPLE,
    "teal": C_TEAL, "orange": C_ORANGE,
}

# ═══════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════
def _find(bold):
    paths = (
        ["DejaVuSans-Bold.ttf",
         "C:/Windows/Fonts/arialbd.ttf",
         "C:/Windows/Fonts/calibrib.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
        if bold else
        ["DejaVuSans.ttf",
         "C:/Windows/Fonts/arial.ttf",
         "C:/Windows/Fonts/calibri.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
    )
    for p in paths:
        try: ImageFont.truetype(p, 10); return p
        except: pass
    return None

_B, _N = _find(True), _find(False)

def F(size, bold=True):
    p = _B if bold else _N
    return ImageFont.truetype(p, size) if p else ImageFont.load_default()

# ═══════════════════════════════════════════
# DRAW HELPERS
# ═══════════════════════════════════════════
def rr(d, xy, r, fill, outline=None, ow=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=ow)

def ln(d, x1, y1, x2, y2, color=C_LINE, w=1):
    d.line([(x1, y1), (x2, y2)], fill=color, width=w)

def cx(d, text, font, y, x1, x2, color):
    bb = d.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    d.text((x1 + (x2 - x1 - tw) // 2, y), text, font=font, fill=color)

def rx(d, text, font, y, right_x, color):
    bb = d.textbbox((0, 0), text, font=font)
    d.text((right_x - (bb[2] - bb[0]), y), text, font=font, fill=color)

def shadow_card(d, xy, radius=10):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle([x1+2, y1+3, x2+2, y2+3], radius=radius, fill=C_SHADOW)
    rr(d, xy, radius, C_CARD, outline=C_BORDER, ow=1)

def dot_grid(img, W, H):
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 40):
        for gy in range(0, H, 40):
            d.ellipse([gx, gy, gx+1, gy+1], fill=(210, 214, 232))

def sec(d, y, title, accent_key, W, sub=None):
    ac = ACC.get(accent_key, C_CYAN)
    rr(d, [20, y, W-20, y+52], 10, C_SECTION)
    d.rectangle([20, y, 26, y+52], fill=ac)
    d.rectangle([42, y+20, 52, y+32], fill=ac)
    d.text((62, y+14), title, font=F(20), fill=C_WHITE)
    if sub:
        bb = d.textbbox((0, 0), sub, font=F(13, bold=False))
        d.text((W-40-(bb[2]-bb[0]), y+18), sub, font=F(13, bold=False), fill=C_DIM)
    return y + 60

def drow(d, y, label, value, W, vc=C_TEXT, alt=False):
    rr(d, [22, y, W-22, y+44], 6, C_CARD2 if alt else C_CARD, outline=C_BORDER, ow=1)
    d.text((44, y+12), label, font=F(17, bold=False), fill=C_TEXT)
    rx(d, value, F(17), y+12, W-40, vc)
    return y + 48

def page_header(d, W, part_label, subtitle, date):
    d.rectangle([0, 0, W, 182], fill=C_HEADER)
    d.rectangle([0, 0, W, 6],   fill=C_GOLD2)
    rr(d, [20, 18, W-20, 82], 12, C_GOLD2)
    cx(d, "PRICE ACTION TELUGU", F(36), 30, 20, W-20, C_HEADER)
    d.text((28, 94),  part_label, font=F(18, bold=False), fill=(190, 205, 255))
    d.text((28, 122), subtitle,   font=F(14, bold=False), fill=(140, 155, 200))
    rr(d, [W-210, 92, W-24, 130], 8, C_GOLD2)
    cx(d, date, F(16), 101, W-210, W-24, C_HEADER)
    d.rectangle([0, 177, W, 182], fill=C_CYAN)
    return 200

def page_footer(d, y, W, msg):
    d.rectangle([0, y, W, y+78], fill=C_HEADER)
    d.rectangle([0, y, W, y+5],  fill=C_GOLD2)
    cx(d, msg, F(17, bold=False), y+18, 0, W, C_GOLD2)
    ln(d, 40, y+48, W-40, y+48, (40, 55, 110), 1)
    cx(d, "For Educational Purposes Only   |   Not SEBI Registered Advice",
       F(13, bold=False), y+54, 0, W, (100, 115, 165))
    d.rectangle([0, y+74, W, y+78], fill=C_CYAN)
    return y + 80

# ═══════════════════════════════════════════
# IMAGE 1
# Index | Breadth | Gainers/Losers | Sectors | 52W
# ═══════════════════════════════════════════
def build_image1(data, W=1080):
    img = Image.new("RGB", (W, 4000), C_PAGE)
    dot_grid(img, W, 4000)
    d = ImageDraw.Draw(img)

    y = page_header(d, W,
        "INSTITUTIONAL SMART MONEY REPORT  —  PART 1 OF 2",
        "INDEX SNAPSHOT   /   GAINERS & LOSERS   /   SECTORS   /   52-WEEK HIGH & LOW",
        data["date"])

    # INDEX SNAPSHOT
    y = sec(d, y, "INDEX SNAPSHOT", "cyan", W)
    iw = (W - 60) // 3
    for i, idx in enumerate(data["indices"]):
        ix = 22 + i * (iw + 8)
        pos = not idx["chg"].startswith("-")
        col = C_GREEN if pos else C_RED
        shadow_card(d, [ix, y, ix+iw, y+108], radius=10)
        d.rounded_rectangle([ix, y, ix+iw, y+6], radius=5, fill=col)
        cx(d, idx["name"],  F(16, bold=False), y+18, ix, ix+iw, C_DIM)
        cx(d, idx["value"], F(32),             y+40, ix, ix+iw, C_TEXT)
        cx(d, idx["chg"],   F(20),             y+78, ix, ix+iw, col)
    y += 124

    # VIX / PCR / A-D
    mw = (W - 60) // 3
    for i, (lbl, val, col) in enumerate([
        ("INDIA VIX",      data["vix"],     C_ORANGE),
        ("PUT CALL RATIO",  data["pcr"],     C_PURPLE),
        ("ADV  /  DEC",     data["adv_dec"], C_CYAN),
    ]):
        mx = 22 + i * (mw + 8)
        shadow_card(d, [mx, y, mx+mw, y+78], radius=10)
        d.rounded_rectangle([mx, y, mx+mw, y+5], radius=4, fill=col)
        cx(d, lbl, F(13, bold=False), y+15, mx, mx+mw, C_DIM)
        cx(d, val, F(30),             y+36, mx, mx+mw, col)
    y += 96

    # MARKET BREADTH
    y = sec(d, y, "MARKET BREADTH", "green", W)
    adv, dec, unc = data["advances"], data["declines"], data["unchanged"]
    total = adv + dec + unc or 1
    shadow_card(d, [20, y, W-20, y+94], radius=10)
    bw = W - 88
    gw, rw = int(bw * adv / total), int(bw * dec / total)
    d.rounded_rectangle([42, y+14, 42+bw,       y+44], radius=6, fill=(225, 228, 245))
    d.rounded_rectangle([42, y+14, 42+gw,       y+44], radius=6, fill=C_GREEN)
    d.rectangle(        [42+gw, y+14, 42+gw+rw, y+44],           fill=C_RED)
    d.rounded_rectangle([42+gw+rw, y+14, 42+bw, y+44], radius=6, fill=(205, 208, 228))
    d.text((44, y+56),  f"  {adv}  ADVANCES",  font=F(16), fill=C_GREEN)
    bb = d.textbbox((0, 0), f"{dec}  DECLINES", font=F(16))
    d.text((W//2-(bb[2]-bb[0])//2, y+56), f"{dec}  DECLINES", font=F(16), fill=C_RED)
    bb2 = d.textbbox((0, 0), f"{unc}  UNCHANGED", font=F(15, bold=False))
    d.text((W-46-(bb2[2]-bb2[0]), y+58), f"{unc}  UNCHANGED", font=F(15, bold=False), fill=C_DIM)
    y += 112

    # GAINERS & LOSERS
    y = sec(d, y, "TOP GAINERS  &  TOP LOSERS", "gold", W)
    hw = (W - 56) // 2
    rr(d, [22, y, 22+hw, y+38], 6, C_GREEN)
    cx(d, "TOP  GAINERS", F(16), y+10, 22, 22+hw, C_WHITE)
    rr(d, [26+hw, y, W-22, y+38], 6, C_RED)
    cx(d, "TOP  LOSERS",  F(16), y+10, 26+hw, W-22, C_WHITE)
    y += 42
    gainers, losers = data["gainers"], data["losers"]
    for i in range(max(len(gainers), len(losers))):
        g  = gainers[i] if i < len(gainers) else ("", "")
        l  = losers[i]  if i < len(losers)  else ("", "")
        bg = C_CARD2 if i % 2 else C_CARD
        rr(d, [22, y, 22+hw, y+46], 6, bg, outline=C_BORDER, ow=1)
        d.rectangle([22, y, 28, y+46], fill=C_GREEN)
        d.text((40, y+13), g[0], font=F(18, bold=False), fill=C_TEXT)
        rx(d, g[1], F(18), y+13, 22+hw-16, C_GREEN)
        rr(d, [26+hw, y, W-22, y+46], 6, bg, outline=C_BORDER, ow=1)
        d.rectangle([26+hw, y, 32+hw, y+46], fill=C_RED)
        d.text((44+hw, y+13), l[0], font=F(18, bold=False), fill=C_TEXT)
        rx(d, l[1], F(18), y+13, W-38, C_RED)
        y += 50
    y += 16

    # SECTOR PERFORMANCE
    y = sec(d, y, "SECTOR PERFORMANCE", "purple", W)
    sw = (W - 60) // 3
    for i, (name, chg) in enumerate(data["sectors"]):
        ci = i % 3
        sx = 22 + ci * (sw + 8)
        if ci == 0 and i > 0:
            y += 64
        pos = not chg.startswith("-")
        col = C_GREEN if pos else C_RED
        shadow_card(d, [sx, y, sx+sw, y+58], radius=10)
        d.rounded_rectangle([sx, y, sx+sw, y+6], radius=5, fill=col)
        cx(d, name, F(15, bold=False), y+16, sx, sx+sw, C_MID)
        cx(d, chg,  F(24),             y+30, sx, sx+sw, col)
    y += 78

    # 52 WEEK HIGH / LOW
    y = sec(d, y, "52-WEEK HIGH  &  52-WEEK LOW", "teal", W)
    cw2 = (W - 56) // 2
    for xp, lbl, col, bg in [
        (22,     "STOCKS AT 52-WEEK HIGH", C_GREEN, (230, 250, 238)),
        (26+cw2, "STOCKS AT 52-WEEK LOW",  C_RED,   (252, 232, 234)),
    ]:
        rr(d, [xp, y, xp+cw2, y+38], 6, bg, outline=col, ow=1)
        cx(d, lbl, F(14), y+10, xp, xp+cw2, col)
    y += 42
    for xp in [22, 26+cw2]:
        rr(d, [xp, y, xp+cw2, y+32], 4, (18, 30, 88))
        d.text((xp+12, y+8), "STOCK", font=F(13), fill=C_GOLD2)
        cx(d, "CMP", F(13), y+8, xp+cw2//2-30, xp+cw2//2+30, C_GOLD2)
        rx(d, "52W LVL", F(13), y+8, xp+cw2-12, C_GOLD2)
    y += 36
    highs, lows = data["week52_high"], data["week52_low"]
    for i in range(max(len(highs), len(lows))):
        h  = highs[i] if i < len(highs) else ("", "", "")
        l  = lows[i]  if i < len(lows)  else ("", "", "")
        bg = C_CARD2 if i % 2 else C_CARD
        for xp, item, col in [(22, h, C_GREEN), (26+cw2, l, C_RED)]:
            rr(d, [xp, y, xp+cw2, y+44], 5, bg, outline=C_BORDER, ow=1)
            d.text((xp+12, y+12), item[0], font=F(16, bold=False), fill=C_TEXT)
            cx(d, item[1], F(16), y+12, xp+cw2//2-40, xp+cw2//2+40, col)
            rx(d, item[2], F(14, bold=False), y+14, xp+cw2-12, C_DIM)
        y += 48
    y += 16

    y = page_footer(d, y+10, W,
        "Continued in Part 2  —  Volume  |  Buildup  |  OI  |  FII / DII")
    return img.crop((0, 0, W, y))


# ═══════════════════════════════════════════
# IMAGE 2
# Volume | Delivery | Buildup | OI | Bulk | FII/DII
# ═══════════════════════════════════════════
def build_image2(data, W=1080):
    img = Image.new("RGB", (W, 4000), C_PAGE)
    dot_grid(img, W, 4000)
    d = ImageDraw.Draw(img)

    y = page_header(d, W,
        "INSTITUTIONAL SMART MONEY REPORT  —  PART 2 OF 2",
        "VOLUME   /   DELIVERY   /   LONG & SHORT BUILDUP   /   OI   /   FII & DII",
        data["date"])

    # TOP VOLUME
    y = sec(d, y, "TOP 5 HIGHEST VOLUME  —  NIFTY 500", "gold", W)
    for i, (stock, vol) in enumerate(data["top_volume"]):
        y = drow(d, y, stock, vol, W, vc=C_BLUE, alt=i%2==1)
        y += 2
    y += 14

    # TOP DELIVERY
    y = sec(d, y, "TOP 5 HIGHEST DELIVERY %", "green", W)
    for i, (stock, pct) in enumerate(data["delivery"]):
        y = drow(d, y, stock, pct, W, vc=C_GREEN, alt=i%2==1)
        y += 2
    y += 14

    # LONG BUILDUP
    y = sec(d, y, "LONG BUILDUP  —  TOP 5  ( PRICE UP  |  OI UP )", "green", W)
    rr(d, [22, y, W-22, y+34], 5, (18, 30, 88))
    d.text((44, y+9), "STOCK", font=F(13), fill=C_GOLD2)
    cx(d, "PRICE CHG", F(13), y+9, W//2-80, W//2+80, C_GOLD2)
    rx(d, "OI CHANGE", F(13), y+9, W-40, C_GOLD2)
    y += 38
    for i, (stock, pchg, oichg) in enumerate(data["long_buildup"]):
        bg = C_CARD2 if i % 2 else C_CARD
        rr(d, [22, y, W-22, y+46], 6, bg, outline=C_BORDER, ow=1)
        d.rectangle([22, y, 28, y+46], fill=C_GREEN)
        d.text((44, y+13), stock, font=F(17, bold=False), fill=C_TEXT)
        cx(d, pchg,  F(17),             y+13, W//2-60, W//2+60, C_GREEN)
        rx(d, oichg, F(16, bold=False), y+15, W-40,             C_CYAN)
        y += 50
    y += 14

    # SHORT BUILDUP
    y = sec(d, y, "SHORT BUILDUP  —  TOP 5  ( PRICE DOWN  |  OI UP )", "red", W)
    rr(d, [22, y, W-22, y+34], 5, (18, 30, 88))
    d.text((44, y+9), "STOCK", font=F(13), fill=C_GOLD2)
    cx(d, "PRICE CHG", F(13), y+9, W//2-80, W//2+80, C_GOLD2)
    rx(d, "OI CHANGE", F(13), y+9, W-40, C_GOLD2)
    y += 38
    for i, (stock, pchg, oichg) in enumerate(data["short_buildup"]):
        bg = C_CARD2 if i % 2 else C_CARD
        rr(d, [22, y, W-22, y+46], 6, bg, outline=C_BORDER, ow=1)
        d.rectangle([22, y, 28, y+46], fill=C_RED)
        d.text((44, y+13), stock, font=F(17, bold=False), fill=C_TEXT)
        cx(d, pchg,  F(17),             y+13, W//2-60, W//2+60, C_RED)
        rx(d, oichg, F(16, bold=False), y+15, W-40,             C_CYAN)
        y += 50
    y += 14

    # OI LEVELS
    y = sec(d, y, "OPEN INTEREST LEVELS", "red", W)
    cw = (W - 56) // 2
    for xp, lbl, col, bg in [
        (22,    "CALL OI  —  RESISTANCE ZONES", C_RED,   (252, 232, 234)),
        (26+cw, "PUT  OI  —  SUPPORT  ZONES",   C_GREEN, (230, 250, 238)),
    ]:
        rr(d, [xp, y, xp+cw, y+38], 6, bg, outline=col, ow=1)
        cx(d, lbl, F(14), y+10, xp, xp+cw, col)
    y += 42
    calls, puts = data["call_oi"], data["put_oi"]
    for i in range(max(len(calls), len(puts))):
        bg = C_CARD2 if i % 2 else C_CARD
        for xp, items, col in [(22, calls, C_RED), (26+cw, puts, C_GREEN)]:
            item = items[i] if i < len(items) else ("", "")
            rr(d, [xp, y, xp+cw, y+46], 5, bg, outline=C_BORDER, ow=1)
            d.text((xp+12, y+13), item[0], font=F(16, bold=False), fill=C_TEXT)
            rx(d, item[1], F(16), y+13, xp+cw-12, col)
        y += 50
    y += 14

    # KEY LEVELS
    y = sec(d, y, "KEY LEVELS  —  BASED ON OI", "cyan", W)
    kl = data.get("key_levels", {})
    levels = [
        ("STRONG RES", kl.get("strong_res", "--"), C_RED),
        ("RESISTANCE",  kl.get("resistance",  "--"), C_ORANGE),
        ("LTP",         kl.get("ltp",         "--"), C_BLUE),
        ("SUPPORT",     kl.get("support",     "--"), C_CYAN),
        ("STRONG SUP",  kl.get("strong_sup",  "--"), C_GREEN),
    ]
    kw = (W - 46) // len(levels)
    shadow_card(d, [20, y, W-20, y+112], radius=10)
    for i, (lbl, val, col) in enumerate(levels):
        kx = 23 + i * kw
        if i > 0:
            ln(d, kx, y+12, kx, y+100, C_LINE, 1)
        d.ellipse([kx+kw//2-5, y+14, kx+kw//2+5, y+24], fill=col)
        cx(d, lbl, F(12, bold=False), y+30, kx, kx+kw, C_DIM)
        cx(d, val, F(24),             y+54, kx, kx+kw, col)
        rr(d, [kx+12, y+90, kx+kw-12, y+102], 4, col)
    y += 126

    # BULK / BLOCK DEALS
    y = sec(d, y, "TOP BULK  &  BLOCK DEALS", "orange", W)
    for i, (stock, activity) in enumerate(data["bulk_deals"]):
        y = drow(d, y, stock, activity, W, vc=C_ORANGE, alt=i%2==1)
        y += 2
    y += 14

    # FII / DII
    y = sec(d, y, "FII  /  DII  DATA", "gold", W)
    fii, dii = data["fii"], data["dii"]
    hw2 = (W - 56) // 2
    for xp, lbl, val, col in [
        (22,     "FII  NET  BUY / SELL", fii, C_GREEN if fii.startswith("+") else C_RED),
        (26+hw2, "DII  NET  BUY / SELL", dii, C_GREEN if dii.startswith("+") else C_RED),
    ]:
        shadow_card(d, [xp, y, xp+hw2, y+98], radius=10)
        d.rounded_rectangle([xp, y, xp+hw2, y+6], radius=5, fill=col)
        cx(d, lbl,           F(14, bold=False), y+18, xp, xp+hw2, C_DIM)
        cx(d, f"Rs. {val} Cr", F(30),           y+48, xp, xp+hw2, col)
    y += 116

    y = page_footer(d, y+10, W,
        "Follow @PriceActionTelugu  for Daily Market Updates")
    return img.crop((0, 0, W, y))


# ═══════════════════════════════════════════
# TELEGRAM
# ═══════════════════════════════════════════
def send_photo(path, caption):
    try:
        with open(path, "rb") as f:
            r = requests.post(TELEGRAM_URL,
                data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "HTML"},
                files={"photo": f}, timeout=30)
        print(f"[TG] {path} ->", "OK" if r.status_code == 200 else r.text)
    except Exception as e:
        print("Error:", e)


# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
if __name__ == "__main__":
    ist_now = now_ist()
    print(f"[EOD] Running at IST: {ist_now.strftime('%d %B %Y  %I:%M %p')}")

    data  = get_report_data()
    today = data["date"]

    print("[EOD] Building images...")
    img1 = build_image1(data)
    img2 = build_image2(data)

    img1.save("eod_part1.png", "PNG", quality=95)
    img2.save("eod_part2.png", "PNG", quality=95)
    print(f"[EOD] Done  Part1:{img1.size}  Part2:{img2.size}")

    send_photo("eod_part1.png", (
        f"<b>PRICE ACTION TELUGU</b>  |  {today}\n"
        f"<b>Part 1</b> — Index | Gainers / Losers | Sectors | 52W\n\n"
        f"<i>For Educational Purposes Only</i>"
    ))
    time.sleep(2)
    send_photo("eod_part2.png", (
        f"<b>PRICE ACTION TELUGU</b>  |  {today}\n"
        f"<b>Part 2</b> — Volume | Buildup | OI | FII / DII\n\n"
        f"<i>For Educational Purposes Only</i>"
    ))
