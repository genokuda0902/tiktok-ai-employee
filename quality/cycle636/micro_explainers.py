"""Cycle636 reusable zero-cost micro-explainer overlay. Human review only."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

BOUNDS=(0,63,130,183,230,278,362,415,468)
NOTES=(
"基板1枚で動く小さなコンピューター",
"小型でもOSやアプリを動かせる",
"画面や入力機器をつないで操作",
"周辺機器をつなぎ、電源を入れる",
"プログラムでLEDを制御できる",
"入力を受けて処理し、結果を出す",
"アイデアを小さく試作してみる",
"公式の導入手順から始めよう",
)
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
CARD_X,CARD_Y=70,1470
CARD_WIDTH,CARD_HEIGHT=830,230

def render_card(note, index, font_path, accent=(85,235,200)):
    """Return a transparent RGBA panel for compositing at (70,1470)."""
    if not (1 <= index <= 8): raise ValueError("scene index must be 1..8")
    im=Image.new("RGBA",(CARD_WIDTH,CARD_HEIGHT),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((2,2,827,227),radius=24,fill=(3,27,42,248),outline=(*accent,205),width=3)
    d.rounded_rectangle((3,3,15,226),radius=6,fill=(*accent,255))
    bold=ImageFont.truetype(font_path,39)
    small=ImageFont.truetype(font_path,29)
    d.text((41,21),"もっとわかる +1",font=small,fill=(*accent,255))
    d.text((40,90),note,font=bold,fill=(251,253,255,255))
    d.rounded_rectangle((40,185,787,190),radius=3,fill=(38,71,82,255))
    d.rounded_rectangle((40,185,40+round(747*index/8),190),radius=3,fill=(*accent,255))
    return im

def filter_chain():
    """For ffmpeg input 0=video, inputs 1..8=looped card PNGs."""
    return ";".join(
        f"[{'0:v' if i==0 else 'v'+str(i)}][{i+1}:v]overlay=x=70:y=1470:format=auto:enable='between(n,{BOUNDS[i]},{BOUNDS[i+1]-1})'[v{i+1}]"
        for i in range(8)
    )

def publication_state():
    return {"status":"HUMAN_REVIEW","publication":"NOT_APPROVED","auto_post":False}
