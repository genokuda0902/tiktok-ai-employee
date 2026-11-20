"""Fail-closed contract for review-only synthetic caption videos."""
SCENES = [("入力を減らす","数字を毎回手入力していませんか？"),("関数で自動集計","=SUM(B2:B5) を入力"),("結果を確認","合計 120 になるか確認")]
def assess(meta):
    required = ("video_decoded","japanese_speech_verified","captions_speech_aligned","asset_rights_approved","employee_approved")
    return {"publication_approved": all(meta.get(k) is True for k in required), "missing": [k for k in required if meta.get(k) is not True]}
