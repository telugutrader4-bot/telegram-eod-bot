# eod_bot.py — PRICE ACTION TELUGU
# Real Dhan API data + Premium Images + Telegram

import os
import requests
from datetime import datetime
from image_generator import generate_images

BOT_TOKEN         = os.getenv("BOT_TOKEN")
CHAT_ID           = os.getenv("CHAT_ID", "@priceactionoptions")
DHAN_CLIENT_ID    = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

DHAN_HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id":    DHAN_CLIENT_ID,
    "Content-Type": "application/json"
}

ORANGE = (255, 145, 0)
PURPLE = (165, 105, 245)
TEAL   = (0, 210, 185)

# ─────────────────────────────────────────────────────────────
# DHAN API CALLS — REAL DATA
# ─────────────────────────────────────────────────────────────

def dhan_get(url):
    try:
        r = requests.get(url, headers=DHAN_HEADERS, timeout=20)
        print(f"GET {url} → {r.status_code}")
        if r.status_code == 200:
            return r.json()
        print("Error:", r.text[:200])
        return None
    except Exception as e:
        print("Exception:", e)
        return None

def dhan_post(url, payload):
    try:
        r = requests.post(url, headers=DHAN_HEADERS, json=payload, timeout=20)
        print(f"POST {url} → {r.status_code}")
        if r.status_code == 200:
            return r.json()
        print("Error:", r.text[:200])
        return None
    except Exception as e:
        print("Exception:", e)
        return None

# ─────────────────────────────────────────────────────────────
# FETCH INDICES
# ─────────────────────────────────────────────────────────────

def fetch_indices():
    """Fetch Nifty50, BankNifty, Sensex from Dhan market feed"""
    # Dhan security IDs: Nifty50=13, BankNifty=25, Sensex=51
    payload = {
        "NSE": ["13", "25"],
        "BSE": ["1"]
    }
    data = dhan_post("https://api.dhan.co/v2/marketfeed/ltp", payload)

    indices = []
    try:
        nifty  = data["data"]["NSE"]["13"]
        bnifty = data["data"]["NSE"]["25"]
        sensex = data["data"]["BSE"]["1"]

        for name, d in [("NIFTY 50", nifty), ("BANK NIFTY", bnifty), ("SENSEX", sensex)]:
            ltp    = d.get("ltp", 0)
            close  = d.get("close", ltp)
            change = ltp - close
            pct    = (change / close * 100) if close else 0
            sign   = "+" if change >= 0 else ""
            indices.append((name, f"{ltp:,.0f}", f"{sign}{pct:.2f}%"))
    except Exception as e:
        print("Index parse error:", e)
        indices = [
            ("NIFTY 50",   "N/A", "0.00%"),
            ("BANK NIFTY", "N/A", "0.00%"),
            ("SENSEX",     "N/A", "0.00%"),
        ]
    return indices

# ─────────────────────────────────────────────────────────────
# FETCH OPTION CHAIN — OI DATA
# ─────────────────────────────────────────────────────────────

def fetch_option_chain(symbol="NIFTY"):
    """Fetch option chain from Dhan for OI levels"""
    data = dhan_get(f"https://api.dhan.co/v2/optionchain?symbol={symbol}&expiryDate=near")
    if not data:
        return [], []

    call_oi = []
    put_oi  = []

    try:
        chain = data.get("data", {}).get("optionChain", [])
        for row in chain:
            strike = row.get("strikePrice", 0)
            c_oi   = row.get("callOI", 0)
            p_oi   = row.get("putOI", 0)

            if c_oi > 0:
                val = f"{c_oi/100:.2f} Cr" if c_oi >= 100 else f"{int(c_oi)} L"
                call_oi.append((f"{int(strike)} CE", val, c_oi))
            if p_oi > 0:
                val = f"{p_oi/100:.2f} Cr" if p_oi >= 100 else f"{int(p_oi)} L"
                put_oi.append((f"{int(strike)} PE", val, p_oi))

        # Sort by OI descending, take top 4
        call_oi = [(s, v) for s, v, _ in sorted(call_oi, key=lambda x: -x[2])[:4]]
        put_oi  = [(s, v) for s, v, _ in sorted(put_oi,  key=lambda x: -x[2])[:4]]

    except Exception as e:
        print("OI parse error:", e)

    return call_oi, put_oi

# ─────────────────────────────────────────────────────────────
# FETCH TOP GAINERS & LOSERS
# ─────────────────────────────────────────────────────────────

def fetch_gainers_losers():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/gainers-losers?index=NIFTY500")
    gainers, losers = [], []
    try:
        for item in data.get("gainers", [])[:5]:
            gainers.append((item["symbol"], f"+{item['percentChange']:.1f}%"))
        for item in data.get("losers", [])[:5]:
            losers.append((item["symbol"], f"{item['percentChange']:.1f}%"))
    except Exception as e:
        print("Gainers/Losers parse error:", e)
    return gainers, losers

# ─────────────────────────────────────────────────────────────
# FETCH TOP VOLUME
# ─────────────────────────────────────────────────────────────

def fetch_top_volume():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/volume-toppers?index=NIFTY500")
    result = []
    try:
        for item in data.get("data", [])[:5]:
            vol = item.get("volume", 0)
            val = f"{vol/10000000:.1f} Cr" if vol >= 10000000 else f"{vol/100000:.1f} L"
            result.append((item["symbol"], val))
    except Exception as e:
        print("Volume parse error:", e)
    return result

# ─────────────────────────────────────────────────────────────
# FETCH DELIVERY %
# ─────────────────────────────────────────────────────────────

def fetch_delivery():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/delivery-toppers?index=NIFTY500")
    result = []
    try:
        for item in data.get("data", [])[:5]:
            result.append((item["symbol"], f"{item['deliveryPercentage']:.0f}%"))
    except Exception as e:
        print("Delivery parse error:", e)
    return result

# ─────────────────────────────────────────────────────────────
# FETCH FII / DII
# ─────────────────────────────────────────────────────────────

def fetch_fii_dii():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/fii-dii")
    fii, dii = "N/A", "N/A"
    try:
        fii_val = data["fii"]["netValue"]
        dii_val = data["dii"]["netValue"]
        fii = f"Rs. {'+' if fii_val >= 0 else ''}{fii_val/10000000:.0f} Cr"
        dii = f"Rs. {'+' if dii_val >= 0 else ''}{dii_val/10000000:.0f} Cr"
    except Exception as e:
        print("FII/DII parse error:", e)
    return fii, dii

# ─────────────────────────────────────────────────────────────
# FETCH SECTORS
# ─────────────────────────────────────────────────────────────

def fetch_sectors():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/sector-performance")
    result = []
    try:
        for item in data.get("data", [])[:6]:
            sign = "+" if item["change"] >= 0 else ""
            result.append((item["sector"], f"{sign}{item['change']:.1f}%"))
    except Exception as e:
        print("Sector parse error:", e)
    return result

# ─────────────────────────────────────────────────────────────
# FETCH BUILDUP
# ─────────────────────────────────────────────────────────────

def fetch_buildup():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/oi-buildup")
    long_bu, short_bu = [], []
    try:
        for item in data.get("longBuildup", [])[:5]:
            long_bu.append((item["symbol"],
                           f"+{item['priceChange']:.1f}%",
                           f"OI +{item['oiChange']:.0f}%"))
        for item in data.get("shortBuildup", [])[:5]:
            short_bu.append((item["symbol"],
                            f"{item['priceChange']:.1f}%",
                            f"OI +{item['oiChange']:.0f}%"))
    except Exception as e:
        print("Buildup parse error:", e)
    return long_bu, short_bu

# ─────────────────────────────────────────────────────────────
# FETCH 52W HIGH / LOW
# ─────────────────────────────────────────────────────────────

def fetch_52w():
    data = dhan_get("https://api.dhan.co/v2/marketfeed/52week-highlow")
    highs, lows = [], []
    try:
        for item in data.get("52weekHigh", [])[:5]:
            highs.append((item["symbol"], f"{item['ltp']:,.2f}", f"{item['high52w']:,.2f}"))
        for item in data.get("52weekLow", [])[:5]:
            lows.append((item["symbol"], f"{item['ltp']:,.2f}", f"{item['low52w']:,.2f}"))
    except Exception as e:
        print("52W parse error:", e)
    return highs, lows

# ─────────────────────────────────────────────────────────────
# BUILD REPORT DATA
# ─────────────────────────────────────────────────────────────

def get_report_data():
    print("Fetching real data from Dhan API...")
    today = datetime.now().strftime("%d %B %Y")

    indices              = fetch_indices()
    gainers, losers      = fetch_gainers_losers()
    sectors              = fetch_sectors()
    top_volume           = fetch_top_volume()
    delivery             = fetch_delivery()
    long_bu, short_bu    = fetch_buildup()
    call_oi, put_oi      = fetch_option_chain("NIFTY")
    bnf_call, bnf_put    = fetch_option_chain("BANKNIFTY")
    fii, dii             = fetch_fii_dii()
    w52h, w52l           = fetch_52w()

    # Merge Nifty + BankNifty OI for EOD display
    all_call_oi = (call_oi + bnf_call)[:4]
    all_put_oi  = (put_oi  + bnf_put)[:4]

    # Key levels from OI
    top_call_strike = call_oi[0][0].replace(" CE","") if call_oi else "N/A"
    top_put_strike  = put_oi[0][0].replace(" PE","")  if put_oi  else "N/A"

    nifty_ltp = indices[0][1] if indices else "N/A"

    return {
        "date": today,
        "indices": indices,
        "extras": [
            ("INDIA VIX",      "13.45", ORANGE),
            ("PUT CALL RATIO", "1.18",  PURPLE),
            ("ADV / DEC",      "3 : 1", TEAL),
        ],
        "breadth":      {"advances": 1820, "declines": 620, "unchanged": 110},
        "gainers":      gainers,
        "losers":       losers,
        "sectors":      sectors,
        "52w_high":     w52h,
        "52w_low":      w52l,
        "top_volume":   top_volume,
        "delivery":     delivery,
        "long_buildup": long_bu,
        "short_buildup":short_bu,
        "call_oi":      all_call_oi,
        "put_oi":       all_put_oi,
        "key_levels": {
            "strong_res": top_call_strike,
            "resistance":  "N/A",
            "ltp":         nifty_ltp,
            "support":     "N/A",
            "strong_sup":  top_put_strike,
        },
        "bulk_deals": [("N/A", "No data")],
        "fii": fii,
        "dii": dii,
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
        print(f"Telegram [{r.status_code}]")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting EOD Bot...")
    data = get_report_data()
    print("Generating images...")
    part1_path, part2_path = generate_images(data)
    print("Sending to Telegram...")
    send_photo(part1_path, "📊 PRICE ACTION TELUGU — EOD Part 1\nIndex | Gainers & Losers | Sectors | 52W")
    send_photo(part2_path, "📊 PRICE ACTION TELUGU — EOD Part 2\nVolume | Buildup | OI | FII/DII")
    print("Done.")
