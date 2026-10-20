"""Fail-closed offline Japanese TTS capability check for TikTok rendering."""
import shutil
import subprocess

def offline_japanese_tts():
    found = []
    for cmd in ("piper", "open_jtalk", "aivis", "voicevox"):
        if shutil.which(cmd):
            found.append(cmd)
    if shutil.which("espeak"):
        p = subprocess.run(["espeak", "--voices=ja"], capture_output=True, text=True, timeout=8)
        if p.returncode == 0 and [line for line in p.stdout.splitlines()[1:] if line.strip()]:
            found.append("espeak:ja")
    return found

def gate_audio(voice_available, transcript_verified, rights_verified):
    return bool(voice_available and transcript_verified and rights_verified)
