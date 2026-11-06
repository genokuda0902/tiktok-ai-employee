"""Fail-closed metadata gate for review-only videos; reusable across ten genres."""
import json
from pathlib import Path

def validate(manifest: dict) -> list[str]:
    errors = []
    if manifest.get("review_only") is not True:
        errors.append("review_only must be true")
    if manifest.get("synthetic_data") is not True:
        errors.append("source approval not established")
    if manifest.get("narration") != "verified_japanese":
        errors.append("Japanese narration unverified")
    if manifest.get("caption_type") != "speech_synced":
        errors.append("speech-synchronized captions unverified")
    if manifest.get("resolution") not in ([1080, 1920], [720, 1280]):
        errors.append("invalid vertical resolution")
    return errors

def main(path: str) -> int:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate(manifest)
    print(json.dumps({"publication_approved": False, "issues": errors}, ensure_ascii=False))
    return 0 if not errors else 1

if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1]))
