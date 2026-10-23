"""Render a clean GPIO → resistor → LED → GND explanatory image."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def generate(path, accent="#52EBD0"):
    im = Image.new("RGB", (1080, 1360), "#061528")
    d = ImageDraw.Draw(im)
    def label(x, y, words, size=48, color="white"):
        d.text((x, y), words, font=ImageFont.truetype(FONT, size), fill=color)
    d.rounded_rectangle((48, 50, 1032, 1240), radius=35, fill="#071D2B", outline=accent, width=4)
    label(82, 100, "LEDも光らせられる。", 74, accent)
    label(160, 340, "GPIO → 抵抗 → LED → GND", 44)
    d.rounded_rectangle((80, 530, 310, 750), radius=20, fill="#0A4247", outline=accent, width=5)
    label(117, 600, "GPIO", 54)
    d.line([(310,640),(400,640)],fill="#F5C676",width=13)
    d.line([(400,640),(430,610),(460,670),(490,610),(520,670),(550,640)],fill="#F5C676",width=13)
    d.line([(550,640),(675,640)],fill="#F5C676",width=13)
    d.ellipse((675,580,805,710),fill=accent)
    d.line([(805,640),(945,640),(945,740)],fill="#F5C676",width=13)
    for offset, half in [(0,44),(18,30),(36,16)]:
        d.line([(945-half,740+offset),(945+half,740+offset)],fill="#F5C676",width=9)
    label(398, 530, "330Ω", 40, "#FFE0A0")
    label(700, 760, "LED", 36)
    label(885, 810, "GND", 36)
    label(125, 1000, "抵抗で電流を制限", 42)
    label(125, 1100, "※330Ωは一例。機器の仕様を確認", 30, "#A9C5CF")
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    im.save(path)

if __name__ == "__main__":
    generate("output/scene5_circuit.png")
