"""cycle863: review-only evidence-backed Before/After motion card.

The 10-genre renderer draws original graphics; the optional screenshot comes ONLY
from a SHA-pinned local review video. This is not v33 source recovery, does not
make a verified AI-performance claim, and never uploads or publishes assets.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS=30
FRAMES=691
START=425  # scene 6, 14.167s
COUNT=82   # frames 425-506, before scene 7
ROI=(40,350,1000,1090)  # x,y,width,height; end y=1440 < caption-safe y1490
GENRES=("ai_work","sales_business","beauty","romance","saving","career","wellness","science","travel_food","product_comparison_lifestyle")
ACCENTS=dict(zip(GENRES,("#30D6F4","#4BE5AC","#FF90BD","#FF83A9","#56E7B3","#86A6FF","#63E6BD","#68D6FF","#F5BA79","#A9B6FF")))
# Other genres deliberately use nonquantitative example wording until evidence exists.
COPY={
 "ai_work":("元データと照合","17","18","入力値を確認して修正"),
 "sales_business":("商談メモを照合","未確認","確認済","記録と事実を突き合わせる"),
 "beauty":("説明文を照合","未確認","確認済","商品の公式情報を確認"),
 "romance":("相手の意図を確認","推測","確認","決めつけずに聞いてみる"),
 "saving":("支出記録を照合","未確認","確認済","元の明細を見直す"),
 "career":("応募条件を照合","未確認","確認済","募集要項と照らし合わせる"),
 "wellness":("健康情報を確認","未確認","確認済","信頼できる資料を調べる"),
 "science":("計算結果を検算","未確認","確認済","元データと式を再確認"),
 "travel_food":("営業時間を確認","未確認","確認済","公式情報を再確認する"),
 "product_comparison_lifestyle":("製品仕様を照合","未確認","確認済","メーカー仕様を確認する")
}
POLICY={"review_only":True,"publication_approved":False,"automatic_posting":False,"external_upload":False,"source_rights_reviewed":False,"contains_personal_data":False,"fictional_example":True}
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def font(size,reg=False):
 p=FONT_REG if reg else FONT
 return ImageFont.truetype(p,size) if Path(p).is_file() else ImageFont.load_default()

def ease(t):
 t=max(0.,min(1.,t));return t*t*(3-2*t)

def validate(source,output,manifest,genre):
 source,output=Path(source),Path(output)
 if genre not in GENRES:raise ValueError('unsupported genre')
 if not source.is_file():raise FileNotFoundError(source)
 if source.resolve()==output.resolve() or output.exists():raise ValueError('output overwrite prohibited')
 if manifest!={**POLICY,"source_sha256":sha256(source)}:raise ValueError('review-only manifest/hash mismatch')
 return source,output

def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))

def check_streams(path):
 s=probe(path)['streams']
 v=next((x for x in s if x.get('codec_type')=='video'),None)
 a=next((x for x in s if x.get('codec_type')=='audio'),None)
 if not v or not a or (v.get('codec_name'),v.get('width'),v.get('height'),v.get('r_frame_rate'),int(v.get('nb_frames') or 0),a.get('codec_name'),a.get('sample_rate')) != ('h264',1080,1920,'30/1',691,'aac','48000'):
  raise ValueError('input/output video format differs from pinned 23-second review master')

def source_evidence(source,tmp):
 p=Path(tmp)/'evidence.png'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss',f'{365/FPS:.6f}','-i',str(source),'-frames:v','1','-y',str(p)],check=True,timeout=35)
 with Image.open(p) as im:
  return im.convert('RGB').crop((78,510,970,1180)).resize((620,310),Image.Resampling.LANCZOS)

def rounded_text(d,xy,text,sz,color):d.text(xy,text,font=font(sz),fill=color)

def draw(frame,genre='ai_work',evidence=None):
 if genre not in GENRES or not 0<=frame<COUNT:raise ValueError('invalid genre/frame')
 w,h=ROI[2:];accent=ACCENTS[genre];title,before,after,proof=COPY[genre]
 im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
 for y in range(h):
  t=y/h;d.line((0,y,w,y),fill=(int(8+9*t),int(20+11*t),int(35+22*t)))
 glow=Image.new('RGBA',(w,h));g=ImageDraw.Draw(glow)
 g.ellipse((360,-280,1210,480),fill=(30,167,234,75))
 g.ellipse((-250,550,490,1240),fill=(18,98,151,60))
 im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(88)));d=ImageDraw.Draw(im)
 d.rounded_rectangle((20,20,980,1060),radius=40,outline=(54,118,152),width=3)
 d.rounded_rectangle((50,50,390,114),radius=21,fill=(11,60,80))
 rounded_text(d,(75,62),'BEFORE  →  AFTER',29,accent)
 rounded_text(d,(54,145),title,53,'#FFFFFF')
 rounded_text(d,(55,225),'例：AIの出力は必ず確認する',31,'#B9CFDB')
 # two independent cards, introduced in different beats
 appear_before=ease((frame-2)/9);appear_after=ease((frame-24)/12)
 for x,label,value,pct,active in [(52,'修正前',before,appear_before,False),(527,'確認後',after,appear_after,True)]:
  y=int(320+(1-pct)*42)
  fill=(23,39,57) if not active else (9,59,76)
  d.rounded_rectangle((x,y,x+419,y+282),radius=28,fill=fill,outline=(84,100,120) if not active else accent,width=4)
  if pct>0.12:
   d.rounded_rectangle((x+22,y+20,x+165,y+72),radius=14,fill=(60,73,90) if not active else (18,121,144))
   rounded_text(d,(x+40,y+27),label,27,'#FFFFFF')
  if pct>0.50:
   size=125 if len(value)<4 else 62
   bb=d.textbbox((0,0),value,font=font(size));tw=bb[2]-bb[0]
   rounded_text(d,(x+210-tw//2,y+100),value,size,'#FFB6B1' if not active else '#FFFFFF')
 # animated directional chevron / progress
 if frame>=22:
  p=ease((frame-22)/14);x=472+int(8*p)
  d.rounded_rectangle((x,419,x+58,496),radius=20,fill=accent)
  d.polygon(((x+19,438),(x+39,456),(x+19,477)),fill='#062432')
 # lower evidence: either original private spreadsheet crop or generic no-asset original graphics
 d.rounded_rectangle((52,668,948,982),radius=27,fill=(12,39,56),outline=(59,113,140),width=3)
 if genre=='ai_work' and evidence is not None:
  mask=Image.new('L',evidence.size,0);ImageDraw.Draw(mask).rounded_rectangle((0,0,evidence.width-1,evidence.height-1),radius=20,fill=255)
  shot=evidence.resize((560,266),Image.Resampling.LANCZOS)
  mask=mask.resize((560,266),Image.Resampling.LANCZOS)
  im.paste(shot,(72,694),mask);d=ImageDraw.Draw(im)
  d.rounded_rectangle((72,694,632,960),radius=20,outline=(90,155,174),width=2)
  d.rounded_rectangle((652,718,927,768),radius=13,fill=(15,89,111))
  rounded_text(d,(670,724),'架空データの例',23,'#FFFFFF')
  for k,ln in enumerate(('実際のCalc画面','元データと照合','17 → 18 に修正')):
   rounded_text(d,(662,793+47*k),ln,25,'#D7EAF2' if k<2 else accent)
 else:
  d.rounded_rectangle((76,714,920,814),radius=22,fill=(13,74,96))
  rounded_text(d,(109,735),'元の情報を確認',42,'#FFFFFF')
  rounded_text(d,(90,850),proof,38,accent)
 # completion bar is timed only to this scene, not a fabricated AI processing indicator
 progress=ease((frame-46)/24)
 d.rounded_rectangle((70,1010,930,1028),radius=9,fill=(40,75,94))
 if progress>0:d.rounded_rectangle((70,1010,70+int(860*progress),1028),radius=9,fill=accent)
 return im.convert('RGB')

def render(source,output,manifest,genre='ai_work'):
 source,output=validate(source,output,manifest,genre);check_streams(source)
 with tempfile.TemporaryDirectory(prefix='cycle863_') as tmp:
  evidence=source_evidence(source,tmp) if genre=='ai_work' else None
  folder=Path(tmp)/'frames';folder.mkdir()
  for i in range(COUNT):draw(i,genre,evidence).save(folder/f'f_{i:03d}.png')
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
        f'[0:v][new]overlay=x={ROI[0]}:y={ROI[1]}:enable=\'between(n,{START},{START+COUNT-1})\':eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate','30','-start_number','0','-i',str(folder/'f_%03d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=250)
 check_streams(output)
 return {'input_sha256':sha256(source),'output_sha256':sha256(output),'changed_frames':COUNT,'frame_range':[START,START+COUNT-1],'genre':genre,'source_evidence_reused':genre=='ai_work','policy':POLICY}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
 result=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre);Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')