#!/usr/bin/env python3
"""cycle566: genre-neutral rights-safe review soundtrack; NO Japanese narration.

Reimplementation: retains cycle565 original synthetic visuals only, never reuses
its unverified audio. Generates deterministic procedural score and scene cues.
"""
from pathlib import Path
import argparse, hashlib, json, math, struct, subprocess, wave

SAMPLE_RATE = 44100
DURATION = 20.0
CUES = (2.0, 4.0, 6.0, 9.0, 12.0, 15.5, 18.5)
CAPTIONS = [
    (0, 2, '4か月の売上を、まず確認'),
    (2, 4, '120＋150＋200＋250'),
    (4, 6, '元データの合計は720'),
    (6, 9, '集計の指示を入力（再現）'),
    (9, 12, 'SUMの範囲を確認'),
    (12, 15.5, '表とグラフの数値を照合'),
    (15.5, 18.5, '計算途中と確定を区別'),
    (18.5, 20, '保存して、後で検算'),
]

def score(path: Path):
    """Write original, deterministic mono 16-bit PCM (no licensed source)."""
    notes = (196.00, 246.94, 293.66, 392.00)
    count = int(DURATION * SAMPLE_RATE)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SAMPLE_RATE)
        buf = bytearray()
        for i in range(count):
            t = i / SAMPLE_RATE
            fade = min(1.0, t / 0.18, (DURATION-t) / 0.26)
            # Gentle chord and slow pulse, below voice-mix loudness.
            chord = sum(math.sin(2*math.pi*f*t + 0.15*math.sin(2*math.pi*0.16*t)) for f in notes) / 4
            base = 0.055 * chord * (0.78 + 0.22*math.sin(2*math.pi*0.5*t)**2)
            cue = 0.0
            for j, at in enumerate(CUES):
                dt = t-at
                if 0 <= dt < 0.18:
                    cue += 0.11 * math.exp(-23*dt) * math.sin(2*math.pi*(640+40*j)*dt)
            val = max(-0.85, min(0.85, (base+cue)*max(0, fade)))
            buf.extend(struct.pack('<h', round(val*32767)))
            if len(buf) >= 262144:
                w.writeframesraw(buf); buf.clear()
        if buf: w.writeframesraw(buf)

def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def make_srt(path):
    path.write_text(''.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{caption}\n\n' for i,(a,b,caption) in enumerate(CAPTIONS,1)), encoding='utf-8')

def render(source:Path, target:Path):
    target.parent.mkdir(parents=True,exist_ok=True)
    wav=target.parent/'cycle566_original_score.wav'
    srt=target.parent/'cycle566_visual_captions.srt'
    score(wav); make_srt(srt)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(wav),'-i',str(srt),
         '-map','0:v:0','-map','1:a:0','-map','2:s:0','-c:v','copy','-c:a','aac','-b:a','160k',
         '-c:s','mov_text','-ar',str(SAMPLE_RATE),'-t','20','-movflags','+faststart',
         '-metadata:s:s:0','language=jpn','-metadata','comment=REVIEW_ONLY; no narration; original procedural audio',str(target)]
    subprocess.run(cmd,check=True)
    manifest={'cycle':'566','source_visual':source.name,'audio_provenance':'deterministic procedural synthesis, created by this script',
       'inherited_audio_used':False,'japanese_narration':'NOT_GENERATED','captions':'visual descriptions, not voice transcripts',
       'scene_cues_seconds':CUES,'caption_count':len(CAPTIONS),'asset_rights':'visual source inherited from cycle565: human review required',
       'publication':'NOT_APPROVED','output_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    (target.parent/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();print(json.dumps(render(Path(a.source),Path(a.output)),ensure_ascii=False,indent=2))
