"""cycle941: three-shot template reuse scene, review-only; synthetic UI, no posting."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,TOTAL=1080,1920,30,691
START,COUNT,SAFE_Y=522,65,1440
POLICY='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('AI仕事術',('営業','採用','事務')),
 'business':('業務改善',('報告','会議','営業')),
 'finance':('お金の管理',('収入','支出','予算')),
 'education':('学習効率',('復習','予習','要約')),
 'health':('健康習慣',('食事','運動','睡眠')),
 'beauty':('美容管理',('肌','髪','習慣')),
 'food':('料理の段取り',('献立','買物','調理')),
 'travel':('旅の計画',('移動','宿泊','観光')),
 'lifestyle':('暮らしの改善',('掃除','家事','整理')),
 'technology':('技術の活用',('設計','検証','記録')),
}

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def guard(genre,expected):
 if genre not in GENRES or len(GENRES)!=10:raise ValueError('invalid genre')
 if not isinstance(expected,str) or len(expected)!=64 or any(c not in '0123456789abcdef' for c in expected):raise ValueError('full pinned lowercase sha256 required')
 if not (START==522 and COUNT==65 and SAFE_Y<=1440 and 'NOT_APPROVED' in POLICY):raise RuntimeError('unsafe timing/policy')
 if not (Path(FONT).is_file() and Path(BOLD).is_file()):raise FileNotFoundError('Noto CJK required')

def phase(i):
 if not 0<=i<COUNT:raise ValueError('frame out of range')
 return 0 if i<22 else (1 if i<44 else 2)

@lru_cache(maxsize=20)
def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)

@lru_cache(maxsize=1)
def backdrop():
 im=Image.new('RGB',(W,SAFE_Y));p=im.load()
 for y in range(SAFE_Y):
  for x in range(W):p[x,y]=(int(7+10*y/SAFE_Y),int(24+15*x/W),int(42+19*y/SAFE_Y))
 glow=Image.new('RGBA',(W,SAFE_Y));g=ImageDraw.Draw(glow)
 g.ellipse((-400,-450,600,600),fill=(33,203,202,115))
 g.ellipse((550,550,1480,1500),fill=(41,109,219,95))
 return Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(150))).convert('RGB')

def card(draw,xy,fill,outline='#43798A',r=24,width=2):draw.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)

def txt(draw,xy,s,n=38,color='#FFFFFF',bold=False):draw.text(xy,s,font=font(n,bold),fill=color)

def frame(i,genre='ai_work'):
 if genre not in GENRES:raise ValueError('invalid genre')
 p=phase(i); title,tasks=GENRES[genre]
 im=backdrop().copy();d=ImageDraw.Draw(im)
 card(d,(43,46,1037,142),'#12394B','#3BB3B8',22,3)
 txt(d,(70,69),f'{title}  /  REUSE',43,'#F3FFFF',True)
 txt(d,(57,187),'一度つくった指示を、何度も使う',51,'#FFFFFF',True)
 txt(d,(58,264),'架空のテンプレート例・実アプリ操作ではありません',27,'#B7D4DC')
 # Native-resolution type and distinct compositions across the three micro-shots.
 if p==0:
  card(d,(72,359,1008,1134),'#EAF5F5','#84D6D4',34,4)
  card(d,(98,383,981,483),'#164A5D','#164A5D',22)
  txt(d,(131,405),'① 使える「型」を保存',49,'#FFFFFF',True)
  for j,(a,b) in enumerate([('目的','何をしたい？'),('条件','何を守る？'),('出力','どんな形？')]):
   y=522+j*176
   card(d,(110,y,969,y+149),'#FFFFFF','#D2E4E8',20,2)
   card(d,(135,y+25,295,y+118),'#C9F1EA','#C9F1EA',17)
   txt(d,(161,y+44),a,41,'#15505A',True)
   txt(d,(332,y+43),b,44,'#173E50',True)
  caption='まず、目的・条件・出力を固定'
 elif p==1:
  txt(d,(82,347),'② 同じ型を、別の仕事に展開',47,'#7DF1DF',True)
  for j,t in enumerate(tasks):
   y=452+j*237
   card(d,(83,y,1000,y+206),'#F0F7F8','#A2D8DB',30,4)
   card(d,(109,y+24,286,y+182),'#174A61','#174A61',24)
   txt(d,(150,y+73),f'{j+1:02}',54,'#91F0DF',True)
   txt(d,(334,y+36),t,55,'#183B4B',True)
   txt(d,(334,y+111),'同じ指示の型を再利用',35,'#476B77')
  caption='3つの用途へ、同じ型を再利用'
 else:
  card(d,(80,390,1000,1040),'#F0F8F8','#8AD9D7',35,4)
  card(d,(107,419,972,542),'#174F61','#174F61',22)
  txt(d,(138,447),'③ 人が確認して再利用',49,'#FFFFFF',True)
  for j,s in enumerate(['元データと照合','用途に合わせて調整','確認後に手動で使う']):
   y=595+j*137
   card(d,(125,y,955,y+112),'#FFFFFF','#D2E7E9',20,2)
   txt(d,(151,y+25),f'{j+1}',43,'#129F99',True)
   txt(d,(235,y+23),s,43,'#1B4655',True)
  caption='保存した型も、毎回人が確認'
 card(d,(67,1180,1013,1349),'#0F5061','#65C8C4',25,3)
 txt(d,(101,1214),caption,43,'#FFFFFF',True)
 txt(d,(104,1286),'架空デモ / 社員未承認 / 手動投稿のみ',27,'#D0E9EA')
 for j in range(3):card(d,(373+j*112,1394,457+j*112,1410),'#76EAD6' if j==p else '#325B69','#76EAD6' if j==p else '#325B69',8,1)
 return im

def render(source,output,tmp,genre,expected):
 guard(genre,expected)
 source=Path(source);output=Path(output);tmp=Path(tmp)
 if not source.is_file():raise FileNotFoundError(source)
 if source.resolve()==output.resolve():raise ValueError('source overwrite blocked')
 if sha(source)!=expected:raise RuntimeError('FAIL_CLOSED_SOURCE_SHA_MISMATCH')
 output.parent.mkdir(parents=True,exist_ok=True)
 seq=tmp/'overlays';seq.mkdir(parents=True,exist_ok=True)
 for i in range(COUNT):frame(i,genre).save(seq/f'{i:03d}.png',compress_level=1)
 graph=f"[1:v]setpts=PTS+{START}/{FPS}/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:enable='between(n,{START},{START+COUNT-1})'[v]"
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate',str(FPS),'-start_number','0','-i',str(seq/'%03d.png'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',str(output)]
 p=subprocess.run(cmd,capture_output=True,text=True)
 (tmp/'ffmpeg.log').write_text(p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError('ffmpeg failed: '+p.stderr[-1000:])
 result={'policy':POLICY,'source_sha256':expected,'output_sha256':sha(output),'changed_scene':[START,START+COUNT-1],'genre':genre,'genre_profiles':len(GENRES),'publication_allowed':False,'original_reference_parity':'NOT_VERIFIED','independent_japanese_asr':'NOT_VERIFIED'}
 (tmp/'render.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser()
 for name in ['source','output','tmp','expected-source-sha']:a.add_argument('--'+name,required=True)
 a.add_argument('--genre',choices=GENRES,default='ai_work')
 x=a.parse_args()
 print(json.dumps(render(x.source,x.output,x.tmp,x.genre,x.expected_source_sha),ensure_ascii=False))
