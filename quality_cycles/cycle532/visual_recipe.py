"""Reusable procedural perspective-board component from cycle532 (no third-party assets).
Requires Pillow, numpy and opencv-python. Safe for all ten genres.
Full MP4 orchestration and QA scripts are distributed with the cycle532 output ZIP.
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import cv2

WIDTH, HEIGHT = 1080, 1920
GENRES = ("AI時短", "仕事術", "営業", "ビジネスマナー", "勉強",
          "お金の管理", "暮らし", "旅行", "ガジェット", "雑学")
PERSPECTIVE = np.float32([[95, 890], [782, 650], [1000, 1080], [300, 1300]])

def board_texture(seed=532):
    """Original conceptual PCB illustration, NOT a product photograph."""
    rng = np.random.default_rng(seed)
    im = Image.new("RGBA", (960, 680), (4, 69, 62, 255))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((16, 16, 944, 664), radius=22,
                        outline=(84, 236, 196, 230), width=7)
    for _ in range(105):
        x, y = int(rng.integers(32, 928)), int(rng.integers(32, 648))
        xx = int(np.clip(x + rng.choice([-1, 1]) * rng.integers(50, 230), 30, 930))
        yy = int(np.clip(y + rng.choice([-1, 1]) * rng.integers(20, 140), 30, 650))
        d.line([(x, y), (xx, y), (xx, yy)], fill=(29, 151, 130, 145), width=3)
        d.ellipse((xx-4, yy-4, xx+4, yy+4), fill=(177, 184, 98, 200))
    d.rounded_rectangle((336, 190, 655, 470), radius=22,
                        fill=(11, 25, 37), outline=(106, 177, 169), width=9)
    for y in (108, 250, 405):
        d.rounded_rectangle((842, y, 956, y+70), radius=6,
                            fill=(177, 187, 183), outline=(232, 234, 219), width=5)
    return im

def composite_perspective(background, seed=532, corners=None):
    """Project an original board illustration into a 3D-like 1080x1920 scene."""
    if background.size != (WIDTH, HEIGHT):
        raise ValueError("background must be 1080x1920")
    corners = PERSPECTIVE.copy() if corners is None else np.asarray(corners, dtype=np.float32)
    if corners.shape != (4, 2):
        raise ValueError("four x/y corners required")
    tex = np.array(board_texture(seed))
    src = np.float32([[0, 0], [960, 0], [960, 680], [0, 680]])
    transform = cv2.getPerspectiveTransform(src, corners)
    projected = cv2.warpPerspective(tex, transform, (WIDTH, HEIGHT),
                                    flags=cv2.INTER_CUBIC,
                                    borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=(0, 0, 0, 0))
    out = background.convert("RGBA")
    shade = Image.new("RGBA", out.size)
    d = ImageDraw.Draw(shade)
    polygon = [tuple(map(int, p)) for p in corners]
    d.polygon([(x+25, y+56) for x, y in polygon], fill=(0, 0, 0, 210))
    out.alpha_composite(shade.filter(ImageFilter.GaussianBlur(53)))
    out.alpha_composite(Image.fromarray(projected, "RGBA"))
    return out

if __name__ == "__main__":
    bg = Image.new("RGB", (WIDTH, HEIGHT), "#081c2c")
    composite_perspective(bg).convert("RGB").save("cycle532_board_preview.jpg", quality=90)
