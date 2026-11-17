"""Reusable four-beat spreadsheet demonstration scene planner (review-only)."""
SCENES = [
    ("この集計、まだ手作業？", "売上表の合計を3秒で"),
    ("SUM関数を入力", "=SUM(B2:B4)"),
    ("合計が自動で出る", "12,000円 → 35,000円"),
    ("数字は必ず確認", "保存して試してみよう"),
]
DURATION = 10.0
def scene_at(seconds):
    if not 0 <= seconds < DURATION:
        raise ValueError("timestamp outside video")
    return min(int(seconds / 2.5), len(SCENES)-1)
def publication_approved(japanese_narration_verified=False, caption_sync_verified=False, assets_approved=False, employee_approved=False):
    return all((japanese_narration_verified,caption_sync_verified,assets_approved,employee_approved))
