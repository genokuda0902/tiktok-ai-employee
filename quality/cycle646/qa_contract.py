"""Genre-independent, fail-closed media QA. Review only: never posts or approves."""
from dataclasses import dataclass

GENRES = ("ai_work", "miniature", "before_after", "cooking", "beauty", "travel", "business", "education", "gadgets", "lifestyle")

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    caption: str

def validate_plan(scenes, duration=20.0, genre="ai_work"):
    if genre not in GENRES or not 15 <= duration <= 45:
        raise ValueError("invalid genre/duration")
    if not 6 <= len(scenes) <= 12:
        raise ValueError("invalid scene count")
    if abs(scenes[0].start) > 0.001 or abs(scenes[-1].end - duration) > 0.001:
        raise ValueError("timeline endpoints")
    for i, scene in enumerate(scenes):
        if not scene.caption or len(scene.caption) > 36:
            raise ValueError("caption missing or too long")
        if scene.end <= scene.start or (i and abs(scene.start-scenes[i-1].end) > 0.001):
            raise ValueError("timeline gap or overlap")
    if scenes[0].end > 2.5:
        raise ValueError("hook too late")
    return True

def evaluate_release(qa):
    required = ("mp4_decode", "vertical_1080x1920", "narration_japanese",
                "captions_semantic_sync", "assets_rights_approved",
                "human_content_approved", "employee_manual_post_only")
    return [key for key in required if qa.get(key) is not True]

def verify_spreadsheet(values, formula, result, chart):
    if formula != "=SUM(B2:B5)" or len(values) != 4:
        raise ValueError("invalid formula/data shape")
    if sum(values) != result or list(values) != list(chart):
        raise ValueError("arithmetic/chart mismatch")
    return True
