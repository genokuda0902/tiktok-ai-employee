#!/usr/bin/env python3
"""Review-only 10-genre Japanese caption legibility upgrade.

Renders from the uncaptioned, SHA-allowlisted cycle757 baseline; does not
publish, upload, use private assets, or assert speech-to-caption alignment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

GENRE_ACCENTS = {
    'ai_work': '&H00DDF44E', 'romance': '&H00C086FF',
    'beauty': '&H00FFA6CB', 'money': '&H00A9E984',
    'trivia': '&H0073CBFF', 'gadgets': '&H00FFB87C',
    'health': '&H00D1E49B', 'sales': '&H007AB3F7',
    'travel': '&H00EFD975', 'mystery': '&H00FAA5BE',
}
# Text is shortened for readability. It is a summary, not verbatim narration.
CAPTION_LINES = (
    ('Excel集計、', 'まだ手作業？', '手作業'),
    ('架空の4か月', 'データを準備', '4か月'),
    ('表をAIへ渡し', 'グラフを依頼', 'AI'),
    ('AIがグラフを', '表示', 'グラフ'),
    ('1月12万・', '2月15万', '12万'),
    ('3月20万・', '4月18万', '20万'),
    ('合計65万円', '最後は人が確認', '65万円'),
    ('保存して', 'あとで試そう', '保存'),
)
FRAME_WIDTH, FRAME_HEIGHT = 1080, 1920
CAPTION_X, CAPTION_Y = 480, 1680  # Provisional placement; TikTok app UI not verified.
MAX_LINE_CHARS = 10


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def parse_srt(raw: str) -> list[tuple[int, int]]:
    blocks = re.split(r'\n\s*\n', raw.strip().replace('\r\n', '\n'))
    def to_ms(s: str) -> int:
        m = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', s)
        if not m:
            raise ValueError('invalid timestamp')
        hh, mm, ss, milli = map(int, m.groups())
        if mm > 59 or ss > 59:
            raise ValueError('invalid time component')
        return ((hh * 60 + mm) * 60 + ss) * 1000 + milli
    cues = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError('invalid SRT cue')
        parts = lines[1].strip().split(' --> ')
        if len(parts) != 2:
            raise ValueError('invalid SRT range')
        a, b = map(to_ms, parts)
        if a >= b:
            raise ValueError('invalid cue duration')
        cues.append((a, b))
    if len(cues) != 8 or cues[0][0] != 0 or not 27200 <= cues[-1][1] <= 27400:
        raise ValueError('unexpected narration cue count or duration')
    if any(a[1] != b[0] for a, b in zip(cues, cues[1:])):
        raise ValueError('gap or overlap in cue timeline')
    return cues


def ass_time(ms: int) -> str:
    cs = (ms + 5) // 10
    hh, rem = divmod(cs, 360000)
    mm, rem = divmod(rem, 6000)
    ss, cc = divmod(rem, 100)
    return f'{hh}:{mm:02}:{ss:02}.{cc:02}'


def validate_layout() -> None:
    if not (120 <= CAPTION_X <= 530 and 1200 <= CAPTION_Y <= 1680):
        raise ValueError('caption position outside configured review band')
    for line1, line2, keyword in CAPTION_LINES:
        if len(line1) > MAX_LINE_CHARS or len(line2) > MAX_LINE_CHARS:
            raise ValueError('caption line too long')
        if keyword not in (line1 + line2):
            raise ValueError('highlight keyword absent')
        if any(ch in (line1 + line2) for ch in ('\\', '{', '}', '\n', '\r')):
            raise ValueError('ASS control character in caption')


def make_ass(cues: list[tuple[int, int]], genre: str = 'ai_work') -> str:
    if genre not in GENRE_ACCENTS:
        raise ValueError('unknown genre')
    validate_layout()
    if len(cues) != len(CAPTION_LINES):
        raise ValueError('cue/caption count mismatch')
    accent = GENRE_ACCENTS[genre]
    header = '''[Script Info]
Title: cycle759 mobile-readable caption experiment - REVIEW ONLY
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Large,Noto Sans CJK JP,68,&H00FFFFFF,&H00FFFFFF,&H0008101D,&H7606101B,-1,0,0,0,100,100,0,0,3,14,0,2,100,210,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines = []
    for (start, end), (top, bottom, keyword) in zip(cues, CAPTION_LINES):
        combined = top + r'\N' + bottom
        # Restrict keyword to a static known literal; no user-controlled ASS markup.
        highlighted = combined.replace(keyword, '{\\c' + accent + '}' + keyword + '{\\c&H00FFFFFF&}', 1)
        effect = '{\\an2\\pos(' + str(CAPTION_X) + ',' + str(CAPTION_Y) + ')\\fad(120,100)}'
        lines.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Large,,0,0,0,,{effect}{highlighted}')
    return header + '\n'.join(lines) + '\n'


def render(source: Path, srt: Path, output: Path, expected_sha: str, genre='ai_work') -> dict:
    source, srt, output = Path(source), Path(srt), Path(output)
    if not re.fullmatch(r'[0-9a-f]{64}', expected_sha):
        raise ValueError('required allowlisted SHA256')
    if not source.is_file() or not srt.is_file() or sha256(source) != expected_sha:
        raise ValueError('source media not present or SHA256 allowlisted')
    if source.resolve() == output.resolve():
        raise ValueError('cannot overwrite input')
    cues = parse_srt(srt.read_text(encoding='utf-8-sig'))
    output.parent.mkdir(parents=True, exist_ok=True)
    ass = output.with_suffix('.ass')
    ass.write_text(make_ass(cues, genre), encoding='utf-8')
    escaped = str(ass.resolve()).replace('\\', r'\\').replace(':', r'\:').replace("'", r"\'")
    subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-loglevel', 'error',
                    '-i', str(source), '-vf',
                    f'drawbox=x=0:y=1530:w=1080:h=220:color=0x06101C@0.87:t=fill,'
                    f'drawbox=x=0:y=1530:w=1080:h=4:color=0x30DED4@0.85:t=fill,'
                    f'ass=filename={escaped}',
                    '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-r', '30', '-c:a', 'copy', '-movflags', '+faststart', str(output)],
                   check=True, timeout=240)
    return {'cycle': 759, 'source_sha256': expected_sha, 'output_sha256': sha256(output),
            'ass_sha256': sha256(ass), 'caption_count': len(cues), 'genre': genre,
            'publication': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--srt', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--expected-sha', required=True)
    p.add_argument('--genre', choices=tuple(GENRE_ACCENTS), default='ai_work')
    a = p.parse_args()
    print(json.dumps(render(a.source, a.srt, a.output, a.expected_sha, a.genre),
                     ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
