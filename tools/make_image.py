#!/usr/bin/env python3
"""Render the entry image: a one-page broadsheet summing up Thursday 19 November 2026.

36 stories, every one occurring or first reported on the date: 3 leads, 10 grid
stories, 23 numbered briefs. Original geometric artwork drawn with Pillow — no
photographs, no third-party art. Facts as reported on 19 Nov 2026 (UTC) by
Reuters, AP, AFP, BBC, Al Jazeera, Euronews, CNBC, NPR, The Hindu, IMD, ABS,
ICJ, Korea Herald and National Grid; disputed claims are attributed.

Run:  python3 tools/make_image.py   (writes entry.png at the repository root)
Renders at 2x and downsamples with Lanczos for crisp type. Deterministic.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
S = 2                      # supersample factor
W = H = 1024               # logical page size
M = 36                     # page margin
CW = W - 2 * M             # content width

PAPER = (247, 242, 232)
CARD = (252, 249, 241)
INK = (24, 24, 22)
GRAY = (104, 98, 86)
RED = (178, 38, 28)
GOLD = (196, 162, 88)
LINE = (60, 56, 48)
PANEL = (238, 232, 218)
NAVY = (20, 28, 44)
LAND = (72, 88, 108)
LAND_EDGE = (96, 114, 136)

REGIONS = {
    "EUROPE": (66, 108, 168),
    "AMERICAS": (58, 128, 80),
    "ASIA": (178, 38, 28),
    "MIDEAST": (198, 118, 40),
    "AFRICA": (138, 88, 50),
    "OCEANIA": (118, 78, 148),
    "WORLD": (108, 103, 93),
}

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(round(size * S)))


def R(x0, y0, x1, y1):
    return [x0 * S, y0 * S, x1 * S, y1 * S]


def T(x, y):
    return (x * S, y * S)


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw * S:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, fnt, maxw, fill, leading=1.22, maxlines=None):
    x, y = xy
    lh = fnt.size * leading
    lines = wrap(d, text, fnt, maxw)
    if maxlines is not None and len(lines) > maxlines:
        raise OverflowError(f"text needs {len(lines)} lines (max {maxlines}): {text[:60]!r}")
    for ln in lines:
        d.text(T(x, y), ln, font=fnt, fill=fill)
        y += lh / S
    return y


def star(d, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.42
        a = math.radians(rot + i * 36)
        pts.append(T(cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=fill)


def flag_us(d, x, y, w, h):
    sh = h / 13
    for i in range(13):
        d.rectangle(R(x, y + i * sh, x + w, y + (i + 1) * sh),
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.42, sh * 7
    d.rectangle(R(x, y, x + cw, y + ch), fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            star(d, x + cw * (c + 0.5) / 5, y + ch * (r + 0.5) / 4, 1.7, (255, 255, 255))
    d.rectangle(R(x, y, x + w, y + h), outline=INK, width=S)


def flag_cn(d, x, y, w, h):
    d.rectangle(R(x, y, x + w, y + h), fill=(222, 41, 16))
    star(d, x + w * 0.18, y + h * 0.28, h * 0.17, (255, 222, 0))
    for dx, dy, rot in [(0.36, 0.10, -60), (0.44, 0.22, -30), (0.44, 0.38, 0), (0.36, 0.50, 30)]:
        star(d, x + w * dx, y + h * dy, h * 0.055, (255, 222, 0), rot=rot)
    d.rectangle(R(x, y, x + w, y + h), outline=INK, width=S)


def flag_ru(d, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 43, 30)]):
        d.rectangle(R(x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
    d.rectangle(R(x, y, x + w, y + h), outline=INK, width=S)


# ── lead illustrations (panels 306 x 86) ─────────────────────────────────────

def art_summit(d, x, y, w, h):
    # gradient dusk sky, low sun, distant Shenzhen skyline — flat foreground on top
    for i in range(int(h)):
        t = i / h
        d.rectangle(R(x, y + i, x + w, y + i + 1),
                    fill=(int(242 - 22 * t), int(228 - 28 * t), int(202 - 36 * t)))
    d.ellipse(R(x + w - 72, y + 10, x + w - 40, y + 42), fill=(224, 128, 86))
    sil = (150, 132, 108)
    for bx, bw, bh in [(8, 14, 18), (26, 10, 26), (40, 16, 14), (60, 12, 30), (76, 18, 20),
                       (98, 10, 36), (112, 14, 22), (130, 12, 16), (146, 16, 28), (166, 10, 18),
                       (180, 14, 24), (198, 12, 14), (214, 16, 32), (234, 10, 20), (248, 14, 26),
                       (266, 12, 16), (282, 14, 22)]:
        d.rectangle(R(x + bx, y + 52 - bh, x + bx + bw, y + 52), fill=sil)
    d.text(T(x + w / 2, y + 8), "APEC 2026 · SHENZHEN", font=font(F_SANS_B, 8), fill=(96, 82, 62), anchor="mm")
    fy, fh, fw = y + 14, 26, 46
    for fx, fn in [(x + 52, flag_us), (x + 130, flag_cn), (x + 208, flag_ru)]:
        d.line([T(fx - 3, fy - 2), T(fx - 3, y + 58)], fill=INK, width=2 * S)
        fn(d, fx, fy, fw, fh)
    for sx in (x + 103, x + 153, x + 203):
        d.ellipse(R(sx - 7, y + 38, sx + 7, y + 52), fill=INK)
        d.pieslice(R(sx - 13, y + 50, sx + 13, y + 72), 180, 360, fill=INK)
    d.ellipse(R(x + 55, y + 54, x + 251, y + 76), fill=(226, 218, 200), outline=INK, width=2 * S)
    for sx in (x + 103, x + 153, x + 203):
        d.rectangle(R(sx - 10, y + 60, sx + 10, y + 65), fill=RED)
        d.line([T(sx + 12, y + 60), T(sx + 16, y + 53)], fill=INK, width=S)
    d.rectangle(R(x, y + h - 12, x + w, y + h), fill=CARD)
    d.text(T(x + w / 2, y + h - 6), "FIRST TRILATERAL · 40-MIN BILATERAL FIRST", font=font(F_SANS_B, 7.5), fill=GRAY, anchor="mm")


def art_gta(d, x, y, w, h):
    # synthwave night over Vice City: banded sky, slitted sun, skyline, palms
    for i in range(int(h)):
        t = i / h
        c = (int(24 + 96 * t), int(16 + 26 * t), int(54 + 36 * t))
        d.rectangle(R(x, y + i, x + w, y + i + 1), fill=c)
    sx, sy, sr = x + 232, y + 30, 20
    d.ellipse(R(sx - sr, sy - sr, sx + sr, sy + sr), fill=(255, 138, 92))
    for i in range(5):
        yy = sy + 2 + i * 4
        d.rectangle(R(sx - sr, yy, sx + sr, yy + 1.6), fill=(int(24 + 96 * (yy - y) / h), int(16 + 26 * (yy - y) / h), int(54 + 36 * (yy - y) / h)))
    for bx, bw, bh in [(16, 20, 12), (44, 16, 18), (84, 22, 14), (120, 18, 20),
                       (156, 24, 12), (196, 16, 16), (240, 20, 14), (268, 18, 18)]:
        d.rectangle(R(x + bx, y + 60 - bh, x + bx + bw, y + 66), fill=(62, 32, 78))
    buildings = [(10, 26, 16), (30, 18, 22), (52, 30, 14), (70, 22, 20), (94, 34, 16),
                 (114, 20, 24), (142, 28, 14), (160, 16, 20), (184, 32, 16), (204, 22, 26),
                 (234, 26, 14), (252, 18, 22), (278, 30, 18)]
    for bx, bw, bh in buildings:
        d.rectangle(R(x + bx, y + 66 - bh, x + bx + bw, y + 66), fill=(14, 10, 26))
        for wi in range(bw // 5):
            for wj in range(bh // 6):
                if (wi * 7 + wj * 13 + bx) % 4 == 0:
                    d.rectangle(R(x + bx + 2 + wi * 5, y + 66 - bh + 2 + wj * 6,
                                  x + bx + 4 + wi * 5, y + 66 - bh + 4 + wj * 6), fill=(255, 214, 120))
    for gx in range(0, int(w) + 1, 24):
        x2 = min(max(x + w / 2 + (gx - w / 2) * 1.8, x), x + w)
        d.line([T(x + gx, y + 66), T(x2, y + 74)], fill=(255, 110, 180), width=S)
    d.line([T(x, y + 66), T(x + w, y + 66)], fill=(255, 110, 180), width=S)
    d.line([T(x, y + 70), T(x + w, y + 70)], fill=(200, 80, 150), width=S)

    def palm(px, py, ph):
        topx, topy = px + 3, py - ph
        d.polygon([T(px - 1.5, py), T(px + 1.5, py), T(topx + 1, topy), T(topx - 1, topy)], fill=(10, 8, 20))
        for a in (-170, -130, -90, -50, -10, 30):
            ar = math.radians(a)
            L = 13
            tipx = topx + L * math.cos(ar)
            tipy = topy + L * math.sin(ar) * 0.55 + 4
            midx = topx + L * 0.55 * math.cos(ar)
            midy = topy + L * 0.55 * math.sin(ar) * 0.3 - 2
            d.polygon([T(topx, topy), T(midx, midy - 1.5), T(tipx, tipy), T(midx, midy + 1.5)], fill=(10, 8, 20))
    palm(x + 26, y + 66, 26)
    palm(x + 64, y + 66, 20)
    d.text(T(x + 150, y + 34), "VI", font=font(F_SERIF_B, 34), fill=(255, 120, 180), anchor="mm")
    d.text(T(x + 150, y + 56), "V I C E  C I T Y", font=font(F_SANS_B, 8), fill=(255, 200, 230), anchor="mm")
    d.rectangle(R(x, y + h - 12, x + w, y + h), fill=(14, 10, 26))
    d.text(T(x + w / 2, y + h - 6), "OUT TODAY · PS5 / XBOX SERIES", font=font(F_SANS_B, 8), fill=(255, 200, 230), anchor="mm")


def art_ipo(d, x, y, w, h):
    for i in range(int(h)):
        t = i / h
        d.rectangle(R(x, y + i, x + w, y + i + 1),
                    fill=(int(22 - 8 * t), int(32 - 10 * t), int(27 - 8 * t)))
    d.text(T(x + 10, y + 8), "ANT · NASDAQ · DEBUT TODAY", font=font(F_SANS_B, 8), fill=(150, 220, 170))
    ax0, ax1 = x + 24, x + w - 24

    def px(v):
        return ax0 + (v - 65) / 25 * (ax1 - ax0)

    ay = y + 52
    d.line([T(ax0, ay), T(ax1, ay)], fill=(120, 150, 130), width=S)
    for v in (65, 70, 75, 80, 85, 90):
        d.line([T(px(v), ay - 2), T(px(v), ay + 2)], fill=(120, 150, 130), width=S)
        d.text(T(px(v), ay + 5), f"${v}", font=font(F_SANS, 7), fill=(130, 160, 140), anchor="ma")
    d.rectangle(R(px(70), y + 30, px(78), y + 44), fill=(70, 92, 80))
    d.text(T((px(70) + px(78)) / 2, y + 24), "MARKETED $70–78", font=font(F_SANS_B, 7), fill=(150, 220, 170), anchor="mm")
    d.line([T(px(83), y + 18), T(px(83), ay)], fill=(255, 120, 100), width=2 * S)
    d.rectangle(R(px(83) - 16, y + 6, px(83) + 16, y + 18), fill=RED)
    d.text(T(px(83), y + 12), "$83", font=font(F_SANS_B, 8.5), fill=(255, 255, 255), anchor="mm")
    d.rectangle(R(x, y + h - 12, x + w, y + h), fill=(10, 16, 14))
    d.text(T(x + w / 2, y + h - 6), "PRICED ABOVE $70–78 RANGE · ~$1.5TN VALUE", font=font(F_SANS_B, 8), fill=(150, 220, 170), anchor="mm")


# ── grid icons (24 px boxes) ─────────────────────────────────────────────────

def ic_scales(d, cx, cy, s):
    r = s / 2
    d.line([T(cx, cy - r * 0.7), T(cx, cy + r * 0.6)], fill=INK, width=2 * S)
    d.line([T(cx - r * 0.6, cy - r * 0.45), T(cx + r * 0.6, cy - r * 0.45)], fill=INK, width=2 * S)
    d.line([T(cx - r * 0.4, cy + r * 0.6), T(cx + r * 0.4, cy + r * 0.6)], fill=INK, width=2 * S)
    for sx in (-1, 1):
        px = cx + sx * r * 0.6
        d.arc(R(px - r * 0.26, cy - r * 0.1, px + r * 0.26, cy + r * 0.3), 0, 180, fill=RED, width=2 * S)
        d.line([T(px, cy - r * 0.45), T(px, cy - r * 0.1)], fill=INK, width=S)


def ic_thermo(d, cx, cy, s):
    r = s / 2
    d.rectangle(R(cx - r * 0.16, cy - r * 0.75, cx + r * 0.16, cy + r * 0.25), outline=INK, width=2 * S)
    d.ellipse(R(cx - r * 0.32, cy + r * 0.15, cx + r * 0.32, cy + r * 0.78), fill=RED)
    d.rectangle(R(cx - r * 0.07, cy - r * 0.4, cx + r * 0.07, cy + r * 0.3), fill=RED)
    for i in range(3):
        d.line([T(cx + r * 0.24, cy - r * 0.6 + i * r * 0.3), T(cx + r * 0.44, cy - r * 0.6 + i * r * 0.3)], fill=INK, width=S)


def ic_cyclone(d, cx, cy, s):
    r = s / 2
    for rr, a0, a1 in [(0.72, 0, 250), (0.48, 120, 380), (0.26, 240, 500)]:
        d.arc(R(cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr), a0, a1, fill=INK, width=2 * S)
    d.ellipse(R(cx - r * 0.1, cy - r * 0.1, cx + r * 0.1, cy + r * 0.1), fill=RED)


def ic_bridge(d, cx, cy, s):
    r = s / 2
    d.line([T(cx - r, cy + r * 0.3), T(cx - r * 0.25, cy + r * 0.3)], fill=INK, width=2 * S)
    d.line([T(cx + r * 0.25, cy + r * 0.3), T(cx + r, cy + r * 0.3)], fill=INK, width=2 * S)
    for tx in (cx - r * 0.6, cx + r * 0.6):
        d.line([T(tx, cy + r * 0.3), T(tx, cy - r * 0.6)], fill=INK, width=2 * S)
    d.arc(R(cx - r * 0.6, cy - r * 0.75, cx + r * 0.6, cy + r * 0.15), 10, 170, fill=INK, width=2 * S)
    for sx in (-0.3, 0.0, 0.3):
        d.line([T(cx + r * sx, cy - r * 0.32), T(cx + r * sx, cy + r * 0.3)], fill=INK, width=S)
    d.line([T(cx - r * 0.15, cy + r * 0.3), T(cx - r * 0.02, cy + r * 0.62)], fill=RED, width=2 * S)
    d.line([T(cx + r * 0.15, cy + r * 0.3), T(cx + r * 0.02, cy + r * 0.62)], fill=RED, width=2 * S)


def ic_radar(d, cx, cy, s):
    r = s / 2
    d.arc(R(cx - r * 0.7, cy - r * 0.2, cx + r * 0.3, cy + r * 0.8), 180, 360, fill=INK, width=2 * S)
    d.line([T(cx - r * 0.2, cy + r * 0.3), T(cx + r * 0.3, cy - r * 0.5)], fill=INK, width=2 * S)
    for rr in (0.35, 0.6, 0.85):
        d.arc(R(cx + r * 0.3 - r * rr, cy - r * 0.5 - r * rr, cx + r * 0.3 + r * rr, cy - r * 0.5 + r * rr), -60, 30, fill=RED, width=S)


def ic_tank(d, cx, cy, s):
    r = s / 2
    d.rounded_rectangle(R(cx - r * 0.85, cy + r * 0.15, cx + r * 0.85, cy + r * 0.6), radius=r * 0.2, fill=INK)
    for wx in (-0.6, -0.2, 0.2, 0.6):
        d.ellipse(R(cx + r * wx - r * 0.13, cy + r * 0.24, cx + r * wx + r * 0.13, cy + r * 0.5), fill=PAPER)
    d.rounded_rectangle(R(cx - r * 0.6, cy - r * 0.15, cx + r * 0.55, cy + r * 0.18), radius=r * 0.08, fill=INK)
    d.pieslice(R(cx - r * 0.35, cy - r * 0.5, cx + r * 0.25, cy - r * 0.05), 180, 360, fill=INK)
    d.line([T(cx + r * 0.2, cy - r * 0.3), T(cx + r * 0.95, cy - r * 0.5)], fill=INK, width=2 * S)
    d.line([T(cx - r * 0.85, cy + r * 0.72), T(cx + r * 0.85, cy + r * 0.72)], fill=RED, width=2 * S)


def ic_exam(d, cx, cy, s):
    r = s / 2
    d.rectangle(R(cx - r * 0.55, cy - r * 0.75, cx + r * 0.45, cy + r * 0.75), outline=INK, width=2 * S, fill=CARD)
    for i in range(3):
        d.line([T(cx - r * 0.35, cy - r * 0.45 + i * r * 0.3), T(cx + r * 0.25, cy - r * 0.45 + i * r * 0.3)], fill=GRAY, width=S)
    d.line([T(cx + r * 0.15, cy + r * 0.55), T(cx + r * 0.75, cy - r * 0.35)], fill=RED, width=3 * S)
    d.polygon([T(cx + r * 0.75, cy - r * 0.35), T(cx + r * 0.62, cy - r * 0.42), T(cx + r * 0.68, cy - r * 0.2)], fill=INK)


def ic_banner(d, cx, cy, s):
    r = s / 2
    d.line([T(cx, cy - r * 0.2), T(cx, cy + r * 0.85)], fill=INK, width=2 * S)
    d.rectangle(R(cx - r * 0.65, cy - r * 0.8, cx + r * 0.65, cy - r * 0.15), fill=CARD, outline=INK, width=2 * S)
    d.rectangle(R(cx - r * 0.08, cy - r * 0.66, cx + r * 0.08, cy - r * 0.4), fill=RED)
    d.ellipse(R(cx - r * 0.08, cy - r * 0.34, cx + r * 0.08, cy - r * 0.24), fill=RED)


def ic_downchart(d, cx, cy, s):
    r = s / 2
    for i, hh in enumerate([0.7, 0.55, 0.4, 0.25]):
        bx = cx - r * 0.7 + i * r * 0.38
        d.rectangle(R(bx, cy + r * 0.6 - r * hh, bx + r * 0.26, cy + r * 0.6), fill=INK if i < 3 else RED)
    d.line([T(cx - r * 0.6, cy - r * 0.5), T(cx + r * 0.5, cy + r * 0.1)], fill=RED, width=2 * S)
    d.polygon([T(cx + r * 0.62, cy + r * 0.22), T(cx + r * 0.28, cy + r * 0.1), T(cx + r * 0.5, cy - r * 0.14)], fill=RED)


def ic_flood(d, cx, cy, s):
    r = s / 2
    d.polygon([T(cx - r * 0.55, cy - r * 0.1), T(cx, cy - r * 0.65), T(cx + r * 0.55, cy - r * 0.1)], fill=INK)
    d.rectangle(R(cx - r * 0.4, cy - r * 0.1, cx + r * 0.4, cy + r * 0.35), fill=INK)
    for i, wx in enumerate((-0.7, -0.2, 0.3)):
        d.arc(R(cx + r * wx - r * 0.25, cy + r * 0.3 + i * 0, cx + r * wx + r * 0.25, cy + r * 0.62), 0, 180, fill=RED, width=2 * S)
    d.line([T(cx - r * 0.85, cy + r * 0.72), T(cx + r * 0.85, cy + r * 0.72)], fill=GRAY, width=S)


# ── the day's stories ────────────────────────────────────────────────────────

LEADS = [
    dict(n=1, region="ASIA", city="SHENZHEN", topic="SUMMIT", lat=22.5, lon=114.1,
         head="Trump, Xi & Putin hold first three-way summit",
         body="The US, Chinese and Russian leaders meet at APEC — their first trilateral. Nuclear arms limits and ending the wars in Ukraine and Iran top the agenda; a 40-minute Trump–Putin bilateral beforehand.",
         src="Reuters · AP · Al Jazeera", art=art_summit),
    dict(n=2, region="AMERICAS", city="NEW YORK", topic="GAMES", lat=40.7, lon=-74.0,
         head="GTA VI arrives after a 13-year wait",
         body="Rockstar's crime saga opens in Vice City at midnight, region by region — New Zealand first. Euphoric reviews for the $1bn+ production; Twitch calls it its biggest game launch ever.",
         src="AP · AFP · Engadget", art=art_gta),
    dict(n=3, region="AMERICAS", city="NASDAQ", topic="MARKETS", lat=40.75, lon=-73.98,
         head="Anthropic debuts in the biggest IPO on record",
         body="The Claude maker priced at $83 a share Wednesday, raising $81.3bn at a ~$1.5tn valuation. Trading starts on Nasdaq today as ANT; investors call demand robust.",
         src="Reuters · CNBC · NPR", art=art_ipo),
]

GRID = [
    dict(n=4, region="EUROPE", city="THE HAGUE", topic="LAW", lat=52.1, lon=4.3, icon=ic_scales,
         head="ICJ: Rohingya genocide ruling",
         body="The World Court finds Myanmar forces killed thousands of Rohingya; the landmark verdict is read out in The Hague."),
    dict(n=5, region="MIDEAST", city="ANTALYA", topic="CLIMATE", lat=36.9, lon=30.7, icon=ic_thermo,
         head="COP31: $120bn goal dropped",
         body="Draft drops the $120bn/yr adaptation goal as El Niño raises stakes; talks end Friday. Adaptation Fund pledges: $50m."),
    dict(n=6, region="ASIA", city="ODISHA", topic="STORM", lat=19.4, lon=85.0, icon=ic_cyclone,
         head="Cyclone Akvan: 105,000 moved",
         body="Odisha moves 105,304 to 9,299 shelters; landfall Friday near Puri, winds to 110 km/h; schools shut."),
    dict(n=7, region="EUROPE", city="KERCH", topic="WAR", lat=45.3, lon=36.5, icon=ic_bridge,
         head="Bridge hit again, rail halted",
         body="Ukraine's third strike in a week halts rail traffic; a road span already fell into the sea. Two Russian refineries also hit."),
    dict(n=8, region="AMERICAS", city="WASHINGTON", topic="CLAIM", lat=38.9, lon=-77.0, icon=ic_radar,
         head="US weighs new Iran offensive",
         body="Reported plans for a fresh offensive; Trump threatens retaliation over a 'dirty bomb' plot claim."),
    dict(n=9, region="MIDEAST", city="NUSEIRAT", topic="WAR", lat=31.4, lon=34.4, icon=ic_tank,
         head="Gaza: tanks cross Yellow Line",
         body="First ground advance since the 2025 ceasefire; residents flee as shelling and airstrikes continue."),
    dict(n=10, region="ASIA", city="SEOUL", topic="EDUCATION", lat=37.5, lon=127.0, icon=ic_exam,
         head="Suneung: alarms hunt phones",
         body="551,864 sit the last exam of its kind; phone-hunt alarms find 22 hidden handsets. Offices open late."),
    dict(n=11, region="AMERICAS", city="BOGOTÁ", topic="LABOUR", lat=4.7, lon=-74.1, icon=ic_banner,
         head="National strike against bill",
         body="Unions march on Plaza de Bolívar against the Economic Rescue Bill; transit disrupted in five cities."),
    dict(n=12, region="OCEANIA", city="CANBERRA", topic="ECONOMY", lat=-35.3, lon=149.1, icon=ic_downchart,
         head="Jobless rate climbs to 4.9%",
         body="October unemployment at a five-year high; employment fell 43,500 — the third straight month of weakening."),
    dict(n=13, region="AMERICAS", city="MIAMI", topic="WEATHER", lat=25.8, lon=-80.2, icon=ic_flood,
         head="Schools shut as floods linger",
         body="Miami-Dade and Broward close all schools; 12–15 in of rain fell in Broward; flash-flood warnings on the Space Coast."),
]

BRIEFS = [
    dict(n=14, region="AMERICAS", city="MEXICO CITY", text="CETES 6.19%; peso at 18.45/USD", lat=19.4, lon=-99.1),
    dict(n=15, region="EUROPE", city="LONDON", text="'Blackout' AI hoax; no outage, grid says", lat=51.5, lon=-0.1),
    dict(n=16, region="ASIA", city="NEW DELHI", text="AQI 286; smog curbs held to Nov 20", lat=28.6, lon=77.2),
    dict(n=17, region="AMERICAS", city="WASHINGTON", text="Fed minutes hint at Dec hike", lat=38.95, lon=-77.05),
    dict(n=18, region="AMERICAS", city="NEW YORK", text="Van Gogh record; provenance row", lat=40.72, lon=-73.99),
    dict(n=19, region="AMERICAS", city="NEW YORK", text="Bodega cats finally get their due", lat=40.73, lon=-73.97),
    dict(n=20, region="AMERICAS", city="UNITED STATES", text="Measles makes a comeback", lat=39.0, lon=-98.0),
    dict(n=21, region="AMERICAS", city="UNITED STATES", text="Thanksgiving dinner costs more", lat=38.5, lon=-97.5),
    dict(n=22, region="OCEANIA", city="SYDNEY", text="Data-centre emissions to rise 70%", lat=-33.9, lon=151.2),
    dict(n=23, region="AMERICAS", city="BENTONVILLE", text="Walmart earnings due today", lat=36.4, lon=-94.2),
    dict(n=24, region="AMERICAS", city="SANTA CLARA", text="Nvidia board keeps Huang out", lat=37.4, lon=-122.0),
    dict(n=25, region="EUROPE", city="COPENHAGEN", text="Greenland–US Arctic pact passes", lat=55.7, lon=12.6),
    dict(n=26, region="ASIA", city="DHAKA", text="Lockdown as Hasina-return unrest grows", lat=23.8, lon=90.4),
    dict(n=27, region="ASIA", city="SEOUL", text="Ex-PM's martial-law charges overturned", lat=37.55, lon=126.95),
    dict(n=28, region="AMERICAS", city="WASHINGTON", text="US–Venezuela military ties back", lat=38.85, lon=-76.95),
    dict(n=29, region="EUROPE", city="LONDON", text="UK–EU summit to reset Brexit ties", lat=51.52, lon=-0.15),
    dict(n=30, region="MIDEAST", city="RIYADH", text="Houthi missile debris damages tower", lat=24.7, lon=46.7),
    dict(n=31, region="MIDEAST", city="HORMUZ", text="Shipping blocked amid Gulf escalation", lat=26.6, lon=56.3),
    dict(n=32, region="ASIA", city="TOKYO", text="Asian equities muted before AI debut", lat=35.7, lon=139.7),
    dict(n=33, region="WORLD", city="ON THIS DAY", text="Gettysburg 1863 · Apollo 12 1969", lat=39.8, lon=-77.2),
    dict(n=34, region="AFRICA", city="KHARTOUM", text="Hemedti gets 2nd death sentence", lat=15.6, lon=32.5),
    dict(n=35, region="OCEANIA", city="AUCKLAND", text="First city to unlock GTA VI at midnight", lat=-36.8, lon=174.8),
    dict(n=36, region="AFRICA", city="MOGADISHU", text="Somalia expels UAE envoy: 72h", lat=2.0, lon=45.3),
]

STATS = [
    ("$81.3bn", "raised in the biggest IPO"),
    ("13 yrs", "the wait for GTA VI"),
    ("551,864", "take the Suneung exam"),
    ("105,304", "evacuated for Cyclone Akvan"),
    ("$120bn", "adaptation goal dropped"),
    ("4.9%", "Australia's jobless rate"),
]

# second classification axis: every story also belongs to one of eight fields
FIELD_OF = {
    1: "POLITICS & DIPLOMACY", 2: "SOCIETY & CULTURE", 3: "ECONOMY & LABOUR",
    4: "JUSTICE", 5: "CLIMATE & ENVIRONMENT", 6: "DISASTERS & WEATHER",
    7: "WAR & SECURITY", 8: "WAR & SECURITY", 9: "WAR & SECURITY",
    10: "SOCIETY & CULTURE", 11: "ECONOMY & LABOUR", 12: "ECONOMY & LABOUR",
    13: "DISASTERS & WEATHER", 14: "ECONOMY & LABOUR", 15: "TECH & AI",
    16: "DISASTERS & WEATHER", 17: "ECONOMY & LABOUR", 18: "SOCIETY & CULTURE",
    19: "SOCIETY & CULTURE", 20: "SOCIETY & CULTURE", 21: "SOCIETY & CULTURE",
    22: "CLIMATE & ENVIRONMENT", 23: "ECONOMY & LABOUR", 24: "TECH & AI",
    25: "POLITICS & DIPLOMACY", 26: "SOCIETY & CULTURE", 27: "JUSTICE",
    28: "POLITICS & DIPLOMACY", 29: "POLITICS & DIPLOMACY", 30: "WAR & SECURITY",
    31: "WAR & SECURITY", 32: "ECONOMY & LABOUR", 33: "SOCIETY & CULTURE",
    34: "JUSTICE", 35: "SOCIETY & CULTURE", 36: "POLITICS & DIPLOMACY",
}

# stylized continent outlines (lon, lat) for the locator map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 72), (-80, 70), (-65, 60), (-55, 50),
     (-70, 44), (-75, 38), (-81, 31), (-81, 25), (-90, 29), (-97, 26), (-97, 20),
     (-105, 20), (-110, 24), (-117, 33), (-124, 40), (-125, 49), (-135, 58), (-152, 60)],
    [(-58, 64), (-45, 60), (-22, 70), (-20, 76), (-35, 79), (-55, 78)],
    [(-78, 8), (-62, 10), (-52, 4), (-44, -2), (-35, -8), (-38, -15), (-48, -25),
     (-53, -34), (-58, -39), (-65, -45), (-68, -52), (-72, -50), (-73, -40),
     (-71, -30), (-70, -18), (-76, -10), (-80, -3)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 52), (5, 58), (10, 58), (18, 56),
     (22, 60), (28, 60), (30, 66), (40, 66), (45, 60), (40, 50), (30, 46), (28, 41),
     (22, 38), (15, 38), (10, 44), (3, 43), (-2, 36)],
    [(-17, 15), (-10, 25), (-5, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 12), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (9, -5), (5, 5), (-5, 5), (-10, 8)],
    [(30, 46), (40, 50), (45, 60), (40, 66), (50, 70), (70, 72), (100, 72), (130, 70),
     (160, 66), (170, 62), (160, 58), (150, 50), (140, 45), (130, 40), (122, 35),
     (120, 28), (110, 20), (105, 10), (100, 5), (98, 10), (92, 20), (88, 22),
     (80, 10), (77, 8), (72, 20), (66, 25), (58, 25), (52, 28), (48, 30), (43, 12),
     (35, 28), (32, 31), (28, 41)],
    [(114, -22), (122, -18), (130, -12), (136, -12), (142, -11), (146, -15), (150, -22),
     (153, -28), (150, -35), (144, -38), (138, -35), (132, -32), (124, -33), (116, -34), (114, -28)],
    [(-5, 50), (-3, 53), (-5, 58), (-2, 57), (0, 52)],
    [(130, 31), (135, 34), (140, 36), (141, 41), (143, 44), (140, 42), (136, 36), (131, 33)],
    [(95, 5), (102, -2), (106, -6), (103, -5), (97, 2)],
    [(109, 1), (115, 4), (119, 1), (116, -3), (110, -2)],
    [(105, -6), (112, -7), (114, -8), (108, -7)],
    [(44, -12), (48, -14), (50, -18), (47, -24), (44, -20)],
    [(173, -35), (175, -38), (174, -40), (172, -44), (168, -46), (170, -43), (172, -40)],
]


def draw_map(d, x, y, w, h):
    d.rectangle(R(x, y, x + w, y + h), fill=NAVY)
    lon0, lon1, lat0, lat1 = -180, 180, 78, -58

    def proj(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w, y + (lat0 - lat) / (lat0 - lat1) * h)

    for glon in range(-150, 180, 30):
        a, b = proj(glon, lat0), proj(glon, lat1)
        d.line([T(*a), T(*b)], fill=(32, 42, 62), width=S)
    for glat in range(-30, 78, 30):
        a, b = proj(lon0, glat), proj(lon1, glat)
        d.line([T(*a), T(*b)], fill=(32, 42, 62), width=S)
    for poly in CONTINENTS:
        d.polygon([T(*proj(lon, lat)) for lon, lat in poly], fill=LAND, outline=LAND_EDGE)
    # brief dots first, numbered pins on top (relaxed apart so numbers stay legible)
    for s in BRIEFS:
        px, py = proj(s["lon"], s["lat"])
        d.ellipse(R(px - 2.2, py - 2.2, px + 2.2, py + 2.2), fill=(186, 186, 180))
    pins = [[*proj(s["lon"], s["lat"]), s["n"]] for s in LEADS + GRID]
    for _ in range(40):
        for i in range(len(pins)):
            for j in range(i + 1, len(pins)):
                dx = pins[j][0] - pins[i][0]
                dy = pins[j][1] - pins[i][1]
                dist = math.hypot(dx, dy)
                if dist < 15:
                    if dist < 0.01:
                        dx, dy, dist = 1.0, 0.3, 1.04
                    push = (15 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pins[i][0] -= ux * push
                    pins[i][1] -= uy * push
                    pins[j][0] += ux * push
                    pins[j][1] += uy * push
    for px, py, n in pins:
        px = min(max(px, x + 6), x + w - 6)
        py = min(max(py, y + 6), y + h - 6)
        d.ellipse(R(px - 5.5, py - 5.5, px + 5.5, py + 5.5), fill=RED, outline=PAPER, width=S)
        d.text(T(px, py + 0.3), str(n), font=font(F_SANS_B, 7), fill=(255, 255, 255), anchor="mm")


def grain(img):
    """Deterministic paper-grain overlay: kills the sterile-vector look."""
    import random
    rng = random.Random(20261119)
    tile = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    px = tile.load()
    for ty in range(128):
        for tx in range(128):
            r = rng.random()
            if r < 0.06:
                v = 0 if r < 0.03 else 255
                px[tx, ty] = (v, v, v, 10)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for oy in range(0, img.size[1], 128):
        for ox in range(0, img.size[0], 128):
            overlay.paste(tile, (ox, oy))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def main():
    all_stories = LEADS + GRID + BRIEFS
    assert len(all_stories) == 36, f"story count {len(all_stories)} != 36"
    assert [s["n"] for s in all_stories] == list(range(1, 37))
    tally = {}
    for s in all_stories:
        tally[s["region"]] = tally.get(s["region"], 0) + 1
    assert sum(tally.values()) == 36

    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    f_run = font(F_SANS_B, 10.5)
    f_date = font(F_SERIF_B, 44)
    f_deck = font(F_SERIF, 13)
    f_tally = font(F_SANS_B, 9)
    f_field = font(F_SANS_B, 8)
    f_time = font(F_SANS, 8.5)
    f_timeb = font(F_SANS_B, 8.5)
    f_stat = font(F_SERIF_B, 22)
    f_statcap = font(F_SANS, 9)
    f_kick = font(F_SANS_B, 10.5)
    f_lhead = font(F_SERIF_B, 18)
    f_lbody = font(F_SANS, 10.4)
    f_src = font(F_SANS, 8.5)
    f_gkick = font(F_SANS_B, 9)
    f_ghead = font(F_SERIF_B, 13.8)
    f_gbody = font(F_SANS, 9.9)
    f_sec = font(F_SANS_B, 12)
    f_brief = font(F_SANS, 9.6)
    f_briefb = font(F_SANS_B, 9.6)
    f_dc = font(F_SANS, 10)
    f_dcb = font(F_SANS_B, 10.2)
    f_foot = font(F_SANS, 9.8)

    # ── running head + nameplate date ──
    d.text(T(M, 16), "THE WORLD TODAY · WORLD EDITION · DAY 323 OF 2026", font=f_run, fill=GRAY)
    d.text(T(W - M, 16), "36 STORIES · 7 REGIONS · 8 FIELDS · 13 ILLUSTRATED", font=f_run, fill=RED, anchor="ra")
    d.line([T(M, 27), T(W - M, 27)], fill=INK, width=3 * S)
    d.line([T(M, 31), T(W - M, 31)], fill=GOLD, width=S)
    d.text(T(W / 2, 52), "Thursday 19 November 2026", font=f_date, fill=INK, anchor="mm")
    deck = "Three leaders meet in Shenzhen · GTA VI unlocks worldwide · A record IPO debuts · The World Court rules on the Rohingya"
    assert d.textlength(deck, font=f_deck) <= CW * S, "deck too wide"
    d.text(T(W / 2, 82), deck, font=f_deck, fill=RED, anchor="mm")
    d.line([T(M, 92), T(W - M, 92)], fill=INK, width=S)

    # ── region tally bar (counts derived from the story data) ──
    order = ["EUROPE", "AMERICAS", "ASIA", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]
    tx = M
    segw = CW / len(order)
    for reg in order:
        cnt = tally.get(reg, 0)
        d.rectangle(R(tx, 96, tx + segw, 114), fill=REGIONS[reg])
        d.text(T(tx + segw / 2, 105), f"{reg} {cnt}", font=f_tally, fill=(255, 255, 255), anchor="mm")
        tx += segw

    # ── field tally bar: the same 36 stories by subject ──
    ford = ["WAR & SECURITY", "POLITICS & DIPLOMACY", "ECONOMY & LABOUR", "SOCIETY & CULTURE",
            "JUSTICE", "CLIMATE & ENVIRONMENT", "DISASTERS & WEATHER", "TECH & AI"]
    ftally = {}
    for s in all_stories:
        f = FIELD_OF[s["n"]]
        ftally[f] = ftally.get(f, 0) + 1
    assert sum(ftally.values()) == 36 and len(ftally) == 8
    d.rectangle(R(M, 116, W - M, 132), fill=INK)
    fshort = {"WAR & SECURITY": "WAR & SEC.", "POLITICS & DIPLOMACY": "POLITICS",
              "ECONOMY & LABOUR": "ECONOMY", "SOCIETY & CULTURE": "SOCIETY",
              "JUSTICE": "JUSTICE", "CLIMATE & ENVIRONMENT": "CLIMATE",
              "DISASTERS & WEATHER": "WEATHER", "TECH & AI": "TECH & AI"}
    fw = CW / 8
    for i, f in enumerate(ford):
        label = f"{fshort[f]} {ftally[f]}"
        assert d.textlength(label, font=f_field) <= (fw - 4) * S, f"field label too wide: {label}"
        d.text(T(M + i * fw + fw / 2, 124), label, font=f_field, fill=GOLD, anchor="mm")

    # ── the day by hours (UTC anchors verified from the reporting) ──
    d.text(T(M, 140), "THE DAY BY HOURS · UTC", font=f_timeb, fill=RED)
    ticker = "00:30 ABS jobs · 05:00 GTA unlocks US East · 08:45 Suneung ends · 14:00 Bogotá marches · 14:30 ANT first trade"
    assert d.textlength(ticker, font=f_time) <= (CW - 150) * S, "ticker too wide"
    d.text(T(M + 150, 140), ticker, font=f_time, fill=GRAY)

    # ── key figures: navy band, gold serif figures ──
    d.rectangle(R(M, 150, W - M, 196), fill=(24, 32, 48))
    d.line([T(M, 150), T(W - M, 150)], fill=GOLD, width=S)
    d.line([T(M, 196), T(W - M, 196)], fill=GOLD, width=S)
    cellw = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cellw
        if i:
            d.line([T(cx, 156), T(cx, 190)], fill=(52, 62, 82), width=S)
        d.text(T(cx + cellw / 2, 168), num, font=f_stat, fill=GOLD, anchor="mm")
        lines = wrap(d, cap, f_statcap, cellw - 12)
        assert len(lines) == 1, f"stat caption wraps: {cap}"
        d.text(T(cx + cellw / 2, 184), cap, font=f_statcap, fill=(232, 228, 216), anchor="mm")

    # ── three lead cards ──
    lw, lh, lgap = (CW - 2 * 17) / 3, 204, 17
    for i, s in enumerate(LEADS):
        x0 = M + i * (lw + lgap)
        y0 = 204
        d.rectangle(R(x0, y0, x0 + lw, y0 + lh), fill=CARD, outline=LINE, width=S)
        d.rectangle(R(x0 + 1, y0 + 1, x0 + lw - 1, y0 + 4), fill=REGIONS[s["region"]])
        s["art"](d, x0 + 1, y0 + 4, lw - 2, 83)
        d.text(T(x0 + 10, y0 + 96), f"{s['n']} · {s['city']} · {s['topic']}", font=f_kick, fill=RED)
        d.text(T(x0 + lw - 10, y0 + 97), s["src"], font=f_src, fill=GRAY, anchor="ra")
        hy = para(d, (x0 + 10, y0 + 110), s["head"], f_lhead, lw - 20, INK, 1.12, maxlines=2)
        by = para(d, (x0 + 10, hy + 2), s["body"], f_lbody, lw - 20, INK, 1.15, maxlines=4)
        assert by <= y0 + lh - 2, f"lead {s['n']} body overflows: {by}"

    d.line([T(M, 416), T(W - M, 416)], fill=INK, width=2 * S)

    # ── ten grid stories, 2 x 5 ──
    gw, gh, ggap = (CW - 4 * 8) / 5, 124, 8
    for i, s in enumerate(GRID):
        r, c = divmod(i, 5)
        x0 = M + c * (gw + ggap)
        y0 = 424 + r * (gh + ggap)
        d.rectangle(R(x0, y0, x0 + gw, y0 + gh), fill=CARD, outline=LINE, width=S)
        d.rectangle(R(x0 + 1, y0 + 1, x0 + gw - 1, y0 + 4), fill=REGIONS[s["region"]])
        d.ellipse(R(x0 + 5, y0 + 6, x0 + 23, y0 + 24), fill=RED)
        d.text(T(x0 + 14, y0 + 15.3), str(s["n"]), font=font(F_SANS_B, 9.5), fill=(255, 255, 255), anchor="mm")
        d.text(T(x0 + 28, y0 + 9), f"{s['city']} · {s['topic']}", font=f_gkick, fill=GRAY)
        s["icon"](d, x0 + gw - 20, y0 + 20, 22)
        hy = para(d, (x0 + 8, y0 + 30), s["head"], f_ghead, gw - 16, INK, 1.1, maxlines=2)
        by = para(d, (x0 + 8, hy + 3), s["body"], f_gbody, gw - 16, INK, 1.15, maxlines=4)
        assert by <= y0 + gh - 4, f"grid {s['n']} body overflows: {by} > {y0 + gh - 4}"

    d.line([T(M, 680), T(W - M, 680)], fill=INK, width=2 * S)

    # ── bottom split: locator map + 23 briefs ──
    d.text(T(M, 690), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    draw_map(d, M, 706, 380, 176)
    d.ellipse(R(M + 2, 888, M + 8, 894), fill=RED)
    d.text(T(M + 12, 886), "1–13 leads & grid", font=f_foot, fill=GRAY)
    d.ellipse(R(M + 108, 888, M + 114, 894), fill=(150, 150, 145))
    d.text(T(M + 118, 886), "14–36 briefs · positions approximate", font=f_foot, fill=GRAY)

    bx0 = M + 396
    d.text(T(bx0, 690), "ALSO ON THURSDAY — 23 MORE STORIES", font=f_sec, fill=INK)
    colw = (W - M - bx0 - 14) / 2
    for i, s in enumerate(BRIEFS):
        col, row = divmod(i, 12)
        x = bx0 + col * (colw + 14)
        y = 708 + row * 16.4
        num = str(s["n"])
        d.text(T(x, y), num, font=f_briefb, fill=RED)
        nx = x + d.textlength(num + " ", font=f_briefb) / S
        city = s["city"]
        d.text(T(nx, y), city + " — ", font=f_briefb, fill=INK)
        cx2 = nx + d.textlength(city + " — ", font=f_briefb) / S
        rest = colw - (cx2 - x)
        lines = wrap(d, s["text"], f_brief, rest)
        assert len(lines) == 1, f"brief {s['n']} wraps: {s['text']!r} ({rest:.0f}px left)"
        d.text(T(cx2, y), s["text"], font=f_brief, fill=INK)

    # ── date check box ──
    d.rectangle(R(M, 908, W - M, 952), outline=RED, width=2 * S)
    d.text(T(M + 8, 914), "DATE CHECK — NOT COUNTED: FIRST REPORTED BEFORE THURSDAY", font=f_dcb, fill=RED)
    l1 = "Wed 18: Iran's Kuwait & Bahrain strikes · Anthropic's $83 pricing · GTA's $1.5bn pre-orders · Gaza's first tank advance (counted above as Thursday's ongoing shelling)."
    l2 = "Mon 16: UK blackout hoax debunked · first COP31 draft. Akvan formed Nov 16 — counted as today's evacuations. GTA's NZ unlock Wed 11:00 GMT sits within today's rollout."
    for ln in (l1, l2):
        assert d.textlength(ln, font=f_dc) <= (CW - 16) * S, f"date check line too wide: {ln[:50]}"
    d.text(T(M + 8, 928), l1, font=f_dc, fill=INK)
    d.text(T(M + 8, 940), l2, font=f_dc, fill=INK)

    # ── footer ──
    d.line([T(M, 962), T(W - M, 962)], fill=LINE, width=S)
    d.text(T(M, 970), "Sources: Reuters · AP · AFP · BBC · Al Jazeera · Euronews · CNBC · NPR · The Hindu · IMD · ABS · ICJ · Korea Herald · National Grid — reporting of 19 Nov 2026 (UTC).", font=f_foot, fill=GRAY)
    d.text(T(M, 984), "Original geometric drawings · disputed claims attributed, not stated as fact · every story occurred or was first reported on the date.", font=f_foot, fill=GRAY)
    d.text(T(W - M, 984), "The World Today · make.fun", font=f_foot, fill=GRAY, anchor="ra")

    img = grain(img)
    final = img.resize((W, H), Image.LANCZOS)
    out = ROOT / "entry.png"
    final.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {final.size[0]}x{final.size[1]})")
    print("tally:", tally)


if __name__ == "__main__":
    main()
