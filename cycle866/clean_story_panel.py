"""cycle866: one composited, collision-free evidence panel across ten genres.

Private review only. Procedural artwork; all example data fictional. This does
not claim to be a real AI service run, Excel export or v33 reproduction.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 30
FRAMES = 691
START = 170  # 5.667 seconds
COUNT = 81
ROI = (0, 330, 1080, 1120)  # captions start below 1490
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES = {
    'ai_work': ('完成見本を決める', '数字の根拠まで見せる'),
    'sales_business': ('比較で伝える', '数字の根拠まで見せる'),
    'beauty': ('変化を見える化', '条件をそろえて比較'),
    'romance': ('伝え方を整理', '事実と解釈を分ける'),
    'saving': ('支出を見える化', '数字の根拠まで見せる'),
    'career': ('実績を見える化', '条件をそろえて比較'),
    'wellness': ('記録を見える化', '無理なく変化を確認'),
    'science': ('データを比較', '根拠を見てから判断'),
    'travel_food': ('候補を比べる', '条件をそろえて比較'),
    'product_comparison_lifestyle': ('商品を比較', '条件をそろえて比較'),
}
DATA = {'4月': (12, 8), '5月': (16, 9), '6月': (18, 12)}
POLICY = dict(review_only=True, publication_approved=False,
              automatic_posting=False, external_upload=False,
              source_rights_reviewed=False, fictional_example=True)
# Positions in the 1080 x 1120 scene-local rectangle, not full frame.
BOXES = {
    'eyebrow': (65, 48, 495, 120),
    'headline': (65, 152, 1015, 270),
    'chart': (65, 320, 1015, 825),
    'summary': (65, 861, 1015, 1056),
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def font(size, bold=True):
    p = FONT if bold else REGULAR
    if not Path(p).exists():
        raise FileNotFoundError('Japanese font required: ' + p)
    return ImageFont.truetype(p, size)

def intersects(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

def layout_ok():
    b = list(BOXES.values())
    return all(0 <= x0 < x1 <= ROI[2] and 0 <= y0 < y1 <= ROI[3]
               for x0, y0, x1, y1 in b) and all(
               not intersects(a, c) for i, a in enumerate(b) for c in b[i+1:])

def text_fits(draw, xy, s, f, box, stroke_width=0):
    x0, y0, x1, y1 = draw.textbbox(xy, s, font=f, stroke_width=stroke_width)
    return box[0] <= x0 and box[1] <= y0 and x1 <= box[2] and y1 <= box[3]

def ease(t):
    t = max(0., min(1., float(t)))
    return t*t*(3.-2.*t)

@lru_cache(maxsize=1)
def background():
    w, h = ROI[2:]
    im = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        z = y / h
        d.line((0, y, w, y), fill=(int(7+7*z), int(19+10*z), int(37+15*z)))
    glow = Image.new('RGBA', (w, h))
    g = ImageDraw.Draw(glow)
    g.ellipse((510, -360, 1540, 660), fill=(17, 126, 230, 120))
    g.ellipse((-420, 510, 410, 1330), fill=(14, 189, 177, 105))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    return Image.alpha_composite(im.convert('RGBA'), glow).convert('RGB')

def draw_frame(i, genre='ai_work'):
    if not 0 <= i < COUNT or genre not in GENRES or not layout_ok():
        raise ValueError('frame, genre or geometry invalid')
    im = background().copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(BOXES['eyebrow'], radius=30, fill=(12, 91, 111),
                        outline=(59, 217, 227), width=2)
    eyebrow = 'WORKFLOW / 架空データ'
    if not text_fits(d, (96, 64), eyebrow, font(30), BOXES['eyebrow']):
        raise ValueError('eyebrow clipping')
    d.text((96, 64), eyebrow, font=font(30), fill='#e3fbff')
    headline, subhead = GENRES[genre]
    if not text_fits(d, (66, 156), headline, font(80), BOXES['headline']):
        raise ValueError('headline clipping')
    d.text((66, 156), headline, font=font(80), fill='#f6fbff')

    # Single chart surface: unlike the inherited panel, no nested legacy card.
    x0, y0, x1, y1 = BOXES['chart']
    d.rounded_rectangle((x0+12, y0+18, x1+12, y1+18), radius=34, fill='#08131f')
    d.rounded_rectangle(BOXES['chart'], radius=34, fill='#102d44',
                        outline='#49d9e7', width=3)
    d.text((104, 350), '月別データの比較', font=font(46), fill='#ffffff')
    d.rounded_rectangle((710, 352, 974, 414), radius=24, fill='#20475b')
    d.ellipse((740, 374, 756, 390), fill='#42d9ec')
    d.text((767, 359), '営業A', font=font(29), fill='#e8fcff')
    d.ellipse((864, 374, 880, 390), fill='#ffbc68')
    d.text((889, 359), 'B', font=font(29), fill='#fff0d9')

    baseline = 731
    for y in (486, 568, 650, 731):
        d.line((145, y, 952, y), fill='#2b536a', width=2)
    for j, (month, values) in enumerate(DATA.items()):
        left = 200 + j * 266
        progress = ease((i - (7+j*7))/30)
        for k, (v, color) in enumerate(zip(values, ('#3cd9ef', '#ffbd6a'))):
            height = int(v/20 * 245 * progress)
            x = left + 68*k
            if height >= 1:
                d.rounded_rectangle((x, baseline-height, x+56, baseline),
                                    radius=10, fill=color)
            if progress > .90:
                d.text((x+4, baseline-height-42), str(v), font=font(31), fill='#ffffff')
        d.text((left+36, 745), month, font=font(35), fill='#edf8ff')

    s0, s1, s2, s3 = BOXES['summary']
    d.rounded_rectangle(BOXES['summary'], radius=28, fill='#09283b',
                        outline='#2a7587', width=3)
    if i < 27:
        title, detail = '見本を先に決める', '何を比較するか明確にする'
    elif i < 55:
        title, detail = '数字を見える化', '4月 → 5月 → 6月を比較'
    else:
        title, detail = '根拠を確認して完成', subhead
    if not text_fits(d, (102, 888), title, font(51), BOXES['summary']):
        raise ValueError('summary title clipping')
    if not text_fits(d, (104, 973), detail, font(34), BOXES['summary']):
        raise ValueError('summary detail clipping')
    d.text((102, 888), title, font=font(51), fill='#ffffff')
    d.text((104, 973), detail, font=font(34), fill='#7fe9e9')
    return im

def media_info(path):
    d = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_streams', '-of', 'json', str(path)], text=True))
    v = next((s for s in d['streams'] if s['codec_type']=='video'), None)
    a = next((s for s in d['streams'] if s['codec_type']=='audio'), None)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],
         int(v.get('nb_frames') or 0),a['codec_name'],a['sample_rate']) != \
         ('h264',1080,1920,'30/1',691,'aac','48000'):
        raise ValueError('unexpected source/output format')

def contract(source, output, manifest, genre):
    source, output = Path(source), Path(output)
    if genre not in GENRES or not source.is_file() or source.resolve() == output.resolve() or output.exists():
        raise ValueError('invalid genre/source/output; never overwrite private media')
    if manifest != {**POLICY, 'source_sha256':sha256(source)}:
        raise ValueError('review-only SHA/rights manifest rejected')
    media_info(source)
    return source, output

def render(source, output, manifest, genre='ai_work'):
    source, output = contract(source, output, manifest, genre)
    with tempfile.TemporaryDirectory(prefix='cycle866_') as temp:
        folder = Path(temp)
        for i in range(COUNT):
            draw_frame(i, genre).save(folder/f'{i:03d}.jpg', quality=91, subsampling=0)
        filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
              f'[0:v][new]overlay=x=0:y={ROI[1]}:enable=\'between(n,{START},{START+COUNT-1})\':'
              f'eof_action=pass:repeatlast=0:format=auto[v]')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
             '-framerate','30','-start_number','0','-i',str(folder/'%03d.jpg'),
             '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30',
             '-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd, check=True, timeout=240)
    media_info(output)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'changed_frames':COUNT,'frame_range':[START,START+COUNT-1],
            'caption_safe_start_y':1490,'genres_supported':len(GENRES),
            'genre_rendered':genre,'layout_ok':layout_ok(),'policy':POLICY}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
    p.add_argument('--genre',default='ai_work');a=p.parse_args()
    report=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')