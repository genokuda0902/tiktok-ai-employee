"""Review-only MP4 QA; fail closed on missing Japanese narration and approval."""
import json
import subprocess
from pathlib import Path


def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def evaluate(info, *, japanese_speech_verified=False, captions_synced=False, assets_approved=False, employee_approved=False):
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = any(s.get("codec_type") == "audio" for s in streams)
    return {
        "video_1080x1920": video.get("width") == 1080 and video.get("height") == 1920,
        "audio_stream": audio,
        "japanese_speech_verified": bool(audio and japanese_speech_verified),
        "captions_synced": bool(captions_synced),
        "assets_approved": bool(assets_approved),
        "employee_approved": bool(employee_approved),
        "publication_approved": bool(video.get("width") == 1080 and video.get("height") == 1920 and audio and japanese_speech_verified and captions_synced and assets_approved and employee_approved),
    }


def test_silent_review_rejected():
    info = {"streams": [{"codec_type": "video", "width": 1080, "height": 1920}]}
    assert not evaluate(info, japanese_speech_verified=True, captions_synced=True, assets_approved=True, employee_approved=True)["publication_approved"]


def test_audio_tone_does_not_count_as_japanese_speech():
    info = {"streams": [{"codec_type": "video", "width": 1080, "height": 1920}, {"codec_type": "audio"}]}
    assert not evaluate(info, captions_synced=True, assets_approved=True, employee_approved=True)["publication_approved"]


def test_approval_is_required():
    info = {"streams": [{"codec_type": "video", "width": 1080, "height": 1920}, {"codec_type": "audio"}]}
    assert not evaluate(info, japanese_speech_verified=True, captions_synced=True, assets_approved=True)["publication_approved"]
