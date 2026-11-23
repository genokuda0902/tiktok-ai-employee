"""Genre-neutral storyboard contract for review-only TikTok drafts.

No third-party/private assets; no claim of narration or posting approval.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    title: str
    subtitle: str
    seconds: float

def validate_storyboard(scenes, *, narration_verified=False, rights_approved=False, employee_approved=False):
    issues=[]
    if not scenes: issues.append("missing_scenes")
    for i, scene in enumerate(scenes):
        if not 1 <= scene.seconds <= 8: issues.append(f"scene_{i}_duration")
        if len(scene.title) > 24 or len(scene.subtitle) > 40: issues.append(f"scene_{i}_text_overflow")
        if not scene.title.strip(): issues.append(f"scene_{i}_missing_title")
    if not narration_verified: issues.append("japanese_narration_unverified")
    if not rights_approved: issues.append("rights_unapproved")
    if not employee_approved: issues.append("employee_approval_missing")
    return {"publication_approved": not issues, "issues": issues}

DEMO = [
    Scene("表がバラバラで", "確認に時間がかかる", 4),
    Scene("AIに条件を渡す", "列名・目的・出力形式", 4),
    Scene("結果は必ず確認", "数字・個人情報・根拠", 4),
]
