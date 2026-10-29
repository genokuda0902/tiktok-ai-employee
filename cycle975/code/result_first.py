#!/usr/bin/env python3
"""Cycle975 source-derived result-first hook. Review only, never posts or uploads."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SAFE_TOP = 1310
PREVIEW_CROP = (137, 580, 773, 1130)
GENRE_PALETTES = {
    'ai_work': '#13d5d1', 'finance': '#f0ba52', 'learning': '#5baceb',
    'health': '#65cda4', 'travel': '#ed9f5e', 'food': '#e4a66c',
    'science': '#9e94ec', 'history': '#b8a27d', 'business': '#51c4de',
    'lifestyle': '#dd98c4',
}
FONT_PATHS = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
def font(sz):
    for p in FONT_PATHS:
        if Path(p).exists(): return ImageFont.truetype(p,sz)
    raise RuntimeError('No usable font installed')
def rgb(s):
    return tuple(int(s[i:i+2],16) for i in (1,3,5))
def check_genre(genre,synthetic=False):
    if genre not in GENRE_PALETTES: raise ValueError('Unknown genre: fail closed')
    if genre!='ai_work' and not synthetic:
        raise ValueError('Unreviewed coordinates for genre: fail closed')
def run(cmd,capture=False):
    return subprocess.run(cmd,check=True,stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                          stderr=subprocess.PIPE).stdout
def source_frame(video,sec,dest):
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(sec),'-i',str(video),
         '-frames:v','1',str(dest)])
    return dest
def build_overlay(preview_path,output_path,genre='ai_work',synthetic=False):
    check_genre(genre,synthetic)
    preview=Image.open(preview_path).convert('RGB')
    if preview.size!=(W,H): raise ValueError('Preview must be 1080x1920 source frame')
    card=preview.crop(PREVIEW_CROP).resize((720,620),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    accent=rgb(GENRE_PALETTES[genre])
    glow=Image.new('RGBA',(W,H),(0,0,0,0));gd=ImageDraw.Draw(glow)
    gd.rounded_rectangle((65,384,1015,1230),radius=44,outline=(*accent,130),width=12)
    im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(16)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((74,392,1006,1222),radius=38,fill=(4,20,40,248),
                        outline=(*accent,245),width=4)
    d.rounded_rectangle((110,417,466,479),radius=22,fill=(*accent,245))
    d.text((135,426),'完成形を先に見る',font=font(30),fill=(5,23,35,255))
    d.rounded_rectangle((725,422,963,474),radius=20,fill=(30,51,72,255))
    d.text((745,432),'SOURCE PREVIEW',font=font(20),fill=(219,239,245,255))
    d.text((188,487),'週次報告｜完成サンプル',font=font(31),fill=(243,251,255,255))
    x,y=180,535
    mask=Image.new('L',card.size,0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,card.width-1,card.height-1),
                                           radius=26,fill=255)
    shadow=Image.new('RGBA',(card.width+28,card.height+28),(0,0,0,0))
    ImageDraw.Draw(shadow).rounded_rectangle((14,14,card.width+13,card.height+13),
                                             radius=26,fill=(0,0,0,120))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(11)),(x-14,y-8))
    im.paste(card,(x,y),mask)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((197,1168,878,1205),radius=12,fill=(14,44,56,245))
    d.text((238,1170),'架空サンプル・実績ではありません',font=font(22),
           fill=(235,246,249,255))
    box=im.getbbox()
    if not box or box[3]>=SAFE_TOP:
        raise ValueError(f'Overlay violates caption safety region: {box}')
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    im.save(output_path)
    return output_path
def render(source,output,genre='ai_work',synthetic=False,preview_image=None,crf=19):
    check_genre(genre,synthetic)
    source=Path(source);output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    assets=output.parent/'assets';assets.mkdir(exist_ok=True)
    if preview_image is None:
        if synthetic: raise ValueError('Synthetic test must supply a preview image')
        preview_image=source_frame(source,7.1,assets/'source_scene03.png')
    overlay=build_overlay(preview_image,assets/'source_derived_hook.png',genre,synthetic)
    info=json.loads(run(['ffprobe','-v','error','-count_frames','-select_streams','v:0',
                         '-show_entries','stream=nb_read_frames','-of','json',str(source)],True))
    frames=int(info['streams'][0]['nb_read_frames'])
    expr="if(lt(t,0.42),1080,if(lt(t,0.88),1080*(1-(t-0.42)/0.46),0))"
    filt=f"[0:v][1:v]overlay=x='{expr}':y=0:enable='between(t,0.42,2.60)':format=auto[v]"
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate','30','-i',str(overlay),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
         '-preset','veryfast','-crf',str(crf),'-pix_fmt','yuv420p',
         '-r','30','-frames:v',str(frames),'-c:a','copy',
         '-movflags','+faststart',str(output)])
    return output
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
    p.add_argument('--preview-image');p.add_argument('--report')
    a=p.parse_args()
    out=render(a.source,a.output,a.genre,a.synthetic,a.preview_image)
    record={'cycle':975,'output':str(out),'sha256':sha(out),'genre':a.genre,
            'improvement':'source-derived finished-report preview in first 1.5s',
            'independent_asr':'NOT_RUN','publication_approved':False}
    if a.report:
        Path(a.report).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False))
if __name__=='__main__': main()
