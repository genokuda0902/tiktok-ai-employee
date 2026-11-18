"""Clean 1080x1920 Japanese slide generator (no cumulative video re-encoding)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TOPICS = [
    ("目的", "最初に目的を伝える"),
    ("画像", "情報を見やすく整理"),
    ("音声", "聞き取りやすい音量"),
    ("字幕", "短く・読みやすく"),
    ("検証", "公開前に品質確認"),
]
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def render_slide(index: int, dest: str | Path) -> None:
    if not 0 <= index < len(TOPICS):
        raise ValueError("slide index must be 0..4")
    image = Image.new("RGB", (1080, 1920), (8, 22, 29))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((65, 110, 1015, 1805), radius=55,
                           fill=(13, 43, 48), outline=(59, 114, 112), width=3)
    font = lambda size: ImageFont.truetype(FONT, size)
    draw.text((118, 200), "SoA / VIDEO QUALITY LAB", font=font(34), fill="#9dd2ca")
    draw.text((118, 300), "動画品質を上げる 5つの視点", font=font(49), fill="#f2f8f3")
    for j in range(5):
        x = 118 + j * 170
        draw.rounded_rectangle((x, 420, x + 150, 432), radius=6,
                               fill="#6ddab5" if j <= index else "#335759")
    draw.text((118, 550), f"{index + 1:02d} / 05", font=font(85), fill="#74e0bb")
    topic, title = TOPICS[index]
    draw.text((118, 780), topic, font=font(65), fill="#99d9ca")
    draw.text((118, 910), title, font=font(52), fill="#ffffff")
    draw.text((118, 1575), "要約字幕 / 音声の逐語転写ではありません",
              font=font(27), fill="#a5c4be")
    draw.text((118, 1675), "社内レビュー用・公開品質未承認",
              font=font(27), fill="#a9c9c2")
    image.save(dest)
