"""Fail-closed technical gate for measured narration candidates.

NOT a language detector, rights approval, or semantic-sync proof.
Only verifies provenance metadata, measured captions, and non-silent PCM WAV.
"""
from __future__ import annotations
from array import array
import math
from pathlib import Path
import sys
import wave
from video_engine.production_v2.measured_caption_validator import validate_measured_caption_timeline


def validate_narration_readiness(plan: dict, wav_path: str | Path) -> dict:
    """Raise ValueError on any missing contract; never infer speech from AAC alone."""
    voice = plan.get("voice_metadata")
    if not isinstance(voice, dict) or voice.get("engine") != "AivisSpeech":
        raise ValueError("AivisSpeech narration provenance missing")
    if not voice.get("speaker") or not voice.get("style"):
        raise ValueError("Voice speaker/style missing")
    scenes = plan.get("scenes")
    if not isinstance(scenes, list) or not 6 <= len(scenes) <= 10:
        raise ValueError("Narration requires 6-10 scenes")
    if any(not isinstance(s.get("narration"), str) or not s["narration"].strip() for s in scenes):
        raise ValueError("Narration text missing in scene")
    captions = validate_measured_caption_timeline(
        scenes, plan.get("caption_timeline"), plan.get("caption_timing_source")
    )
    target = float(captions[-1]["end"])
    if not 15 <= target <= 25:
        raise ValueError("Narration target duration outside 15-25 seconds")
    try:
        with wave.open(str(wav_path), "rb") as w:
            channels, width, rate = w.getnchannels(), w.getsampwidth(), w.getframerate()
            frames = w.getnframes()
            if channels not in (1, 2) or width != 2 or rate < 16000:
                raise ValueError("Narration must be PCM16 mono/stereo WAV at >=16kHz")
            raw = w.readframes(frames)
    except (OSError, EOFError, wave.Error) as exc:
        raise ValueError("Narration WAV unreadable") from exc
    actual = frames / rate
    if abs(actual - target) > 0.08:
        raise ValueError("Narration WAV duration differs from measured captions")
    samples = array("h")
    samples.frombytes(raw)
    if sys.byteorder != "little":
        samples.byteswap()
    if not samples:
        raise ValueError("Narration WAV has no samples")
    rms = math.sqrt(sum(v*v for v in samples) / len(samples))
    if rms < 100:
        raise ValueError("Narration WAV silent or extremely quiet")
    return {
        "technical_narration_contract": "PASS",
        "measured_caption_count": len(captions),
        "duration_seconds": round(actual, 3),
        "rms_dbfs": round(20 * math.log10(rms / 32768), 1),
        "japanese_language_verified": False,
        "semantic_sync_verified": False,
        "human_pronunciation_review": "PENDING",
        "rights_approved": False,
        "publication_approved": False,
    }
