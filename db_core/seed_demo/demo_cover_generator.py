"""
Генерация PNG-обложек для демо-произведений (seed_demo).

Стиль ближе к современному минималистичному: радиально-плавный фон
(набор фиксированных палитр), блок текста сверху слева: автор жирным sans,
название тонким sans, CAPS.

Кадр 300×430 (см. ``WORK_DEMO_COVER_FILENAME`` / ``work_demo_preview_relative_path`` в ``data.py``).
"""

from __future__ import annotations

import colorsys
import math
import os
import uuid
from io import BytesIO
from typing import NamedTuple

from PIL import Image, ImageDraw, ImageFont

from db_core.seed_demo import data as seed_data

_COVER_SIZE = (300, 430)


class _RadialPalette(NamedTuple):
    """Пара ``colorsys.hls_to_rgb(h, l, s)`` для светлого «пятна» и для края."""

    hue: float
    l_center: float
    s_center: float
    l_edge: float
    s_edge: float


# Порядок: голубой, синий, светло-коричневый, светло-зелёный, тёмно-зелёный, серый, светло-оранжевый.
_RADIAL_PALETTES: tuple[_RadialPalette, ...] = (
    _RadialPalette(0.52, 0.58, 0.30, 0.26, 0.38),
    _RadialPalette(0.58, 0.50, 0.42, 0.22, 0.54),
    _RadialPalette(0.076, 0.72, 0.22, 0.42, 0.26),
    _RadialPalette(0.32, 0.64, 0.34, 0.30, 0.42),
    _RadialPalette(0.30, 0.40, 0.42, 0.15, 0.52),
    _RadialPalette(0.0, 0.57, 0.04, 0.26, 0.07),
    _RadialPalette(0.087, 0.70, 0.42, 0.34, 0.52),
)

_FONT_AUTHOR_BOLD: tuple[str, ...] = (
    "/usr/share/fonts/opentype/noto/NotoSansCondensed-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\SegoeUI-Bold.ttf",
)

_FONT_TITLE_LIGHT: tuple[str, ...] = (
    "/usr/share/fonts/opentype/noto/NotoSansCondensed-Thin.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCondensed-ExtraLight.ttf",
    "/usr/share/fonts/opentype/noto/NotoSans-Thin.ttf",
    "/usr/share/fonts/opentype/noto/NotoSans-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Light.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf",
    "/System/Library/Fonts/Supplemental/NotoSans-ExtraLight.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/NotoSans-Light.ttf",
    r"C:\Windows\Fonts\SegoeUI-Light.ttf",
    r"C:\Windows\Fonts\arialnarrow.ttf",
)

_FONT_TITLE_FALLBACK: tuple[str, ...] = (
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
)


def _load_font(candidates: tuple[str, ...], size: int) -> ImageFont.ImageFont | None:
    size = max(8, size)
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                continue
    return None


def _palette_for_work(work_id: str) -> _RadialPalette:
    """Стабильный выбор палитры по uuid произведения."""
    idx = uuid.UUID(work_id).int % len(_RADIAL_PALETTES)
    return _RADIAL_PALETTES[idx]


def _radial_background(size: tuple[int, int], work_id: str) -> Image.Image:
    wf = max(120, size[0] // 2)
    hf = max(172, size[1] // 2)
    img = Image.new("RGB", (wf, hf))
    px = img.load()
    cx, cy = wf // 2, int(hf * 0.1)
    pal = _palette_for_work(work_id)
    h = pal.hue % 1.0
    bright = colorsys.hls_to_rgb(h, pal.l_center, pal.s_center)
    dim = colorsys.hls_to_rgb(h, pal.l_edge, pal.s_edge)
    br = tuple(int(round(x * 255)) for x in bright)
    dr = tuple(int(round(x * 255)) for x in dim)
    max_d = math.hypot(wf * 0.55, hf * 0.95)

    for yy in range(hf):
        for xx in range(wf):
            d = math.hypot(xx - cx, yy - cy) / max_d
            d = max(0.0, min(1.05, d * 1.1))
            t = d * d
            r = int(br[0] * (1 - t) + dr[0] * t)
            g = int(br[1] * (1 - t) + dr[1] * t)
            b = int(br[2] * (1 - t) + dr[2] * t)
            px[xx, yy] = (r, g, b)

    out = img.resize(size, Image.Resampling.LANCZOS)
    return out


def _wrap_lines(title: str, font: ImageFont.ImageFont, draw: ImageDraw.ImageDraw, max_width: int) -> list[str]:
    words = title.replace("\n", " ").split()
    if not words:
        return [""]
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textlength(trial, font=font) <= max_width:
            current.append(word)
            continue
        if current:
            lines.append(" ".join(current))
            current = []
        if draw.textlength(word, font=font) <= max_width:
            current.append(word)
            continue
        chunk = ""
        for ch in word:
            t2 = chunk + ch
            if not chunk and draw.textlength(ch, font=font) > max_width:
                lines.append(ch)
                continue
            if draw.textlength(t2, font=font) <= max_width:
                chunk = t2
            else:
                if chunk:
                    lines.append(chunk)
                chunk = ch
        if chunk:
            current.append(chunk)
    if current:
        lines.append(" ".join(current))
    return lines or [title]


def _draw_left_aligned_block(
    draw: ImageDraw.ImageDraw,
    margin_x: int,
    y: int,
    lines: list[str],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
) -> int:
    """Рисует строки слева, возвращает y под последней строкой."""
    fz = getattr(font, "size", 16)
    line_gap = max(4, fz // 14)
    for line in lines:
        draw.text((margin_x, y), line, font=font, fill=fill, anchor="lt")
        bbox = draw.textbbox((margin_x, y), line, font=font, anchor="lt")
        y = bbox[3] + line_gap
    return y


def _render_cover_png(size: tuple[int, int], title: str, author: str, work_id: str) -> bytes:
    w, h = size
    img = _radial_background(size, work_id)
    draw = ImageDraw.Draw(img)

    margin_x = max(14, round(w * 0.068))
    top_y = max(14, round(h * 0.052))
    max_text_w = max(56, w - margin_x - 12)

    font_author_px = max(22, min(32, round(h * 0.064)))
    font_title_px = max(17, min(26, round(h * 0.052)))

    font_author = _load_font(_FONT_AUTHOR_BOLD, font_author_px) or ImageFont.load_default()
    font_title = _load_font(_FONT_TITLE_LIGHT, font_title_px)
    if font_title is None:
        font_title = _load_font(_FONT_TITLE_FALLBACK, max(font_title_px - 2, 14)) or ImageFont.load_default()

    white = (255, 255, 255)

    blocks_gap = round(h * 0.028)
    cursor_y = float(top_y)

    author_uc = author.strip().upper() if author else ""
    title_uc = title.strip().upper()

    if author_uc:
        author_lines = _wrap_lines(author_uc, font_author, draw, max_text_w)
        cursor_y = _draw_left_aligned_block(draw, margin_x, int(cursor_y), author_lines, font_author, white)
        cursor_y += blocks_gap * 2

    title_lines = _wrap_lines(title_uc, font_title, draw, max_text_w)
    _draw_left_aligned_block(draw, margin_x, int(cursor_y), title_lines, font_title, white)

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def build_demo_cover_png_for_work(work_id: str, title: str, author: str = "") -> bytes:
    return _render_cover_png(_COVER_SIZE, title, author, work_id)


def demo_work_specs() -> list[tuple[str, str, str]]:
    """Тройки ``(work_id, title, главный автор)`` из seed."""
    authors = {a.id: a.name for a in seed_data.AUTHORS}
    out: list[tuple[str, str, str]] = []
    for w in seed_data.WORKS:
        primary_author = ""
        if w.author_ids:
            primary_author = authors.get(w.author_ids[0], "")
        out.append((w.id, w.title, primary_author))
    return out
