"""Review-only PCM scene QA. Never infer Japanese speech from audio energy."""
import math
import wave
from array import array

def scene_audio_gate(path, durations, narration_claimed=False, provenance=None):
    if not 6 <= len(durations) <= 10:
        raise ValueError("scene count")
    if any(not math.isfinite(float(d)) or d <= 0 for d in durations):
        raise ValueError("invalid durations")
    total = sum(durations)
    if not 15 <= total <= 25:
        raise ValueError("total duration")
    with wave.open(str(path), "rb") as w:
        rate, ch, width, frames = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        if width != 2 or ch not in (1, 2) or rate < 16000:
            raise ValueError("PCM16 expected")
        raw = w.readframes(frames)
    if abs(frames / rate - total) > .08:
        raise ValueError("timeline mismatch")
    pcm = array("h")
    pcm.frombytes(raw)
    if len(pcm) != frames * ch:
        raise ValueError("truncated audio")
    if sum(abs(x) >= 32760 for x in pcm) / len(pcm) > .01:
        raise ValueError("clipping")
    cursor = 0
    levels = []
    for d in durations:
        a = round(cursor * rate) * ch
        cursor += d
        b = round(cursor * rate) * ch
        block = pcm[a:b]
        rms = math.sqrt(sum(x*x for x in block) / len(block))
        levels.append(round(20 * math.log10(max(rms, 1e-9) / 32768), 1))
    if narration_claimed and (provenance != "AivisSpeech" or any(x < -50 for x in levels)):
        raise ValueError("narration claim unsupported")
    return {"technical_audio": "PASS", "levels_dbfs": levels,
            "japanese_verified": False, "semantic_sync_verified": False,
            "publication_approved": False}
