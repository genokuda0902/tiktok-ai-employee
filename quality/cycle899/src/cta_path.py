"""cycle899 review-only 3-step action-path overlay (no private assets)."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

WIDTH, HEIGHT, FPS = 1080, 1920, 30
START_SEC = 20.37
FRAME_COUNT = 80
POINTS = ((165, 758), (165, 902), (165, 1050))
RAIL_X = 106
CAPTION_TOP = 1450
GENRES = ('ai_productivity','business','study','cooking','travel','beauty','health','finance','pets','hobbies')
POLICY = {'publication_approved': False, 'automatic_posting': False, 'external_upload': False, 'paid_service': False, 'human_review_required': True}

@dataclass(frozen=True)
class FrameState:
    progress: float
    active_index: int
    highlight_alpha: tuple[int, int, int]
    rail_end_y: int

def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))

def smoothstep(x: float) -> float:
    x = clamp(x)
    return x*x*(3-2*x)

def state_at(frame: int) -> FrameState:
    if not 0 <= frame < FRAME_COUNT:
        raise ValueError('frame out of range')
    p = (frame + 1) / FRAME_COUNT
    segment = min(2, int(p * 3))
    alpha = []
    for i in range(3):
        arrive = i / 3
        strength = smoothstep((p - arrive) * 7.5)
        pulse = max(0.0, 1.0 - abs((p - arrive) * 6 - 0.65))
        alpha.append(int(100 * strength + 90 * pulse))
    y0, y1 = POINTS[0][1], POINTS[-1][1]
    return FrameState(p, segment, tuple(min(220, v) for v in alpha), int(y0 + (y1-y0) * smoothstep(p)))

def overlay_bounds() -> tuple[int,int,int,int]:
    return (80, 680, 230, 1140)

def render_overlay(frame: int, output: Path) -> None:
    from PIL import Image, ImageDraw, ImageFilter
    s = state_at(frame)
    canvas = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    glow = Image.new('RGBA', (220, 480), (0,0,0,0))
    g = ImageDraw.Draw(glow)
    for i, (cx,cy) in enumerate(POINTS):
        a = min(110, s.highlight_alpha[i] // 2)
        if a:
            xx, yy = cx - 75, cy - 680
            g.ellipse((xx-52, yy-52, xx+52, yy+52), outline=(26,228,205,a), width=12)
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(11)), (80,680))
    d = ImageDraw.Draw(canvas, 'RGBA')
    d.line((RAIL_X, POINTS[0][1], RAIL_X, POINTS[-1][1]), fill=(32,145,163,60), width=6)
    d.line((RAIL_X, POINTS[0][1], RAIL_X, s.rail_end_y), fill=(37,229,209,160), width=7)
    d.ellipse((RAIL_X-9, s.rail_end_y-9, RAIL_X+9, s.rail_end_y+9), fill=(230,255,252,230))
    for i,(cx,cy) in enumerate(POINTS):
        a = s.highlight_alpha[i]
        if a > 0:
            d.ellipse((cx-48,cy-48,cx+48,cy+48), outline=(45,237,212,a), width=5)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)

def render_all(directory: Path) -> None:
    for i in range(FRAME_COUNT):
        render_overlay(i, directory / f'{i:04d}.png')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('directory', type=Path)
    args = p.parse_args()
    render_all(args.directory)
