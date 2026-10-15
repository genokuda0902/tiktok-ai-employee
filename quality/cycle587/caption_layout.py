"""Offline caption placement with scene-aware exclusion regions for review-only videos.

This is a reimplementation, NOT the original v33 renderer. No asset, audio,
private source video, or publishing credentials are embedded in this module.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess

WIDTH, HEIGHT = 1080, 1920
DURATION_MS = 20_000
GENRES = (
    'AI_productivity', 'beauty', 'relationships', 'money', 'sales',
    'career', 'health', 'science', 'travel_food', 'product_comparison',
)

@dataclass(frozen=True)
class Rect:
    left: int
    top: int
    right: int
    bottom: int

    def intersects(self, other: 'Rect') -> bool:
        return (self.left < other.right and other.left < self.right
                and self.top < other.bottom and other.top < self.bottom)


@dataclass(frozen=True)
class Cue:
    start_ms: int
    end_ms: int
    text: str
    scene: str = 'default'


# Deliberately explicit per-scene geometry; auto-layout MUST fail closed if no
# collision-free placement is known. Generic genres can use the same contract.
CAPTION_BOXES = {
    'default': Rect(145, 1260, 935, 1420),
    'chart_proof': Rect(280, 827, 800, 869),
}
SCENE_EXCLUSIONS = {
    'chart_proof': (
        Rect(35, 40, 900, 475),      # scene heading and lead text
        Rect(35, 500, 900, 826),     # source data cells
        Rect(35, 875, 900, 1620),    # chart and x-axis labels
        Rect(35, 1660, 900, 1850),   # native evidence callout
    ),
}


def parse_srt(path: Path) -> list[Cue]:
    raw = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').strip()
    cues: list[Cue] = []
    for block in re.split(r'\n\s*\n', raw):
        lines = [x.strip() for x in block.splitlines() if x.strip()]
        if lines and lines[0].isdigit():
            lines.pop(0)
        if len(lines) < 2 or ' --> ' not in lines[0]:
            raise ValueError('Invalid SRT cue')
        def millis(tc: str) -> int:
            hh, mm, ss, ms = map(int, re.split(r'[:,]', tc))
            return ((hh * 60 + mm) * 60 + ss) * 1000 + ms
        start, end = (millis(t) for t in lines[0].split(' --> '))
        text = ''.join(lines[1:])
        if not text or any(x in text for x in ('{', '}', '\\')):
            raise ValueError('Unsafe/empty text')
        if not 0 <= start < end <= DURATION_MS or (cues and start < cues[-1].end_ms):
            raise ValueError('Overlapping/out-of-bounds cue')
        scene = 'chart_proof' if start == 12000 and end == 16000 else 'default'
        cues.append(Cue(start, end, text, scene))
    if not cues:
        raise ValueError('No cues')
    return cues


def validate_geometry(cue: Cue, genre: str = 'AI_productivity') -> None:
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    box = CAPTION_BOXES.get(cue.scene)
    if box is None:
        raise ValueError('Unknown scene layout')
    if not (0 <= box.left < box.right <= WIDTH and 192 <= box.top < box.bottom <= 1536):
        raise ValueError('Caption violates vertical safe area')
    if any(box.intersects(excluded) for excluded in SCENE_EXCLUSIONS.get(cue.scene, ())):
        raise ValueError('Caption overlaps protected content')
    if cue.scene == 'chart_proof' and len(cue.text) > 14:
        raise ValueError('Gap caption too long')


def ass_timestamp(ms: int) -> str:
    sec, centis = divmod(ms // 10, 100)
    return f'{sec//3600}:{sec//60%60:02d}:{sec%60:02d}.{centis:02d}'


def wrap(text: str, width: int = 12) -> str:
    if len(text) <= width:
        return text
    # One or two lines only; Japanese punctuation makes more natural breaks.
    splits = [i+1 for i, c in enumerate(text[:width]) if c in '、。 ']
    n = splits[-1] if splits else (len(text) + 1) // 2
    if max(len(text[:n]), len(text[n:])) > width:
        raise ValueError('Caption too long')
    return text[:n] + r'\N' + text[n:]


def make_ass(cues: list[Cue], genre: str = 'AI_productivity') -> str:
    for cue in cues:
        validate_geometry(cue, genre)
    head = '''[Script Info]
Title: Scene-aware Japanese captions / review only
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Normal,Noto Sans CJK JP,86,&H00FFFFFF,&H00FFFFFF,&H66071525,&H66071525,-1,0,0,0,100,100,0,0,3,10,0,2,145,195,300,1
Style: Gap,Noto Sans CJK JP,46,&H00FFFFFF,&H00FFFFFF,&H66071525,&H66071525,-1,0,0,0,100,100,0,0,3,4,0,5,100,100,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    for c in cues:
        if c.scene == 'chart_proof':
            # 827-869px empty gap between the source card and the chart card.
            content = r'{\pos(540,849)}' + c.text
            style = 'Gap'
        else:
            content = wrap(c.text)
            style = 'Normal'
        head += f'Dialogue: 0,{ass_timestamp(c.start_ms)},{ass_timestamp(c.end_ms)},{style},,0,0,0,,{content}\n'
    return head


def render(source: Path, srt: Path, out: Path, genre: str = 'AI_productivity') -> Path:
    if not source.is_file() or source.stat().st_size == 0:
        raise FileNotFoundError(source)
    out.parent.mkdir(parents=True, exist_ok=True)
    ass = out.with_suffix('.ass')
    ass.write_text(make_ass(parse_srt(srt), genre), encoding='utf-8')
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(source),
           '-vf', f'ass={ass}:fontsdir=/usr/share/fonts/opentype/noto',
           '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264',
           '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
           '-c:a', 'copy', '-t', '20', '-movflags', '+faststart',
           '-metadata', 'comment=REVIEW ONLY - no publication approval', str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (out.parent / 'render.log').write_text(f'command: {cmd!r}\nexit={r.returncode}\n{r.stderr}', encoding='utf-8')
    if r.returncode:
        raise RuntimeError(r.stderr[-1000:])
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--srt', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--genre', default='AI_productivity')
    a = p.parse_args()
    print(render(a.source, a.srt, a.out, a.genre))
