"""Offline audio-only chapter-boundary QC. Not independent Japanese ASR."""
from __future__ import annotations
import json, subprocess
import numpy as np
SAMPLE_RATE=16000

def load_mono(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
      '-vn','-ac','1','-ar',str(SAMPLE_RATE),'-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4')

def rms_db(samples,t,span=0.12):
    lo=max(0,int((t-span/2)*SAMPLE_RATE))
    hi=min(len(samples),int((t+span/2)*SAMPLE_RATE))
    if hi<=lo: return -120.0
    return float(20*np.log10(np.sqrt(np.mean(
      np.square(samples[lo:hi],dtype=np.float64)))+1e-9))

def chapters(path):
    p=json.loads(subprocess.check_output(
      ['ffprobe','-v','error','-show_chapters','-of','json',str(path)],text=True))
    return [float(c['start_time']) for c in p.get('chapters',[])[1:]]

def report(path,threshold=-26.0):
    a=load_mono(path);cuts=chapters(path)
    rows=[{'time_s':t,'rms_dbfs':round(rms_db(a,t),2),
      'low_energy':rms_db(a,t)<threshold} for t in cuts]
    return {'scene_cuts':rows,'low_energy_count':sum(r['low_energy'] for r in rows),
      'total_cuts':len(rows),'threshold_dbfs':threshold,
      'semantic_transcription':'NOT_VERIFIED','subtitle_word_sync':'NOT_VERIFIED'}
