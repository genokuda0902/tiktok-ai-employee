"""cycle820: complete who/what/deadline action card. Review-only; 10 genre palettes."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS=30
START_FRAME=450
FRAME_COUNT=90
WIDTH,HEIGHT=880,700
X,Y=92,650
GENRE_COLORS={
 'sales_business':'#5CD6C5','ai_tools':'#56A7F6','money':'#E8C76A',
 'beauty':'#ED94B4','fitness':'#EF955E','career':'#7AC3E8',
 'study':'#A6A0EF','life_hacks':'#8BD6A0','food':'#E6AE73',
 'travel':'#82B7EC'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
ROWS=(('担当','自分が実行'),('行動','改善を１つ試す'),('期限','今日の稼働終了まで'))

def _font(size,bold=False):
 path=BOLD if bold and Path(BOLD).exists() else FONT
 if not Path(path).exists(): raise RuntimeError('Noto Sans CJK required')
 return ImageFont.truetype(path,size)

def validate_plan(rows=ROWS):
 if len(rows)!=3: raise ValueError('three rows required')
 for label,value in rows:
  if not label or not value.strip() or value.strip() in ('-','—','未定','TBD'):
   raise ValueError('unfilled action-plan field')
 if [x[0] for x in rows]!=['担当','行動','期限']:
  raise ValueError('required fields: 担当, 行動, 期限')
 return True

def render_frame(frame,genre='sales_business'):
 if not 0<=frame<FRAME_COUNT: raise ValueError('frame out of range')
 if genre not in GENRE_COLORS: raise ValueError('unsupported genre')
 validate_plan()
 accent=tuple(bytes.fromhex(GENRE_COLORS[genre][1:]))
 im=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0))
 shadow=Image.new('RGBA',(WIDTH,HEIGHT))
 sd=ImageDraw.Draw(shadow)
 sd.rounded_rectangle((15,18,865,690),radius=26,fill=(0,0,0,180))
 im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
 d=ImageDraw.Draw(im,'RGBA')
 d.rounded_rectangle((12,8,863,676),radius=24,fill=(14,37,54,255),outline=(150,217,215,255),width=3)
 d.rounded_rectangle((27,24,847,119),radius=14,fill=(28,75,86,255))
 d.text((48,48),'今日の実行プラン',font=_font(34,True),fill='white')
 d.text((728,60),'実践例',font=_font(24),fill=(235,218,137))
 for i,(label,value) in enumerate(ROWS):
  top=148+i*132
  active=max(0,min(1,(frame-i*23)/10))
  fill=(round(23+12*active),round(53+30*active),round(68+27*active),255)
  d.rounded_rectangle((35,top,845,top+113),radius=14,fill=fill,outline=(68,124,137,255),width=2)
  d.ellipse((60,top+28,115,top+83),fill=accent+(255,) if active else (65,94,108,255))
  d.text((80,top+37),str(i+1),font=_font(23,True),fill=(8,35,49) if active else (228,243,247))
  d.text((140,top+37),label,font=_font(26,True),fill=(185,217,224))
  if active>0:
   txt=Image.new('RGBA',(470,80));td=ImageDraw.Draw(txt)
   td.text((0,15),value,font=_font(36,True),fill='white')
   w=max(1,round(470*active))
   im.alpha_composite(txt.crop((0,0,w,80)),(310,top+12))
   if active>=1:
    d=ImageDraw.Draw(im,'RGBA')
    d.text((796,top+37),'✓',font=_font(26,True),fill=accent+(255,))
 d=ImageDraw.Draw(im,'RGBA')
 d.text((44,587),'考えるだけで終わらせない。',font=_font(25,True),fill=(225,244,242))
 d.rounded_rectangle((35,643,845,653),radius=4,fill=(55,97,106))
 progress=max(0,min(1,frame/(FRAME_COUNT-1)))
 d.rounded_rectangle((35,643,35+int(810*progress),653),radius=4,fill=accent+(255,))
 return im

def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def render(source,output,genre='sales_business',synthetic=False):
 if genre not in GENRE_COLORS: raise ValueError('unsupported genre')
 if not Path(source).is_file(): raise FileNotFoundError(source)
 meta=probe(source)
 v=next(s for s in meta['streams'] if s['codec_type']=='video')
 a=[s for s in meta['streams'] if s['codec_type']=='audio']
 if (v['width'],v['height'],v['avg_frame_rate'])!=(1080,1920,'30/1') or not a:
  raise ValueError('requires 1080x1920 30fps source with audio')
 if float(meta['format']['duration'])<18: raise ValueError('source too short')
 output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 frames=output.parent/'frames820';frames.mkdir(exist_ok=True)
 for i in range(FRAME_COUNT): render_frame(i,genre).save(frames/f'{i:03}.png',compress_level=3)
 filt=("[1:v]setpts=PTS-STARTPTS+15/TB[card];"
       "[0:v][card]overlay=92:650:eof_action=pass:"
       "enable='gte(t,15)*lt(t,18)',format=yuv420p[v]")
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
  '-i',str(source),'-framerate','30','-start_number','0','-i',str(frames/'%03d.png'),
  '-filter_complex',filt,'-map','[v]','-map','0:a:0',
  '-c:v','libx264','-preset','veryfast','-crf','21','-threads','2',
  '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True)
 out=probe(output);ov=next(s for s in out['streams'] if s['codec_type']=='video')
 report={'cycle':820,'genre':genre,'genre_count':len(GENRE_COLORS),
  'width':ov['width'],'height':ov['height'],'fps':ov['avg_frame_rate'],
  'duration_s':float(out['format']['duration']),
  'replaced_start_s':15,'replaced_end_s':18,'frames':FRAME_COUNT,
  'all_action_fields_completed':validate_plan(),
  'source_rights_verified':False,'japanese_speech_semantics_verified':False,
  'phone_verified':False,'publication_approved':False,'auto_post':False,
  'synthetic_source':synthetic}
 (output.parent/'qa820.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--source',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--genre',choices=sorted(GENRE_COLORS),default='sales_business')
 p.add_argument('--synthetic',action='store_true')
 a=p.parse_args()
 print(json.dumps(render(a.source,a.output,a.genre,a.synthetic),ensure_ascii=False))
