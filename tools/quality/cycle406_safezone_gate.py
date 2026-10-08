"""Cycle406 zero-cost safe-zone gate shared across 10 TikTok genres."""
from pathlib import Path
import json

W, H = 1080, 1920
CAPTION_BOX = (76, 1220, 1004, 1455)
SAFE_BOTTOM_START = 1560
GENRES = ("AI時短","仕事効率化","Excel","営業","学習","暮らし","旅行","料理","健康情報","趣味")
PUBLICATION = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"

def check_caption_box(box=CAPTION_BOX):
    x1,y1,x2,y2=box
    return 0<=x1<x2<=W and 0<=y1<y2<SAFE_BOTTOM_START

def verify_manifest(manifest):
    if manifest.get("resolution") != [W,H]: return False
    if not check_caption_box(tuple(manifest.get("caption_box",[]))): return False
    if manifest.get("publication") != PUBLICATION: return False
    if manifest.get("auto_post") is not False: return False
    return True

def write_contract(path):
    obj={"cycle":406,"resolution":[W,H],"caption_box":list(CAPTION_BOX),
         "safe_bottom_start":SAFE_BOTTOM_START,"genres":list(GENRES),
         "auto_post":False,"publication":PUBLICATION,
         "voice_status":"unverified until voiced MP4 is actually rendered"}
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    return obj
