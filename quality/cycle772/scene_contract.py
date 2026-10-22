"""Cycle772 review-only, genre-neutral evidence-scene contract.

Local final renderer is supplied with the review MP4 ZIP. This module contains
the reusable quality/rights/number invariants and a synthetic CI smoke frame.
It does not access or publish the user-provided reference asset.
"""
from __future__ import annotations
import hashlib
from pathlib import Path

GENRES = {
    "AI・仕事効率化": "#49E1DC", "美容・身だしなみ": "#F5B0D5",
    "恋愛・心理": "#F99CB4", "お金・節約": "#F4D478",
    "営業・ビジネス": "#86B9FF", "転職・キャリア": "#B8ACF7",
    "健康・生活改善": "#92DAB9", "雑学・科学": "#8DDEEF",
    "旅行・グルメ": "#FFB985", "商品比較・暮らし": "#D1B9FA",
}
WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_START, SCENE_END = 493, 604
SAFE = (78, 180, 1000, 1600)
DATA = {"1月": 120000, "2月": 150000, "3月": 200000, "4月": 180000}
EXPECTED_CUE = "三月二十万円、四月十八万円。"


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(manifest, source=None, storyboard=None):
    if manifest.get("genre") not in GENRES:
        raise ValueError("unknown genre")
    if set(manifest.get("supported_genres", [])) != set(GENRES):
        raise ValueError("ten-genre contract mismatch")
    if manifest.get("review_status") != "HUMAN_REVIEW" or manifest.get("quality_approved") is not False:
        raise ValueError("publication not approved")
    if manifest.get("post_policy") != "employee_manual_after_approval":
        raise ValueError("automatic posting forbidden")
    if manifest.get("media_rights") != "unverified_review_only":
        raise ValueError("asset rights not verified")
    if manifest.get("source_origin") != "user_provided_storyboard_review_only":
        raise ValueError("asset provenance missing")
    if manifest.get("claim") != "synthetic_comparison_only" or manifest.get("synthetic_data") is not True:
        raise ValueError("unsupported result claim")
    if manifest.get("narration_cue") != EXPECTED_CUE:
        raise ValueError("narration mismatch")
    if manifest.get("data") != DATA or sum(DATA.values()) != 650000:
        raise ValueError("unverified dataset")
    if DATA["4月"] - DATA["3月"] != -20000:
        raise ValueError("arithmetic mismatch")
    if source is not None and sha256(source) != manifest.get("source_sha256"):
        raise ValueError("source video checksum mismatch")
    if storyboard is not None and sha256(storyboard) != manifest.get("storyboard_sha256"):
        raise ValueError("storyboard checksum mismatch")
    return True


def safe_bbox(box):
    return SAFE[0] <= box[0] and box[2] <= SAFE[2] and SAFE[1] <= box[1] and box[3] <= SAFE[3]


def synthetic_smoke_frame(genre):
    """Public-safe smoke frame only. NOT the final inherited-media video."""
    from PIL import Image, ImageDraw, ImageFont
    if genre not in GENRES:
        raise ValueError("unknown genre")
    im = Image.new("RGB", (WIDTH, HEIGHT), (5, 20, 39))
    d = ImageDraw.Draw(im)
    accent = tuple(bytes.fromhex(GENRES[genre][1:]))
    d.rounded_rectangle((85, 250, 990, 1540), radius=40, outline=accent, width=5)
    d.rounded_rectangle((120, 550, 520, 1110), radius=30, fill=(20, 56, 75))
    d.rounded_rectangle((565, 550, 960, 1110), radius=30, fill=(20, 56, 75))
    d.rounded_rectangle((175, 810, 450, 1030), radius=20, fill=(61, 184, 230))
    d.rounded_rectangle((625, 835, 900, 1030), radius=20, fill=accent)
    d.rounded_rectangle((120, 1200, 960, 1430), radius=28, outline=accent, width=4)
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    f = ImageFont.truetype(font_path, 55)
    for xy, value in [((140, 650), "3月 200,000円"), ((590, 650), "4月 180,000円"), ((180, 1250), "前月比 −20,000円")]:
        box = d.textbbox(xy, value, font=f)
        if not safe_bbox(box):
            raise ValueError("unsafe text")
        d.text(xy, value, font=f, fill=(245, 251, 255))
    return im
