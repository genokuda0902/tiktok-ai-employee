"""Review-only provenance and narration gate shared by ten TikTok genres.
No publication approval is inferred from a generated MP4.
"""
from dataclasses import dataclass
from typing import Mapping

GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)

@dataclass(frozen=True)
class Asset:
    asset_id: str
    origin: str
    public_rights_approved: bool = False
    privacy_approved: bool = False

def review_gate(genre: str, assets: tuple[Asset, ...], audio: Mapping[str, object]) -> dict:
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    if not assets or len({a.asset_id for a in assets}) != len(assets):
        raise ValueError("Missing or duplicated assets")
    for a in assets:
        if not a.asset_id or not a.origin:
            raise ValueError("Asset provenance missing")
    rights = all(a.public_rights_approved and a.privacy_approved for a in assets)
    voice = (audio.get("japanese_narration") is True
             and audio.get("voice_caption_sync_verified") is True)
    human = audio.get("human_approved") is True
    return {
        "genre": genre,
        "assets": len(assets),
        "rights_approved": rights,
        "japanese_voice_approved": voice,
        "human_approved": human,
        "publication": "APPROVED_FOR_MANUAL_POST" if rights and voice and human else "NOT_APPROVED",
        "posting_mode": "MANUAL_ONLY",
    }
