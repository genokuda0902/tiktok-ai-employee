"""Reusable fail-closed technical preflight. Not a publication approval."""
import json
import subprocess

def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        check=True, capture_output=True, text=True)
    return json.loads(result.stdout)

def inspect(path, min_fps=24):
    data = probe(path)
    videos = [s for s in data["streams"] if s.get("codec_type") == "video"]
    audios = [s for s in data["streams"] if s.get("codec_type") == "audio"]
    reasons = []
    if len(videos) != 1:
        reasons.append("expected_one_video_stream")
    else:
        video = videos[0]
        if video.get("width", 0) < 720 or video.get("height", 0) < 1280:
            reasons.append("low_resolution")
        n, d = map(int, video.get("avg_frame_rate", "0/1").split("/"))
        if not d or n / d < min_fps:
            reasons.append("low_frame_rate")
    if not audios:
        reasons.append("missing_audio")
    # Audio stream presence never proves Japanese narration or caption alignment.
    reasons.extend(["japanese_speech_unverified", "timed_captions_unverified",
                    "asset_rights_unverified", "employee_approval_missing"])
    return {"publication_approved": False, "reasons": reasons,
            "duration_seconds": float(data["format"].get("duration", 0))}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
