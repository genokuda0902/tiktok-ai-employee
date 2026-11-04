"""Review-only structural gate for timed Japanese captions and audio presence.

No semantic speech verification: a human must listen and approve.
"""
import json
import subprocess
from pathlib import Path


def probe_media(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def validate_timing(captions, duration, *, max_chars=24, min_duration=0.45):
    """Captions: [{start, end, text}]. Reject invalid/overlapping/out-of-bounds."""
    issues = []
    previous_end = 0.0
    if not captions:
        issues.append("missing_captions")
    for index, item in enumerate(captions):
        try:
            start, end = float(item["start"]), float(item["end"])
            text = item["text"]
            if not isinstance(text, str) or not text.strip():
                issues.append(f"{index}:empty_text")
            if len(text.strip()) > max_chars:
                issues.append(f"{index}:too_many_characters")
            if not (0 <= start < end <= duration):
                issues.append(f"{index}:out_of_bounds")
            if end - start < min_duration:
                issues.append(f"{index}:too_short")
            if start < previous_end - 0.001:
                issues.append(f"{index}:overlap_or_unsorted")
            previous_end = max(previous_end, end)
        except (KeyError, TypeError, ValueError):
            issues.append(f"{index}:invalid_caption")
    return issues


def review_gate(media_path, captions_path):
    media_path, captions_path = Path(media_path), Path(captions_path)
    if not media_path.is_file() or not captions_path.is_file():
        return {"passed": False, "issues": ["missing_input"]}
    metadata = probe_media(media_path)
    streams = metadata.get("streams", [])
    issues = []
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video or (video.get("width"), video.get("height")) != (1080, 1920):
        issues.append("invalid_video_resolution")
    if not audio:
        issues.append("missing_audio")
    duration = float(metadata.get("format", {}).get("duration", 0))
    if duration <= 0:
        issues.append("invalid_duration")
    try:
        captions = json.loads(captions_path.read_text(encoding="utf-8"))
        if not isinstance(captions, list):
            raise ValueError("captions must be a list")
        issues.extend(validate_timing(captions, duration))
    except (OSError, ValueError, TypeError):
        issues.append("invalid_caption_json")
    return {
        "passed": not issues,
        "issues": issues,
        "semantic_sync_verified": False,
        "human_review_required": True,
        "publication_approved": False,
    }
