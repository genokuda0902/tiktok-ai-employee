"""Fail-closed audio QA: an AAC track is not proof of Japanese narration."""
import json
import subprocess

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,width,height:format=duration", "-of", "json",
        str(path)], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)

def assess(path, narration_verified=False, caption_sync_verified=False,
           rights_approved=False, employee_approved=False):
    info = probe(path)
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    reasons = []
    if (video.get("width"), video.get("height")) != (1080, 1920):
        reasons.append("resolution")
    if not audio:
        reasons.append("audio_missing")
    if not narration_verified:
        reasons.append("japanese_narration_unverified")
    if not caption_sync_verified:
        reasons.append("speech_caption_sync_unverified")
    if not rights_approved:
        reasons.append("rights_unapproved")
    if not employee_approved:
        reasons.append("employee_unapproved")
    return {"publication_approved": not reasons, "reasons": reasons,
            "video": video, "audio": audio,
            "duration": info.get("format", {}).get("duration")}
