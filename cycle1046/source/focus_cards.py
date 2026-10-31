#!/usr/bin/env python3
"""Review-only, offline 10-genre scene focus cards. Never posts or uploads media.

Only the upper picture of scene 2 (2.9–5.8 s) is replaced; inherited Japanese
captions and original AAC remain unchanged. Other genres fail closed without
approved media. This is a new reimplementation, not the original v33 renderer.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
START, END, PROTECTED_Y = 87, 174, 1460
SOURCE_SHA = '5d6415d4879e802f40c982a2313742de1471101286b0f04e5b4fe40c6cbd8f77'
GENRES = ('ai_work','beauty','romance_psychology','money_saving','sales_business',
          'career','health_lifestyle','science_trivia','travel_food','product_comparison_lifestyle')
PALETTES = {g: c for g, c in zip(GENRES, ('#24D9D2','#F28DAB','#C7A4FB','#FFD166',
             '#69A9FF','#8DD6A0','#F9A86C','#B8D8FF','#FFB18A','#E2B5F8'))}
CARDS = ('データの集計', '報告メール', '資料の整形')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()


def cmd(args, binary=False):
    p = subprocess.run([str(a) for a in args], capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
    return p.stdout if binary else p.stdout.decode()


def audio_sha(path):
    return hashlib.sha256(cmd(['ffmpeg','-v','error','-i',path,'-map','0:a:0',
                               '-c','copy','-f','adts','-'], True)).hexdigest()


def validate(path, expected_sha, genre, review_only):
    if not review_only: raise ValueError('review-only required')
    if genre not in GENRES: raise ValueError('unknown genre')
    if genre != 'ai_work': raise ValueError('approved source missing for this genre')
    if expected_sha != SOURCE_SHA or sha256(path) != SOURCE_SHA:
        raise ValueError('private source SHA mismatch')
    info = json.loads(cmd(['ffprobe','-v','error','-show_streams','-of','json',path]))
    v = [s for s in info['streams'] if s['codec_type']=='video']
    a = [s for s in info['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or v[0]['width']!=W or v[0]['height']!=H or \
       v[0]['r_frame_rate']!='30/1' or int(v[0]['nb_frames'])!=691 or \
       a[0]['codec_name']!='aac' or int(a[0]['sample_rate'])!=48000:
        raise ValueError('unexpected source media profile')


def visible_cards(local_frame):
    if not 0 <= local_frame < END-START: raise ValueError('frame outside scene')
    return min(3, 1 + local_frame // 24)


def make_frame(local_frame, genre='ai_work', width=W, height=PROTECTED_Y):
    if genre not in PALETTES: raise ValueError('unknown genre')
    if width < 540 or height < 800: raise ValueError('canvas too small')
    accent = PALETTES[genre]
    img = Image.new('RGB',(width,height),'#071322')
    d = ImageDraw.Draw(img)
    for y in range(height):
        t=y/height
        d.line((0,y,width,y),fill=(int(7+7*t),int(19+10*t),int(34+13*t)))
    # restrained grid; large empty margins instead of nested text panels
    for x in range(80,width,120): d.line((x,0,x,height),fill='#102A3A',width=1)
    for y in range(110,height,140): d.line((0,y,width,y),fill='#102A3A',width=1)
    scale=width/W
    def pos(v): return int(v*scale)
    def f(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,pos(size))
    d.rounded_rectangle((pos(62),pos(84),pos(314),pos(154)),radius=pos(28),fill='#0F3342',outline=accent,width=3)
    d.text((pos(92),pos(95)),'STEP 01 / 08',font=f(34,True),fill=accent)
    d.text((pos(64),pos(214)),'繰り返す作業を',font=f(74,True),fill='white')
    d.text((pos(64),pos(320)),'3つ書き出そう',font=f(74,True),fill='white')
    d.text((pos(68),pos(443)),'最初は「毎日やっていること」から',font=f(34),fill='#B9CDD7')
    count=visible_cards(local_frame)
    for i,label in enumerate(CARDS):
        y=pos(540+i*172)
        if i >= count: continue
        active=(i==min(2,local_frame//24))
        fill='#14414C' if active else '#112638'
        stroke=accent if active else '#355466'
        d.rounded_rectangle((pos(64),y,pos(1016),y+pos(142)),radius=pos(26),fill=fill,outline=stroke,width=pos(4 if active else 2))
        d.rounded_rectangle((pos(91),y+pos(26),pos(180),y+pos(114)),radius=pos(20),fill=accent if active else '#234A5C')
        d.text((pos(107),y+pos(39)),f'{i+1:02d}',font=f(38,True),fill='#061725' if active else '#D8EDF4')
        d.text((pos(217),y+pos(35)),label,font=f(54,True),fill='white' if active else '#C6D9E0')
    d.line((pos(70),pos(1140),pos(1010),pos(1140)),fill='#3D6979',width=2)
    d.text((pos(70),pos(1170)),'まずは 1つ選んで試す',font=f(35,True),fill=accent)
    return img


def render(source, output, expected_sha, genre='ai_work', review_only=False):
    validate(source,expected_sha,genre,review_only)
    source_audio=audio_sha(source)
    with tempfile.TemporaryDirectory(prefix='cycle1046_') as tmp:
        folder=Path(tmp)
        for n in range(END-START):
            make_frame(n,genre).save(folder/f'{n:03d}.png',optimize=True)
        filtergraph=f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]'
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate',str(FPS),'-i',str(folder/'%03d.png'),'-filter_complex',filtergraph,
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
             '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',output])
    if audio_sha(output)!=source_audio: raise RuntimeError('AAC payload changed')
    cmd(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'audio_adts_sha256':source_audio,'changed_frames':[START,END-1],
            'picture_overlay_y':[0,PROTECTED_Y-1],
            'review_status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--source-sha',required=True);ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--review-only',action='store_true');ap.add_argument('--report')
    a=ap.parse_args()
    result=render(a.source,a.output,a.source_sha,a.genre,a.review_only)
    if a.report: Path(a.report).write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(json.dumps(result,ensure_ascii=False))
