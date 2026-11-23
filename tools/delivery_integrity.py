"""Independent recipient-side MP4 integrity check; no publication approval implied."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

def inspect(path, expected_sha):
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], text=True))
    videos = [s for s in probe["streams"] if s["codec_type"] == "video"]
    audios = [s for s in probe["streams"] if s["codec_type"] == "audio"]
    resolution_ok = len(videos) == 1 and videos[0].get("width") == 1080 and videos[0].get("height") == 1920
    return {"sha256": digest, "checksum_match": digest == expected_sha,
            "resolution_ok": resolution_ok, "video_codec": videos[0].get("codec_name") if videos else None,
            "audio_stream_present": bool(audios),
            "japanese_narration_verified": False, "caption_sync_verified": False,
            "posting_allowed": False, "quality_approved": False,
            "delivery_verified": digest == expected_sha and resolution_ok}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("mp4")
    p.add_argument("--expected-sha256", required=True)
    args = p.parse_args()
    result = inspect(args.mp4, args.expected_sha256)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["delivery_verified"] else 2)

if __name__ == "__main__":
    main()
