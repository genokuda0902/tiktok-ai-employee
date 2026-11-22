"""Offline Japanese TTS readiness gate. No paid services or network calls."""
import json
import shutil
import subprocess
import sys

def inspect():
    voices = ""
    executable = shutil.which("espeak-ng") or shutil.which("espeak")
    if executable:
        result = subprocess.run([executable, "--voices"], capture_output=True, text=True)
        voices = result.stdout
    japanese = any(line.split()[1:2] == ["ja"] for line in voices.splitlines()[1:])
    return {"espeak_binary": executable, "espeak_ja_voice": japanese,
            "ffmpeg": bool(shutil.which("ffmpeg")),
            "tts_ready": japanese}

if __name__ == "__main__":
    status = inspect()
    print(json.dumps(status, ensure_ascii=False))
    sys.exit(0 if status["tts_ready"] else 2)
