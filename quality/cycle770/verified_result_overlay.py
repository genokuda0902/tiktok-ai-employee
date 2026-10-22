"""Review-only verified numeric overlays. Original v33 engine not recovered."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
GENRES={'AI・仕事効率化':'#35E5D4','美容・身だしなみ':'#F3A4D1','恋愛・心理':'#FF99AB','お金・節約':'#F6CE72','営業・ビジネス':'#82B5FF','転職・キャリア':'#AEA9F5','健康・生活改善':'#89D6B4','雑学・科学':'#89DDF1','旅行・グルメ':'#FFB47E','商品比較・暮らし':'#CBB5FA'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
VALUES=[120000,150000,200000,180000]
WINDOWS={'intro':(0,96),'chart':(300,384)}
def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def validate(m,source):
 if m.get('genre') not in GENRES or set(m.get('supported_genres',[]))!=set(GENRES):raise ValueError('genre allowlist')
 if m.get('quality_approved') is not False or m.get('status')!='HUMAN_REVIEW':raise ValueError('quality gate')
 if m.get('post_policy')!='employee_manual_after_approval':raise ValueError('manual posting only')
 if m.get('source_origin')!='inherited_review_only' or m.get('synthetic_data') is not True:raise ValueError('source provenance')
 if m.get('claim')!='synthetic_arithmetic_only':raise ValueError('unverified claim')
 if m.get('values')!=VALUES or sum(VALUES)!=650000:raise ValueError('arithmetic')
 if m.get('source_sha256')!=sha256(source):raise ValueError('source hash')
 if not Path(FONT).is_file():raise ValueError('Japanese font missing')
def overlay(scene,genre):
 if scene not in WINDOWS or genre not in GENRES:raise ValueError('unsupported scene/genre')
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 accent=tuple(bytes.fromhex(GENRES[genre][1:]))+(255,)
 if scene=='intro':
  d.rectangle((92,1306,845,1409),fill=(3,15,36,255))
  d.text((103,1308),'65',font=ImageFont.truetype(FONT,71),fill=accent)
  d.text((286,1336),'万円',font=ImageFont.truetype(FONT,43),fill=(251,253,255,255))
  d.text((502,1340),'集計結果',font=ImageFont.truetype(FONT,27),fill=(169,201,214,255))
  d.rounded_rectangle((98,1396,833,1407),radius=4,fill=accent)
 else:
  d.rectangle((82,1368,854,1459),fill=(9,38,61,255))
  d.text((88,1366),'650,000',font=ImageFont.truetype(FONT,71),fill=(249,252,255,255))
  d.text((757,1388),'円',font=ImageFont.truetype(FONT,45),fill=accent)
 return im
def render(source,manifest_path,out):
 source,manifest_path,out=map(Path,(source,manifest_path,out))
 m=json.loads(manifest_path.read_text(encoding='utf-8'));validate(m,source)
 out.parent.mkdir(parents=True,exist_ok=True)
 p0,p1=out.parent/'intro_verified.png',out.parent/'chart_verified.png'
 overlay('intro',m['genre']).save(p0);overlay('chart',m['genre']).save(p1)
 flt=("[0:v][1:v]overlay=0:0:enable='between(n,0,95)':format=auto[v1];"
      "[v1][2:v]overlay=0:0:enable='between(n,300,383)':format=auto,format=yuv420p[v]")
 tmp=out.parent/'video_only.mp4'
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),
  '-loop','1','-framerate','30','-i',str(p0),'-loop','1','-framerate','30','-i',str(p1),
  '-filter_complex',flt,'-map','[v]','-c:v','libx264','-preset','ultrafast',
  '-crf','20','-r','30','-frames:v','819','-an','-movflags','+faststart',str(tmp)],check=True)
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(tmp),'-i',str(source),
  '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(out)],check=True)
 tmp.unlink();return out
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True);p.add_argument('--manifest',required=True);p.add_argument('--out',required=True)
 a=p.parse_args();print(render(a.source,a.manifest,a.out))
