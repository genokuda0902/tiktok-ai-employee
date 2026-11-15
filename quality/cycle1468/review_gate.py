"""Fail-closed review gate: stream existence is not proof of Japanese speech."""
import json
import subprocess
import sys

def probe(path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams",
                                   "-show_format", "-of", "json", path], text=True)
    return json.loads(raw)

def assess(metadata, *, japanese_narration_verified=False,
           captions_synchronized_verified=False, assets_approved=False,
           employee_approved=False):
    video = [s for s in metadata.get("streams", []) if s.get("codec_type") == "video"]
    audio = [s for s in metadata.get("streams", []) if s.get("codec_type") == "audio"]
    portrait = bool(video and video[0].get("width", 0) < video[0].get("height", 0))
    checks = {"portrait_video": portrait, "audio_stream": bool(audio),
              "japanese_narration_verified": bool(audio and japanese_narration_verified),
              "captions_synchronized_verified": bool(captions_synchronized_verified),
              "assets_approved": bool(assets_approved),
              "employee_approved": bool(employee_approved)}
    return {"checks": checks, "posting_allowed": all(checks.values()),
            "publication_status": "APPROVED_FOR_MANUAL_POST" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}

if __name__ == "__main__":
    result = assess(probe(sys.argv[1]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not result["posting_allowed"] else 1)  # review-only CLI must never approve
