"""Fail-closed media audio preflight. Audio presence never proves Japanese speech."""
import json
import subprocess

def inspect_media(path, japanese_voice_reviewed=False, captions_synced_reviewed=False):
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True))
    streams=probe.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=[s for s in streams if s.get("codec_type")=="audio"]
    reasons=[]
    if not video: reasons.append("missing_video")
    if not audio: reasons.append("missing_audio_stream")
    if not japanese_voice_reviewed: reasons.append("japanese_narration_unverified")
    if not captions_synced_reviewed: reasons.append("speech_caption_sync_unverified")
    return {"publishable":False,"technical_audio_present":bool(audio),"video_codec":video.get("codec_name") if video else None,"reasons":reasons,"manual_approval_required":True}
