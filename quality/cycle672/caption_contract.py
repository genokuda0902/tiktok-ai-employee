"""Reusable scene caption checks for review-only TikTok videos."""
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
REVIEW_POLICY={"publication":"NOT_APPROVED","caption_sync":"SCENE_TIMED_NOT_SPEECH_SYNCED"}

def validate_scene_captions(cues,suppressed,duration=20.0):
    if len(GENRES)!=10 or not cues or abs(cues[0][0])>1e-6 or abs(cues[-1][1]-duration)>1e-6:
        raise ValueError("invalid timeline")
    for i,(a,b,text) in enumerate(cues):
        if a>=b or not text or (i and abs(a-cues[i-1][1])>1e-6):
            raise ValueError("caption gap")
    for i,e in suppressed.items():
        if i<0 or i>=len(cues) or not e.get("reviewed") or not e.get("reason") or not e.get("existing_text"):
            raise ValueError("missing suppression evidence")
    return True

def select_burned_cues(cues,suppressed):
    validate_scene_captions(cues,suppressed,cues[-1][1])
    return [c for i,c in enumerate(cues) if i not in suppressed]
