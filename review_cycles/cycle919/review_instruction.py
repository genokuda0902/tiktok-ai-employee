"""cycle919: offline, review-only correction-instruction motion card.

Original procedural art, 10 genre presets. No uploads, no posting, no
personal data or factual performance claims. Designed to replace only
scene 06 (frames 435..521, y=300..1459) of the inherited review MP4.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H, N, FPS, FIRST, TOP = 1080, 1160, 87, 30, 435, 300
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
 'ai_work':('AIの出力を改善','もっと良くして','冒頭の見出し','1行で短くする','画面で読みやすさを確認'),
 'business':('提案資料を改善','いい感じにして','提案の結論','最初に1文で示す','読み手に伝わるか確認'),
 'learning':('学習メモを改善','分かりやすくして','用語の説明','具体例を1つ添える','自分の言葉で説明して確認'),
 'health':('記録表を改善','見やすくして','睡眠の記録欄','日付と時間を分ける','記録漏れがないか確認'),
 'beauty':('ケア記録を改善','整えてほしい','使用アイテム欄','商品名を短くまとめる','読み間違いがないか確認'),
 'travel':('旅行メモを改善','便利にして','移動予定の欄','出発地と到着地を分ける','順番を見直して確認'),
 'money':('家計メモを改善','きれいにして','固定費の欄','項目と金額を分ける','入力漏れがないか確認'),
 'cooking':('レシピを改善','簡単にして','材料の一覧','分量を横に並べる','買い物前に見直して確認'),
 'pets':('お世話記録を改善','分かりやすく','食事の記録欄','時刻と量を分ける','記録漏れがないか確認'),
 'entertainment':('企画案を改善','もっと面白く','冒頭の一言','主題を先に伝える','最初の数秒を見直す'),
}

def font(size:int,bold:bool=False):
 return ImageFont.truetype(BOLD if bold else REG,size)

def ease(t):
 t=max(0.,min(1.,t));return t*t*(3-2*t)

def text_width(s,size,bold=True):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 return d.textbbox((0,0),s,font=font(size,bold))[2]

def validate_presets():
 assert len(GENRES)==10
 for key,vals in GENRES.items():
  assert len(vals)==5 and all(vals),key
  assert text_width(vals[0],57)<850,key
  assert text_width(vals[1],57)<700,key
  assert text_width(vals[2],47)<670,key
  assert text_width(vals[3],47)<670,key
  assert text_width(vals[4],39)<850,key
 return True

def base_image():
 yy,xx=np.mgrid[0:H,0:W];u=xx/W;v=yy/H
 light=np.exp(-((u-.88)**2/.18+(v-.10)**2/.1))
 arr=np.empty((H,W,3),dtype=np.uint8)
 arr[:,:,0]=np.clip(7+8*v+16*light,0,255)
 arr[:,:,1]=np.clip(20+12*v+22*light,0,255)
 arr[:,:,2]=np.clip(41+17*v+27*light,0,255)
 im=Image.fromarray(arr,'RGB');d=ImageDraw.Draw(im)
 for x in range(-800,1500,96):d.line((x,0,x+900,H),fill='#17344A',width=2)
 d.rounded_rectangle((49,39,1031,1121),radius=50,outline='#2E526B',width=2)
 d.rounded_rectangle((79,63,321,119),radius=26,fill='#21435D')
 d.text((111,72),'REVIEW  /  06',font=font(27,True),fill='#B9E8EF')
 d.text((772,77),'ONE CHANGE',font=font(23,True),fill='#86B4C7')
 return im

_BG=None

def panel(im,rect,fill,stroke,shadow=True):
 if shadow:
  layer=Image.new('RGBA',im.size,(0,0,0,0));ld=ImageDraw.Draw(layer)
  x1,y1,x2,y2=rect;ld.rounded_rectangle((x1+8,y1+14,x2+8,y2+14),radius=34,fill=(0,0,0,125))
  layer=layer.filter(ImageFilter.GaussianBlur(15));im.paste(layer,(0,0),layer)
 d=ImageDraw.Draw(im);d.rounded_rectangle(rect,radius=34,fill=fill,outline=stroke,width=3)

def render(index:int,genre:str='ai_work'):
 global _BG
 if genre not in GENRES:raise ValueError('unknown genre')
 if not 0<=index<N:raise ValueError('frame outside scene')
 if _BG is None:_BG=base_image()
 title,vague,target,action,verify=GENRES[genre]
 t=index/(N-1);ng=ease(t/.23);focus=ease((t-.28)/.24);ok=ease((t-.30)/.55)
 im=_BG.copy();d=ImageDraw.Draw(im)
 d.text((83,143),title,font=font(57,True),fill='#F6FBFF')
 d.text((86,227),'曖昧な指示を、確認できる1項目に。',font=font(34),fill='#B8D2E0')
 by=int(323+17*(1-ng));panel(im,(78,by,1002,by+226),'#F5F5F7','#F6ACAC')
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((109,by+27,278,by+83),radius=18,fill='#B54B5B')
 d.text((138,by+35),'BEFORE',font=font(27,True),fill='#FFFFFF')
 d.text((114,by+102),vague,font=font(57,True),fill='#253649')
 d.text((118,by+175),'直す場所が曖昧',font=font(27),fill='#A44E5C')
 if focus>0:
  x2=118+int((text_width(vague,57)+24)*focus)
  d.line((114,by+171,x2,by+171),fill='#E76A75',width=8)
  d.rounded_rectangle((805,by+34,962,by+87),radius=18,fill='#FBE0E1')
  d.text((829,by+42),'要修正',font=font(27,True),fill='#A94554')
 y_arrow=587
 d.rounded_rectangle((481,y_arrow,599,y_arrow+50),radius=20,fill='#1D6071')
 d.polygon([(518,y_arrow+50),(562,y_arrow+50),(540,y_arrow+77)],fill='#1D6071')
 ay=688;panel(im,(78,ay,1002,1012),'#F6FCFD','#73E2D0')
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((109,ay+27,259,ay+82),radius=18,fill='#087B78')
 d.text((137,ay+34),'AFTER',font=font(27,True),fill='white')
 if ok>.04:
  if ok>.16:
   d.text((119,ay+111),'直す場所',font=font(31,True),fill='#287E8C')
   d.text((330,ay+104),target,font=font(47,True),fill='#193A4B')
  if ok>.55:
   d.line((119,ay+184,960,ay+184),fill='#D4E5EA',width=3)
   d.text((119,ay+210),'直し方',font=font(31,True),fill='#287E8C')
   d.text((330,ay+203),action,font=font(47,True),fill='#193A4B')
  if ok>.85:
   d.rounded_rectangle((116,ay+273,964,ay+314),radius=14,fill='#DFF7F0')
   d.text((138,ay+275),'✓  '+verify,font=font(30,True),fill='#165B57')
 d.text((125,1062),'1つずつ直し、見比べて確認する',font=font(40,True),fill='#E8F8FB')
 return im

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--preview-only',action='store_true');a=p.parse_args()
 validate_presets();a.output.mkdir(parents=True,exist_ok=True)
 indices=[12,44,78] if a.preview_only else range(N)
 for i in indices:render(i,a.genre).save(a.output/f'frame_{FIRST+i:04d}.png',compress_level=2)
 print(f'frames={len(indices)} genre={a.genre} folder={a.output}')
if __name__=='__main__':main()
