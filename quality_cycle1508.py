"""Fail-closed QA for synthetic demo videos (standard library only)."""
import json
import subprocess
from pathlib import Path

def inspect(video, manifest):
    metadata = json.loads(Path(manifest).read_text(encoding="utf-8"))
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(video)], text=True))
    streams = probe.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    problems = []
    if not v or v.get("codec_name") != "h264": problems.append("H264_VIDEO_MISSING")
    if not a: problems.append("AUDIO_TRACK_MISSING")
    if not metadata.get("japanese_narration_verified", False): problems.append("JAPANESE_NARRATION_UNVERIFIED")
    if not metadata.get("speech_caption_alignment_verified", False): problems.append("SPEECH_CAPTIONS_UNVERIFIED")
    if not metadata.get("asset_rights_approved", False): problems.append("ASSET_RIGHTS_UNVERIFIED")
    if not metadata.get("human_quality_approved", False): problems.append("HUMAN_APPROVAL_MISSING")
    return {"posting_allowed": not problems, "problems": problems,
            "width": v.get("width") if v else None, "height": v.get("height") if v else None,
            "duration": float(probe.get("format", {}).get("duration", 0))}

if __name__ == "__main__":
    import sys
    result = inspect(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["posting_allowed"] else 2)
