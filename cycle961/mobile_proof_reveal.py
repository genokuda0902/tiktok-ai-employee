"""cycle961: mobile-legible, source-backed two-beat proof reveal (REVIEW ONLY).

Independent reimplementation, not the v33 original generator.
Do not publish, post, upload private source media, or override manual approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EXPECTED_SOURCE_SHA = '5b56fc8b72b984f5fc81397738d06900adaedbe35620de99b3b15f2a25bfcc07'
WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
CAPTION_TOP = 1490
X, Y, W, H = 155, 520, 770, 630
SOURCE_PROOF_SECONDS = 13.8
GENRE_POLICIES = {
    'ai_work': 'fictional Calc recording; independently checked sums',
    'finance': 'verified primary calculation; no financial advice',
    'history': 'primary dated archival citation',
    'science': 'reproducible source-backed experiment',
    'health': 'reviewed non-personal health sources',
    'travel': 'verified location and date',
    'food': 'original filmed cooking evidence',
    'career': 'original workflow demo',
    'education': 'checked worked example',
    'lifestyle': 'original before-after provenance',
}
REVIEWED_GENRES = frozenset({'ai_work'})

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def validate(source, genre, review_only=True, publication_approved=False):
    if genre not in GENRE_POLICIES:
        raise ValueError('unknown genre')
    if genre not in REVIEWED_GENRES:
        raise ValueError('genre geometry, source evidence and rights not reviewed')
    if review_only is not True or publication_approved is not False:
        raise ValueError('manual employee approval mandatory: publication not approved')
    if not Path(source).is_file() or sha256(source) != EXPECTED_SOURCE_SHA:
        raise ValueError('missing or SHA-mismatched private source')
    if X < 0 or Y < 0 or X + W > WIDTH or Y + H >= CAPTION_TOP:
        raise ValueError('proof card overlaps video or protected Japanese caption area')

def jpfont(size, bold=True):
    name = 'NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'
    path = Path('/usr/share/fonts/opentype/noto') / name
    if not path.exists():
        raise FileNotFoundError(f'Japanese font missing: {path}')
    return ImageFont.truetype(str(path), size)

def source_crop(frame):
    if frame.size != (WIDTH, HEIGHT):
        raise ValueError('proof frame must be 1080x1920')
    return frame.crop((80, 460, 1000, 950)).convert('RGB')

def draw_base():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 2, W-3, H-3), radius=30,
                        fill=(4, 27, 43, 255), outline=(95, 235, 213, 255), width=5)
    return im, d

def make_cards(proof_frame):
    crop = source_crop(proof_frame)
    first, d = draw_base()
    d.text((38, 22), '実演の検算結果', font=jpfont(49), fill=(243, 255, 255))
    d.text((525, 44), '架空データ', font=jpfont(23, False), fill=(161, 212, 220))
    pic = crop.resize((700, 373), Image.Resampling.LANCZOS)
    first.paste(pic, (35, 115))
    d.rounded_rectangle((34, 510, 736, 589), radius=16, fill=(15, 70, 78, 255))
    d.text((55, 521), 'A＝46   /   B＝29', font=jpfont(48), fill=(255, 255, 255))

    second, d2 = draw_base()
    d2.text((40, 21), '合計を照合', font=jpfont(49), fill=(244, 255, 255))
    d2.text((570, 45), '架空データ', font=jpfont(21, False), fill=(161, 212, 220))
    pic2 = crop.resize((680, 362), Image.Resampling.LANCZOS)
    second.paste(pic2, (45, 106))
    d2.rounded_rectangle((36, 484, 733, 598), radius=16, fill=(9, 78, 82, 255))
    d2.text((64, 492), '46', font=jpfont(82), fill=(170, 255, 217))
    d2.text((275, 514), '／', font=jpfont(48), fill=(220, 244, 247))
    d2.text((386, 492), '29', font=jpfont(82), fill=(255, 250, 195))
    d2.text((581, 536), '検算OK', font=jpfont(23), fill=(238, 255, 255))
    return first, second

def frame_at(source, seconds, dest):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-ss', str(seconds), '-i', str(source), '-frames:v', '1', str(dest)],
                   check=True, timeout=45)

def render(source, output, genre='ai_work'):
    validate(source, genre)
    source, output = Path(source), Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle961_') as temp:
        tmp = Path(temp)
        frame_at(source, SOURCE_PROOF_SECONDS, tmp/'proof.png')
        with Image.open(tmp/'proof.png') as f:
            first, second = make_cards(f.convert('RGB'))
        first.save(tmp/'card1.png'); second.save(tmp/'card2.png')
        filt = (
            '[1:v]format=rgba,fade=t=in:st=0.35:d=0.12:alpha=1,'
            'fade=t=out:st=1.25:d=0.16:alpha=1[a];'
            '[2:v]format=rgba,fade=t=in:st=1.26:d=0.16:alpha=1,'
            'fade=t=out:st=2.15:d=0.19:alpha=1[b];'
            f"[0:v][a]overlay=x={X}:y={Y}:enable='between(t,0.35,1.41)':format=auto[v1];"
            f"[v1][b]overlay=x={X}:y={Y}:enable='between(t,1.26,2.34)':format=auto[v]"
        )
        cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
               '-loop','1','-framerate',str(FPS),'-i',str(tmp/'card1.png'),
               '-loop','1','-framerate',str(FPS),'-i',str(tmp/'card2.png'),
               '-filter_complex',filt,'-map','[v]','-map','0:a:0',
               '-frames:v',str(FRAMES),'-c:v','libx264','-preset','veryfast',
               '-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=240)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'source_proof_seconds':SOURCE_PROOF_SECONDS,
            'proof_values':{'A':[12,16,18,46],'B':[8,9,12,29]},
            'source_crop':[80,460,1000,950], 'card':[X,Y,W,H],
            'caption_protected_y':CAPTION_TOP,
            'active_seconds':[0.35,2.34], 'genre':genre,
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--qa',required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    result=render(a.source,a.output,a.genre)
    Path(a.qa).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
