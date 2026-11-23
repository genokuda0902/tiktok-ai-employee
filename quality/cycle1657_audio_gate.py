"""Fail-closed, genre-independent readiness probe for Japanese narration."""
import json
import subprocess
import sys

def probe(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", path], capture_output=True, text=True, check=True)
    streams = json.loads(p.stdout)["streams"]
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    return {"video_present": video is not None,
            "vertical_1080p": bool(video and video.get("width") == 1080 and video.get("height") == 1920),
            "audio_stream_present": bool(audio),
            "japanese_speech_verified": False,
            "speech_caption_sync_verified": False,
            "publication_approved": False}

def ready(result, *, japanese_speech_verified=False, sync_verified=False, rights_approved=False, employee_approved=False):
    return all([result["video_present"], result["vertical_1080p"], result["audio_stream_present"],
                japanese_speech_verified, sync_verified, rights_approved, employee_approved])

if __name__ == "__main__":
    result = probe(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if ready(result) else 2)
