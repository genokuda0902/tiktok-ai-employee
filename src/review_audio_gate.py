"""Fail-closed audio and caption QA for review-only videos (stdlib only)."""
import json
import subprocess
from pathlib import Path

def inspect(mp4, srt=None):
    p = Path(mp4)
    if not p.is_file() or p.stat().st_size == 0:
        return {"approved": False, "issues": ["missing_mp4"]}
    proc = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)],capture_output=True,text=True,check=True)
    info = json.loads(proc.stdout)
    streams = info.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    issues = []
    if not videos or videos[0].get("width") != 1080 or videos[0].get("height") != 1920:
        issues.append("vertical_1080p_missing")
    if not audios:
        issues.append("narration_audio_missing")
    # Audio stream alone never establishes Japanese speech or timing.
    issues.append("japanese_speech_unverified")
    if not srt or not Path(srt).is_file() or not Path(srt).read_text(encoding="utf-8").strip():
        issues.append("caption_file_missing")
    issues.append("speech_caption_sync_unverified")
    issues.append("human_publication_approval_missing")
    return {"approved": False, "issues": issues, "duration": float(info.get("format",{}).get("duration",0))}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None),ensure_ascii=False,indent=2))
