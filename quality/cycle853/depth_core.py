"""Ten-genre, two-plane depth motion core; standard library only.

Review-only: the sharp foreground never exceeds 1.12x its source pixels.
The enlarged backdrop is always intentionally blurred and decorative.
"""
from __future__ import annotations

GENRE_ACCENTS = {
    'ai_work': '#36E0C4',
    'sales_business': '#FFBE70',
    'beauty': '#F0A5D1',
    'romance': '#F9A1C0',
    'saving': '#A5E0AC',
    'career': '#FFB69B',
    'wellness': '#B9E99D',
    'science': '#91D0F8',
    'travel_food': '#74DFE1',
    'product_comparison_lifestyle': '#D7B0F7',
}
MAX_SCALE = 1.12
FPS = 30
SCENE_COUNT = 8
FRAMES = 691


def fit_scale(source_width, source_height, box_width=800, box_height=740):
    if min(source_width, source_height, box_width, box_height) <= 0:
        raise ValueError('positive image dimensions required')
    return min(box_width/source_width, box_height/source_height, MAX_SCALE)


def scene_frames(index):
    if not 0 <= index < SCENE_COUNT:
        raise ValueError('scene index out of range')
    return 96 if index == 7 else 94


def scene_filter(index):
    """FFmpeg graph: blurred background and sharp photo move at distinct rates."""
    scene_frames(index)
    return (
        f'[0:v]format=yuv420p,crop=1080:1920:'
        f'x=60+16*sin(n/17+{index}):y=90+12*cos(n/21+{index})[bg];'
        f'[bg][1:v]overlay=x=80+23*sin(n/19+{index}):'
        f'y=434+12*cos(n/23+{index}):eval=frame[t];'
        f'[t][2:v]overlay=0:0:format=auto,format=yuv420p[v]'
    )


def check_segments(frame_counts):
    expected = [scene_frames(i) for i in range(SCENE_COUNT)]
    if list(frame_counts) != expected:
        raise ValueError(f'truncated or invalid segments: {frame_counts} != {expected}')
    return True
