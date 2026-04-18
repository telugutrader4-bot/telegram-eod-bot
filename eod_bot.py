# eod_bot.py
# PRICE ACTION TELUGU — EOD Bot (Production)
# Data from Dhan API → Premium Images → Telegram Channel

import os
import requests
from datetime import datetime
from image_generator import generate_images, ORANGE, PURPLE, TEAL

# =====================================================
# CONFIG
# =====================================================

BOT_TOKEN         = os.getenv("BOT_TOKEN")
CHAT_ID           = "@priceactionoptions"
DHAN_CLIENT_ID    = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

print("DHAN TOKEN FOUND:", bool(DHAN_ACCESS_TOKEN))

if not DHAN_ACCESS_TOKEN:
    raise Exception("DHAN_ACCESS_TOKEN missing in GitHub Secrets")

DHAN_HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id":    DHAN_CLIENT_ID,
    "Content-Type": "application/json",
}

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# =====================================================
# SAFE API FETCH
# =====================================================

def safe_get(url, params=None):
    try:
        r = requests.get(url, headers=DHAN_HEADERS, params=params, timeout=20)
        print("API:", r.status_code, url)
        if r.status_code == 200:
            return r.json()
        print("API Failed:", r.text)
        return None
    except Exception as e:
        print("API Error:", str(e))
        return None

# =====================================================
# DATA FETCHING  (replace URLs with real Dhan endpoints)
# =====================================================

def get_report_data():
    today = datetime.now().strftime("%d %B %Y")

    # ── REPLACE THESE with your actual Dhan API calls ──
    # index_data   = safe_get("https://api.dhan.co/market/index")
    # gainers_data = safe_get("https://api.dhan.co/market/gainers")
    # losers_data  = safe_get("https://api.dhan.co/market/losers")
    # sector_data  = safe_get("https://api.dhan.co/market/sectors")
    # volume_data  = safe_get("https://api.dhan.co/market/volume")
    # delivery_data= safe_get("https://api.dhan.co/market/delivery")
    # oi_data      = safe_get("https://api.dhan.co/options/oi")
    # fii_data     = safe_get("https://api.dhan.co/market/fii-dii")
    # ───────────────────────────────────────────────────

    # ── Parse your API responses and fill the dict below ──
    # Example for indices (adapt keys to match actual Dhan response):
    # nifty_val  = f"{index_data['nifty50']['last']:,.0f}"
    # nifty_chg  = f"{index_data['nifty50']['changePercent']:+.2f}%"

    # ── FALLBACK / TEST DATA (replace with real parsed data) ──
    return {
        "date": today,

        # Part 1
        "indices": [
            ("NIFTY 50",   "24,315", "+0.82%"),
            ("BANK NIFTY", "52,840", "+1.14%"),
            ("SENSEX",     "80,218", "+0.79%"),
        ],
        "extras": [
            ("INDIA VIX",      "13.45", ORANGE),
            ("PUT CALL RATIO", "1.18",  PURPLE),
            ("ADV / DEC",      "3 : 1", TEAL),
        ],
        "breadth": {"advances": 1820, "declines": 620, "unchanged": 110},
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
            ("DEFENCE",   "+3.4%"), ("PSU BANKS", "+2.1%"), ("METAL",  "+1.8%"),
            ("IT",        "-1.2%"), ("FMCG",      "-0.8%"), ("PHARMA", "+0.5%"),
        ],
        "52w_high": [
            ("BEL",        "310.50", "311.00"),
            ("HAL",        "4,820",  "4,850"),
            ("IRFC",       "229.40", "230.00"),
            ("RECLTD",     "498.70", "500.00"),
            ("TATA POWER", "415.20", "416.50"),
        ],
        "52w_low": [
            ("HINDUNILVR", "2,190",  "2,180"),
            ("NESTLEIND",  "2,050",  "2,040"),
            ("WIPRO",      "442.30", "440.00"),
            ("TECHM",      "1,315",  "1,310"),
            ("DABUR",      "488.60", "485.00"),
        ],

        # Part 2
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
        "long_buildup": [
            ("BEL",        "+5.2%", "OI +18%"),
            ("HAL",        "+4.1%", "OI +14%"),
            ("RECLTD",     "+3.2%", "OI +12%"),
            ("IRFC",       "+3.8%", "OI +11%"),
            ("TATA POWER", "+2.9%", "OI +9%"),
        ],
        "short_buildup": [
            ("HINDUNILVR", "-2.1%", "OI +16%"),
            ("NESTLEIND",  "-1.8%", "OI +13%"),
            ("WIPRO",      "-1.5%", "OI +11%"),
            ("TECHM",      "-1.2%", "OI +8%"),
            ("DABUR",      "-0.9%", "OI +7%"),
        ],
        "call_oi": [
            ("NIFTY  24500 CE", "1.82 Cr"),
            ("NIFTY  24600 CE", "1.35 Cr"),
            ("BNIFTY 56000 CE", "95 L"),
            ("BNIFTY 56200 CE", "72 L"),
        ],
        "put_oi": [
            ("NIFTY  24000 PE", "2.10 Cr"),
            ("NIFTY  24100 PE", "1.64 Cr"),
            ("BNIFTY 55000 PE", "1.12 Cr"),
            ("BNIFTY 54800 PE", "88 L"),
        ],
        "key_levels": {
            "strong_res": "24,600",
            "resistance":  "24,450",
            "ltp":         "24,315",
            "support":     "24,150",
            "strong_sup":  "24,000",
        },
        "bulk_deals": [
            ("RELIANCE", "Institutional Buy"),
            ("INFY",     "Fund Activity"),
            ("BEL",      "Large Accumulation"),
            ("LT",       "Bulk Buying"),
            ("HDFCLIFE", "Promoter Activity"),
        ],
        "fii": "Rs. +2,350 Cr",
        "dii": "Rs. -1,120 Cr",
    }

# =====================================================
# SEND TO TELEGRAM
# =====================================================

def send_photo(path, caption):
    try:
        with open(path, "rb") as f:
            r = requests.post(
                TELEGRAM_URL,
                data={"chat_id": CHAT_ID, "caption": caption},
                files={"photo": f},
                timeout=30,
            )
        print("Telegram:", r.status_code, r.text[:120])
        return r.status_code == 200
    except Exception as e:
        print("Telegram Error:", str(e))
        return False

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("Starting EOD Bot...")

    data = get_report_data()

    print("Generating images...")
    part1_path, part2_path = generate_images(data)

    print("Sending Part 1...")
    send_photo(part1_path, "📊 PRICE ACTION TELUGU — EOD Report Part 1 of 2\nIndex | Gainers & Losers | Sectors | 52W High & Low")

    print("Sending Part 2...")
    send_photo(part2_path, "📊 PRICE ACTION TELUGU — EOD Report Part 2 of 2\nVolume | Delivery | Buildup | OI | FII/DII")

    print("Done.")
