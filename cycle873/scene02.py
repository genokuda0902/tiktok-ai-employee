"""Cycle873: legible motion scene for ten genres. REVIEW ONLY; private media never committed."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W,H,FPS,FRAMES=1080,1920,30,691
START,COUNT,TOP,BOTTOM=90,80,132,1490
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES={
 'ai_work':('繰り返し作業を','見つける',('月別データの集計','同じ表を毎週更新','転記と数字の照合')),
 'trivia':('知りたい疑問を','書き出す',('気になる事実','根拠を確認','出典をメモ')),
 'cooking':('料理の手順を','整理する',('材料をそろえる','下準備を分ける','加熱時間を確認')),
 'beauty':('毎日のケアを','見直す',('今の習慣を記録','使ったものを整理','変化を振り返る')),
 'money':('家計の支出を','整理する',('毎月の固定費','変動費の記録','合計を確認')),
 'wellness':('小さな習慣を','記録する',('睡眠時間を記録','運動を振り返る','無理なく継続')),
 'travel':('旅の予定を','組み立てる',('移動時間を確認','訪問先を整理','予備時間を確保')),
 'product':('比較する条件を','そろえる',('必要な機能','予算の範囲','購入前に確認')),
 'story':('物語の流れを','組み立てる',('始まりの出来事','登場人物の選択','結末を考える')),
 'business':('日々の仕事を','棚卸しする',('反復業務を探す','時間の使い方','改善案を記録')),
}
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

@lru_cache(maxsize=30)
def font(size,bold=True):
 return ImageFont.truetype(FONT if bold else FONT_REG,size)

def text_fits(text,size,width):
 b=ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),text,font=font(size))
 return b[2]-b[0]<=width

def validate(genre,photo):
 if genre not in GENRES:raise ValueError('unknown genre')
 if photo.mode not in ('RGB','RGBA') or min(photo.size)<850:raise ValueError('photo rejected')
 a,b,rows=GENRES[genre]
 if len(rows)!=3:raise ValueError('expected 3 steps')
 if not all(text_fits(t,s,w) for t,s,w in [(a,74,950),(b,87,950),*[(r,47,740) for r in rows]]):
  raise ValueError('text overflow')

def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)

def make_frame(bg,frame,genre='ai_work'):
 if not 0<=frame<COUNT:raise ValueError('frame outside target')
 a,b,rows=GENRES[genre]
 im=bg.copy().convert('RGBA'); d=ImageDraw.Draw(im,'RGBA')
 # All artwork is constrained to y=132..1490 of the full frame.
 d.rounded_rectangle((66,47,440,113),radius=21,fill=(5,47,66,235),outline=(84,220,234,170),width=2)
 d.text((93,61),'STEP 01  /  発見',font=font(32),fill=(230,251,255))
 d.text((65,155),a,font=font(74),fill=(250,252,255))
 d.text((65,252),b,font=font(87),fill=(255,214,130))
 d.rounded_rectangle((64,410,1016,1137),radius=28,fill=(6,21,36,242),outline=(80,183,209,220),width=3)
 d.text((100,443),'作業の棚卸し  /  例',font=font(39),fill=(219,246,250))
 for i,txt in enumerate(rows):
  y=535+i*176
  active=frame>=12+i*18
  d.rounded_rectangle((98,y,982,y+137),radius=18,fill=(15,67,83,238) if active else (24,45,58,230),outline=(79,192,210,190) if active else (66,89,103,180),width=2)
  d.rounded_rectangle((121,y+37,181,y+97),radius=12,fill=(33,175,181,240) if active else (45,70,83,255))
  d.text((136,y+42),str(i+1),font=font(36),fill=(255,255,255))
  d.text((213,y+37),txt,font=font(47),fill=(255,255,255) if active else (151,169,177))
 d.rounded_rectangle((65,1170,1016,1304),radius=24,fill=(6,53,71,238),outline=(86,207,225,190),width=2)
 d.text((101,1201),'まずは1つ、書き出そう',font=font(50),fill=(249,252,255))
 d.rounded_rectangle((68,1330,1016,1345),radius=7,fill=(48,82,96,230))
 d.rounded_rectangle((68,1330,68+round(948*smooth((frame+1)/COUNT)),1345),radius=7,fill=(82,227,233,255))
 return im.convert('RGB')

def render(old,photo,out,manifest,genre='ai_work'):
 old,photo,out=map(Path,(old,photo,out))
 if out.exists():raise ValueError('refuse overwrite')
 if not old.is_file() or not photo.is_file():raise FileNotFoundError('missing private input')
 if manifest!={**POLICY,'source_sha256':sha(old),'photo_sha256':sha(photo)}:raise ValueError('fail closed manifest')
 with Image.open(photo) as p: pic=p.copy()
 validate(genre,pic)
 ht=BOTTOM-TOP
 # Blur background once; animate foreground cards to reduce motion clutter.
 ratio=max(W/pic.width,ht/pic.height)
 size=(round(pic.width*ratio),round(pic.height*ratio))
 base=ImageEnhance.Color(pic.convert('RGB')).enhance(.7).resize(size,Image.Resampling.LANCZOS)
 x=max(0,(base.width-W)//2);y=max(0,(base.height-ht)//2)
 base=base.crop((x,y,x+W,y+ht)).filter(ImageFilter.GaussianBlur(5)).convert('RGBA')
 base=Image.alpha_composite(base,Image.new('RGBA',(W,ht),(1,13,26,178))).convert('RGB')
 with tempfile.TemporaryDirectory(prefix='cycle873_') as td:
  for i in range(COUNT):make_frame(base,i,genre).save(Path(td)/f'{i:03}.png')
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[overlay];'
        f"[0:v][overlay]overlay=x=0:y={TOP}:enable='between(n,{START},{START+COUNT-1})':"
        'eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(old),'-framerate','30','-i',str(Path(td)/'%03d.png'),'-filter_complex',filt,
       '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(out)]
  subprocess.run(cmd,check=True,timeout=300)
 return {'old_sha256':sha(old),'new_sha256':sha(out),'changed_frames':COUNT,'start_frame':START,'genres_supported':len(GENRES),'policy':POLICY}

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for name in ('source','photo','output','manifest','report'):ap.add_argument('--'+name,required=True)
 ap.add_argument('--genre',default='ai_work');a=ap.parse_args()
 data=render(a.source,a.photo,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
 Path(a.report).write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps(data,ensure_ascii=False))
