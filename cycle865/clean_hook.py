"""cycle865: overlap-free, caption-safe opening hook for ten genres.
Private review render only. The evidence screenshot comes from a SHA-pinned
prior fictional-data review MP4; no new external assets or AI footage.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS, FRAMES, START, COUNT = 30, 691, 0, 89
ROI = (0, 330, 1080, 1120)  # absolute y=330..1449; inherited captions start >=1490
GENRES = ('ai_work','sales_business','beauty','romance','saving','career','wellness','science','travel_food','product_comparison_lifestyle')
HOOKS = {
 'ai_work':('その集計、','まだ手作業？'),
 'sales_business':('その営業資料、','毎回ゼロから？'),
 'beauty':('そのケア方法、','続けられる？'),
 'romance':('その伝え方、','届いている？'),
 'saving':('その家計管理、','続いている？'),
 'career':('その応募準備、','進んでいる？'),
 'wellness':('その習慣、','無理してない？'),
 'science':('その数字、','根拠はある？'),
 'travel_food':('その旅プラン、','迷ってない？'),
 'product_comparison_lifestyle':('その商品選び、','比べた？'),
}
POLICY = dict(review_only=True,publication_approved=False,automatic_posting=False,external_upload=False,source_rights_reviewed=False,fictional_example=True)
FONT_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_R = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def font(size,bold=True):
 p=FONT_B if bold else FONT_R
 return ImageFont.truetype(p,size) if Path(p).is_file() else ImageFont.load_default()

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()

def ease(t):
 t=max(0,min(1,t));return t*t*(3-2*t)

def contract(source,output,manifest,genre):
 source,output=Path(source),Path(output)
 if genre not in GENRES:raise ValueError('unknown genre')
 if not source.is_file():raise FileNotFoundError(source)
 if source.resolve()==output.resolve() or output.exists():raise ValueError('never overwrite private media')
 if manifest!={**POLICY,'source_sha256':sha256(source)}:raise ValueError('private media manifest rejected')
 return source,output

def media_info(path):
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
 v=next((s for s in data['streams'] if s['codec_type']=='video'),None)
 a=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
 if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v.get('nb_frames') or 0),a['codec_name'],a['sample_rate'])!=('h264',1080,1920,'30/1',691,'aac','48000'):
  raise ValueError('unexpected private review media format')

def extract_fictional_sheet(source,temporary):
 frame=Path(temporary)/'source_evidence.png'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss','11.5','-i',str(source),'-frames:v','1','-y',str(frame)],check=True,timeout=40)
 with Image.open(frame) as im:
  # This is a prior review-only fictional table; remove inherited UI banners.
  return im.convert('RGB').crop((96,575,862,1090)).resize((820,455),Image.Resampling.LANCZOS)

# Explicit layout boxes: testable safe geometry and no conflicting headline layers.
LAYOUT={'eyebrow':(72,42,550,112),'line1':(72,134,1000,250),
        'line2':(72,253,1020,375),'evidence':(95,403,985,960),
        'steps':(76,978,1000,1088)}
def intersects(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
def layout_ok():
 boxes=list(LAYOUT.values())
 return all(0<=x0<x1<=ROI[2] and 0<=y0<y1<=ROI[3] for x0,y0,x1,y1 in boxes) and not any(intersects(a,b) for i,a in enumerate(boxes) for b in boxes[i+1:])

@lru_cache(maxsize=1)
def backdrop():
 w,h=ROI[2:];im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
 for y in range(h):
  f=y/h;d.line((0,y,w,y),fill=(int(8+11*f),int(24+13*f),int(44+19*f)))
 layer=Image.new('RGBA',(w,h));q=ImageDraw.Draw(layer)
 for x,y,r,c in ((990,150,390,(50,168,255,130)),(130,860,370,(18,191,172,95)),(700,780,320,(252,178,92,75))):
  q.ellipse((x-r,y-r,x+r,y+r),fill=c)
 layer=layer.filter(ImageFilter.GaussianBlur(110))
 return Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')

def draw_frame(i,genre='ai_work',evidence=None):
 if genre not in GENRES or not 0<=i<COUNT:raise ValueError('invalid genre or frame')
 if not layout_ok():raise ValueError('overlapping text layout')
 im=backdrop().copy();d=ImageDraw.Draw(im,'RGBA')
 # Distinct, single-purpose hook. Do not stack old UI labels on top of headline.
 d.rounded_rectangle((72,42,515,112),radius=29,fill=(12,85,117,220),outline=(100,213,247,225),width=2)
 d.text((103,51),'3秒で分かる仕事の改善',font=font(34),fill=(255,255,255,255))
 a,b=HOOKS[genre]
 d.text((72,140),a,font=font(82),fill=(242,250,255,255))
 d.text((72,259),b,font=font(96),fill=(255,224,112,255),stroke_width=2,stroke_fill=(8,23,42,255))
 # Screen appears with a short, deliberate upward slide, then settles.
 alpha=ease((i-10)/15);dy=int((1-alpha)*60)
 x0,y0,x1,y1=LAYOUT['evidence']; y0+=dy;y1+=dy
 d.rounded_rectangle((x0+8,y0+12,x1+8,y1+12),radius=30,fill=(0,0,0,85))
 d.rounded_rectangle((x0,y0,x1,y1),radius=30,fill=(11,28,48,255),outline=(123,213,237,255),width=4)
 d.rounded_rectangle((x0+20,y0+17,x1-20,y0+64),radius=14,fill=(17,65,87,255))
 d.text((x0+38,y0+20),'実際の表計算操作から / 架空データ',font=font(26),fill=(226,251,255,255))
 if evidence is not None and genre=='ai_work':
  im.paste(evidence,(x0+35,y0+75));d=ImageDraw.Draw(im,'RGBA')
 else:
  d.rounded_rectangle((x0+35,y0+75,x1-35,y1-35),radius=16,fill=(236,248,251,255))
  d.text((x0+93,y0+230),'確認できる根拠を示す',font=font(47),fill=(22,72,93,255))
 # Only one short secondary line; it never collides with the video or title.
 step=ease((i-43)/18)
 d.rounded_rectangle((76,978,1000,1088),radius=29,fill=(9,44,61,int(215*step)),outline=(84,221,211,int(240*step)),width=3)
 if step>.05:
  d.text((140,998),'見る  →  整理  →  確認',font=font(48),fill=(255,255,255,int(255*step)))
 return im

def render(source,output,manifest,genre='ai_work'):
 source,output=contract(source,output,manifest,genre);media_info(source)
 with tempfile.TemporaryDirectory(prefix='cycle865_') as tmp:
  evidence=extract_fictional_sheet(source,tmp) if genre=='ai_work' else None
  folder=Path(tmp)/'frames';folder.mkdir()
  for i in range(COUNT):draw_frame(i,genre,evidence).save(folder/f'{i:03d}.jpg',quality=90,subsampling=0)
  # Video region only; original Japanese burned captions and original AAC are kept.
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
        f'[0:v][new]overlay=x={ROI[0]}:y={ROI[1]}:enable=\'between(n,{START},{START+COUNT-1})\':eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate','30','-start_number','0','-i',str(folder/'%03d.jpg'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=240)
 media_info(output)
 return dict(source_sha256=sha256(source),output_sha256=sha256(output),frame_range=[START,START+COUNT-1],changed_frames=COUNT,genre=genre,layout_ok=layout_ok(),policy=POLICY)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');args=p.parse_args()
 report=render(args.source,args.output,json.loads(Path(args.manifest).read_text()),args.genre)
 Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
