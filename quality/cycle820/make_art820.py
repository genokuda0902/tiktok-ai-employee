"""Cycle820: original portrait-free editorial slide artwork (Pillow only).
No third-party images, icons, fonts, remote services or personal data.
All captions and narration are applied separately by the existing CI renderer.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1080,1920
PALETTES={
 'ai_work':'#31B7DA','beauty':'#E978A4','love_psychology':'#A98DE7',
 'money_saving':'#E8A548','sales_business':'#16A996','career':'#4D88DB',
 'health_life':'#75B46D','science':'#3A9CCB','travel_food':'#E58C5B',
 'product_life':'#A480CC'}
HEADS=[('01  /  THE QUESTION','質問が違う','問いが変われば、行動が変わる'),
 ('02  /  THE GOAL','ゴールを確認','最初に、目指す場所を決める'),
 ('03  /  THE DATA','数字を確かめる','感覚ではなく、事実を見よう'),
 ('04  /  THE GAP','差を一つに絞る','最優先の課題は、ひとつ'),
 ('05  /  WHY × 3','なぜを三回','表面の答えで、止まらない'),
 ('06  /  TODAY','今日の行動へ','いつ・誰が・何をするか'),
 ('07  /  REVIEW','結果を見て修正','試す → 測る → 直す'),
 ('08  /  TEAM','強いチームへ','改善の積み重ねが、未来を変える')]
DURATIONS=[3.355,3.085,3.025,3.285,3.265,3.36,2.97,3.495]
SPEECH=['仕事ができる人は、質問が違う。','まず、目指すゴールを確認する。',
 '次に、今の数字を確かめる。','そして、理想との差を一つに絞る。',
 '原因には、なぜを三回重ねる。','対策は、今日できる行動に変える。',
 '結果を見て、また修正する。','小さな改善が、強いチームをつくる。']
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def rgb(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def font(sz,bold=True):return ImageFont.truetype(FONT if bold else FONT_REG,sz)
def rect(d,box,r,fill,outline=None,width=1):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def center(d,xy,text,f,fill,anchor='mm'):d.text(xy,text,font=f,fill=fill,anchor=anchor,stroke_width=0)
def line(d,pts,fill,width=8,joint='curve'):d.line(pts,fill=fill,width=width,joint=joint)
def shadow_box(im,box,r=34,fill='#FFFFFF',border='#DFE7E5'):
 layer=Image.new('RGBA',im.size,(0,0,0,0));q=ImageDraw.Draw(layer)
 q.rounded_rectangle((box[0]+2,box[1]+14,box[2]+2,box[3]+14),radius=r,fill=(19,51,60,34))
 im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(22)))
 d=ImageDraw.Draw(im);rect(d,box,r,fill,border,2)
 return d

def arrow(d,x1,y1,x2,y2,color,width=10):
 line(d,[(x1,y1),(x2,y2)],color,width)
 a=math.atan2(y2-y1,x2-x1);s=22
 d.polygon([(x2,y2),(x2-s*math.cos(a-.55),y2-s*math.sin(a-.55)),
 (x2-s*math.cos(a+.55),y2-s*math.sin(a+.55))],fill=color)

def diagram(im,i,accent):
 d=ImageDraw.Draw(im)
 ink='#143449';muted='#68818A';pale='#DDF6F0';gold='#F2B860'
 shadow_box(im,(64,482,1016,1130),r=46)
 d=ImageDraw.Draw(im)
 if i==0:
  d.ellipse((305,562,775,1032),fill='#E9F9F5',outline=accent,width=10)
  d.ellipse((358,615,722,979),outline='#B3DED6',width=5)
  center(d,(540,778),'?',font(265),accent)
  rect(d,(116,1052,964,1110),26,'#EFF7F5')
  center(d,(540,1080),'答えより、問いを磨く',font(39),ink)
 elif i==1:
  for radius,col,w in [(245,'#DCEEEA',11),(190,'#A8D8D0',11),(130,accent,15),(54,gold,0)]:
   d.ellipse((540-radius,795-radius,540+radius,795+radius),fill=col if w==0 else None,outline=col if w else None,width=w)
  arrow(d,232,1050,546,803,ink,15)
  center(d,(540,1080),'目標を言葉にする',font(39),ink)
 elif i==2:
  d.line((180,1020,890,1020),fill='#B9C9C9',width=6)
  vals=[210,290,360,455];labs=['1','2','3','4']
  for j,h in enumerate(vals):
   x=200+j*178;rect(d,(x,1007-h,x+114,1007),20,accent if j==3 else '#B4D8D4')
   center(d,(x+57,1047),labs[j],font(33),muted)
  center(d,(540,560),'いまの数字を見える化',font(42),ink)
 elif i==3:
  center(d,(200,655),'現状',font(40),ink)
  center(d,(820,655),'目標',font(40),ink)
  rect(d,(136,735,945,815),40,'#E3EEEC')
  rect(d,(136,735,560,815),40,accent)
  d.line((820,702,820,846),fill=gold,width=9)
  center(d,(540,925),'一番大きな差は？',font(57),ink)
  arrow(d,480,1010,655,1010,accent,9)
 elif i==4:
  for j in range(3):
   x=135+j*305
   d.ellipse((x,684,x+214,898),fill='#E9F7F4',outline=accent if j==2 else '#A6D8D1',width=7)
   center(d,(x+107,770),'なぜ？',font(41),ink)
   center(d,(x+107,839),f'{j+1}',font(37),accent)
   if j<2:arrow(d,x+225,791,x+291,791,gold,8)
  center(d,(540,1005),'原因の「奥」まで考える',font(43),ink)
 elif i==5:
  for j,(tag,label) in enumerate([('WHEN','今日'),('WHO','担当者'),('WHAT','行動')]):
   y=583+j*162
   rect(d,(130,y,947,y+131),25,'#EAF6F2')
   rect(d,(158,y+32,223,y+97),14,accent)
   center(d,(190,y+64),'✓',font(45),'#FFFFFF')
   center(d,(285,y+42),tag,font(25),muted,anchor='lm')
   center(d,(285,y+89),label,font(49),ink,anchor='lm')
 elif i==6:
  coords=[(540,630),(786,854),(540,1057),(294,854)]
  for j in range(4):
   x1,y1=coords[j];x2,y2=coords[(j+1)%4]
   arrow(d,x1+18,y1+18,x2-18,y2-18,gold,7)
  for (x,y),label in zip(coords,['実行','確認','修正','再挑戦']):
   d.ellipse((x-103,y-72,x+103,y+72),fill='#E8F7F2',outline=accent,width=6)
   center(d,(x,y),label,font(39),ink)
 elif i==7:
  pts=[(305,750),(520,622),(770,725),(690,970),(380,982)]
  for j,p in enumerate(pts):
   q=pts[(j+1)%len(pts)];line(d,[p,q],'#A2D6CC',10)
  for j,(x,y) in enumerate(pts):
   d.ellipse((x-60,y-60,x+60,y+60),fill=accent if j==0 else '#E3F4F0',outline=ink if j==0 else accent,width=5)
   center(d,(x,y),'人' if j==0 else '✓',font(40),'#FFFFFF' if j==0 else ink)
  center(d,(540,1080),'一人の改善が、チームへ',font(40),ink)

def draw_scene(i,genre,dest):
 accent=PALETTES[genre];ink='#143449'
 im=Image.new('RGBA',(W,H),'#F7F9F7')
 d=ImageDraw.Draw(im)
 for y in range(0,1160,55):d.line((0,y,W,y),fill='#F0F4F1',width=1)
 for x in range(0,W,55):d.line((x,0,x,1160),fill='#F0F4F1',width=1)
 d.ellipse((815,-170,1220,235),fill='#E4F3EE')
 d.ellipse((-180,940,215,1335),fill='#E7F3F1')
 rect(d,(64,72,405,132),25,ink)
 center(d,(235,102),'WORK SMARTER',font(31),'#FFFFFF')
 center(d,(940,100),f'{i+1:02} / 08',font(35),ink)
 rect(d,(64,154,1016,165),5,'#DDE9E5')
 rect(d,(64,154,64+int(952*(i+1)/8),165),5,accent)
 center(d,(70,245),HEADS[i][0],font(34),accent,anchor='lm')
 center(d,(70,340),HEADS[i][1],font(78),ink,anchor='lm')
 center(d,(70,423),HEADS[i][2],font(37,False),'#526C76',anchor='lm')
 diagram(im,i,accent)
 d=ImageDraw.Draw(im)
 rect(d,(0,1150,1079,1919),0,'#0A2132')
 d.line((64,1172,1016,1172),fill=accent,width=6)
 center(d,(78,1810),'小さな改善を、今日から。',font(29),'#8CA7B0',anchor='lm')
 im.convert('RGB').save(dest,optimize=True)

def create(root:Path,genre='sales_business'):
 if genre not in PALETTES:raise ValueError('unsupported genre')
 src=root/'source';src.mkdir(parents=True,exist_ok=True)
 for i in range(8):draw_scene(i,genre,src/f'scene_{i+1:02}.png')
 timing={'cycle':820,'genre':genre,'sentences':[{'scene':i+1,'text':SPEECH[i],
 'seconds':DURATIONS[i]} for i in range(8)],'voice_engine':'Open JTalk',
 'voice_model':'nitech_jp_atr503_m001.htsvoice',
 'rights_review_required':True,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
 (src/'voice_timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf8')
 (src/'asset_provenance.json').write_text(json.dumps({'images':'Original procedural Pillow graphics; no portraits, external imagery or personal data',
 'font':'System Noto Sans CJK JP, embedded only as rasterized glyphs',
 'genre':genre,'publication_approved':False},ensure_ascii=False,indent=2),encoding='utf8')
 return src
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
 p.add_argument('--genre',choices=sorted(PALETTES),default='sales_business')
 a=p.parse_args();print(create(a.root,a.genre))
