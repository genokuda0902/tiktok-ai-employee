"""Fail-closed narration evidence: AAC does not prove Japanese speech."""
import json, subprocess
def evaluate(path, transcript=None, speech_verified=False, rights_approved=False, employee_approved=False):
    result=subprocess.run(["ffprobe","-v","error","-show_streams","-of","json",str(path)],check=True,capture_output=True,text=True)
    streams=json.loads(result.stdout)["streams"]
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    checks={"video":bool(video),"vertical":bool(video and video.get("height",0)>video.get("width",0)),
      "audio_track":bool(audio),"japanese_transcript":bool(transcript and transcript.strip()),
      "narration_verified":bool(speech_verified and audio and transcript and transcript.strip()),
      "rights_approved":bool(rights_approved),"employee_approved":bool(employee_approved)}
    return {"checks":checks,"publication_approved":all(checks.values())}
