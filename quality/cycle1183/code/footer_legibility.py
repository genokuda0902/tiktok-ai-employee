#!/usr/bin/env python3
"""Cycle1183: improve Japanese review-footer legibility without changing narration."""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

GENRE_ACCENTS = {
    'ai': '0x4de0d2', 'business': '0x5fc5e8', 'money': '0xe7bc66',
    'learning': '0x8bcbff', 'health': '0x77d6aa', 'food': '0xf3a67a',
    'travel': '0x6fc9f2', 'beauty': '0xe4a8ce', 'career': '0xa6b7ff',
    'life': '0xb5d1a2',
}
FOOTER=(68,1740,944,128)
FONT_CANDIDATES=(
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
)

def probe(path):
    r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format',
                      '-show_chapters','-of','json',str(path)],capture_output=True,
                     text=True,check=True)
    return json.loads(r.stdout)

def validate(meta, genre, rect=FOOTER):
    if genre not in GENRE_ACCENTS: raise ValueError('unknown genre')
    x,y,w,h=rect
    if x<40 or x+w>1040 or y<1720 or y+h>1880 or min(w,h)<=0:
        raise ValueError('footer rectangle must not touch content, narration or frame edge')
    v=[s for s in meta['streams'] if s.get('codec_type')=='video']
    a=[s for s in meta['streams'] if s.get('codec_type')=='audio']
    if len(v)!=1 or len(a)!=1 or a[0].get('codec_name')!='aac':
        raise ValueError('requires one video and one AAC audio stream')
    if (int(v[0]['width']),int(v[0]['height']))!=(1080,1920) or v[0]['r_frame_rate']!='30/1':
        raise ValueError('requires 1080x1920 30fps')
    return int(v[0]['nb_frames'])

def escape_filter_path(p):
    return str(p).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")

def graph(genre, font, line1_file, line2_file):
    x,y,w,h=FOOTER
    accent=GENRE_ACCENTS[genre]
    font=escape_filter_path(font)
    f1=escape_filter_path(line1_file)
    f2=escape_filter_path(line2_file)
    return (f'[0:v]drawbox=x={x}:y={y}:w={w}:h={h}:color=0x06121e@0.97:t=fill,'
            f'drawbox=x={x}:y={y}:w=5:h={h}:color={accent}@0.90:t=fill,'
            f'drawtext=fontfile={font}:textfile={f1}:fontsize=28:fontcolor=0xdbe9ef:'
            f'x={x+25}:y={y+18}:fix_bounds=1,'
            f'drawtext=fontfile={font}:textfile={f2}:fontsize=24:fontcolor=0xa9c4d0:'
            f'x={x+25}:y={y+70}:fix_bounds=1,format=yuv420p[v]')

def render(source,output,genre='ai',topic='AI時短術',font=None):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve(): raise ValueError('source overwrite forbidden')
    if not topic or len(topic)>20 or any(c in topic for c in '\r\n'):
        raise ValueError('topic must be a single short line')
    n=validate(probe(source),genre)
    font=font or next((f for f in FONT_CANDIDATES if Path(f).exists()),None)
    if not font or not Path(font).is_file(): raise FileNotFoundError('Noto Sans CJK font required')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        f1=Path(d)/'topic.txt';f2=Path(d)/'review.txt'
        f1.write_text(f'{topic}｜架空データで解説',encoding='utf-8')
        f2.write_text('確認用サンプル・社員承認前・投稿禁止',encoding='utf-8')
        cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-filter_complex',graph(genre,font,f1,f2),'-map','[v]','-map','0:a:0',
             '-map_metadata','0','-map_chapters','0','-c:v','libx264','-preset','veryfast',
             '-crf','17','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(n),
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True)
    actual=probe(output)
    v=next(s for s in actual['streams'] if s['codec_type']=='video')
    if int(v['nb_frames'])!=n: raise RuntimeError('output frame count changed')
    return {'genre':genre,'frames':n,'footer':FOOTER,'font_size':[28,24],
            'publication_approved':False,'semantic_asr_verified':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',default='ai',choices=GENRE_ACCENTS)
    p.add_argument('--topic',default='AI時短術')
    p.add_argument('--font')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,a.topic,a.font),ensure_ascii=False,indent=2))
