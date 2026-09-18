#!/usr/bin/env python3
"""Config-driven portrait-native TikTok renderer; no scraping, auto-posting, or private assets."""
import argparse,json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
W,H=720,1280
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def cmd(x):subprocess.run(x,check=True,stdout=subprocess.DEVNULL)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def font(n):return ImageFont.truetype(FONT,n)
def image_card(s,base,out):
    source=(base/s['asset']).resolve();im=Image.open(source).convert('RGB');iw,ih=im.size
    if iw/ih>.72 or iw/ih<.48:raise ValueError('Non-portrait asset rejected: '+str(source))
    if iw<540 or ih<960:raise ValueError('Insufficient portrait resolution: '+str(source))
    im=ImageOps.contain(im,(W,H),Image.Resampling.LANCZOS)
    if im.size!=(W,H):raise ValueError('Exact 9:16 asset required; no padding or crop: '+str(source))
    d=ImageDraw.Draw(im,'RGBA');title=s.get('title','')
    if title:
        if len(title)>22:raise ValueError('Headline too long')
        d.rounded_rectangle((25,155,690,270),radius=22,fill=(4,15,26,215))
        d.text((46,180),title,font=font(39),fill='white')
    im.save(out,quality=94)
def render(config):
    cpath=Path(config).resolve();base=cpath.parent;c=json.loads(cpath.read_text(encoding='utf8'))
    if c.get('asset_approval')!='approved':raise ValueError('asset_approval must be approved after human rights/privacy review')
    scenes=c['scenes'];assert 2<=len(scenes)<=12
    dest=(base/c.get('output','render.mp4')).resolve();dest.parent.mkdir(parents=True,exist_ok=True)
    tmp=dest.parent/(dest.stem+'_segments');tmp.mkdir(exist_ok=True)
    seg=[];dur=0
    for i,s in enumerate(scenes):
        sec=float(s['seconds']);assert 1.0<=sec<=15.0
        src=(base/s['asset']).resolve()
        if not src.is_file():raise FileNotFoundError(src)
        clip=tmp/f'{i:02}.mp4';kind=s['type']
        if kind=='image':
            still=tmp/f'{i:02}.jpg';image_card(s,base,still)
            cmd(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(sec),'-i',str(still),'-vf','format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-an',str(clip)])
        elif kind=='video':
            meta=probe(src);v=next(z for z in meta['streams'] if z['codec_type']=='video')
            if not .55<=v['width']/v['height']<=.57:raise ValueError('Video must be native 9:16: '+str(src))
            if float(meta['format']['duration'])+.05<sec:raise ValueError('Clip shorter than requested scene')
            cmd(['ffmpeg','-v','error','-y','-i',str(src),'-t',str(sec),'-vf','scale=720:1280:flags=lanczos,setsar=1,fps=30','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(clip)])
        else:raise ValueError('type must be image or video')
        seg.append(clip);dur+=sec
    manifest=tmp/'concat.txt';manifest.write_text(''.join("file '"+str(p)+"'\n" for p in seg))
    silent=tmp/'silent.mp4';cmd(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(silent)])
    narration=c.get('narration')
    if narration:
        audio=(base/narration).resolve()
        if not audio.is_file():raise FileNotFoundError(audio)
        ad=float(probe(audio)['format']['duration'])
        if abs(ad-dur)>.6:raise ValueError(f'Narration duration {ad:.2f}s differs from scenes {dur:.2f}s; no padding or retiming')
        cmd(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-t',str(dur),'-movflags','+faststart',str(dest)])
    else:
        if c.get('mode')!='visual_test':raise ValueError('Narration required for publish candidate')
        dest.write_bytes(silent.read_bytes())
    p=probe(dest);v=next(z for z in p['streams'] if z['codec_type']=='video')
    assert (v['width'],v['height'])==(W,H)
    if c.get('mode')!='visual_test' and not any(z['codec_type']=='audio' for z in p['streams']):raise AssertionError('Missing audio')
    report={'genre':c['genre'],'output':str(dest),'dimensions':[W,H],'duration':float(p['format']['duration']),'scenes':len(scenes),'audio':bool(narration),'mode':c.get('mode','review'),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'manual_gates':['review every scene at phone size','confirm narration matches each scene','check rights/privacy/claims','approve posting manually']}
    (dest.parent/(dest.stem+'_qa.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);render(ap.parse_args().config)
