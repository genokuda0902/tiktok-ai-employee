"""Offline seven-band narration-reactive header. No ASR or publishing."""
from dataclasses import dataclass
import numpy as np
from scipy.signal import butter, sosfilt
FPS=30
BAR_COUNT=7
TEN_GENRES=('AI時短','雑学','料理','美容','お金','健康','旅行','商品','ストーリー','仕事術')
@dataclass(frozen=True)
class HeaderGeometry:
    x:int=570
    y:int=61
    width:int=180
    height:int=54
    def safe(self):
        return 440<=self.x and self.x+self.width<=760 and 0<=self.y<=120-self.height

def audio_bands(audio,sample_rate,frames):
    """Deterministic 7-band energy per video frame; not speech recognition."""
    if audio.ndim!=1 or sample_rate<12000 or frames<=0 or not np.all(np.isfinite(audio)):
        raise ValueError('valid mono audio >=12kHz and positive frames required')
    freqs=[(90,220),(220,420),(420,750),(750,1250),(1250,2100),(2100,3500),(3500,5500)]
    result=np.zeros((frames,7),dtype=np.float64)
    for k,(lo,hi) in enumerate(freqs):
        filtered=sosfilt(butter(2,[lo,hi],btype='bandpass',fs=sample_rate,output='sos'),audio)
        for f in range(frames):
            a=int(f*sample_rate/FPS);b=min(len(audio),int((f+1)*sample_rate/FPS))
            if b>a:result[f,k]=np.sqrt(np.mean(filtered[a:b]**2))
    for k in range(7):
        p90=np.percentile(result[:,k],90)
        result[:,k]=np.clip(result[:,k]/p90,0,1) if p90>1e-5 else 0
    for f in range(1,frames):result[f]=.60*result[f-1]+.40*result[f]
    return result

def bar_heights(bands):
    if bands.ndim!=2 or bands.shape[1]!=7:raise ValueError('seven bands required')
    return np.rint(4+39*np.sqrt(np.clip(bands,0,1))).astype(np.uint8)

def draw_bars(heights):
    import cv2
    if len(heights)!=7:raise ValueError('seven heights required')
    frame=np.zeros((54,180,3),dtype=np.uint8)
    for i,h in enumerate(heights):
        x=12+23*i;hh=int(np.clip(h,4,43));y=(54-hh)//2
        cv2.rectangle(frame,(x,y),(x+8,y+hh),(201,225,75),-1,lineType=cv2.LINE_AA)
    return frame

def cue_energy(audio,sr,intervals):
    values=[]
    for a,b in intervals:
        if a<0 or b<=a:raise ValueError('invalid cue')
        chunk=audio[int(a*sr):min(len(audio),int(b*sr))]
        values.append(round(float(np.sqrt(np.mean(chunk**2))) if len(chunk) else 0,6))
    return values
