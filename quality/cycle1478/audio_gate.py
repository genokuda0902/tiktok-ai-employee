"""Fail-closed technical gate for review-only TikTok MP4s (cycle1478).

Does not assert visual appeal, Japanese language, licensing, or approval.
"""
import json
import subprocess
from pathlib import Path


def inspect(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,codec_name,width,height",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = any(s.get("codec_type") == "audio" for s in streams)
    return {"vertical": video.get("height", 0) > video.get("width", 0),
            "audio_present": audio,
            "duration": float(data.get("format", {}).get("duration", 0))}


def publication_gate(path, *, japanese_narration_verified=False,
                     speech_caption_sync_verified=False,
                     asset_rights_approved=False, privacy_approved=False,
                     employee_approved=False):
    info = inspect(path)
    technical = info["vertical"] and info["audio_present"] and info["duration"] > 0
    approved = all([technical, japanese_narration_verified,
                    speech_caption_sync_verified, asset_rights_approved,
                    privacy_approved, employee_approved])
    return {"publication_approved": approved, **info}


def test_fail_closed_without_narration():
    # Missing audio must never pass even if every human flag is set.
    import unittest.mock as mock
    with mock.patch(__name__ + ".inspect", return_value={
        "vertical": True, "audio_present": False, "duration": 12.0
    }):
        result = publication_gate("demo.mp4", japanese_narration_verified=True,
            speech_caption_sync_verified=True, asset_rights_approved=True,
            privacy_approved=True, employee_approved=True)
        assert not result["publication_approved"]


def test_fail_closed_without_approval():
    import unittest.mock as mock
    with mock.patch(__name__ + ".inspect", return_value={
        "vertical": True, "audio_present": True, "duration": 12.0
    }):
        result = publication_gate("demo.mp4", japanese_narration_verified=True,
            speech_caption_sync_verified=True, asset_rights_approved=True,
            privacy_approved=True, employee_approved=False)
        assert not result["publication_approved"]


if __name__ == "__main__":
    test_fail_closed_without_narration()
    test_fail_closed_without_approval()
    print("2 tests passed")
