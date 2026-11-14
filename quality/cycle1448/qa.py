"""Review-only video QA; never equate technical validity with publication approval."""
import json
import subprocess

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))

def check_video(metadata, *, captions_burned=False, japanese_voice_verified=False,
                rights_approved=False, employee_approved=False):
    streams=metadata.get("streams", [])
    video=next((s for s in streams if s.get("codec_type")=="video"), None)
    audio=any(s.get("codec_type")=="audio" for s in streams)
    issues=[]
    if not video or (video.get("width"),video.get("height"))!=(1080,1920):
        issues.append("vertical_1080p_missing")
    if not captions_burned: issues.append("burned_captions_unverified")
    if not audio or not japanese_voice_verified: issues.append("japanese_narration_unverified")
    if not rights_approved: issues.append("rights_unapproved")
    if not employee_approved: issues.append("employee_unapproved")
    return {"publication_approved":not issues, "issues":issues}

if __name__=="__main__":
    import sys
    print(json.dumps(check_video(probe(sys.argv[1])),ensure_ascii=False,indent=2))
