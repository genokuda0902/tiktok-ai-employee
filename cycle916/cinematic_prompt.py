"""cycle916 original cinematic prompt-editor scene; synthetic artwork only.
10 genres; frame 261-347 at 30fps, 1080x1160 overlay starting y=300.
No external media, automatic publishing, or actual data/results.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,FRAMES,START,Y0=1080,1160,30,87,261,300
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('週次報告を作る','数字と根拠を入れる','箇条書き３点','#38D8CB'),
 'business':('営業メモをまとめる','実績だけを使う','見出し＋３項目','#65BEFF'),
 'learning':('復習メモを作る','教科書に沿って確認','要点を３つ','#AD9CFF'),
 'health':('生活記録を整理','記録した事実だけ','日付順に３項目','#7ADBB0'),
 'beauty':('ケア記録を整理','使った内容を確認','手順を３つ','#FFB3CF'),
 'travel':('旅程を整理する','移動時刻を確認','時間順に３項目','#71D8F1'),
 'money':('支出をまとめる','実際の金額を確認','費目別に３項目','#8AE2AD'),
 'cooking':('献立をまとめる','材料と分量を確認','手順を３つ','#FFCA80'),
 'pets':('お世話メモ作成','観察した事実だけ','時系列で３項目','#F1D785'),
 'entertainment':('企画案を整理する','根拠のある内容だけ','アイデア３つ','#C8A7FF'),
}
def ft(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def width(s,size,bold=False):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)));b=d.textbbox((0,0),s,font=ft(size,bold));return b[2]-b[0]
def smooth(t):
 t=max(0.,min(1.,t));return t*t*(3-2*t)
def validate():
 assert len(GENRES)==10
 assert START==261 and FRAMES==87 and Y0+H==1460
 for k,(a,b,c,color) in GENRES.items():
  assert all(width(s,37,True)<565 for s in (a,b,c)),k
  assert color.startswith('#') and len(color)==7
 return True
def gradient():
 im=Image.new('RGB',(W,H));p=im.load()
 for y in range(H):
  for x in range(W):
   z=x/W;v=y/H
   g1=max(0,1-((z-.13)**2/.19+(v-.18)**2/.17))
   g2=max(0,1-((z-.92)**2/.16+(v-.73)**2/.23))
   p[x,y]=(int(8+16*v+20*g1+25*g2),int(24+22*v+34*g1+12*g2),int(43+16*v+43*g1+2*g2))
 return im
_BASE=None
def base():
 im=gradient().convert('RGBA');d=ImageDraw.Draw(im)
 d.ellipse((-290,-240,400,420),fill=(29,106,123,28))
 d.polygon([(0,880),(1080,770),(1080,1160),(0,1160)],fill='#162E43')
 for i in range(8):
  yy=900+i*34;d.line((0,yy,1080,yy-80),fill='#254459',width=2)
 sh=Image.new('RGBA',(W,H),(0,0,0,0));s=ImageDraw.Draw(sh)
 s.rounded_rectangle((108,150,974,920),radius=44,fill=(0,0,0,170))
 im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(35)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((99,138,958,900),radius=39,fill='#162C3B',outline='#55778B',width=6)
 d.rounded_rectangle((123,161,934,862),radius=23,fill='#E8F0F6')
 d.rounded_rectangle((123,161,934,250),radius=22,fill='#D7E5F0')
 d.rectangle((123,229,934,250),fill='#D7E5F0')
 for i,c in enumerate(('#F18C91','#EBC56D','#67CDB4')):
  d.ellipse((161+i*30,196,175+i*30,210),fill=c)
 d.text((280,183),'PROMPT EDITOR',font=ft(25,True),fill='#43677C')
 d.rounded_rectangle((142,277,914,798),radius=26,fill='#F7FAFD',outline='#CADDE9',width=3)
 d.text((175,308),'目的・条件・形式を分けて入力',font=ft(35,True),fill='#1A354B')
 for tag,y in (('01  目的',389),('02  条件',522),('03  形式',655)):
  d.rounded_rectangle((172,y,885,y+114),radius=18,fill='#EDF4F9',outline='#CFDFE8',width=2)
  d.text((200,y+13),tag,font=ft(24,True),fill='#567B90')
 d.polygon([(92,906),(974,906),(1052,1022),(17,1022)],fill='#8DA6B5')
 d.polygon([(108,920),(959,920),(1007,986),(60,986)],fill='#263E4C')
 for row in range(3):
  for col in range(12):
   x=135+col*68-row*10;y=930+row*18
   d.rounded_rectangle((x,y,x+52,y+11),radius=3,fill='#59717D')
 d.polygon([(24,1023),(1052,1023),(1022,1047),(47,1047)],fill='#B5C8D0')
 d.text((110,1082),'ORIGINAL ILLUSTRATION  /  REVIEW REQUIRED',font=ft(21),fill='#A8C4D4')
 return im.convert('RGB')
def render(frame,genre='ai_work'):
 global _BASE
 if not 0<=frame<FRAMES:raise ValueError('frame out of scene')
 if genre not in GENRES:raise ValueError('unknown genre')
 if _BASE is None:_BASE=base()
 texts=GENRES[genre][:3];accent=GENRES[genre][3]
 im=_BASE.copy();d=ImageDraw.Draw(im);stage=min(2,frame//29)
 for i,(txt,y) in enumerate(zip(texts,(389,522,655))):
  active=i==stage
  d.rounded_rectangle((172,y,885,y+114),radius=18,outline=accent if active else '#CADDE8',width=5 if active else 2)
  if active:
   p=smooth((frame-stage*29)/23)
   d.rounded_rectangle((184,y+100,184+int(686*p),y+106),radius=3,fill=accent)
  d.text((200,y+50),txt,font=ft(37,True),fill='#16364C' if active else '#5D7788')
  if i<stage:
   d.rounded_rectangle((823,y+17,859,y+52),radius=10,fill=accent)
   d.line((832,y+33,839,y+41,851,y+24),fill='#143749',width=4)
 x=144+int(680*smooth(frame/(FRAMES-1)))
 d.line((x,280,x+10,280),fill=accent,width=4)
 d.rounded_rectangle((700,298,870,344),radius=15,fill='#153F53')
 d.text((721,306),f'0{stage+1} / 03',font=ft(26,True),fill='#FFFFFF')
 return im
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work');args=p.parse_args()
 validate();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES):render(i,args.genre).save(out/f'{i:03d}.png')
 print('rendered',FRAMES,'frames',args.genre)
if __name__=='__main__':main()
