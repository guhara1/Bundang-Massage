#!/usr/bin/env python3
"""파비콘 PNG/ICO와 OG 이미지 생성 — 바로GO(B 이니셜) 브랜딩.

사용법: python3 tools/make_icons.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

NAVY = (10, 17, 32, 255)        # #0a1120
GOLD = (200, 162, 94, 255)      # #c8a25e
GOLD_SOFT = (233, 215, 171, 255)  # #e9d7ab
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def mark(size: int) -> Image.Image:
    """네이비 원 + 골드 링 + 세리프 B."""
    s = size * 4  # 슈퍼샘플링
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, s - 1, s - 1], fill=NAVY)
    ring_w = max(int(s * 0.035), 4)
    pad = int(s * 0.02)
    d.ellipse([pad, pad, s - 1 - pad, s - 1 - pad], outline=GOLD, width=ring_w)
    pad2 = int(s * 0.085)
    d.ellipse(
        [pad2, pad2, s - 1 - pad2, s - 1 - pad2],
        outline=GOLD[:3] + (90,), width=max(ring_w // 4, 2),
    )
    font = ImageFont.truetype(SERIF, int(s * 0.58))
    bbox = d.textbbox((0, 0), "B", font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((s - w) / 2 - bbox[0], (s - h) / 2 - bbox[1]), "B",
           font=font, fill=GOLD_SOFT)
    return img.resize((size, size), Image.LANCZOS)


def og_image() -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), NAVY[:3])
    d = ImageDraw.Draw(img)
    # 상단 골드 라인
    d.rectangle([0, 0, W, 6], fill=GOLD[:3])
    d.rectangle([0, H - 6, W, H], fill=GOLD[:3])
    m = mark(220)
    img.paste(m, ((W - 220) // 2, 80), m)
    f_brand = ImageFont.truetype(SERIF, 64)
    f_sub = ImageFont.truetype(SERIF, 30)
    for text, font, y, fill in [
        ("BARO GO", f_brand, 340, GOLD_SOFT[:3]),
        ("BUNDANG PREMIUM VISITING SPA", f_sub, 432, GOLD[:3]),
        ("0508-202-4719", f_brand, 492, GOLD_SOFT[:3]),
    ]:
        bbox = d.textbbox((0, 0), text, font=font)
        d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], y), text,
               font=font, fill=fill)
    img.save(os.path.join(ASSETS, "og-image.png"))


def main():
    for name, size in [
        ("favicon-16.png", 16),
        ("favicon-32.png", 32),
        ("apple-touch-icon.png", 180),
        ("icon-192.png", 192),
        ("icon-512.png", 512),
    ]:
        mark(size).save(os.path.join(ASSETS, name))
    mark(48).save(os.path.join(ROOT, "favicon.ico"),
                  sizes=[(16, 16), (32, 32), (48, 48)])
    og_image()
    print("icons + og-image generated")


if __name__ == "__main__":
    main()
