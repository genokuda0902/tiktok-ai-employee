#!/usr/bin/env python3
"""Review-only, generic formula evidence magnifier. No private media in repo.

This overlay is placed in the verified blank portion of an AI-work Calc GUI
scene, never in the burned Japanese caption region. Other genres fail closed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
START, END = 174, 261  # 5.80-8.70 seconds, 87 frames
SAFE_Y = 1440
ORIGIN = (35, 28)
SIZE = (859, 77)
GENRES = ('ai_work', 'finance', 'learning', 'health', 'travel',
          'food', 'science', 'history', 'business', 'lifestyle')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-show_entries', 'format=duration', '-of', 'json', str(path)]))


def validate_genre(genre, synthetic=False):
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    if genre != 'ai_work' and not synthetic:
        raise ValueError('Unreviewed geometry: fail closed')


def beat(i, count):
    if not 0 <= i < count:
        raise ValueError('Invalid overlay frame')
    return 0 if i < count // 2 else 1


def overlay_frame(i, count):
    """Rebuild the existing top banner, not the spreadsheet or subtitle area."""
    active = beat(i, count)
    im = Image.new('RGBA', SIZE, (0,0,0,0))
    d = ImageDraw.Draw(im, 'RGBA')
    jp = ImageFont.truetype(FONT, 25)
    formula = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 25)
    big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
    label, expr, result = [('営業A', '=SUM(B2:B4)', '46'),
                           ('営業B', '=SUM(C2:C4)', '29')][active]
    # Keep explicit source provenance visible; no claim this is Excel/ChatGPT.
    d.rounded_rectangle((1,1,SIZE[0]-2,SIZE[1]-2), radius=12,
                        fill=(9,43,61,255), outline=(67,213,204,255), width=3)
    d.text((17,17),'LibreOffice Calc｜実操作',font=jp,fill=(232,255,250,255))
    d.line(((338,13),(338,54)),fill=(59,130,144,255),width=2)
    d.text((353,17),label,font=jp,fill=(230,255,250,255))
    d.text((443,18),expr,font=formula,fill=(210,248,241,255))
    d.text((783,11),result,font=big,fill=(255,255,255,255))
    return im


def render(source, output, work, expected_sha=None, genre='ai_work',
           synthetic=False, start=START, end=END):
    validate_genre(genre, synthetic)
    source, output, work = map(Path, (source, output, work))
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError('Refuse to overwrite input')
    source_hash = sha256(source)
    if not synthetic and (not expected_sha or expected_sha != source_hash):
        raise ValueError('Source SHA approval required; fail closed')
    info = probe(source)
    v = [s for s in info['streams'] if s['codec_type']=='video']
    a = [s for s in info['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac':
        raise ValueError('Expected H.264 and AAC')
    if (v[0]['width'], v[0]['height'], v[0]['r_frame_rate']) != (1080,1920,'30/1'):
        raise ValueError('Unreviewed resolution/FPS')
    n = int(v[0].get('nb_frames') or 0)
    if not 0 <= start < end <= n:
        raise ValueError('Invalid frame interval')
    if ORIGIN[1] + SIZE[1] >= 110 or ORIGIN[1] + SIZE[1] >= SAFE_Y:
        raise ValueError('Source GUI or caption safe area violated')
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    frames = work/'focus_frames'
    frames.mkdir(exist_ok=True)
    for i in range(end-start):
        overlay_frame(i,end-start).save(frames/f'{i:04d}.png')
    x,y=ORIGIN
    graph=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/{FPS}/TB[focus];'
           f"[0:v][focus]overlay=x={x}:y={y}:eof_action=pass:enable='between(n,{start},{end-1})'[v]")
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate',str(FPS),'-i',str(frames/'%04d.png'),'-filter_complex',graph,
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset',
         'ultrafast' if synthetic else 'veryfast','-crf','19','-pix_fmt','yuv420p',
         '-r',str(FPS),'-frames:v',str(n),'-c:a','copy','-movflags','+faststart',str(output)])
    result=probe(output)
    vv=[s for s in result['streams'] if s['codec_type']=='video'][0]
    aa=[s for s in result['streams'] if s['codec_type']=='audio'][0]
    if int(vv.get('nb_frames') or 0)!=n or aa['codec_name']!='aac':
        raise RuntimeError('Output verification failed')
    return {'input_sha256':source_hash,'output_sha256':sha256(output),
            'start_frame':start,'end_exclusive':end,'frames':n,'genre':genre,
            'caption_safe_y':SAFE_Y,'review_only':True,'publication_approved':False}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--work',required=True)
    p.add_argument('--expected-sha')
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    p.add_argument('--start',type=int,default=START)
    p.add_argument('--end',type=int,default=END)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.work,a.expected_sha,
        a.genre,a.synthetic,a.start,a.end),indent=2))
