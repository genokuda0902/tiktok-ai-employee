"""Cycle503 reusable 10-genre quality contract. No publish permission is granted."""
GENRES = ("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約",
          "営業・ビジネス","転職・キャリア","健康・生活改善",
          "雑学・科学","旅行・グルメ","商品比較・暮らし")
RESOLUTION = (1080, 1920)
SAFE_TEXT_BOX = (90, 260, 820, 1360)
CAPTION_LIMIT = 20

def validate_timeline(beats):
    if len(beats) != 16:
        raise ValueError("expected exactly 16 beats")
    end = 0.0
    for i, beat in enumerate(beats):
        if beat["scene"] != i // 2 or beat["phase"] != i % 2:
            raise ValueError("scene/phase order")
        if abs(beat["start"] - end) > 0.005:
            raise ValueError("timeline gap or overlap")
        if beat["end"] <= beat["start"]:
            raise ValueError("non-positive duration")
        if not 0 < len(beat["caption"]) <= CAPTION_LIMIT:
            raise ValueError("caption length")
        if not beat.get("spoken"):
            raise ValueError("spoken script missing")
        end = beat["end"]
    if not 18 <= end <= 24:
        raise ValueError("duration out of range")
    return end

def release_gate(q):
    return all((
        q.get("resolution") == [1080, 1920],
        q.get("full_decode") == "PASS",
        q.get("native_japanese_voice") == "HUMAN_VERIFIED",
        q.get("voice_caption_sync") == "PASS",
        q.get("human_review") == "APPROVED",
        q.get("publication") == "MANUAL_POST_APPROVED",
    ))
