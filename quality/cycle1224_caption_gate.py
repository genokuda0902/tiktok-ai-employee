"""Fail-closed, genre-neutral subtitle timing gate. Structural evidence only.

This does NOT establish Japanese narration meaning or word-level sync.
"""
from __future__ import annotations
import json
from pathlib import Path


def validate_cues(cues: list[dict], duration: float, *, min_gap: float = 0.0) -> list[str]:
    errors: list[str] = []
    if not isinstance(cues, list) or not cues:
        return ["missing subtitle cues"]
    if not isinstance(duration, (int, float)) or not 0 < duration < 3600:
        return ["invalid video duration"]
    previous_end = 0.0
    for i, cue in enumerate(cues):
        if not isinstance(cue, dict):
            errors.append(f"cue {i}: not an object")
            continue
        start, end, text = cue.get("start"), cue.get("end"), cue.get("text")
        if not isinstance(start, (int, float)) or isinstance(start, bool) or not isinstance(end, (int, float)) or isinstance(end, bool):
            errors.append(f"cue {i}: invalid timestamps")
            continue
        if not isinstance(text, str) or not text.strip():
            errors.append(f"cue {i}: empty text")
        if start < 0 or end <= start or end > duration + 0.05:
            errors.append(f"cue {i}: outside video or nonpositive duration")
        if start < previous_end + min_gap - 0.001:
            errors.append(f"cue {i}: overlap or insufficient gap")
        previous_end = max(previous_end, end)
    return errors


def audit_manifest(manifest: dict) -> dict:
    errors = validate_cues(manifest.get("cues"), manifest.get("duration"))
    for field in ("japanese_speech_reviewed", "semantic_sync_reviewed", "visual_reviewed", "asset_rights_approved"):
        if manifest.get(field) is not True:
            errors.append(f"missing human approval: {field}")
    return {"passed": not errors, "errors": errors, "publication_approved": not errors}


if __name__ == "__main__":
    import sys
    result = audit_manifest(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
