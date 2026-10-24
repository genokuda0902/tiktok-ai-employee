"""cycle821: cinematic photo-first 0–3 s hook, review only.

The optional photo is an externally supplied, rights-reviewed asset and is
intentionally not bundled in the GitHub repository. Synthetic CI uses a
locally drawn placeholder; never label synthetic audio as Japanese narration.
"""
from __future__ import annotations
import argparse
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
FRAMES = 90
W, H = 1080, 1920
GENRES = {
    'sales_business': '#5CD6C5', 'ai_tools': '#56A7F6', 'money': '#E8C76A',
    'beauty': '#ED94B4', 'fitness': '#EF955E', 'career': '#7AC3E8',
    'study': '#A6A0EF', 'life_hacks': '#8BD6A0', 'food': '#E6AE73',
    'travel': '#82B7EC',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SAFE = (90, 120, 990, 1620)
HEADLINE = ('仕事ができる人は', '質問が違う。')


def font(size: int, bold: bool = False):
    path = BOLD if bold else FONT
    if not Path(path).is_file():
        raise RuntimeError('Noto Sans CJK fonts are required')
    return ImageFont.truetype(path, size)


def rgb(hex_color: str):
    return tuple(bytes.fromhex(hex_color.lstrip('#')))


def validate_genre(genre):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    return True


def clamp(x):
    return max(0., min(1., x))


def text_alpha(frame, start, duration=13):
    return round(255 * clamp((frame-start)/duration))


def synthetic_photo():
    """Original non-photographic placeholder for CI only."""
    im = Image.new('RGB', (941, 1672), (12, 30, 50))
    d = ImageDraw.Draw(im)
    for y in range(1672):
        t = y / 1672
        d.line((0, y, 941, y), fill=(int(12+24*t), int(30+10*t), int(50-15*t)))
    d.rounded_rectangle((90, 470, 850, 1060), radius=36, fill=(29, 48, 64), outline=(80, 117, 132), width=7)
    d.rounded_rectangle((115, 505, 825, 970), radius=15, fill=(17, 41, 62))
    d.polygon([(130, 875), (290, 770), (430, 800), (570, 630), (805, 580), (805, 920), (130, 920)], fill=(25, 73, 93))
    return im


def make_frame(frame: int, image: Image.Image, genre='sales_business'):
    if not 0 <= frame < FRAMES:
        raise ValueError('frame out of range')
    validate_genre(genre)
    scale = 1.115 + 0.035 * frame / (FRAMES-1)
    iw = math.ceil(W*scale)
    ih = math.ceil(H*scale)
    bg = image.convert('RGB').resize((iw, ih), Image.Resampling.LANCZOS)
    left = round((iw-W)/2 + 9*math.sin(frame/(FRAMES-1)*math.pi))
    top = round((ih-H)/2 + 10*frame/(FRAMES-1))
    im = bg.crop((left, top, left+W, top+H)).convert('RGBA')
    shade = Image.new('RGBA', (W,H), (0,0,0,0))
    s = ImageDraw.Draw(shade, 'RGBA')
    for y in range(H):
        darkness = 0
        if y < 280:
            darkness = round(115*(1-y/280))
        if y > 900:
            darkness = max(darkness, round(180*clamp((y-900)/700)))
        if darkness:
            s.line((0,y,W,y), fill=(3,12,23,darkness))
    im.alpha_composite(shade)
    overlay = Image.new('RGBA', (W,H), (0,0,0,0))
    d = ImageDraw.Draw(overlay, 'RGBA')
    accent = rgb(GENRES[genre])
    d.rounded_rectangle((90,130,840,208), radius=24, fill=(5,21,32,205))
    d.text((124,144), '営業・仕事術  /  実践ノート' if genre=='sales_business' else '今日の実践ノート', font=font(33,True), fill=(255,255,255,255))
    d.text((868,147), '01/08', font=font(29,True), fill=accent+(255,))
    for idx, (line, start, y) in enumerate(((HEADLINE[0], 0, 1090),(HEADLINE[1], 16, 1210))):
        alpha = text_alpha(frame, start)
        if alpha:
            f = font(75 if idx==0 else 99, True)
            bb=d.textbbox((0,0), line, font=f)
            x=(W-(bb[2]-bb[0]))//2
            if x < SAFE[0] or x+bb[2]-bb[0] > SAFE[2]:
                raise ValueError('headline escapes horizontal safe area')
            d.text((x+4,y+5), line, font=f, fill=(0,0,0,round(alpha*.85)), stroke_width=6, stroke_fill=(0,0,0,round(alpha*.7)))
            d.text((x,y), line, font=f, fill=(255,255,255,alpha), stroke_width=2, stroke_fill=(12,26,39,alpha))
    a=text_alpha(frame,40,12)
    if a:
        d.rounded_rectangle((170,1430,910,1515), radius=30, fill=(4,24,36,round(210*a/255)))
        d.text((231,1447), '目的  →  原因  →  行動', font=font(43,True), fill=accent+(a,))
    d.rounded_rectangle((90,1658,650,1738), radius=16, fill=(3,18,29,220))
    d.text((114,1675), '社内レビュー用｜投稿禁止', font=font(28,True), fill=(255,255,255,240))
    d.rounded_rectangle((90,1785,990,1795), radius=4, fill=(255,255,255,100))
    d.rounded_rectangle((90,1785,90+int(900*frame/(FRAMES-1)),1795), radius=4, fill=accent+(255,))
    im.alpha_composite(overlay)
    return im.convert('RGB')


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)], text=True))


def render(source, output, photo=None, genre='sales_business', synthetic=False):
    validate_genre(genre)
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if photo and not Path(photo).is_file():
        raise FileNotFoundError(photo)
    meta=probe(source)
    video=next(s for s in meta['streams'] if s['codec_type']=='video')
    audio=[s for s in meta['streams'] if s['codec_type']=='audio']
    if (video['width'],video['height'],video['avg_frame_rate']) != (W,H,'30/1') or not audio:
        raise ValueError('requires 1080x1920 30fps video with audio')
    if float(meta['format']['duration']) < 3:
        raise ValueError('source must last at least 3 seconds')
    if not synthetic and not photo:
        raise ValueError('review render requires an explicit photo')
    img=Image.open(photo).convert('RGB') if photo else synthetic_photo()
    output.parent.mkdir(parents=True,exist_ok=True)
    frames=output.parent/'frames821'; frames.mkdir(exist_ok=True)
    for n in range(FRAMES):
        make_frame(n,img,genre).save(frames/f'{n:03}.jpg',quality=90,subsampling=0)
    filt=("[1:v]setpts=PTS-STARTPTS[hook];"
          "[0:v][hook]overlay=0:0:eof_action=pass:enable='lt(t,3)',format=yuv420p[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
       '-i',str(source),'-framerate',str(FPS),'-start_number','0','-i',str(frames/'%03d.jpg'),
       '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
       '-preset','veryfast','-crf','21','-threads','2','-pix_fmt','yuv420p',
       '-c:a','copy','-movflags','+faststart',str(output)],check=True)
    out=probe(output)
    ov=next(s for s in out['streams'] if s['codec_type']=='video')
    result={'cycle':821,'genre':genre,'genre_count':len(GENRES),'width':ov['width'],
      'height':ov['height'],'fps':ov['avg_frame_rate'],
      'duration_s':float(out['format']['duration']),'hook_frames':FRAMES,
      'photo_asset':'synthetic' if synthetic else 'generated_original_review_only',
      'japanese_narration_semantics_verified':False,'caption_audio_semantics_verified':False,
      'phone_verified':False,'publication_approved':False,'auto_post':False,
      'source_rights_review_pending':True,'synthetic_audio':bool(synthetic)}
    (output.parent/'qa821.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--photo')
    p.add_argument('--genre',choices=sorted(GENRES),default='sales_business')
    p.add_argument('--synthetic',action='store_true')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.photo,args.genre,args.synthetic),ensure_ascii=False))
