"""cycle953: cinematic illustrative story beat (private human review only).

Reimplementation. Does NOT recover v33 source or license the asset for public use.
Source MP4, user Library generated illustration and their SHA256 hashes must be
provided locally. No private media is committed to public GitHub.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

GENRES = ('ai_work', 'finance', 'history', 'science', 'health', 'travel', 'food', 'career', 'education', 'lifestyle')
# Genre-independent layout; each new genre requires separate human approval of image and semantics.
GENRE_STEPS = {
    'ai_work': ('毎日の集計', '何度も転記', '定型の報告'),
    'finance': ('支出を集計', '数字を転記', '月次の報告'),
    'history': ('資料を調べる', '年代を整理', '出典を確認'),
    'science': ('観測を整理', '仮説を記録', '結果を検証'),
    'health': ('記録を整理', '変化を確認', '専門家に相談'),
    'travel': ('行程を調べる', '候補を比較', '予約を確認'),
    'food': ('材料を整理', '手順を確認', '分量を調整'),
    'career': ('求人を比較', '経験を整理', '応募を確認'),
    'education': ('課題を整理', '復習を計画', '理解を確認'),
    'lifestyle': ('家事を整理', '予定を確認', '習慣を見直す'),
}
FPS = 30
FRAMES = 691
SCENE_START, SCENE_END = 2.9, 5.8
SUBTITLE_Y = 1490
CANVAS = (1080, 1920)
PHOTO_BOX = (0, 0, 1080, 1490)  # full-bleed upper image, preserves existing Japanese subtitle strip
FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def validate(manifest):
    needed = ('genre', 'source_sha256', 'asset_sha256', 'asset_origin', 'asset_review_only',
              'publication_approved', 'geometry_reviewed', 'source_scene', 'caption')
    if any(k not in manifest for k in needed):
        raise ValueError('missing provenance or approval gate')
    if manifest['genre'] not in GENRES:
        raise ValueError('unsupported genre')
    if manifest['source_scene'] != 2 or manifest['caption'] != 'まず、繰り返している作業を書き出そう。':
        raise ValueError('unreviewed scene or Japanese caption')
    if manifest['genre'] != 'ai_work' or manifest['geometry_reviewed'] is not True:
        raise ValueError('only AI-work geometry and story approved for private review')
    if manifest['asset_origin'] != 'user_library_generated_image':
        raise ValueError('asset provenance unknown')
    if manifest['asset_review_only'] is not True or manifest['publication_approved'] is not False:
        raise ValueError('must remain private and publication-unapproved')
    for key in ('source_sha256', 'asset_sha256'):
        value = manifest[key]
        if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('invalid SHA256')
    return True


def font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError('Noto CJK font unavailable')


def prepare_photo(asset):
    """Pre-crop generated illustration without resizing text or touching captions."""
    im = Image.open(asset).convert('RGB')
    if im.width < 800 or im.height < 1400:
        raise ValueError('asset below approved source dimensions')
    # Portrait composition: preserve both human and robot; exclude unreliable book lettering.
    im = im.crop((0, 235, im.width, min(im.height, 1470)))
    x1, y1, x2, y2 = PHOTO_BOX
    return ImageOps.fit(im, (x2-x1, y2-y1), method=Image.Resampling.LANCZOS, centering=(0.50, 0.48))


def make_scene(photo, t, genre='ai_work'):
    """Generate a frame's upper scene; safe zone y>=1490 is never drawn."""
    x1,y1,x2,y2=PHOTO_BOX
    w,h=x2-x1,y2-y1
    phase=np.clip((t-SCENE_START)/(SCENE_END-SCENE_START),0,1)
    scale=1.0+0.025*phase
    zoom=photo.resize((round(w*scale),round(h*scale)),Image.Resampling.BICUBIC)
    zx=(zoom.width-w)//2; zy=(zoom.height-h)//2
    im=zoom.crop((zx,zy,zx+w,zy+h)).convert('RGBA')
    shade=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(shade)
    for y in range(h):
        alpha=int(15+155*np.clip((y/h-0.48)/0.52,0,1)**1.4)
        d.line((0,y,w,y),fill=(1,9,25,alpha))
    im=Image.alpha_composite(im,shade)
    draw=ImageDraw.Draw(im)
    # Draw our own complete header, so no clipped original header remains.
    draw.rectangle((0,0,w,94),fill=(2,15,33,236))
    draw.text((54,26),'AI WORK / 02',font=font(30),fill=(215,240,245,255))
    draw.text((840,26),'02 / 08',font=font(30),fill=(215,240,245,255))
    # Genuine AI-generated illustration, not a real workflow capture.
    draw.rounded_rectangle((28,118,w-28,272),radius=22,fill=(4,18,37,215),outline=(59,216,216,220),width=3)
    draw.text((52,140),'まず、繰り返す作業を選ぶ',font=font(50),fill=(245,252,255,255))
    draw.text((52,213),'イメージ映像 / 架空の作業例',font=font(24),fill=(176,213,222,255))
    steps=GENRE_STEPS[genre]
    for j,label in enumerate(steps):
        appear=SCENE_START+0.30+j*0.55
        p=np.clip((t-appear)/0.24,0,1)
        if p<=0:continue
        ease=p*p*(3-2*p)
        y=1020+j*112+int((1-ease)*20)
        alpha=int(235*ease)
        layer=Image.new('RGBA',(w,h),(0,0,0,0));ld=ImageDraw.Draw(layer)
        ld.rounded_rectangle((28,y,w-28,y+85),radius=18,fill=(3,20,36,int(alpha*.90)),outline=(64,228,210,alpha),width=3)
        ld.rounded_rectangle((49,y+15,110,y+70),radius=12,fill=(38,205,195,alpha))
        ld.text((67,y+19),str(j+1),font=font(33),fill=(3,23,31,alpha))
        ld.text((134,y+14),label,font=font(38),fill=(245,253,253,alpha))
        im=Image.alpha_composite(im,layer)
    return np.array(im.convert('RGB'))[:,:,::-1].copy()


def composite(frame, photo, t, genre='ai_work'):
    if not (SCENE_START <= t < SCENE_END):
        return frame
    if frame.shape != (1920,1080,3):
        raise ValueError('unexpected video dimensions')
    out=frame.copy()
    x1,y1,x2,y2=PHOTO_BOX
    out[y1:y2,x1:x2]=make_scene(photo,t,genre)
    return out


def render(source, asset, output, manifest):
    validate(manifest)
    if sha256(source)!=manifest['source_sha256'] or sha256(asset)!=manifest['asset_sha256']:
        raise ValueError('source or asset SHA mismatch')
    photo=prepare_photo(asset)
    cap=cv2.VideoCapture(str(source))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    if count!=FRAMES or abs(fps-FPS)>.01:
        raise ValueError('unexpected frame count or fps')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    tmp=output.with_suffix('.video.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-c:v','libx264','-preset','veryfast',
         '-crf','18','-pix_fmt','yuv420p',str(tmp)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(count):
            ok,frame=cap.read()
            if not ok:raise RuntimeError('source truncated')
            proc.stdin.write(composite(frame,photo,i/FPS,manifest['genre']).tobytes())
    finally:
        proc.stdin.close();cap.release()
    if proc.wait()!=0:raise RuntimeError('video encoder failed')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(tmp),'-i',str(source),
                    '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy',
                    '-movflags','+faststart',str(output)],check=True)
    tmp.unlink()
    return {'source_sha256':sha256(source),'asset_sha256':sha256(asset),
            'output_sha256':sha256(output),'modified_seconds':[SCENE_START,SCENE_END],
            'frames':count,'genre':manifest['genre'],'asset_license_for_publication':'UNVERIFIED',
            'independent_japanese_asr':'UNVERIFIED','publication':'NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for key in ('source','asset','output','manifest','qa'):ap.add_argument('--'+key,required=True)
    a=ap.parse_args()
    report=render(Path(a.source),Path(a.asset),Path(a.output),json.loads(Path(a.manifest).read_text(encoding='utf-8')))
    Path(a.qa).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
