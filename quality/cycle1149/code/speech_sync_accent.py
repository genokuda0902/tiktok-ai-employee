"""Review-only 10-genre narration-energy onset accent; NOT Japanese ASR.
Original Japanese audio is stream-copied; no external media or auto posting.
"""
from __future__ import annotations
import argparse, json, math, subprocess
from pathlib import Path
import numpy as np

SR=16000
BOUNDARIES=[0.,3.133,5.6,8.233,11.,13.733,16.633,19.167]
CAPTION_TOP=1363
CAPTION_LEFT=94
ACCENT_LENGTH=252
ACCENT_HEIGHT=7
THEMES={
 'ai-work':'61f6e2','finance':'d5b76a','career':'a1d2ff',
 'health':'7fdeb7','learning':'9d9aff','travel':'ffbd8b',
 'technology':'72e3ff','business':'79dfcd','life':'f2a7c9',
 'history':'e5c78f',
}

def capture_pcm(path):
 p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                   '-ac','1','-ar',str(SR),'-f','f32le','-'],
                  stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 return np.frombuffer(p.stdout,dtype='<f4').copy()

def db_rms(pcm,start,length=.065):
 a=max(0,round(start*SR));b=min(len(pcm),round((start+length)*SR))
 if b<=a:return -120.
 rms=float(np.sqrt(np.mean(pcm[a:b].astype(np.float64)**2)))
 return 20*math.log10(max(1e-10,rms))

def detect_onsets(pcm,boundaries=BOUNDARIES,threshold_db=-27.):
 onsets=[];duration=len(pcm)/SR
 for i,start in enumerate(boundaries):
  stop=min(duration-.15,(boundaries[i+1] if i+1<len(boundaries) else duration)-.18)
  chosen=None;t=start+.14
  while t<min(start+1.1,stop):
   if db_rms(pcm,t)>=threshold_db and db_rms(pcm,t+.055)>=threshold_db:
    chosen=round(t,3);break
   t+=.02
  onsets.append(chosen)
 return onsets

def filtergraph(onsets,theme='ai-work'):
 if theme not in THEMES:raise ValueError('Unknown theme')
 color=THEMES[theme];filters=[]
 for onset in onsets:
  if onset is None:continue
  for step in range(4):
   a=onset+step*.1;b=onset+(step+1)*.1-.001
   w=round(ACCENT_LENGTH*(step+1)/4)
   filters.append(f'drawbox=x={CAPTION_LEFT}:y={CAPTION_TOP}:w={w}:h={ACCENT_HEIGHT}:'
                  f'color=0x{color}@0.85:t=fill:enable=between(t\\,{a:.3f}\\,{b:.3f})')
 return ','.join(filters) if filters else 'null'

def run(source,output,theme='ai-work',report=None,preset='veryfast'):
 source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 onsets=detect_onsets(capture_pcm(source))
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
  '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
  '-vf',filtergraph(onsets,theme),'-c:v','libx264','-preset',preset,
  '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True)
 result={'source':str(source),'output':str(output),'genre':theme,
         'chapter_boundaries':BOUNDARIES,'voice_energy_onsets':onsets,
         'onset_offsets_ms':[None if o is None else round((o-b)*1000)
                             for o,b in zip(onsets,BOUNDARIES)],
         'threshold_dbfs':-27.,'effect':'four-step 400ms caption-top accent',
         'meaning_or_asr_verified':False,'commercial_rights_verified':False,
         'human_review_required':True,'publication_approved':False}
 if report:Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('source');p.add_argument('output')
 p.add_argument('--theme',default='ai-work');p.add_argument('--report')
 p.add_argument('--preset',default='veryfast')
 a=p.parse_args();print(json.dumps(run(a.source,a.output,a.theme,a.report,a.preset),ensure_ascii=False))
