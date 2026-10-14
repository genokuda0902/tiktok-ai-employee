#!/usr/bin/env python3
"""cycle567: visible review-only visual annotations, not speech transcripts.

Audio and soft subtitle streams are copied bit-for-bit from the input container.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

CUES = [
    (0.0, 2.0, '4か月の売上を、まず確認'),
    (2.0, 4.0, '120＋150＋200＋250'),
    (4.0, 6.0, '元データの合計は720'),
    (6.0, 9.0, '集計の指示を入力（再現）'),
    (9.0, 12.0, 'SUMの範囲を確認'),
    (12.0, 15.5, '表とグラフの数値を照合'),
    (15.5, 18.5, '計算途中と確定を区別'),
    (18.5, 20.0, '保存して、後で検算'),
]
PANEL = (50, 1625, 1030, 1775)
VIDEO = (1080, 1920)

def ts(t: float) -> str:
    return f'{int(t//3600)}:{int(t//60)%60:02}:{t%60:05.2f}'

def make_ass(path: Path, cues=CUES) -> None:
    if not (1 <= len(cues) <= 12) or cues[0][0] != 0 or cues[-1][1] != 20 or any(cues[i][1] != cues[i+1][0] for i in range(len(cues)-1)):
        raise ValueError("cue timeline must cover 0..20s without gaps or overlaps")
    header = '''[Script Info]
Title: cycle567 review-only visual step cues
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,70,&H00FFFFFF,&H00000000,&H000F2431,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,0,0,0,1
Style: Label,Noto Sans CJK JP,31,&H009AFFFF,&H00000000,&H000F2431,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines = [header]
    for i, (a, b, caption) in enumerate(cues, 1):
        if not 0 <= a < b <= 20.0 or '\\' in caption or '\n' in caption or len(caption) > 26:
            raise ValueError('unsafe cue data')
        start, end = ts(a), ts(b)
        shape = r'{\an7\pos(50,1625)\p1\1c&H38290D&\alpha&H12000000&\fad(120,120)}m 0 0 l 980 0 980 150 0 150'
        label = r'{\an7\pos(90,1636)\fad(120,120)}VISUAL STEP ' + f'{i:02}/{len(cues):02}'
        title = r'{\an5\pos(540,1715)\fad(120,120)}' + caption
        lines += [f'Dialogue: 0,{start},{end},Caption,,0,0,0,,{shape}\n',
                  f'Dialogue: 1,{start},{end},Label,,0,0,0,,{label}\n',
                  f'Dialogue: 2,{start},{end},Caption,,0,0,0,,{title}\n']
    path.write_text(''.join(lines), encoding='utf-8')

def render(source: Path, output: Path, cues=CUES, genre="ai_productivity") -> dict:
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    ass = output.parent / 'cycle567_visible_cues.ass'
    make_ass(ass, cues)
    filter_arg = 'ass=' + str(ass).replace('\\', '\\\\').replace(':', '\\:')
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
           '-vf',filter_arg,'-map','0:v:0','-map','0:a:0','-map','0:s:0',
           '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
           '-c:a','copy','-c:s','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd, check=True)
    result = {
        'cycle': 567, 'source': source.name, 'output': output.name,
        'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'change': 'burn-in 8 non-speech visual step cues in dedicated lower panel',
        'genre': genre, 'caption_intervals': len(cues), 'caption_region': PANEL,
        'critical_content_region': [0,0,1080,1600],
        'narration': 'NOT_GENERATED', 'voice_transcript_match': 'NOT_TESTABLE',
        'audio': 'cycle566 original procedural instrumental, copied',
        'soft_subtitles': 'cycle566 soft subtitle stream copied',
        'rights': 'synthetic inherited visuals; final human review required',
        'publication': 'NOT_APPROVED', 'cost_jpy': 0,
    }
    (output.parent/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--cues-json',type=Path,help='JSON {genre,cues:[{start,end,text}]} for other genres')
    args=p.parse_args()
    spec=json.loads(args.cues_json.read_text(encoding='utf8')) if args.cues_json else {}
    cues=[(float(x['start']),float(x['end']),str(x['text'])) for x in spec['cues']] if spec else CUES
    print(json.dumps(render(args.source,args.output,cues,spec.get('genre','ai_productivity')),ensure_ascii=False,indent=2))
