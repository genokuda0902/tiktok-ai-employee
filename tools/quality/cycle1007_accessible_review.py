#!/usr/bin/env python3
"""Offline review-only MP4 accessibility mux: selectable JP text + chapter navigation.

The 8 text cues are *manual transcriptions of visible, burned-in scene captions*,
NOT independent ASR or verified narration transcription. Never auto-publish.
Source video/audio packets are stream-copied. No rights clearance is implied.
"""
from __future__ import annotations
import argparse
import dataclasses
import json
import subprocess
import tempfile
from pathlib import Path

GENRES = ('ai_work', 'business', 'finance', 'education', 'health',
          'travel', 'cooking', 'lifestyle', 'technology', 'entertainment')
PUBLICATION = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'

@dataclasses.dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str
    chapter: str

# Boundary estimates checked against source video scene-cut frames:
# 0, 79, 174, 262, 348, 435, 515, 609, 691 @ 30fps.
# Cues represent on-screen Japanese text, NOT speech-aligned transcripts.
CUT_FRAMES = (0, 79, 174, 262, 348, 435, 515, 609, 691)
TEXTS = (
    'AIで仕事を早くするなら、最初の一歩が大事。',
    'まず、繰り返している作業を書き出す。',
    '次に、完成形の見本を用意する。',
    '指示は、目的と条件を具体的に伝える。',
    '最初の出力は、必ず自分で確かめる。',
    '違いがあれば、修正点を一つずつ伝える。',
    '使える指示は、テンプレートに残す。',
    '小さな時短を、毎日の習慣にしよう。',
)
CHAPTERS = (
    '最初の一歩', '作業を書き出す', '完成形の見本', '目的と条件',
    '出力の確認', '修正点を伝える', 'テンプレート化', '毎日の習慣',
)

def default_cues() -> tuple[Cue, ...]:
    return tuple(Cue(round(CUT_FRAMES[i]/30 + .10, 3),
                     round(CUT_FRAMES[i+1]/30 - .07, 3),
                     TEXTS[i], CHAPTERS[i]) for i in range(8))

def validate_cues(cues: tuple[Cue, ...], duration: float) -> None:
    if not cues:
        raise ValueError('empty captions')
    last = -1.0
    for cue in cues:
        if not cue.text.strip() or not cue.chapter.strip():
            raise ValueError('blank cue or chapter')
        if not (0 <= cue.start < cue.end <= duration + .02):
            raise ValueError('cue outside duration')
        if cue.start < last:
            raise ValueError('overlapping or unordered cues')
        last = cue.end

def stamp(t: float) -> str:
    ms = round(t*1000)
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def srt_text(cues: tuple[Cue, ...]) -> str:
    return ''.join(f'{i}\n{stamp(c.start)} --> {stamp(c.end)}\n{c.text}\n\n'
                   for i, c in enumerate(cues, 1))

def ffmetadata(cues: tuple[Cue, ...], duration: float) -> str:
    lines = [';FFMETADATA1', 'title=AI仕事術 | 社内確認用（未承認）']
    for i, c in enumerate(cues):
        start = 0 if i == 0 else round(CUT_FRAMES[i]/30*1000)
        end = round(CUT_FRAMES[i+1]/30*1000) if len(cues)==8 else round(c.end*1000)
        lines += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={start}', f'END={end}',
                  f'title={i+1:02}/{len(cues):02} {c.chapter}']
    return '\n'.join(lines)+'\n'

def run(args: list[str], timeout: int = 240) -> str:
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f'{args[0]} exit={p.returncode}: {p.stderr[-1500:]}')
    return p.stdout

def probe(path: Path) -> dict:
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_format', '-of', 'json', str(path)]))

def mux(source: Path, output: Path, *, genre: str = 'ai_work',
        cues: tuple[Cue, ...] | None = None, synthetic_test: bool = False) -> dict:
    source, output = Path(source), Path(output)
    if genre not in GENRES:
        raise ValueError('unknown genre')
    # Prevent accidental use of AI-work Japanese copy on other genres.
    if genre != 'ai_work':
        raise ValueError('genre-specific text requires approved cues: fail closed')
    if not source.is_file() or source.stat().st_size == 0:
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError('never overwrite source')
    if not synthetic_test and cues is not None:
        raise ValueError('custom cues only permitted in synthetic CI tests')
    meta = probe(source)
    streams = meta['streams']
    video = next((s for s in streams if s['codec_type']=='video'), None)
    audio = next((s for s in streams if s['codec_type']=='audio'), None)
    if not video or not audio:
        raise ValueError('both video and audio are required')
    if (video['codec_name'], video['width'], video['height'],
            video['avg_frame_rate']) != ('h264', 1080, 1920, '30/1'):
        raise ValueError('expected H264 1080x1920 30fps')
    if audio['codec_name'] != 'aac' or audio['sample_rate'] != '48000':
        raise ValueError('expected AAC 48kHz')
    duration = float(meta['format']['duration'])
    if not synthetic_test and not (23.0 <= duration <= 23.1):
        raise ValueError('unexpected review master duration')
    if synthetic_test and cues is None:
        cues = (Cue(0.1, min(duration-0.1, 1.8), '合成テスト字幕', '合成検証'),)
    cues = tuple(cues if cues is not None else default_cues())
    validate_cues(cues, duration)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle1007_') as td:
        srt, chapters = Path(td)/'screen_text.srt', Path(td)/'chapters.ffmeta'
        srt.write_text(srt_text(cues), encoding='utf-8')
        chapters.write_text(ffmetadata(cues, duration), encoding='utf-8')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-i', str(source), '-f', 'srt', '-i', str(srt),
               '-f', 'ffmetadata', '-i', str(chapters),
               '-map', '0:v:0', '-map', '0:a:0', '-map', '1:s:0',
               '-map_metadata', '2', '-map_chapters', '2',
               '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text',
               '-metadata:s:a:0', 'language=jpn',
               '-metadata:s:s:0', 'language=jpn',
               '-metadata:s:s:0', 'title=画面字幕の転記・音声未照合',
               '-disposition:s:0', '0', '-movflags', '+faststart', str(output)]
        run(cmd)
    out = probe(output)
    return {'genre':genre,'source':str(source),'output':str(output),
            'duration':duration,'cue_count':len(cues),'chapter_count':len(cues),
            'screen_text_only':True,'independent_asr':False,
            'audio_semantic_sync':'NOT_VERIFIED', 'publication':PUBLICATION,
            'streams':[(s['codec_type'],s['codec_name']) for s in out['streams']]}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai_work',choices=GENRES)
    p.add_argument('--synthetic-test',action='store_true',
                   help='CI only; never for real private video')
    a=p.parse_args()
    print(json.dumps(mux(Path(a.source),Path(a.output),genre=a.genre,
                         synthetic_test=a.synthetic_test),ensure_ascii=False,indent=2))
