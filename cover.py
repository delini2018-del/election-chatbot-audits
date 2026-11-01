"""Text cover for 'Voters Will Ask AI Chatbots About Tuesday's Election. I Checked Every Test of How Often They're Wrong.'
Drawn with code (numpy + Pillow), no AI image generation. Numbers from the published audits pooled in this repo."""
import csv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

A = list(csv.DictReader(open("../data/audits.csv")))
Wp, Hp = 2880, 1620
F = "/usr/share/fonts/opentype/inter/"
fnt = lambda n, s: ImageFont.truetype(F + n, s)
ORANGE, BLUE, GREEN, GREY, ICE, YEL = (255, 140, 66), (90, 170, 255), (63, 185, 120), (200, 206, 216), (160, 220, 255), (237, 161, 0)

yy, xx = np.mgrid[0:Hp, 0:Wp] / np.array([Hp, Wp])[:, None, None]
bg = np.zeros((Hp, Wp, 3)); bg[..., 0] = 9 + 6 * xx; bg[..., 1] = 11 + 6 * xx; bg[..., 2] = 20 + 10 * xx
img = Image.fromarray(bg.clip(0, 255).astype("uint8")).convert("RGBA")
d = ImageDraw.Draw(img)

# right: one vertical strip, every audit's headline rate as a dot on a 0-100% scale
x0, top, bot = 2350, 200, 1380
d.line((x0, top, x0, bot), fill=(90, 100, 120, 255), width=4)
for v, lab in ((0, "0%"), (50, "50%"), (100, "100%")):
    y = bot - (bot - top) * v / 100
    d.line((x0 - 16, y, x0 + 16, y), fill=(90, 100, 120, 255), width=3)
    d.text((x0 - 36, y), lab, font=fnt("Inter-Medium.otf", 30), fill=GREY, anchor="rm")
col = {"voting procedures": GREEN, "local political issues": GREEN, "false news claims": ORANGE}
rng = np.random.default_rng(4)
for a in A:
    for key, hollow in (("strict_pct", False), ("broad_pct", True)):
        if a[key] and not (a["id"] == "aidp24" and hollow):
            v = float(a[key]); y = bot - (bot - top) * v / 100; x = x0 + 60 + rng.integers(0, 180)
            c = col.get(a["task"], BLUE if "facts" in a["task"] else YEL)
            r = 20
            if hollow: d.ellipse((x - r, y - r, x + r, y + r), outline=c, width=6)
            else: d.ellipse((x - r, y - r, x + r, y + r), fill=c)
d.text((x0 + 60, bot + 40), "15 audits, 2023–2026", font=fnt("Inter-Medium.otf", 30), fill=GREY)

X = 170
d.text((X, 200), "AI & ELECTIONS  ·  A REAL EXPERIMENT", font=fnt("Inter-SemiBold.otf", 40), fill=ICE)
big = fnt("InterDisplay-ExtraBold.otf", 104)
for i, line in enumerate(("Voters will ask AI", "about Tuesday's", "election.")):
    d.text((X, 270 + i * 124), line, font=big, fill="white")
d.text((X, 670), "I checked every test of how often it's wrong.", font=fnt("Inter-SemiBold.otf", 58), fill=ORANGE)
for j, (num, l1, l2, c) in enumerate((("0–90%", "error rates across", "15 published audits", ORANGE),
                                      ("1 in 4", "chance of a bad answer", "in 5 questions at 6% error", GREEN))):
    cx = X + j * 900
    d.rounded_rectangle((cx, 820, cx + 860, 980), radius=24, outline=c, width=3, fill=(18, 24, 36, 255))
    d.text((cx + 30, 846), num, font=fnt("Inter-ExtraBold.otf", 80), fill=c)
    d.text((cx + 340, 856), l1, font=fnt("Inter-Medium.otf", 32), fill="white")
    d.text((cx + 340, 898), l2, font=fnt("Inter-Medium.otf", 32), fill=GREY)
d.text((X, 1050), "US midterms  ·  3 November 2026", font=fnt("Inter-Medium.otf", 36), fill=GREY)
img.convert("RGB").save("cover_election_chatbots.png", optimize=True)
img.convert("RGB").resize((1400, 788), Image.LANCZOS).save("cover_election_chatbots_medium.png", optimize=True)
print("ok")
