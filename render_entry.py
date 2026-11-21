#!/usr/bin/env python3
"""Renderer entry sum21 (news-image-20261121) — 40 cerita, Pillow.
Transkripsi + adaptasi build_main() sketsa rank-3 MAIN rev3:
- placeholder dashed_box DIGANTI ilustrasi asli (ditempel apa adanya,
  hero 180x102, strip 151x42, tanpa resize); label strip dihapus.
- masthead kanan = "40 STORIES \u2022 6 REGIONS" saja (tanpa label model).
- headline A1 = "GTA VI: $3.79B DAY ONE" (titik, Ruling 1).
- footer SATU baris terpusat vertikal (legenda chip + Sources), tanpa metadata build (Ruling 14).
Deterministik: tanpa random, tanpa timestamp.
Jalankan: python3 render_entry.py  -> entry.png (1024x1024)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

PAPER = (250, 246, 236)
INK = (20, 20, 20)
RULE_RED = (178, 34, 34)
GREY = (110, 105, 95)

REGION = {
    "EUROPE":   ((37, 99, 235), "EUROPE"),
    "MID EAST": ((147, 51, 234), "MID EAST"),
    "ASIA":     ((220, 38, 38), "ASIA"),
    "AMERICAS": ((22, 163, 74), "AMERICAS"),
    "AFRICA":   ((234, 88, 12), "AFRICA"),
    "OCEANIA":  ((13, 148, 136), "OCEANIA"),
}
CODE = {"EUROPE": "EU", "MID EAST": "ME", "ASIA": "AS",
        "AMERICAS": "AM", "AFRICA": "AF", "OCEANIA": "OC"}
STATUS = {
    "CONFIRMED": ((22, 120, 60), (255, 255, 255)),
    "OFFICIAL":  ((37, 99, 235), (255, 255, 255)),
    "REPORTED":  ((245, 158, 11), (30, 30, 30)),
    "CLAIM":     ((220, 60, 20), (255, 255, 255)),
}

# Slot -> file ilustrasi final (nama sumber apa adanya, di root repo).
HERO_IMG = {1: "hero-h1-nasdaq-only.png", 2: "hero-h2.png",
            3: "hero-h3.png", 4: "hero-h4.png"}
STRIP_IMG = {5: "strip-a1-gtavi-text.png", 6: "strip-a2.png",
             7: "strip-a3.png", 8: "strip-a4.png", 9: "strip-a5.png",
             10: "strip-a6.png", 11: "strip-a7.png", 12: "strip-a8.png",
             13: "strip-a9.png", 14: "strip-a10.png", 15: "strip-a11.png",
             16: "strip-a12-logo-b.png"}

def F(px, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(SERIFB if bold else SERIF, px)
    return ImageFont.truetype(SANSB if bold else SANS, px)

def pt(p):
    return round(p * 96 / 72)

violations = []
stories_seen = []
pins_outside = 0
pins_overlap_pairs = 0

# ---------------------------------------------------------------- data 40 cerita
HERO = [
    (1, "AMERICAS", "WALL ST", "AI MELTDOWN: NASDAQ \u22125.3%",
     "Nasdaq \u22125.28% Fri, worst week since Mar 2020; Bitcoin $55,106 Sat AM.",
     "CONFIRMED", -74.0, 40.7),
    (2, "MID EAST", "HORMUZ", "HORMUZ: TWO TANKERS HIT",
     "Two tankers hit Sat 21 Nov near Khasab, Oman; no deaths.",
     "CONFIRMED", 56.2, 26.2),
    (3, "EUROPE", "KRYVYI RIH", "RUSSIA TRIPLE-TAP KRYVYI RIH",
     "Missile then drones as rescuers arrived; boy, 7, and medic, 20, killed.",
     "CONFIRMED", 33.4, 47.9),
    (4, "EUROPE", "ANTALYA", "COP31: NO DEAL, FOSSIL CUT",
     "Overtime Sat with no deal; draft drops the word \u2018fossil\u2019.",
     "CONFIRMED", 30.7, 36.9),
]
TIER_A = [
    (5, "AMERICAS", "MIAMI", "GTA VI: $3.79B DAY ONE",
     "$3.79B day one, biggest ever; announced 20 Nov.",
     "CONFIRMED", -80.2, 25.8),
    (6, "AMERICAS", "ROCH.", "RADIATION ALTERS BRAIN",
     "Rochester: immune cells alter; behaviour unchanged.",
     "REPORTED", -77.6, 43.16),
    (7, "AMERICAS", "S.F.", "RIEMANN CLAIMED",
     "CLAIMED \u2014 unverified; Stanford counters.",
     "CLAIM", -122.4, 37.8),
    (8, "EUROPE", "GENEVA", "KILLER ROBOTS",
     "Talks by 2028; US, Russia, Israel balk.",
     "CONFIRMED", 6.14, 46.2),
    (9, "ASIA", "SHENZ.", "SHENZHEN: XI WINS MOST",
     "Analysis 21 Nov; summit was 19 Nov.",
     "CONFIRMED", 114.06, 22.55),
    (10, "MID EAST", "GAZA", "ISRAEL KILLS 3 WCK STAFF",
     "Aid vehicle hit in Gaza City Sat.",
     "REPORTED", 34.47, 31.5),
    (11, "ASIA", "YONG.", "YONGBYON EXPANDS",
     "Satellite images; IAEA confirms.",
     "REPORTED", 126.3, 39.8),
    (12, "ASIA", "TOKYO", "CHINA SNUBS JAPAN PM",
     "Xi refuses formal talks; handshake only.",
     "REPORTED", 139.69, 35.68),
    (13, "AFRICA", "BADME", "BADME CLASH",
     "Fighting since 9 Nov; build-up 21 Nov.",
     "REPORTED", 37.9, 14.7),
    (14, "AMERICAS", "TEXAS", "SPACE ARMOR: 16,100 MPH",
     "3mm projectile stopped at 16,100 mph; aluminium fails.",
     "REPORTED", -97.7, 30.3),
    (15, "AFRICA", "KINSHASA", "EBOLA: WHO ALERT STAYS",
     "11,613 cases; 5,678 deaths.",
     "OFFICIAL", 15.3, -4.3),
    (16, "AMERICAS", "VEGAS", "VERSTAPPEN TAKES POLE",
     "Antonelli fastest; Verstappen inherits pole.",
     "OFFICIAL", -115.14, 36.17),
]
BRIEFS = [
    (17, "ASIA", 85.8, 20.3, "Akvan weakens \u2014 rain 209mm"),
    (18, "ASIA", 85.1, 25.6, "Modi Bihar \u20b934,470cr"),
    (19, "ASIA", 77.2, 28.6, "Ramayana \u20b91,574.6cr box office"),
    (20, "ASIA", 116.4, 39.9, "House: 879,868 AI chips to China"),
    (21, "ASIA", 125.75, 39.03, "Kim inspects factory (Sat)"),
    (22, "ASIA", 72.8, 19.07, "India 1cr HPV doses"),
    (23, "EUROPE", 4.35, 50.85, "Gen Z protests, 25 countries"),
    (24, "EUROPE", -3.7, 40.42, "Spain bank levy to 2027"),
    (25, "EUROPE", 2.35, 48.86, "EU 3% digital tax"),
    (26, "EUROPE", -2.24, 53.48, "Man City 1\u20131 Fulham"),
    (27, "EUROPE", 0.5, 51.8, "Pattinson debuts as Bond"),
    (28, "MID EAST", 51.4, 35.7, "Qatar talks in Tehran"),
    (29, "MID EAST", 46.7, 24.7, "Houthis hit Riyadh, 3 down"),
    (30, "AMERICAS", -81.7, 41.5, "Harden 51 pts"),
    (31, "AMERICAS", -118.24, 34.05, "Hunger Games $76M global"),
    (32, "AMERICAS", -118.5, 34.2, "Rosal\u00eda fave \u2014 55% Kalshi, 9 noms"),
    (33, "AMERICAS", -122.12, 47.67, "Microsoft 365 recovers"),
    (34, "AMERICAS", -75.2, -10.5, "Peru quake 6.7\u20136.8"),
    (35, "AFRICA", 28.05, -26.2, "Mlambo-Ngcuka dies at 71"),
    (36, "AFRICA", 11.17, 10.29, "Gombe troops kill 3"),
    (37, "AFRICA", -8.0, 12.65, "U-17: Mali 3\u20130, Morocco 6\u20130"),
    (38, "OCEANIA", 151.2, -33.87, "Cummins stays captain"),
    (39, "OCEANIA", 144.96, -37.81, "North Melbourne AFLW GF"),
    (40, "OCEANIA", 174.78, -41.29, "Rahul SENA century"),
]
assert len(BRIEFS) == 24 and BRIEFS[0][0] == 17 and BRIEFS[-1][0] == 40
GROUP_STARTS = {17: "ASIA", 23: "EUROPE", 28: "MID EAST", 30: "AMERICAS",
                35: "AFRICA", 38: "OCEANIA"}

# ---------------------------------------------------------------- helpers
def text_fit(d, x, y, s, font, max_w, tag):
    w = d.textlength(s, font=font)
    if w > max_w:
        violations.append(f"{tag}: '{s[:44]}' lebar {w:.0f} > {max_w}")
    d.text((x, y), s, font=font, fill=INK)
    return w

def wrap_lines(d, s, font, max_w, max_lines, tag):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        violations.append(f"{tag}: '{s[:44]}' butuh {len(lines)} baris > {max_lines}")
        lines = lines[:max_lines]
    for ln in lines:
        if d.textlength(ln, font=font) > max_w:
            violations.append(f"{tag}: baris '{ln[:44]}' terlalu lebar")
    return lines

def status_chip(d, x, y, status, tag):
    bg, fg = STATUS[status]
    f = F(8, bold=True)
    tw = d.textlength(status, font=f)
    w = int(tw) + 10
    d.rounded_rectangle([x - w, y, x, y + 14], radius=3, fill=bg)
    d.text((x - w + 5, y + 2), status, font=f, fill=fg)
    return w

def num_dot(d, x, y, n, color, r=9, fs=10):
    stories_seen.append(n)
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=color, outline=(255, 255, 255), width=1)
    s = str(n)
    f = F(fs, bold=True)
    d.text((x + r - d.textlength(s, font=f) / 2, y + r - fs / 2 - 1), s, font=f,
           fill=(255, 255, 255))

def paste_illustration(img, x, y, filename, expect_w, expect_h, tag):
    """Tempel ilustrasi asli apa adanya (tanpa resize); ukuran dicek."""
    p = os.path.join(ROOT, filename)
    with Image.open(p) as im:
        if im.size != (expect_w, expect_h):
            violations.append(f"{tag}: '{filename}' ukuran {im.size} != {(expect_w, expect_h)}")
        img.paste(im.convert("RGB"), (x, y))

# ---------------------------------------------------------------- masthead + timeline
def masthead(d, y, h):
    d.text((15, y + 1), "THE WORLD IN ONE PAGE", font=F(10, bold=True), fill=RULE_RED)
    r = "40 STORIES  \u2022  6 REGIONS"
    rf = F(10, bold=True)
    text_fit(d, 1024 - 15 - d.textlength(r, font=rf), y + 1, r, rf, 500, "masthead-right")
    d.line([(15, y + 15), (1009, y + 15)], fill=INK, width=1)
    df = F(pt(26), bold=True, serif=True)
    text_fit(d, 15, y + 17, "Saturday 21 November 2026", df, 994, "masthead-date")
    d.line([(15, y + h - 2), (1009, y + h - 2)], fill=RULE_RED, width=2)

def timeline(d, y, h):
    d.rectangle([15, y, 125, y + h], fill=RULE_RED)
    d.text((25, y + h // 2 - 13), "THE DAY", font=F(10, bold=True), fill=(255, 255, 255))
    d.text((25, y + h // 2 + 1), "IN UTC", font=F(10, bold=True), fill=(255, 255, 255))
    segs = [
        ("FRI 20 NOV", "Nasdaq \u22125.3%, worst week since Mar 2020"),
        ("SAT 06:00 UTC", "Bitcoin low $55,106"),
        ("SAT 21 NOV", "Hormuz: two tankers hit"),
        ("SAT 21 NOV", "COP31 overtime, no deal"),
    ]
    x0, w = 133, (1009 - 133) // 4
    for i, (t, s) in enumerate(segs):
        x = x0 + i * w
        if i:
            d.line([(x, y + 4), (x, y + h - 4)], fill=(200, 195, 185), width=1)
        text_fit(d, x + 8, y + 3, t, F(9, bold=True), w - 12, f"timeline{i}")
        lines = wrap_lines(d, s, F(9), w - 12, 2, f"timeline{i}")
        for j, ln in enumerate(lines):
            d.text((x + 8, y + 14 + j * 10), ln, font=F(9), fill=INK)

# ---------------------------------------------------------------- hero + Tier A
def hero_rows(img, d, y, hh, headline_pt, iw):
    w = (994 - 8) // 2
    for i, (n, reg, city, head, dek, status, _lon, _lat) in enumerate(HERO):
        r, c = divmod(i, 2)
        x = 15 + c * (w + 8)
        yy = y + r * (hh + 6)
        rc = REGION[reg][0]
        d.rectangle([x, yy, x + w, yy + hh], fill=(255, 255, 255), outline=INK, width=2)
        paste_illustration(img, x + 6, yy + 6, HERO_IMG[n], iw, hh - 12, f"hero{n}")
        tx = x + 6 + iw + 10
        tw = x + w - 8 - tx
        num_dot(d, tx, yy + 6, n, rc, r=9, fs=10)
        text_fit(d, tx + 22, yy + 8, f"{CODE[reg]} \u2022 {city}", F(9, bold=True), tw - 90,
                 f"hero{n}-region")
        status_chip(d, x + w - 8, yy + 6, status, f"hero{n}-status")
        hf = F(pt(headline_pt), bold=True, serif=True)
        lines = wrap_lines(d, head, hf, tw, 2, f"hero{n}-headline")
        ly = yy + 25
        for ln in lines:
            d.text((tx, ly), ln, font=hf, fill=INK)
            ly += pt(headline_pt)
        df = F(10)
        for j, ln in enumerate(wrap_lines(d, dek, df, tw, 2, f"hero{n}-dek")):
            d.text((tx, ly + 2 + j * 12), ln, font=df, fill=INK)

def tier_grid(img, d, y, cell_h, headline_pt, strip_h):
    gap = 8
    for i, (n, reg, city, head, fact, status, _lon, _lat) in enumerate(TIER_A):
        r, c = divmod(i, 6)
        x = 15 + c * (159 + gap)
        yy = y + r * (cell_h + gap)
        rc = REGION[reg][0]
        d.rectangle([x, yy, x + 159, yy + cell_h], fill=(255, 255, 255), outline=INK, width=1)
        paste_illustration(img, x + 4, yy + 4, STRIP_IMG[n], 151, strip_h, f"tier{n}")
        ty = yy + 4 + strip_h + 5
        num_dot(d, x + 6, ty, n, rc, r=8, fs=9)
        chip_w = status_chip(d, x + 155, ty, status, f"tier{n}-status")
        text_fit(d, x + 24, ty + 2, f"{CODE[reg]} \u2022 {city}", F(8, bold=True),
                 (x + 155 - chip_w) - (x + 24) - 6, f"tier{n}-region")
        hf = F(pt(headline_pt), bold=True, serif=True)
        lines = wrap_lines(d, head, hf, 159 - 12, 2, f"tier{n}-headline")
        ly = ty + 19
        for ln in lines:
            d.text((x + 6, ly), ln, font=hf, fill=INK)
            ly += pt(headline_pt)
        ff = F(10)
        for j, ln in enumerate(wrap_lines(d, fact, ff, 159 - 12, 2, f"tier{n}-fact")):
            d.text((x + 6, ly + 1 + j * 12), ln, font=ff, fill=INK)

# ---------------------------------------------------------------- peta dunia
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-75, 62),
     (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
     (-90, 21), (-95, 19), (-105, 20), (-110, 23), (-117, 32), (-125, 40), (-125, 48),
     (-135, 58), (-155, 58), (-165, 60)],
    [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 64)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -50), (-73, -54),
     (-70, -20), (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 68), (40, 60),
     (35, 55), (30, 50), (28, 45), (23, 40), (19, 42), (15, 44), (12, 44), (8, 44),
     (3, 43), (-2, 37)],
    [(-6, 35), (-10, 31), (-17, 15), (-17, 12), (-12, 8), (-8, 5), (0, 6), (6, 4),
     (9, 4), (13, -1), (12, -6), (13, -12), (12, -18), (16, -28), (20, -35),
     (26, -34), (32, -29), (35, -24), (40, -16), (40, -10), (46, -11), (51, -10),
     (51, 2), (48, 11), (43, 11), (40, 15), (38, 18), (35, 22), (32, 31), (25, 32),
     (19, 33), (10, 34)],
    [(30, 70), (60, 69), (90, 75), (120, 73), (150, 70), (162, 60), (158, 52),
     (142, 50), (135, 42), (127, 38), (122, 32), (115, 22), (108, 10), (100, 6),
     (95, 15), (90, 22), (80, 10), (75, 15), (70, 22), (62, 25), (57, 26),
     (52, 28), (48, 30), (43, 28), (40, 20), (43, 12), (50, 16), (58, 22),
     (56, 26), (50, 29), (44, 29), (40, 32), (36, 36), (32, 38), (28, 42),
     (30, 50), (35, 55), (40, 62), (45, 68)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(95, 5), (98, 2), (101, -2), (104, -5), (106, -6), (102, 0), (98, 4)],
    [(108, -6), (112, -7), (114, -8), (110, -7)],
    [(131, -1), (136, -2), (141, -4), (146, -7), (141, -8), (136, -4)],
    [(139, 35), (140, 38), (141, 41), (142, 44), (143, 42), (141, 38), (140, 35)],
    [(103, 1), (104, 2), (104, 5), (102, 5), (101, 2)],
    [(167, -45), (169, -43), (171, -41), (173, -40), (175, -38), (174, -41),
     (172, -43), (169, -46)],
]
PIN_SHIFT = {26: (-13, 10), 27: (13, -10), 8: (-12, 12), 23: (-13, 10),
             24: (13, 12), 25: (0, 14), 32: (-14, -8)}

def draw_map(d, x, y, w, h):
    global pins_outside, pins_overlap_pairs
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 238), outline=INK, width=1)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED", font=F(11, bold=True), fill=INK)
    mx, my = x + 6, y + 22
    mw, mh = w - 12, h - 22 - 34
    for k in range(1, 6):
        d.line([(mx + k * mw / 6, my), (mx + k * mw / 6, my + mh)], fill=(190, 210, 220), width=1)
    for k in range(1, 4):
        d.line([(mx, my + k * mh / 4), (mx + mw, my + k * mh / 4)], fill=(190, 210, 220), width=1)
    def proj(lon, lat):
        return (mx + (lon + 180) / 360 * mw, my + (75 - lat) / 130 * mh)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(232, 222, 196), outline=(150, 140, 120))
    all_pins = [(n, reg, lon, lat) for (n, reg, _c, _h, _d, _s, lon, lat) in HERO] + \
               [(n, reg, lon, lat) for (n, reg, _c, _h, _f, _s, lon, lat) in TIER_A] + \
               [(n, reg, lon, lat) for (n, reg, lon, lat, _s) in BRIEFS]
    placed = []
    for n, reg, lon, lat in all_pins:
        px, py = proj(lon, lat)
        dx, dy = PIN_SHIFT.get(n, (0, 0))
        px, py = px + dx - 7, py + dy - 7
        px = max(mx, min(px, mx + mw - 15))
        py = max(my, min(py, my + mh - 15))
        placed.append([px, py])
    for _ in range(40):
        disp = [[0.0, 0.0] for _ in placed]
        moved = False
        for i in range(len(placed)):
            for j in range(i + 1, len(placed)):
                dx = placed[j][0] - placed[i][0]
                dy = placed[j][1] - placed[i][1]
                if abs(dx) < 15 and abs(dy) < 15:
                    moved = True
                    if abs(dx) <= abs(dy):
                        push = (15 - abs(dx)) / 2 + 1
                        s = 1 if dx >= 0 else -1
                        disp[i][0] -= push * s
                        disp[j][0] += push * s
                    else:
                        push = (15 - abs(dy)) / 2 + 1
                        s = 1 if dy >= 0 else -1
                        disp[i][1] -= push * s
                        disp[j][1] += push * s
        if not moved:
            break
        for i in range(len(placed)):
            mx_, my_ = disp[i]
            m = max(abs(mx_), abs(my_))
            if m > 7:
                mx_, my_ = mx_ * 7 / m, my_ * 7 / m
            placed[i] = [placed[i][0] + mx_, placed[i][1] + my_]
        placed = [[max(mx, min(px, mx + mw - 15)),
                   max(my, min(py, my + mh - 15))] for (px, py) in placed]
    for (n, reg, lon, lat), (px, py) in zip(all_pins, placed):
        d.ellipse([px, py, px + 14, py + 14], fill=REGION[reg][0],
                  outline=(255, 255, 255), width=1)
        s = str(n)
        f = F(8, bold=True)
        d.text((px + 7 - d.textlength(s, font=f) / 2, py + 2), s, font=f, fill=(255, 255, 255))
        stories_seen.append(n)
    for (px, py) in placed:
        if px < mx or px > mx + mw - 15 or py < my or py > my + mh - 15:
            pins_outside += 1
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            if abs(placed[i][0] - placed[j][0]) < 14 and abs(placed[i][1] - placed[j][1]) < 14:
                pins_overlap_pairs += 1
                print(f"  OVERLAP PIN: #{all_pins[i][0]} vs #{all_pins[j][0]}")
    ix, iy, iw, ih = x + 8, y + h - 34 - 52 - 15, 92, 46
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(250, 246, 236), outline=INK, width=1)
    d.text((ix + 4, iy + 2), "THE GULF", font=F(8, bold=True), fill=INK)
    d.ellipse([ix + 48, iy + 20, ix + 58, iy + 30], fill=REGION["MID EAST"][0])
    d.text((ix + 61, iy + 21), "#2", font=F(8, bold=True), fill=INK)
    d.text((ix + 4, iy + 33), "Hormuz #2 \u2022 Riyadh #29", font=F(8), fill=INK)
    for ly, regs in ((y + h - 45, ["EUROPE", "MID EAST", "ASIA"]),
                     (y + h - 30, ["AMERICAS", "AFRICA", "OCEANIA"])):
        lx = x + 8
        for reg in regs:
            d.ellipse([lx, ly + 1, lx + 8, ly + 9], fill=REGION[reg][0])
            lx += 10
            f = F(8, bold=True)
            label = f"{reg} ({CODE[reg]})"
            tw = d.textlength(label, font=f)
            if lx + tw > x + w - 8:
                violations.append(f"map-legenda: '{label}' melebihi lebar peta")
            d.text((lx, ly), label, font=f, fill=INK)
            lx += tw + 6
    d.text((x + 8, y + h - 15), "40 of 40 pinned  \u2022  lat \u221290\u00b0 to +90\u00b0 (approx.)",
           font=F(9), fill=GREY)

# ---------------------------------------------------------------- brief
def brief_cols(d, y, h, cols, rows_per_col, row_h, font_pt, map_w):
    draw_map(d, 15, y, map_w, h)
    bx0 = 15 + map_w + 10
    bw = (994 - map_w - 10 - (cols - 1) * 8) // cols
    idx = 0
    for c in range(cols):
        x = bx0 + c * (bw + 8)
        d.rectangle([x, y, x + bw, y + h], fill=(255, 255, 255), outline=INK, width=1)
        for r in range(rows_per_col[c]):
            n, reg, _lon, _lat, label = BRIEFS[idx]
            idx += 1
            yy = y + 5 + r * row_h
            rc = REGION[reg][0]
            gw = 0
            if n in GROUP_STARTS:
                d.line([(x + 6, yy - 3), (x + bw - 6, yy - 3)], fill=rc, width=2)
                gf = F(8, bold=True)
                gname = GROUP_STARTS[n]
                gw = d.textlength(gname, font=gf)
                d.text((x + bw - 6 - gw, yy - 1), gname, font=gf, fill=rc)
            d.ellipse([x + 6, yy, x + 24, yy + 18], fill=rc)
            s = str(n)
            fnum = F(9, bold=True)
            d.text((x + 15 - d.textlength(s, font=fnum) / 2, yy + 3), s, font=fnum,
                   fill=(255, 255, 255))
            stories_seen.append(n)
            avail = bw - 34 - (int(gw) + 10 if gw else 0)
            text_fit(d, x + 28, yy + 1, label, F(font_pt), avail, f"brief#{n}")
    assert idx == 24, f"brief terpakai {idx}, harus 24"

def zone_head(d, y, note):
    d.rectangle([15, y, 1009, y + 16], fill=(238, 230, 210))
    d.text((25, y + 2), "BRIEF  \u2022  24 stories #17\u201340", font=F(11, bold=True), fill=INK)
    rf = F(9, bold=True)
    d.text((300, y + 3), note, font=rf, fill=GREY)

def date_check(d, y, dh):
    d.rectangle([15, y, 1009, y + dh], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([15, y, 108, y + dh], fill=RULE_RED)
    d.text((25, y + dh // 2 - 7), "DATE CHECK", font=F(10, bold=True), fill=(255, 255, 255))
    lines = [
        "Fri 20 Nov: Nasdaq crash (US markets closed Sat)  \u2022  Sat 21 Nov: Bitcoin low $55,106; Hormuz tankers hit; COP31 overtime.  \u2022  GTA VI announced 20 Nov.",
        "Riemann = CLAIM, unverified; Stanford counter-draft 21 Nov  \u2022  Shenzhen = analysis 21 Nov (summit 19 Nov)  \u2022  Badme fighting since 9 Nov  \u2022  Peru quake 6.7\u20136.8.",
        "Left out on purpose: C3 (Jul 2026 article)  \u2022  Egypt\u2013IMF (deal 18 Nov)  \u2022  Morocco \u20ac366M (18 Nov).",
    ]
    for j, ln in enumerate(lines):
        text_fit(d, 118, y + 2 + j * 11, ln, F(10), 884, f"datecheck{j}")

def numbers_strip(d, y, dh):
    d.rectangle([15, y, 1009, y + dh], fill=(238, 230, 210))
    s = "THE DAY IN NUMBERS:  Nasdaq \u22125.28%  \u2022  Bitcoin $55,106  \u2022  GTA VI $3.79B  \u2022  Space Armor 16,100 mph  \u2022  Ebola 11,613 cases"
    text_fit(d, 25, y + 2, s, F(11, bold=True), 970, "numbers")

def footer(d, y, dh):
    # SATU baris, terpusat vertikal di zona dh=30: chip 14px -> ly = y+8.
    lx = 25
    ly = y + 8
    for status, meaning in [("CONFIRMED", "= 2+ outlets"), ("OFFICIAL", "= primary source"),
                            ("REPORTED", "= one outlet"), ("CLAIM", "= one-sided claim")]:
        bg, fg = STATUS[status]
        f = F(8, bold=True)
        tw = d.textlength(status, font=f)
        w = int(tw) + 10
        d.rounded_rectangle([lx, ly, lx + w, ly + 14], radius=3, fill=bg)
        d.text((lx + 5, ly + 2), status, font=f, fill=fg)
        lx += w + 4
        mf = F(9)
        mtw = d.textlength(meaning, font=mf)
        d.text((lx, ly + 2), meaning, font=mf, fill=INK)
        lx += mtw + 14
    text_fit(d, lx, ly + 1,
             "Sources: Reuters, CNN, AP, WHO, Formula1.com, WSJ",
             F(10), 995 - lx, "footer")

# ---------------------------------------------------------------- build
def build_main():
    global stories_seen, violations, pins_outside, pins_overlap_pairs
    stories_seen, violations, pins_outside, pins_overlap_pairs = [], [], 0, 0
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    y = 10
    masthead(d, y, 54); y += 54 + 3
    timeline(d, y, 32); y += 32 + 3
    hero_rows(img, d, y, 114, 22, 180); y += 114 + 6 + 114 + 3
    tier_grid(img, d, y, 132, 13, 42); y += 132 + 8 + 132 + 3
    zone_head(d, y, "AS 6 \u2022 EU 5 \u2022 ME 2 \u2022 AM 5 \u2022 AF 3 \u2022 OC 3")
    y += 16 + 2
    brief_cols(d, y, 292, cols=2, rows_per_col=[12, 12], row_h=23, font_pt=14, map_w=330)
    y += 292 + 3
    date_check(d, y, 36); y += 36 + 3
    numbers_strip(d, y, 18); y += 18 + 3
    footer(d, y, 30)
    total = y + 30
    return img, total

def run():
    img, total = build_main()
    n = sorted(set(stories_seen))
    ok_count = (n == list(range(1, 41)))
    ok_h = (total <= 1024)
    img.save(os.path.join(ROOT, "entry.png"))
    print(f"RANK3-MAIN: total={total}/1024 slack={1024-total} | cerita unik={len(n)} "
          f"count_ok={ok_count} height_ok={ok_h} | pelanggaran teks={len(violations)} | "
          f"pin di luar peta={pins_outside} | pasang pin tumpang tindih={pins_overlap_pairs}")
    for v in violations[:20]:
        print("  VIOLATION:", v)
    if not ok_count:
        missing = sorted(set(range(1, 41)) - set(n))
        print("  NOMOR HILANG:", missing, "| seen total:", len(stories_seen))

if __name__ == "__main__":
    run()
    print("SELESAI — entry.png di", ROOT)
