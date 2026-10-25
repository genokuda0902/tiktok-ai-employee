"""Local-only review compositor: animated before/after illustration, ten genres.
Reimplementation, not original v33. No uploading, merging, or posting.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

FPS = 30
SCENE_FRAMES = (89, 81, 79, 87, 86, 89, 77, 103)
START_FRAME = sum(SCENE_FRAMES[:-1])
FRAME_COUNT = SCENE_FRAMES[-1]
REGION = (45, 370, 960, 760)
GENRE_PALETTES = {
    'ai_work': ('#4BDCD1', '#F6D76E'),
    'sales_business': ('#49D3FF', '#FFE18A'),
    'beauty': ('#F0A4D6', '#FDE5A7'),
    'romance': ('#FCA9B3', '#FDE5A7'),
    'saving': ('#7DE8B2', '#FFDB7C'),
    'career': ('#99BCFF', '#FCE29D'),
    'wellness': ('#90E0C6', '#FFE7AB'),
    'science': ('#A9ACFF', '#F9D88A'),
    'travel_food': ('#FFB677', '#B4F2DE'),
    'product_comparison_lifestyle': ('#C6ACFF', '#FBEAA1'),
}
REQUIRED = {
    'data_classification': 'fictional',
    'contains_personal_data': False,
    'contains_confidential_media': False,
    'review_only': True,
    'publication_approved': False,
    'external_upload': False,
    'automatic_posting': False,
    'source_rights_reviewed': False,
}
FONT_REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def validate_manifest(manifest: dict, genre: str, source: Path, output: Path):
    if genre not in GENRE_PALETTES or len(GENRE_PALETTES) != 10:
        raise ValueError('Only ten supported genres allowed')
    if not isinstance(manifest, dict) or any(manifest.get(k) != v for k, v in REQUIRED.items()):
        raise ValueError('Unapproved/private/unspecified material: fail closed')
    if not isinstance(manifest.get('source_sha256'), str) or len(manifest['source_sha256']) != 64:
        raise ValueError('Pinned source SHA256 required')
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('Missing source or source/output collision')
    if sha256(source) != manifest['source_sha256']:
        raise ValueError('Source SHA256 mismatch')

def ease(t: float) -> float:
    t = max(0., min(1., t))
    return t*t*(3-2*t)

def font(size: int, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)

@lru_cache(maxsize=3)
def _gradient_background(size):
    w, h = size
    im = Image.new('RGB', size)
    px = im.load()
    for y in range(h):
        for x in range(w):
            halo = math.exp(-(((x-w*.83)/(w*.65))**2+((y-h*.13)/(h*.75))**2)*2)
            px[x,y] = (int(7+11*halo),int(21+19*halo),int(38+22*halo))
    return im

def panel_frame(i: int, genre: str = 'ai_work', size=(960, 760)) -> Image.Image:
    """Fictional process comparison. No unverified time-savings claim."""
    if genre not in GENRE_PALETTES:
        raise ValueError('Unsupported genre')
    w, h = size
    if w < 600 or h < 500:
        raise ValueError('Production panel requires >=600x500')
    teal, gold = GENRE_PALETTES[genre]
    img = _gradient_background(size).copy()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((10,10,w-10,h-10),radius=30,outline=(64,146,162),width=3)
    d.text((38,26),'WORKFLOW  /  BEFORE & AFTER',font=font(25,True),fill=teal)
    d.text((38,73),'同じ仕事、進め方を見直す',font=font(40,True),fill='#FFFFFF')
    d.text((40,128),'作業の流れを比べる 〈一例〉',font=font(25),fill='#B9CBD8')
    margin, gap = 36, 24
    colw=(w-2*margin-gap)//2
    top,bottom=181,610
    d.rounded_rectangle((margin,top,margin+colw,bottom),radius=23,fill='#172A3A',outline='#617180',width=2)
    d.rounded_rectangle((margin+colw+gap,top,w-margin,bottom),radius=23,fill='#123C44',outline=teal,width=3)
    d.rounded_rectangle((margin+15,top+13,margin+colw-15,top+67),radius=14,fill='#2D3D4B')
    d.rounded_rectangle((margin+colw+gap+15,top+13,w-margin-15,top+67),radius=14,fill='#0D5960')
    d.text((margin+32,top+18),'BEFORE  /  手作業',font=font(26,True),fill='#E9EEF3')
    d.text((margin+colw+gap+32,top+18),'AFTER  /  AI活用',font=font(26,True),fill='#E9FFFF')
    left_steps=['データを確認','項目を整理','下書きを作成','内容をチェック']
    right_steps=['目的を伝える','下書きを受け取る','人が確認・修正']
    for k,s in enumerate(left_steps):
        y=top+87+k*81
        d.rounded_rectangle((margin+18,y,margin+colw-18,y+64),radius=11,fill='#273F50')
        d.ellipse((margin+29,y+17,margin+60,y+48),fill='#8195A4')
        d.text((margin+36,y+18),str(k+1),font=font(18,True),fill='#0C1E2C')
        d.text((margin+71,y+15),s,font=font(25,True),fill='#E6EDF3')
    progress=ease((i-6)/28)
    for k,s in enumerate(right_steps):
        y=top+92+k*106
        visible=ease((i-8-k*14)/20)
        if visible<=0:
            continue
        x0=int(margin+colw+gap+19+(1-visible)*40)
        x1=w-margin-18
        d.rounded_rectangle((x0,y,x1,y+76),radius=13,fill='#19616A')
        d.rounded_rectangle((x0,y,x0+7,y+76),radius=3,fill=teal)
        d.text((x0+20,y+19),f'{k+1:02d}',font=font(24,True),fill=gold)
        d.text((x0+69,y+18),s,font=font(24,True),fill='#FFFFFF')
    arrow_x=int(w/2-22)
    d.rounded_rectangle((arrow_x-11,top+193,arrow_x+56,top+250),radius=19,fill='#F1C85D')
    d.text((arrow_x+5,top+193),'→',font=font(36,True),fill='#10293A')
    d.text((42,641),'今日の1つから試す',font=font(32,True),fill='#FFFFFF')
    d.text((42,692),'※手順は例示です。効果は作業内容により異なります。',font=font(20),fill='#AABFCB')
    d.rounded_rectangle((42,727,w-42,735),radius=4,fill='#26424E')
    d.rounded_rectangle((42,727,42+int((w-84)*max(0.04,progress)),735),radius=4,fill=teal)
    return img

def run(cmd, timeout=300):
    return subprocess.run(cmd,check=True,timeout=timeout,capture_output=True,text=True)

def probe(path: Path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))

def verify(path: Path):
    streams=probe(path)['streams']
    v=next((s for s in streams if s['codec_type']=='video'),None)
    a=next((s for s in streams if s['codec_type']=='audio'),None)
    if not v or not a or v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('H264/AAC required')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames'])) != (1080,1920,'30/1',sum(SCENE_FRAMES)):
        raise ValueError('Unexpected resolution, fps or frame count')
    if abs(float(a['duration'])-sum(SCENE_FRAMES)/FPS)>.12:
        raise ValueError('Truncated narration')
    return {'width':v['width'],'height':v['height'],'frames':int(v['nb_frames']),
            'video_duration':float(v['duration']),'audio_duration':float(a['duration']),
            'audio_sample_rate':int(a['sample_rate'])}

def audio_pcm_md5(path: Path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-f','md5',
                      '-acodec','pcm_s16le','-ar','48000','-ac','2','-'],
                     check=True,capture_output=True,text=True)
    return p.stdout.strip()

def generate_panel_clip(path: Path, genre: str):
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
         '-video_size','960x760','-framerate',str(FPS),'-i','pipe:0',
         '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAME_COUNT):
            p.stdin.write(panel_frame(i,genre).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait(timeout=180):
            raise RuntimeError('Panel encoding failed: '+err[-1200:])
    finally:
        if p.poll() is None:
            p.kill()

def render(source: Path, output: Path, manifest: dict, genre: str='ai_work'):
    source,output=Path(source),Path(output)
    validate_manifest(manifest,genre,source,output)
    before=verify(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    panel=output.with_suffix('.panel.tmp.mp4')
    try:
        generate_panel_clip(panel,genre)
        x,y,w,h=REGION
        start=START_FRAME/FPS
        dur=FRAME_COUNT/FPS
        filt=(f'[1:v]format=yuva420p,fade=t=in:st=0:d=0.22:alpha=1,'
              f'fade=t=out:st={dur-0.24:.5f}:d=0.24:alpha=1,'
              f'setpts=PTS+{start:.8f}/TB[card];'
              f'[0:v][card]overlay={x}:{y}:shortest=1:format=auto[v]')
        cmd=['ffmpeg','-v','error','-y','-threads','2','-filter_complex_threads','2',
             '-i',str(source),'-i',str(panel),'-filter_complex',filt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
             '-r','30','-c:a','copy','-movflags','+faststart',str(output)]
        run(cmd,timeout=300)
    finally:
        panel.unlink(missing_ok=True)
    after=verify(output)
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],timeout=180)
    a,b=audio_pcm_md5(source),audio_pcm_md5(output)
    if a!=b:
        raise ValueError('Decoded Japanese audio was modified')
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'source':before,'output':after,'audio_pcm_md5':a,'audio_pcm_equal':True,
            'overlay_region':list(REGION),'overlay_frame_range':[START_FRAME,sum(SCENE_FRAMES)-1],
            'ten_genre_engine':len(GENRE_PALETTES),
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
            'semantic_voice_verification':False,'word_level_caption_sync':False,
            'rights_approved':False,'v33_compared':False,'phone_playback_verified':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
