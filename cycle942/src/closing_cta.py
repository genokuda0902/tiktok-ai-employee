"""cycle942: rights-safe, caption-protected cinematic end-card, review only.

Reimplementation over a PRIVATE review source. No video/audio bytes are committed.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,TOTAL=1080,1920,30,691
START,COUNT,SAFE_Y=609,82,1400
POLICY='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# Genre-specific next-action examples, not a generic copy-and-paste claim.
GENRES={
 'ai_work':('AI仕事術','作業を1つ選ぶ','元データと照合','AIは下書き、人が確認'),
 'business':('業務改善','業務を1つ選ぶ','手順と結果を確認','成果を誇張しない'),
 'finance':('家計の見直し','支出を1つ選ぶ','金額と条件を確認','数字は必ず再確認'),
 'education':('学習効率','学習を1つ選ぶ','理解できたか確認','自分の言葉で復習'),
 'health':('健康習慣','習慣を1つ選ぶ','無理のない範囲で','体調に合わせて調整'),
 'beauty':('美容習慣','ケアを1つ選ぶ','肌の様子を確認','無理せず続ける'),
 'food':('料理の段取り','献立を1つ選ぶ','食材と手順を確認','衛生と加熱を確認'),
 'travel':('旅の計画','行き先を1つ選ぶ','移動と予約を確認','最新情報を確認'),
 'lifestyle':('暮らしの工夫','家事を1つ選ぶ','自分に合うか確認','小さく試してみる'),
 'technology':('技術の活用','課題を1つ選ぶ','結果をテスト','公開前に人が確認'),
}

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()

def guard(genre,expected):
 if genre not in GENRES or len(GENRES)!=10:raise ValueError('unknown genre')
 if not isinstance(expected,str) or len(expected)!=64 or any(c not in '0123456789abcdef' for c in expected):raise ValueError('pin full lowercase source sha256')
 if START!=609 or COUNT!=82 or START+COUNT!=TOTAL or SAFE_Y>1400:raise RuntimeError('unsafe scene geometry')
 if not POLICY.endswith('PUBLICATION_NOT_APPROVED'):raise RuntimeError('publication gate missing')
 for p in (FONT,BOLD):
  if not Path(p).is_file():raise FileNotFoundError(p)

def phase(i):
 if not 0<=i<COUNT:raise ValueError('frame out of range')
 return 0 if i<27 else 1 if i<54 else 2

@lru_cache(maxsize=32)
def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)

@lru_cache(maxsize=1)
def base():
 y=np.linspace(0,1,SAFE_Y,dtype=np.float32)[:,None]
 x=np.linspace(0,1,W,dtype=np.float32)[None,:]
 a=np.empty((SAFE_Y,W,3),dtype=np.uint8)
 a[:,:,0]=np.clip(5+13*y+5*x,0,255)
 a[:,:,1]=np.clip(20+16*y+13*x,0,255)
 a[:,:,2]=np.clip(41+20*y+13*x,0,255)
 im=Image.fromarray(a,'RGB').convert('RGBA')
 glow=Image.new('RGBA',(W,SAFE_Y));d=ImageDraw.Draw(glow)
 d.ellipse((-400,-320,610,730),fill=(22,193,224,128))
 d.ellipse((570,520,1510,1560),fill=(85,86,222,105))
 return Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(170))).convert('RGB')

def rect(d,xy,fill,outline=None,r=24,width=2):
 d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)

def txt(d,xy,s,n=42,color='#F4FBFF',bold=False):d.text(xy,s,font=font(n,bold),fill=color)

def frame(i,genre='ai_work'):
 if genre not in GENRES:raise ValueError('unknown genre')
 p=phase(i); local=i-(0 if p==0 else 27 if p==1 else 54)
 label,action,check,principle=GENRES[genre]
 im=base().copy();d=ImageDraw.Draw(im)
 # Fixed brand and visual hierarchy; deliberately below 1400px to preserve burned captions.
 rect(d,(52,60,1028,158),'#11344D','#3A7B94',22,3)
 txt(d,(83,84),f'{label}  /  TODAY',42,'#E7FCFF',True)
 txt(d,(70,215),'小さな時短を、毎日の習慣に。',51,'#FFFFFF',True)
 txt(d,(74,300),'1つ試して、確かめて、次につなげる',31,'#A9D6E5')
 if p==0:
  rect(d,(83,407,998,1113),'#F1F8FB','#78C5DC',38,4)
  rect(d,(111,440,971,563),'#153D5B',r=24)
  txt(d,(144,467),'01  今日の1歩',53,'#FFFFFF',True)
  txt(d,(147,624),action,64,'#173E55',True)
  txt(d,(147,750),'「全部やる」より、まず1つ。',38,'#456C7D')
  rect(d,(146,890,928,1009),'#D8F4F1',r=24)
  txt(d,(175,924),'試すことを決めたら、次へ',39,'#14645E',True)
 elif p==1:
  rect(d,(83,407,998,1113),'#F1F8FB','#78C5DC',38,4)
  rect(d,(111,440,971,563),'#153D5B',r=24)
  txt(d,(144,467),'02  確認する',53,'#FFFFFF',True)
  txt(d,(147,623),check,59,'#173E55',True)
  txt(d,(147,754),principle,38,'#456C7D')
  rect(d,(145,888,932,1007),'#FCE9D4',r=24)
  txt(d,(173,922),'自動投稿・自動承認はしません',36,'#8B5624',True)
 else:
  rect(d,(75,388,1005,1158),'#0D324B','#54A6C0',36,4)
  rect(d,(111,438,970,594),'#0B5367','#50D7D1',25,3)
  txt(d,(149,478),'03  あとで見返すなら',49,'#D9FFFB',True)
  # More cinematic high-contrast CTA; it is a prompt, NOT a functional button.
  rect(d,(128,665,952,856),'#FFE8B4','#FFE8B4',34,2)
  txt(d,(219,713),'保 存 し て お く',62,'#183D51',True)
  txt(d,(169,916),'役立つかどうかは、実際に確認。',37,'#E5F5F7')
  txt(d,(169,985),'誇張した成果・自動化は約束しません',30,'#B3D1D9')
 # Persistent release status; never hidden by the animation.
 rect(d,(83,1190,997,1316),'#6D233B','#EF8092',24,3)
 txt(d,(117,1215),'未承認  /  社員確認後に手動投稿',39,'#FFFFFF',True)
 for j in range(3):
  rect(d,(375+j*112,1354,451+j*112,1371),'#6CE7D7' if j==p else '#365D70',r=8)
 # Animated slim timeline changes on every frame, while typography stays still.
 d.rounded_rectangle((72,352,72+int(934*(i+1)/COUNT),360),radius=4,fill='#75EEE2')
 return im

def render(source,output,tmp,genre,expected):
 guard(genre,expected)
 source,output,tmp=Path(source),Path(output),Path(tmp)
 if not source.is_file():raise FileNotFoundError(source)
 if source.resolve()==output.resolve():raise ValueError('source overwrite forbidden')
 if sha(source)!=expected:raise RuntimeError('FAIL_CLOSED_SOURCE_SHA_MISMATCH')
 output.parent.mkdir(parents=True,exist_ok=True)
 seq=tmp/'frames';seq.mkdir(parents=True,exist_ok=True)
 for i in range(COUNT):frame(i,genre).save(seq/f'{i:03d}.png',compress_level=1)
 graph=f"[1:v]setpts=PTS+{START}/{FPS}/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:enable='between(n,{START},{START+COUNT-1})'[v]"
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate',str(FPS),'-start_number','0','-i',str(seq/'%03d.png'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',str(output)]
 p=subprocess.run(cmd,capture_output=True,text=True)
 (tmp/'ffmpeg.log').write_text(' '.join(cmd)+'\n'+p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError('ffmpeg failed: '+p.stderr[-1500:])
 result={'policy':POLICY,'source_sha256':expected,'output_sha256':sha(output),'changed_frames':[START,TOTAL-1],'genre':genre,'genre_profiles':len(GENRES),'source_assets_publication_approved':False,'independent_japanese_asr':'NOT_VERIFIED','publication_allowed':False}
 (tmp/'render.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser()
 for n in ('source','output','tmp','expected-source-sha'):a.add_argument('--'+n,required=True)
 a.add_argument('--genre',choices=GENRES,default='ai_work')
 x=a.parse_args()
 print(json.dumps(render(x.source,x.output,x.tmp,x.genre,x.expected_source_sha),ensure_ascii=False))
