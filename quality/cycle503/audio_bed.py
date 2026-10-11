#!/usr/bin/env python3
"""Cycle503: original, genre-neutral ambient cues for internal-review video only.

Reimplementation, not original v33 code. Input must be a synthetic,
non-confidential, approved-for-INTERNAL-REVIEW 20s H264/AAC MP4.
No Japanese narration, spoken-caption sync or release approval is claimed.
Requires only Python3 stdlib, ffmpeg and ffprobe; no paid services.
"""
from __future__ import annotations
import argparse, array, hashlib, json, math, os, subprocess, tempfile, wave
from pathlib import Path

SAMPLE_RATE = 44100
SECONDS = 20
SCENE_CUTS = (0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5)

def safety_check(rights: str, audio_status: str, auto_post: bool = False,
                 public_release_approved: bool = False, private_data: bool = False):
    if rights != "original_procedural":
        raise ValueError("Unapproved source rights: fail closed")
    if audio_status != "sfx_only":
        raise ValueError("Cannot verify existing narration provenance")
    if auto_post or public_release_approved or private_data:
        raise ValueError("Release, posting or private content is not permitted")

def call(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"Command failed: {cmd[:8]}\\n{p.stderr[-2400:]}")
    return p.stdout

def probe(path: Path) -> dict:
    return json.loads(call(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,nb_frames",
        "-of", "json", str(path)]))

def validate_video(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size < 10000:
        raise ValueError("Input MP4 missing or empty")
    info = probe(path)
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not v or not a or v.get("codec_name") != "h264" or a.get("codec_name") != "aac":
        raise ValueError("H264/AAC streams required")
    if (v.get("width"), v.get("height"), v.get("r_frame_rate")) != (1080, 1920, "30/1"):
        raise ValueError("Expected native 1080x1920 at 30fps")
    if abs(float(info["format"]["duration"]) - SECONDS) > .10:
        raise ValueError("Expected 20 second review source")
    return info

def cue_signal(t: float) -> float:
    phrase = t % 2.5
    pad = .011 * math.sin(2 * math.pi * 220 * t) + .005 * math.sin(2 * math.pi * 330 * t)
    decay = math.exp(-phrase * 10.0) * min(1.0, phrase / .018)
    bell = .022 * decay * math.sin(2 * math.pi * 660 * phrase)
    return pad + bell

def smooth_boundary(t: float, duration: float = SECONDS) -> float:
    edge = .11
    return min(1.0, max(0.0, t / edge), max(0.0, (duration - t) / edge))

def synthesize_pcm(samples: int = SAMPLE_RATE * SECONDS) -> array.array:
    if samples <= 0:
        raise ValueError("samples must be positive")
    out = array.array('h')
    for i in range(samples):
        t = i / SAMPLE_RATE
        x = cue_signal(t) * smooth_boundary(t)
        out.append(int(max(-1.0, min(1.0, x)) * 32767))
    return out

def write_wav(path: Path, samples: array.array) -> None:
    if samples.typecode != 'h':
        raise TypeError("16-bit PCM required")
    if os.sys.byteorder != 'little':
        samples = array.array('h', samples)
        samples.byteswap()
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(samples.tobytes())

def build(base: Path, out: Path, *, rights: str, audio_status: str) -> dict:
    safety_check(rights, audio_status)
    validate_video(base)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle503_') as tmp:
        tone = Path(tmp) / 'original_ambient.wav'
        write_wav(tone, synthesize_pcm())
        graph = ('[0:a:0]aformat=sample_rates=44100:channel_layouts=mono[sfx];'
                 '[1:a:0]aformat=sample_rates=44100:channel_layouts=mono[bed];'
                 '[sfx][bed]amix=inputs=2:duration=first:normalize=0,'
                 'alimiter=limit=0.89:attack=5:release=30[a]')
        call(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(base),
              '-i', str(tone), '-filter_complex', graph, '-map', '0:v:0',
              '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
              '-ar', '44100', '-ac', '1', '-t', str(SECONDS),
              '-movflags', '+faststart', str(out)])
    info = validate_video(out)
    call(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(out), '-f', 'null', '-'])
    return {'cycle': 503, 'previous': 502,
            'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
            'probe': info, 'full_decode': 'PASS',
            'new_japanese_narration': 'NOT_GENERATED',
            'audio': 'SFX_PLUS_ORIGINAL_SYNTH_BED',
            'spoken_caption_sync': 'NOT_VERIFIED',
            'caption_overlay': 'UNCHANGED_FROM_CYCLE502',
            'human_review': 'HUMAN_REVIEW', 'publication': 'NOT_APPROVED',
            'auto_post': False, 'genre_reusable': True}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--rights', required=True)
    p.add_argument('--audio-status', required=True)
    a = p.parse_args()
    print(json.dumps(build(a.base, a.out, rights=a.rights,
        audio_status=a.audio_status), ensure_ascii=False, indent=2))
