"""Zero-cost 10-genre speech-safe transition placement. Human review only.
Full private MP4 renderer and original narration are NOT stored in this public repo.
Use FFmpeg silencedetect on voice-only source and pass detected (start,end) intervals.
"""
GENRES = ("ai_work","business","money","learning","health","lifestyle","psychology","science","history","travel")
SFX_DURATION = 0.18
MAX_SHIFT = 0.19
MIN_PAUSE = 0.20

def schedule(boundaries, pauses, genre="ai_work", duration=23.033):
    if genre not in GENRES:
        raise ValueError("Unknown genre; fail closed")
    if not boundaries or boundaries[0] <= 0 or boundaries[-1] >= duration:
        raise ValueError("Invalid timing")
    if any(a >= b for a,b in zip(boundaries,boundaries[1:])):
        raise ValueError("Boundaries not strictly increasing")
    result=[]
    for boundary in boundaries:
        candidates=[]
        for start,end in pauses:
            if end-start < MIN_PAUSE:
                continue
            lo=start+SFX_DURATION/2+0.002
            hi=end-SFX_DURATION/2-0.002
            if lo > hi:
                continue
            center=min(max(boundary,lo),hi)
            if abs(center-boundary) <= MAX_SHIFT:
                candidates.append((abs(center-boundary),center,start,end))
        if candidates:
            _,center,start,end=min(candidates)
            result.append({"boundary_s":boundary,"status":"PAUSE_PLACED",
                           "cue_center_s":round(center,5),
                           "pause_s":[start,end],
                           "shift_s":round(center-boundary,5)})
        else:
            result.append({"boundary_s":boundary,"status":"SUPPRESSED_NO_SAFE_PAUSE",
                           "cue_center_s":None,"pause_s":None,"shift_s":None})
    return result

def require_review_approval(approved=False):
    if not approved:
        raise PermissionError("Rights, speech and staff approval missing; posting forbidden")
    # Even with review flag, no posting integration exists in this module.
    return "REVIEW_ONLY"
