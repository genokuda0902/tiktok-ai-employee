"""Deterministic original audio cues for cycle605. No samples, no narration."""
import numpy as np

SAMPLE_RATE = 44100
GENRES = ("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約",
          "営業・ビジネス","転職・キャリア","健康・生活改善",
          "雑学・科学","旅行・グルメ","商品比較・暮らし")
CUES = (0.25,2.1,4.2,6.35,8.4,10.45,12.65,14.7,16.65,18.55)

def soundtrack(seconds, genre="AI・仕事効率化"):
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    n = round(seconds * SAMPLE_RATE)
    t = np.arange(n) / SAMPLE_RATE
    y = np.zeros(n, dtype=np.float64)
    beat = 60.0 / 110.0
    for k in range(int(seconds / beat) + 2):
        start = round(k * beat * SAMPLE_RATE)
        if start >= n: break
        count = min(round(0.2*SAMPLE_RATE), n-start)
        u = np.arange(count) / SAMPLE_RATE
        y[start:start+count] += .08*np.sin(2*np.pi*80*u)*np.exp(-25*u)
    for i, cue in enumerate(CUES):
        start = round(cue * SAMPLE_RATE)
        if start >= n: continue
        count = min(round(.15*SAMPLE_RATE),n-start)
        u = np.arange(count) / SAMPLE_RATE
        y[start:start+count] += .05*np.sin(2*np.pi*(660+220*(i%2))*u)*np.exp(-28*u)
    fade = np.clip(t/.3,0,1)*np.clip((seconds-t)/.5,0,1)
    y = y*fade + .012*np.sin(2*np.pi*220*t)*fade
    return np.column_stack([y, np.roll(y,66)*.97]).astype("float32")
