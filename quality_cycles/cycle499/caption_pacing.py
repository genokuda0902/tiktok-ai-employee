"""Cycle499 review-only caption pacing contract shared across ten genres.
No natural Japanese narration is available in this cycle. Never mark approved.
"""
from dataclasses import dataclass
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理",
    "お金・節約", "営業・ビジネス", "転職・キャリア",
    "健康・生活改善", "雑学・科学", "旅行・グルメ",
    "商品比較・暮らし",
)
BEAT_SECONDS = (1.55, 1.65, 1.70, 1.80, 1.65, 1.85,
                1.75, 1.85, 1.65, 1.90, 1.65, 1.85)
CAPTIONS = (
    "「最近どう？」だけでは", "答えに困ることも。",
    "「特にないです」で終わる。", "具体的な話題を作ろう。",
    "今週うまくいったことは？", "小さな成功から聞いてみる。",
    "いま一番の障害は何？", "一緒に整理してみよう。",
    "来週まず何をする？", "小さな行動をひとつ決める。",
    "成功、障害、次の一歩。", "次の1on1で試してみよう。",
)
@dataclass(frozen=True)
class CaptionBeat:
    text: str
    start: float
    end: float
def timeline(captions=CAPTIONS, durations=BEAT_SECONDS):
    if len(captions) != len(durations) or not captions:
        raise ValueError("caption/duration mismatch")
    beats = []
    start = 0.0
    for s, dur in zip(captions, durations):
        if len(s) > 22 or not (1.55 <= dur <= 1.90):
            raise ValueError("unsafe caption reading load")
        end = round(start + dur, 3)
        beats.append(CaptionBeat(s, round(start, 3), end))
        start = end
    return tuple(beats)
def publish_gate(qa):
    return all((
        qa.get("native_japanese_voice") == "HUMAN_VERIFIED",
        qa.get("voice_caption_sync") == "PASS",
        qa.get("full_decode") == "PASS",
        qa.get("human_review") == "APPROVED",
        qa.get("publication") == "MANUAL_POST_APPROVED",
    ))
