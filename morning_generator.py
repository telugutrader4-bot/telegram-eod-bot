"""
PRICE ACTION TELUGU — Morning Report Image Generator
Part A: Global Markets Snapshot
Part B: Nifty & BankNifty OI Snapshot (color-coded, no support/resistance labels)
Bloomberg white style — matches EOD report aesthetic
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ─────────────────────────────────────────────────────────────
# FONTS
# ─────────────────────────────────────────────────────────────

LIB     = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"
POPPINS = "/usr/share/fonts/truetype/google-fonts/Poppins-{}.ttf"
DEJAVU  = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed{}.ttf"

def F(size, style="Regular"):
    paths = {
        "Bold":      [LIB.format("Bold"),       POPPINS.format("Bold"),    DEJAVU.format("-Bold")],
        "Regular":   [LIB.format("Regular"),    POPPINS.format("Regular"), DEJAVU.format("")],
        "Italic":    [LIB.format("Italic"),      POPPINS.format("Italic"),  DEJAVU.format("-Oblique")],
        "BoldItalic":[LIB.format("BoldItalic"), POPPINS.format("BoldItalic"), DEJAVU.format("-BoldOblique")],
    }
    for p in paths.get(style, paths["Regular"]):
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

# ─────────────────────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────────────────────

WHITE      = (255, 255, 255)
PAPER      = (252, 252, 250)
PANEL      = (245, 245, 243)
RULE       = (220, 220, 218)
RULE_DARK  = (180, 180, 175)

INK        = (10, 10, 10)
INK_MED    = (55, 55, 55)
INK_LIGHT  = (115, 115, 115)
INK_GHOST  = (175, 175, 175)

ORANGE     = (255, 102, 0)
RED        = (204, 0, 0)
RED_BG     = (255, 238, 238)
RED_DEEP   = (160, 0, 0)
GREEN      = (0, 140, 60)
GREEN_BG   = (238, 255, 245)
GREEN_DEEP = (0, 100, 40)
BLUE       = (0, 80, 180)
BLUE_BG    = (238, 246, 255)
BLUE_MID   = (30, 100, 200)
YELLOW_BG  = (255, 253, 220)
YELLOW     = (180, 140, 0)
PURPLE     = (110, 50, 180)
PURPLE_BG  = (245, 238, 255)
GREY_MID   = (100, 100, 100)

# OI Color system (no labels — pure color coding)
OI_CALL_HIGH   = (210, 0,   0)     # Strongest call wall — deep red
OI_CALL_MED    = (240, 80,  80)    # Medium call OI — medium red
OI_CALL_LOW    = (255, 180, 180)   # Lower call OI — light red
OI_PUT_HIGH    = (0,   160, 60)    # Strongest put floor — deep green
OI_PUT_MED     = (60,  190, 110)   # Medium put OI — medium green
OI_PUT_LOW     = (160, 230, 185)   # Lower put OI — light green
OI_NEUTRAL     = (200, 200, 200)   # LTP zone — neutral grey

W   = 900
PAD = 28

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def rr(draw, x1, y1, x2, y2, r, fill, outline=None, ow=1):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r,
                            fill=fill, outline=outline, width=ow)

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def tc(draw, cx, y, text, font, color):
    draw.text((int(cx - tw(draw, text, font) / 2), y), text, font=font, fill=color)

def tr(draw, rx, y, text, font, color):
    draw.text((int(rx - tw(draw, text, font)), y), text, font=font, fill=color)

def hairline(draw, y, x1=PAD, x2=None, color=RULE):
    if x2 is None: x2 = W - PAD
    draw.rectangle([x1, y, x2, y], fill=color)

def section_hdr(draw, y, title, accent=ORANGE, gap_top=16, gap_bot=12):
    y += gap_top
    draw.rectangle([PAD, y, W - PAD, y + 2], fill=accent)
    y += 6
    draw.text((PAD, y), title, font=F(11, "Bold"), fill=accent)
    y += 20
    draw.rectangle([PAD, y, W - PAD, y], fill=RULE)
    y += gap_bot
    return y

def masthead_morning(draw, date_str, time_str):
    draw.rectangle([0, 0, W, 5], fill=ORANGE)
    y = 12

    # Brand
    draw.text((PAD, y), "PRICE ACTION TELUGU", font=F(26, "Bold"), fill=INK)

    # Live badge
    rr(draw, W - 170, y + 2, W - PAD, y + 26, r=3, fill=ORANGE)
    tr(draw, W - PAD - 6, y + 6, "MORNING REPORT", F(10, "Bold"), WHITE)

    y += 34
    draw.rectangle([PAD, y, W - PAD, y], fill=RULE_DARK)
    y += 7

    draw.text((PAD, y), "PRE-MARKET INTELLIGENCE", font=F(10, "Bold"), fill=INK_LIGHT)
    draw.text((PAD + 230, y), "—", font=F(10, "Regular"), fill=INK_GHOST)
    draw.text((PAD + 244, y), "GLOBAL MARKETS  /  NIFTY OI  /  BANKNIFTY OI",
              font=F(10, "Regular"), fill=INK_LIGHT)

    # Date + time
    dt_str = f"{date_str}  •  {time_str} IST"
    rr(draw, W - 180, y - 2, W - PAD, y + 18, r=3, fill=ORANGE)
    tr(draw, W - PAD - 6, y, dt_str, F(10, "Bold"), WHITE)

    y += 20
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=INK)
    y += 10
    return y

# ─────────────────────────────────────────────────────────────
# PART A — GLOBAL MARKETS
# ─────────────────────────────────────────────────────────────

def build_morning_global(data):
    """Builds Part A: Global Markets Snapshot image."""
    img  = Image.new("RGB", (W, 1600), PAPER)
    draw = ImageDraw.Draw(img)

    y = masthead_morning(draw, data["date"], data.get("time", "08:00"))

    # ══ SGX NIFTY HERO CARD ══════════════════════════════════
    # Big feature card — most important pre-market signal
    sgx = data.get("sgx_nifty", {"value": "24,380", "change": "+65", "pct": "+0.27%"})
    sgx_pos = not str(sgx["change"]).startswith("-")
    sgx_clr = GREEN if sgx_pos else RED
    sgx_bg  = GREEN_BG if sgx_pos else RED_BG

    rr(draw, PAD, y, W - PAD, y + 88, r=6,
       fill=sgx_bg, outline=sgx_clr, ow=2)
    draw.rectangle([PAD, y, W - PAD, y + 4], fill=sgx_clr)

    draw.text((PAD + 16, y + 12), "SGX NIFTY", font=F(11, "Bold"), fill=INK_LIGHT)
    draw.text((PAD + 16, y + 30), sgx["value"], font=F(28, "Bold"), fill=INK)

    # Change pill
    chg_txt = f"{sgx['change']}  ({sgx['pct']})"
    rr(draw, PAD + 16, y + 64, PAD + 16 + tw(draw, chg_txt, F(13, "Bold")) + 16,
       y + 82, r=4, fill=sgx_clr)
    draw.text((PAD + 24, y + 66), chg_txt, font=F(13, "Bold"), fill=WHITE)

    # Sentiment label right side
    sentiment = "BULLISH GAP UP" if sgx_pos else "BEARISH GAP DOWN"
    s_font = F(13, "Bold")
    tr(draw, W - PAD - 16, y + 42, sentiment, s_font, sgx_clr)
    arrow = "▲" if sgx_pos else "▼"
    tr(draw, W - PAD - 16 - tw(draw, sentiment, s_font) - 8,
       y + 42, arrow, F(18, "Bold"), sgx_clr)

    y += 104

    # ══ US MARKETS ═══════════════════════════════════════════
    y = section_hdr(draw, y, "US MARKETS  —  PREVIOUS CLOSE", BLUE)

    us = data.get("us_markets", [
        ("DOW JONES",   "39,218", "+312", "+0.80%"),
        ("S&P 500",     "5,218",  "+28",  "+0.54%"),
        ("NASDAQ",      "18,340", "+95",  "+0.52%"),
    ])

    cw = (W - PAD * 2 - 16) // 3
    for i, (name, val, chg, pct) in enumerate(us):
        cx  = PAD + i * (cw + 8)
        pos = not chg.startswith("-")
        clr = GREEN if pos else RED
        bg  = GREEN_BG if pos else RED_BG

        rr(draw, cx, y, cx + cw, y + 82, r=4,
           fill=WHITE, outline=clr, ow=1)
        draw.rectangle([cx, y, cx + cw, y + 3], fill=clr)

        draw.text((cx + 10, y + 10), name, font=F(9, "Bold"), fill=INK_LIGHT)
        draw.text((cx + 10, y + 26), val,  font=F(20, "Bold"), fill=INK)

        # Change row
        rr(draw, cx + 10, y + 56, cx + 10 + tw(draw, pct, F(11, "Bold")) + 14,
           y + 74, r=3, fill=bg)
        draw.text((cx + 17, y + 58), pct, font=F(11, "Bold"), fill=clr)
        draw.text((cx + 10 + tw(draw, pct, F(11,"Bold")) + 20, y + 58),
                  chg, font=F(11, "Regular"), fill=clr)

    y += 98

    # ══ ASIAN MARKETS ════════════════════════════════════════
    y = section_hdr(draw, y, "ASIAN MARKETS  —  LIVE / LATEST", RED)

    asia = data.get("asian_markets", [
        ("NIKKEI 225",  "38,940", "-210", "-0.54%", "JP"),
        ("HANG SENG",   "18,215", "+185", "+1.03%", "HK"),
        ("SHANGHAI",    "3,285",  "+12",  "+0.37%", "CN"),
    ])

    for i, item in enumerate(asia):
        name, val, chg, pct = item[0], item[1], item[2], item[3]
        country = item[4] if len(item) > 4 else ""
        pos = not chg.startswith("-")
        clr = GREEN if pos else RED
        bg  = GREEN_BG if pos else RED_BG

        cx = PAD + i * (cw + 8)
        rr(draw, cx, y, cx + cw, y + 82, r=4,
           fill=WHITE, outline=clr, ow=1)
        draw.rectangle([cx, y, cx + cw, y + 3], fill=clr)

        # Country tag
        if country:
            rr(draw, cx + cw - 34, y + 8, cx + cw - 8, y + 24, r=3,
               fill=PANEL)
            tc(draw, cx + cw - 21, y + 10, country, F(9, "Bold"), INK_LIGHT)

        draw.text((cx + 10, y + 10), name, font=F(9, "Bold"), fill=INK_LIGHT)
        draw.text((cx + 10, y + 26), val,  font=F(20, "Bold"), fill=INK)
        rr(draw, cx + 10, y + 56, cx + 10 + tw(draw, pct, F(11,"Bold")) + 14,
           y + 74, r=3, fill=bg)
        draw.text((cx + 17, y + 58), pct, font=F(11, "Bold"), fill=clr)
        draw.text((cx + 10 + tw(draw, pct, F(11,"Bold")) + 20, y + 58),
                  chg, font=F(11, "Regular"), fill=clr)

    y += 98

    # ══ COMMODITIES & CURRENCY ═══════════════════════════════
    y = section_hdr(draw, y, "COMMODITIES  &  CURRENCY", YELLOW)

    commodities = data.get("commodities", [
        ("CRUDE OIL",     "85.40", "+0.8%",  "$/bbl", YELLOW),
        ("GOLD",          "2,312", "+0.3%",  "$/oz",  YELLOW),
        ("DOLLAR INDEX",  "104.2", "-0.2%",  "DXY",   BLUE),
        ("USD/INR",       "83.45", "+0.1%",  "₹",     BLUE),
    ])

    com_w = (W - PAD * 2 - 3 * 10) // 4
    for i, (name, val, pct, unit, accent) in enumerate(commodities):
        cx  = PAD + i * (com_w + 10)
        pos = not pct.startswith("-")
        clr = GREEN if pos else RED

        rr(draw, cx, y, cx + com_w, y + 76, r=4,
           fill=WHITE, outline=RULE, ow=1)
        draw.rectangle([cx, y, cx + com_w, y + 3], fill=accent)

        draw.text((cx + 8, y + 10), name, font=F(9, "Bold"), fill=INK_LIGHT)
        draw.text((cx + 8, y + 26), val,  font=F(17, "Bold"), fill=INK)
        draw.text((cx + 8, y + 50), unit, font=F(9, "Regular"), fill=INK_GHOST)
        tr(draw, cx + com_w - 8, y + 52, pct, F(10, "Bold"), clr)

    y += 92

    # ══ GIFT NIFTY / INDIA VIX STRIP ═════════════════════════
    y += 8
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=RULE_DARK)
    y += 10

    quick = data.get("quick_metrics", [
        ("INDIA VIX",     "13.45", "-3.2%",  PURPLE),
        ("GIFT NIFTY",    "24,380","+0.27%", GREEN if True else RED),
        ("US 10Y YIELD",  "4.28%", "+0.02",  BLUE),
        ("FEAR & GREED",  "62",    "GREED",  YELLOW),
    ])

    qw = (W - PAD * 2 - 3 * 10) // 4
    for i, (name, val, note, clr) in enumerate(quick):
        cx = PAD + i * (qw + 10)
        draw.text((cx, y + 2),  name, font=F(9, "Bold"),    fill=INK_LIGHT)
        draw.text((cx, y + 18), val,  font=F(15, "Bold"),   fill=clr)
        draw.text((cx, y + 38), note, font=F(9, "Italic"),  fill=INK_LIGHT)

    y += 58

    # ── FOOTER ───────────────────────────────────────────────
    y += 8
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=INK)
    y += 8
    draw.text((PAD, y),
              "OI Snapshot in Part B  —  Nifty & BankNifty Strike Analysis",
              font=F(10, "Bold"), fill=ORANGE)
    tr(draw, W - PAD, y,
       "For Educational Purposes Only  |  Not SEBI Registered Advice",
       F(9, "Italic"), INK_LIGHT)
    y += 20
    draw.rectangle([0, y, W, y + 4], fill=ORANGE)
    y += 4

    img = img.crop((0, 0, W, y))
    img.save("morning_global.png", "PNG", optimize=True)
    print(f"[OK] Morning Part A (Global)  {W}x{y}px")
    return "morning_global.png"


# ─────────────────────────────────────────────────────────────
# PART B — OI SNAPSHOT (Color-coded, zero support/resistance labels)
# ─────────────────────────────────────────────────────────────

def oi_color(rank, side):
    """
    Returns fill color + text color based on OI rank and side.
    rank=1 → highest OI (strongest wall/floor)
    side='call' → red spectrum | side='put' → green spectrum
    No labels — pure color intensity tells the story.
    """
    if side == "call":
        if rank == 1:   return OI_CALL_HIGH,  WHITE
        elif rank == 2: return OI_CALL_MED,   WHITE
        elif rank == 3: return OI_CALL_LOW,   INK
        else:           return (255, 220, 220), INK
    else:  # put
        if rank == 1:   return OI_PUT_HIGH,   WHITE
        elif rank == 2: return OI_PUT_MED,    WHITE
        elif rank == 3: return OI_PUT_LOW,    INK
        else:           return (210, 245, 220), INK


def draw_oi_table(draw, y, index_name, ltp, strikes, accent):
    """
    Draws a complete OI table for one index.
    strikes = list of dicts:
      { "strike": 24500, "call_oi": 182, "put_oi": 210, "is_ltp": False }
    OI values in Lakhs (L) or Crores (Cr) — raw float for bar sizing.
    Returns new y position.
    """
    # Section title
    draw.rectangle([PAD, y, W - PAD, y + 36], fill=INK)
    draw.text((PAD + 14, y + 9), index_name, font=F(15, "Bold"), fill=WHITE)

    # LTP badge
    ltp_txt = f"LTP  {ltp}"
    rr(draw, W - PAD - tw(draw, ltp_txt, F(12,"Bold")) - 24,
       y + 7, W - PAD - 4, y + 29, r=4, fill=ORANGE)
    tr(draw, W - PAD - 12, y + 9, ltp_txt, F(12, "Bold"), WHITE)
    y += 40

    # Color legend strip
    legend_items = [
        (OI_CALL_HIGH, "Highest Call OI"),
        (OI_CALL_MED,  "High Call OI"),
        (OI_CALL_LOW,  "Moderate Call OI"),
        (OI_PUT_LOW,   "Moderate Put OI"),
        (OI_PUT_MED,   "High Put OI"),
        (OI_PUT_HIGH,  "Highest Put OI"),
    ]
    leg_w = (W - PAD * 2) // len(legend_items)
    for i, (clr, label) in enumerate(legend_items):
        lx = PAD + i * leg_w
        draw.rectangle([lx, y, lx + leg_w - 2, y + 18], fill=clr)
        tc(draw, lx + leg_w // 2, y + 3, label, F(7, "Bold"),
           WHITE if i in [0, 1, 4, 5] else INK)
    y += 22

    # Column headers
    draw.rectangle([PAD, y, W - PAD, y + 24], fill=PANEL)
    hairline(draw, y, PAD, W - PAD, RULE_DARK)

    COL_CALL_OI  = PAD + 18
    COL_CALL_BAR = PAD + 130
    COL_STRIKE   = W // 2
    COL_PUT_BAR  = W // 2 + 40
    COL_PUT_OI   = W - PAD - 18

    draw.text((COL_CALL_OI, y + 6),  "CALL OI", font=F(9, "Bold"), fill=RED_DEEP)
    tc(draw, W // 2, y + 6, "STRIKE", F(9, "Bold"), INK_MED)
    tr(draw, COL_PUT_OI, y + 6, "PUT OI", F(9, "Bold"), GREEN_DEEP)
    y += 26

    # Rank calls and puts for color coding
    sorted_calls = sorted(strikes, key=lambda s: s.get("call_oi", 0), reverse=True)
    sorted_puts  = sorted(strikes, key=lambda s: s.get("put_oi", 0),  reverse=True)
    call_ranks = {s["strike"]: i + 1 for i, s in enumerate(sorted_calls)}
    put_ranks  = {s["strike"]: i + 1 for i, s in enumerate(sorted_puts)}

    max_call = max((s.get("call_oi", 0) for s in strikes), default=1)
    max_put  = max((s.get("put_oi",  0) for s in strikes), default=1)

    BAR_MAX = 120  # max bar width in pixels
    ROW_H   = 36

    for i, s in enumerate(strikes):
        ry = y + i * ROW_H
        strike = s["strike"]
        call_v = s.get("call_oi", 0)
        put_v  = s.get("put_oi",  0)
        is_ltp = s.get("is_ltp", False)

        c_rank = call_ranks.get(strike, 99)
        p_rank = put_ranks.get(strike,  99)

        call_fill, call_txt_clr = oi_color(c_rank, "call")
        put_fill,  put_txt_clr  = oi_color(p_rank, "put")

        # Row background — LTP row gets special treatment
        if is_ltp:
            draw.rectangle([PAD, ry, W - PAD, ry + ROW_H - 1], fill=YELLOW_BG)
            draw.rectangle([PAD, ry, PAD + 3, ry + ROW_H - 1], fill=ORANGE)
            draw.rectangle([W - PAD - 3, ry, W - PAD, ry + ROW_H - 1], fill=ORANGE)
        else:
            row_bg = WHITE if i % 2 == 0 else PANEL
            draw.rectangle([PAD, ry, W - PAD, ry + ROW_H - 1], fill=row_bg)

        # CALL side — bar grows LEFT from center
        call_bar_w = int(BAR_MAX * call_v / max_call) if max_call > 0 else 0
        bar_x2 = COL_STRIKE - 50
        bar_x1 = bar_x2 - call_bar_w
        if call_bar_w > 0:
            rr(draw, bar_x1, ry + 8, bar_x2, ry + ROW_H - 9,
               r=3, fill=call_fill)

        # Call OI text — left side
        call_str = _fmt_oi(call_v)
        draw.text((COL_CALL_OI, ry + 10), call_str,
                  font=F(12, "Bold"), fill=RED if c_rank <= 2 else INK_MED)

        # STRIKE — center, bold, with LTP marker
        strike_str = f"{strike:,}"
        strike_clr = ORANGE if is_ltp else INK
        strike_font = F(14, "Bold") if is_ltp else F(13, "Bold")
        tc(draw, COL_STRIKE, ry + 10, strike_str, strike_font, strike_clr)
        if is_ltp:
            # LTP arrow
            draw.text((COL_STRIKE + tw(draw, strike_str, strike_font) // 2 + 8,
                       ry + 10), "◄", font=F(10, "Bold"), fill=ORANGE)

        # PUT side — bar grows RIGHT from center
        put_bar_w = int(BAR_MAX * put_v / max_put) if max_put > 0 else 0
        bar_x1 = COL_STRIKE + 50
        bar_x2 = bar_x1 + put_bar_w
        if put_bar_w > 0:
            rr(draw, bar_x1, ry + 8, bar_x2, ry + ROW_H - 9,
               r=3, fill=put_fill)

        # Put OI text — right side
        put_str = _fmt_oi(put_v)
        tr(draw, COL_PUT_OI, ry + 10, put_str,
           F(12, "Bold"), GREEN if p_rank <= 2 else INK_MED)

        # Hairline between rows
        hairline(draw, ry + ROW_H - 1, PAD, W - PAD, RULE)

    y += len(strikes) * ROW_H

    # Summary row — highest OI strikes
    top_call = sorted_calls[0] if sorted_calls else None
    top_put  = sorted_puts[0]  if sorted_puts  else None

    y += 6
    draw.rectangle([PAD, y, W - PAD, y + 32], fill=PANEL)
    draw.rectangle([PAD, y, PAD + 3, y + 32], fill=accent)

    summary_parts = []
    if top_call:
        summary_parts.append(
            f"Biggest Call Wall: {top_call['strike']:,}  ({_fmt_oi(top_call.get('call_oi',0))})"
        )
    if top_put:
        summary_parts.append(
            f"Biggest Put Floor: {top_put['strike']:,}  ({_fmt_oi(top_put.get('put_oi',0))})"
        )

    draw.text((PAD + 10, y + 9), "  |  ".join(summary_parts),
              font=F(10, "Bold"), fill=INK_MED)
    y += 38

    return y


def _fmt_oi(val):
    """Format OI number: val in Lakhs → display as Cr or L"""
    if val >= 100:
        return f"{val/100:.2f} Cr"
    else:
        return f"{int(val)} L"


def build_morning_oi(data):
    """Builds Part B: OI Snapshot image."""
    img  = Image.new("RGB", (W, 2200), PAPER)
    draw = ImageDraw.Draw(img)

    y = masthead_morning(draw, data["date"], data.get("time", "08:00"))

    # Intro strip
    draw.rectangle([PAD, y, W - PAD, y + 28], fill=INK)
    tc(draw, W // 2, y + 7,
       "OPEN INTEREST SNAPSHOT  —  COLOR INTENSITY = OI STRENGTH",
       F(10, "Bold"), WHITE)
    y += 38

    # ══ NIFTY OI TABLE ═══════════════════════════════════════
    y = section_hdr(draw, y, "NIFTY 50  —  OPTION CHAIN OI", GREEN, gap_top=10)

    nifty_strikes = data.get("nifty_oi", [
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
    ])

    y = draw_oi_table(draw, y,
                      "NIFTY 50",
                      data.get("nifty_ltp", "24,315"),
                      nifty_strikes, GREEN)

    y += 20

    # ══ BANKNIFTY OI TABLE ═══════════════════════════════════
    y = section_hdr(draw, y, "BANK NIFTY  —  OPTION CHAIN OI", BLUE, gap_top=10)

    bnf_strikes = data.get("banknifty_oi", [
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
    ])

    y = draw_oi_table(draw, y,
                      "BANK NIFTY",
                      data.get("banknifty_ltp", "52,840"),
                      bnf_strikes, BLUE)

    y += 10

    # ── FOOTER ───────────────────────────────────────────────
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=INK)
    y += 8
    draw.text((PAD, y),
              "Deeper red = heavier call writing  |  Deeper green = heavier put writing",
              font=F(10, "Bold"), fill=INK_MED)
    tr(draw, W - PAD, y,
       "For Educational Purposes Only  |  Not SEBI Registered Advice",
       F(9, "Italic"), INK_LIGHT)
    y += 20
    draw.rectangle([0, y, W, y + 4], fill=ORANGE)
    y += 4

    img = img.crop((0, 0, W, y))
    img.save("morning_oi.png", "PNG", optimize=True)
    print(f"[OK] Morning Part B (OI)  {W}x{y}px")
    return "morning_oi.png"


# ─────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────

def generate_morning_images(data):
    """Returns (global_path, oi_path)"""
    p_a = build_morning_global(data)
    p_b = build_morning_oi(data)
    return p_a, p_b


# ─────────────────────────────────────────────────────────────
# TEST
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from image_generator import ORANGE as _O  # just to confirm import works

    sample = {
        "date": "18 April 2026",
        "time": "08:00",

        "sgx_nifty": {"value": "24,380", "change": "+65", "pct": "+0.27%"},

        "us_markets": [
            ("DOW JONES", "39,218", "+312", "+0.80%"),
            ("S&P 500",   "5,218",  "+28",  "+0.54%"),
            ("NASDAQ",    "18,340", "+95",  "+0.52%"),
        ],

        "asian_markets": [
            ("NIKKEI 225", "38,940", "-210", "-0.54%", "JP"),
            ("HANG SENG",  "18,215", "+185", "+1.03%", "HK"),
            ("SHANGHAI",   "3,285",  "+12",  "+0.37%", "CN"),
        ],

        "commodities": [
            ("CRUDE OIL",    "85.40", "+0.8%", "$/bbl", YELLOW),
            ("GOLD",         "2,312", "+0.3%", "$/oz",  YELLOW),
            ("DOLLAR INDEX", "104.2", "-0.2%", "DXY",   BLUE),
            ("USD/INR",      "83.45", "+0.1%", "₹",     BLUE),
        ],

        "quick_metrics": [
            ("INDIA VIX",    "13.45", "-3.2%",  PURPLE),
            ("GIFT NIFTY",   "24,380","+0.27%", GREEN),
            ("US 10Y YIELD", "4.28%", "+0.02",  BLUE),
            ("FEAR & GREED", "62",    "GREED",  YELLOW),
        ],

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

    pa, pb = generate_morning_images(sample)
    print(f"\nDone:  {pa}  |  {pb}")
