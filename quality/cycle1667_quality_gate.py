"""Cycle1667 fail-closed video QA: no speech proof means no publication."""
import json
import subprocess
from pathlib import Path

def probe(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def assess(data, evidence):
    videos=[s for s in data.get("streams",[]) if s.get("codec_type")=="video"]
    audio=[s for s in data.get("streams",[]) if s.get("codec_type")=="audio"]
    reasons=[]
    if not videos or (videos[0].get("width"),videos[0].get("height"))!=(1080,1920):
        reasons.append("vertical_resolution_unverified")
    if not audio: reasons.append("audio_stream_missing")
    if not evidence.get("japanese_speech_verified"): reasons.append("japanese_speech_unverified")
    if not evidence.get("caption_alignment_verified"): reasons.append("caption_alignment_unverified")
    if not evidence.get("assets_approved"): reasons.append("assets_unapproved")
    if not evidence.get("employee_approved"): reasons.append("employee_approval_missing")
    return {"publication_approved":not reasons,"blockers":reasons}

def test_silent_video_rejected():
    d={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
    assert "audio_stream_missing" in assess(d,{})["blockers"]

def test_effects_not_speech():
    d={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
    assert "japanese_speech_unverified" in assess(d,{})["blockers"]

def test_all_evidence_required():
    d={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
    e={k:True for k in ("japanese_speech_verified","caption_alignment_verified","assets_approved","employee_approved")}
    assert assess(d,e)["publication_approved"]
    e["employee_approved"]=False
    assert not assess(d,e)["publication_approved"]

if __name__=="__main__":
    test_silent_video_rejected()
    test_effects_not_speech()
    test_all_evidence_required()
    print("3 QA regression tests passed")
