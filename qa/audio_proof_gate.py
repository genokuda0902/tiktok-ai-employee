"""Fail-closed QA for 10-genre review renders; no speech claims from an audio stream alone."""
import json
import subprocess
from pathlib import Path

def probe(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def review(path, *, speech_verified=False, captions_verified=False, assets_approved=False, human_approved=False):
    data=probe(path)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    problems=[]
    if not video: problems.append("missing_video")
    elif (video.get("width"),video.get("height"))!=(1080,1920): problems.append("not_native_1080_vertical")
    if not audio: problems.append("missing_audio")
    if not speech_verified: problems.append("japanese_speech_unverified")
    if not captions_verified: problems.append("speech_caption_sync_unverified")
    if not assets_approved: problems.append("assets_unapproved")
    if not human_approved: problems.append("human_review_pending")
    # Even with a valid audio stream, explicit independent speech verification is required.
    return {"publishable":not problems,"problems":problems,"duration":data.get("format",{}).get("duration")}

if __name__=="__main__":
    import sys
    print(json.dumps(review(Path(sys.argv[1])),ensure_ascii=False,indent=2))
