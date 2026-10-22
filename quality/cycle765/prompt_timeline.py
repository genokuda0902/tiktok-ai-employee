"""Reusable review-only 30fps prompt-entry timeline for 10 TikTok genres.

This pure-Python contract is used by cycle765's full offline Pillow/FFmpeg
renderer. It never executes an AI request or authorizes publication.
"""
from __future__ import annotations

FPS = 30
START = 195
END = 299
STAGES = tuple((START + 15 * i, START + 15 * i + 14) for i in range(7))
PROMPT = "この売上データを集計して、\n月別の棒グラフを作成。\n合計も計算して。"
PREFIX = (0, 8, 18, 29, 40, 999, 999)
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)

def prompt_at(stage: int) -> str:
    if not isinstance(stage, int) or not 0 <= stage < len(STAGES):
        raise ValueError("invalid stage")
    return PROMPT[:PREFIX[stage]]

def validate_review_manifest(config: dict) -> None:
    if config.get("genre") not in GENRES:
        raise ValueError("unknown genre")
    if config.get("status") != "HUMAN_REVIEW":
        raise ValueError("approval gate")
    if config.get("post_policy") != "employee_manual_after_approval":
        raise ValueError("no auto posting")
    if config.get("asset_origin") != "original_synthetic_pillow":
        raise ValueError("asset rights gate")
    if config.get("synthetic_data") is not True:
        raise ValueError("data rights gate")
    if config.get("sales") != [120000, 150000, 200000, 180000]:
        raise ValueError("synthetic data mismatch")

def ffmpeg_splice_filter() -> str:
    """Frame-exact replacement: first 195, new 105, last 519 frames."""
    return (
        "[0:v]trim=start_frame=0:end_frame=195,setpts=PTS-STARTPTS[a];"
        "[1:v]setpts=PTS-STARTPTS[b];"
        "[0:v]trim=start_frame=300,setpts=PTS-STARTPTS[c];"
        "[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[out]"
    )
