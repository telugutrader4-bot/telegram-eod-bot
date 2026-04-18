"""
PRICE ACTION TELUGU — Bloomberg-Style Image Generator
White background, editorial typography, data-dense financial terminal aesthetic.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ─────────────────────────────────────────────────────────────
# FONTS  (Liberation Sans = Arial clone — tight, editorial)
# ─────────────────────────────────────────────────────────────

LIB = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"
POPPINS = "/usr/share/fonts/truetype/google-fonts/Poppins-{}.ttf"
DEJAVU  = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed{}.ttf"

def F(size, style="Regular"):
    # Try Liberation → Poppins → DejaVu
    paths = {
        "Bold":      [LIB.format("Bold"),    POPPINS.format("Bold"),   DEJAVU.format("-Bold")],
        "Regular":   [LIB.format("Regular"), POPPINS.format("Regular"),DEJAVU.format("")],
        "Italic":    [LIB.format("Italic"),  POPPINS.format("Italic"), DEJAVU.format("-Oblique")],
        "BoldItalic":[LIB.format("BoldItalic"), POPPINS.format("BoldItalic"), DEJAVU.format("-BoldOblique")],
    }
    for p in paths.get(style, paths["Regular"]):
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

# ─────────────────────────────────────────────────────────────
# BLOOMBERG COLOR PALETTE
# White background, black editorial text, orange accent brand,
# precise green/red financial data colors
# ─────────────────────────────────────────────────────────────

WHITE      = (255, 255, 255)
PAPER      = (252, 252, 250)      # Warm white background
PANEL      = (245, 245, 243)      # Light panel fill
RULE       = (220, 220, 218)      # Hairline dividers
RULE_DARK  = (180, 180, 175)      # Stronger dividers

INK        = (10, 10, 10)         # Near-black body text
INK_MED    = (60, 60, 60)         # Secondary text
INK_LIGHT  = (120, 120, 120)      # Tertiary / labels
INK_GHOST  = (180, 180, 180)      # Placeholder / muted

ORANGE     = (255, 102, 0)        # Bloomberg orange brand
ORANGE_DIM = (255, 130, 40)
RED        = (204, 0, 0)          # Financial red (loss)
RED_BG     = (255, 240, 240)      # Red tinted cell bg
GREEN      = (0, 140, 60)         # Financial green (gain)
GREEN_BG   = (240, 255, 245)      # Green tinted cell bg
BLUE       = (0, 80, 180)         # Data blue
BLUE_BG    = (240, 246, 255)
PURPLE_CLR = (110, 50, 180)
GOLD_CLR   = (180, 130, 0)

W   = 900
PAD = 28

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def rr(draw, x1, y1, x2, y2, r, fill, outline=None, ow=1):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill,
                            outline=outline, width=ow)

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def th(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def tc(draw, cx, y, text, font, color):
    draw.text((int(cx - tw(draw, text, font) / 2), y), text, font=font, fill=color)

def tr(draw, rx, y, text, font, color):
    draw.text((int(rx - tw(draw, text, font)), y), text, font=font, fill=color)

def hairline(draw, y, x1=PAD, x2=None, color=RULE, w=1):
    if x2 is None:
        x2 = W - PAD
    draw.rectangle([x1, y, x2, y + w - 1], fill=color)

def thick_line(draw, y, color=INK, h=3):
    draw.rectangle([PAD, y, W - PAD, y + h - 1], fill=color)

# ─────────────────────────────────────────────────────────────
# SECTION HEADER  (Bloomberg editorial style)
# ─────────────────────────────────────────────────────────────

def section_hdr(draw, y, title, accent=ORANGE, gap_top=18, gap_bot=14):
    y += gap_top
    # Thick top rule
    draw.rectangle([PAD, y, W - PAD, y + 2], fill=accent)
    y += 6
    # Section label in ALL CAPS, compact
    draw.text((PAD, y), title, font=F(11, "Bold"), fill=accent)
    y += 20
    # Thin bottom rule
    draw.rectangle([PAD, y, W - PAD, y], fill=RULE)
    y += gap_bot
    return y

# ─────────────────────────────────────────────────────────────
# TITLE / MASTHEAD
# ─────────────────────────────────────────────────────────────

def masthead(draw, part_num, date_str, meta_line):
    """Bloomberg-style masthead. Returns y after it."""
    # Top black bar (Bloomberg terminal top bar)
    draw.rectangle([0, 0, W, 6], fill=ORANGE)

    y = 14
    # Brand name — bold editorial
    draw.text((PAD, y), "PRICE ACTION TELUGU", font=F(28, "Bold"), fill=INK)

    # Part label right-aligned
    part_label = f"PART {part_num} OF 2"
    tr(draw, W - PAD, y + 6, part_label, F(11, "Bold"), ORANGE)

    y += 38
    # Thin rule under brand
    draw.rectangle([PAD, y, W - PAD, y], fill=RULE_DARK)
    y += 8

    # Meta line
    draw.text((PAD, y), "INSTITUTIONAL SMART MONEY REPORT", font=F(10, "Bold"), fill=INK_LIGHT)
    draw.text((PAD + 270, y), "—", font=F(10, "Regular"), fill=INK_GHOST)
    draw.text((PAD + 285, y), meta_line, font=F(10, "Regular"), fill=INK_LIGHT)

    # Date badge right
    rr(draw, W - 136, y - 3, W - PAD, y + 17, r=3, fill=ORANGE)
    tr(draw, W - PAD - 6, y, date_str, F(10, "Bold"), WHITE)

    y += 22
    # Heavy rule below masthead
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=INK)
    y += 10

    return y

# ─────────────────────────────────────────────────────────────
# PART 1
# ─────────────────────────────────────────────────────────────

def build_part1(data):
    img  = Image.new("RGB", (W, 2400), PAPER)
    draw = ImageDraw.Draw(img)

    y = masthead(draw, "1", data["date"],
                 "INDEX SNAPSHOT  /  GAINERS & LOSERS  /  SECTORS  /  52-WEEK HIGH & LOW")

    # ══ INDEX SNAPSHOT ═══════════════════════════════════════
    y = section_hdr(draw, y, "INDEX SNAPSHOT", ORANGE)

    # 3 index cards in a row
    cw = (W - PAD * 2 - 20) // 3
    for i, (name, val, chg) in enumerate(data["indices"][:3]):
        cx = PAD + i * (cw + 10)
        pos = chg.startswith("+")
        clr = GREEN if pos else RED
        bg  = GREEN_BG if pos else RED_BG

        # Card with subtle border
        rr(draw, cx, y, cx + cw, y + 86, r=4, fill=WHITE,
           outline=GREEN if pos else RED, ow=1)

        # Colored top stripe
        draw.rectangle([cx, y, cx + cw, y + 3], fill=clr)

        draw.text((cx + 10, y + 10), name, font=F(10, "Bold"), fill=INK_LIGHT)
        draw.text((cx + 10, y + 28), val,  font=F(24, "Bold"), fill=INK)

        # Change badge
        rr(draw, cx + 10, y + 60, cx + 10 + tw(draw, chg, F(12, "Bold")) + 12,
           y + 78, r=3, fill=bg)
        draw.text((cx + 16, y + 62), chg, font=F(12, "Bold"), fill=clr)

    y += 100

    # Row 2: VIX / PCR / Adv-Dec — smaller metric cards
    extras = data.get("extras", [
        ("INDIA VIX",      "13.45", ORANGE,    "Low volatility"),
        ("PUT CALL RATIO", "1.18",  PURPLE_CLR, "Bullish"),
        ("ADV / DEC",      "3 : 1", BLUE,       "Breadth positive"),
    ])
    for i, item in enumerate(extras):
        name, val, clr = item[0], item[1], item[2]
        note = item[3] if len(item) > 3 else ""
        cx = PAD + i * (cw + 10)
        rr(draw, cx, y, cx + cw, y + 68, r=4, fill=WHITE, outline=RULE, ow=1)
        draw.text((cx + 10, y + 8),  name, font=F(9, "Bold"),    fill=INK_LIGHT)
        draw.text((cx + 10, y + 26), val,  font=F(20, "Bold"),   fill=clr)
        if note:
            draw.text((cx + 10, y + 52), note, font=F(9, "Italic"), fill=INK_LIGHT)
    y += 84

    # ══ MARKET BREADTH ═══════════════════════════════════════
    y = section_hdr(draw, y, "MARKET BREADTH", BLUE)

    breadth = data.get("breadth", {"advances": 1820, "declines": 620, "unchanged": 110})
    total   = breadth["advances"] + breadth["declines"] + breadth["unchanged"]
    bw      = W - PAD * 2
    adv_w   = int(bw * breadth["advances"] / total)
    dec_w   = int(bw * breadth["declines"] / total)

    # Segmented bar
    BAR_H = 28
    draw.rectangle([PAD, y, W - PAD, y + BAR_H], fill=PANEL)
    rr(draw, PAD, y, PAD + adv_w, y + BAR_H, r=2, fill=GREEN)
    draw.rectangle([PAD + adv_w, y, PAD + adv_w + dec_w, y + BAR_H], fill=RED)

    # Tick marks
    for i in range(1, 10):
        tx = PAD + int(bw * i / 10)
        draw.rectangle([tx, y, tx + 1, y + BAR_H], fill=WHITE)

    y += BAR_H + 8

    # Labels under bar
    adv_pct = breadth['advances'] * 100 // total
    dec_pct = breadth['declines'] * 100 // total
    unc_pct = 100 - adv_pct - dec_pct

    draw.text((PAD, y), f"▲ {breadth['advances']:,}  ADVANCES ({adv_pct}%)",
              font=F(11, "Bold"), fill=GREEN)
    tc(draw, W // 2, y, f"▼ {breadth['declines']:,}  DECLINES ({dec_pct}%)",
       F(11, "Bold"), RED)
    tr(draw, W - PAD, y, f"— {breadth['unchanged']}  UNCHANGED ({unc_pct}%)",
       F(11, "Regular"), INK_LIGHT)
    y += 28

    # ══ TOP GAINERS & LOSERS ══════════════════════════════════
    y = section_hdr(draw, y, "TOP GAINERS  &  TOP LOSERS", ORANGE)

    col_w = (W - PAD * 2 - 14) // 2
    gx, lx = PAD, PAD + col_w + 14

    gainers = data.get("gainers", [])
    losers  = data.get("losers",  [])

    # Column headers
    for base, label, clr in [(gx, "TOP GAINERS", GREEN), (lx, "TOP LOSERS", RED)]:
        draw.rectangle([base, y, base + col_w, y + 26], fill=clr)
        tc(draw, base + col_w // 2, y + 6, label, F(11, "Bold"), WHITE)
    y += 30

    # Column subheaders
    for base in [gx, lx]:
        draw.rectangle([base, y, base + col_w, y + 22], fill=PANEL)
        draw.text((base + 10, y + 5), "STOCK", font=F(9, "Bold"), fill=INK_LIGHT)
        tr(draw, base + col_w - 8, y + 5, "CHANGE", F(9, "Bold"), INK_LIGHT)
        hairline(draw, y + 22, base, base + col_w)
    y += 24

    for i in range(max(len(gainers), len(losers))):
        ry   = y + i * 32
        odd  = i % 2 == 1
        bg   = PANEL if odd else WHITE

        if i < len(gainers):
            draw.rectangle([gx, ry, gx + col_w, ry + 31], fill=bg)
            draw.text((gx + 10, ry + 8), gainers[i][0], font=F(13, "Bold"), fill=INK)
            val = gainers[i][1]
            rr(draw, gx + col_w - tw(draw, val, F(12,"Bold")) - 22,
               ry + 6, gx + col_w - 8, ry + 26, r=3, fill=GREEN_BG)
            tr(draw, gx + col_w - 12, ry + 8, val, F(12, "Bold"), GREEN)
            hairline(draw, ry + 31, gx, gx + col_w, RULE)

        if i < len(losers):
            draw.rectangle([lx, ry, lx + col_w, ry + 31], fill=bg)
            draw.text((lx + 10, ry + 8), losers[i][0], font=F(13, "Bold"), fill=INK)
            val = losers[i][1]
            rr(draw, lx + col_w - tw(draw, val, F(12,"Bold")) - 22,
               ry + 6, lx + col_w - 8, ry + 26, r=3, fill=RED_BG)
            tr(draw, lx + col_w - 12, ry + 8, val, F(12, "Bold"), RED)
            hairline(draw, ry + 31, lx, lx + col_w, RULE)

    y += max(len(gainers), len(losers)) * 32 + 10

    # ══ SECTOR PERFORMANCE ════════════════════════════════════
    y = section_hdr(draw, y, "SECTOR PERFORMANCE", ORANGE)

    sectors = data.get("sectors", [])
    cols = 3
    sw   = (W - PAD * 2 - (cols - 1) * 10) // cols

    for i, (name, chg) in enumerate(sectors):
        ri, ci  = i // cols, i % cols
        sx, sy  = PAD + ci * (sw + 10), y + ri * 76
        pos     = chg.startswith("+")
        clr     = GREEN if pos else RED
        bg      = GREEN_BG if pos else RED_BG
        border  = GREEN if pos else RED

        rr(draw, sx, sy, sx + sw, sy + 66, r=4, fill=WHITE, outline=border, ow=1)
        draw.rectangle([sx, sy, sx + sw, sy + 3], fill=clr)
        draw.text((sx + 10, sy + 10), name, font=F(10, "Bold"), fill=INK_LIGHT)

        # Big change number
        draw.text((sx + 10, sy + 28), chg, font=F(19, "Bold"), fill=clr)

        # Mini bar indicator
        bar_max = sw - 20
        bar_len = int(bar_max * min(abs(float(chg.strip('%+').replace(',',''))), 5) / 5)
        draw.rectangle([sx + 10, sy + 58, sx + 10 + bar_len, sy + 62], fill=clr)
        draw.rectangle([sx + 10 + bar_len, sy + 58, sx + sw - 10, sy + 62], fill=RULE)

    rows_sec = (len(sectors) + cols - 1) // cols
    y += rows_sec * 76 + 10

    # ══ 52-WEEK HIGH & LOW ════════════════════════════════════
    y = section_hdr(draw, y, "52-WEEK HIGH  &  52-WEEK LOW", ORANGE)

    col_w = (W - PAD * 2 - 14) // 2
    gx, lx = PAD, PAD + col_w + 14
    w52h   = data.get("52w_high", [])
    w52l   = data.get("52w_low",  [])

    # Headers
    draw.rectangle([gx, y, gx + col_w, y + 26], fill=GREEN)
    draw.rectangle([lx, y, lx + col_w, y + 26], fill=RED)
    tc(draw, gx + col_w // 2, y + 6, "AT 52-WEEK HIGH", F(10, "Bold"), WHITE)
    tc(draw, lx + col_w // 2, y + 6, "AT 52-WEEK LOW",  F(10, "Bold"), WHITE)
    y += 30

    # Column labels
    for base in [gx, lx]:
        draw.rectangle([base, y, base + col_w, y + 22], fill=PANEL)
        draw.text((base + 8,  y + 5), "STOCK",   font=F(9, "Bold"), fill=INK_LIGHT)
        tc(draw, base + col_w * 58 // 100, y + 5, "CMP",     F(9, "Bold"), INK_LIGHT)
        tr(draw, base + col_w - 6,  y + 5, "52W LEVEL", F(9, "Bold"), INK_LIGHT)
        hairline(draw, y + 22, base, base + col_w)
    y += 24

    for i in range(max(len(w52h), len(w52l))):
        ry  = y + i * 32
        bg  = PANEL if i % 2 == 1 else WHITE

        if i < len(w52h):
            draw.rectangle([gx, ry, gx + col_w, ry + 31], fill=bg)
            draw.text((gx + 8, ry + 8), w52h[i][0], font=F(12, "Bold"), fill=INK)
            tc(draw, gx + col_w * 58 // 100, ry + 8, w52h[i][1], F(12, "Bold"), GREEN)
            tr(draw, gx + col_w - 6,  ry + 8, w52h[i][2], F(11, "Regular"), INK_LIGHT)
            hairline(draw, ry + 31, gx, gx + col_w)

        if i < len(w52l):
            draw.rectangle([lx, ry, lx + col_w, ry + 31], fill=bg)
            draw.text((lx + 8, ry + 8), w52l[i][0], font=F(12, "Bold"), fill=INK)
            tc(draw, lx + col_w * 58 // 100, ry + 8, w52l[i][1], F(12, "Bold"), RED)
            tr(draw, lx + col_w - 6,  ry + 8, w52l[i][2], F(11, "Regular"), INK_LIGHT)
            hairline(draw, ry + 31, lx, lx + col_w)

    y += max(len(w52h), len(w52l)) * 32 + 20

    # ── FOOTER ───────────────────────────────────────────────
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=INK)
    y += 8
    draw.text((PAD, y),
              "Continued in Part 2  —  Volume  |  Buildup  |  OI  |  FII / DII",
              font=F(10, "Bold"), fill=ORANGE)
    tr(draw, W - PAD, y,
       "For Educational Purposes Only  |  Not SEBI Registered Advice",
       F(9, "Italic"), INK_LIGHT)
    y += 22

    draw.rectangle([0, y, W, y + 4], fill=ORANGE)
    y += 4

    img = img.crop((0, 0, W, y))
    img.save("part1_report.png", "PNG", optimize=True)
    print(f"[OK] Part 1  {W}x{y}px")
    return "part1_report.png"


# ─────────────────────────────────────────────────────────────
# PART 2
# ─────────────────────────────────────────────────────────────

def build_part2(data):
    img  = Image.new("RGB", (W, 2800), PAPER)
    draw = ImageDraw.Draw(img)

    y = masthead(draw, "2", data["date"],
                 "VOLUME  /  DELIVERY  /  LONG & SHORT BUILDUP  /  OI  /  FII & DII")

    # ── Simple list helper ────────────────────────────────────
    def list_rows(items, val_color=GREEN, rank=True):
        nonlocal y
        for i, (stock, val) in enumerate(items):
            bg = PANEL if i % 2 == 1 else WHITE
            draw.rectangle([PAD, y, W - PAD, y + 32], fill=bg)
            # Rank number
            if rank:
                rr(draw, PAD + 2, y + 4, PAD + 28, y + 28, r=3,
                   fill=INK, outline=None)
                tc(draw, PAD + 15, y + 8, str(i + 1), F(11, "Bold"), WHITE)
            draw.text((PAD + 36, y + 8), stock, font=F(13, "Bold"), fill=INK)
            tr(draw, W - PAD - 8, y + 8, val, F(13, "Bold"), val_color)
            hairline(draw, y + 32, PAD, W - PAD)
            y += 32
        y += 10

    # ── Table header helper ───────────────────────────────────
    def tbl_header(cols):
        """cols = list of (label, x_start, align)"""
        nonlocal y
        draw.rectangle([PAD, y, W - PAD, y + 24], fill=INK)
        for label, x, align in cols:
            if align == "left":
                draw.text((x, y + 5), label, font=F(9, "Bold"), fill=WHITE)
            elif align == "center":
                tc(draw, x, y + 5, label, F(9, "Bold"), WHITE)
            else:
                tr(draw, x, y + 5, label, F(9, "Bold"), WHITE)
        y += 24

    # ══ TOP 5 VOLUME ══════════════════════════════════════════
    y = section_hdr(draw, y, "TOP 5 HIGHEST VOLUME  —  NIFTY 500", BLUE)
    tbl_header([("RANK", PAD + 8, "left"), ("STOCK", PAD + 50, "left"),
                ("VOLUME (SHARES)", W - PAD - 8, "right")])
    list_rows(data.get("top_volume", []), val_color=BLUE)

    # ══ TOP 5 DELIVERY % ══════════════════════════════════════
    y = section_hdr(draw, y, "TOP 5 HIGHEST DELIVERY %", GREEN)
    tbl_header([("RANK", PAD + 8, "left"), ("STOCK", PAD + 50, "left"),
                ("DELIVERY %", W - PAD - 8, "right")])
    list_rows(data.get("delivery", []), val_color=GREEN)

    # ══ LONG BUILDUP ══════════════════════════════════════════
    y = section_hdr(draw, y, "LONG BUILDUP  —  TOP 5  (PRICE UP  |  OI UP)", GREEN)
    tbl_header([("STOCK", PAD + 10, "left"), ("PRICE CHG", W // 2, "center"),
                ("OI CHANGE", W - PAD - 8, "right")])

    for i, (stock, pchg, oichg) in enumerate(data.get("long_buildup", [])):
        bg = PANEL if i % 2 == 1 else WHITE
        draw.rectangle([PAD, y, W - PAD, y + 32], fill=bg)
        # Green left accent bar
        draw.rectangle([PAD, y, PAD + 4, y + 32], fill=GREEN)
        draw.text((PAD + 12, y + 8), stock, font=F(13, "Bold"), fill=INK)
        # Price badge
        rr(draw, W // 2 - 35, y + 6, W // 2 + 35, y + 26, r=3, fill=GREEN_BG)
        tc(draw, W // 2, y + 8, pchg, F(12, "Bold"), GREEN)
        # OI badge
        rr(draw, W - PAD - tw(draw, oichg, F(11, "Bold")) - 20,
           y + 6, W - PAD - 4, y + 26, r=3, fill=BLUE_BG)
        tr(draw, W - PAD - 8, y + 8, oichg, F(11, "Bold"), BLUE)
        hairline(draw, y + 32)
        y += 32
    y += 10

    # ══ SHORT BUILDUP ═════════════════════════════════════════
    y = section_hdr(draw, y, "SHORT BUILDUP  —  TOP 5  (PRICE DOWN  |  OI UP)", RED)
    tbl_header([("STOCK", PAD + 10, "left"), ("PRICE CHG", W // 2, "center"),
                ("OI CHANGE", W - PAD - 8, "right")])

    for i, (stock, pchg, oichg) in enumerate(data.get("short_buildup", [])):
        bg = PANEL if i % 2 == 1 else WHITE
        draw.rectangle([PAD, y, W - PAD, y + 32], fill=bg)
        draw.rectangle([PAD, y, PAD + 4, y + 32], fill=RED)
        draw.text((PAD + 12, y + 8), stock, font=F(13, "Bold"), fill=INK)
        rr(draw, W // 2 - 35, y + 6, W // 2 + 35, y + 26, r=3, fill=RED_BG)
        tc(draw, W // 2, y + 8, pchg, F(12, "Bold"), RED)
        rr(draw, W - PAD - tw(draw, oichg, F(11,"Bold")) - 20,
           y + 6, W - PAD - 4, y + 26, r=3, fill=BLUE_BG)
        tr(draw, W - PAD - 8, y + 8, oichg, F(11, "Bold"), BLUE)
        hairline(draw, y + 32)
        y += 32
    y += 10

    # ══ OPEN INTEREST LEVELS ═════════════════════════════════
    y = section_hdr(draw, y, "OPEN INTEREST LEVELS", ORANGE)

    col_w = (W - PAD * 2 - 14) // 2
    gx, lx = PAD, PAD + col_w + 14
    call_oi = data.get("call_oi", [])
    put_oi  = data.get("put_oi",  [])

    # Sub-headers
    draw.rectangle([gx, y, gx + col_w, y + 26], fill=RED)
    draw.rectangle([lx, y, lx + col_w, y + 26], fill=GREEN)
    tc(draw, gx + col_w // 2, y + 6, "CALL OI — RESISTANCE", F(10, "Bold"), WHITE)
    tc(draw, lx + col_w // 2, y + 6, "PUT OI — SUPPORT",     F(10, "Bold"), WHITE)
    y += 30

    for base in [gx, lx]:
        draw.rectangle([base, y, base + col_w, y + 22], fill=PANEL)
        draw.text((base + 8, y + 5), "STRIKE",    font=F(9, "Bold"), fill=INK_LIGHT)
        tr(draw, base + col_w - 6, y + 5, "OPEN INTEREST", F(9, "Bold"), INK_LIGHT)
        hairline(draw, y + 22, base, base + col_w)
    y += 24

    for i in range(max(len(call_oi), len(put_oi))):
        ry  = y + i * 32
        bg  = PANEL if i % 2 == 1 else WHITE
        if i < len(call_oi):
            draw.rectangle([gx, ry, gx + col_w, ry + 31], fill=bg)
            draw.text((gx + 8, ry + 8), call_oi[i][0], font=F(12, "Bold"), fill=INK)
            tr(draw, gx + col_w - 6, ry + 8, call_oi[i][1], F(12, "Bold"), RED)
            hairline(draw, ry + 31, gx, gx + col_w)
        if i < len(put_oi):
            draw.rectangle([lx, ry, lx + col_w, ry + 31], fill=bg)
            draw.text((lx + 8, ry + 8), put_oi[i][0], font=F(12, "Bold"), fill=INK)
            tr(draw, lx + col_w - 6, ry + 8, put_oi[i][1], F(12, "Bold"), GREEN)
            hairline(draw, ry + 31, lx, lx + col_w)

    y += max(len(call_oi), len(put_oi)) * 32 + 10

    # ══ KEY LEVELS ════════════════════════════════════════════
    y = section_hdr(draw, y, "KEY LEVELS  —  BASED ON OI", BLUE)

    kl  = data.get("key_levels", {})
    lev = [
        ("STRONG\nRES",   kl.get("strong_res", ""), RED,         (255, 235, 235)),
        ("RESISTANCE",    kl.get("resistance", ""),  (200, 80, 0),(255, 245, 235)),
        ("LTP",           kl.get("ltp", ""),         BLUE,        BLUE_BG),
        ("SUPPORT",       kl.get("support", ""),     GREEN,       GREEN_BG),
        ("STRONG\nSUP",   kl.get("strong_sup", ""),  (0, 100, 40),(230, 255, 240)),
    ]
    lw = (W - PAD * 2 - 4 * 10) // 5

    for i, (label, val, clr, bg) in enumerate(lev):
        lx2 = PAD + i * (lw + 10)

        # Card
        rr(draw, lx2, y, lx2 + lw, y + 82, r=4, fill=bg, outline=clr, ow=2)

        # Top stripe
        draw.rectangle([lx2, y, lx2 + lw, y + 3], fill=clr)

        # Label (handle multiline)
        lines = label.split("\n")
        for li, line in enumerate(lines):
            tc(draw, lx2 + lw // 2, y + 8 + li * 14, line, F(9, "Bold"), clr)

        # Value — big and bold
        tc(draw, lx2 + lw // 2, y + 40, val, F(16, "Bold"), clr)

        # Arrow indicator
        arrow = "▲" if i >= 3 else "▼" if i <= 1 else "●"
        tc(draw, lx2 + lw // 2, y + 64, arrow, F(11, "Bold"), clr)

    y += 96

    # ══ BULK & BLOCK DEALS ════════════════════════════════════
    y = section_hdr(draw, y, "TOP BULK  &  BLOCK DEALS", PURPLE_CLR)
    tbl_header([("STOCK", PAD + 10, "left"), ("ACTIVITY TYPE", W - PAD - 8, "right")])

    activity_colors = [BLUE, GREEN, ORANGE, PURPLE_CLR, GOLD_CLR]
    for i, (stock, deal) in enumerate(data.get("bulk_deals", [])):
        bg = PANEL if i % 2 == 1 else WHITE
        draw.rectangle([PAD, y, W - PAD, y + 32], fill=bg)
        draw.text((PAD + 10, y + 8), stock, font=F(13, "Bold"), fill=INK)
        clr = activity_colors[i % len(activity_colors)]
        rr(draw, W - PAD - tw(draw, deal, F(11,"Bold")) - 18,
           y + 6, W - PAD - 4, y + 26, r=12, fill=clr)
        tr(draw, W - PAD - 10, y + 8, deal, F(11, "Bold"), WHITE)
        hairline(draw, y + 32)
        y += 32
    y += 10

    # ══ FII / DII DATA ════════════════════════════════════════
    y = section_hdr(draw, y, "FII / DII  DATA", ORANGE)

    fii = data.get("fii", "Rs. +0 Cr")
    dii = data.get("dii", "Rs. +0 Cr")
    fc  = GREEN if "+" in fii else RED
    dc  = GREEN if "+" in dii else RED

    col_w = (W - PAD * 2 - 14) // 2
    gx, lx = PAD, PAD + col_w + 14

    # FII card
    rr(draw, gx, y, gx + col_w, y + 96, r=6, fill=WHITE, outline=fc, ow=2)
    draw.rectangle([gx, y, gx + col_w, y + 3], fill=fc)
    draw.text((gx + 12, y + 10), "FII  NET BUY / SELL", font=F(10, "Bold"), fill=INK_LIGHT)
    draw.text((gx + 12, y + 32), fii, font=F(22, "Bold"), fill=fc)
    # FII sentiment bar
    draw.rectangle([gx + 12, y + 72, gx + col_w - 12, y + 80], fill=RULE)
    bar_fill = fc
    fill_w = col_w - 24
    draw.rectangle([gx + 12, y + 72, gx + 12 + fill_w, y + 80], fill=bar_fill)

    # DII card
    rr(draw, lx, y, lx + col_w, y + 96, r=6, fill=WHITE, outline=dc, ow=2)
    draw.rectangle([lx, y, lx + col_w, y + 3], fill=dc)
    draw.text((lx + 12, y + 10), "DII  NET BUY / SELL", font=F(10, "Bold"), fill=INK_LIGHT)
    draw.text((lx + 12, y + 32), dii, font=F(22, "Bold"), fill=dc)
    draw.rectangle([lx + 12, y + 72, lx + col_w - 12, y + 80], fill=RULE)

    y += 110

    # ── FOOTER ───────────────────────────────────────────────
    draw.rectangle([PAD, y, W - PAD, y + 1], fill=INK)
    y += 8
    draw.text((PAD, y), "Follow @PriceActionTelugu  for Daily Market Updates",
              font=F(11, "Bold"), fill=ORANGE)
    tr(draw, W - PAD, y,
       "For Educational Purposes Only  |  Not SEBI Registered Advice",
       F(9, "Italic"), INK_LIGHT)
    y += 22
    draw.rectangle([0, y, W, y + 4], fill=ORANGE)
    y += 4

    img = img.crop((0, 0, W, y))
    img.save("part2_report.png", "PNG", optimize=True)
    print(f"[OK] Part 2  {W}x{y}px")
    return "part2_report.png"


# ─────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────

def generate_images(data):
    return build_part1(data), build_part2(data)


if __name__ == "__main__":
    sample = {
        "date": "18 April 2026",
        "indices": [
            ("NIFTY 50",   "24,315", "+0.82%"),
            ("BANK NIFTY", "52,840", "+1.14%"),
            ("SENSEX",     "80,218", "+0.79%"),
        ],
        "extras": [
            ("INDIA VIX",      "13.45", ORANGE,    "Low volatility"),
            ("PUT CALL RATIO", "1.18",  PURPLE_CLR, "Bullish stance"),
            ("ADV / DEC",      "3 : 1", BLUE,       "Breadth positive"),
        ],
        "breadth": {"advances": 1820, "declines": 620, "unchanged": 110},
        "gainers": [
            ("BEL",        "+5.2%"), ("HAL",        "+4.1%"),
            ("IRFC",       "+3.8%"), ("RECLTD",     "+3.2%"),
            ("TATA POWER", "+2.9%"),
        ],
        "losers": [
            ("HINDUNILVR", "-2.1%"), ("NESTLEIND",  "-1.8%"),
            ("WIPRO",      "-1.5%"), ("TECHM",      "-1.2%"),
            ("DABUR",      "-0.9%"),
        ],
        "sectors": [
            ("DEFENCE",   "+3.4%"), ("PSU BANKS", "+2.1%"), ("METAL",  "+1.8%"),
            ("IT",        "-1.2%"), ("FMCG",      "-0.8%"), ("PHARMA", "+0.5%"),
        ],
        "52w_high": [
            ("BEL",        "310.50", "311.00"), ("HAL",        "4,820",  "4,850"),
            ("IRFC",       "229.40", "230.00"), ("RECLTD",     "498.70", "500.00"),
            ("TATA POWER", "415.20", "416.50"),
        ],
        "52w_low": [
            ("HINDUNILVR", "2,190",  "2,180"), ("NESTLEIND",  "2,050",  "2,040"),
            ("WIPRO",      "442.30", "440.00"), ("TECHM",      "1,315",  "1,310"),
            ("DABUR",      "488.60", "485.00"),
        ],
        "top_volume": [
            ("RELIANCE","4.2 Cr"), ("SBIN","3.8 Cr"), ("BEL","3.1 Cr"),
            ("TATA MOTORS","2.9 Cr"), ("IRFC","2.6 Cr"),
        ],
        "delivery": [
            ("BEL","78%"), ("IRCTC","74%"), ("HAL","71%"),
            ("BHEL","69%"), ("COAL INDIA","67%"),
        ],
        "long_buildup": [
            ("BEL","+5.2%","OI +18%"), ("HAL","+4.1%","OI +14%"),
            ("RECLTD","+3.2%","OI +12%"), ("IRFC","+3.8%","OI +11%"),
            ("TATA POWER","+2.9%","OI +9%"),
        ],
        "short_buildup": [
            ("HINDUNILVR","-2.1%","OI +16%"), ("NESTLEIND","-1.8%","OI +13%"),
            ("WIPRO","-1.5%","OI +11%"), ("TECHM","-1.2%","OI +8%"),
            ("DABUR","-0.9%","OI +7%"),
        ],
        "call_oi": [
            ("NIFTY  24500 CE","1.82 Cr"), ("NIFTY  24600 CE","1.35 Cr"),
            ("BNIFTY 56000 CE","95 L"),    ("BNIFTY 56200 CE","72 L"),
        ],
        "put_oi": [
            ("NIFTY  24000 PE","2.10 Cr"), ("NIFTY  24100 PE","1.64 Cr"),
            ("BNIFTY 55000 PE","1.12 Cr"), ("BNIFTY 54800 PE","88 L"),
        ],
        "key_levels": {
            "strong_res": "24,600", "resistance": "24,450",
            "ltp":        "24,315", "support":    "24,150", "strong_sup": "24,000",
        },
        "bulk_deals": [
            ("RELIANCE","Institutional Buy"), ("INFY","Fund Activity"),
            ("BEL","Large Accumulation"), ("LT","Bulk Buying"),
            ("HDFCLIFE","Promoter Activity"),
        ],
        "fii": "Rs. +2,350 Cr",
        "dii": "Rs. -1,120 Cr",
    }
    p1, p2 = generate_images(sample)
    print(f"\nDone:  {p1}  |  {p2}")
