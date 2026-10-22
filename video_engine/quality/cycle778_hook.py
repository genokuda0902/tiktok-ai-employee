"""cycle778 reusable image-first hook contract + review-only frame renderer.

Local full-video compositor and final MP4 are distributed in the cycle778 ZIP.
No confidential imagery, voice or other assets are stored in GitHub.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1080,1920,30
GENRES={
 "AI・仕事効率化":"#33E8DB","美容・身だしなみ":"#FF9CC7",
 "恋愛・心理":"#FF98C5","お金・節約":"#F7CD67",
 "営業・ビジネス":"#7CBFFF","転職・キャリア":"#C0A5FF",
 "健康・生活改善":"#82E5AF","雑学・科学":"#7FE0F1",
 "旅行・グルメ":"#FFB784","商品比較・暮らし":"#D6B7FF"}
MONTHS=(120000,150000,200000,180000)
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def validate(meta):
    if set(meta.get("supported_genres",[]))!=set(GENRES):
        raise ValueError("exact ten genres required")
    if meta.get("genre") not in GENRES: raise ValueError("unknown genre")
    if meta.get("monthly_sales")!=list(MONTHS) or meta.get("total_yen")!=sum(MONTHS):
        raise ValueError("numeric mismatch")
    if meta.get("source_rights")!="unverified_review_only" or meta.get("audio_rights")!="unverified_review_only":
        raise ValueError("rights must remain unverified")
    if meta.get("publication_approved") is not False or meta.get("quality_approved") is not False:
        raise ValueError("review required")
    if meta.get("manual_post_only") is not True or meta.get("performance_claim") is not None:
        raise ValueError("no auto post or fabricated claim")
    if meta.get("new_assets")!="original_graphics_plus_inherited_robot":
        raise ValueError("asset provenance required")
    return True

def ease(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)

@lru_cache(maxsize=30)
def font(size,bold=True):
    return ImageFont.truetype(BOLD if bold else REG,size)

def safe_box(box,important=True):
    x0,y0,x1,y1=box
    return x0>=58 and x1<=1000 and y0>=190 and y1<=(1530 if important else 1710)

def draw_text(d,x,y,s,size,color="#FFFFFF",bold=True):
    d.text((x+4,y+5),s,font=font(size,bold),fill="#06131F")
    d.text((x,y),s,font=font(size,bold),fill=color)

def vector_robot():
    im=Image.new("RGB",(720,610),"#0D2540");d=ImageDraw.Draw(im)
    d.ellipse((140,60,620,480),fill="#C7E5F9",outline="#7CCCF3",width=12)
    d.rounded_rectangle((192,144,570,380),radius=95,fill="#071523",outline="#7DD5F6",width=7)
    for x in (295,458):d.ellipse((x-25,235,x+25,300),fill="#36E5F5")
    d.rounded_rectangle((225,420,570,610),radius=90,fill="#9FC8E9")
    return im

def draw_frame(frame,robot=None,genre="AI・仕事効率化"):
    if frame not in range(96):raise ValueError("hook frame out of range")
    if genre not in GENRES:raise ValueError("unknown genre")
    if robot is None:robot=vector_robot()
    t=frame/FPS
    accent=tuple(bytes.fromhex(GENRES[genre][1:]))
    im=Image.new("RGB",(W,H))
    d=ImageDraw.Draw(im)
    for y in range(0,H,6):
        a=y/H
        d.rectangle((0,y,W,y+6),fill=(int(7+8*a),int(19+19*a),int(39+19*a)))
    glow=Image.new("RGBA",(W,H));g=ImageDraw.Draw(glow)
    g.ellipse((160,480,1380,1480),fill=(*accent,65))
    im=Image.alpha_composite(im.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(140))).convert("RGB")
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((68,210,483,280),radius=22,fill="#123B50",outline=accent,width=3)
    draw_text(d,92,226,"AI時短ラボ / EXCEL",30)
    draw_text(d,67,325,"Excel集計、",88)
    draw_text(d,67,443,"まだ手作業？",96,"#FFDA72")
    d.rounded_rectangle((75,584,75+max(1,int(885*ease((t+.1)/.6))),596),radius=5,fill=accent)
    scale=1.04-.04*ease(t/2.5)
    rw,rh=int(792*scale),int(628*scale)
    subject=robot.resize((rw,rh),Image.Resampling.LANCZOS)
    card=Image.new("RGB",(840,660),"#10263A")
    card.paste(subject,((840-rw)//2,(660-rh)//2))
    mask=Image.new("L",(840,660),0)
    ImageDraw.Draw(mask).rounded_rectangle((8,8,832,650),radius=58,fill=255)
    im.paste(card,(120,643),mask.filter(ImageFilter.GaussianBlur(8)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((115,637,965,1310),radius=62,outline=accent,width=5)
    if t>=.9:
        d.rounded_rectangle((75,1350,994,1540),radius=32,fill="#071B2F",outline=accent,width=4)
        draw_text(d,109,1370,"4か月の売上合計（架空データ）",32)
        if t>=1.15:
            draw_text(d,107,1422,"65",82)
            draw_text(d,269,1440,"万円",52)
            draw_text(d,655,1454,"= 650,000円",30)
    d.text((86,1630),"※ 操作の再現イメージ / 効果未検証",font=font(29,False),fill="#BCD0DE")
    return im
