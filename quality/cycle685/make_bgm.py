"""Original, no-sample synthetic music bed. This is NOT Japanese narration."""
from pathlib import Path
import wave
import numpy as np
def synth_bgm(path,duration=20.0,sample_rate=48000):
    if duration<=0 or sample_rate<16000: raise ValueError('invalid audio settings')
    n=round(duration*sample_rate);t=np.arange(n,dtype=np.float64)/sample_rate
    chords=((261.63,329.63,392.),(220.,261.63,329.63),(174.61,220.,261.63),(196.,246.94,293.66))
    bed=np.zeros(n,dtype=np.float64)
    for i,chord in enumerate(chords):
        lo=int(i*5*sample_rate);hi=min(n,int((i+1)*5*sample_rate))
        if lo>=n:break
        u=t[lo:hi]-i*5
        ramp=np.minimum(1,np.maximum(0,u/.25))*np.minimum(1,np.maximum(0,(5-u)/.35))
        pad=sum(np.sin(2*np.pi*f*u+.13*j) for j,f in enumerate(chord))/3
        bed[lo:hi]+=0.050*pad*ramp
    for k in range(int(duration*2)):
        lo=int(k*.5*sample_rate);hi=min(n,lo+int(.16*sample_rate))
        if lo>=n:break
        u=np.arange(hi-lo)/sample_rate
        bed[lo:hi]+=0.032*np.sin(2*np.pi*(740-230*u)*u)*np.exp(-26*u)
    for k in range(int(duration)):
        lo=int(k*sample_rate);hi=min(n,lo+int(.18*sample_rate))
        if lo>=n:break
        u=np.arange(hi-lo)/sample_rate
        bed[lo:hi]+=0.045*np.sin(2*np.pi*(84-40*u)*u)*np.exp(-25*u)
    bed*=np.maximum(0,np.minimum(1,t/.35)*np.minimum(1,(duration-t)/.55))
    pcm=np.clip(np.stack((bed,np.roll(bed,29)*.98),axis=-1),-1,1)
    out=Path(path);out.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(out),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sample_rate)
        w.writeframes((pcm*32767).astype('<i2').tobytes())
    return out
