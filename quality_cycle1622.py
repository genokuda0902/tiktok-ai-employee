"""Review-only media gate. Fails closed on missing narration or approval."""
import json
import subprocess
from pathlib import Path

def inspect(path, captions, *, assets_approved=False, employee_approved=False):
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ], text=True))
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(probe.get("format", {}).get("duration", 0))
    spans = sorted(captions, key=lambda c: c["start"])
    timed = bool(spans) and spans[0]["start"] <= 0.1 and spans[-1]["end"] >= duration - 0.1
    timed = timed and all(c["start"] < c["end"] and bool(c.get("text", "").strip()) for c in spans)
    timed = timed and all(a["end"] >= b["start"] - 0.1 for a, b in zip(spans, spans[1:]))
    checks = {
        "video_present": video is not None,
        "portrait": bool(video and int(video.get("height", 0)) > int(video.get("width", 0))),
        "audio_present": audio is not None,
        "captions_cover_timeline": timed,
        "assets_approved": assets_approved,
        "employee_approved": employee_approved,
    }
    return {"checks": checks, "posting_allowed": all(checks.values()),
            "status": "APPROVED_FOR_MANUAL_REVIEW" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("captions")
    args = p.parse_args()
    print(json.dumps(inspect(Path(args.video), json.loads(Path(args.captions).read_text(encoding="utf-8"))), indent=2))
