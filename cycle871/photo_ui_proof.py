"""Review-only photo + actual local-browser screenshot compositing.

Synthetic, offline demo; no brand imitation, no private media upload, no posting.
Requires an explicit review-only SHA-pinned manifest for real MP4 rendering.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H, FPS, N = 1080, 1920, 30, 691
START, COUNT = 510, 78
TOP, BOTTOM = 132, 1490
GENRES = {
 'ai_work': ('使える指示は、資産になる', '指示を保存'),
 'sales_business': ('提案の型を、チームの資産に', '提案を保存'),
 'beauty': ('続くケアを、記録に残す', '手順を保存'),
 'romance': ('大切な言葉を、整理する', '会話を保存'),
 'saving': ('家計のルールを、見える化', '予算を保存'),
 'career': ('学びを、次の行動に', '計画を保存'),
 'wellness': ('小さな習慣を、記録する', '習慣を保存'),
 'science': ('仮説と根拠を、残しておく', '仮説を保存'),
 'travel_food': ('旅の準備を、ひとまとめ', '計画を保存'),
 'product_comparison_lifestyle': ('選ぶ条件を、整理する', '比較を保存'),
}
POLICY = {'review_only': True, 'publication_approved': False,
          'automatic_posting': False, 'external_upload': False,
          'source_rights_reviewed': False, 'offline_synthetic_demo': True}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha(path):
 h = hashlib.sha256()
 with open(path, 'rb') as f:
  for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
 return h.hexdigest()

@lru_cache(maxsize=8)
def font(size): return ImageFont.truetype(FONT, size)

def fit_text(text, max_width, size):
 f = font(size)
 if ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),text,font=f)[2] > max_width:
  raise ValueError('text clipping risk: '+text)
 return f

def check_inputs(genre, photo, ui_frames):
 if genre not in GENRES: raise ValueError('unknown genre')
 if photo.mode not in ('RGB','RGBA') or min(photo.size) < 850: raise ValueError('photo too small')
 if len(ui_frames) != 26: raise ValueError('26 offline browser frames required')
 if any(f.size != (900,560) or f.mode not in ('RGB','RGBA') for f in ui_frames):
  raise ValueError('browser screenshot dimensions invalid')

def draw_frame(photo, ui_frames, frame, genre='ai_work'):
 check_inputs(genre, photo, ui_frames)
 if not 0 <= frame < COUNT: raise ValueError('frame out of range')
 p = frame / (COUNT-1)
 ease = p*p*(3-2*p)
 height = BOTTOM-TOP
 scale = max(W/photo.width, height/photo.height)*(1.02+.04*ease)
 nw,nh = math.ceil(photo.width*scale),math.ceil(photo.height*scale)
 im = ImageEnhance.Contrast(photo.convert('RGB')).enhance(1.06).resize((nw,nh),Image.Resampling.LANCZOS)
 sx,sy=nw-W,nh-height
 im = im.crop((round(sx*(.48+.05*ease)),round(sy*.52),round(sx*(.48+.05*ease))+W,round(sy*.52)+height)).convert('RGBA')
 shade=Image.new('RGBA',(W,height),(0,0,0,0))
 d=ImageDraw.Draw(shade,'RGBA')
 d.rounded_rectangle((40,65,1040,320),radius=35,fill=(5,20,35,222),outline=(98,223,244,200),width=3)
 title,action=GENRES[genre]
 d.text((82,106),title,font=fit_text(title,900,53),fill='white')
 d.text((83,213),'写真の質感 × 操作の証拠',font=font(30),fill=(151,230,255))
 d.rounded_rectangle((41,493,1039,1183),radius=30,fill=(4,16,31,242),outline=(124,219,244,255),width=3)
 d.text((84,518),'OFFLINE DEMO  /  架空データ',font=font(27),fill=(145,226,255))
 if frame >= 57:
  d.rounded_rectangle((654,1202,1038,1293),radius=21,fill=(5,72,71,240),outline=(135,249,211),width=2)
  d.text((684,1220),action+' ✓',font=fit_text(action+' ✓',340,37),fill='white')
 im=Image.alpha_composite(im,shade)
 # Browser screenshots come from a real headless Chromium page with synthetic values.
 shot=ui_frames[min(25,frame//3)].convert('RGB').resize((920,572),Image.Resampling.LANCZOS)
 im.paste(shot,(80,584))
 return im.convert('RGB')

def probe(path):
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
 v=next(s for s in info['streams'] if s['codec_type']=='video')
 a=next(s for s in info['streams'] if s['codec_type']=='audio')
 if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']),a['codec_name'],a['sample_rate']) != ('h264',W,H,'30/1',N,'aac','48000'):
  raise ValueError('video/audio technical gate failed')
 return {'width':W,'height':H,'fps':30,'frames':N,'audio':'AAC 48kHz'}

def render(source, photo_path, frames_dir, output, manifest, genre='ai_work'):
 source,photo_path,frames_dir,output=map(Path,(source,photo_path,frames_dir,output))
 if output.exists(): raise ValueError('will not overwrite output')
 if not source.is_file() or not photo_path.is_file(): raise ValueError('missing input')
 screenshots=[frames_dir/f'{i:02d}.png' for i in range(26)]
 if any(not p.is_file() for p in screenshots): raise ValueError('missing screenshot')
 expected={**POLICY,'source_sha256':sha(source),'photo_sha256':sha(photo_path),'screenshots_sha256':[sha(p) for p in screenshots]}
 if manifest != expected: raise ValueError('manifest approval/provenance gate failed')
 probe(source)
 with Image.open(photo_path) as x: photo=x.copy()
 ui=[]
 for p in screenshots:
  with Image.open(p) as x: ui.append(x.copy())
 check_inputs(genre,photo,ui)
 with tempfile.TemporaryDirectory(prefix='cycle871_') as td:
  for i in range(COUNT):
   draw_frame(photo,ui,i,genre).save(Path(td)/f'{i:03}.jpg',quality=91,subsampling=0)
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
        f'[0:v][new]overlay=x=0:y={TOP}:enable=\'between(n,{START},{START+COUNT-1})\':'
        'eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate','30','-i',str(Path(td)/'%03d.jpg'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(N),'-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=240)
 return {'source_sha256':sha(source),'output_sha256':sha(output),'changed_scene_frames':COUNT,'genres_supported':len(GENRES),'policy':POLICY,'media':probe(output)}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for a in ['source','photo','frames_dir','output','manifest','report']: p.add_argument('--'+a,required=True)
 p.add_argument('--genre',default='ai_work')
 args=p.parse_args()
 result=render(args.source,args.photo,args.frames_dir,args.output,json.loads(Path(args.manifest).read_text()),args.genre)
 Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False))
