"""cycle928: original, review-only animated scene-01 hero. Never publishes media."""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
SCENE_FRAMES, CAPTION_SAFE_Y = 87, 1460
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES = {
 'ai_work': ('AIで仕事を速くする', '月次集計の作業', '#4AE0D0'),
 'finance': ('支出を見える化する', '支出記録の作業', '#7FC8FF'),
 'health': ('生活記録を整理する', '習慣記録の作業', '#9BE3BA'),
 'travel': ('旅行の準備を整理する', '旅程作成の作業', '#A7BBFF'),
 'beauty': ('毎日のケアを整理する', 'ケア記録の作業', '#F2B9DA'),
 'cooking': ('献立を整理する', '買い物計画の作業', '#FFC995'),
 'education': ('復習を見える化する', '学習計画の作業', '#C8BCFF'),
 'career': ('面談の準備を整理する', '面談準備の作業', '#F4D28B'),
 'lifestyle': ('家事を見える化する', '家事分担の作業', '#F1BFC7'),
 'technology': ('設定手順を整理する', '設定確認の作業', '#9EE1E8'),
}

def stage(frame):
 if not 0 <= frame < SCENE_FRAMES: raise ValueError('outside intro')
 return min(frame // 29, 2)

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def validate():
 assert len(GENRES)==10 and SCENE_FRAMES==87 and CAPTION_SAFE_Y < HEIGHT
 assert all(len(x)==3 and x[2].startswith('#') and len(x[2])==7 for x in GENRES.values())
 assert 'PUBLICATION_NOT_APPROVED' in POLICY
 return True

def render_frame(frame, genre='ai_work'):
 validate()
 if genre not in GENRES: raise ValueError('unknown genre')
 beat=stage(frame)
 title, topic, accent=GENRES[genre]
 img=Image.new('RGB',(WIDTH,CAPTION_SAFE_Y),(6,17,33));d=ImageDraw.Draw(img)
 for y in range(CAPTION_SAFE_Y):
  d.line((0,y,WIDTH,y),fill=(6+int(10*y/CAPTION_SAFE_Y),17+int(14*y/CAPTION_SAFE_Y),33+int(23*y/CAPTION_SAFE_Y)))
 font=lambda n,b=False:ImageFont.truetype(BOLD if b else REG,n)
 def t(x,y,s,n,c,b=False):d.text((x,y),s,font=font(n,b),fill=c)
 def rr(box,r,fill,outline=None,w=1):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
 # Layered editorial composition; all illustrations and numbers are fictional.
 rr((60,48,1020,126),24,'#113149','#2D6077',2)
 t(90,65,'AI WORK / 01',30,'#C8EDF3',True)
 t(832,65,'01 / 08',30,'#C8EDF3',True)
 rr((65,164,1015,394),34,'#0B2B40','#2C647B',3)
 t(99,182,'最初の一歩',31,accent,True)
 t(97,237,title,55,'#FFFFFF',True)
 t(100,320,'手作業を見える化する',39,'#F9D17B',True)
 # Soft glows, offset shadows and layered laptop-like evidence card.
 for i in range(6,0,-1):
  d.ellipse((205-i*13,485-i*13,900+i*13,1155+i*13),outline=(14+i*3,50+i*4,65+i*3),width=4)
 rr((116,490,976,1172),38,'#06111F','#3A8393',5)
 rr((140,518,952,1095),20,'#F2F7FB','#B7D4E2',3)
 rr((140,518,952,617),20,'#16394B')
 d.rectangle((140,576,952,617),fill='#16394B')
 t(180,541,'DEMO / 架空の表',33,'#E5FCFF',True)
 t(190,643,topic,40,'#12344A',True)
 rr((178,719,916,801),14,'#D4E8F0')
 for x,s in [(209,'月'),(457,'項目A'),(726,'項目B')]:t(x,735,s,31,'#1C435A',True)
 rows=[('4月','12','8'),('5月','16','9'),('6月','—','—')]
 for i,(month,a,b) in enumerate(rows):
  y=817+i*84
  selected=i==2
  rr((178,y,916,y+72),13,'#FFF2D2' if selected else ('#E8F2F8' if i%2==0 else '#F7FAFC'), '#F5B94F' if selected else None, 4 if selected else 1)
  for x,s in [(208,month),(486,a),(759,b)]:t(x,y+12,s,32,'#17374A',True)
 # Smooth moving focus and temporal editorial stages.
 if beat==0:
  msg='① まず作業を見つける'
 elif beat==1:
  msg='② 未入力は推測しない'
  pulse=4+int(3*(1+math.sin(frame*.36)))
  rr((174-pulse,981-pulse,920+pulse,1061+pulse),17,None,accent,4)
 else:
  msg='③ 確認してから改善'
  rr((187,983,905,1053),14,None,accent,5)
 rr((126,1192,954,1302),24,'#13394C','#397B8A',2)
 t(160,1217,msg,44,'#FFFFFF',True)
 # A visible 3-beat progress indicator and clear disclosure.
 for i in range(3):rr((177+i*248,1333,393+i*248,1348),7,accent if i<=beat else '#355267')
 t(74,1380,'FICTIONAL EXAMPLE  /  HUMAN REVIEW ONLY',23,'#9EC1CD')
 return img

def encode(source, output, frames_dir):
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(frames_dir/'%03d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
 return subprocess.run(cmd,capture_output=True,text=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--workdir',type=Path,required=True);p.add_argument('--genre',choices=GENRES,default='ai_work');a=p.parse_args()
 a.workdir.mkdir(parents=True,exist_ok=True);a.output.parent.mkdir(parents=True,exist_ok=True)
 for i in range(SCENE_FRAMES):render_frame(i,a.genre).save(a.workdir/f'{i:03d}.png',compress_level=1)
 r=encode(a.source,a.output,a.workdir)
 (a.workdir/'ffmpeg.log').write_text(r.stderr,encoding='utf-8')
 if r.returncode:raise RuntimeError(f'ffmpeg exit {r.returncode}: {r.stderr[-1500:]}')
 report={'policy':POLICY,'genre':a.genre,'source_sha256':sha256(a.source),'output_sha256':sha256(a.output),'changed_scene_frames':[0,86],'caption_safe_y':CAPTION_SAFE_Y,'reference':'reimplementation, not original v33','audio_semantic_alignment':'not independently verified'}
 (a.workdir/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
