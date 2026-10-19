"""Reusable original procedural proof-hook graphic for 10 TikTok genres.

Draws a first-second truthful result card on a PIL frame. This is the
reusable hook component, not the full cycle704 20s video renderer.
"""
import math
from PIL import ImageDraw, ImageFont
from retention_contract import proof_hook

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def draw_verified_hook(image, t, *, label="青の売上だけなら",
                       equation="2,500 + 3,500", value=6000):
    proof_hook(t, value=value)
    d = ImageDraw.Draw(image)
    def text(x, y, string, size, color="#ffffff"):
        font = ImageFont.truetype(FONT, size)
        d.text((x, y), string, font=font, fill=color, anchor="ma")
    d.rounded_rectangle((43,286,496,614),radius=28,fill="#0b3155",
                        outline="#18bfe5",width=4)
    d.rounded_rectangle((64,305,474,367),radius=14,fill="#124b73")
    text(270,315,label,26,"#d8f6ff")
    size=int(61*(1+.035*math.sin(2*math.pi*1.5*t)))
    text(270,404,f"{value:,}円",size,"#80ffdb")
    d.rounded_rectangle((81,510,460,575),radius=12,fill="#123f60")
    text(270,525,equation,29)
    # No reference art reused: a simple geometric accent.
    d.ellipse((375,600,484,709),fill="#bcefff",outline="#36c5f0",width=5)
    d.rounded_rectangle((392,623,469,674),radius=14,fill="#0a2340")
    for x in (414,448):
        d.ellipse((x-7,640,x+7,655),fill="#40dfff")
    d.arc((411,659,448,680),start=10,end=170,fill="#54e9ed",width=3)
    end=90+int(340*min(1.,t/1.6))
    d.rounded_rectangle((88,587,end,595),radius=3,fill="#22e6c1")
    return image
