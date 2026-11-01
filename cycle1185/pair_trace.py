#!/usr/bin/env python3
"""Review-only three-pair diagram trace; requires private 1080x1920 AAC source."""
import argparse
import json
import subprocess
from pathlib import Path

GENRE_ACCENTS={
 'ai':'0x4de0d2','business':'0x5fc5e8','money':'0xe7bc66',
 'learning':'0x8bcbff','health':'0x77d6aa','food':'0xf3a67a',
 'travel':'0x6fc9f2','beauty':'0xe4a8ce','career':'0xa6b7ff','life':'0xb5d1a2',
}
DEFAULT_PAIRS=[
 ((96,655,385,143),(553,763,420,104)),
 ((96,827,385,144),(553,885,420,106)),
 ((96,1001,385,149),(553,1003,420,108)),
]

def probe(path):
 r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)],check=True,text=True,capture_output=True)
 return json.loads(r.stdout)

def validate_layout(pairs):
 if len(pairs)!=3: raise ValueError('requires exactly three left/right pairs')
 for pair in pairs:
  if len(pair)!=2: raise ValueError('each pair requires two boxes')
  for rect in pair:
   if len(rect)!=4: raise ValueError('rectangle must be x,y,w,h')
   x,y,w,h=rect
   if not all(isinstance(z,int) for z in rect): raise ValueError('integer coordinates only')
   if not (40<=x and 390<=y and w>=80 and h>=50 and x+w<=1035 and y+h<=1150):
    raise ValueError('diagram outline outside safe region')
 return pairs

def chapter_window(meta,label='04/08'):
 for ch in meta.get('chapters',[]):
  if label in ch.get('tags',{}).get('title',''):
   return float(ch['start_time']),float(ch['end_time'])
 raise ValueError('chapter 04/08 not found')

def filter_graph(genre,start,end,pairs=DEFAULT_PAIRS):
 if genre not in GENRE_ACCENTS: raise ValueError('unknown genre')
 validate_layout(pairs)
 if end-start<2.6: raise ValueError('scene too short for three legible cues')
 color=GENRE_ACCENTS[genre]
 chain=[]
 for i,pair in enumerate(pairs):
  a=start+0.20+i*0.81
  b=min(end-0.12,a+0.69)
  for x,y,w,h in pair:
   chain.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}@0.88:t=5:enable='between(t,{a:.3f},{b:.3f})'")
 return '[0:v]'+','.join(chain)+',format=yuv420p[v]'

def render(source,output,genre='ai',pairs=DEFAULT_PAIRS,crf=18):
 source,output=Path(source),Path(output)
 if source.resolve()==output.resolve(): raise ValueError('source overwrite forbidden')
 if not source.is_file(): raise FileNotFoundError(source)
 meta=probe(source)
 vids=[s for s in meta['streams'] if s['codec_type']=='video']
 auds=[s for s in meta['streams'] if s['codec_type']=='audio']
 if len(vids)!=1 or len(auds)!=1 or auds[0]['codec_name']!='aac':
  raise ValueError('one video and one AAC narration required')
 v=vids[0]
 if (int(v['width']),int(v['height']),v['r_frame_rate'])!=(1080,1920,'30/1'):
  raise ValueError('1080x1920 30fps required')
 start,end=chapter_window(meta)
 graph=filter_graph(genre,start,end,pairs)
 output.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-filter_complex',graph,'-map','[v]','-map','0:a:0',
      '-map_metadata','0','-map_chapters','0','-c:v','libx264','-preset','veryfast',
      '-crf',str(crf),'-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 actual=probe(output)
 outv=next(s for s in actual['streams'] if s['codec_type']=='video')
 if int(outv['nb_frames'])!=int(v['nb_frames']): raise RuntimeError('frame count changed')
 return {'genre':genre,'scene_start':start,'scene_end':end,'pairs':pairs,
         'frame_count':int(outv['nb_frames']),'audio_copied':True,
         'publication_approved':False,'independent_japanese_asr':False}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('source');p.add_argument('output')
 p.add_argument('--genre',default='ai',choices=GENRE_ACCENTS)
 p.add_argument('--layout-json')
 a=p.parse_args()
 layout=json.loads(Path(a.layout_json).read_text()) if a.layout_json else DEFAULT_PAIRS
 print(json.dumps(render(a.source,a.output,a.genre,layout),ensure_ascii=False,indent=2))
