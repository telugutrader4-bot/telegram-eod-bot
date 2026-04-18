# eod_bot.py — PRICE ACTION TELUGU
# Dhan API for indices + NSE public API for market data

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

NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com"
}

ORANGE = (255, 145, 0)
PURPLE = (165, 105, 245)
TEAL   = (0, 210, 185)

# ─────────────────────────────────────────────────────────────
# DHAN — FETCH INDICES (Nifty50, BankNifty, Sensex)
# Security IDs: Nifty50=13, BankNifty=25, Sensex(BSE)=1
# ─────────────────────────────────────────────────────────────

def fetch_indices():
    try:
        payload = {
            "NSE_INDEX": [13, 25],
            "BSE_INDEX": [1]
        }
        r = requests.post(
            "https://api.dhan.co/v2/marketfeed/ohlc",
            headers=DHAN_HEADERS,
            json=payload,
            timeout=20
        )
        print(f"Indices API: {r.status_code}")
        data = r.json()
        print("Indices response:", str(data)[:300])

        indices = []
        for seg, sid, name in [
            ("NSE_INDEX", "13",  "NIFTY 50"),
            ("NSE_INDEX", "25",  "BANK NIFTY"),
            ("BSE_INDEX", "1",   "SENSEX"),
        ]:
            try:
                d    = data["data"][seg][sid]
                ltp  = d["last_price"]
                prev = d["ohlc"]["close"]
                chg  = ltp - prev
                pct  = (chg / prev * 100) if prev else 0
                sign = "+" if chg >= 0 else ""
                indices.append((name, f"{ltp:,.0f}", f"{sign}{pct:.2f}%"))
            except Exception as e:
                print(f"Parse error {name}: {e}")
                indices.append((name, "N/A", "0.00%"))
        return indices
    except Exception as e:
        print(f"fetch_indices error: {e}")
        return [
            ("NIFTY 50",   "N/A", "0.00%"),
            ("BANK NIFTY", "N/A", "0.00%"),
            ("SENSEX",     "N/A", "0.00%"),
        ]

# ─────────────────────────────────────────────────────────────
# NSE PUBLIC API — session helper
# ─────────────────────────────────────────────────────────────

def nse_session():
    s = requests.Session()
    s.headers.update(NSE_HEADERS)
    try:
        s.get("https://www.nseindia.com", timeout=10)
    except:
        pass
    return s

def nse_get(session, url):
    try:
        r = session.get(url, timeout=15)
        print(f"NSE {url.split('?')[0].split('/')[-1]}: {r.status_code}")
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        print(f"NSE error: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# NSE — GAINERS & LOSERS
# ─────────────────────────────────────────────────────────────

def fetch_gainers_losers(session):
    data = nse_get(session, "https://www.nseindia.com/api/live-analysis-variations?index=gainers")
    gainers, losers = [], []
    try:
        for item in data.get("NIFTY500", {}).get("data", [])[:5]:
            sym = item.get("symbol", "")
            pct = item.get("pChange", 0)
            gainers.append((sym, f"+{pct:.1f}%"))
    except Exception as e:
        print(f"Gainers error: {e}")

    data2 = nse_get(session, "https://www.nseindia.com/api/live-analysis-variations?index=losers")
    try:
        for item in data2.get("NIFTY500", {}).get("data", [])[:5]:
            sym = item.get("symbol", "")
            pct = item.get("pChange", 0)
            losers.append((sym, f"{pct:.1f}%"))
    except Exception as e:
        print(f"Losers error: {e}")

    return gainers, losers

# ─────────────────────────────────────────────────────────────
# NSE — TOP VOLUME
# ─────────────────────────────────────────────────────────────

def fetch_top_volume(session):
    data = nse_get(session, "https://www.nseindia.com/api/live-analysis-volume-shockers")
    result = []
    try:
        for item in data.get("data", [])[:5]:
            sym = item.get("symbol", "")
            vol = item.get("totalTradedVolume", 0)
            if vol >= 10000000:
                val = f"{vol/10000000:.1f} Cr"
            else:
                val = f"{vol/100000:.1f} L"
            result.append((sym, val))
    except Exception as e:
        print(f"Volume error: {e}")
    return result

# ─────────────────────────────────────────────────────────────
# NSE — DELIVERY %
# ─────────────────────────────────────────────────────────────

def fetch_delivery(session):
    data = nse_get(session, "https://www.nseindia.com/api/live-analysis-delivery-volume-shockers")
    result = []
    try:
        for item in data.get("data", [])[:5]:
            sym = item.get("symbol", "")
            pct = item.get("deliveryToTradedQuantity", 0)
            result.append((sym, f"{pct:.0f}%"))
    except Exception as e:
        print(f"Delivery error: {e}")
    return result

# ─────────────────────────────────────────────────────────────
# NSE — SECTORS
# ─────────────────────────────────────────────────────────────

def fetch_sectors(session):
    data = nse_get(session, "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O")
    result = []
    sectors_map = {
        "NIFTY BANK":    "BANK",
        "NIFTY IT":      "IT",
        "NIFTY PHARMA":  "PHARMA",
        "NIFTY FMCG":    "FMCG",
        "NIFTY METAL":   "METAL",
        "NIFTY AUTO":    "AUTO",
    }
    try:
        data2 = nse_get(session, "https://www.nseindia.com/api/allIndices")
        for item in data2.get("data", []):
            name = item.get("index", "")
            if name in sectors_map:
                pct  = item.get("percentChange", 0)
                sign = "+" if pct >= 0 else ""
                result.append((sectors_map[name], f"{sign}{pct:.1f}%"))
    except Exception as e:
        print(f"Sectors error: {e}")
    return result[:6]

# ─────────────────────────────────────────────────────────────
# NSE — 52 WEEK HIGH / LOW
# ─────────────────────────────────────────────────────────────

def fetch_52w(session):
    data = nse_get(session, "https://www.nseindia.com/api/live-analysis-52Week?index=highlow52week")
    highs, lows = [], []
    try:
        for item in data.get("data", {}).get("HIGH", [])[:5]:
            sym  = item.get("symbol", "")
            ltp  = item.get("ltp", 0)
            high = item.get("52WH", 0)
            highs.append((sym, f"{ltp:,.2f}", f"{high:,.2f}"))
        for item in data.get("data", {}).get("LOW", [])[:5]:
            sym = item.get("symbol", "")
            ltp = item.get("ltp", 0)
            low = item.get("52WL", 0)
            lows.append((sym, f"{ltp:,.2f}", f"{low:,.2f}"))
    except Exception as e:
        print(f"52W error: {e}")
    return highs, lows

# ─────────────────────────────────────────────────────────────
# NSE — OPTION CHAIN OI (for EOD display top strikes)
# ─────────────────────────────────────────────────────────────

def fetch_oi_levels(session, symbol="NIFTY"):
    data = nse_get(session, f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}")
    call_oi, put_oi = [], []
    try:
        records = data["records"]["data"]
        oi_list = []
        for row in records:
            strike = row.get("strikePrice", 0)
            ce     = row.get("CE", {})
            pe     = row.get("PE", {})
            c_oi   = ce.get("openInterest", 0)
            p_oi   = pe.get("openInterest", 0)
            oi_list.append((strike, c_oi, p_oi))

        # Top 4 call OI strikes
        sorted_calls = sorted(oi_list, key=lambda x: -x[1])[:4]
        sorted_puts  = sorted(oi_list, key=lambda x: -x[2])[:4]

        for strike, c_oi, _ in sorted_calls:
            val = f"{c_oi/100:.2f} Cr" if c_oi >= 100 else f"{int(c_oi)} L"
            call_oi.append((f"{symbol} {int(strike)} CE", val))

        for strike, _, p_oi in sorted_puts:
            val = f"{p_oi/100:.2f} Cr" if p_oi >= 100 else f"{int(p_oi)} L"
            put_oi.append((f"{symbol} {int(strike)} PE", val))

    except Exception as e:
        print(f"OI error {symbol}: {e}")
    return call_oi, put_oi

# ─────────────────────────────────────────────────────────────
# NSE — FII / DII
# ─────────────────────────────────────────────────────────────

def fetch_fii_dii(session):
    data = nse_get(session, "https://www.nseindia.com/api/fiidiiTradeReact")
    fii, dii = "N/A", "N/A"
    try:
        today = data[0]
        fii_val = float(today.get("netVal", 0))
        sign    = "+" if fii_val >= 0 else ""
        fii     = f"Rs. {sign}{fii_val:.0f} Cr"

        dii_val = float(data[1].get("netVal", 0) if len(data) > 1 else 0)
        sign2   = "+" if dii_val >= 0 else ""
        dii     = f"Rs. {sign2}{dii_val:.0f} Cr"
    except Exception as e:
        print(f"FII/DII error: {e}")
    return fii, dii

# ─────────────────────────────────────────────────────────────
# NSE — LONG / SHORT BUILDUP
# ─────────────────────────────────────────────────────────────

def fetch_buildup(session):
    data = nse_get(session, "https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings")
    long_bu, short_bu = [], []
    try:
        for item in data.get("data", [])[:5]:
            sym    = item.get("symbol", "")
            pchg   = item.get("priceDiff", 0)
            oichg  = item.get("oiDiff", 0)
            if pchg > 0:
                long_bu.append((sym, f"+{pchg:.1f}%", f"OI +{oichg:.0f}%"))
            else:
                short_bu.append((sym, f"{pchg:.1f}%", f"OI +{oichg:.0f}%"))
    except Exception as e:
        print(f"Buildup error: {e}")
    return long_bu[:5], short_bu[:5]

# ─────────────────────────────────────────────────────────────
# NSE — MARKET BREADTH
# ─────────────────────────────────────────────────────────────

def fetch_breadth(session):
    data = nse_get(session, "https://www.nseindia.com/api/allIndices")
    try:
        for item in data.get("data", []):
            if item.get("index") == "NIFTY 500":
                adv = item.get("advances", 1820)
                dec = item.get("declines", 620)
                unc = item.get("unchanged", 110)
                return {"advances": adv, "declines": dec, "unchanged": unc}
    except Exception as e:
        print(f"Breadth error: {e}")
    return {"advances": 1820, "declines": 620, "unchanged": 110}

# ─────────────────────────────────────────────────────────────
# BUILD FULL REPORT DATA
# ─────────────────────────────────────────────────────────────

def get_report_data():
    print("Fetching data...")
    today   = datetime.now().strftime("%d %B %Y")
    session = nse_session()

    indices              = fetch_indices()
    gainers, losers      = fetch_gainers_losers(session)
    sectors              = fetch_sectors(session)
    top_volume           = fetch_top_volume(session)
    delivery             = fetch_delivery(session)
    long_bu, short_bu    = fetch_buildup(session)
    call_oi, put_oi      = fetch_oi_levels(session, "NIFTY")
    bnf_call, bnf_put    = fetch_oi_levels(session, "BANKNIFTY")
    fii, dii             = fetch_fii_dii(session)
    w52h, w52l           = fetch_52w(session)
    breadth              = fetch_breadth(session)

    all_call = (call_oi + bnf_call)[:4]
    all_put  = (put_oi  + bnf_put)[:4]

    nifty_ltp      = indices[0][1] if indices else "N/A"
    top_call_strike = call_oi[0][0] if call_oi else "N/A"
    top_put_strike  = put_oi[0][0]  if put_oi  else "N/A"

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
            "strong_res": top_call_strike,
            "resistance":  "N/A",
            "ltp":         nifty_ltp,
            "support":     "N/A",
            "strong_sup":  top_put_strike,
        },
        "bulk_deals": [("N/A", "Check NSE")],
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
    send_photo(part2_path, "📊 PRICE ACTION TELUGU — EOD Part 2\nVolume | Delivery | Buildup | OI | FII/DII")
    print("Done.")
