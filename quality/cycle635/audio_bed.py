"""Reusable, sample-free ambient score with narration-aware ducking.
For TikTok image slides. This does not approve posting or replace Japanese speech.
"""
import numpy as np

SR=48000
FPS=30
FRAME_BOUNDARIES=(0,63,130,183,230,278,362,415,468)
CHORDS=((130.81,155.56,196.00),(103.83,155.56,207.65),
        (155.56,196.00,233.08),(116.54,174.61,233.08))

def synthesize(voice, sample_rate=SR):
    """Return original mono music bed. voice: stereo float PCM ndarray."""
    n=len(voice)
    t=np.arange(n,dtype=np.float64)/sample_rate
    duration=n/sample_rate
    bed=np.zeros(n,dtype=np.float64)
    for j,(a,b,c) in enumerate(CHORDS):
        center=(j+0.5)*duration/4
        env=np.maximum(0,1-np.abs(t-center)/(duration/4))**1.3
        bed+=.0062*env*(np.sin(2*np.pi*a*t)+.65*np.sin(2*np.pi*b*t)+.45*np.sin(2*np.pi*c*t))/2.1
    for j,frame in enumerate(FRAME_BOUNDARIES[:-1]):
        u=t-frame/FPS
        mask=(u>=0)&(u<.38)
        z=u[mask]
        hz=(523.25,587.33,659.25,698.46)[j%4]
        bed[mask]+=.009*np.minimum(1,z/.016)*np.exp(-11*z)*np.sin(2*np.pi*hz*z+.08*np.sin(2*np.pi*3*z))
    mono=voice.mean(axis=1)
    block=max(1,int(sample_rate*.05))
    rms=np.sqrt([np.mean(mono[i:i+block]**2) for i in range(0,n,block)])
    smooth=np.convolve(rms,np.ones(7)/7,mode='same')
    gain=np.interp(smooth,[0,.015,.04,.12],[.9,.72,.30,.18])
    bed*=np.interp(np.arange(n),np.minimum(np.arange(len(gain))*block,n-1),gain)
    bed*=np.minimum(1,t/.08)*np.minimum(1,np.maximum(0,duration-t)/.18)
    return bed.astype(np.float32)

def mix(voice,bed):
    """Mix without overwriting original speech; requires human audio QA."""
    if voice.ndim!=2 or voice.shape[1]!=2 or len(voice)!=len(bed):
        raise ValueError("expected stereo PCM and matching mono bed")
    return np.clip(voice+bed[:,None],-.99,.99)

STATUS="HUMAN_REVIEW"
PUBLICATION="NOT_APPROVED"
