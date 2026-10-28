"""Cycle917: 3-beat reusable prompt template, private review-only overlay.
All artwork is original Pillow shapes and text. No external assets, data, or publishing.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,FRAMES,START,Y0=1080,1260,30,78,510,150
SAFE_CAPTION_Y=1490
STATUS='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('月次の売上を整理','元データだけを使う','表＋要点３つ','#16B8C8'),
 'business':('営業報告を整理','確定した実績のみ','表＋改善点３つ','#3888DC'),
 'learning':('学習内容を整理','教科書と照合する','要点＋復習３問','#7967D8'),
 'health':('生活記録を整理','診断は断定しない','日付順の一覧','#20A784'),
 'beauty':('ケア記録を整理','使用履歴を確認','手順＋注意点','#D978A0'),
 'travel':('旅程を整理する','移動時刻を確認','時系列の旅程表','#278EB9'),
 'money':('支出記録を整理','金額を元票で確認','費目別の集計表','#368D62'),
 'cooking':('献立を整理する','材料と分量を確認','買い物リスト','#C68435'),
 'pets':('お世話記録を整理','観察事実のみ記載','日付順のメモ','#AD8935'),
 'entertainment':('企画案を整理する','事実と案を区別','企画案を３つ','#9B70CA'),
}
LABELS=('目的','条件','出力')

def ft(size,bold=False):
 return ImageFont.truetype(BOLD if bold else FONT,size)

def tw(text,size,bold=False):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 a=d.textbbox((0,0),text,font=ft(size,bold))
 return a[2]-a[0]

def smooth(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)

def validate():
 assert len(GENRES)==10
 assert Y0+H < SAFE_CAPTION_Y and START+FRAMES<=691
 for genre,(a,b,c,col) in GENRES.items():
  assert all(tw(t,49,True)<660 for t in (a,b,c)),genre
  assert len(col)==7 and col[0]=='#'
 return True

def background():
 im=Image.new('RGB',(W,H));p=im.load()
 for y in range(H):
  v=y/H
  for x in range(W):
   u=x/W;glow=max(0,1-((u-.84)**2/.15+(v-.1)**2/.19))
   p[x,y]=(int(8+22*v+8*glow),int(29+19*v+45*glow),int(54+23*v+62*glow))
 return im
BASE=None

def frame(i,genre='ai_work'):
 global BASE
 if not 0<=i<FRAMES: raise ValueError('frame out of range')
 if genre not in GENRES: raise ValueError('unknown genre')
 if BASE is None: BASE=background()
 im=BASE.copy().convert('RGBA');d=ImageDraw.Draw(im)
 values=GENRES[genre];accent=values[3]
 d.rounded_rectangle((65,38,1015,146),radius=27,fill='#0D334A',outline='#2B7286',width=3)
 d.text((95,60),'使える指示は、型に残す',font=ft(59,True),fill='#FFFFFF')
 d.text((86,166),'保存用テンプレート  /  架空の例',font=ft(33,True),fill='#C5E9F4')
 sh=Image.new('RGBA',(W,H),(0,0,0,0));s=ImageDraw.Draw(sh)
 s.rounded_rectangle((76,228,1005,940),radius=40,fill=(0,0,0,135))
 im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(27)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((66,212,994,922),radius=38,fill='#F3F8FB')
 d.rounded_rectangle((66,212,994,298),radius=38,fill='#DDEDF5')
 d.rectangle((66,260,994,298),fill='#DDEDF5')
 d.text((100,232),'PROMPT TEMPLATE',font=ft(37,True),fill='#173A50')
 for j,(label,val) in enumerate(zip(LABELS,values[:3])):
  y=330+j*181
  local=(i-j*26)/26
  glow=smooth(min(1,max(0,local*4))) if 0<=local<=1 else 0
  active=j==min(2,i//26)
  fill='#FFFFFF' if not active else '#E3F8F8'
  outline='#D1E2E9' if not active else accent
  d.rounded_rectangle((104,y,958,y+156),radius=24,fill=fill,outline=outline,width=5 if active else 2)
  d.rounded_rectangle((123,y+20,241,y+72),radius=17,fill=accent if active else '#B9CBD4')
  d.text((143,y+22),label,font=ft(34,True),fill='#FFFFFF' if active else '#193A4B')
  d.text((270,y+29),val,font=ft(49,True),fill='#12364A')
  if active:
   xx=272+int(600*smooth(min(1,(i%26)/25)))
   d.rounded_rectangle((270,y+119,xx,y+126),radius=3,fill=accent)
  else:
   d.line((270,y+122,912,y+122),fill='#E5EEF2',width=3)
 d.text((80,965),'目的',font=ft(33,True),fill='#FFFFFF')
 d.text((400,965),'条件',font=ft(33,True),fill='#FFFFFF')
 d.text((735,965),'出力',font=ft(33,True),fill='#FFFFFF')
 for j,x in enumerate((80,398,733)):
  d.rounded_rectangle((x,1017,x+267,1030),radius=6,fill=accent if j<=i//26 else '#3B6274')
 d.text((84,1054),'数字は必ず元データと照合',font=ft(31),fill='#C6E4EB')
 d.line((84,1144,994,1144),fill='#2D6577',width=3)
 d.text((86,1173),'AI時短ラボ   /   REVIEW ONLY',font=ft(28,True),fill='#95CBD6')
 return im.convert('RGB')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--genre',default='ai_work',choices=sorted(GENRES));ap.add_argument('--out',required=True)
 a=ap.parse_args();validate();p=Path(a.out);p.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES):frame(i,a.genre).save(p/f'{i:03d}.png',compress_level=1)
 print(f'generated {FRAMES} original frames: {p}')
if __name__=='__main__':main()
