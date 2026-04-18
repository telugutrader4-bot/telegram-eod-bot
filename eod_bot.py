"""
PRICE ACTION TELUGU — Professional EOD Report Bot
2 Images | Light Theme | Brand Colors
Drop-in replacement — same config, same data structure
"""

import os
import time
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

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
    today = datetime.now().strftime("%d %B %Y")
    return {
        "date": today,
        "indices": [
            {"name": "NIFTY 50",   "value": "24,315", "chg": "+0.82%"},
            {"name": "BANK NIFTY", "value": "52,840", "chg": "+1.14%"},
            {"name": "SENSEX",     "value": "80,218", "chg": "+0.79%"},
        ],
        "vix": "13.45",
        "pcr": "1.18",
        "adv_dec": "3 : 1",
        "advances": 1820,
        "declines":  620,
        "unchanged": 110,
        "gainers": [
            ("BEL",        "+5.2%"),
            ("HAL",        "+4.1%"),
            ("IRFC",       "+3.8%"),
            ("RECLTD",     "+3.2%"),
            ("TATA POWER", "+2.9%"),
        ],
        "losers": [
            ("HINDUNILVR", "-2.1%"),
            ("NESTLEIND",  "-1.8%"),
            ("WIPRO",      "-1.5%"),
            ("TECHM",      "-1.2%"),
            ("DABUR",      "-0.9%"),
        ],
        "sectors": [
            ("Defence",   "+3.4%"),
            ("PSU Banks", "+2.1%"),
            ("Metal",     "+1.8%"),
            ("IT",        "-1.2%"),
            ("FMCG",      "-0.8%"),
            ("Pharma",    "+0.5%"),
        ],
        "top_volume": [
            ("RELIANCE",    "4.2 Cr"),
            ("SBIN",        "3.8 Cr"),
            ("BEL",         "3.1 Cr"),
            ("TATA MOTORS", "2.9 Cr"),
            ("IRFC",        "2.6 Cr"),
        ],
        "delivery": [
            ("BEL",        "78%"),
            ("IRCTC",      "74%"),
            ("HAL",        "71%"),
            ("BHEL",       "69%"),
            ("COAL INDIA", "67%"),
        ],
        "call_oi": [
            ("N-24500 CE",  "1.82 Cr"),
            ("N-24600 CE",  "1.35 Cr"),
            ("BN-56000 CE", "95 L"),
            ("BN-56200 CE", "72 L"),
        ],
        "put_oi": [
            ("N-24000 PE",  "2.10 Cr"),
            ("N-24100 PE",  "1.64 Cr"),
            ("BN-55000 PE", "1.12 Cr"),
            ("BN-54800 PE", "88 L"),
        ],
        "key_levels": {
            "strong_res": "24600",
            "resistance":  "24450",
            "ltp":         "24315",
            "support":     "24150",
            "strong_sup":  "24000",
        },
        "bulk_deals": [
            ("RELIANCE", "Institutional Buy"),
            ("INFY",     "Fund Activity"),
            ("BEL",      "Large Accumulation"),
            ("LT",       "Bulk Buying"),
            ("HDFCLIFE", "Promoter Activity"),
        ],
        "fii": "+2,350",
        "dii": "-1,120",
    }

# ═══════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════
BG     = (248, 248, 252)
CARD   = (255, 255, 255)
CARD2  = (240, 242, 252)
NAVY   = (10,  18,  70)
YELLOW = (255, 196,   0)
CYAN   = (0,  180, 200)
TDARK  = (15,  20,  55)
TMID   = (60,  70, 110)
TDIM   = (130, 140, 175)
GREEN  = (0,  160,  80)
RED    = (210,  45,  45)
ORANGE = (220, 120,   0)
GOLD   = (180, 130,   0)
PURPLE = (100,  70, 200)
BORDER = (210, 215, 235)
SHADOW = (224, 227, 244)
WHITE  = (255, 255, 255)

# ═══════════════════════════════════════════
# FONTS  (Windows + Linux compatible)
# ═══════════════════════════════════════════
def _find_font(bold=False):
    candidates_bold = [
        "DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    candidates_normal = [
        "DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in (candidates_bold if bold else candidates_normal):
        try:
            ImageFont.truetype(path, 10)
            return path
        except:
            pass
    return None

_BOLD_PATH   = _find_font(bold=True)
_NORMAL_PATH = _find_font(bold=False)

def F(size, bold=True):
    path = _BOLD_PATH if bold else _NORMAL_PATH
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# ═══════════════════════════════════════════
# DRAW HELPERS
# ═══════════════════════════════════════════
def rr(d, xy, r, fill, outline=None, ow=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=ow)

def dot(d, x, y, r, color):
    d.ellipse([x-r, y-r, x+r, y+r], fill=color)

def centered(d, text, font, y, x1, x2, color):
    bb = d.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    d.text((x1 + (x2 - x1 - tw) // 2, y), text, font=font, fill=color)

def shadow_card(d, xy, radius=12):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle([x1+3, y1+3, x2+3, y2+3], radius=radius, fill=SHADOW)
    rr(d, xy, radius, CARD, outline=BORDER, ow=1)

def dotgrid(img, W, H):
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 32):
        for gy in range(0, H, 32):
            d.ellipse([gx, gy, gx+1, gy+1], fill=(218, 221, 238))

def section_tab(d, y, title, accent, W):
    rr(d, [20, y, W-20, y+54], 12, NAVY)
    d.rectangle([20, y, 34, y+54], fill=accent)
    dot(d, 52, y+27, 9, accent)
    d.text((70, y+15), title, font=F(22), fill=WHITE)
    return y + 64

def data_row(d, y, label, value, W, vc=TDARK, alt=False):
    rr(d, [22, y, W-22, y+46], 7, CARD2 if alt else CARD, outline=BORDER, ow=1)
    d.text((44, y+13), label, font=F(18, bold=False), fill=TDARK)
    bb = d.textbbox((0, 0), value, font=F(18))
    d.text((W-44-(bb[2]-bb[0]), y+13), value, font=F(18), fill=vc)
    return y + 50

def page_header(d, W, line1, line2, date_str):
    d.rectangle([0, 0, W, 178], fill=NAVY)
    d.rectangle([0, 0, W, 5],   fill=YELLOW)
    rr(d, [18, 16, W-18, 84], 14, YELLOW)
    centered(d, "✦  PRICE ACTION TELUGU  ✦", F(34), 28, 18, W-18, NAVY)
    d.text((30, 96),  line1, font=F(19, bold=False), fill=(200, 212, 255))
    d.text((30, 124), line2, font=F(16, bold=False), fill=(150, 165, 210))
    rr(d, [W-218, 94, W-20, 134], 10, YELLOW)
    centered(d, date_str, F(17), 104, W-218, W-20, NAVY)
    d.rectangle([0, 173, W, 178], fill=CYAN)
    return 196

def page_footer(d, y, W, msg=""):
    d.rectangle([0, y, W, y+76], fill=NAVY)
    d.rectangle([0, y, W, y+4], fill=YELLOW)
    centered(d, msg, F(18, bold=False), y+14, 0, W, (255, 213, 0))
    centered(d, "⚠️  For Educational Purposes Only  |  Not SEBI Registered Advice",
             F(14, bold=False), y+48, 0, W, (140, 155, 200))
    d.rectangle([0, y+72, W, y+76], fill=CYAN)
    return y + 78

# ═══════════════════════════════════════════
# IMAGE 1 — Market Overview
# ═══════════════════════════════════════════
def build_image1(data, W=1080):
    H = 2600
    img = Image.new("RGB", (W, H), BG)
    dotgrid(img, W, H)
    d = ImageDraw.Draw(img)

    y = page_header(d, W,
        "📊 Institutional Smart Money Report — Part 1 of 2",
        "Index Snapshot  |  Gainers & Losers  |  Sector Performance",
        data["date"])

    # INDEX CARDS
    y = section_tab(d, y, "📈  INDEX SNAPSHOT", CYAN, W)
    iw = (W - 60) // 3
    for i, idx in enumerate(data["indices"]):
        ix = 22 + i * (iw + 8)
        pos = not idx["chg"].startswith("-")
        col = GREEN if pos else RED
        shadow_card(d, [ix, y, ix+iw, y+106], radius=14)
        d.rounded_rectangle([ix, y, ix+iw, y+8], radius=6, fill=col)
        centered(d, idx["name"],  F(17, bold=False), y+18, ix, ix+iw, TMID)
        centered(d, idx["value"], F(30),             y+40, ix, ix+iw, TDARK)
        centered(d, idx["chg"],   F(22),             y+76, ix, ix+iw, col)
    y += 122

    # VIX / PCR / A-D
    mw = (W - 60) // 3
    for i, (lbl, val, col) in enumerate([
        ("India VIX",  data["vix"],     ORANGE),
        ("PCR",        data["pcr"],     PURPLE),
        ("Adv / Dec",  data["adv_dec"], CYAN),
    ]):
        mx = 22 + i * (mw + 8)
        shadow_card(d, [mx, y, mx+mw, y+80], radius=12)
        d.rounded_rectangle([mx, y, mx+mw, y+6], radius=4, fill=col)
        centered(d, lbl, F(16, bold=False), y+16, mx, mx+mw, TDIM)
        centered(d, val, F(28),             y+38, mx, mx+mw, col)
    y += 96

    # MARKET BREADTH
    y = section_tab(d, y, "📊  MARKET BREADTH", GREEN, W)
    adv   = data["advances"]
    dec   = data["declines"]
    unc   = data["unchanged"]
    total = adv + dec + unc or 1
    shadow_card(d, [20, y, W-20, y+96], radius=12)
    bw = W - 86
    gw = int(bw * adv / total)
    rw = int(bw * dec / total)
    d.rounded_rectangle([42, y+14, 42+bw,       y+46], radius=8, fill=(228, 231, 245))
    d.rounded_rectangle([42, y+14, 42+gw,       y+46], radius=8, fill=(0, 180, 90))
    d.rectangle(        [42+gw, y+14, 42+gw+rw, y+46],           fill=(200, 50, 50))
    d.rounded_rectangle([42+gw+rw, y+14, 42+bw, y+46], radius=8, fill=(200, 204, 224))
    d.text((44, y+58), f"▲ {adv} Advances", font=F(18), fill=GREEN)
    bb = d.textbbox((0,0), f"▼ {dec} Declines", font=F(18))
    d.text((W//2-(bb[2]-bb[0])//2, y+58), f"▼ {dec} Declines", font=F(18), fill=RED)
    bb2 = d.textbbox((0,0), f"– {unc}", font=F(18))
    d.text((W-46-(bb2[2]-bb2[0]), y+58), f"– {unc}", font=F(18), fill=TDIM)
    y += 114

    # GAINERS & LOSERS
    y = section_tab(d, y, "🚀  TOP GAINERS & LOSERS", YELLOW, W)
    hw = (W - 56) // 2
    rr(d, [22, y, 22+hw, y+40], 8, GREEN)
    centered(d, "▲  TOP GAINERS", F(17), y+11, 22, 22+hw, WHITE)
    rr(d, [26+hw, y, W-22, y+40], 8, RED)
    centered(d, "▼  TOP LOSERS",  F(17), y+11, 26+hw, W-22, WHITE)
    y += 44
    gainers = data["gainers"]
    losers  = data["losers"]
    for i in range(max(len(gainers), len(losers))):
        g  = gainers[i] if i < len(gainers) else ("", "")
        l  = losers[i]  if i < len(losers)  else ("", "")
        bg = CARD2 if i % 2 else CARD
        rr(d, [22, y, 22+hw, y+48], 7, bg, outline=BORDER, ow=1)
        d.rectangle([22, y, 29, y+48], fill=GREEN)
        d.text((40, y+13), g[0], font=F(19, bold=False), fill=TDARK)
        bb = d.textbbox((0,0), g[1], font=F(19))
        d.text((22+hw-16-(bb[2]-bb[0]), y+13), g[1], font=F(19), fill=GREEN)
        rr(d, [26+hw, y, W-22, y+48], 7, bg, outline=BORDER, ow=1)
        d.rectangle([26+hw, y, 33+hw, y+48], fill=RED)
        d.text((44+hw, y+13), l[0], font=F(19, bold=False), fill=TDARK)
        bb2 = d.textbbox((0,0), l[1], font=F(19))
        d.text((W-38-(bb2[2]-bb2[0]), y+13), l[1], font=F(19), fill=RED)
        y += 52
    y += 14

    # SECTOR HEATMAP
    y = section_tab(d, y, "🏭  SECTOR PERFORMANCE", PURPLE, W)
    sw = (W - 60) // 3
    for i, (name, chg) in enumerate(data["sectors"]):
        ci = i % 3
        sx = 22 + ci * (sw + 8)
        if ci == 0 and i > 0:
            y += 62
        pos = not chg.startswith("-")
        col = GREEN if pos else RED
        shadow_card(d, [sx, y, sx+sw, y+56], radius=12)
        d.rounded_rectangle([sx, y, sx+sw, y+7], radius=5, fill=col)
        centered(d, name, F(16, bold=False), y+16, sx, sx+sw, TMID)
        centered(d, chg,  F(23),             y+30, sx, sx+sw, col)
    y += 74

    y = page_footer(d, y+8, W, "Continued in Part 2  →  Volume | OI | FII/DII")
    return img.crop((0, 0, W, y))


# ═══════════════════════════════════════════
# IMAGE 2 — Smart Money Data
# ═══════════════════════════════════════════
def build_image2(data, W=1080):
    H = 2600
    img = Image.new("RGB", (W, H), BG)
    dotgrid(img, W, H)
    d = ImageDraw.Draw(img)

    y = page_header(d, W,
        "🏛 Institutional Smart Money Report — Part 2 of 2",
        "Volume  |  Delivery  |  OI Levels  |  Bulk Deals  |  FII/DII",
        data["date"])

    # TOP VOLUME
    y = section_tab(d, y, "🔥  TOP 5 HIGHEST VOLUME  (Nifty 500)", YELLOW, W)
    for i, (stock, vol) in enumerate(data["top_volume"]):
        y = data_row(d, y, stock, vol, W, vc=NAVY, alt=i%2==1)
        y += 2
    y += 14

    # TOP DELIVERY
    y = section_tab(d, y, "📦  TOP 5 HIGHEST DELIVERY %", GREEN, W)
    for i, (stock, pct) in enumerate(data["delivery"]):
        y = data_row(d, y, stock, pct, W, vc=GREEN, alt=i%2==1)
        y += 2
    y += 14

    # OI LEVELS
    y = section_tab(d, y, "📉  OPEN INTEREST LEVELS", RED, W)
    cw = (W - 56) // 2
    for xp, lbl, col, bg in [
        (22,    "🔴  CALL OI — Resistance", RED,   (255, 236, 236)),
        (26+cw, "🟢  PUT OI  — Support",    GREEN, (234, 252, 240)),
    ]:
        rr(d, [xp, y, xp+cw, y+40], 8, bg, outline=col, ow=1)
        d.text((xp+14, y+10), lbl, font=F(16), fill=col)
    y += 44
    calls = data["call_oi"]
    puts  = data["put_oi"]
    for i in range(max(len(calls), len(puts))):
        bg = CARD2 if i % 2 else CARD
        for xp, items, col in [(22, calls, RED), (26+cw, puts, GREEN)]:
            item = items[i] if i < len(items) else ("", "")
            rr(d, [xp, y, xp+cw, y+46], 6, bg, outline=BORDER, ow=1)
            d.text((xp+14, y+13), item[0], font=F(17, bold=False), fill=TDARK)
            bb = d.textbbox((0,0), item[1], font=F(17))
            d.text((xp+cw-14-(bb[2]-bb[0]), y+13), item[1], font=F(17), fill=col)
        y += 50
    y += 14

    # KEY LEVELS
    y = section_tab(d, y, "🎯  KEY LEVELS  (Based on OI)", CYAN, W)
    kl = data.get("key_levels", {})
    levels = [
        ("Strong Res", kl.get("strong_res", "--"), RED),
        ("Resistance",  kl.get("resistance",  "--"), ORANGE),
        ("LTP",         kl.get("ltp",         "--"), NAVY),
        ("Support",     kl.get("support",     "--"), CYAN),
        ("Strong Sup",  kl.get("strong_sup",  "--"), GREEN),
    ]
    kw = (W - 46) // len(levels)
    shadow_card(d, [20, y, W-20, y+116], radius=14)
    for i, (lbl, val, col) in enumerate(levels):
        kx = 23 + i * kw
        if i > 0:
            d.line([(kx, y+12), (kx, y+104)], fill=BORDER, width=1)
        dot(d, kx + kw//2, y+16, 5, col)
        centered(d, lbl, F(14, bold=False), y+26, kx, kx+kw, TDIM)
        centered(d, val, F(25),             y+54, kx, kx+kw, col)
        rr(d, [kx+10, y+94, kx+kw-10, y+108], 4, col)
    y += 130

    # BULK DEALS
    y = section_tab(d, y, "🏦  TOP BULK / BLOCK DEALS", GOLD, W)
    for i, (stock, activity) in enumerate(data["bulk_deals"]):
        y = data_row(d, y, stock, activity, W, vc=GOLD, alt=i%2==1)
        y += 2
    y += 14

    # FII / DII
    y = section_tab(d, y, "💰  FII / DII DATA", YELLOW, W)
    fii = data["fii"]
    dii = data["dii"]
    hw2 = (W - 56) // 2
    for xp, lbl, val, col in [
        (22,     "FII Net Buy / Sell", fii, GREEN if fii.startswith("+") else RED),
        (26+hw2, "DII Net Buy / Sell", dii, GREEN if dii.startswith("+") else RED),
    ]:
        shadow_card(d, [xp, y, xp+hw2, y+96], radius=14)
        d.rounded_rectangle([xp, y, xp+hw2, y+7], radius=5, fill=col)
        centered(d, lbl,           F(16, bold=False), y+18, xp, xp+hw2, TDIM)
        centered(d, f"₹ {val} Cr", F(30),             y+48, xp, xp+hw2, col)
    y += 114

    y = page_footer(d, y+8, W, "🔔  Follow @PriceActionTelugu for Daily Updates")
    return img.crop((0, 0, W, y))


# ═══════════════════════════════════════════
# TELEGRAM SENDER
# ═══════════════════════════════════════════
def send_photo(image_path, caption):
    try:
        with open(image_path, "rb") as photo:
            response = requests.post(
                TELEGRAM_URL,
                data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "HTML"},
                files={"photo": photo},
                timeout=30
            )
        print(f"[TG] {image_path} →", "✅ OK" if response.status_code == 200 else f"❌ {response.text}")
    except Exception as e:
        print("Telegram Error:", str(e))


# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
if __name__ == "__main__":
    data  = get_report_data()
    today = data["date"]

    print("[EOD] Building images...")
    img1 = build_image1(data)
    img2 = build_image2(data)

    img1.save("eod_part1.png", "PNG", quality=95)
    img2.save("eod_part2.png", "PNG", quality=95)
    print(f"[EOD] ✅ Part1: {img1.size}  Part2: {img2.size}")

    send_photo("eod_part1.png", (
        f"<b>🔥 PRICE ACTION TELUGU</b>  |  {today}\n"
        f"📊 <b>Part 1</b> — Index Snapshot, Gainers/Losers &amp; Sectors\n\n"
        f"<i>⚠️ For Educational Purposes Only</i>"
    ))
    time.sleep(2)
    send_photo("eod_part2.png", (
        f"<b>🔥 PRICE ACTION TELUGU</b>  |  {today}\n"
        f"🏛 <b>Part 2</b> — Volume, OI Levels, FII/DII &amp; Bulk Deals\n\n"
        f"<i>⚠️ For Educational Purposes Only</i>"
    ))
