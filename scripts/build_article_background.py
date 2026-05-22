#!/usr/bin/env python3
"""Build article background from public-domain Mark I Perceptron (Wikimedia Commons)."""

from __future__ import annotations

import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "article_background.png"
PERCEPTRON_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/1/13/"
    "Mark_I_Perceptron%2C_Figure_2_of_operator%27s_manual.png"
)

W, H = 1920, 1080


def make_gradient_base() -> Image.Image:
    img = Image.new("RGB", (W, H), "#2a3142")
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(42 + (30 - 42) * t)
        g = int(49 + (35 - 49) * t)
        b = int(66 + (50 - 66) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    # Glow only on outer edges, not over diagram area
    gdraw.ellipse((-120, 120, 520, 960), fill=(99, 102, 241, 40))
    gdraw.ellipse((1480, 200, 2100, 900), fill=(13, 110, 253, 30))
    return Image.alpha_composite(img.convert("RGBA"), glow)


def load_perceptron_photo() -> Image.Image:
    req = urllib.request.Request(
        PERCEPTRON_URL,
        headers={"User-Agent": "SOS-Website/1.0 (educational; contact: local-dev)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()

    photo = Image.open(BytesIO(data)).convert("RGBA")
    photo = ImageEnhance.Contrast(photo).enhance(1.08)
    # Smaller so cover/contain does not crop to a single rack panel
    target_h = int(H * 0.42)
    scale = target_h / photo.height
    target_w = int(photo.width * scale)
    return photo.resize((target_w, target_h), Image.Resampling.LANCZOS)


def draw_photo_card(photo: Image.Image) -> Image.Image:
    pad = 28
    card_w = photo.width + pad * 2
    card_h = photo.height + pad * 2
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle((0, 0, card_w, card_h), radius=20, fill=(255, 255, 255, 245))
    card.paste(photo, (pad, pad), photo)
    return card


def draw_diagram_panel() -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Frosted panel behind diagram (high contrast)
    panel_x1, panel_y1 = int(W * 0.52), int(H * 0.12)
    panel_x2, panel_y2 = int(W * 0.96), int(H * 0.88)
    draw.rounded_rectangle(
        (panel_x1, panel_y1, panel_x2, panel_y2),
        radius=24,
        fill=(255, 255, 255, 210),
    )

    cx = int(W * 0.72)
    cy = H // 2
    input_x = cx - 200
    output_x = cx + 200
    sum_x = cx - 20
    node_r = 22
    input_ys = [cy - 140, cy - 70, cy, cy + 70, cy + 140]

    edge = (13, 110, 253, 255)
    edge_hi = (99, 102, 241, 255)
    node_fill = (13, 110, 253, 255)
    node_stroke = (255, 255, 255, 255)
    text_color = (26, 29, 41, 255)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
        font_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font
        font_lg = font

    for i, iy in enumerate(input_ys):
        draw.line(
            [(input_x + node_r, iy), (sum_x - 32, cy)],
            fill=edge_hi if i % 2 == 0 else edge,
            width=4,
        )

    draw.line([(sum_x + 32, cy), (output_x - node_r, cy)], fill=edge_hi, width=5)

    for iy in input_ys:
        draw.ellipse(
            (input_x - node_r, iy - node_r, input_x + node_r, iy + node_r),
            fill=(219, 234, 254, 255),
            outline=edge,
            width=3,
        )

    draw.ellipse(
        (sum_x - 36, cy - 36, sum_x + 36, cy + 36),
        fill=node_fill,
        outline=node_stroke,
        width=3,
    )
    draw.ellipse(
        (output_x - node_r, cy - node_r, output_x + node_r, cy + node_r),
        fill=(99, 102, 241, 255),
        outline=node_stroke,
        width=3,
    )

    draw.text((input_x - 58, cy - 200), "Inputs", fill=text_color, font=font)
    draw.text((sum_x - 14, cy - 58), "Σ", fill=(255, 255, 255, 255), font=font_lg)
    draw.text((output_x - 36, cy - 58), "Output", fill=text_color, font=font_sm)
    for i, iy in enumerate(input_ys):
        draw.text((input_x - 14, iy - 9), f"x{i + 1}", fill=text_color, font=font_sm)

    ax, ay = output_x + 95, cy - 50
    draw.rounded_rectangle((ax, ay, ax + 88, ay + 100), radius=8, fill=(248, 249, 250, 255), outline=edge, width=2)
    draw.line(
        [(ax + 12, ay + 78), (ax + 40, ay + 78), (ax + 40, ay + 28), (ax + 76, ay + 28)],
        fill=edge,
        width=3,
    )
    draw.text((ax + 10, ay + 82), "f", fill=text_color, font=font_sm)

    draw.text(
        (panel_x1 + 24, panel_y2 - 36),
        "Perceptron: inputs → weighted sum → activation → output",
        fill=(80, 86, 110, 255),
        font=font_sm,
    )

    return layer


def draw_center_calm_zone() -> Image.Image:
    """Soft center so the area behind the article panel is not busy."""
    zone = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    zdraw = ImageDraw.Draw(zone)
    cx = W // 2
    zdraw.ellipse((cx - 520, 40, cx + 520, H - 40), fill=(236, 238, 245, 120))
    return zone


def compose() -> None:
    base = make_gradient_base()
    photo_card = draw_photo_card(load_perceptron_photo())

    px = int(W * 0.06)
    py = (H - photo_card.height) // 2
    base.paste(photo_card, (px, py), photo_card)

    base = Image.alpha_composite(base, draw_center_calm_zone())
    base = Image.alpha_composite(base, draw_diagram_panel())

    caption = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(caption)
    try:
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
    except OSError:
        font_sm = ImageFont.load_default()
    cdraw.text(
        (W // 2 - 280, H - 40),
        "Mark I Perceptron (public domain, U.S. federal work) · Rosenblatt, 1960",
        fill=(120, 128, 150, 220),
        font=font_sm,
    )
    base = Image.alpha_composite(base, caption)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    compose()
