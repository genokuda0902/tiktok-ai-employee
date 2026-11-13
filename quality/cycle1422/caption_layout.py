"""Reusable caption fitting and safety checks for review-only videos."""
from PIL import Image, ImageDraw, ImageFont

def fit_caption(text, font_path, max_width=455, initial_size=24, min_size=16):
    if not text or not text.strip():
        raise ValueError("empty caption")
    canvas = ImageDraw.Draw(Image.new("RGB", (540, 960)))
    for size in range(initial_size, min_size - 1, -1):
        font = ImageFont.truetype(font_path, size)
        if canvas.textbbox((0, 0), text, font=font)[2] <= max_width:
            return size
    raise ValueError("caption too long for safe area; split it")

def publication_gate(has_japanese_voice, captions_synced, rights_approved, staff_approved):
    return all((has_japanese_voice, captions_synced, rights_approved, staff_approved))
