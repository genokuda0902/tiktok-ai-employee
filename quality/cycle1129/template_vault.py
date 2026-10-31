"""Original 10-genre kinetic template-vault illustration for scene 07.
No external media, logos, personal data, publishing or auto-posting.
All example data are fictional. PUBLICATION_NOT_APPROVED.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W,H=951,803
GENRE_DATA={
 'ai_work':('#58E5D8','週次報告','数字と根拠を含める'),
 'business':('#71B8FF','会議メモ','決定事項を整理'),
 'money':('#F6CA76','家計メモ','費目を分けて整理'),
 'learning':('#A4A1FF','復習ノート','重要語句を3点に'),
 'health':('#6FE5B4','生活メモ','観察事項を整理'),
 'lifestyle':('#F5A5BF','買い物リスト','優先度を付ける'),
 'psychology':('#CE9CF6','読書メモ','要点を整理'),
 'science':('#8FDDFB','実験メモ','条件を記録'),
 'history':('#E4BA8C','年表メモ','年代順に並べる'),
 'travel':('#81D8D3','旅の持ち物','忘れ物を確認'),
}
FONT_DIR='/usr/share/fonts/opentype/noto/'
def font(n,bold=False):
 return ImageFont.truetype(FONT_DIR+('NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'),n)
def rgb(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def mix(a,b,f):return tuple(int(a[i]*(1-f)+b[i]*f) for i in range(3))
def clamp(v):return max(0.,min(1.,v))
def ease(v):
 t=clamp(v);return t*t*(3-2*t)
def rr(d,box,r,fill,outline=None,width=1):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def tx(d,x,y,s,n,c,bold=False):d.text((x,y),s,font=font(n,bold),fill=c)

def render_art(t,genre='ai_work'):
 """Return deterministic original 951x803 RGB frame for scene-07 local time t."""
 if genre not in GENRE_DATA:raise ValueError('unsupported genre')
 accent_hex,name,detail=GENRE_DATA[genre];accent=rgb(accent_hex)
 im=Image.new('RGB',(W,H),(7,23,41));d=ImageDraw.Draw(im)
 rr(d,(1,1,W-2,H-2),32,(10,30,49),(52,98,116),3)
 light=Image.new('RGBA',(W,H),(0,0,0,0));ld=ImageDraw.Draw(light)
 ld.ellipse((220,-260,1110,610),fill=(*accent,72))
 im=Image.alpha_composite(im.convert('RGBA'),light.filter(ImageFilter.GaussianBlur(105))).convert('RGB');d=ImageDraw.Draw(im)
 rr(d,(33,29,424,94),17,(22,57,74),(66,113,129),2)
 tx(d,55,42,'STEP 07  /  SAVE',27,accent,True)
 tx(d,690,44,'実演・架空例',23,(170,204,218),True)
 tx(d,47,122,'使える指示は「保存」して再利用',38,(245,251,255),True)
 rr(d,(42,218,491,589),24,(18,43,62),(69,102,121),3)
 rr(d,(43,219,490,283),22,(32,61,80))
 d.rectangle((43,258,490,283),fill=(32,61,80))
 for i,c in enumerate(((250,130,130),(246,198,111),(121,208,164))):d.ellipse((66+i*31,241,79+i*31,254),fill=c)
 tx(d,178,232,'指示エディター',25,(231,246,250),True)
 rr(d,(69,317,461,548),17,(11,30,49),(56,93,111),2)
 tx(d,90,342,'目的',25,accent,True)
 tx(d,166,341,name,32,(246,252,254),True)
 d.line((91,402,434,402),fill=(44,77,95),width=2)
 tx(d,90,423,'条件',25,accent,True)
 tx(d,166,421,detail,27,(228,244,247),True)
 tx(d,90,488,'形式',25,accent,True)
 tx(d,166,485,'3つの箇条書き',27,(228,244,247),True)
 rr(d,(544,218,908,589),24,(17,45,64),(67,107,121),3)
 rr(d,(566,241,884,315),18,(33,69,85))
 tx(d,585,256,'保存ライブラリ',29,(248,252,254),True)
 for i,(label,kind) in enumerate([('01','保存済み'),('02','保存済み'),('03','今回追加')]):
  y=345+i*70
  rr(d,(566,y,885,y+59),13,(24,60,76) if i<2 else (19,53,69),(48,86,102),2)
  tx(d,584,y+11,label,23,(144,183,199),True)
  tx(d,648,y+11,kind,25,(208,228,237),True)
 p=ease((t-.45)/.85)
 bx=int(434+330*p);by=int(554-110*math.sin(math.pi*p))
 if .45<=t<1.45:
  rr(d,(bx-72,by-38,bx+72,by+38),14,(39,112,115),accent,3)
  tx(d,bx-54,by-19,'指示文',27,(250,255,254),True)
 d.line((502,395,534,395),fill=accent,width=5)
 d.polygon(((528,385),(542,395),(528,405)),fill=accent)
 done=ease((t-1.43)/.28)
 if done>0:
  rr(d,(567,485,884,563),14,mix((25,60,76),(29,101,94),done),mix((56,94,107),accent,done),3)
  tx(d,584,505,'✓',31,accent,True)
  tx(d,640,507,'テンプレ保存',25,(241,254,250),True)
 rr(d,(45,640,906,747),22,(15,47,64),(53,97,110),2)
 if t<1.43:tx(d,79,669,'① 目的・条件・形式をまとめる',33,(241,250,252),True)
 else:tx(d,79,669,'② 次回は保存した指示から始める',33,(241,250,252),True)
 rr(d,(47,766,905,777),5,(25,63,78))
 rr(d,(47,766,47+int(858*clamp(t/2.54)),777),5,accent)
 return im
