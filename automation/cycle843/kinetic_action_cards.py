"""cycle843: voice-safe example cards for 10 TikTok genres; review only."""
import argparse
import json
import subprocess
from pathlib import Path

FPS = 30
SCENES = (89, 81, 79, 87, 86, 89, 77, 103)
GENRES = {
    'ai_work': ('&H00E1C7&','&H28180C&'),
    'sales_business': ('&H20E8FF&','&H21101A&'),
    'beauty': ('&HAD8BFF&','&H2A1A24&'),
    'romance': ('&H9F85FF&','&H281A29&'),
    'saving': ('&H71E8A5&','&H201B0E&'),
    'career': ('&HFFB674&','&H281B0F&'),
    'wellness': ('&H99DF8D&','&H1E2214&'),
    'science': ('&HFFE086&','&H221A16&'),
    'travel_food': ('&H86D8FF&','&H241B16&'),
    'product_comparison_lifestyle': ('&HFFB5D6&','&H251721&'),
}
POLICY = {
    'review_only': True, 'publication_approved': False,
    'automatic_posting': False, 'external_upload': False,
    'source_rights_reviewed': False, 'contains_personal_data': False,
}
EXAMPLES = (
    '例：毎朝の売上集計', '例：月次レポートの転記',
    '例：理想のレポート1枚', '例：300字・箇条書き・敬語',
    '例：数字・固有名詞・事実', '例：「結論を先に」に修正',
    '例：テンプレートに登録', '例：朝5分で1件試す',
)
PANEL_TOP, PANEL_BOTTOM, PHOTO_BOTTOM = 1072, 1238, 1300

def check_manifest(manifest, genre):
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('Unsupported genre')
    if any(manifest.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Fail closed: review-only policy mismatch')

def stamp(frames):
    cs = round(frames * 100 / FPS)
    seconds, fraction = divmod(cs, 100)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}:{minutes:02d}:{seconds:02d}.{fraction:02d}'

def generate_ass(genre='ai_work'):
    if genre not in GENRES: raise ValueError('Unknown genre')
    accent, panel = GENRES[genre]
    header = """[Script Info]
Title: cycle843 - example cards, review only
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Panel,Noto Sans CJK JP,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Text,Noto Sans CJK JP,49,&H00FFFFFF,&H00FFFFFF,&H00121A22,&H00000000,1,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1
Style: Small,Noto Sans CJK JP,28,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events, cursor = [], 0
    for i, (duration, example) in enumerate(zip(SCENES, EXAMPLES), 1):
        start, end = stamp(cursor + 5), stamp(cursor + duration - 3)
        rect = 'm 0 0 l 930 0 l 930 166 l 0 166'
        events.append(f'Dialogue: 0,{start},{end},Panel,,0,0,0,,{{\\an7\\pos(75,{PANEL_TOP})\\p1\\1c{panel}\\1a&H28&\\fad(180,140)}}{rect}{{\\p0}}')
        events.append(f'Dialogue: 1,{start},{end},Panel,,0,0,0,,{{\\an7\\pos(75,{PANEL_TOP})\\p1\\1c{accent}\\fad(180,140)}}m 0 0 l 12 0 l 12 166 l 0 166{{\\p0}}')
        events.append(f'Dialogue: 2,{start},{end},Small,,0,0,0,,{{\\an7\\pos(124,1090)\\1c{accent}\\fad(200,140)}}EXAMPLE  {i:02d} / 08')
        events.append(f'Dialogue: 3,{start},{end},Text,,0,0,0,,{{\\an7\\move(124,1175,124,1150,0,240)\\1c&H00FFFFFF&\\fad(220,140)}}{example}')
        cursor += duration
    assert cursor == 691 and len(events) == 32
    return header + '\n'.join(events) + '\n'

def render(source, dest, ass_path):
    if not source.is_file(): raise FileNotFoundError(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    escaped = str(ass_path).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2',
           '-i',str(source),'-vf',f'subtitles=filename={escaped}:fontsdir=/usr/share/fonts/opentype/noto',
           '-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast',
           '-crf','20','-pix_fmt','yuv420p','-r','30','-c:a','copy',
           '-movflags','+faststart',str(dest)]
    result = subprocess.run(cmd,capture_output=True,text=True,timeout=300)
    if result.returncode: raise RuntimeError(result.stderr[-3000:])

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    check_manifest(json.loads(a.manifest.read_text(encoding='utf-8')),a.genre)
    ass=a.output.with_suffix('.ass')
    ass.parent.mkdir(parents=True,exist_ok=True)
    ass.write_text(generate_ass(a.genre),encoding='utf-8')
    render(a.source,a.output,ass)
    print(json.dumps({'output':str(a.output),'genres':len(GENRES),
                      'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'},ensure_ascii=False))
if __name__=='__main__': main()
