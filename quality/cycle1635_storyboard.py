"""Five-scene review-only storyboard, original synthetic data; no speech claim."""
from pathlib import Path
import json
SCENES=[
("その入力、毎回やり直していませんか？","表記ゆれが確認作業を増やします"),
("BEFORE｜入力がバラバラ","株式会社ABC / (株)ABC / ABC"),
("AFTER｜ルールを統一","株式会社ABC → 株式会社ABC"),
("最後に人が確認","AIの提案は必ず目視でチェック"),
("3ステップで始める","①決める ②揃える ③確認する"),
]
DURATION=18
FPS=24
SIZE=(1080,1920)
POSTING_ALLOWED=False
def qa(metadata):
    errors=[]
    if metadata.get("audio_codec") not in ("aac","opus"): errors.append("JAPANESE_NARRATION_MISSING")
    if not metadata.get("speech_verified"): errors.append("SPEECH_UNVERIFIED")
    if not metadata.get("captions_synced"): errors.append("CAPTION_SYNC_UNVERIFIED")
    if not metadata.get("asset_approved"): errors.append("ASSET_APPROVAL_MISSING")
    if not metadata.get("employee_approved"): errors.append("EMPLOYEE_APPROVAL_MISSING")
    return {"posting_allowed":not errors,"issues":errors}
def write_manifest(path):
    obj={"scenes":SCENES,"duration":DURATION,"fps":FPS,"size":SIZE,"review_only":True,
         "synthetic_data":True,"audio_status":"missing","caption_status":"not_speech_synced",
         "posting_allowed":False}
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
    write_manifest(Path(__file__).with_name("cycle1635_manifest.json"))
