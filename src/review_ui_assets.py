"""Deterministic, rights-safe UI mockups for review renders.

Creates abstract workflow/dashboard frames without logos, customer data, screenshots,
or external assets. These are review fixtures, not representations of a real product.
"""
import struct
import zlib
from pathlib import Path

WIDTH = 1080
HEIGHT = 1920


def _rect(buf, x0, y0, x1, y1, rgb):
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(WIDTH, x1), min(HEIGHT, y1)
    for y in range(y0, y1):
        row = y * WIDTH * 3
        for x in range(x0, x1):
            p = row + x * 3
            buf[p:p + 3] = bytes(rgb)


def _png_bytes(rgb):
    raw = b''.join(b'\x00' + rgb[y * WIDTH * 3:(y + 1) * WIDTH * 3] for y in range(HEIGHT))
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', struct.pack('>IIBBBBB', WIDTH, HEIGHT, 8, 2, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))


def make_sanitized_ui_frame(path, variant=0):
    """Create an abstract portrait UI frame with enough structure for motion review."""
    palettes = [
        ((15, 23, 42), (30, 41, 59), (71, 85, 105), (226, 232, 240)),
        ((17, 24, 39), (31, 41, 55), (75, 85, 99), (229, 231, 235)),
        ((24, 24, 27), (39, 39, 42), (82, 82, 91), (244, 244, 245)),
        ((12, 32, 45), (22, 48, 65), (69, 92, 110), (226, 232, 240)),
        ((28, 25, 23), (41, 37, 36), (87, 83, 78), (245, 245, 244)),
    ]
    bg, panel, muted, bright = palettes[variant % len(palettes)]
    buf = bytearray(bytes(bg) * WIDTH * HEIGHT)
    # Browser/app chrome and navigation.
    _rect(buf, 60, 110, 1020, 1810, panel)
    _rect(buf, 60, 110, 1020, 220, muted)
    _rect(buf, 100, 145, 130, 175, bright)
    _rect(buf, 150, 145, 180, 175, bright)
    _rect(buf, 200, 145, 230, 175, bright)
    _rect(buf, 95, 270, 280, 1720, bg)
    # Main content cards / rows.
    for i in range(5):
        y = 285 + i * 250
        _rect(buf, 320, y, 950, y + 190, muted)
        _rect(buf, 350, y + 35, 650 + ((i + variant) % 3) * 80, y + 65, bright)
        _rect(buf, 350, y + 95, 860, y + 118, panel)
        _rect(buf, 350, y + 135, 760, y + 158, panel)
    # Variant-specific chart/table emphasis, creating visible scene-to-scene change.
    for i in range(6):
        h = 45 + ((i * 37 + variant * 53) % 150)
        _rect(buf, 360 + i * 90, 1620 - h, 415 + i * 90, 1620, bright)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(_png_bytes(buf))
    return out
