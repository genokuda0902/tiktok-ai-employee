"""Cycle824 CI: original spatial laptop/desk slides from existing fictional UI.
Review only. No external photos, real screenshots, private data or auto-post.
The local full renderer is distributed separately in the cycle824 review ZIP.
"""
from __future__ import annotations
import argparse, json, importlib.util, random, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'cycle823'/'cycle823_ci.py'
spec=importlib.util.spec_from_file_location('cycle823_for_824',BASE)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
PALETTES=prior.art.PALETTES
FONT=prior.art.FONT

def upgrade_scene(path,number):
    original=Image.open(path).convert('RGB')
    W,H=original.size
    im=Image.new('RGBA',(W,H),'#F1E9DC')
    d=ImageDraw.Draw(im)
    # Spatial desk background and wood grain: entirely procedural.
    d.rectangle((0,770,W,1335),fill='#A98765')
    rng=random.Random(8240+number)
    for j in range(170):
        x=rng.randint(0,1050);y=rng.randint(775,1325)
        d.line((x,y,x+rng.randint(15,260),y),fill='#967453',width=1)
    d.ellipse((856,850,1065,1059),fill='#F1E8DB',outline='#C5B39D',width=9)
    d.ellipse((888,881,1035,1028),fill='#7C5541')
    d.polygon([(0,912),(262,896),(293,1278),(0,1302)],fill='#EAE4D6')
    for j in range(8):
        d.line((18,967+j*34,243,950+j*34),fill='#BEC9C5',width=3)
    # Original app UI, rendered onto a perspective laptop-like body.
    d.polygon([(102,491),(965,491),(992,1112),(115,1112)],fill='#203845')
    ui=original.crop((95,513,985,1100)).resize((795,528),Image.Resampling.LANCZOS)
    im.paste(ui,(142,532))
    d=ImageDraw.Draw(im)
    d.polygon([(115,1108),(995,1108),(1060,1242),(30,1242)],fill='#B1C0C0')
    d.polygon([(156,1120),(949,1120),(982,1195),(108,1195)],fill='#405A62')
    for row in range(3):
        for col in range(15):
            x=152+col*52+row*6;y=1128+row*20
            d.rounded_rectangle((x,y,x+44,y+13),radius=3,fill='#6D858A')
    d.polygon([(392,1200),(688,1200),(700,1227),(381,1227)],fill='#889E9E')
    # Retain original title and subtitle-safe region.
    im.paste(original.crop((0,0,W,480)),(0,0))
    im.paste(original.crop((0,1325,W,H)),(0,1325))
    im.convert('RGB').save(path,optimize=True)

def prepare(root:Path):
    prior.prepare(root)
    for i in range(1,9):
        upgrade_scene(root/'source'/f'scene_{i:02}.png',i)
    manifest={'cycle':824,'visual_change':'flat UI to original spatial laptop/desk',
      'external_photos':False,'real_screenshots':False,'personal_data':False,
      'review_only':True,'local_renderer_visuals_may_differ_from_CI':True}
    (root/'source'/'asset_provenance824.json').write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')

def render(root:Path):
    result=prior.render(root)
    source=Path(result) if result else root/'output'/'cycle823_UI_DEMO_JAPANESE_HUMAN_REVIEW.mp4'
    dest=root/'output'/'cycle824_CI_DESK_JAPANESE_HUMAN_REVIEW.mp4'
    source.rename(dest)
    return dest

def verify(root:Path):
    mp4=root/'output'/'cycle824_CI_DESK_JAPANESE_HUMAN_REVIEW.mp4'
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(mp4)]))
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    frames=[Image.open(root/'source'/f'scene_{i:02}.png').crop((140,540,937,1050)).resize((80,50)) for i in range(1,9)]
    ass=(root/'output'/'captions817.ass').read_text(encoding='utf8')
    checks={
      'mp4_exists':mp4.stat().st_size>1000000,
      '1080x1920':(v['width'],v['height'])==(1080,1920),
      'h264_30fps':v['codec_name']=='h264' and v['r_frame_rate']=='30/1',
      '775_frames':int(v.get('nb_frames',0))==775,
      'aac_48khz':a['codec_name']=='aac' and a['sample_rate']=='48000',
      '24_caption_states':ass.count('Dialogue: 0,')==24,
      'eight_distinct':all(ImageChops.difference(frames[i],frames[i+1]).getbbox() for i in range(7)),
      'full_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-map','0:v:0','-f','null','-'],capture_output=True).returncode==0,
      'review_only':(root/'source'/'asset_provenance824.json').exists()
    }
    report={'cycle':824,'checks':checks,'passed':sum(bool(x) for x in checks.values()),
      'total':len(checks),'sha256':hashlib.sha256(mp4.read_bytes()).hexdigest(),
      'review_status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
      'note':'CI simplified visual compositor differs from delivered full local renderer'}
    (root/'output'/'qa824_ci.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--step',choices=['prepare','render','verify'],required=True)
    a=p.parse_args();{'prepare':prepare,'render':render,'verify':verify}[a.step](a.root)
