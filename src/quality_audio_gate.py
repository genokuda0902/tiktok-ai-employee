"""Fail closed on silent or unverified Japanese narration."""
import re, subprocess

def check_audio(path, narration_verified=False, transcript_verified=False, sync_verified=False):
    p=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",str(path),"-af","volumedetect","-vn","-f","null","-"],capture_output=True,text=True)
    m=re.search(r"mean_volume:\\s*(-?(?:\\d+(?:\\.\\d+)?|inf)) dB",p.stderr)
    volume=float(m.group(1)) if m else None
    blockers=[]
    if p.returncode: blockers.append("audio_decode_failed")
    if volume is None or volume < -55: blockers.append("audio_silent_or_unmeasurable")
    if not narration_verified: blockers.append("japanese_narration_unverified")
    if not transcript_verified: blockers.append("transcript_unverified")
    if not sync_verified: blockers.append("caption_sync_unverified")
    return {"approved":not blockers,"mean_volume_db":volume,"blockers":blockers}
