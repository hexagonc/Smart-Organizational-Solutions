#!/usr/bin/env python3
"""Generate a seamless tileable article background (math / vision / perceptron themes)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "article_tile.png"

T = 320


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    """Sparse graph grid — major lines only."""
    major = (210, 218, 235, 255)
    step = 40
    for x in range(0, T + 1, step):
        draw.line([(x, 0), (x, T)], fill=major, width=1)
    for y in range(0, T + 1, step):
        draw.line([(0, y), (T, y)], fill=major, width=1)


def draw_linear_rays(draw: ImageDraw.ImageDraw) -> None:
    """Two faint diagonal families (linear functions)."""
    for offset in range(0, T * 2, 80):
        draw.line([(offset - T, T), (offset, 0)], fill=(99, 102, 241, 32), width=1)
        draw.line([(offset, 0), (offset + T, T)], fill=(13, 110, 253, 28), width=1)


def draw_peripheral_rings(draw: ImageDraw.ImageDraw) -> None:
    """Soft rings at tile center only (peripheral vision metaphor)."""
    cx, cy = T // 2, T // 2
    for r in range(50, 130, 40):
        alpha = max(6, 22 - r // 8)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(120, 130, 160, alpha), width=1)


def draw_perceptron_halo(img: Image.Image, cx: int, cy: int) -> Image.Image:
    """Very light translucent halo — grid remains visible underneath."""
    halo = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(halo)
    hdraw.rounded_rectangle(
        (cx - 58, cy - 72, cx + 118, cy + 72),
        radius=18,
        fill=(255, 255, 255, 38),
    )
    return Image.alpha_composite(img, halo)


def draw_perceptron_network(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Centered perceptron motif — main focal point of each tile."""
    ox = cx - 42
    oy = cy
    node_stroke = (99, 102, 241, 255)
    node_fill = (219, 234, 254, 210)
    sum_fill = (13, 110, 253, 255)
    out_fill = (99, 102, 241, 255)
    edge = (13, 110, 253, 200)
    edge_hi = (99, 102, 241, 220)
    r = 7

    inputs = [(ox, oy - 36), (ox, oy - 12), (ox, oy + 12), (ox, oy + 36)]
    sx, sy = ox + 52, oy
    out_x, out_y = ox + 104, oy

    for i, (ix, iy) in enumerate(inputs):
        draw.line([(ix + r, iy), (sx - 12, sy)], fill=edge_hi if i % 2 == 0 else edge, width=2)
    draw.line([(sx + 12, sy), (out_x - r, out_y)], fill=edge_hi, width=3)

    for ix, iy in inputs:
        draw.ellipse(
            (ix - r, iy - r, ix + r, iy + r),
            fill=node_fill,
            outline=node_stroke,
            width=2,
        )
    draw.ellipse((sx - 14, sy - 14, sx + 14, sy + 14), fill=sum_fill, outline=node_stroke, width=2)
    draw.ellipse(
        (out_x - r, out_y - r, out_x + r, out_y + r),
        fill=out_fill,
        outline=node_stroke,
        width=2,
    )

    try:
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)
    except OSError:
        font_sm = ImageFont.load_default()
    draw.text((sx - 10, sy - 28), "Σ", fill=(255, 255, 255, 255), font=font_sm)


def compose_tile() -> Image.Image:
    img = Image.new("RGBA", (T, T), (245, 247, 252, 255))
    draw = ImageDraw.Draw(img)

    draw_peripheral_rings(draw)
    draw_linear_rays(draw)
    draw_grid(draw)

    # Translucent halo, then network on top
    img = draw_perceptron_halo(img, T // 2 - 28, T // 2)
    draw = ImageDraw.Draw(img)
    draw_perceptron_network(draw, T // 2 - 28, T // 2)

    return img


def main() -> None:
    tile = compose_tile()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tile.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({T}x{T}, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
