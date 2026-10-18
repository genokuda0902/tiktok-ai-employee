"""Original, zero-cost music bed for review-only TikTok prototypes.
No third-party samples, uploads, or publishing.
"""
import numpy as np
import wave
SAMPLE_RATE=48000
SECONDS=20
CUES=(0,2,4,6,8,10,14,16,18)

def soundtrack():
    sr=SAMPLE_RATE
    n=sr*SECONDS
    t=np.arange(n,dtype=np.float64)/sr
    x=np.zeros(n,dtype=np.float64)
    chords=((196.00,233.08,293.66),(174.61,220.00,261.63),
            (164.81,196.00,246.94),(174.61,220.00,293.66))
    for k,notes in enumerate(chords):
        mask=(t>=5*k)&(t<5*(k+1))
        q=t[mask]-5*k
        env=np.sin(np.pi*q/5)**.7
        x[mask]+=.055*env*sum(
            np.sin(2*np.pi*f*q+.25*np.sin(2*np.pi*.17*q))/(j+2)
            for j,f in enumerate(notes))
    for at in CUES:
        i=int(at*sr);q=np.arange(int(.23*sr))/sr
        x[i:i+len(q)]+=.058*np.sin(2*np.pi*(128-72*q)*q)*np.exp(-q*20)
        x[i:i+len(q)]+=.023*np.sin(2*np.pi*(700+220*q)*q)*np.exp(-q*30)
    for at in np.arange(.5,SECONDS,.5):
        i=int(at*sr);q=np.arange(int(.045*sr))/sr
        x[i:i+len(q)]+=.0055*np.sin(2*np.pi*3500*q)*np.exp(-q*130)
    fade=np.minimum(1,np.minimum(t/.2,(SECONDS-t)/.45))
    x*=np.maximum(0,fade)
    delayed=np.roll(x,37);delayed[:37]=0
    result=np.stack([.91*x+.09*delayed,.82*x+.18*delayed],axis=1)
    if np.max(np.abs(result))>=1:raise ValueError("Audio clipping")
    return result

def save_wav(path):
    data=(soundtrack()*32767).astype('<i2')
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SAMPLE_RATE)
        w.writeframes(data.tobytes())
