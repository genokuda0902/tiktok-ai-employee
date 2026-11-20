"""Cycle1603 reusable review-only scene continuity checks (stdlib)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    headline: str
    evidence: str

SCENES = (
    Scene(0, 2.5, "毎日、合計を手入力？", "12件 → 20件まで あと8件"),
    Scene(2.5, 5, "BEFORE｜手計算", "入力ミスも起きやすい"),
    Scene(5, 8, "操作｜差分を計算", "=B2-C2 を入力"),
    Scene(8, 11.5, "AFTER｜自動で残数表示", "目標20 − 現在12 = 残り8"),
    Scene(11.5, 15, "最後に必ず検算", "保存して試してみよう"),
)

def validate(scenes=SCENES, duration=15):
    if not scenes or scenes[0].start != 0 or scenes[-1].end != duration:
        raise ValueError("Scene timeline does not cover entire video")
    for index, scene in enumerate(scenes):
        if scene.end <= scene.start or not scene.headline or not scene.evidence:
            raise ValueError("Invalid scene")
        if index and scenes[index - 1].end != scene.start:
            raise ValueError("Gap or overlap")
    return True

def publication_allowed(*, japanese_narration_verified=False,
                        speech_caption_sync_verified=False,
                        asset_rights_approved=False,
                        privacy_approved=False,
                        employee_approved=False):
    return all((japanese_narration_verified, speech_caption_sync_verified,
                asset_rights_approved, privacy_approved, employee_approved))
