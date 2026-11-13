"""Portable scene subtitle timing for review-only videos."""

def srt_timestamp(seconds):
    if seconds < 0: raise ValueError("negative time")
    ms=round(seconds*1000)
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"

def scene_srt(captions, duration):
    if not captions or duration <= 0: raise ValueError("invalid scenes")
    if any(not str(c).strip() for c in captions): raise ValueError("blank caption")
    step=duration/len(captions)
    return "".join(f"{i+1}\n{srt_timestamp(i*step)} --> {srt_timestamp((i+1)*step)}\n{caption}\n\n" for i,caption in enumerate(captions))
