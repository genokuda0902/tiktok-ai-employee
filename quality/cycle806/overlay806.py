#!/usr/bin/env python3
"""cycle806: review-only 2-beat Japanese caption overlay on an existing MP4.
Reuses the original H.264 video and AAC audio. No TTS, posting or purchases.
Emphasis is sentence-relative; NOT word-level speech recognition.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
FPS=30
GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
'career','health_life','science','travel_food','product_life')
COLORS=('#66DDF0','#FFB2D5','#F7A7BC','#FFD182','#55E5D4',
'#8DC8F5','#A5EDB8','#B4BDFF','#FFC794','#92E5E2')
KEYS=('質問が違う','ゴール','今の数字','一つ','なぜ','今日','修正','小さな改善')
FONT_PATHS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
'/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
'/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf')
def font(n):
 p=next((p for p in FONT_PATHS if Path(p).exists()),None)
 if not p:raise RuntimeError('Noto Japanese font required')
 return ImageFont.truetype(p,n)
def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1400:])
 return p.stdout
def counts(m):
 if len(m.get('sentences',[]))!=8:raise ValueError('8 sentences required')
 t=0.;last=0;out=[]
 for s in m['sentences']:
  dur=float(s['seconds'])
  if not 1<dur<7:raise ValueError('invalid duration')
  t+=dur;now=round(t*FPS);out.append(now-last);last=now
 return out
def lines(text,f,width=810):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)));out=[];line=''
 for ch in text:
  if line and d.textlength(line+ch,font=f)>width:out.append(line);line=ch
  else:line+=ch
 if line:out.append(line)
 return out
def overlay(text,key,idx,stage,accent):
 im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle((100,1280,980,1665),radius=30,fill=(6,26,43,252),outline=accent,width=3)
 d.rounded_rectangle((128,1308,352,1360),radius=13,fill=(22,62,81,255))
 d.text((145,1318),'VOICE / 字幕',font=font(28),fill=accent)
 for size in (54,51,48,45,42):
  f=font(size);parts=lines(text,f)
  if len(parts)<=2:break
 if len(parts)>2:raise ValueError('caption too long')
 top=1395 if len(parts)==1 else 1369
 for j,line in enumerate(parts):
  w=d.textlength(line,font=f);x=round((1080-w)/2);y=top+j*72
  if x<128 or x+w>952:raise ValueError('caption out of safe area')
  pos=line.find(key)
  if stage and pos>=0:
   a,b,c=line[:pos],key,line[pos+len(key):]
   for piece,color in ((a,'#FFFFFF'),(b,accent),(c,'#FFFFFF')):
    d.text((x,y),piece,font=f,fill=color);x+=d.textlength(piece,font=f)
  else:d.text((x,y),line,font=f,fill='#FFFFFF')
 d.text((137,1561),f'{idx+1:02d} / 08',font=font(26),fill='#A9CCD9')
 d.rounded_rectangle((270,1573,936,1587),radius=6,fill='#294C5F')
 pw=round(666*(idx+(0.48 if stage==0 else 1))/8)
 d.rounded_rectangle((270,1573,270+pw,1587),radius=6,fill=accent)
 d.text((137,1614),'保存して、今日からひとつ実践。',font=font(28),fill='#B6D0DB')
 return im
def render(base,timing,out,genre='sales_business'):
 if genre not in GENRES or len(GENRES)!=10:raise ValueError('invalid genre contract')
 m=json.loads(Path(timing).read_text(encoding='utf-8'))
 if m.get('genre')!=genre or m.get('voice_engine')!='Open JTalk':raise ValueError('unexpected voice manifest')
 nframes=counts(m);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 directory=out.parent/'overlay_states';directory.mkdir(exist_ok=True)
 accent=COLORS[GENRES.index(genre)];entries=[];cues=[];start=0
 for i,(s,n) in enumerate(zip(m['sentences'],nframes)):
  if KEYS[i] not in s['text'] or '@' in s['text']:raise ValueError('unsafe/mismatched caption')
  n0=min(n-1,45 if i==0 else max(12,round(n*.42)))
  for stage,count in ((0,n0),(1,n-n0)):
   p=directory/f'{i+1:02d}_{stage}.png';overlay(s['text'],KEYS[i],i,stage,accent).save(p)
   entries.append((p,count))
  cues.append({'scene':i+1,'start_frame':start,'end_frame':start+n,'emphasis_frame':start+n0,'text':s['text']})
  start+=n
 manifest=out.parent/'overlay.ffconcat';l=['ffconcat version 1.0']
 for p,n in entries:l.extend([f"file '{p.resolve()}'",f'duration {n/FPS:.9f}'])
 l.append(f"file '{entries[-1][0].resolve()}'");manifest.write_text('\n'.join(l)+'\n')
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),'-f','concat','-safe','0','-i',str(manifest),
 '-filter_complex','[1:v]fps=30,format=rgba[ol];[0:v][ol]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]',
 '-map','[v]','-map','0:a:0','-frames:v',str(start),'-c:v','libx264','-preset','veryfast','-crf','19',
 '-c:a','copy','-movflags','+faststart',str(out)])
 run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
 probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video')
 a=next(s for s in probe['streams'] if s['codec_type']=='audio')
 if (v['width'],v['height'],int(v['nb_frames']))!=(1080,1920,start):raise RuntimeError('video QA mismatch')
 if v['codec_name']!='h264' or a['codec_name']!='aac' or a['sample_rate']!='48000':raise RuntimeError('audio QA mismatch')
 visual=ImageChops.difference(Image.open(entries[0][0]),Image.open(entries[1][0])).getbbox() is not None
 if not visual:raise RuntimeError('no visual change')
 q={'cycle':806,'genre':genre,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
 'improvement':'two-stage keyword emphasis and 1.5s hook, motion and Japanese AAC preserved',
 'resolution':[1080,1920],'fps':30,'frames':start,'duration':float(probe['format']['duration']),
 'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'audio_hz':int(a['sample_rate']),
 'caption_source':'same Open JTalk manifest as audio, sentence-level only',
 'visual_stage_difference':visual,'full_decode':'PASS','scene_cues':cues,
 'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'ten_genre_configs':len(GENRES),
 'license_review_required':True,'phone_playback_unverified':True,'employee_approval':False}
 (out.parent/'qa806.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
 return q
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--timing',required=True)
 p.add_argument('--output',required=True);p.add_argument('--genre',default='sales_business',choices=GENRES)
 a=p.parse_args();print(json.dumps(render(a.base,a.timing,a.output,a.genre),ensure_ascii=False,indent=2))
