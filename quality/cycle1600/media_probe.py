"""Review-only media evidence; a detected audio stream is NOT proof of Japanese speech."""
import json
import subprocess
from pathlib import Path

def probe(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    streams = info.get("streams", [])
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    if len(video) != 1:
        raise ValueError("Exactly one video stream required")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                   check=True, capture_output=True)
    return {"width": video[0]["width"], "height": video[0]["height"],
            "duration": float(info["format"]["duration"]),
            "audio_streams": len(audio), "decode_ok": True,
            "japanese_narration_verified": False, "caption_sync_verified": False,
            "publication_approved": False}

def publication_allowed(evidence):
    return all(evidence.get(key) is True for key in
               ("decode_ok", "japanese_narration_verified",
                "caption_sync_verified", "assets_approved",
                "privacy_approved", "employee_approved"))

if __name__ == "__main__":
    import sys
    print(json.dumps(probe(sys.argv[1]), ensure_ascii=False, indent=2))
