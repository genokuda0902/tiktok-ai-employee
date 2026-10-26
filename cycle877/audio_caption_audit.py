"""Objective non-silence vs expected caption windows, NOT speech recognition.

This deliberately does not infer Japanese words or semantic correctness. Background
music can trigger activity. Reports acoustic evidence only; manual listening/ASR
and phone QA remain publication blockers.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import numpy as np

CAPTION_WINDOWS=((.27,2.93),(3.31,5.60),(5.90,8.23),(8.52,11.10),
                 (11.41,13.97),(14.28,16.93),(17.26,19.50),(19.86,23.03))

def active_mask(samples,sr=16000,frame_ms=20,threshold_db=-34):
 if sr<=0 or frame_ms<=0:raise ValueError('invalid sample rate')
 n=max(1,round(sr*frame_ms/1000))
 count=len(samples)//n
 if count==0:raise ValueError('no audio')
 x=np.asarray(samples[:count*n],dtype=np.float64).reshape(count,n)
 rms=np.sqrt(np.mean(x*x,axis=1)+1e-12)
 return 20*np.log10(rms)>threshold_db

def decode_pcm(path,sr=16000):
 b=subprocess.run(['ffmpeg','-v','error','-nostdin','-i',str(path),'-map','0:a:0',
                   '-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True,
                  check=True,timeout=90).stdout
 return np.frombuffer(b,dtype='<i2').astype(np.float64)/32768

def audit(path,windows=CAPTION_WINDOWS,threshold_db=-34):
 pcm=decode_pcm(path);mask=active_mask(pcm,threshold_db=threshold_db)
 result=[]
 for start,end in windows:
  if not (0<=start<end<=len(pcm)/16000+.04):raise ValueError('bad caption timing')
  a,b=round(start*50),min(len(mask),round(end*50))
  if b<=a:raise ValueError('empty caption')
  coverage=float(mask[a:b].mean())
  result.append({'start_s':start,'end_s':end,'audible_fraction':round(coverage,3),
                 'contains_non_silent_audio':bool(mask[a:b].any())})
 return {'method':'20ms mono RMS > -34 dBFS, may include music/noise',
         'caption_windows':result,
         'all_caption_windows_have_audio':all(x['contains_non_silent_audio'] for x in result),
         'japanese_transcription_verified':False,'caption_semantics_verified':False,
         'word_level_alignment_verified':False,'voice_naturalness_verified':False,
         'publication_approved':False}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--video',required=True);p.add_argument('--report',required=True)
 a=p.parse_args();r=audit(a.video)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False))
