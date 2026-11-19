#!/usr/bin/env python3
"""Render the entry image: a one-page front page summing up 19 November 2026 world news.

Original geometric artwork drawn with Pillow (no photographs, no third-party art).
Facts as reported on 19 Nov 2026 by Reuters, AP, AFP, Al Jazeera, BBC, Euronews.
Run:  python3 tools/make_image.py   (writes entry.png at the repository root)
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W = H = 1024
M = 40  # page margin

PAPER = (246, 241, 231)
CARD = (251, 248, 240)
INK = (26, 26, 24)
GRAY = (107, 101, 88)
RED = (179, 39, 30)
LINE = (58, 54, 46)
PANEL = (238, 232, 218)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, maxw, fill, leading=1.22):
    x, y = xy
    lh = int(fnt.size * leading)
    for ln in wrap(draw, text, fnt, maxw):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def star(draw, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.42
        a = math.radians(rot + i * 36)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    draw.polygon(pts, fill=fill)


def flag_us(draw, x, y, w, h):
    sh = h / 13
    for i in range(13):
        draw.rectangle([x, y + i * sh, x + w, y + (i + 1) * sh],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.42, sh * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            star(draw, x + cw * (c + 0.5) / 5, y + ch * (r + 0.5) / 4, 2.6, (255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.18, y + h * 0.28, h * 0.17, (255, 222, 0))
    for dx, dy, rot in [(0.36, 0.10, -60), (0.44, 0.22, -30), (0.44, 0.38, 0), (0.36, 0.50, 30)]:
        star(draw, x + w * dx, y + h * dy, h * 0.055, (255, 222, 0), rot=rot)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 43, 30)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def icon_bridge(draw, cx, cy, s):
    # suspension bridge with a broken central span, over water
    d = s / 2
    draw.line([cx - d, cy + d * 0.45, cx - d * 0.25, cy + d * 0.45], fill=INK, width=4)
    draw.line([cx + d * 0.25, cy + d * 0.45, cx + d, cy + d * 0.45], fill=INK, width=4)
    for tx in (cx - d * 0.62, cx + d * 0.62):
        draw.line([tx, cy + d * 0.45, tx, cy - d * 0.55], fill=INK, width=4)
    draw.arc([cx - d * 0.62, cy - d * 0.55, cx + d * 0.62, cy + d * 0.75], 200, 340, fill=INK, width=3)
    draw.line([cx - d * 0.18, cy + d * 0.45, cx - d * 0.05, cy + d * 0.72], fill=RED, width=3)
    draw.line([cx + d * 0.18, cy + d * 0.45, cx + d * 0.05, cy + d * 0.72], fill=RED, width=3)
    for wx in (-0.7, -0.2, 0.3, 0.8):
        draw.arc([cx + d * wx - 8, cy + d * 0.8, cx + d * wx + 8, cy + d * 0.98], 0, 180, fill=GRAY, width=2)


def icon_drone(draw, cx, cy, s):
    d = s / 2
    draw.ellipse([cx - d * 0.28, cy - d * 0.12, cx + d * 0.28, cy + d * 0.16], fill=INK)
    for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        ax, ay = cx + sx * d * 0.62, cy + sy * d * 0.42
        draw.line([cx + sx * d * 0.18, cy + sy * d * 0.06, ax, ay], fill=INK, width=3)
        draw.ellipse([ax - d * 0.22, ay - d * 0.07, ax + d * 0.22, ay + d * 0.07], outline=INK, width=3)
    draw.line([cx, cy + d * 0.16, cx, cy + d * 0.55], fill=RED, width=3)
    draw.polygon([(cx - 5, cy + d * 0.5), (cx + 5, cy + d * 0.5), (cx, cy + d * 0.72)], fill=RED)


def icon_scales(draw, cx, cy, s):
    d = s / 2
    draw.line([cx, cy - d * 0.7, cx, cy + d * 0.55], fill=INK, width=4)
    draw.line([cx - d * 0.55, cy - d * 0.45, cx + d * 0.55, cy - d * 0.45], fill=INK, width=4)
    draw.line([cx - d * 0.35, cy + d * 0.55, cx + d * 0.35, cy + d * 0.55], fill=INK, width=4)
    for sx in (-1, 1):
        px = cx + sx * d * 0.55
        draw.line([px, cy - d * 0.45, px - d * 0.22, cy + d * 0.05], fill=INK, width=2)
        draw.line([px, cy - d * 0.45, px + d * 0.22, cy + d * 0.05], fill=INK, width=2)
        draw.arc([px - d * 0.24, cy - d * 0.05, px + d * 0.24, cy + d * 0.28], 0, 180, fill=INK, width=3)
    star(draw, cx, cy - d * 0.78, d * 0.12, RED)


def icon_chart(draw, cx, cy, s):
    d = s / 2
    draw.line([cx - d * 0.7, cy + d * 0.6, cx + d * 0.7, cy + d * 0.6], fill=INK, width=3)
    for i, hh in enumerate([0.3, 0.5, 0.75, 1.05]):
        bx = cx - d * 0.6 + i * d * 0.36
        draw.rectangle([bx, cy + d * 0.6 - d * hh, bx + d * 0.24, cy + d * 0.6],
                       fill=RED if i == 3 else INK)
    draw.line([cx - d * 0.62, cy + d * 0.18, cx + d * 0.5, cy - d * 0.62], fill=GRAY, width=3)
    draw.polygon([(cx + d * 0.66, cy - d * 0.74), (cx + d * 0.34, cy - d * 0.6),
                  (cx + d * 0.58, cy - d * 0.36)], fill=GRAY)


def icon_chip(draw, cx, cy, s):
    d = s / 2
    draw.rectangle([cx - d * 0.5, cy - d * 0.5, cx + d * 0.5, cy + d * 0.5], outline=INK, width=4)
    draw.rectangle([cx - d * 0.22, cy - d * 0.22, cx + d * 0.22, cy + d * 0.22], fill=RED)
    for i in range(4):
        off = -d * 0.36 + i * d * 0.24
        draw.line([cx + off, cy - d * 0.5, cx + off, cy - d * 0.74], fill=INK, width=3)
        draw.line([cx + off, cy + d * 0.5, cx + off, cy + d * 0.74], fill=INK, width=3)
        draw.line([cx - d * 0.5, cy + off, cx - d * 0.74, cy + off], fill=INK, width=3)
        draw.line([cx + d * 0.5, cy + off, cx + d * 0.74, cy + off], fill=INK, width=3)


def icon_snow(draw, cx, cy, s):
    d = s / 2
    # shield outline with a snowflake inside
    draw.polygon([(cx - d * 0.62, cy - d * 0.62), (cx + d * 0.62, cy - d * 0.62),
                  (cx + d * 0.62, cy + d * 0.1), (cx, cy + d * 0.78),
                  (cx - d * 0.62, cy + d * 0.1)], outline=INK, width=4)
    for a in range(0, 180, 60):
        ar = math.radians(a)
        x1, y1 = cx - d * 0.36 * math.cos(ar), cy - d * 0.06 - d * 0.36 * math.sin(ar)
        x2, y2 = cx + d * 0.36 * math.cos(ar), cy - d * 0.06 + d * 0.36 * math.sin(ar)
        draw.line([x1, y1, x2, y2], fill=RED, width=3)
        for px, py in [(x1, y1), (x2, y2)]:
            for da in (-40, 40):
                br = math.radians(a + 180 + da) if (px, py) == (x1, y1) else math.radians(a + da)
                draw.line([px, py, px + d * 0.13 * math.cos(br), py + d * 0.13 * math.sin(br)], fill=RED, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(F_SERIF, 58)
    f_kicker = font(F_SANS_B, 14)
    f_date = font(F_SANS_B, 27)
    f_small = font(F_SANS, 13)
    f_tag = font(F_SANS_B, 14)
    f_head = font(F_SERIF, 45)
    f_sub = font(F_SANS, 19)
    f_src = font(F_SANS, 13)
    f_cardtag = font(F_SANS_B, 12)
    f_cardhead = font(F_SANS_B, 22)
    f_cardbody = font(F_SANS, 14)
    f_brief = font(F_SANS, 13)
    f_briefb = font(F_SANS_B, 13)
    f_foot = font(F_SANS, 12)

    # ── masthead ──
    d.text((W / 2, 26), "THE DAY'S WORLD NEWS, IN ONE IMAGE", font=f_kicker, fill=GRAY, anchor="mm")
    d.text((W / 2, 68), "The World Today", font=f_mast, fill=INK, anchor="mm")
    d.line([M, 104, W - M, 104], fill=INK, width=4)
    d.line([M, 111, W - M, 111], fill=INK, width=1)
    d.text((M, 126), "WORLD EDITION", font=f_small, fill=GRAY)
    d.text((W / 2, 126), "THURSDAY · 19 NOVEMBER 2026", font=f_date, fill=INK, anchor="ma")
    d.text((W - M, 126), "AS REPORTED · UTC", font=f_small, fill=GRAY, anchor="ra")
    d.line([M, 162, W - M, 162], fill=INK, width=2)

    # ── lead: first-ever US–China–Russia trilateral summit ──
    px0, py0, px1, py1 = M, 176, M + 330, 470
    d.rectangle([px0, py0, px1, py1], fill=PANEL, outline=LINE, width=2)
    # three flags on poles over a round table
    fy, fh, fw = py0 + 34, 62, 96
    for i, (fx, fn) in enumerate([(px0 + 26, flag_us), (px0 + 122, flag_cn), (px0 + 218, flag_ru)]):
        d.line([fx - 4, fy - 12, fx - 4, py0 + 218], fill=INK, width=4)
        fn(d, fx, fy, fw, fh)
    ty = py0 + 212
    d.ellipse([px0 + 60, ty, px0 + 270, ty + 48], outline=INK, width=4, fill=(228, 220, 202))
    for sx in (px0 + 95, px0 + 165, px0 + 235):
        d.ellipse([sx - 7, ty + 47, sx + 7, ty + 61], fill=INK)
    d.text(((px0 + px1) / 2, py1 - 10), "APEC · SHENZHEN, CHINA", font=f_tag, fill=GRAY, anchor="mm")

    tx = px1 + 22
    tw = W - M - tx
    d.rectangle([tx, 180, tx + 218, 204], fill=RED)
    d.text((tx + 9, 192), "FIRST-EVER TRILATERAL", font=f_tag, fill=(255, 255, 255), anchor="lm")
    y = para(d, (tx, 216), "Trump, Xi & Putin hold first three-way summit", f_head, tw, INK, 1.12)
    y = para(d, (tx, y + 10),
             "The US, Chinese and Russian leaders meet at APEC in Shenzhen — their first "
             "three-way summit. Nuclear arms limits and ending the wars in Ukraine and "
             "Iran top the agenda.", f_sub, tw, INK)
    f_sub2 = font(F_SANS, 17)
    y = para(d, (tx, y + 8),
             "Beforehand, a 40-minute Trump–Putin bilateral: no deal announced.",
             f_sub2, tw, GRAY)
    print(f"lead text ends at y={y}")
    d.text((tx, 456), "Reuters · AP · Al Jazeera", font=f_src, fill=GRAY)

    d.line([M, 484, W - M, 484], fill=INK, width=2)
    d.text((W / 2, 498), "THE DAY'S OTHER TOP STORIES", font=f_kicker, fill=GRAY, anchor="mm")

    # ── six story cards, 3 × 2 ──
    cards = [
        ("EUROPE · WAR", "Kerch Bridge hit again", icon_bridge,
         "Ukraine's third strike in a week halts rail traffic; a road span already fell into the sea. Two Russian refineries also hit."),
        ("MIDDLE EAST", "Iran war spreads", icon_drone,
         "Iranian drones target US sites in Bahrain and Kuwait; Houthi missile debris damages a Riyadh tower. Hormuz stays blocked."),
        ("ASIA · LAW", "ICJ: Rohingya verdict", icon_scales,
         "World Court finds Myanmar forces killed thousands of Rohingya; the landmark genocide ruling is read out in The Hague."),
        ("BUSINESS · AI", "Record Anthropic IPO", icon_chart,
         "Claude maker prices the largest IPO ever at $83 a share, raising about $81bn at a ~$1.5tn value; Nasdaq debut today as ANT."),
        ("TECHNOLOGY", "Nvidia board stands firm", icon_chip,
         "Directors say they will not reinstate Jensen Huang as CEO amid the China spy scandal; chips reached a military-linked lab."),
        ("EUROPE · ARCTIC", "Arctic security pact", icon_snow,
         "Denmark's parliament approves a Greenland–US deal to strengthen security in the Arctic and North Atlantic."),
    ]
    gx, gy = M, 516
    cw, ch, gap = 304, 182, 16
    for i, (tag, head, icon, body) in enumerate(cards):
        r, c = divmod(i, 3)
        x0, y0 = gx + c * (cw + gap), gy + r * (ch + gap)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=LINE, width=1)
        d.rectangle([x0, y0, x0 + 4, y0 + ch], fill=RED)
        icon(d, x0 + 42, y0 + 52, 56)
        d.text((x0 + 78, y0 + 14), tag, font=f_cardtag, fill=RED)
        hy = y0 + 32
        for ln in wrap(d, head, f_cardhead, cw - 92)[:2]:
            d.text((x0 + 78, hy), ln, font=f_cardhead, fill=INK)
            hy += 25
        para(d, (x0 + 16, y0 + 92), body, f_cardbody, cw - 32, INK, 1.24)

    # ── in-brief strip ──
    by = 906
    d.line([M, by - 8, W - M, by - 8], fill=INK, width=2)
    d.rectangle([M, by, M + 86, by + 22], fill=INK)
    d.text((M + 43, by + 11), "IN BRIEF", font=f_tag, fill=PAPER, anchor="mm")
    briefs = [
        ("Bangladesh:", "lockdown as Hasina-return unrest grows"),
        ("S. Korea:", "ex-PM's martial-law charges overturned"),
        ("Americas:", "US–Venezuela military ties restored"),
        ("Europe:", "UK–EU summit to reset Brexit ties"),
    ]
    bx = M + 100
    colw = (W - M - bx - 12) / 2
    for i, (b, t) in enumerate(briefs):
        r, c = divmod(i, 2)
        x = bx + c * (colw + 12)
        y = by + 2 + r * 24
        total = 14 + d.textlength(b + " ", font=f_briefb) + d.textlength(t, font=f_brief)
        assert total <= colw, f"brief {i} too wide: {total:.0f} > {colw:.0f}"
        d.text((x, y), "▪", font=f_briefb, fill=RED)
        d.text((x + 14, y), b, font=f_briefb, fill=INK)
        d.text((x + 14 + d.textlength(b + " ", font=f_briefb), y), t, font=f_brief, fill=INK)

    # ── footer ──
    d.line([M, 974, W - M, 974], fill=LINE, width=1)
    d.text((M, 986), "Sources: Reuters · AP · AFP · Al Jazeera · BBC · Euronews — reporting of 19 November 2026", font=f_foot, fill=GRAY)
    d.text((W - M, 986), "Events as reported that day · make.fun", font=f_foot, fill=GRAY, anchor="ra")

    out = ROOT / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
