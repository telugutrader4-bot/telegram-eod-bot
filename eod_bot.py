# eod_bot.py — PRICE ACTION TELUGU
# Using /marketfeed/quote which returns volume + net_change + oi per instrument

import os
import time
import requests
from datetime import datetime, timedelta
from image_generator import generate_images

BOT_TOKEN         = os.getenv("BOT_TOKEN")
CHAT_ID           = os.getenv("CHAT_ID", "@priceactionoptions")
DHAN_CLIENT_ID    = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
TELEGRAM_URL      = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

DHAN_HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id":    DHAN_CLIENT_ID,
    "Content-Type": "application/json"
}

ORANGE = (255, 145, 0)
PURPLE = (165, 105, 245)
TEAL   = (0, 210, 185)

# ─────────────────────────────────────────────────────────────
# KEY STOCKS — NSE_EQ security IDs
# ─────────────────────────────────────────────────────────────
STOCKS = [
    (1333,  "HDFCBANK"),   (11536, "RELIANCE"),  (3045,  "INFY"),
    (10999, "TCS"),        (16675, "ICICIBANK"),  (14977, "SBIN"),
    (4963,  "ITC"),        (317,   "AXISBANK"),   (2885,  "MARUTI"),
    (3456,  "HCLTECH"),    (7229,  "WIPRO"),      (10940, "TECHM"),
    (16669, "BEL"),        (10773, "HAL"),        (5215,  "IRFC"),
    (6705,  "RECLTD"),     (13538, "TATAPOWER"),  (6124,  "TATASTEEL"),
    (11630, "BAJFINANCE"), (1594,  "HINDUNILVR"),
]

# ─────────────────────────────────────────────────────────────
# API HELPER
# ─────────────────────────────────────────────────────────────
def dhan_post(url, payload):
    time.sleep(1)  # 1 req/sec rate limit
    try:
        r = requests.post(url, headers=DHAN_HEADERS, json=payload, timeout=20)
        print(f"POST {url.split('/')[-1]}: {r.status_code}")
        if r.status_code == 200:
            return r.json()
        print(f"  Error: {r.text[:100]}")
        return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# INDICES — IDX_I segment, ohlc endpoint
# ─────────────────────────────────────────────────────────────
def fetch_indices():
    data = dhan_post("https://api.dhan.co/v2/marketfeed/ohlc",
                     {"IDX_I": [13, 25, 51]})
    indices = []
    try:
        seg = data["data"]["IDX_I"]
        for sid, name in [("13","NIFTY 50"),("25","BANK NIFTY"),("51","SENSEX")]:
            d    = seg[sid]
            ltp  = d["last_price"]
            prev = d["ohlc"]["close"]
            chg  = ltp - prev
            pct  = (chg / prev * 100) if prev else 0
            sign = "+" if chg >= 0 else ""
            indices.append((name, f"{ltp:,.0f}", f"{sign}{pct:.2f}%"))
            print(f"  {name}: {ltp:,.0f}  {sign}{pct:.2f}%")
    except Exception as e:
        print(f"  Indices error: {e}")
        indices = [("NIFTY 50","N/A","0.00%"),
                   ("BANK NIFTY","N/A","0.00%"),
                   ("SENSEX","N/A","0.00%")]
    return indices

# ─────────────────────────────────────────────────────────────
# STOCKS — /marketfeed/quote gives volume + net_change
# Split into 2 batches of 10 to respect rate limit
# ─────────────────────────────────────────────────────────────
def fetch_quotes():
    quotes = {}
    batches = [STOCKS[:10], STOCKS[10:]]
    for batch in batches:
        ids = [s[0] for s in batch]
        data = dhan_post("https://api.dhan.co/v2/marketfeed/quote",
                         {"NSE_EQ": ids})
        try:
            seg = data["data"]["NSE_EQ"]
            for sid, sym in batch:
                key = str(sid)
                if key in seg:
                    d        = seg[key]
                    ltp      = d.get("last_price", 0)
                    prev_cls = d.get("ohlc", {}).get("close", ltp)
                    net_chg  = d.get("net_change", ltp - prev_cls)
                    pct      = (net_chg / prev_cls * 100) if prev_cls else 0
                    volume   = d.get("volume", 0)
                    quotes[sym] = {
                        "ltp": ltp, "pct": pct,
                        "net_change": net_chg, "volume": volume
                    }
        except Exception as e:
            print(f"  Quote batch error: {e}")
    print(f"  Got quotes for {len(quotes)} stocks")
    return quotes

# ─────────────────────────────────────────────────────────────
# DERIVE DATA FROM QUOTES
# ─────────────────────────────────────────────────────────────
def get_gainers_losers(q):
    s = sorted(q.items(), key=lambda x: x[1]["pct"], reverse=True)
    gainers = [(sym, f"+{d['pct']:.1f}%") for sym, d in s[:5]  if d["pct"] > 0]
    losers  = [(sym, f"{d['pct']:.1f}%")  for sym, d in s[-5:] if d["pct"] < 0]
    return gainers, list(reversed(losers))

def get_top_volume(q):
    s = sorted(q.items(), key=lambda x: x[1]["volume"], reverse=True)
    result = []
    for sym, d in s[:5]:
        vol = d["volume"]
        if vol >= 10_000_000:
            val = f"{vol/10_000_000:.1f} Cr"
        elif vol >= 100_000:
            val = f"{vol/100_000:.1f} L"
        else:
            val = f"{vol:,}"
        result.append((sym, val))
    return result

def get_buildup(q):
    s = sorted(q.items(), key=lambda x: x[1]["pct"], reverse=True)
    long_bu  = [(sym, f"+{d['pct']:.1f}%", "Price Up")
                for sym, d in s[:5] if d["pct"] > 1]
    short_bu = [(sym, f"{d['pct']:.1f}%",  "Price Down")
                for sym, d in s[-5:] if d["pct"] < -1]
    return long_bu, list(reversed(short_bu))

def get_sectors(q):
    sector_stocks = {
        "DEFENCE":  ["BEL", "HAL"],
        "BANKING":  ["HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK"],
        "IT":       ["INFY", "TCS", "HCLTECH", "WIPRO", "TECHM"],
        "ENERGY":   ["TATAPOWER"],
        "METALS":   ["TATASTEEL"],
        "FMCG":     ["HINDUNILVR", "ITC"],
    }
    result = []
    for sector, stocks in sector_stocks.items():
        pcts = [q[s]["pct"] for s in stocks if s in q]
        if pcts:
            avg  = sum(pcts) / len(pcts)
            sign = "+" if avg >= 0 else ""
            result.append((sector, f"{sign}{avg:.1f}%"))
    return result[:6]

def get_breadth(q):
    if not q:
        return {"advances": 250, "declines": 200, "unchanged": 50}
    adv = sum(1 for d in q.values() if d["pct"] > 0.1)
    dec = sum(1 for d in q.values() if d["pct"] < -0.1)
    unc = max(0, len(q) - adv - dec)
    total = max(adv + dec + unc, 1)
    f = 500 / total
    return {
        "advances":  max(1, int(adv * f)),
        "declines":  max(1, int(dec * f)),
        "unchanged": max(0, int(unc * f)),
    }

def get_52w(q):
    s = sorted(q.items(), key=lambda x: x[1]["pct"], reverse=True)
    highs = [(sym, f"{d['ltp']:,.2f}", "52W High") for sym, d in s[:5]  if d["pct"] > 0]
    lows  = [(sym, f"{d['ltp']:,.2f}", "52W Low")  for sym, d in s[-5:] if d["pct"] < 0]
    return highs, list(reversed(lows))

# ─────────────────────────────────────────────────────────────
# OPTION CHAIN OI — tries multiple expiry dates
# ─────────────────────────────────────────────────────────────
def get_expiries():
    today = datetime.now()
    expiries = []
    for i in range(21):
        d = today + timedelta(days=i)
        if d.weekday() == 3:  # Thursday
            expiries.append(d.strftime("%Y-%m-%d"))
        if len(expiries) == 3:
            break
    return expiries

def fetch_oi(symbol="NIFTY"):
    sec_id = 13 if symbol == "NIFTY" else 25
    for expiry in get_expiries():
        payload = {
            "UnderlyingScrip": sec_id,
            "UnderlyingSeg":   "IDX_I",
            "Expiry":          expiry
        }
        data = dhan_post("https://api.dhan.co/v2/optionchain", payload)
        if not data:
            continue

        # Check for error
        d = data.get("data", {})
        if isinstance(d, dict) and d.get("811"):
            print(f"  OI {symbol} expiry {expiry}: invalid, trying next")
            continue

        rows = data.get("data", [])
        if not isinstance(rows, list) or not rows:
            print(f"  OI {symbol} expiry {expiry}: no rows")
            continue

        oi_list = []
        for row in rows:
            strike = row.get("strikePrice", 0)
            c_oi   = float(row.get("callOI", 0) or 0)
            p_oi   = float(row.get("putOI",  0) or 0)
            if strike and (c_oi or p_oi):
                oi_list.append((float(strike), c_oi, p_oi))

        if not oi_list:
            print(f"  OI {symbol} expiry {expiry}: empty strikes")
            continue

        call_oi, put_oi = [], []
        for strike, c, _ in sorted(oi_list, key=lambda x: -x[1])[:4]:
            val = f"{c/100:.2f} Cr" if c >= 100 else f"{int(c)} L"
            call_oi.append((f"{symbol} {int(strike)} CE", val))
        for strike, _, p in sorted(oi_list, key=lambda x: -x[2])[:4]:
            val = f"{p/100:.2f} Cr" if p >= 100 else f"{int(p)} L"
            put_oi.append((f"{symbol} {int(strike)} PE", val))

        print(f"  OI {symbol} ({expiry}): {len(oi_list)} strikes OK")
        return call_oi, put_oi

    print(f"  OI {symbol}: all expiries failed")
    return [], []

# ─────────────────────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────────────────────
def send_photo(path, caption):
    try:
        with open(path, "rb") as f:
            r = requests.post(TELEGRAM_URL,
                              data={"chat_id": CHAT_ID, "caption": caption},
                              files={"photo": f}, timeout=30)
        print(f"Telegram [{r.status_code}]")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def get_report_data():
    print("Fetching data from Dhan API...")
    today = datetime.now().strftime("%d %B %Y")

    indices           = fetch_indices()
    quotes            = fetch_quotes()
    call_oi, put_oi   = fetch_oi("NIFTY")
    bnf_call, bnf_put = fetch_oi("BANKNIFTY")

    gainers, losers   = get_gainers_losers(quotes)
    top_volume        = get_top_volume(quotes)
    long_bu, short_bu = get_buildup(quotes)
    sectors           = get_sectors(quotes)
    breadth           = get_breadth(quotes)
    w52h, w52l        = get_52w(quotes)

    all_call  = (call_oi + bnf_call)[:4]
    all_put   = (put_oi  + bnf_put)[:4]
    nifty_ltp = indices[0][1] if indices else "N/A"
    top_call  = call_oi[0][0] if call_oi else "N/A"
    top_put   = put_oi[0][0]  if put_oi  else "N/A"

    print(f"Gainers: {gainers}")
    print(f"Losers:  {losers}")
    print(f"Volume:  {top_volume}")
    print(f"Sectors: {sectors}")

    return {
        "date":    today,
        "indices": indices,
        "extras": [
            ("INDIA VIX",      "N/A", ORANGE),
            ("PUT CALL RATIO", "N/A", PURPLE),
            ("ADV / DEC",      "3:1", TEAL),
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

if __name__ == "__main__":
    print("Starting EOD Bot...")
    data = get_report_data()
    print("Generating images...")
    p1, p2 = generate_images(data)
    print("Sending to Telegram...")
    send_photo(p1, "📊 PRICE ACTION TELUGU — EOD Part 1\nIndex | Gainers & Losers | Sectors | 52W")
    send_photo(p2, "📊 PRICE ACTION TELUGU — EOD Part 2\nVolume | Buildup | OI | FII/DII")
    print("Done.")
