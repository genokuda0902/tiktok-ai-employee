"""Genre-independent Japanese narration QA. Technical evidence is NOT language proof."""
from __future__ import annotations
import math
import struct
import wave
from pathlib import Path

def inspect_voice(wav_path, segments, expected_duration, provenance):
    """Return fail-closed diagnostics; never approve publishing automatically."""
    errors = []
    info = {"technical_pass": False, "human_review_required": True,
            "publication": "NOT_APPROVED", "errors": errors}
    p = Path(wav_path)
    if not p.is_file():
        errors.append("WAV_MISSING")
        return info
    try:
        with wave.open(str(p), "rb") as w:
            channels, width, rate = w.getnchannels(), w.getsampwidth(), w.getframerate()
            count = w.getnframes()
            raw = w.readframes(count)
        if channels not in (1, 2) or width != 2 or rate < 16000 or count == 0:
            errors.append("INVALID_PCM")
            return info
        values = struct.unpack("<" + "h" * (len(raw)//2), raw)
        rms = math.sqrt(sum(v*v for v in values) / len(values)) / 32768
        duration = count / rate
        info.update({"duration": round(duration, 3), "sample_rate": rate,
                     "rms": round(rms, 6)})
        if rms < 0.005:
            errors.append("SILENT_OR_TOO_QUIET")
        if abs(duration - expected_duration) > 0.35:
            errors.append("DURATION_MISMATCH")
        if not segments:
            errors.append("NO_CAPTIONS")
        else:
            last = 0.0
            for s in segments:
                start, end = float(s["start"]), float(s["end"])
                if start < last - 0.001 or end <= start or end > duration + 0.35:
                    errors.append("BAD_CAPTION_TIMELINE")
                    break
                if not str(s.get("text", "")).strip():
                    errors.append("EMPTY_CAPTION")
                    break
                last = end
            if last < duration - 1.0:
                errors.append("CAPTIONS_END_EARLY")
        if provenance.get("license_status") != "APPROVED":
            errors.append("VOICE_LICENSE_UNVERIFIED")
        if not provenance.get("synthesized_for_this_video"):
            errors.append("VOICE_PROVENANCE_UNVERIFIED")
        if not provenance.get("japanese_listening_confirmed"):
            errors.append("JAPANESE_LISTENING_UNVERIFIED")
        if not provenance.get("meaning_sync_confirmed"):
            errors.append("SEMANTIC_SYNC_UNVERIFIED")
        if provenance.get("auto_post") is not False:
            errors.append("AUTO_POST_NOT_FORBIDDEN")
        info["technical_pass"] = not errors
        return info
    except (OSError, EOFError, ValueError, KeyError, struct.error, TypeError) as e:
        errors.append("WAV_OR_MANIFEST_ERROR:" + type(e).__name__)
        return info
