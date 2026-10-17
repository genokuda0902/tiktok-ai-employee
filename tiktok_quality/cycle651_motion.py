"""Cycle 651: zero-cost image-slide motion utilities.

No publishing. Existing Japanese audio is inherited and NOT transcript-verified.
"""
FPS = 30
BOUNDS = [0, 63, 130, 191, 238, 278, 362, 414, 468]
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
VOICE_NEWLY_GENERATED = False
SPOKEN_CAPTION_SEMANTIC_MATCH_VERIFIED = False
PUBLICATION_APPROVED = False

def zoom_expr(scene_index: int, count: int) -> str:
    """Return FFmpeg zoompan filter for 1080x1920 alternating 7.5% zoom."""
    if count < 2:
        raise ValueError("scene must have at least 2 frames")
    step = 0.075 / (count - 1)
    z = (f"1.075-{step:.9f}*on" if scene_index % 2
         else f"1+{step:.9f}*on")
    return (f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':d={count}:"
            "s=1080x1920:fps=30,format=yuv420p")

def frame_counts():
    return [b-a for a,b in zip(BOUNDS[:-1], BOUNDS[1:])]

def validate_genre(genre):
    if genre not in GENRES:
        raise ValueError("Unsupported genre")
    return genre
