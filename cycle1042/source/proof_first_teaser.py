#!/usr/bin/env python3
"""Original 3-cut proof-first teaser built only from frames in a SHA-locked private MP4.

Replaces frames 45..86 (1.5..2.9 seconds) in the upper picture (y < 1280).
No third-party assets, no network, no original video/audio uploaded to GitHub.
Fail-closed on genre/source and publication; preserve original AAC bitstream.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SAFE_Y = 1280
START_FRAME, END_FRAME = 45, 87
FRAMES = 691
SOURCE_SHA = 'ac8cc088a379d21903b2bef186c451aa4d2b3acbe937c30cffb0b796d28702b4'
GENRES = ('ai_work','beauty','romance_psychology','money_saving','sales_business',
          'career','health_lifestyle','science_trivia','travel_food','product_comparison_lifestyle')
PALETTES = {
 'ai_work': ('#49E8F4','#FFE267'), 'beauty':('#FFBADB','#FFF0B9'),
 'romance_psychology':('#C8ADFF','#FFD7E4'), 'money_saving':('#7EE9B6','#FFE58A'),
 'sales_business':('#67C9FF','#FFD47B'), 'career':('#95C5FF','#FFF0AA'),
 'health_lifestyle':('#86E9BF','#FFF2C0'), 'science_trivia':('#8DE8F7','#E4C8FF'),
 'travel_food':('#FFCF85','#B3F0E4'), 'product_comparison_lifestyle':('#FFAD8E','#D2E8FF')}
# Private source frames; deliberately use screenshots of the *existing* work demo.
# All content in these frames is fictional training data, not real customer data.
SHOT_SPECS = ((195,'完成見本を決める','01 / 完成形'),
              (328,'AIへ条件を伝える','02 / 指示'),
              (483,'数値を自分で検算','03 / 確認'))
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def rgb(hex_color):
    c=hex_color.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()

def command(cmd, binary=False):
    p=subprocess.run([str(x) for x in cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr.decode(errors='replace')[-2000:]}")
    return p.stdout if binary else p.stdout.decode()

def probe(path):
    return json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def audio_hash(path):
    return hashlib.sha256(command(['ffmpeg','-v','error','-i',path,'-map','0:a:0',
                                  '-c','copy','-f','adts','-'],binary=True)).hexdigest()

def validate(path, expected_sha, genre, review_only):
    if not review_only: raise ValueError('human-review-only gate required')
    if genre not in GENRES: raise ValueError('unknown genre')
    if genre!='ai_work': raise ValueError('no approved private source for this genre')
    if expected_sha!=SOURCE_SHA or sha(path)!=SOURCE_SHA: raise ValueError('private source SHA mismatch')
    p=probe(path)
    v=[x for x in p['streams'] if x['codec_type']=='video']
    a=[x for x in p['streams'] if x['codec_type']=='audio']
    if len(p['streams'])!=2 or len(v)!=1 or len(a)!=1:raise ValueError('requires exactly 1 video + 1 audio')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],
        int(v[0]['nb_frames']),a[0]['codec_name'],int(a[0]['sample_rate'])) != \
       ('h264',W,H,'30/1',FRAMES,'aac',48000):raise ValueError('unexpected format')
    return p

def shot_index(frame):
    if not START_FRAME<=frame<END_FRAME:raise ValueError('frame outside teaser')
    return min(2,(frame-START_FRAME)//14)

def source_still(path, frame):
    # ffmpeg selects by exact presentation frame index, no images are checked into Git.
    raw=command(['ffmpeg','-v','error','-i',path,'-vf',f'select=eq(n\\,{frame})',
                 '-frames:v','1','-f','image2pipe','-vcodec','png','-'],binary=True)
    import io
    return Image.open(io.BytesIO(raw)).convert('RGB')

def font(size): return ImageFont.truetype(FONT,size)

def teaser_frame(frame,still,genre='ai_work'):
    if genre not in GENRES:raise ValueError('unknown genre')
    j=shot_index(frame)
    accent,warm=PALETTES[genre]
    accent_rgb=rgb(accent)
    local=(frame-START_FRAME)%14
    # Original gradient background with restrained kinetic light, no outside art.
    img=Image.new('RGB',(W,SAFE_Y),(5,15,33))
    d=ImageDraw.Draw(img)
    for y in range(0,SAFE_Y,5):
        k=y/SAFE_Y
        d.rectangle((0,y,W,y+5),fill=(5+int(8*k),15+int(12*k),33+int(17*k)))
    halo=Image.new('RGBA',(W,SAFE_Y),(0,0,0,0));h=ImageDraw.Draw(halo)
    h.ellipse((75,200,1030,1130),fill=(*accent_rgb,43))
    img=Image.alpha_composite(img.convert('RGBA'),halo.filter(ImageFilter.GaussianBlur(125)))
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((78,55,405,118),radius=22,fill=(12,53,79,255),outline=accent,width=3)
    d.text((105,68),'AI仕事術 / 3秒予告',font=font(30),fill='white')
    d.text((80,150),SHOT_SPECS[j][1],font=font(64),fill='white',stroke_width=2,stroke_fill=(2,10,25))
    d.text((83,244),SHOT_SPECS[j][2],font=font(35),fill=warm)
    # Original source-derived UI screenshot. All source frames are from the same private MP4.
    # Crop only picture area, excluding original burned subtitles and status footer.
    crop=still.crop((0,0,W,1100))
    zoom=1.0+0.023*(local/13)
    tw,th=round(780*zoom),round(794*zoom)
    screenshot=crop.resize((tw,th),Image.Resampling.LANCZOS)
    sx=(W-tw)//2;sy=330-(th-794)//2
    # Shadow + thin matte frame; no fade ghosting at shot boundaries.
    shadow=Image.new('RGBA',(W,SAFE_Y),(0,0,0,0));sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((sx-19,sy-19,sx+tw+19,sy+th+19),radius=33,fill=(0,0,0,160))
    img=Image.alpha_composite(img,shadow.filter(ImageFilter.GaussianBlur(25)))
    mask=Image.new('L',(tw,th));md=ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,tw-1,th-1),radius=23,fill=255)
    img.paste(screenshot,(sx,sy),mask)
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((sx-3,sy-3,sx+tw+3,sy+th+3),radius=25,outline=accent,width=5)
    # 3-stage visual proof rail, not a claim about narrated-word timing.
    for k in range(3):
        left=205+k*230
        d.rounded_rectangle((left,1165,left+205,1179),radius=7,
                            fill=accent if k==j else (44,77,97,255))
    d.text((290,1190),'見本  →  指示  →  検算',font=font(35),fill='white')
    img.putalpha(255)
    return img

def render(source,dest,report,genre='ai_work',expected_sha=SOURCE_SHA,review_only=False):
    source,dest,report=map(Path,(source,dest,report))
    if len({source.resolve(),dest.resolve(),report.resolve()})!=3 or dest.exists() or report.exists():
        raise ValueError('source/destination/report path collision')
    validate(source,expected_sha,genre,review_only)
    dest.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    stills=[source_still(source,x[0]) for x in SHOT_SPECS]
    with tempfile.TemporaryDirectory(prefix='proof1042_') as tmp:
        temp=Path(tmp)
        for f in range(START_FRAME,END_FRAME):
            teaser_frame(f,stills[shot_index(f)],genre).save(temp/f'{f-START_FRAME:03d}.png')
        # Delay PNG overlay to 1.5 seconds; explicitly preserve video after 2.9s.
        command(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
                 '-i',source,'-framerate','30','-i',temp/'%03d.png',
                 '-filter_complex',f'[1:v]setpts=PTS+{START_FRAME}/({FPS}*TB)[teaser];'
                                   f'[0:v][teaser]overlay=0:0:eof_action=pass:format=auto[v]',
                 '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
                 '-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p',
                 '-frames:v',str(FRAMES),'-c:a','copy','-metadata:s:a:0','language=jpn',
                 '-movflags','+faststart',dest])
    command(['ffmpeg','-v','error','-xerror','-i',dest,'-f','null','-'])
    p=probe(dest);v=next(s for s in p['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'],int(v['nb_frames']))!=(W,H,FRAMES):raise RuntimeError('bad output')
    a0,a1=audio_hash(source),audio_hash(dest)
    if a0!=a1:raise RuntimeError('AAC elementary stream changed')
    out={'source_sha256':SOURCE_SHA,'output_sha256':sha(dest),
         'replaced_frames':[START_FRAME,END_FRAME-1],'source_proof_frames':[s[0] for s in SHOT_SPECS],
         'new_visual_beats':3,'frames':FRAMES,'duration_seconds':float(p['format']['duration']),
         'video':'H264 1080x1920 30fps','audio':'AAC 48kHz jpn',
         'audio_adts_sha256':a1,'full_av_decode':'PASS',
         'independent_japanese_asr':'NOT_VERIFIED','caption_semantic_alignment':'NOT_VERIFIED',
         'rights':'NOT_VERIFIED','publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for n in ('source','dest','report'):ap.add_argument('--'+n,required=True)
    ap.add_argument('--expected-sha',default=SOURCE_SHA)
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--review-only',action='store_true')
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.dest,a.report,a.genre,a.expected_sha,a.review_only),ensure_ascii=False))
