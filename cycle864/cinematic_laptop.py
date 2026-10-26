"""cycle864: review-only cinematic, image-first laptop evidence scene.
No network, external asset, AI-service claim, publication, or automatic posting.
The sole screenshot is extracted from a SHA-pinned local private review MP4.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS, FRAMES, START, COUNT = 30, 691, 507, 81
ROI = (0, 330, 1080, 1120)  # image never touches burned caption region y >=1490
GENRES = ('ai_work','sales_business','beauty','romance','saving','career','wellness','science','travel_food','product_comparison_lifestyle')
TITLES = dict(zip(GENRES,('使える指示を、資産に','成功した型を、次にも','手順を、再現できる形に','伝え方を、整理する','家計管理を、仕組みに','応募準備を、効率化','記録を、続けやすく','検証手順を、残す','旅の計画を、保存','比較条件を、記録する')))
POLICY = dict(review_only=True,publication_approved=False,automatic_posting=False,external_upload=False,source_rights_reviewed=False,fictional_example=True)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def font(size, regular=False):
 p = FONT_REG if regular else FONT
 return ImageFont.truetype(p,size) if Path(p).is_file() else ImageFont.load_default()

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def ease(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)

def validate(source, output, manifest, genre):
 source,output=Path(source),Path(output)
 if genre not in GENRES:raise ValueError('unknown genre')
 if not source.is_file():raise FileNotFoundError(source)
 if source.resolve()==output.resolve() or output.exists():raise ValueError('no overwrite')
 if manifest!={**POLICY,'source_sha256':sha256(source)}:raise ValueError('fail-closed source policy/hash')
 return source,output

def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))['streams']

def check_streams(path):
 s=probe(path);v=next((a for a in s if a['codec_type']=='video'),None);a=next((a for a in s if a['codec_type']=='audio'),None)
 if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v.get('nb_frames') or 0),a['codec_name'],a['sample_rate']) != ('h264',1080,1920,'30/1',691,'aac','48000'):
  raise ValueError('unexpected video/audio contract')

def extract_evidence(source,tmp):
 out=Path(tmp)/'writer_evidence.jpg'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss','18.1','-i',str(source),'-frames:v','1','-y',str(out)],check=True,timeout=35)
 with Image.open(out) as im:
  return im.convert('RGB').crop((94,520,836,918)).resize((720,386),Image.Resampling.LANCZOS)

@lru_cache(maxsize=1)
def background():
 w,h=ROI[2:];im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
 for y in range(h):
  t=y/h;d.line((0,y,w,y),fill=(int(11+22*t),int(30+15*t),int(56+11*t)))
 glow=Image.new('RGBA',(w,h));g=ImageDraw.Draw(glow)
 for x,y,r,c in [(885,150,350,(255,194,119,135)),(125,660,310,(23,173,214,100)),(930,950,230,(255,137,74,80))]:
  g.ellipse((x-r,y-r,x+r,y+r),fill=c)
 glow=glow.filter(ImageFilter.GaussianBlur(112))
 im=Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB');d=ImageDraw.Draw(im,'RGBA')
 for x,y,r in [(90,120,13),(960,220,18),(790,470,10),(150,900,15),(1010,800,12)]:
  d.ellipse((x-r,y-r,x+r,y+r),fill=(255,234,201,100))
 d.polygon([(0,935),(1080,830),(1080,1120),(0,1120)],fill=(9,19,34,240))
 d.line([(0,934),(1080,829)],fill=(217,181,137,145),width=6)
 return im

def draw_frame(i,genre='ai_work',evidence=None):
 if genre not in GENRES or not 0<=i<COUNT:raise ValueError('invalid genre/frame')
 im=background().copy();d=ImageDraw.Draw(im,'RGBA');t=i/(COUNT-1)
 d.text((64,42),TITLES[genre],font=font(55),fill=(255,255,255,255))
 d.text((66,123),'架空データで確認した操作例',font=font(29,True),fill=(196,222,234,255))
 # Perspective-inspired floating laptop: independent shadow, glass display, metallic base.
 shift=int(16*(1-ease(i/19))-10*t)
 d.rounded_rectangle((100,207+shift,995,800+shift),radius=34,fill=(0,0,0,115))
 d.rounded_rectangle((85,187+shift,977,782+shift),radius=33,fill=(13,22,37,255),outline=(156,189,205,255),width=6)
 d.rounded_rectangle((106,210+shift,955,757+shift),radius=20,fill=(6,16,28,255))
 d.ellipse((522,196+shift,535,209+shift),fill=(62,121,151,255))
 d.rounded_rectangle((125,234+shift,935,716+shift),radius=13,fill=(241,248,249,255))
 d.rounded_rectangle((125,234+shift,935,292+shift),radius=12,fill=(20,58,78,255))
 d.text((155,243+shift),'WRITER  /  保存した作業テンプレート',font=font(25),fill=(255,255,255,255))
 if evidence is not None:
  im.paste(evidence.resize((756,405),Image.Resampling.LANCZOS),(152,300+shift));d=ImageDraw.Draw(im,'RGBA')
 else:
  for j,txt in enumerate(('目的：やることを決める','条件：必要な情報だけ使う','確認：元の資料と照合する')):
   d.text((174,340+shift+j*100),txt,font=font(32),fill=(18,57,71,255))
 d.polygon([(83,782+shift),(977,782+shift),(1042,837+shift),(25,837+shift)],fill=(174,194,201,255))
 d.polygon([(118,793+shift),(950,793+shift),(984,818+shift),(83,818+shift)],fill=(49,69,85,255))
 d.rounded_rectangle((420,827+shift,650,843+shift),radius=8,fill=(97,116,129,255))
 # One clear three-beat transformation: document -> reusable checklist -> save.
 for j,(label,threshold) in enumerate((('目的',9),('条件',26),('確認',43))):
  a=ease((i-threshold)/12)
  x=91+j*310;y=892+int(24*(1-a))
  d.rounded_rectangle((x,y,x+280,y+94),radius=24,fill=(17,57,75,int(215*a)),outline=(84,219,228,int(245*a)),width=3)
  if a>.12:
   d.ellipse((x+20,y+23,x+64,y+67),fill=(38,199,178,int(255*a)))
   d.text((x+31,y+23),'✓',font=font(28),fill=(255,255,255,int(255*a)))
   d.text((x+84,y+21),label,font=font(38),fill=(255,255,255,int(255*a)))
 if i>=58:
  a=ease((i-58)/14)
  d.rounded_rectangle((245,1010,842,1090),radius=27,fill=(11,118,132,int(235*a)),outline=(132,242,233,int(250*a)),width=3)
  d.text((325,1016),'保存して、次も使う',font=font(39),fill=(255,255,255,int(255*a)))
 return im

def render(source,output,manifest,genre='ai_work'):
 source,output=validate(source,output,manifest,genre);check_streams(source)
 with tempfile.TemporaryDirectory(prefix='cycle864_') as td:
  shot=extract_evidence(source,td) if genre=='ai_work' else None
  frames=Path(td)/'frames';frames.mkdir()
  for i in range(COUNT):draw_frame(i,genre,shot).save(frames/f'{i:03d}.jpg',quality=90,subsampling=0)
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[layer];'
        f'[0:v][layer]overlay=x={ROI[0]}:y={ROI[1]}:enable=\'between(n,{START},{START+COUNT-1})\':eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate','30','-start_number','0','-i',str(frames/'%03d.jpg'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=240)
 check_streams(output)
 return dict(source_sha256=sha256(source),output_sha256=sha256(output),genre=genre,changed_frames=COUNT,frame_range=[START,START+COUNT-1],policy=POLICY)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
 report=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
 Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')