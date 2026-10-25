"""cycle852: 10-genre, caption-safe real LibreOffice Writer cutaway.

Real offline GUI screen recording contains invented instruction text only.
No original v33 assets, no auto-posting; output is review-only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison_lifestyle')
POLICY = {'review_only': True, 'publication_approved': False,
          'automatic_posting': False, 'external_upload': False,
          'source_rights_reviewed': False, 'contains_personal_data': False,
          'capture_is_fictional': True, 'capture_is_real_local_gui': True}
PANEL = (86, 476, 994, 1234)
WINDOW = (507, 588)  # scene 7 only; scene 8 begins at frame 588
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PALETTES = {g: (34 + (i * 9) % 43, 204 - (i * 6) % 37, 203 - (i * 5) % 31)
            for i, g in enumerate(GENRES)}


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_streams', '-show_format', '-of', 'json', str(path)], text=True))


def streams(path):
    a = probe(path)['streams']
    return (next((s for s in a if s['codec_type'] == 'video'), None),
            next((s for s in a if s['codec_type'] == 'audio'), None))


def beat(frame, total):
    if not 0 <= frame < total:
        raise ValueError('invalid frame')
    # 3 distinct shots in one narration scene: overview -> key lines -> saved instruction.
    return min(2, 3 * frame // total)


def validate(source, capture, output, manifest, genre, window):
    source, capture, output = map(Path, (source, capture, output))
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('unknown genre')
    if not source.is_file() or not capture.is_file():
        raise FileNotFoundError('source or capture absent')
    if manifest != {**POLICY, 'source_sha256': sha256(source),
                    'capture_sha256': sha256(capture)}:
        raise ValueError('fail-closed manifest mismatch')
    if output.exists() or output.resolve() in (source.resolve(), capture.resolve()):
        raise ValueError('overwrite forbidden')
    if len(window) != 2 or any(type(x) is not int for x in window):
        raise ValueError('invalid window')
    v, a = streams(source)
    if not v or not a or (v['codec_name'], v['width'], v['height'],
                         v['r_frame_rate'], a['codec_name']) != (
                         'h264', 1080, 1920, '30/1', 'aac'):
        raise ValueError('source must be 1080x1920 30fps H264/AAC')
    cv, _ = streams(capture)
    if not cv or cv['width'] < 1300 or cv['height'] < 800 or cv['r_frame_rate'] != '30/1':
        raise ValueError('capture must be 1440x900-like real GUI 30fps')
    n = int(v['nb_frames'])
    if not 0 <= window[0] < window[1] <= n:
        raise ValueError('window out of bounds')
    if window[1] - window[0] > int(cv['nb_frames']):
        raise ValueError('capture too short')
    return n


def panel_image(capture_bgr, local_frame, total, genre):
    if capture_bgr.shape[0] < 800 or capture_bgr.shape[1] < 1300:
        raise ValueError('invalid GUI frame')
    stage = beat(local_frame, total)
    accent = PALETTES[genre]
    im = Image.new('RGB', (908, 758), (5, 18, 30))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, 902, 752), radius=24, fill=(7, 28, 43),
                        outline=accent, width=4)
    d.rounded_rectangle((22, 24, 886, 111), radius=13, fill=(10, 50, 68))
    f = lambda s: ImageFont.truetype(FONT, s)
    d.text((45, 48), '実際のWriter操作', font=f(42), fill=(255, 255, 255))
    d.text((860, 71), '架空データ', font=f(25), anchor='rm', fill=(172, 228, 236))
    # Genuine Writer document and toolbar. 3 reframings increase mobile legibility.
    crops = ((165, 210, 1220, 765), (250, 260, 1130, 710),
             (250, 290, 1030, 680))
    x0, y0, x1, y1 = crops[stage]
    crop = capture_bgr[y0:y1, x0:x1]
    if crop.size == 0:
        raise ValueError('empty capture crop')
    # Aspect-fit within wide inset (no synthetic or altered spreadsheet text).
    shot = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    shot.thumbnail((856, 475), Image.Resampling.LANCZOS)
    x = (908 - shot.width) // 2
    y = 135 + (475 - shot.height) // 2
    d.rounded_rectangle((22, 127, 886, 610), radius=14, fill=(229, 233, 237))
    im.paste(shot, (x, y))
    d.rectangle((21, 126, 887, 612), outline=accent, width=3)
    labels = ('目的と条件', '使える指示に整理', 'テンプレート化')
    d.rounded_rectangle((32, 634, 876, 729), radius=18, fill=(8, 43, 58),
                        outline=accent, width=2)
    d.text((454, 673), labels[stage], font=f(41), anchor='mm',
           fill=(243, 251, 252))
    for i in range(3):
        d.rounded_rectangle((364 + i * 66, 716, 406 + i * 66, 722),
                            radius=3, fill=accent if i == stage else (48, 87, 102))
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)


def composite(frame, capture, local_frame, total, genre):
    if frame.shape[:2] != (1920, 1080):
        raise ValueError('source frame invalid')
    x0, y0, x1, y1 = PANEL
    out = frame.copy()
    # Remove inherited illustration text protruding above the old picture inset.
    # Keep scene heading (< y=420) and burned-in subtitles (> y=1300) untouched.
    out[430:y0, x0:x1] = (5, 18, 30)
    out[y0:y1, x0:x1] = panel_image(capture, local_frame, total, genre)
    return out


def render(source, capture, output, manifest, genre='ai_work', window=WINDOW):
    source, capture, output = map(Path, (source, capture, output))
    n = validate(source, capture, output, manifest, genre, window)
    inp = cv2.VideoCapture(str(source)); cap = cv2.VideoCapture(str(capture))
    ff = subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
        '-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264',
        '-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy',
        '-movflags','+faststart',str(output)],stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    edited=0
    try:
        for idx in range(n):
            ok, frame=inp.read()
            if not ok: raise RuntimeError('source early EOF')
            if window[0] <= idx < window[1]:
                ok, shot=cap.read()
                if not ok: raise RuntimeError('capture early EOF')
                frame=composite(frame,shot,idx-window[0],window[1]-window[0],genre)
                edited+=1
            ff.stdin.write(frame.tobytes())
        ff.stdin.close()
        err=ff.stderr.read().decode(errors='replace')
        if ff.wait(): raise RuntimeError('ffmpeg failed: '+err[-1200:])
    except Exception:
        ff.kill();ff.wait();output.unlink(missing_ok=True);raise
    finally:
        inp.release();cap.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),
                    '-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    v,a=streams(output)
    if int(v['nb_frames'])!=n or a['codec_name']!='aac':
        raise RuntimeError('output A/V mismatch')
    return {'cycle':852,'frames':n,'edited_frames':edited,
            'edit_window':list(window),'visual_beats_in_scene7':3,
            'genre':genre,'source_sha256':sha256(source),
            'capture_sha256':sha256(capture),'output_sha256':sha256(output),
            'full_av_decode':True,'resolution':'1080x1920','fps':30,
            'audio':'original AAC elementary bitstream copied',
            'caption_semantic_alignment_verified':False,
            'independent_japanese_asr_verified':False,
            'smartphone_playback_verified':False,'rights_cleared':False,
            'publication_approved':False,
            'quality_status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('source','capture','output','report'): ap.add_argument('--'+k,required=True)
    ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--window',default='507,588')
    args=ap.parse_args();s=Path(args.source);c=Path(args.capture)
    w=tuple(map(int,args.window.split(',')))
    result=render(s,c,args.output,{**POLICY,'source_sha256':sha256(s),
                                  'capture_sha256':sha256(c)},args.genre,w)
    Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))