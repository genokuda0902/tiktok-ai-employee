"""Cycle1286 review-only synthetic storyboard and caption contract.
Render reference: Python/Pillow and ffmpeg; audio intentionally absent.
Never label as publication-ready.
"""
SCENES = [
    ("AIの回答、", "そのまま提出？", "まずは確認"),
    ("01  出典を確認", "情報の根拠は？", "出典を開いて確かめる"),
    ("02  日付を確認", "情報は最新？", "更新日と対象期間を確認"),
    ("03  最後は人が判断", "誤りを見逃さない", "確認してから使おう"),
]
DURATION_PER_SCENE = 3
WIDTH, HEIGHT = 1080, 1920
REVIEW_ONLY = True
POSTING_ALLOWED = False

def srt():
    return "".join(
        f"{i+1}\n00:00:{i*3:02},000 --> 00:00:{(i+1)*3:02},000\n{scene[2]}\n\n"
        for i, scene in enumerate(SCENES)
    )

def validate_publication(audio_verified=False, captions_synced=False,
                         rights_approved=False, employee_approved=False):
    return all((audio_verified, captions_synced, rights_approved, employee_approved))
