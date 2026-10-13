"""cycle557: fail-closed Japanese narration approval gate; not a language detector."""
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理",
    "お金・節約", "営業・ビジネス", "転職・キャリア",
    "健康・生活改善", "雑学・科学", "旅行・グルメ",
    "商品比較・暮らし",
)
def validate_genre(genre):
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    return True

def voice_approved(provenance, semantic_sync):
    if not isinstance(provenance, dict):
        return False
    return (
        provenance.get("source") not in (None, "", "inherited", "unknown")
        and provenance.get("native_ja_tts_verified_by_human") is True
        and provenance.get("rights_cleared") is True
        and semantic_sync is True
    )
