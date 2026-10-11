"""Reusable 10-genre 8-scene/16-beat contract; fails closed without real Japanese speech."""
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
SIZE=(1080,1920)
SAFE_BOX=(75,260,930,1550)
MAX_CHARS=20
def validate(beats):
    if len(beats)!=16: raise ValueError("expected 16 beats")
    end=0.
    for k,b in enumerate(beats):
        if b["scene"]!=k//2 or b["phase"]!=k%2: raise ValueError("scene/phase")
        if abs(b["start"]-end)>.002: raise ValueError("gap/overlap")
        if b["end"]<=b["start"]: raise ValueError("duration")
        if not 0<len(b["caption"])<=MAX_CHARS: raise ValueError("caption")
        if not b.get("spoken"): raise ValueError("missing spoken text")
        end=b["end"]
    if not 18<=end<=24: raise ValueError("duration outside 18-24s")
    return end
def release_gate(q):
    return all((q.get("resolution")==[1080,1920],
      q.get("full_decode")=="PASS",q.get("native_japanese_voice")=="HUMAN_VERIFIED",
      q.get("voice_caption_sync")=="PASS",q.get("human_review")=="APPROVED",
      q.get("publication")=="MANUAL_POST_APPROVED"))
