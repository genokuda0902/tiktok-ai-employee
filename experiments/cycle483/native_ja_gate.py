"""Cycle483 native Japanese narration gate. No paid services, no publishing."""
from __future__ import annotations
from pathlib import Path
import json, shutil, subprocess, wave

def preflight():
    engine = shutil.which("open_jtalk")
    dictionary = Path("/var/lib/mecab/dic/open-jtalk/naist-jdic")
    voices = sorted(Path("/usr/share/hts-voice").rglob("*.htsvoice")) if Path("/usr/share/hts-voice").exists() else []
    return {"ready": bool(engine and dictionary.is_dir() and voices),
            "engine": engine, "dictionary": str(dictionary),
            "voice": str(voices[0]) if voices else None}

def synthesize(text: str, destination: str):
    if not text.strip(): raise ValueError("Empty Japanese narration")
    conf = preflight()
    if not conf["ready"]: raise RuntimeError("Native Japanese TTS unavailable; do not label SFX as narration")
    out = Path(destination); out.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([conf["engine"], "-x", conf["dictionary"],
        "-m", conf["voice"], "-r", "1.08", "-ow", str(out)],
        input=text+"\n", text=True, capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr[-300:])
    with wave.open(str(out), "rb") as wav:
        duration = wav.getnframes()/wav.getframerate()
    if duration < .25: raise RuntimeError("TTS waveform suspiciously short")
    return {"path": str(out), "duration": duration, "engine": "OPEN_JTALK_NATIVE_JA"}

def approval_gate(qa):
    return bool(qa.get("full_decode")=="PASS" and
        qa.get("native_ja_voice")=="GENERATED_UNREVIEWED" and
        qa.get("voice_caption_sync")=="SCENE_BOUNDARY_ONLY_UNREVIEWED" and
        qa.get("human_listening_approved") is True and
        qa.get("human_visual_approved") is True)

if __name__=="__main__":
    print(json.dumps(preflight(), ensure_ascii=False))
