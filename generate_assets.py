from PIL import Image, ImageDraw, ImageFont
import math

def avatar(path, initials, bg=(99, 102, 241), fg=(255, 255, 255), size=300):
    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", size // 3)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), initials, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), initials, fill=fg, font=font)
    img.save(path)

def gradient_banner(path, size=(1200, 260), start=(99, 102, 241), end=(236, 72, 153)):
    w, h = size
    img = Image.new("RGB", size, start)
    draw = ImageDraw.Draw(img)
    for x in range(w):
        t = x / w
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))
    for cx, cy, r, alpha in [(200, 60, 70, 40), (950, 180, 90, 30), (600, 40, 50, 25)]:
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        odraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, alpha))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(path)

def icon_badge(path, emoji_text, bg, size=200):
    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=40, outline=(255, 255, 255), width=6)
    try:
        font = ImageFont.truetype("seguiemj.ttf", size // 2)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), emoji_text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), emoji_text, font=font, embedded_color=True)
    img.save(path)

avatar("assets/avatar.png", "HK")
gradient_banner("assets/banner.png")
icon_badge("assets/badge_code.png", "💻", (79, 70, 229))
icon_badge("assets/badge_idea.png", "💡", (219, 39, 119))
icon_badge("assets/badge_rocket.png", "🚀", (13, 148, 136))

print("done")
