"""Offline Japanese narration helper for human-review-only previews.

Requires an installed open_jtalk engine, Japanese dictionary and licensed HTS voice.
Fails closed when Japanese narration is unavailable; no fallback SFX counts as voice.
"""
from pathlib import Path
import subprocess
import wave

def synthesize(text: str, dictionary: Path, model: Path, output: Path) -> Path:
    if not text.strip() or not dictionary.exists() or not model.is_file():
        raise RuntimeError("Japanese TTS prerequisites missing")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["open_jtalk", "-x", str(dictionary), "-m", str(model),
                    "-ow", str(output)], input=text, text=True, check=True)
    with wave.open(str(output), "rb") as wav:
        if wav.getnframes() == 0 or wav.getframerate() < 16000:
            raise RuntimeError("Invalid Japanese narration WAV")
    return output
