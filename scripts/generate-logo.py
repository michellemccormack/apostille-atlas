#!/usr/bin/env python3
"""Generate Apostille Atlas Colophon Seal SVGs (Newsreader wordmark, wax-wafer counter)."""
from __future__ import annotations
import math
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

NEWSREADER = Path("/usr/share/fonts/truetype/sand-box/google/Newsreader/Newsreader-VariableFont_opsz,wght.ttf")
BRAND = "#6B2A3A"
INK = "#1B1F24"
WHITE = "#FFFFFF"

def load_font(path: Path, inst: dict | None = None) -> TTFont:
    font = TTFont(path)
    if inst and "fvar" in font:
        font = instantiateVariableFont(font, inst, overlap=True)
    return font

def font_metrics(font: TTFont, size: float) -> tuple[float, float, float]:
    upem = font["head"].unitsPerEm
    scale = size / upem
    os2 = font["OS/2"]
    cap = getattr(os2, "sCapHeight", 0) or 0
    xh = getattr(os2, "sxHeight", 0) or 0
    if cap <= 0:
        cap = font["hhea"].ascent * 0.7
    if xh <= 0:
        xh = cap * 0.52
    return cap * scale, xh * scale, scale

def text_paths(font: TTFont, text: str, size: float, x: float, y: float) -> tuple[str, float]:
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    scale = size / upem
    kern_table = None
    if "kern" in font:
        for sub in font["kern"].kernTables:
            if sub.coverage & 1:
                kern_table = sub.kernTable
                break
    parts: list[str] = []
    pen_x = 0.0
    prev = None
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            prev = None
            continue
        if prev and kern_table:
            kern = kern_table.get((prev, name), 0)
            pen_x += kern * scale
        svg_pen = SVGPathPen(glyph_set)
        tp = TransformPen(svg_pen, Transform(scale, 0, 0, -scale, x + pen_x, y))
        glyph_set[name].draw(tp)
        d = svg_pen.getCommands()
        if d:
            parts.append(d)
        pen_x += glyph_set[name].width * scale
        prev = name
    return " ".join(parts), pen_x

def path_el(d: str, fill: str) -> str:
    return f'<path fill="{fill}" d="{d}"/>'

def circle_d(cx: float, cy: float, r: float, n: int = 28) -> str:
    pts = []
    for i in range(n + 1):
        a = math.radians(-90 + i * (360 / n))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + "L".join(f"{x:.3f},{y:.3f}" for x, y in pts) + "Z"

def a_outer() -> str:
    return (
        "M16,5.4 L26.4,25.4 L22.15,25.4 L19.95,20.3 L12.05,20.3 "
        "L9.85,25.4 L5.6,25.4Z"
    )

def a_counter_wafer() -> str:
    return circle_d(16, 12.85, 2.15, n=28)

def a_counter_triangle() -> str:
    return "M16,10.6 L19.05,18.05 L12.95,18.05Z"

def seal_mark(color: str, variant: str, badge: bool = False) -> str:
    counter = a_counter_wafer() if variant == "apostille" else a_counter_triangle()
    if badge:
        return f'<path fill="{color}" fill-rule="evenodd" d="{a_outer()} {counter}"/>'
    disk = "M16,2.2 A13.8,13.8 0 1 1 15.99,2.2Z"
    d = f"{disk} {a_outer()} {counter}"
    return f'<path fill="{color}" fill-rule="evenodd" d="{d}"/>'

def header_logo() -> str:
    mark = seal_mark(BRAND, "apostille", badge=False)
    f1 = load_font(NEWSREADER, {"wght": 550, "opsz": 48})
    f2 = load_font(NEWSREADER, {"wght": 650, "opsz": 48})
    s1 = s2 = 24.0
    cap1, _, _ = font_metrics(f1, s1)
    cap2, _, _ = font_metrics(f2, s2)
    cap = max(cap1, cap2)
    baseline = 20 + cap / 2 - 0.4
    space = s1 * 0.28
    _, w1 = text_paths(f1, "Apostille", s1, 0, 0)
    _, w2 = text_paths(f2, "Atlas", s2, 0, 0)
    mark_x, mark_y, mark_size = 0, 4, 32
    gap = 9.5
    text_x = mark_x + mark_size + gap
    p1, _ = text_paths(f1, "Apostille", s1, text_x, baseline)
    p2, _ = text_paths(f2, "Atlas", s2, text_x + w1 + space, baseline)
    text = path_el(p1, BRAND) + path_el(p2, BRAND)
    width = text_x + w1 + space + w2 + 2
    body = f'<g transform="translate({mark_x},{mark_y})">{mark}</g>{text}'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.2f} 40" '
        f'width="{width:.2f}" height="40">{body}</svg>\n'
    )

def icon_svg() -> str:
    inner = seal_mark(WHITE, "apostille", badge=True)
    field = f'<rect width="32" height="32" rx="6" fill="{BRAND}"/>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
        f"{field}{inner}</svg>\n"
    )

def main() -> None:
    out = Path("/workspace/sites/apostille-atlas/public")
    out.mkdir(parents=True, exist_ok=True)
    logo = header_logo()
    (out / "logo.svg").write_text(logo)
    print("logo.svg", logo.split('viewBox="')[1].split('"')[0], "bytes", len(logo))
    icon = icon_svg()
    (out / "favicon.svg").write_text(icon)
    print("favicon.svg bytes", len(icon))
    footer_src = Path("/workspace/sites/branding/chosen/atlas-guides-footer.svg")
    (out / "atlas-guides.svg").write_text(footer_src.read_text())
    print("copied atlas-guides.svg")

if __name__ == "__main__":
    main()
