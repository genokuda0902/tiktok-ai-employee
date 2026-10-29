"""Review-only original focus-selection animation for an 8-slide Japanese video.

A visual continuity cue: scan three work cards and select the '週次報告' card
that appears in the following scene. Reuses the existing Japanese narration,
subtitles, and artwork; only the upper artwork region of scene 1 is edited.
Ten genre palettes are configured, but only ai_work has approved coordinates.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
GENRE_COLORS = {
    'ai_work': (48, 224, 211), 'business': (113, 184, 251),
    'finance': (238, 190, 111), 'education': (247, 165, 114),
    'career': (158, 190, 254), 'wellness': (131, 211, 158),
    'lifestyle': (229, 156, 209), 'technology': (87, 202, 230),
    'travel': (229, 186, 140), 'trivia': (194, 166, 242),
}
REVIEWED_GENRES = {'ai_work'}
REGION = (0, 500, 900, 975)
CARDS = {'weekly': (70, 552, 347, 864), 'sorting': (347, 548, 591, 841),
         'mail': (602, 553, 862, 864)}
FONT_CANDIDATES = ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                   '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']

def run(argv, capture=False, timeout=300):
    p = subprocess.run(argv, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                       stderr=subprocess.PIPE, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f'{argv[0]} exit={p.returncode}: {p.stderr.decode(errors="replace")[-1000:]}')
    return p.stdout if capture else None

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def media_info(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)], True))

def validate(info, genre, synthetic=False):
    if genre not in GENRE_COLORS:
        raise ValueError('Unknown genre')
    if genre not in REVIEWED_GENRES:
        raise PermissionError('Layout has not been reviewed for this genre')
    streams = info['streams']
    v = next((s for s in streams if s['codec_type']=='video'), None)
    a = next((s for s in streams if s['codec_type']=='audio'), None)
    if not v or not a:
        raise ValueError('Video and Japanese audio both required')
    if (v['codec_name'], v['width'], v['height'], v['r_frame_rate']) != ('h264',1080,1920,'30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if a['codec_name'] != 'aac' or int(a['sample_rate']) != 48000:
        raise ValueError('Expected existing AAC 48kHz audio')
    duration = float(info['format']['duration'])
    if not synthetic and not 22.9 <= duration <= 23.1:
        raise ValueError('Unreviewed duration')
    return duration

def font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise FileNotFoundError('Noto CJK font required; fail closed for Japanese captions')

def alpha_at(frame):
    """Explicit scene-1 sequence: scan sorting -> mail -> select weekly."""
    t = frame / FPS
    if t < .15: return None, 0
    if t < .48: return 'sorting', min(1.0, (t-.15)/.13)
    if t < .81: return 'mail', min(1.0, (t-.48)/.13)
    if t < 2.65: return 'weekly', min(1.0, (t-.81)/.22)
    return None, 0

def overlay_frame(frame, genre='ai_work'):
    if genre not in REVIEWED_GENRES:
        raise PermissionError('Unreviewed genre')
    w, h = REGION[2]-REGION[0], REGION[3]-REGION[1]
    im = Image.new('RGBA',(w,h),(0,0,0,0))
    d = ImageDraw.Draw(im)
    key, strength = alpha_at(frame)
    if key is None or strength <= 0:
        return im
    color = GENRE_COLORS[genre]
    x0,y0,x1,y1 = CARDS[key]
    y0-=REGION[1];y1-=REGION[1]
    for pad,opacity,width in [(13,28,12),(8,68,7),(3,220,4)]:
        d.rounded_rectangle((x0-pad,y0-pad,x1+pad,y1+pad), radius=29,
                            outline=(*color,int(opacity*strength)), width=width)
    if key == 'weekly':
        cx,cy=x1-9,y0+19
        d.ellipse((cx-25,cy-25,cx+25,cy+25), fill=(4,34,49,int(236*strength)),
                  outline=(*color,int(240*strength)), width=3)
        d.line([(cx-11,cy),(cx-2,cy+9),(cx+14,cy-10)],
               fill=(245,255,255,int(245*strength)), width=5, joint='curve')
        badge=(90,377,340,443)
        d.rounded_rectangle(badge,radius=22,fill=(3,24,42,int(238*strength)),
                            outline=(*color,int(200*strength)),width=3)
        label='週次報告を選ぶ'
        ft=font(32)
        bb=d.textbbox((0,0),label,font=ft)
        tx=(badge[0]+badge[2]-(bb[2]-bb[0]))/2
        ty=(badge[1]+badge[3]-(bb[3]-bb[1]))/2-bb[1]
        d.text((tx,ty),label,font=ft,fill=(248,253,255,int(250*strength)))
    return im

def render(source, output, report, genre='ai_work', synthetic=False):
    source,output,report=map(Path,(source,output,report))
    if source.resolve()==output.resolve():
        raise ValueError('In-place modifications forbidden')
    info=media_info(source)
    duration=validate(info,genre,synthetic)
    count=round(duration*FPS)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle969_focus_') as tmp:
        for i in range(80):
            overlay_frame(i,genre).save(f'{tmp}/focus_{i:04d}.png')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate','30','-i',f'{tmp}/focus_%04d.png',
             '-filter_complex','[0:v:0][1:v:0]overlay=0:500:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','18','-pix_fmt','yuv420p','-c:a','copy',
             '-metadata:s:a:0','language=jpn','-movflags','+faststart',
             '-frames:v',str(count),str(output)],timeout=300)
    result={'cycle':969,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'improvement':'Scene01 story continuity: scan 3 task cards then select weekly report',
            'changed_region':list(REGION),'animation_frames':80,'genres_configured':10,
            'genres_rendered':[genre],'human_review_required':True,
            'publication_approved':False,'independent_japanese_asr':'NOT_VERIFIED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output');p.add_argument('report')
    p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.report,args.genre,args.synthetic),ensure_ascii=False))
