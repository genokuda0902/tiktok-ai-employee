"""cycle836: reusable, photo-first 9:16 slide layout. Human review only.

Synthetic or properly licensed photographs only. No upload or publication.
This layout is the shared component of the local cycle836 video renderer.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

WIDTH, HEIGHT = 1080, 1920
FRAMES = (101, 93, 91, 99, 98, 101, 89, 103)
PALETTES = {
    "ai_work": "#43F1DC", "sales_business": "#FFC16E",
    "beauty": "#FF9CC4", "romance": "#F9B6DD",
    "saving": "#F5D76E", "career": "#8FB5FF",
    "wellness": "#9CE2B0", "science": "#FFA980",
    "travel_food": "#C7A3FF", "productivity": "#75DCEB",
}

def cover(image, size, focal_x=0.5):
    """Fill target frame by cropping, never stretching the photo."""
    width, height = size
    ratio = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * ratio),
                            round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = max(0, min(resized.width - width,
                      round((resized.width - width) * focal_x)))
    top = max(0, min(resized.height - height,
                     round((resized.height - height) * 0.43)))
    return resized.crop((left, top, left + width, top + height))

def slide(photo, headline, subheadline, index, genre="ai_work", font_path=None):
    """Render a photo-first slide with reserved bottom Japanese subtitle space."""
    if genre not in PALETTES:
        raise ValueError("Unknown genre")
    if not 0 <= index < 8:
        raise ValueError("Slide index must be 0..7")
    photo = photo.convert("RGB")
    bg = ImageEnhance.Brightness(
        cover(photo, (WIDTH, HEIGHT)).filter(ImageFilter.GaussianBlur(28))
    ).enhance(0.46)
    fg = ImageEnhance.Contrast(cover(photo, (WIDTH, 1500))).enhance(1.08)
    bg.paste(fg, (0, 0))
    mask = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pix = mask.load()
    for y in range(HEIGHT):
        if y < 450:
            alpha = round(205 * (1 - y / 480) ** .75)
        elif y < 930:
            alpha = 0
        else:
            alpha = round(246 * min(1, (y - 930) / 580) ** 1.3)
        for x in range(WIDTH):
            pix[x, y] = (3, 13, 20, alpha)
    result = Image.alpha_composite(bg.convert("RGBA"), mask)
    if font_path is None:
        return result.convert("RGB")  # useful for layout-only testing
    bold = lambda size: ImageFont.truetype(str(font_path), size)
    draw = ImageDraw.Draw(result)
    accent = PALETTES[genre]
    draw.rounded_rectangle((46, 55, 345, 119), radius=26, fill="#0C2733")
    draw.text((68, 63), "AI × WORK", font=bold(35), fill=accent)
    draw.rounded_rectangle((921, 52, 1038, 121), radius=26, fill="#0C2733")
    draw.text((940, 62), f"{index+1:02d}/08", font=bold(30), fill="#FFFFFF")
    for k in range(8):
        x = 59 + k * 122
        draw.rounded_rectangle((x, 148, x+105, 159), radius=5,
                               fill=accent if k <= index else "#A4B8BD")
    for j, line in enumerate((headline, subheadline)):
        draw.text((58, 195 + j * 124), line,
                  font=bold(91 if len(line) < 11 else 74),
                  fill="#FFFFFF" if j == 0 else accent,
                  stroke_width=4, stroke_fill="#0C2630")
    draw.rounded_rectangle((55, 1348, 495, 1423), radius=27, fill="#0D2633")
    draw.text((77, 1359), "今日の一歩  •  保存して実践",
              font=bold(34), fill="#FFFFFF")
    return result.convert("RGB")
