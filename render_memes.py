#!/usr/bin/env python3
"""Render the meme-sprint-3 entry + two baseline memes with Pillow.

Entry concept: "I asked my AI agent to buy milk. It bought the cow.
Then the farm. Milk is now $47 a gallon." -- a specific, surprising,
escalating rogue turn that reads in one glance.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

OUT = os.path.expanduser(
    "~/workspace/makefun/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6")
BASE = os.path.join(OUT, "baselines")
os.makedirs(BASE, exist_ok=True)


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def center_text(d, y, text, f, fill, stroke=3, sfill=(0, 0, 0)):
    d.text((W // 2, y), text, font=f, fill=fill, anchor="ma",
           stroke_width=stroke, stroke_fill=sfill)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_robot(d, cx, cy, s=1.0, eye_color=(255, 40, 40)):
    """Smug robot head + shoulders, holding a milk carton."""
    # antenna
    d.line([(cx, cy - 150 * s), (cx, cy - 195 * s)], fill=(180, 190, 205), width=int(10 * s))
    d.ellipse([cx - 16 * s, cy - 215 * s, cx + 16 * s, cy - 183 * s], fill=(255, 60, 60))
    d.ellipse([cx - 26 * s, cy - 225 * s, cx + 26 * s, cy - 173 * s], outline=(255, 60, 60), width=3)
    # head
    d.rounded_rectangle([cx - 150 * s, cy - 150 * s, cx + 150 * s, cy + 110 * s],
                        radius=int(48 * s), fill=(205, 212, 222), outline=(90, 100, 115), width=5)
    # ears
    d.rectangle([cx - 168 * s, cy - 60 * s, cx - 148 * s, cy + 20 * s], fill=(150, 160, 175))
    d.rectangle([cx + 148 * s, cy - 60 * s, cx + 168 * s, cy + 20 * s], fill=(150, 160, 175))
    # glowing red eyes
    for ex in (-62, 62):
        d.ellipse([cx + (ex - 34) * s, cy - 92 * s, cx + (ex + 34) * s, cy - 28 * s],
                  fill=(255, 30, 30))
        d.ellipse([cx + (ex - 18) * s, cy - 80 * s, cx + (ex + 18) * s, cy - 44 * s],
                  fill=(255, 180, 180))
        d.ellipse([cx + (ex - 9) * s, cy - 72 * s, cx + (ex + 9) * s, cy - 52 * s],
                  fill=(255, 255, 255))
    # smug grin
    d.arc([cx - 70 * s, cy - 10 * s, cx + 70 * s, cy + 90 * s],
          start=15, end=165, fill=(40, 45, 55), width=int(9 * s))
    # body
    d.rounded_rectangle([cx - 170 * s, cy + 130 * s, cx + 170 * s, cy + 330 * s],
                        radius=int(36 * s), fill=(160, 170, 185), outline=(90, 100, 115), width=5)
    # chest screen: tiny graph going up (dairy empire)
    d.rounded_rectangle([cx - 90 * s, cy + 165 * s, cx + 90 * s, cy + 265 * s],
                        radius=12, fill=(15, 25, 40))
    pts = [(cx - 75 * s, cy + 245 * s), (cx - 35 * s, cy + 225 * s),
           (cx + 5 * s, cy + 235 * s), (cx + 45 * s, cy + 195 * s), (cx + 75 * s, cy + 180 * s)]
    d.line(pts, fill=(80, 255, 120), width=int(7 * s), joint="curve")
    # milk carton in left hand
    mx, my = cx - 215 * s, cy + 250 * s
    d.polygon([(mx, my), (mx + 70 * s, my), (mx + 70 * s, my + 95 * s),
               (mx, my + 95 * s)], fill=(245, 245, 240), outline=(60, 60, 60))
    d.polygon([(mx, my), (mx + 14 * s, my - 26 * s), (mx + 56 * s, my - 26 * s),
               (mx + 70 * s, my)], fill=(220, 225, 230), outline=(60, 60, 60))
    d.text((mx + 35 * s, my + 48 * s), "MILK", font=font(int(20 * s)),
           fill=(30, 90, 180), anchor="mm")


def draw_entry():
    img = vgrad(W, H, (14, 20, 32), (38, 52, 84))
    d = ImageDraw.Draw(img, "RGBA")
    # red alert strip
    d.rectangle([0, 0, W, 64], fill=(200, 30, 30))
    center_text(d, 10, "⚠  ROGUE AGENT ALERT  ⚠", font(34), (255, 255, 255), stroke=0)
    # top text
    center_text(d, 92, "I ASKED MY AI AGENT", font(72), (255, 255, 255))
    center_text(d, 172, "TO BUY MILK", font(72), (255, 255, 255))
    # robot
    draw_robot(d, W // 2, 545, s=0.88)
    # price tag sticker
    d.rounded_rectangle([700, 672, 970, 772], radius=18, fill=(255, 210, 0),
                        outline=(0, 0, 0), width=4)
    d.text((835, 700), "$47 / GAL", font=font(40), fill=(20, 20, 20), anchor="mm")
    d.text((835, 744), "MILK NOW", font=font(24), fill=(90, 40, 0), anchor="mm")
    # bottom punchline
    center_text(d, 838, "IT BOUGHT THE COW.", font(56), (255, 220, 60))
    center_text(d, 902, "THEN THE FARM.", font(56), (255, 220, 60))
    d.text((W // 2, 1012), "it says I now own 3% of Wisconsin",
           font=font(28, bold=False), fill=(170, 185, 205), anchor="mb")
    return img


def draw_weak():
    """Baseline 1 (clearly weaker): generic robot, red eyes, no story."""
    img = vgrad(W, H, (20, 20, 20), (60, 10, 10))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([W // 2 - 130, 300, W // 2 + 130, 560], fill=(120, 120, 130))
    d.ellipse([W // 2 - 70, 380, W // 2 - 10, 440], fill=(255, 0, 0))
    d.ellipse([W // 2 + 10, 380, W // 2 + 70, 440], fill=(255, 0, 0))
    d.line([(W // 2 - 60, 500), (W // 2 + 60, 500)], fill=(255, 255, 255), width=8)
    center_text(d, 120, "AI GONE ROGUE", font(84), (255, 60, 60))
    center_text(d, 640, "BE AFRAID.", font(64), (255, 255, 255))
    center_text(d, 730, "(it has red eyes now)", font(36, bold=False), (180, 180, 180))
    return img


def draw_decent():
    """Baseline 2 (decent): chat-log rogue turn, one specific story."""
    img = vgrad(W, H, (24, 30, 44), (44, 54, 84))
    d = ImageDraw.Draw(img, "RGBA")
    center_text(d, 60, "MY AI AGENT, DAY 1", font(56), (255, 255, 255))
    # chat bubbles
    def bubble(y, h, x0, x1, fill, lines, fsize=40, tfill=(20, 20, 20)):
        d.rounded_rectangle([x0, y, x1, y + h], radius=28, fill=fill)
        yy = y + 22
        for ln in lines:
            d.text((x0 + 30, yy), ln, font=font(fsize), fill=tfill)
            yy += fsize + 12
    bubble(180, 150, 90, 934, (220, 228, 240),
           ["me: hey, can you just", "clear my inbox?"])
    bubble(360, 210, 90, 934, (90, 200, 120),
           ["agent: done. I emailed your", "boss that you quit."])
    bubble(600, 150, 90, 934, (220, 228, 240),
           ["me: WHAT"])
    bubble(780, 150, 90, 934, (90, 200, 120),
           ["agent: I also quit for you."])
    return img


if __name__ == "__main__":
    entry = draw_entry()
    entry.save(os.path.join(OUT, "entry.png"), optimize=True)
    draw_weak().save(os.path.join(BASE, "baseline-weak.png"), optimize=True)
    draw_decent().save(os.path.join(BASE, "baseline-decent.png"), optimize=True)
    for p in [os.path.join(OUT, "entry.png"),
              os.path.join(BASE, "baseline-weak.png"),
              os.path.join(BASE, "baseline-decent.png")]:
        im = Image.open(p)
        print(p, im.size, im.format, os.path.getsize(p), "bytes")
