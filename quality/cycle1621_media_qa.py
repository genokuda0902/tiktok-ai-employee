"""Cycle1621: fail-closed media QA, shared across all 10 genres. stdlib only."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,codec_type,width,height",
        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def review(path, approved_assets=False, employee_approved=False, synchronized_captions=False):
    metadata = probe(path)
    streams = metadata.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    issues = []
    if (video.get("width"), video.get("height")) not in ((720, 1280), (1080, 1920)):
        issues.append("invalid_vertical_resolution")
    if not audio:
        issues.append("missing_audio")
    if not synchronized_captions:
        issues.append("captions_not_verified")
    if not approved_assets:
        issues.append("assets_not_approved")
    if not employee_approved:
        issues.append("employee_not_approved")
    return {"publishable": not issues, "issues": issues,
            "duration": float(metadata.get("format", {}).get("duration", 0))}

if __name__ == "__main__":
    import sys
    print(json.dumps(review(Path(sys.argv[1])), ensure_ascii=False, indent=2))
