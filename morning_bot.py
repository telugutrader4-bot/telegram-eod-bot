# morning_bot.py
# PRICE ACTION TELUGU — Morning Report Bot
# Sends at 8:00 AM IST: Global Markets + Nifty/BankNifty OI Snapshot

import os
import requests
from datetime import datetime
from morning_generator import generate_morning_images

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

BOT_TOKEN         = os.getenv("BOT_TOKEN")
CHAT_ID           = "@priceactionoptions"
DHAN_CLIENT_ID    = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

DHAN_HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id":    DHAN_CLIENT_ID,
    "Content-Type": "application/json",
}

# ─────────────────────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────────────────────

def safe_get(url, params=None):
    try:
        r = requests.get(url, headers=DHAN_HEADERS, params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
        print(f"API Failed {r.status_code}: {r.text[:100]}")
        return None
    except Exception as e:
        print(f"API Error: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# DATA FETCHING
# Replace the dummy data below with real API calls
# ─────────────────────────────────────────────────────────────

def get_morning_data():
    now   = datetime.now()
    today = now.strftime("%d %B %Y")
    time  = now.strftime("%I:%M %p")

    # ── GLOBAL MARKETS ──────────────────────────────────────
    # Replace with real API calls to Yahoo Finance / Alpha Vantage
    # / your preferred global data source
    #
    # Example (Yahoo Finance via yfinance):
    # import yfinance as yf
    # dow  = yf.Ticker("^DJI").fast_info
    # sp   = yf.Ticker("^GSPC").fast_info
    # nas  = yf.Ticker("^IXIC").fast_info
    # nik  = yf.Ticker("^N225").fast_info
    # hang = yf.Ticker("^HSI").fast_info
    # shan = yf.Ticker("000001.SS").fast_info
    # sgx  = yf.Ticker("^NSEI").fast_info   # or SGX Nifty specific
    # crude= yf.Ticker("CL=F").fast_info
    # gold = yf.Ticker("GC=F").fast_info
    # dxy  = yf.Ticker("DX-Y.NYB").fast_info
    # usdinr = yf.Ticker("INR=X").fast_info

    # ── OI DATA from Dhan ────────────────────────────────────
    # Replace with real Dhan option chain endpoints:
    # nifty_chain   = safe_get("https://api.dhan.co/options/chain?symbol=NIFTY&expiry=NEAR")
    # bnf_chain     = safe_get("https://api.dhan.co/options/chain?symbol=BANKNIFTY&expiry=NEAR")

    # ─────────────────────────────────────────────────────────
    # FALLBACK / TEST DATA — replace values with parsed API data
    # ─────────────────────────────────────────────────────────
    return {
        "date": today,
        "time": time,

        # SGX / Gift Nifty
        "sgx_nifty": {
            "value": "24,380",
            "change": "+65",
            "pct":   "+0.27%",
        },

        # US Markets (previous close)
        "us_markets": [
            ("DOW JONES", "39,218", "+312", "+0.80%"),
            ("S&P 500",   "5,218",  "+28",  "+0.54%"),
            ("NASDAQ",    "18,340", "+95",  "+0.52%"),
        ],

        # Asian Markets (live pre-market)
        "asian_markets": [
            ("NIKKEI 225", "38,940", "-210", "-0.54%", "JP"),
            ("HANG SENG",  "18,215", "+185", "+1.03%", "HK"),
            ("SHANGHAI",   "3,285",  "+12",  "+0.37%", "CN"),
        ],

        # Commodities & Currency
        # accent color tuple: (R, G, B)
        "commodities": [
            ("CRUDE OIL",    "85.40", "+0.8%", "$/bbl", (180, 140, 0)),
            ("GOLD",         "2,312", "+0.3%", "$/oz",  (180, 140, 0)),
            ("DOLLAR INDEX", "104.2", "-0.2%", "DXY",   (0, 80, 180)),
            ("USD/INR",      "83.45", "+0.1%", "Rs",    (0, 80, 180)),
        ],

        # Quick metric strip (bottom of global page)
        "quick_metrics": [
            ("INDIA VIX",    "13.45", "-3.2%",  (110, 50, 180)),
            ("GIFT NIFTY",   "24,380","+0.27%", (0, 140, 60)),
            ("US 10Y YIELD", "4.28%", "+0.02",  (0, 80, 180)),
            ("FEAR & GREED", "62",    "GREED",  (180, 140, 0)),
        ],

        # Nifty OI — list of strikes around LTP
        # call_oi and put_oi in Lakhs (e.g. 182 = 182L = 1.82Cr)
        "nifty_ltp": "24,315",
        "nifty_oi": [
            {"strike": 24000, "call_oi": 45,  "put_oi": 210, "is_ltp": False},
            {"strike": 24100, "call_oi": 55,  "put_oi": 164, "is_ltp": False},
            {"strike": 24200, "call_oi": 68,  "put_oi": 112, "is_ltp": False},
            {"strike": 24300, "call_oi": 82,  "put_oi": 88,  "is_ltp": False},
            {"strike": 24315, "call_oi": 0,   "put_oi": 0,   "is_ltp": True},
            {"strike": 24400, "call_oi": 95,  "put_oi": 72,  "is_ltp": False},
            {"strike": 24500, "call_oi": 182, "put_oi": 58,  "is_ltp": False},
            {"strike": 24600, "call_oi": 135, "put_oi": 42,  "is_ltp": False},
            {"strike": 24700, "call_oi": 90,  "put_oi": 35,  "is_ltp": False},
            {"strike": 24800, "call_oi": 65,  "put_oi": 28,  "is_ltp": False},
        ],

        # BankNifty OI — same structure
        "banknifty_ltp": "52,840",
        "banknifty_oi": [
            {"strike": 52000, "call_oi": 38,  "put_oi": 95,  "is_ltp": False},
            {"strike": 52200, "call_oi": 44,  "put_oi": 88,  "is_ltp": False},
            {"strike": 52400, "call_oi": 52,  "put_oi": 75,  "is_ltp": False},
            {"strike": 52600, "call_oi": 68,  "put_oi": 62,  "is_ltp": False},
            {"strike": 52800, "call_oi": 72,  "put_oi": 48,  "is_ltp": False},
            {"strike": 52840, "call_oi": 0,   "put_oi": 0,   "is_ltp": True},
            {"strike": 53000, "call_oi": 95,  "put_oi": 35,  "is_ltp": False},
            {"strike": 53200, "call_oi": 112, "put_oi": 28,  "is_ltp": False},
            {"strike": 53400, "call_oi": 85,  "put_oi": 22,  "is_ltp": False},
            {"strike": 53600, "call_oi": 55,  "put_oi": 18,  "is_ltp": False},
        ],
    }

# ─────────────────────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────────────────────

def send_photo(path, caption):
    try:
        with open(path, "rb") as f:
            r = requests.post(
                TELEGRAM_URL,
                data={"chat_id": CHAT_ID, "caption": caption},
                files={"photo": f},
                timeout=30,
            )
        print(f"Telegram [{r.status_code}]: {path}")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting Morning Report Bot...")

    data = get_morning_data()

    print("Generating morning images...")
    global_path, oi_path = generate_morning_images(data)

    print("Sending Global Markets...")
    send_photo(global_path,
               "🌍 PRICE ACTION TELUGU — Morning Report\nGlobal Markets Snapshot | Pre-Market Intelligence")

    print("Sending OI Snapshot...")
    send_photo(oi_path,
               "📊 PRICE ACTION TELUGU — OI Snapshot\nNifty & BankNifty Option Chain | Color = OI Strength")

    print("Done.")
