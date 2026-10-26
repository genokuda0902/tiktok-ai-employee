"""cycle874: data-consistent animated chart; all ten genres, review only."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,tempfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

WIDTH,HEIGHT,FPS,FRAMES=1080,1920,30,691
START,COUNT,TOP,BOTTOM=170,81,285,1245
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,'automatic_posting':False,'source_rights_reviewed':False}

@dataclass(frozen=True)
class Genre:
    headline:str
    label_a:str
    label_b:str
    period:tuple[str,str,str]
    a:tuple[int,int,int]
    b:tuple[int,int,int]

# Single source for displayed numbers AND bar geometry; fictional samples only.
GENRES={
 'ai_work':Genre('月別データの完成見本','営業A','営業B',('4月','5月','6月'),(12,16,18),(8,9,12)),
 'trivia':Genre('調査結果の完成見本','項目A','項目B',('1回','2回','3回'),(5,7,9),(3,4,6)),
 'cooking':Genre('調理時間の完成見本','工程A','工程B',('1品','2品','3品'),(12,15,18),(7,9,11)),
 'beauty':Genre('記録結果の完成見本','項目A','項目B',('1週','2週','3週'),(3,5,7),(2,4,6)),
 'money':Genre('家計記録の完成見本','費目A','費目B',('4月','5月','6月'),(10,12,14),(6,8,9)),
 'wellness':Genre('活動記録の完成見本','項目A','項目B',('1週','2週','3週'),(4,6,8),(3,4,5)),
 'travel':Genre('旅程比較の完成見本','候補A','候補B',('1日','2日','3日'),(4,5,6),(2,3,4)),
 'product':Genre('商品比較の完成見本','商品A','商品B',('条件1','条件2','条件3'),(5,7,8),(4,6,7)),
 'story':Genre('構成比較の完成見本','案A','案B',('序盤','中盤','終盤'),(3,5,7),(2,4,6)),
 'business':Genre('業務記録の完成見本','作業A','作業B',('4月','5月','6月'),(8,10,12),(5,6,9)),
}
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
 return h.hexdigest()
@lru_cache(maxsize=64)
def font(size,bold=True):
 return ImageFont.truetype(FONT if bold else REGULAR,size)
def ease(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def validate_genre(key):
 if key not in GENRES:raise ValueError('unknown genre')
 g=GENRES[key]
 if not all(len(x)==3 for x in (g.period,g.a,g.b)):raise ValueError('3 periods required')
 if any(not isinstance(v,int) or not 0<v<=1000 for v in (*g.a,*g.b)):raise ValueError('invalid values')
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 for txt,size,limit in [(g.headline,57,900),(g.label_a,34,150),(g.label_b,34,150),*[(p,35,170) for p in g.period]]:
  box=d.textbbox((0,0),txt,font=font(size))
  if box[2]-box[0]>limit:raise ValueError('Japanese text clipping')
 return g
def bar_heights(g):
 peak=max((*g.a,*g.b))
 return tuple(round(260*x/peak) for x in g.a),tuple(round(260*x/peak) for x in g.b)
@lru_cache(maxsize=1)
def background():
 h=BOTTOM-TOP;im=Image.new('RGB',(WIDTH,h));d=ImageDraw.Draw(im)
 for y in range(h):d.line((0,y,WIDTH,y),fill=(8,17+round(26*y/h),52+round(12*y/h)),width=1)
 return im
def draw_frame(i,genre='ai_work'):
 if not 0<=i<COUNT:raise ValueError('frame index outside scene')
 g=validate_genre(genre);im=background().copy();d=ImageDraw.Draw(im,'RGBA')
 d.rounded_rectangle((58,29,454,91),radius=24,fill=(8,85,103,255),outline=(72,214,227,230),width=2)
 d.text((88,44),'WORKFLOW / 架空データ',font=font(29),fill=(235,252,254))
 d.text((57,125),g.headline,font=font(57),fill=(255,255,255))
 d.text((58,211),'数値とグラフを同じデータから作る',font=font(36,False),fill=(177,225,238))
 d.rounded_rectangle((55,281,1025,843),radius=28,fill=(11,33,53,255),outline=(62,165,192,255),width=3)
 d.text((84,307),'元データ → グラフ',font=font(41),fill=(250,252,255))
 d.ellipse((590,324,613,347),fill=(49,207,221,255));d.text((625,314),g.label_a,font=font(34),fill=(226,247,249))
 d.ellipse((805,324,828,347),fill=(255,181,97,255));d.text((839,314),g.label_b,font=font(34),fill=(255,244,226))
 ha,hb=bar_heights(g);baseline=747
 for j,(period,va,vb) in enumerate(zip(g.period,g.a,g.b)):
  cx=234+j*301
  if ease((i-2-j*5)/14)>0:
   d.rounded_rectangle((cx-120,380,cx+122,437),radius=15,fill=(19,69,84,255),outline=(65,169,188,230),width=2)
   d.text((cx-104,387),f'{period}  {va} / {vb}',font=font(29),fill=(244,252,254))
  progress=ease((i-16-j*6)/34);a_height=round(ha[j]*progress);b_height=round(hb[j]*progress)
  if a_height:d.rounded_rectangle((cx-62,baseline-a_height,cx+1,baseline),radius=10,fill=(51,209,226,255))
  if b_height:d.rounded_rectangle((cx+16,baseline-b_height,cx+79,baseline),radius=10,fill=(255,185,100,255))
  if progress>.97:
   d.text((cx-58,baseline-ha[j]-42),str(va),font=font(32),fill=(224,252,255))
   d.text((cx+20,baseline-hb[j]-42),str(vb),font=font(32),fill=(255,236,207))
  d.text((cx-35,760),period,font=font(36),fill=(241,249,253))
 d.line((106,747,976,747),fill=(101,140,162,255),width=3)
 if i>=52:
  d.rounded_rectangle((61,863,1020,933),radius=16,fill=(8,77,90,255),outline=(76,211,224,255),width=2)
  d.text((95,876),'照合：6月  営業A 18 ／ 営業B 12' if genre=='ai_work' else '見本の数値と棒の高さが一致',font=font(35),fill=(245,255,253))
 return im
def render(source,output,manifest,genre='ai_work',start=START,count=COUNT,total=FRAMES):
 source,output=Path(source),Path(output)
 if output.exists():raise ValueError('refuse overwrite')
 if not source.is_file():raise FileNotFoundError('missing private source')
 if manifest!={**POLICY,'source_sha256':sha(source)}:raise ValueError('source manifest not approved for private review')
 validate_genre(genre)
 if count<1 or count>COUNT or start<0 or start+count>total:raise ValueError('invalid frame range')
 with tempfile.TemporaryDirectory(prefix='cycle874_') as td:
  for i in range(count):draw_frame(i,genre).save(Path(td)/f'{i:03}.png')
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{start}/({FPS}*TB)[overlay];'
        f'[0:v][overlay]overlay=x=0:y={TOP}:enable=\'between(n,{start},{start+count-1})\':'
        'eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate',str(FPS),
       '-i',str(Path(td)/'%03d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0',
       '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r',str(FPS),
       '-frames:v',str(total),'-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=300)
 return {'source_sha256':sha(source),'output_sha256':sha(output),'start_frame':start,'changed_frames':count,
         'supported_genres':len(GENRES),'policy':POLICY,'scene_data':{'periods':GENRES[genre].period,'a':GENRES[genre].a,'b':GENRES[genre].b}}
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for k in ('source','output','manifest','report'):ap.add_argument('--'+k,required=True)
 ap.add_argument('--genre',default='ai_work');args=ap.parse_args()
 data=render(args.source,args.output,json.loads(Path(args.manifest).read_text()),args.genre)
 Path(args.report).write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps(data,ensure_ascii=False))
