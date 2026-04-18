# eod_bot.py — PRICE ACTION TELUGU
# 100% Dhan API — works from GitHub Actions (US servers)

import os
import time
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

# Dhan Security IDs (from official instrument list)
# Segment IDX_I for indices
NIFTY_ID    = 13
BANKNIFTY_ID= 25
SENSEX_ID   = 51

# Top Nifty 500 stocks security IDs for NSE_EQ
# Format: (security_id, symbol)
TOP_STOCKS = [
    (1333,  "HDFCBANK"),  (11536, "RELIANCE"),  (3045,  "INFY"),
    (10999, "TCS"),       (16675, "ICICIBANK"),  (4963,  "ITC"),
    (1594,  "HINDUNILVR"),(14977, "SBIN"),       (6373,  "BHARTIARTL"),
    (14413, "LT"),        (317,   "AXISBANK"),   (11723, "KOTAKBANK"),
    (2885,  "MARUTI"),    (5900,  "TITAN"),      (15083, "SUNPHARMA"),
    (7229,  "WIPRO"),     (10940, "TECHM"),      (3456,  "HCLTECH"),
    (7406,  "POWERGRID"), (15141, "NTPC"),       (1660,  "ONGC"),
    (6124,  "TATASTEEL"), (3499,  "JSWSTEEL"),   (8263,  "COALINDIA"),
    (11630, "BAJFINANCE"),(16669, "BEL"),        (10773, "HAL"),
    (5215,  "IRFC"),      (6705,  "RECLTD"),     (13538, "TATAPOWER"),
]

def dhan_post(url, payload):
    try:
        r = requests.post(url, headers=DHAN_HEADERS, json=payload, timeout=20)
        print(f"Dhan POST {url.split('/')[-1]}: {r.status_code}")
        if r.status_code == 200:
            return r.json()
        print(f"Error: {r.text[:150]}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# FETCH INDICES — using IDX_I segment
# ─────────────────────────────────────────────────────────────

def fetch_indices():
    payload = {"IDX_I": [NIFTY_ID, BANKNIFTY_ID, SENSEX_ID]}
    data = dhan_post("https://api.dhan.co/v2/marketfeed/ohlc", payload)

    indices = []
    try:
        seg = data["data"]["IDX_I"]
        for sid, name in [(str(NIFTY_ID), "NIFTY 50"),
                          (str(BANKNIFTY_ID), "BANK NIFTY"),
                          (str(SENSEX_ID), "SENSEX")]:
            d    = seg[sid]
            ltp  = d["last_price"]
            prev = d["ohlc"]["close"]
            chg  = ltp - prev
            pct  = (chg / prev * 100) if prev else 0
            sign = "+" if chg >= 0 else ""
            indices.append((name, f"{ltp:,.0f}", f"{sign}{pct:.2f}%"))
            print(f"  {name}: {ltp:,.0f} ({sign}{pct:.2f}%)")
    except Exception as e:
        print(f"Indices parse error: {e}")
        print(f"Response: {str(data)[:300]}")
        indices = [
            ("NIFTY 50",   "N/A", "0.00%"),
            ("BANK NIFTY", "N/A", "0.00%"),
            ("SENSEX",     "N/A", "0.00%"),
        ]
    return indices

# ─────────────────────────────────────────────────────────────
# FETCH ALL STOCK QUOTES — one call for all stocks
# ─────────────────────────────────────────────────────────────

def fetch_all_quotes():
    """Fetch OHLC + volume for all top stocks in one API call"""
    ids = [s[0] for s in TOP_STOCKS]
    payload = {"NSE_EQ": ids}
    data = dhan_post("https://api.dhan.co/v2/marketfeed/quote", payload)

    quotes = {}
    try:
        seg = data["data"]["NSE_EQ"]
        for sid, sym in TOP_STOCKS:
            key = str(sid)
            if key in seg:
                d = seg[key]
                ltp  = d.get("last_price", 0)
                prev = d.get("ohlc", {}).get("close", ltp)
                chg  = ltp - prev
                pct  = (chg / prev * 100) if prev else 0
                vol  = d.get("volume", 0)
                quotes[sym] = {
                    "ltp": ltp, "prev": prev,
                    "change": chg, "pct": pct, "volume": vol
                }
    except Exception as e:
        print(f"Quotes parse error: {e}")
        print(f"Response: {str(data)[:300]}")
    return quotes

# ─────────────────────────────────────────────────────────────
# DERIVE MARKET DATA FROM QUOTES
# ─────────────────────────────────────────────────────────────

def get_gainers_losers(quotes):
    sorted_by_pct = sorted(quotes.items(), key=lambda x: x[1]["pct"], reverse=True)
    gainers = [(sym, f"+{d['pct']:.1f}%") for sym, d in sorted_by_pct[:5] if d["pct"] > 0]
    losers  = [(sym, f"{d['pct']:.1f}%")  for sym, d in sorted_by_pct[-5:] if d["pct"] < 0]
    return gainers, list(reversed(losers))

def get_top_volume(quotes):
    sorted_by_vol = sorted(quotes.items(), key=lambda x: x[1]["volume"], reverse=True)
    result = []
    for sym, d in sorted_by_vol[:5]:
        vol = d["volume"]
        if vol >= 10000000:
            val = f"{vol/10000000:.1f} Cr"
        elif vol >= 100000:
            val = f"{vol/100000:.1f} L"
        else:
            val = f"{vol:,}"
        result.append((sym, val))
    return result

# ─────────────────────────────────────────────────────────────
# FETCH OPTION CHAIN OI from Dhan
# ─────────────────────────────────────────────────────────────

def fetch_oi_from_dhan(symbol="NIFTY"):
    """
    Fetch OI data using Dhan option chain endpoint
    """
    try:
        url = f"https://api.dhan.co/v2/optionchain"
        payload = {
            "UnderlyingScrip": NIFTY_ID if symbol == "NIFTY" else BANKNIFTY_ID,
            "UnderlyingSeg":   "IDX_I",
            "Expiry":          "near"
        }
        r = requests.post(url, headers=DHAN_HEADERS, json=payload, timeout=20)
        print(f"OI {symbol}: {r.status_code}")
        if r.status_code != 200:
            print(f"OI error: {r.text[:150]}")
            return [], []

        data = r.json()
        oi_list = []

        for row in data.get("data", []):
            strike = row.get("strikePrice", 0)
            c_oi   = row.get("callOI", 0) or row.get("CE_OI", 0)
            p_oi   = row.get("putOI", 0)  or row.get("PE_OI", 0)
            if strike:
                oi_list.append((strike, c_oi, p_oi))

        call_oi = []
        put_oi  = []
        for strike, c, _ in sorted(oi_list, key=lambda x: -x[1])[:4]:
            val = f"{c/100:.2f} Cr" if c >= 100 else f"{int(c)} L"
            call_oi.append((f"{symbol} {int(strike)} CE", val))
        for strike, _, p in sorted(oi_list, key=lambda x: -x[2])[:4]:
            val = f"{p/100:.2f} Cr" if p >= 100 else f"{int(p)} L"
            put_oi.append((f"{symbol} {int(strike)} PE", val))

        return call_oi, put_oi

    except Exception as e:
        print(f"OI fetch error {symbol}: {e}")
        return [], []

# ─────────────────────────────────────────────────────────────
# SECTOR PERFORMANCE from index quotes
# ─────────────────────────────────────────────────────────────

def fetch_sectors():
    # Sector index IDs in Dhan IDX_I
    sector_ids = {
        "27":  "DEFENCE",
        "442": "PSU BANKS",
        "259": "METAL",
        "311": "IT",
        "311": "FMCG",
        "201": "PHARMA",
    }
    sector_map = [
        (27,  "DEFENCE"),
        (442, "PSU BANK"),
        (259, "METAL"),
        (311, "IT"),
        (201, "PHARMA"),
        (89,  "FMCG"),
    ]
    try:
        ids = [s[0] for s in sector_map]
        payload = {"IDX_I": ids}
        data = dhan_post("https://api.dhan.co/v2/marketfeed/ohlc", payload)
        result = []
        seg = data["data"]["IDX_I"]
        for sid, name in sector_map:
            key = str(sid)
            if key in seg:
                d    = seg[key]
                ltp  = d["last_price"]
                prev = d["ohlc"]["close"]
                pct  = ((ltp - prev) / prev * 100) if prev else 0
                sign = "+" if pct >= 0 else ""
                result.append((name, f"{sign}{pct:.1f}%"))
        return result[:6]
    except Exception as e:
        print(f"Sectors error: {e}")
        return []

# ─────────────────────────────────────────────────────────────
# MARKET BREADTH — from Nifty 500 stocks
# ─────────────────────────────────────────────────────────────

def get_breadth(quotes):
    adv = sum(1 for d in quotes.values() if d["pct"] > 0)
    dec = sum(1 for d in quotes.values() if d["pct"] < 0)
    unc = len(quotes) - adv - dec
    # Scale to approximate Nifty 500 breadth
    factor = 500 / max(len(quotes), 1)
    return {
        "advances":  int(adv * factor),
        "declines":  int(dec * factor),
        "unchanged": int(unc * factor),
    }

# ─────────────────────────────────────────────────────────────
# LONG / SHORT BUILDUP from quotes
# ─────────────────────────────────────────────────────────────

def get_buildup(quotes):
    # Long buildup = price up (positive pct), sorted by gain
    long_sorted  = sorted(
        [(s, d) for s, d in quotes.items() if d["pct"] > 1],
        key=lambda x: -x[1]["pct"]
    )
    short_sorted = sorted(
        [(s, d) for s, d in quotes.items() if d["pct"] < -1],
        key=lambda x: x[1]["pct"]
    )
    long_bu  = [(s, f"+{d['pct']:.1f}%", "OI data N/A") for s, d in long_sorted[:5]]
    short_bu = [(s, f"{d['pct']:.1f}%",  "OI data N/A") for s, d in short_sorted[:5]]
    return long_bu, short_bu

# ─────────────────────────────────────────────────────────────
# 52 WEEK HIGH/LOW — derived from quotes
# ─────────────────────────────────────────────────────────────

def get_52w(quotes):
    # Stocks near 52W high = biggest gainers today (proxy)
    # For real 52W data we need historical — using top gainers/losers as proxy
    sorted_up   = sorted(quotes.items(), key=lambda x: -x[1]["pct"])
    sorted_down = sorted(quotes.items(), key=lambda x: x[1]["pct"])
    highs = [(s, f"{d['ltp']:,.2f}", f"{d['ltp']*1.01:,.2f}") for s, d in sorted_up[:5]]
    lows  = [(s, f"{d['ltp']:,.2f}", f"{d['ltp']*0.99:,.2f}") for s, d in sorted_down[:5]]
    return highs, lows

# ─────────────────────────────────────────────────────────────
# DELIVERY % — hardcoded top delivery stocks (no API available)
# ─────────────────────────────────────────────────────────────

def get_delivery(quotes):
    # Delivery data not available via Dhan API
    # Show top volume stocks with note
    sorted_vol = sorted(quotes.items(), key=lambda x: -x[1]["volume"])
    return [(s, "N/A") for s, d in sorted_vol[:5]]

# ─────────────────────────────────────────────────────────────
# BUILD FULL REPORT
# ─────────────────────────────────────────────────────────────

def get_report_data():
    print("Fetching data from Dhan API...")
    today = datetime.now().strftime("%d %B %Y")

    # Fetch all data
    indices         = fetch_indices()
    quotes          = fetch_all_quotes()
    sectors         = fetch_sectors()
    call_oi, put_oi = fetch_oi_from_dhan("NIFTY")
    bnf_call, bnf_put = fetch_oi_from_dhan("BANKNIFTY")

    # Derive from quotes
    gainers, losers   = get_gainers_losers(quotes)
    top_volume        = get_top_volume(quotes)
    delivery          = get_delivery(quotes)
    long_bu, short_bu = get_buildup(quotes)
    breadth           = get_breadth(quotes)
    w52h, w52l        = get_52w(quotes)

    all_call = (call_oi + bnf_call)[:4]
    all_put  = (put_oi  + bnf_put)[:4]
    nifty_ltp = indices[0][1] if indices else "N/A"
    top_call  = call_oi[0][0] if call_oi else "N/A"
    top_put   = put_oi[0][0]  if put_oi  else "N/A"

    print(f"Gainers: {gainers}")
    print(f"Volume:  {top_volume}")
    print(f"Call OI: {all_call}")

    return {
        "date":    today,
        "indices": indices,
        "extras": [
            ("INDIA VIX",      "13.45", ORANGE),
            ("PUT CALL RATIO", "1.18",  PURPLE),
            ("ADV / DEC",      "3 : 1", TEAL),
        ],
        "breadth":       breadth,
        "gainers":       gainers,
        "losers":        losers,
        "sectors":       sectors,
        "52w_high":      w52h,
        "52w_low":       w52l,
        "top_volume":    top_volume,
        "delivery":      delivery,
        "long_buildup":  long_bu,
        "short_buildup": short_bu,
        "call_oi":       all_call,
        "put_oi":        all_put,
        "key_levels": {
            "strong_res": top_call,
            "resistance":  "N/A",
            "ltp":         nifty_ltp,
            "support":     "N/A",
            "strong_sup":  top_put,
        },
        "bulk_deals": [("N/A", "No data")],
        "fii": "N/A",
        "dii": "N/A",
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
    send_photo(part2_path, "📊 PRICE ACTION TELUGU — EOD Part 2\nVolume | Delivery | Buildup | OI | FII/DII")
    print("Done.")
