"""Reusable zero-cost video layout + narration release gate (cycle521).
Technical checks are NOT equivalent to TikTok posting approval.
"""
from dataclasses import dataclass
from pathlib import Path
import json, shutil, subprocess

GENRES = {
    "ai_work":"AI・仕事効率化","business":"営業・ビジネス",
    "career":"転職・キャリア","finance":"お金・節約",
    "psychology":"恋愛・心理","beauty":"美容・身だしなみ",
    "lifestyle":"健康・生活改善","science":"雑学・科学",
    "travel":"旅行・グルメ","comparison":"商品比較・暮らし"
}
FRAME=(1080,1920)
LOCAL_SAFE=(64,245,870,1505)  # conservative preview; not official device guarantee

def assert_text_safe(boxes, safe=LOCAL_SAFE):
    for entry in boxes:
        x1,y1,x2,y2=entry["bbox"]
        if not (safe[0]<=x1<x2<=safe[2] and safe[1]<=y1<y2<=safe[3]):
            raise ValueError("Unsafe critical text: "+str(entry))
    return len(boxes)

def probe_mp4(path):
    p=Path(path)
    if not p.is_file() or p.stat().st_size<100_000:
        raise ValueError("Missing or suspiciously small MP4")
    result=subprocess.run(["ffprobe","-v","error","-show_streams",
                           "-show_format","-of","json",str(p)],
                          check=True,capture_output=True,text=True)
    data=json.loads(result.stdout)
    v=next(s for s in data["streams"] if s["codec_type"]=="video")
    a=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    if (v.get("width"),v.get("height"))!=FRAME or v.get("codec_name")!="h264":
        raise ValueError("Wrong video dimensions or codec")
    if a is None or a.get("codec_name")!="aac":
        raise ValueError("Missing AAC audio")
    subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(p),
                    "-f","null","-"],check=True,capture_output=True)
    return {"width":FRAME[0],"height":FRAME[1],
            "duration":float(data["format"]["duration"]),
            "audio_codec":a["codec_name"],"video_codec":v["codec_name"]}

def tts_preflight():
    return {"open_jtalk":shutil.which("open_jtalk"),
            "model_required":True,"dictionary_required":True}

def release_gate(*, japanese_voice_verified=False, human_approved=False,
                 rights_verified=False, audio_sync_verified=False):
    return ("APPROVED_FOR_MANUAL_POST" if all((
        japanese_voice_verified,human_approved,rights_verified,
        audio_sync_verified)) else "PUBLICATION_NOT_APPROVED")
