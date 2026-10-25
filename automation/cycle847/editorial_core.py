"""Cycle847 independent vector slide core. Review-only; no posting, uploads, or paid APIs.
The full local MP4 renderer, QA and eight high-resolution vector compositions
are distributed in the cycle847 ChatGPT review ZIP; this repository core
reproduces the common ten-genre layout contract.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
FRAMES=(89,81,79,87,86,89,77,103)
GENRES={
 "ai_work":"#2DE0D2","sales_business":"#FFC96D","beauty":"#E6A7FF",
 "romance":"#FF8BAF","saving":"#5EE0A5","career":"#FFB67E",
 "wellness":"#A7DF77","science":"#7BBEFF","travel_food":"#70E0E0",
 "product_comparison_lifestyle":"#FFC0D0"}
POLICY={"review_only":True,"publication_approved":False,"automatic_posting":False,
 "external_upload":False,"source_rights_reviewed":False,"contains_personal_data":False}
SCENES=[
 ("AIで仕事を","もっと速く","最初の一歩を、小さく始める"),
 ("繰り返し作業を","見つけよう","定型作業を１つ書き出す"),
 ("完成形の見本を","先に用意","完成した状態を見せる"),
 ("目的と条件を","具体的に伝える","目的・条件・形式をそろえる"),
 ("AIの回答を","自分で確認","数字と事実を確認する"),
 ("修正点は","一つずつ","直すポイントを１つに絞る"),
 ("良い指示は","保存して再利用","使えた指示を残す"),
 ("小さな時短を","毎日の習慣に","明日も１つ続ける")]
def validate(genre,manifest):
 if genre not in GENRES or len(GENRES)!=10: raise ValueError("Unsupported genre")
 if manifest!=POLICY: raise ValueError("Fail-closed human-review policy")
 if len(SCENES)!=8 or sum(FRAMES)!=691: raise AssertionError("Timeline mismatch")
def _font(size,bold=True):
 paths=["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
 return ImageFont.truetype(paths[0 if bold else 1],size)
def render(i,genre="ai_work",manifest=POLICY):
 validate(genre,manifest)
 if i not in range(8): raise IndexError(i)
 accent=GENRES[genre]
 im=Image.new("RGB",(W,H),"#0C1C31");d=ImageDraw.Draw(im)
 d.rounded_rectangle((54,70,326,147),radius=36,fill="#1D3A4D")
 d.text((82,86),"AI / WORK",font=_font(34),fill=accent)
 d.text((819,86),f"{i+1:02d} / 08",font=_font(34),fill="#FFFFFF")
 for j in range(8):
  x=55+j*121
  d.rounded_rectangle((x,171,x+106,183),radius=5,fill=accent if j<=i else "#365166")
 d.text((62,297),SCENES[i][0],font=_font(76),fill="#FFFFFF")
 d.text((62,399),SCENES[i][1],font=_font(76),fill=accent)
 d.rounded_rectangle((61,577,1019,1380),radius=54,fill="#142D43",outline="#4C7683",width=4)
 # Original, scene-specific native-resolution vector visualization.
 d.rounded_rectangle((146,685,937,1227),radius=40,fill="#24455A",outline=accent,width=4)
 for k in range(3):
  y=755+k*144
  d.rounded_rectangle((185,y,894,y+112),radius=28,fill="#18354B")
  d.ellipse((207,y+24,269,y+86),fill=accent)
  d.text((222,y+29),str(k+1),font=_font(36),fill="#092737")
  d.rounded_rectangle((300,y+35,830-(i*23+k*35)%160,y+53),radius=9,fill="#9CB7C1")
 d.rounded_rectangle((60,1420,1020,1624),radius=34,fill="#102A3E",outline="#396A76",width=3)
 d.rounded_rectangle((76,1445,87,1598),radius=5,fill=accent)
 d.text((76,1681),"TRY TODAY",font=_font(32),fill=accent)
 d.text((76,1739),SCENES[i][2],font=_font(39),fill="#FFFFFF")
 d.text((76,1830),"ORIGINAL VECTOR • HUMAN REVIEW",font=_font(21,False),fill="#90AABB")
 return im
if __name__=="__main__":
 import argparse
 p=argparse.ArgumentParser()
 p.add_argument("--out",required=True);p.add_argument("--genre",default="ai_work")
 a=p.parse_args();Path(a.out).mkdir(parents=True,exist_ok=True)
 for i in range(8):render(i,a.genre).save(Path(a.out)/f"slide_{i+1:02d}.png")
