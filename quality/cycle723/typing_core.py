"""Cycle723 generic Japanese prompt animation. Review-only, no publishing."""
from PIL import Image, ImageDraw, ImageFont
FPS = 30
DURATION = 3.3
GENRES = ("ai_work","beauty","love_psychology","saving","sales_business","career","health","science","travel_food","product_comparison")
PUBLISH_ALLOWED = False

def visible_chars(frame, length, fps=FPS):
    return min(length, max(0, int(length * min(1, frame / (fps * 2.7)))))

def phase(frame, fps=FPS):
    t = frame / fps
    return "typing" if t < 2.7 else ("send" if t < 3.02 else "sent")

def render_prompt_frame(prompt, frame, font_path, size=(900,600)):
    im = Image.new("RGBA", size, "#11344f")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20,30,size[0]-20,size[1]-30),radius=26,fill="#f4faff",outline="#43bfd9",width=4)
    font = ImageFont.truetype(font_path,35)
    d.text((60,70),"AIへの指示 / DEMO",font=font,fill="#153e62")
    lines = [prompt[i:i+16] for i in range(0,len(prompt),16)]
    shown = prompt[:visible_chars(frame,len(prompt))]
    for idx in range(min(4,len(lines))):
        line = shown[idx*16:(idx+1)*16]
        d.text((60,165+idx*60),line,font=font,fill="#173d58")
    d.rounded_rectangle((620,470,820,545),radius=18,fill="#1473b8")
    d.text((647,480),"送信 →",font=font,fill="white")
    if phase(frame)=="sent":
        d.text((65,485),"送信済み（デモ）",font=font,fill="#087d70")
    return im
