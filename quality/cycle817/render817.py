"""Cycle 817: clean-source slide renderer (no inherited encoded video).

Requires ffmpeg, ffprobe, Pillow. Eight original PNG slides + licensed Japanese
narration are user-reviewed inputs. This renderer neither downloads nor posts.
The voice activity estimator is not word-level forced alignment.
"""
from __future__ import annotations
import argparse, json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
GENRE_ACCENTS={
 'ai_work':'#73CBFF','beauty':'#FF9EC4','love_psychology':'#C3A2FF',
 'money_saving':'#FFD475','sales_business':'#5DE7C4','career':'#86B7FF',
 'health_life':'#B6E984','science':'#8DD9FF','travel_food':'#FFBB8C',
 'product_life':'#D8B0FF'}
PHRASES=[
 ['仕事ができる人は、','質問が','違う。'],
 ['まず、','目指すゴールを','確認する。'],
 ['次に、','今の数字を','確かめる。'],
 ['そして、','理想との差を','一つに絞る。'],
 ['原因には、','なぜを','三回重ねる。'],
 ['対策は、','今日できる','行動に変える。'],
 ['結果を見て、','また','修正する。'],
 ['小さな改善が、','強いチームを','つくる。']]

def run(cmd):
 return subprocess.run(cmd,check=True,capture_output=True,text=True)

def scene_frames(timing):
 data=json.loads(Path(timing).read_text(encoding='utf8'))
 sentences=data['sentences']
 if len(sentences)!=8: raise ValueError('Expected 8 scenes')
 if any(''.join(PHRASES[i])!=s['text'] for i,s in enumerate(sentences)):
  raise ValueError('Narration/phrase mismatch; do not publish mismatched captions')
 boundaries=[0]; elapsed=0
 for scene in sentences:
  elapsed+=float(scene['seconds'])
  boundaries.append(round(elapsed*FPS))
 if boundaries[-1]!=775: raise ValueError('Unexpected duration')
 return boundaries

def clean_slide(source, dest, accent):
 """Replace previously burned-in caption area before compositing new captions."""
 im=Image.open(source).convert('RGB')
 if im.size!=(1080,1920): raise ValueError('Wrong slide dimensions')
 # The source caption panel occupies y=1160..1420; remove it completely.
 # The surrounding background is dark blue and no meaningful art is below y=1160.
 d=ImageDraw.Draw(im)
 d.rectangle((0,1155,1079,1645),fill=(9,31,49))
 d.rounded_rectangle((64,1200,1016,1540),radius=34,fill=(5,23,39),outline=accent,width=4)
 d.rounded_rectangle((91,1215,320,1273),radius=18,fill=accent)
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',29)
 d.text((111,1224),'今日のポイント',font=font,fill=(5,29,42))
 # No rasterized subtitle text: all subtitles are separately timed ASS events.
 dest.parent.mkdir(parents=True,exist_ok=True)
 im.save(dest,optimize=True)

def ass_time(frames):
 centiseconds=round(frames*100/FPS)
 return f'{centiseconds//360000}:{centiseconds//6000%60:02}:{centiseconds//100%60:02}.{centiseconds%100:02}'

def detect_silence(audio, duration):
 proc=run(['ffmpeg','-hide_banner','-nostats','-i',str(audio),'-af',
  'silencedetect=noise=-34dB:d=0.16','-f','null','-'])
 starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',proc.stderr)]
 ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',proc.stderr)]
 return [(max(0,s),min(duration,ends[i] if i<len(ends) else duration)) for i,s in enumerate(starts)]

def speech_phases(start,end,silences):
 voiced=[];cur=start
 for a,b in silences:
  if b<=start or a>=end:continue
  a=max(start,a);b=min(end,b)
  if a>cur+0.07:voiced.append((cur,a))
  cur=max(cur,b)
 if cur<end-0.07:voiced.append((cur,end))
 if not voiced:return [start,start+(end-start)/3,start+2*(end-start)/3,end]
 onset=voiced[0][0];offset=min(end,voiced[-1][1]+0.12)
 gaps=[(voiced[i][1]+voiced[i+1][0])/2 for i in range(len(voiced)-1)]
 b1=gaps[0] if gaps else onset+(offset-onset)*0.34
 b2=gaps[1] if len(gaps)>1 else b1+(offset-b1)*0.50 if gaps else onset+(offset-onset)*0.68
 b1=max(onset+0.12,min(b1,offset-0.24))
 b2=max(b1+0.12,min(b2,offset-0.12))
 return [onset,b1,b2,offset]

def build_ass(boundaries,audio,dest):
 header='''[Script Info]
Title: cycle817 clean-source karaoke captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,80,&H00FFFFFF,&H00FFFFFF,&H00131B25,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,8,70,70,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 silences=detect_silence(audio,boundaries[-1]/FPS)
 events=[];phases=[]
 for i,parts in enumerate(PHRASES):
  start,end=[n/FPS for n in boundaries[i:i+2]]
  cuts=speech_phases(start,end,silences)
  # Convert to frames to avoid fractional-frame gaps and duplicate events.
  ticks=[max(boundaries[i],min(boundaries[i+1],round(x*FPS))) for x in cuts]
  for j in range(1,4):ticks[j]=max(ticks[j],ticks[j-1]+1)
  ticks[-1]=min(ticks[-1],boundaries[i+1])
  phases.append(ticks)
  for phase in range(3):
   spans=[]
   for j,p in enumerate(parts):
    color='&H0067CEFF&' if j==phase else '&H00FFFFFF&'
    spans.append(r'{\c'+color+'}'+p)
   content=r'{\an8\pos(540,1300)}'+spans[0]+r'\N'+spans[1]+spans[2]
   events.append(f'Dialogue: 0,{ass_time(ticks[phase])},{ass_time(ticks[phase+1])},Caption,,0,0,0,,{content}')
 dest.write_text(header+'\n'.join(events)+'\n',encoding='utf8')
 return phases

def make_filter(framecounts,ass_path):
 stages=[]
 for i,n in enumerate(framecounts):
  # Small center zoom. Each source still is rendered once, avoiding repeated MP4 re-encoding.
  z=f"min(1.0+on*0.00019,1.027)"
  stages.append(f"[{i}:v]zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps=30,setsar=1[v{i}]")
 joined=''.join(f'[v{i}]' for i in range(len(framecounts)))
 stages.append(f'{joined}concat=n=8:v=1:a=0[all]')
 stages.append(f'[all]ass={ass_path}:shaping=complex,format=yuv420p[out]')
 return ';'.join(stages)

def render(root:Path, output:Path, genre='sales_business'):
 if genre not in GENRE_ACCENTS:raise ValueError('Unsupported genre')
 src=root/'source';out=root/'output';out.mkdir(exist_ok=True,parents=True)
 timing=src/'voice_timing.json';audio=src/'voice.m4a'
 boundaries=scene_frames(timing)
 for i in range(1,9):
  clean_slide(src/f'scene_{i:02}.png',out/f'clean_scene_{i:02}.png',GENRE_ACCENTS[genre])
 ass=out/'captions817.ass';phases=build_ass(boundaries,audio,ass)
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error']
 for i in range(1,9):cmd+=['-i',str(out/f'clean_scene_{i:02}.png')]
 # Stage 1: render video only; keep audio separate so an interrupted video
 # encode cannot silently truncate the narration (observed in a previous run).
 video_only=out/'cycle817_video_only.mp4'
 cmd+=['-filter_complex',make_filter([b-a for a,b in zip(boundaries,boundaries[1:])],ass),
  '-map','[out]','-frames:v','775','-r','30','-c:v','libx264',
  '-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p',
  '-an','-movflags','+faststart',str(video_only)]
 run(cmd)
 # Stage 2: copy already encoded video, normalize the FULL original audio.
 run(['ffmpeg','-y','-hide_banner','-loglevel','error',
  '-i',str(video_only),'-i',str(audio),'-map','0:v:0','-map','1:a:0',
  '-c:v','copy','-af','loudnorm=I=-18:TP=-2:LRA=9',
  '-c:a','aac','-b:a','160k','-ar','48000','-t',str(boundaries[-1]/FPS),
  '-movflags','+faststart',str(output)])
 (out/'timing817.json').write_text(json.dumps({'boundaries_frames':boundaries,'caption_phases_frames':phases,
  'timing_method':'FFmpeg silencedetect pause guided; not word aligned',
  'audio_filter':'loudnorm I=-18 TP=-2 LRA=9 (single-pass)'},ensure_ascii=False,indent=2),encoding='utf8')
 return output

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--root',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--genre',choices=sorted(GENRE_ACCENTS),default='sales_business')
 a=p.parse_args();render(a.root,a.output,a.genre)
