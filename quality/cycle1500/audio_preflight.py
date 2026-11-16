"""Fail-closed media preflight. Audio presence is necessary, not sufficient for approval."""
import json
import subprocess
import sys

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True)
    if p.returncode:
        return {"approved":False,"reason":"ffprobe_failed","stderr":p.stderr}
    data=json.loads(p.stdout)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    if not video:
        return {"approved":False,"reason":"missing_video"}
    if not audio:
        return {"approved":False,"reason":"missing_audio","resolution":[video.get("width"),video.get("height")]}
    return {"approved":False,"reason":"japanese_speech_sync_rights_and_employee_approval_unverified","audio_codec":audio.get("codec_name")}

if __name__=="__main__":
    result=inspect(sys.argv[1])
    print(json.dumps(result,ensure_ascii=False))
    sys.exit(0 if result["approved"] else 2)
