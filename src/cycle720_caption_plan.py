"""Cycle720 shared subtitle plan. No external dependencies, no posting side effects."""
from __future__ import annotations

GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善", "雑学・科学",
    "旅行・グルメ", "商品比較・暮らし",
)
PHRASES = (
    ("この基板、", "実はパソコン。"),
    ("手のひらサイズ、", "でも本格派。"),
    ("画面につなげば、", "操作できる。"),
    ("必要なのは、", "三つの接続。"),
    ("LEDも", "光らせられる。"),
    ("入力、処理、", "出力。"),
    ("最初は、", "たった一行。"),
    ("保存して、", "あとで試そう。"),
)
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=7"


def plan(scene_timings, phrases=PHRASES):
    """Build estimated two-phrase cues; exact word sync is NOT claimed.

    Input scene_timings: records with start_s/end_s/text. Output is JSON-safe.
    """
    if len(scene_timings) != len(phrases):
        raise ValueError("scene and phrase counts must match")
    cues = []
    for idx, (row, parts) in enumerate(zip(scene_timings, phrases), 1):
        if "".join(parts) != row["text"]:
            raise ValueError(f"scene {idx}: TTS text differs from captions")
        start, end = float(row["start_s"]), float(row["end_s"])
        if not end > start:
            raise ValueError(f"scene {idx}: invalid duration")
        left_chars = len(parts[0].replace("、", "").replace("。", ""))
        right_chars = len(parts[1].replace("、", "").replace("。", ""))
        boundary = round(start + (end - start) * left_chars / (left_chars + right_chars), 3)
        if not start < boundary < end:
            raise ValueError(f"scene {idx}: invalid boundary")
        cues.append({"scene": idx, "start_s": start, "boundary_s": boundary,
                     "end_s": end, "phrases": list(parts),
                     "timing_method": "text_proportional_estimate_not_ASR"})
    return cues


def validate(cues):
    if len(cues) != 8 or len(GENRES) != 10:
        return False
    for idx, c in enumerate(cues):
        if c["scene"] != idx + 1 or not (c["start_s"] < c["boundary_s"] < c["end_s"]):
            return False
        if idx and abs(cues[idx - 1]["end_s"] - c["start_s"]) > 0.002:
            return False
    return True
