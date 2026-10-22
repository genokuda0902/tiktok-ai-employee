"""Cycle771 review-only quality contract, shared by ten genres."""
GENRES = {
    "AI・仕事効率化": "#36E1D5",
    "美容・身だしなみ": "#F3A4D1",
    "恋愛・心理": "#FF99AB",
    "お金・節約": "#F6CE72",
    "営業・ビジネス": "#82B5FF",
    "転職・キャリア": "#AEA9F5",
    "健康・生活改善": "#89D6B4",
    "雑学・科学": "#89DDF1",
    "旅行・グルメ": "#FFB47E",
    "商品比較・暮らし": "#CBB5FA",
}
FPS = 30
WIDTH = 1080
HEIGHT = 1920
START_FRAME = 729
END_FRAME = 819
SAFE = (80, 180, 960, 1590)
VOICE = "保存して、あとで試してみて。"
CAPTION = "保存して、あとで試そう"

def validate(config):
    if config.get("genre") not in GENRES:
        raise ValueError("unknown genre")
    if set(config.get("supported_genres", [])) != set(GENRES):
        raise ValueError("genre contract mismatch")
    if config.get("quality_approved") is not False:
        raise ValueError("quality approval missing")
    if config.get("status") != "HUMAN_REVIEW":
        raise ValueError("review state required")
    if config.get("post_policy") != "employee_manual_after_approval":
        raise ValueError("manual posting only")
    if config.get("media_rights") != "unverified_review_only":
        raise ValueError("inherited media not scoped")
    if config.get("narration_cue") != VOICE or config.get("onscreen_cta") != CAPTION:
        raise ValueError("voice and caption do not match")
    if config.get("claim") != "synthetic_arithmetic_only":
        raise ValueError("unverified claim")
    return True
