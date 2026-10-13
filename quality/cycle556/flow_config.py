"""Reusable 10-genre, zero-cost image-slide effect configuration."""
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善", "雑学・科学",
    "旅行・グルメ", "商品比較・暮らし",
)
VIDEO = {"width": 1080, "height": 1920, "fps": 30, "seconds": 12.5}
EFFECT = {
    "start_frame": 241, "num_frames": 39, "overlay_y": 770,
    "overlay_height": 460, "cards": (
        (24, 790, 328, 1110), (375, 790, 680, 1110), (725, 790, 1030, 1110)
    ), "arrows": ((328, 375), (680, 725)), "arrow_y": 962,
}
APPROVAL = {"human_review": True, "publication_approved": False, "auto_publish": False}

def smooth(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)

def card_intensity(card_index, seconds):
    phase = seconds - card_index * 0.37
    return (smooth(-0.08, 0.08, phase)
            * (1 - smooth(0.31, 0.55, phase))
            * smooth(0, 0.10, seconds)
            * (1 - smooth(1.12, 1.29, seconds)))
