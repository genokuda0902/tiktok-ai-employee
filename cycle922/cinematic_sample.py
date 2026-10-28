"""cycle922: original, rights-safe cinematic paper-stack slide for scene 03.

Generates only local imagery; no accounts, real metrics, personal data or posting.
Target source region: scene03, frames 174..260, overlay at (0,315) size 1080x1130.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,N,START=540,565,87,174
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('週次報告',['今週の成果','気づき','次の行動'],'#0B8F8E'),
 'business':('営業メモ',['成果','改善点','次の行動'],'#186BA0'),
 'learning':('復習ノート',['学んだこと','理解度','次の課題'],'#6953BA'),
 'health':('体調記録',['体調','生活習慣','次の確認'],'#388466'),
 'beauty':('ケア記録',['ケア内容','気づき','次の予定'],'#A75584'),
 'travel':('旅程メモ',['行き先','移動','持ち物'],'#A56A2E'),
 'money':('家計メモ',['支出','振り返り','次の予算'],'#427C51'),
 'cooking':('献立メモ',['献立','材料','手順'],'#B16E34'),
 'pets':('お世話メモ',['体調','お世話','次の確認'],'#4B7897'),
 'entertainment':('企画メモ',['アイデア','準備','次の行動'],'#7957AD'),
}
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else REG,size)
def ease(t):
 t=max(0.,min(1.,t));return t*t*(3-2*t)
def text_width(s,size,bold=False):
 return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),s,font=font(size,bold))[2]
def validate_genres():
 assert len(GENRES)==10
 for name,(title,labels,color) in GENRES.items():
  assert len(labels)==3 and all(labels) and title
  assert text_width(title,38,True)<330,name
  assert all(text_width(v,25,True)<220 for v in labels),name
  assert color.startswith('#') and len(color)==7
 return True

def desk_background():
 rng=np.random.default_rng(922)
 yy,xx=np.mgrid[:H,:W];u=xx/W;v=yy/H
 grain=rng.normal(0,2.0,(H,W))
 wood=np.sin((xx*0.09)+(np.sin(yy*.018)*4))*2.2
 light=np.exp(-(((u-.18)/.7)**2+((v-.05)/.7)**2)*1.7)
 out=np.empty((H,W,3),dtype=np.uint8)
 for i,(base,glow) in enumerate([(41,30),(32,24),(27,17)]):
  out[:,:,i]=np.clip(base+glow*light+grain+wood,0,255)
 im=Image.fromarray(out,'RGB').convert('RGBA')
 light_layer=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(light_layer)
 for k in range(4):
  x=-100+k*180;d.polygon([(x,0),(x+75,0),(x+260,H),(x+180,H)],fill=(248,211,154,12))
 im=Image.alpha_composite(im,light_layer.filter(ImageFilter.GaussianBlur(23)))
 return im

def sheet(title,labels,accent,beat,phase):
 paper=Image.new('RGBA',(420,445),(0,0,0,0));d=ImageDraw.Draw(paper)
 d.rounded_rectangle((8,7,410,439),radius=11,fill=(247,246,239,255),outline=(218,214,203,255),width=2)
 texture=Image.new('RGBA',paper.size,(0,0,0,0));td=ImageDraw.Draw(texture)
 for y in range(14,431,8):td.line((12,y,407,y),fill=(134,115,94,6),width=1)
 paper=Image.alpha_composite(paper,texture);d=ImageDraw.Draw(paper)
 d.rounded_rectangle((33,28,184,57),7,fill=(222,235,231,255))
 d.text((45,34),'SAMPLE / ORIGINAL',font=font(12,True),fill=(38,95,94,255))
 d.text((34,82),title,font=font(38,True),fill=(33,45,47,255))
 d.line((34,137,378,137),fill=(185,190,185,255),width=2)
 d.text((35,151),'完成形を先に決める',font=font(18,True),fill=(61,71,70,255))
 for k,label in enumerate(labels):
  y=197+k*74
  active=k==beat
  if active:
   d.rounded_rectangle((27,y-7,390,y+63),radius=12,fill=(224,242,237,255),outline=accent,width=3)
  else:
   d.rounded_rectangle((29,y-5,389,y+61),radius=10,fill=(255,255,253,255),outline=(215,217,212,255),width=1)
  d.rounded_rectangle((43,y+4,75,y+36),radius=8,fill=accent if active else (225,230,224,255))
  d.text((54,y+8),str(k+1),font=font(15,True),fill='white' if active else (90,100,98,255))
  d.text((88,y+4),label,font=font(25,True),fill=(28,50,49,255))
  d.line((89,y+44,352,y+44),fill=(196,201,195,255),width=2)
  if active:
   length=int(258*ease(phase))
   d.line((89,y+48,89+length,y+48),fill=accent,width=4)
 d.text((35,418),'※架空の記入例｜数字・個人情報なし',font=font(11),fill=(120,122,113,255))
 return paper

def draw_frame(i,genre='ai_work'):
 if genre not in GENRES:raise ValueError('unknown genre')
 if not 0<=i<N:raise ValueError('invalid frame')
 title,labels,accent=GENRES[genre]
 beat=min(2,i//29);phase=(i%29)/28
 im=desk_background()
 layer=Image.new('RGBA',(W,H),(0,0,0,0));ld=ImageDraw.Draw(layer)
 ld.rounded_rectangle((91,34,481,481),radius=12,fill=(225,222,211,255))
 layer=layer.rotate(-4,resample=Image.Resampling.BICUBIC,expand=False)
 im=Image.alpha_composite(im,layer)
 shadow=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(shadow)
 sd.rounded_rectangle((83,31,483,483),radius=14,fill=(0,0,0,135))
 im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(19)))
 sheet_img=sheet(title,labels,accent,beat,phase)
 x=53+int(3*math.sin(i/N*math.pi));y=14+int(4*math.sin(i/N*math.pi))
 im.alpha_composite(sheet_img,(x,y))
 glow=Image.new('RGBA',(W,H),(0,0,0,0));gd=ImageDraw.Draw(glow)
 center=-70+int(600*i/(N-1))
 gd.polygon([(center-40,0),(center+12,0),(center+155,H),(center+105,H)],fill=(255,229,187,15))
 im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(20)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,13,156,42),radius=11,fill=(7,31,35,220))
 d.text((25,20),'EXAMPLE / 03',font=font(13,True),fill=(198,241,233,255))
 return im.convert('RGB')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--genre',default='ai_work');ap.add_argument('--preview-only',action='store_true');a=ap.parse_args()
 validate_genres();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 ids=[4,42,75] if a.preview_only else range(N)
 for i in ids:draw_frame(i,a.genre).save(out/f'frame_{START+i:04d}.png',compress_level=3)
 print('rendered',len(ids),'frames')
if __name__=='__main__':main()
