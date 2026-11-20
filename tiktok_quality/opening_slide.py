"""Reusable Japanese intro card for 10 content genres. Requires Pillow."""
from PIL import Image, ImageDraw, ImageFont

def render_intro(path, headline, subline, font_path, *, width=1080, height=1920):
    if not headline or not subline:
        raise ValueError("headline and subline are required")
    im = Image.new("RGB", (width, height), "#031c21")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((65,260,width-65,height-360),radius=55,fill="#08383b",outline="#4edcc0",width=3)
    for y, message, size, color in [(440,headline,70,"#ffffff"),(790,subline,52,"#60e6c9")]:
        font=ImageFont.truetype(font_path,size)
        bounds=d.textbbox((0,0),message,font=font)
        if bounds[2]-bounds[0] > width-160:
            raise ValueError("text exceeds safe width")
        d.text(((width-(bounds[2]-bounds[0]))//2,y),message,font=font,fill=color)
    im.save(path)
