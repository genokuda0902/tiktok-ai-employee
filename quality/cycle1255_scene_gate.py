"""Fail-closed scene-level review gate for silent prototypes (cycle1255).

This gate does NOT claim that visual captions are speech-synchronized.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    caption: str

def check_scenes(scenes, duration, has_japanese_narration=False):
    if not scenes or duration <= 0:
        raise ValueError("empty timeline")
    expected = 0.0
    for scene in scenes:
        if abs(scene.start - expected) > 0.04:
            raise ValueError("scene gap/overlap")
        if scene.end <= scene.start or scene.end > duration + 0.04:
            raise ValueError("invalid scene range")
        if not scene.caption.strip():
            raise ValueError("caption missing")
        expected = scene.end
    if abs(expected-duration) > 0.04:
        raise ValueError("duration mismatch")
    return {"timeline_valid": True, "narration_verified": False,
            "speech_synced_captions_verified": False,
            "publication_approved": False,
            "narration_present_claim": bool(has_japanese_narration)}

if __name__ == "__main__":
    print(check_scenes([Scene(0,3,"数字が伸びない理由"),
                        Scene(3,6,"まず工程を分ける"),
                        Scene(6,9,"改善結果を比較")],9))
