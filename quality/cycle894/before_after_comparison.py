"""cycle894: review-only, fictional Before/After workflow illustration.
Not actual Excel/ChatGPT footage; no measured time-saving claims.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
START, END, FRAMES = 588, 691, 691
X, Y, W, H = 66, 196, 948, 1210
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES = ('ai_productivity','beauty','romance_psychology','money_saving',
          'sales_business','career','health_lifestyle','trivia_science',
          'travel_food','product_lifestyle')
POLICY = {'review_only': True, 'publication_approved': False,
          'external_upload': False, 'automatic_posting': False,
          'source_rights_reviewed': False, 'synthetic_ui': True,
          'time_saving_measured': False}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def validate_copy(m):
    if not isinstance(m, dict):
        raise ValueError('Manifest must be an object')
    for k, v in POLICY.items():
        if m.get(k) is not v:
            raise ValueError(f'Fail-closed policy: {k}')
    if m.get('genre') not in GENRES:
        raise ValueError('Unknown genre')
    keys = ('before_title','after_title','before_steps','after_steps','cta')
    for key in keys:
        v = m.get(key)
        if key.endswith('_steps'):
            if not isinstance(v, list) or len(v) != 3:
                raise ValueError(f'{key} must contain exactly 3 steps')
            strings = v
        else:
            strings = [v]
        for s in strings:
            if not isinstance(s, str) or not (1 <= len(s) <= 18):
                raise ValueError(f'Invalid length: {key}')
            if re.search(r'https?://|@|\d{8,}|[<>\n\r]|(?:\d+\s*(?:分|時間|%|倍)\s*(?:短縮|削減|アップ|改善))', s, re.I):
                raise ValueError(f'Unsafe or unverified claim: {key}')
    if m['before_steps'] == m['after_steps']:
        raise ValueError('No meaningful Before/After difference')
    return True

def stage(frame):
    if type(frame) is not int or not 0 <= frame < END-START:
        raise ValueError('Invalid local frame')
    return 0 if frame < 35 else 1 if frame < 70 else 2

def ease(t):
    t = max(0.0, min(1.0, t))
    return t*t*(3-2*t)

def ft(size):
    if not Path(FONT).is_file():
        raise RuntimeError('Noto Japanese font required')
    return ImageFont.truetype(FONT, size)

def draw_panel(d, rect, title, steps, tint, focused, frame):
    x0,y0,x1,y1=rect
    border = tint if focused else (70,95,112,255)
    fill=(8,36,58,255) if focused else (12,27,44,255)
    d.rounded_rectangle((x0+8,y0+12,x1+8,y1+12),radius=27,fill=(0,7,16,200))
    d.rounded_rectangle(rect,radius=27,fill=fill,outline=border,width=5 if focused else 3)
    d.rounded_rectangle((x0+22,y0+25,x1-22,y0+114),radius=15,fill=(22,66,91,255) if focused else (29,44,61,255))
    d.text((x0+40,y0+40),title,font=ft(42),fill=(245,250,255))
    for i,line in enumerate(steps):
        y=y0+151+i*143
        active = focused and ((frame//10)%3 == i)
        if active:
            d.rounded_rectangle((x0+23,y-8,x1-23,y+99),radius=15,fill=(18,89,108,255))
        d.rounded_rectangle((x0+39,y+10,x0+97,y+68),radius=15,fill=tint if focused else (76,96,110,255))
        d.text((x0+58,y+13),str(i+1),font=ft(29),fill=(3,19,35))
        d.text((x0+115,y+16),line,font=ft(31),fill=(255,255,255) if focused else (184,196,204))
    d.rounded_rectangle((x0+25,y1-106,x1-25,y1-39),radius=16,fill=tint if focused else (46,66,83,255))
    note='手作業の工程' if title.startswith('BEFORE') else '確認は省略しない'
    d.text((x0+42,y1-92),note,font=ft(28),fill=(3,22,37) if focused else (224,234,238))

def draw_patch(frame, m):
    validate_copy(m)
    s=stage(frame)
    im=Image.new('RGBA',(W,H),(4,16,31,255))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((8,5,W-8,113),radius=24,fill=(10,53,82,255))
    d.text((40,24),'BEFORE / AFTER',font=ft(52),fill=(255,255,255))
    d.text((40,121),'作業の流れを比較する',font=ft(36),fill=(198,234,241))
    d.rounded_rectangle((23,215,W-23,978),radius=28,fill=(5,29,47,255),outline=(55,113,139,255),width=3)
    bw=438; gap=20
    left=(34,232,34+bw,944)
    right=(34+bw+gap,232,34+2*bw+gap,944)
    draw_panel(d,left,'BEFORE',m['before_steps'],(255,176,100,255),s in (0,2),frame)
    draw_panel(d,right,'AFTER',m['after_steps'],(88,229,221,255),s in (1,2),frame)
    d.rounded_rectangle((26,1002,W-26,1096),radius=22,fill=(13,85,113,255))
    label=m['cta'] if s==2 else ('まず手作業を見直す' if s==0 else '次に確認付きの手順へ')
    d.text((53,1020),label,font=ft(35),fill=(255,255,255))
    d.text((35,1124),'架空の作業例 ／ 時短効果は未計測',font=ft(26),fill=(169,198,209))
    for i in range(3):
        x=38+i*302
        d.rounded_rectangle((x,1175,x+277,1185),radius=5,fill=(69,223,222,255) if i<=s else (54,84,104,255))
    return im

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of','json',str(p)],text=True))

def render(source, output, manifest, work, report):
    source,output,work,report=map(Path,(source,output,work,report))
    m=json.loads(Path(manifest).read_text(encoding='utf-8'))
    validate_copy(m)
    if m.get('source_sha256') != sha256(source):
        raise ValueError('Source SHA mismatch')
    info=probe(source)
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    a=next(x for x in info['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',691):
        raise ValueError('Unsupported video')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):
        raise ValueError('Unsupported audio')
    if not (Y>=160 and Y+H<1480 and X>=60 and X+W<=1020):
        raise ValueError('Caption safe-area overlap')
    work.mkdir(parents=True,exist_ok=True); output.parent.mkdir(parents=True,exist_ok=True)
    for f in range(END-START):
        draw_patch(f,m).save(work/f'{f:03d}.png',compress_level=2)
    filt=(f'[1:v]format=rgba,setpts=PTS+{START}/({FPS}*TB)[ov];'
          f"[0:v][ov]overlay={X}:{Y}:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-framerate','30','-start_number','0','-i',str(work/'%03d.png'),
        '-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v','691',
        '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
        '-c:a','copy','-movflags','+faststart',str(output)],check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=120)
    result={'cycle':894,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'changed_scene_frames':END-START,'full_av_decode':'PASS',
            'original_ui':'synthetic_not_real_excel','japanese_asr':'UNVERIFIED',
            'semantic_caption_match':'UNVERIFIED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','work','report'):
        p.add_argument('--'+n,required=True)
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.manifest,args.work,args.report),ensure_ascii=False))
