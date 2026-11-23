"""Review-only narration evidence contract. No audio stream alone proves speech."""
import json
import subprocess
from pathlib import Path


def verify(video_path, evidence_path):
    video = Path(video_path)
    evidence = json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-of", "json", str(video)
    ], text=True))
    audio = [s for s in probe["streams"] if s["codec_type"] == "audio"]
    problems = []
    if not audio:
        problems.append("missing_audio_stream")
    if evidence.get("audio_kind") != "japanese_narration":
        problems.append("not_japanese_narration")
    if not evidence.get("transcript_ja", "").strip():
        problems.append("missing_transcript")
    if evidence.get("speech_reviewed_by_human") is not True:
        problems.append("speech_not_reviewed")
    if evidence.get("subtitle_sync_reviewed_by_human") is not True:
        problems.append("subtitle_sync_not_reviewed")
    if evidence.get("assets_approved") is not True:
        problems.append("assets_not_approved")
    if evidence.get("employee_approved") is not True:
        problems.append("employee_not_approved")
    return {"publication_approved": not problems, "problems": problems}


if __name__ == "__main__":
    import sys
    print(json.dumps(verify(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))
