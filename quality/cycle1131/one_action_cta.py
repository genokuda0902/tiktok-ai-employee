"""Original 10-genre animated one-action CTA for scene 08. No third-party media."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=951,803
GENRE_DATA={
 'ai_work':('#58E5D8','毎週の集計','作業を1つ選ぶ','見本を用意する','指示を保存する'),
 'business':('#71B8FF','会議メモ','議題を1つ選ぶ','要点を整理する','書式を保存する'),
 'money':('#F6CA76','家計メモ','費目を1つ選ぶ','表で整理する','形式を保存する'),
 'learning':('#A4A1FF','復習ノート','テーマを1つ選ぶ','要点をまとめる','型を保存する'),
 'health':('#6FE5B4','生活記録','項目を1つ選ぶ','記録をまとめる','型を保存する'),
 'lifestyle':('#F5A5BF','買い物メモ','用件を1つ選ぶ','条件を整理する','型を保存する'),
 'psychology':('#CE9CF6','読書メモ','疑問を1つ選ぶ','要点を整理する','型を保存する'),
 'science':('#8FDDFB','実験メモ','条件を1つ選ぶ','結果を整理する','型を保存する'),
 'history':('#E4BA8C','年表メモ','時代を1つ選ぶ','出来事を整理する','型を保存する'),
 'travel':('#81D8D3','旅の準備','行き先を選ぶ','持ち物を整理する','型を保存する'),
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-'
def font(size,bold=False):return ImageFont.truetype(FONT+('Bold' if bold else 'Regular')+'.ttc',size)
def rgb(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def clamp(x):return max(0.,min(1.,x))
def ease(x):
 x=clamp(x);return x*x*(3-2*x)
def rr(d,b,r,fill,outline=None,width=1):d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=width)
def tx(d,x,y,s,size,color,bold=False):d.text((x,y),s,font=font(size,bold),fill=color)
def state_at(t):
 return sum(t>=v for v in (.18,.82,1.46))
def render_art(t,genre='ai_work'):
 if genre not in GENRE_DATA:raise ValueError('unsupported genre')
 accent_hex,subject,*steps=GENRE_DATA[genre];accent=rgb(accent_hex)
 im=Image.new('RGB',(W,H),(8,25,43));d=ImageDraw.Draw(im)
 rr(d,(1,1,W-2,H-2),32,(11,31,49),(52,98,116),3)
 light=Image.new('RGBA',(W,H),(0,0,0,0));ld=ImageDraw.Draw(light)
 ld.ellipse((420,-270,1130,470),fill=(*accent,65))
 im=Image.alpha_composite(im.convert('RGBA'),light.filter(ImageFilter.GaussianBlur(92))).convert('RGB')
 d=ImageDraw.Draw(im)
 rr(d,(31,29,413,94),18,(20,54,70),(67,111,124),2)
 tx(d,54,43,'STEP 08  /  START',26,accent,True)
 tx(d,690,46,'架空の例',25,(163,200,216),True)
 tx(d,45,120,'今日、1つだけ始めよう',47,(247,252,255),True)
 tx(d,47,187,'例：'+subject,30,(185,218,227))
 for i,(title,desc) in enumerate(zip(('選ぶ','試す','残す'),steps)):
  reveal=(.18,.82,1.46)[i]
  appear=ease((t-reveal)/.38)
  y=278+i*128
  if appear<=0:continue
  x=int(44+(1-appear)*60)
  active=i==min(2,max(0,state_at(t)-1))
  fill=(24,70,79) if active else (17,45,63)
  rr(d,(x,y,905,y+109),23,fill,accent if active else (47,83,99),3 if active else 2)
  rr(d,(x+20,y+19,x+88,y+87),17,accent if active else (33,75,88))
  tx(d,x+39,y+28,f'{i+1}',30,(8,29,41) if active else (190,226,236),True)
  tx(d,x+114,y+19,title,39,(251,255,255),True)
  tx(d,x+278,y+27,desc,31,(209,234,241))
  if t>reveal+.35:tx(d,x+810,y+31,'✓',33,accent,True)
 p=ease((t-1.90)/.58)
 if p>0:
  rr(d,(45,682,905,761),18,(24,75,81),accent,2)
  tx(d,85,695,'次回も使える形で残そう',34,(241,255,252),True)
  rr(d,(45,650,905,661),5,(28,60,78))
  rr(d,(45,650,45+int(860*p),661),5,accent)
 return im
