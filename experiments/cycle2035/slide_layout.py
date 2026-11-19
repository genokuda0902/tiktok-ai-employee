"""Reusable slide composition: independent non-overlapping text regions."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess

REGIONS = {"heading": (110, 480, 970, 650), "body": (110, 745, 970, 1200), "caption": (110, 1410, 970, 1620)}
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def make_slide(number: int, heading: str, body: str, caption: str, output: Path):
    im = Image.new("RGB", (1080, 1920), "#081b23")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((58, 92, 1022, 1828), radius=48, fill="#103138", outline="#3d7979", width=3)
    d.text((110, 155), "SOA / VIDEO QUALITY LAB", font=ImageFont.truetype(FONT, 31), fill="#b1d3cf")
    d.text((110, 345), f"{number:02d} / 05", font=ImageFont.truetype(BOLD, 80), fill="#62e3bf")
    d.text((110, 570), heading, font=ImageFont.truetype(BOLD, 66), fill="white")
    d.rounded_rectangle(REGIONS["body"], radius=32, fill="#17434a")
    d.text((165, 850), body, font=ImageFont.truetype(BOLD, 46), fill="white")
    d.rounded_rectangle(REGIONS["caption"], radius=22, fill="#061f27")
    d.text((145, 1472), caption, font=ImageFont.truetype(FONT, 35), fill="white")
    d.text((110, 1725), "社内レビュー用・公開品質未承認", font=ImageFont.truetype(FONT, 27), fill="#a8c1bf")
    im.save(output)
