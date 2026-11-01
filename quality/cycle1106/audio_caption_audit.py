"""Signal-only 8-cue audio QA. Does NOT transcribe Japanese or prove subtitle sync.

Accepts local H264/AAC MP4; analyzes decoded PCM RMS in configurable visual cue windows.
Not a VAD/ASR, not proof of speech or Japanese pronunciation.
"""
import argparse
import json
import math
import subprocess
from pathlib import Path
import numpy as np

DEFAULT_CUTS=[0,2.9,5.7,8.7,11.5,14.3,17.333333,20.3,23.033333]

def analyze_pcm(pcm,sample_rate,cuts,frame_ms=20):
 if len(cuts)<2 or cuts[0]<0 or any(b<=a for a,b in zip(cuts,cuts[1:])):raise ValueError('bad cue boundaries')
 if frame_ms<=0 or sample_rate<=0:raise ValueError('bad sampling')
 out=[]
 for i,(start,end) in enumerate(zip(cuts,cuts[1:]),1):
  chunk=pcm[round(start*sample_rate):round(end*sample_rate)]
  if len(chunk)==0:raise ValueError('empty cue')
  rms=float(np.sqrt(np.mean(np.square(chunk.astype(np.float64)))))
  peak=float(np.max(np.abs(chunk)))
  out.append({'cue':i,'start_s':round(start,3),'end_s':round(end,3),
              'rms_dbfs':round(20*math.log10(max(rms,1e-9)),2),
              'peak_dbfs':round(20*math.log10(max(peak,1e-9)),2),
              'nonzero_signal':bool(rms>1e-5)})
 return out

def decode(path):
 p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1'],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1000:])
 return np.frombuffer(p.stdout,dtype='<f4').copy()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--video',required=True);ap.add_argument('--out',required=True)
 ap.add_argument('--cuts',default=','.join(map(str,DEFAULT_CUTS)))
 a=ap.parse_args();cuts=[float(x) for x in a.cuts.split(',')]
 result={'scope':'signal-energy only; not ASR, not speech detection, not semantic/sync verification',
         'cut_source':'approximate visual scene boundaries; NOT forced aligned',
         'cues':analyze_pcm(decode(a.video),16000,cuts)}
 Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
