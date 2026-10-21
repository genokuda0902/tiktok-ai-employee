"""Reusable original concept-board illustration for slide-based video.

Pillow only, no third-party photographs, logos or remote image services.
The full MP4 compositor and technical QA live in the cycle740 reproducibility ZIP.
"""
from __future__ import annotations
from PIL import Image, ImageDraw
import random


def make_pcb(seed: int = 740, width: int = 1280, height: int = 820) -> Image.Image:
    rng = random.Random(seed)
    image = Image.new("RGB", (width, height), (5, 48, 45))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        draw.line((0, y, width, y), fill=(5, 52 - y // 55, 49 - y // 65))
    draw.rounded_rectangle((10, 10, width-11, height-11),
                           radius=24, outline=(96, 220, 183), width=9)
    for x, y in ((77, 76), (width-77, 76), (77, height-76), (width-77, height-76)):
        draw.ellipse((x-24, y-24, x+24, y+24), fill=(207, 177, 103))
        draw.ellipse((x-12, y-12, x+12, y+12), fill=(5, 25, 29))
    for _ in range(150):
        x = rng.randint(60, width-190)
        y = rng.randint(60, height-120)
        dx = rng.randint(24, 120)
        dy = rng.choice((-24, 24))
        draw.line([(x,y),(x+dx//2,y),(x+dx,y+dy)],
                  fill=(24, 125, 104), width=3)
    # Generic processor silhouette; not a commercial product depiction.
    draw.rounded_rectangle((400, 210, 840, 610), radius=30,
                           fill=(11, 30, 37), outline=(60, 166, 152), width=11)
    draw.rounded_rectangle((455, 260, 790, 555), radius=14,
                           fill=(12, 24, 33), outline=(172, 188, 185), width=10)
    for x in range(475, 775, 21):
        draw.rectangle((x, 244, x+9, 256), fill=(213, 166, 90))
        draw.rectangle((x, 560, x+9, 572), fill=(213, 166, 90))
    for y in range(278, 550, 21):
        draw.rectangle((440, y, 453, y+9), fill=(213, 166, 90))
        draw.rectangle((793, y, 805, y+9), fill=(213, 166, 90))
    for x,y,w,h in ((125,175,205,115),(145,337,190,90),(840,635,155,100)):
        draw.rounded_rectangle((x,y,x+w,y+h),radius=8,
                               fill=(13,26,34),outline=(116,146,143),width=5)
    for n in range(3):
        y=195+n*145
        draw.rounded_rectangle((1040,y,1225,y+120),radius=13,
                               fill=(39,54,60),outline=(186,199,196),width=7)
        draw.rounded_rectangle((1080,y+27,1195,y+87),radius=5,fill=(4,16,23))
    for x in range(250,940,24):
        draw.rectangle((x,63,x+10,92),fill=(210,167,89))
    # Subtle, seeded solder-mask flecks add material texture.
    for _ in range(500):
        x = rng.randint(50, width-50)
        y = rng.randint(50, height-50)
        draw.point((x, y), fill=(rng.randint(12, 52),
                                 rng.randint(65, 140), rng.randint(55, 130)))
    return image


if __name__ == "__main__":
    make_pcb().save("original_concept_board.png")
