"""Keep captions identical to their planned Japanese narration script."""
GENRES = ("AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
          "営業・ビジネス", "転職・キャリア", "健康・生活改善",
          "雑学・科学", "旅行・グルメ", "商品比較・暮らし")

def split_caption(text, max_chars=16):
    if not text:
        raise ValueError("empty text")
    if len(text) <= max_chars:
        return text, ""
    mid = (len(text) + 1) // 2
    if max(mid, len(text) - mid) > max_chars:
        raise ValueError("caption too long")
    return text[:mid], text[mid:]

def validate_script_contract(items):
    proof = []
    previous_end = 0
    for scene in items:
        start, end = scene["start"], scene["end"]
        if start < previous_end or end <= start:
            raise ValueError("invalid timing")
        first, second = split_caption(scene["spoken_text"])
        proof.append({"scene": scene["scene"], "script_exact": first + second == scene["spoken_text"]})
        previous_end = end
    return proof
