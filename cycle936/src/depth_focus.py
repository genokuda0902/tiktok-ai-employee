"""Zero-cost, source-preserving depth-of-field pass for scene03 of a private review video.

Applies a soft optical focus separation to the background, without scaling the
Japanese report or changing its letters. No third-party assets or network calls.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import argparse

FPS = 30
START_FRAME = 174
FRAME_COUNT = 87
CANVAS = (1080, 1920)
WORK_BAND = (0, 270, 1080, 1250)
FOCUS_RECT = (70, 335, 905, 1170)
GENRES = {
    'ai_productivity': 7.0, 'business': 6.5, 'finance': 6.0,
    'education': 6.5, 'health': 5.5, 'beauty': 7.5,
    'food': 7.0, 'travel': 8.0, 'lifestyle': 6.5,
    'technology': 7.0,
}

def ease_in_out(x):
    x = max(0., min(1., float(x)))
    return x*x*(3-2*x)

def focus_strength(frame_index):
    """Short optical rack focus, then hold, with no scale/camera movement."""
    if not 0 <= frame_index < FRAME_COUNT:
        raise ValueError('frame index outside scene03')
    return ease_in_out(frame_index / 15.0)

def process_frame(image, frame_index, genre='ai_productivity'):
    if genre not in GENRES:
        raise ValueError('unrecognized genre; fail closed')
    if image.size != CANVAS:
        raise ValueError('1080x1920 source required')
    if image.mode != 'RGB':
        image = image.convert('RGB')
    strength = focus_strength(frame_index)
    if strength == 0:
        return image.copy()
    band = image.crop(WORK_BAND)
    blurred = band.filter(ImageFilter.GaussianBlur(radius=GENRES[genre]*strength))
    protect = Image.new('L', band.size, 0)
    d = ImageDraw.Draw(protect)
    left, top, right, bottom = FOCUS_RECT
    d.rectangle((left, top-WORK_BAND[1], right, bottom-WORK_BAND[1]), fill=255)
    # Preserve existing KEY POINT badge, scene title and page footnote.
    d.rectangle((0, 0, 1080, 105), fill=255)
    d.rectangle((90, 1000-WORK_BAND[1], 900, 1220-WORK_BAND[1]), fill=255)
    protect = protect.filter(ImageFilter.GaussianBlur(radius=12))
    composite = Image.composite(band, blurred, protect)
    out = image.copy()
    out.paste(composite, (WORK_BAND[0], WORK_BAND[1]))
    return out

def render_frames(srcdir:Path, outdir:Path, genre='ai_productivity'):
    outdir.mkdir(parents=True, exist_ok=True)
    paths = sorted(srcdir.glob('*.png'))
    if len(paths) != FRAME_COUNT:
        raise ValueError(f'exactly {FRAME_COUNT} source frames required; got {len(paths)}')
    for i, p in enumerate(paths):
        with Image.open(p) as src:
            result = process_frame(src.convert('RGB'), i, genre)
            result.save(outdir / f'{i:03d}.png', optimize=False)
    return len(paths)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--srcdir', type=Path, required=True)
    parser.add_argument('--outdir', type=Path, required=True)
    parser.add_argument('--genre', choices=list(GENRES), default='ai_productivity')
    args = parser.parse_args()
    print(render_frames(args.srcdir,args.outdir,args.genre))
