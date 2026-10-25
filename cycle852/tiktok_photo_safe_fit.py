"""Reusable no-crop image fitting for 10 TikTok genres (cycle852).

Use in review-only videos. Source image rights and model releases must be
verified separately; this module does not authorize publication.
"""
from pathlib import Path
from PIL import Image

MAX_UPSCALE = 1.12
GENRES = (
    'ai_work', 'sales_business', 'beauty', 'romance', 'saving',
    'career', 'wellness', 'science', 'travel_food',
    'product_comparison_lifestyle',
)

def contain_native(source: Image.Image, width: int, height: int):
    """Fit without cropping, and never upscale above 112% of source pixels."""
    if min(source.size) < 1 or min(width, height) < 1:
        raise ValueError('Invalid source or target dimensions')
    scale = min(width / source.width, height / source.height, MAX_UPSCALE)
    fitted = source.resize(
        (max(1, int(source.width * scale)), max(1, int(source.height * scale))),
        Image.Resampling.LANCZOS,
    )
    return fitted, scale

def validate_inputs(photos, captions, genre):
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('Unknown genre')
    if len(photos) != 8 or not all(Path(p).is_file() for p in photos):
        raise ValueError('Exactly eight photos are required')
    if len(captions) != 24:
        raise ValueError('Exactly 24 subtitle beats are required')
    previous_end = 0.0
    for beat in captions:
        start, end = float(beat['start']), float(beat['end'])
        if start < previous_end or end <= start or end > 23.04:
            raise ValueError('Invalid subtitle beat')
        previous_end = end
    return True

REVIEW_GATE = {
    'publication_approved': False,
    'employee_approved': False,
    'rights_confirmed': False,
    'automatic_posting': False,
}
