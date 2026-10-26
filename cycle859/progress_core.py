"""Cycle859: noninteractive, ten-genre, voice-duration-aware watch progress indicator.

This does not infer attention or predict retention; it provides an unambiguous
remaining-length cue without moving protected captions or photo content.
"""
from dataclasses import dataclass

FPS = 30
FRAMES = 691
BAR_X = 60
BAR_Y = 156
BAR_WIDTH = 960
BAR_HEIGHT = 12
PALETTES = {
    'ai_work': '#54F0D4',
    'sales_business': '#FFBD71',
    'beauty': '#F4A6D3',
    'romance': '#F9A3C0',
    'saving': '#A4E6B0',
    'career': '#FFB49B',
    'wellness': '#B9E99D',
    'science': '#91D0F8',
    'travel_food': '#74DFE1',
    'product_comparison_lifestyle': '#D7B0F7',
}


def progress_pixels(frame_index, total_frames=FRAMES, width=BAR_WIDTH):
    """Monotone progress, inclusive endpoints, never outside the bar."""
    if total_frames < 2 or width <= 0:
        raise ValueError('invalid geometry')
    if not 0 <= frame_index < total_frames:
        raise ValueError('frame index out of range')
    return round(width * frame_index / (total_frames - 1))


def color_for_genre(genre):
    if genre not in PALETTES:
        raise ValueError('unknown genre')
    return PALETTES[genre]


def bar_geometry():
    return BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT


def validate_placement():
    x, y, w, h = bar_geometry()
    return x >= 48 and x + w <= 1032 and 140 <= y <= 180 and y + h < 192
