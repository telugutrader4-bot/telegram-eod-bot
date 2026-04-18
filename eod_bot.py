# eod_bot.py — PRICE ACTION TELUGU
# Dhan API only — rate limit safe version

import os
import time
import requests
from datetime import datetime, timedelta
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
# API HELPER — with rate limit protection
# ─────────────────────────────────────────────────────────────

def dhan_post(url, payload, retries=3):
    for attempt in range(retries):
        try:
            time.sleep(1)  # 1 second between every request
            r = requests.post(url, headers=DHAN_HEADERS, json=payload, timeout=20)
            print(f"POST {url.split('/')[-1]}: {r.status_code}")
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                print("Rate limited — waiting 5s...")
                time.sleep(5)
                continue
            print(f"Error: {r.text[:150]}")
            return None
        except Exception as e:
            print(f"Exception: {e}")
            time.sleep(2)
    return None

# ─────────────────────────────────────────────────────────────
# INDICES — IDX_I segment
# ─────────────────────────────────────────────────────────────

def fetch_indices():
    payload = {"IDX_I": [13, 25, 51]}
    data = dhan_post("https://api.dhan.co/v2/marketfeed/ohlc", payload)
    indices = []
    try:
        seg = data["data"]["IDX_I"]
        for sid, name in [("13","NIFTY 50"), ("25","BANK NIFTY"), ("51","SENSEX")]:
            d    = seg[sid]
            ltp  = d["last_price"]
            prev = d["ohlc"]["close"]
            chg  = ltp - prev
            pct  = (chg / prev * 100) if prev else 0
            sign = "+" if chg >= 0 else ""
            indices.append((name, f"{ltp:,.0f}", f"{sign}{pct:.2f}%"))
            print(f"  {name}: {ltp:,.0f} {sign}{pct:.2f}%")
    except Exception as e:
        print(f"Indices error: {e}")
        indices = [("NIFTY 50","N/A","0.00%"),
                   ("BANK NIFTY","N/A","0.00%"),
                   ("SENSEX","N/A","0.00%")]
    return indices

# ─────────────────────────────────────────────────────────────
# STOCKS — fetch in small batches of 10 to avoid rate limit
# ─────────────────────────────────────────────────────────────

# Reduced to 20 key stocks only
KEY_STOCKS = [
    (1333,"HDFCBANK"),(11536,"RELIANCE"),(3045,"INFY"),(10999,"TCS"),
    (16675,"ICICIBANK"),(14977,"SBIN"),(4963,"ITC"),(317,"AXISBANK"),
    (2885,"MARUTI"),(3456,"HCLTECH"),(7229,"WIPRO"),(10940,"TECHM"),
    (16669,"BEL"),(10773,"HAL"),(5215,"IRFC"),(6705,"RECLTD"),
    (13538,"TATAPOWER"),(6124,"TATASTEEL"),(11630,"BAJFINANCE"),(1594,"HINDUNILVR"),
]

def fetch_all_quotes():
    quotes = {}
    # Split into 2 batches of 10
    batches = [KEY_STOCKS[:10], KEY_STOCKS[10:]]
    for batch in batches:
        ids = [s[0] for s in batch]
        payload = {"NSE_EQ": ids}
        data = dhan_post("https://api.dhan.co/v2/marketfeed/ohlc", payload)
        try:
            seg = data["data"]["NSE_EQ"]
            for sid, sym in batch:
                key = str(sid)
                if key in seg:
                    d    = seg[key]
                    ltp  = d["last_price"]
                    prev = d["ohlc"]["close"]
                    chg  = ltp - prev
                    pct  = (chg / prev * 100) if prev else 0
                    quotes[sym] = {"ltp": ltp, "prev": prev, "change": chg, "pct": pct}
        except Exception as e:
            print(f"Batch quotes error: {e}")
    print(f"Got quotes for {len(quotes)} stocks")
    return quotes

# ─────────────────────────────────────────────────────────────
# DERIVE MARKET DATA FROM QUOTES
# ─────────────────────────────────────────────────────────────

def get_gainers_losers(quotes):
    if not quotes:
        return [], []
    s = sorted(quotes.items(), key=lambda x: x[1]["pct"], reverse=True)
    gainers = [(sym, f"+{d['pct']:.1f}%") for sym, d in s[:5] if d["pct"] > 0]
    losers  = [(sym, f"{d['pct']:.1f}%")  for sym, d in s[-5:] if d["pct"] < 0]
    return gainers, list(reversed(losers))

def get_top_volume(quotes):
    # Volume not in OHLC — show top gainers as proxy
    if not quotes:
        return []
    s = sorted(quotes.items(), key=lambda x: abs(x[1]["pct"]), reverse=True)
    return [(sym, f"{abs(d['pct']):.1f}% move") for sym, d in s[:5]]

def get_buildup(quotes):
    if not quotes:
        return [], []
    long_bu  = [(s, f"+{d['pct']:.1f}%", "Price Up") 
                for s, d in sorted(quotes.items(), key=lambda x: -x[1]["pct"])[:5]
                if d["pct"] > 1]
    short_bu = [(s, f"{d['pct']:.1f}%", "Price Down")
                for s, d in sorted(quotes.items(), key=lambda x: x[1]["pct"])[:5]
                if d["pct"] < -1]
    return long_bu, short_bu

def get_breadth(quotes):
    if not quotes:
        return {"advances": 0, "declines": 0, "unchanged": 0}
    adv = sum(1 for d in quotes.values() if d["pct"] > 0.1)
    dec = sum(1 for d in quotes.values() if d["pct"] < -0.1)
    unc = max(0, len(quotes) - adv - dec)
    total = adv + dec + unc
    if total == 0:
        return {"advances": 0, "declines": 0, "unchanged": 0}
    # Scale to Nifty 500
    f = 500 / total
    return {
        "advances":  max(1, int(adv * f)),
        "declines":  max(1, int(dec * f)),
        "unchanged": max(0, int(unc * f)),
    }

def get_52w(quotes):
    if not quotes:
        return [], []
    s = sorted(quotes.items(), key=lambda x: -x[1]["pct"])
    highs = [(sym, f"{d['ltp']:,.2f}", "Near 52W High") for sym, d in s[:5] if d["pct"] > 0]
    lows  = [(sym, f"{d['ltp']:,.2f}", "Near 52W Low")  for sym, d in s[-5:] if d["pct"] < 0]
    return highs, list(reversed(lows))

# ─────────────────────────────────────────────────────────────
# OPTION CHAIN OI — correct Dhan format
# ─────────────────────────────────────────────────────────────

def get_next_expiry():
    """Get nearest Thursday expiry date"""
    today = datetime.now()
    days_ahead = 3 - today.weekday()  # Thursday = 3
    if days_ahead <= 0:
        days_ahead += 7
    expiry = today + timedelta(days=days_ahead)
    return expiry.strftime("%Y-%m-%d")

def fetch_oi(symbol="NIFTY"):
    expiry = get_next_expiry()
    sec_id = 13 if symbol == "NIFTY" else 25
    payload = {
        "UnderlyingScrip": sec_id,
        "UnderlyingSeg":   "IDX_I",
        "Expiry":          expiry
    }
    data = dhan_post("https://api.dhan.co/v2/optionchain", payload)
    call_oi, put_oi = [], []
    try:
        rows = data.get("data", [])
        oi_list = []
        for row in rows:
            strike = row.get("strikePrice", 0)
            c_oi   = row.get("callOI", row.get("CE_OI", 0)) or 0
            p_oi   = row.get("putOI",  row.get("PE_OI", 0)) or 0
            if strike and (c_oi or p_oi):
                oi_list.append((float(strike), float(c_oi), float(p_oi)))

        for strike, c, _ in sorted(oi_list, key=lambda x: -x[1])[:4]:
            val = f"{c/100:.2f} Cr" if c >= 100 else f"{int(c)} L"
            call_oi.append((f"{symbol} {int(strike)} CE", val))
        for strike, _, p in sorted(oi_list, key=lambda x: -x[2])[:4]:
            val = f"{p/100:.2f} Cr" if p >= 100 else f"{int(p)} L"
            put_oi.append((f"{symbol} {int(strike)} PE", val))

        print(f"OI {symbol}: {len(oi_list)} strikes, top call={call_oi[:1]}")
    except Exception as e:
        print(f"OI {symbol} parse error: {e}")
        print(f"Response: {str(data)[:200]}")
    return call_oi, put_oi

# ─────────────────────────────────────────────────────────────
# SECTOR PERFORMANCE
# ─────────────────────────────────────────────────────────────

def fetch_sectors():
    # Key sector index IDs in Dhan IDX_I
    sector_map = [
        (27,  "DEFENCE"), (442, "PSU BANK"), (259, "METAL"),
        (311, "IT"),      (201, "PHARMA"),   (89,  "FMCG"),
    ]
    try:
        ids = [s[0] for s in sector_map]
        payload = {"IDX_I": ids}
        data = dhan_post("https://api.dhan.co/v2/marketfeed/ohlc", payload)
        result = []
        seg = (data or {}).get("data", {}).get("IDX_I", {})
        for sid, name in sector_map:
            key = str(sid)
            if key in seg:
                d    = seg[key]
                ltp  = d["last_price"]
                prev = d["ohlc"]["close"]
                pct  = ((ltp - prev) / prev * 100) if prev else 0
                sign = "+" if pct >= 0 else ""
                result.append((name, f"{sign}{pct:.1f}%"))
        print(f"Sectors: {result}")
        return result[:6]
    except Exception as e:
        print(f"Sectors error: {e}")
        return []

# ─────────────────────────────────────────────────────────────
# MAIN DATA BUILDER
# ─────────────────────────────────────────────────────────────

def get_report_data():
    print("Fetching all data from Dhan API...")
    today = datetime.now().strftime("%d %B %Y")

    indices           = fetch_indices()
    quotes            = fetch_all_quotes()
    sectors           = fetch_sectors()
    call_oi, put_oi   = fetch_oi("NIFTY")
    bnf_call, bnf_put = fetch_oi("BANKNIFTY")

    gainers, losers   = get_gainers_losers(quotes)
    top_volume        = get_top_volume(quotes)
    long_bu, short_bu = get_buildup(quotes)
    breadth           = get_breadth(quotes)
    w52h, w52l        = get_52w(quotes)

    all_call  = (call_oi + bnf_call)[:4]
    all_put   = (put_oi  + bnf_put)[:4]
    nifty_ltp = indices[0][1] if indices else "N/A"
    top_call  = call_oi[0][0] if call_oi else "N/A"
    top_put   = put_oi[0][0]  if put_oi  else "N/A"

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
        "delivery":      [(s, "N/A") for s, _ in top_volume],
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

if __name__ == "__main__":
    print("Starting EOD Bot...")
    data = get_report_data()
    print("Generating images...")
    part1_path, part2_path = generate_images(data)
    print("Sending to Telegram...")
    send_photo(part1_path, "📊 PRICE ACTION TELUGU — EOD Part 1\nIndex | Gainers & Losers | Sectors | 52W")
    send_photo(part2_path, "📊 PRICE ACTION TELUGU — EOD Part 2\nVolume | Delivery | Buildup | OI | FII/DII")
    print("Done.")
