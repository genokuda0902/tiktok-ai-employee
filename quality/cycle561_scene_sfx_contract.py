"""Reusable fail-closed scene SFX and narration provenance contract (cycle561)."""
import math
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
CUES=(2.0,4.0,6.0,9.0,12.0,15.5,18.5)
def check_cues(cues=CUES,genre=GENRES[0],duration=20):
    if genre not in GENRES: raise ValueError("unsupported genre")
    if not 1<=len(cues)<=12: raise ValueError("cue count")
    if any(not .2<=t<=duration-.2 for t in cues): raise ValueError("cue bounds")
    if any(b-a<.3 for a,b in zip(cues,cues[1:])): raise ValueError("cue overlap")
    return True
def scene_tone(cues=CUES,sample_rate=44100):
    """Pure-Python mono PCM samples; original synthesis, no copyrighted samples."""
    check_cues(cues)
    out=[0.0]*round(20*sample_rate)
    length=round(.115*sample_rate)
    for stamp in cues:
        start=round(stamp*sample_rate)
        for i in range(length):
            t=i/sample_rate
            envelope=math.sin(math.pi*min(t/.115,1))**2*math.exp(-13*t)
            out[start+i]+=(math.sin(2*math.pi*630*t)+.3*math.sin(2*math.pi*1260*t))*envelope*.085
    if max(map(abs,out))>.10:raise ValueError("cue peak too loud")
    return out
def approval_gate(meta):
    """No voice/transcript or rights verification => never mark publishable."""
    return bool(meta.get("new_japanese_voice_verified") and
                meta.get("speech_caption_sync_verified") and
                meta.get("assets_rights_verified") and
                meta.get("employee_approved"))
