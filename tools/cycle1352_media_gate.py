"""Review-only media acceptance gate; no publication decisions based on audio presence alone."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def review(path, *, japanese_narration_verified=False, synced_captions_verified=False, rights_approved=False, human_approved=False):
    data=probe(path)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),{})
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    issues=[]
    if (video.get("width"),video.get("height"))!=(1080,1920): issues.append("resolution")
    if audio is None: issues.append("audio_missing")
    if not japanese_narration_verified: issues.append("japanese_narration_unverified")
    if not synced_captions_verified: issues.append("speech_caption_sync_unverified")
    if not rights_approved: issues.append("rights_unapproved")
    if not human_approved: issues.append("human_approval_missing")
    return {"quality":"REVIEW_ONLY" if issues else "REQUIRES_MANUAL_POST_DECISION","posting_allowed":False,"issues":issues,"width":video.get("width"),"height":video.get("height"),"has_audio_stream":audio is not None}

if __name__=="__main__":
    import sys
    print(json.dumps(review(Path(sys.argv[1])),ensure_ascii=False,indent=2))
