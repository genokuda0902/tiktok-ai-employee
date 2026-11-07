"""Fail-closed media inspection for ten-category review videos (cycle1291)."""
import json
import subprocess

def inspect(path, require_narration=True):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    reasons = []
    if not video or video.get("width", 0) < 1080 or video.get("height", 0) < 1920:
        reasons.append("resolution_below_1080x1920")
    if require_narration and not audio:
        reasons.append("narration_missing")
    if float(data.get("format", {}).get("duration", 0)) <= 0:
        reasons.append("invalid_duration")
    return {"approved": not reasons, "reasons": reasons, "video": video is not None, "audio": audio is not None}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False))
