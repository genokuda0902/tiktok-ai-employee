#!/usr/bin/env python3
"""Reusable portrait-first TikTok editor. Input video narration is never re-timed."""
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H=720,1280
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def run(args): subprocess.run(args,check=True)
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def intro(photo,out,title,subtitle):
    src=Image.open(photo).convert('RGB');iw,ih=src.size
    if iw/ih>.72 or iw/ih<.50:raise ValueError(f'Hero asset must be portrait (near 9:16), got {iw}x{ih}')
    bg=Image.new('RGB',(W,H),'#081423')
    hero=src.crop((int(iw*.43),int(ih*.02),int(iw*.99),int(ih*.22)))
    hero.thumbnail((680,560),Image.Resampling.LANCZOS)
    bg.paste(hero,((W-hero.width)//2,315))
    d=ImageDraw.Draw(bg,'RGBA')
    d.rounded_rectangle((22,56,698,264),radius=26,fill=(4,18,32,255))
    f=ImageFont.truetype(FONT,48);sm=ImageFont.truetype(FONT,30)
    d.text((50,108),title,font=f,fill='white')
    d.rounded_rectangle((24,820,696,1130),radius=24,fill=(8,32,49,255))
    d.text((48,858),'Excelのデータを',font=ImageFont.truetype(FONT,46),fill='white')
    d.text((48,943),'AIでグラフ化する。',font=ImageFont.truetype(FONT,48),fill='#68f0e4')
    d.text((48,1180),subtitle,font=sm,fill='#c4e9e9')
    bg.save(out,quality=95)
def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);a=p.parse_args()
    cfg=json.loads(Path(a.config).read_text(encoding='utf-8'))
    base=Path(a.config).resolve().parent
    body=(base/cfg['body_video']).resolve();photo=(base/cfg['portrait_image']).resolve()
    dest=(base/cfg.get('output','release.mp4')).resolve();dest.parent.mkdir(parents=True,exist_ok=True)
    if not body.is_file() or not photo.is_file():raise FileNotFoundError('Required approved input video/portrait image missing')
    meta=probe(body);video=next(s for s in meta['streams'] if s['codec_type']=='video')
    if video['width']/video['height']>.72:raise ValueError('Body video is not portrait; no landscape-to-portrait zoom allowed')
    if not any(s['codec_type']=='audio' for s in meta['streams']):raise ValueError('Body narration missing; refusing silent publish candidate')
    card=dest.parent/'opening.jpg';intro(photo,card,cfg['title'],cfg['subtitle'])
    intro_sec=float(cfg.get('intro_seconds',2.0))
    if not 1<=intro_sec<=4:raise ValueError('intro_seconds must be 1..4')
    fc='[0:v]scale=720:1280:force_original_aspect_ratio=decrease:flags=lanczos,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=0x071321,setsar=1,fps=30,trim=duration=%s,setpts=PTS-STARTPTS[iv];[1:v]scale=720:1280:force_original_aspect_ratio=decrease:flags=lanczos,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=0x071321,setsar=1,fps=30,setpts=PTS-STARTPTS[bv];[iv][bv]concat=n=2:v=1:a=0[v];[1:a]adelay=%s|%s,apad[a]'%(intro_sec,int(intro_sec*1000),int(intro_sec*1000))
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-t',str(intro_sec),'-i',str(card),'-i',str(body),'-filter_complex',fc,'-map','[v]','-map','[a]','-shortest','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(dest)])
    result=probe(dest);v=next(s for s in result['streams'] if s['codec_type']=='video')
    assert (v['width'],v['height'])==(720,1280)
    print(json.dumps({'output':str(dest),'duration':result['format']['duration'],'dimensions':'720x1280','audio':'body narration delayed to align with unchanged body'},ensure_ascii=False))
if __name__=='__main__':main()
