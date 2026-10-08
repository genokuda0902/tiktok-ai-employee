#!/usr/bin/env python3
"""Build a review-only 20-second Pi 5 video from runner-local CC0 image and NEW Aivis WAV.
No media is committed. Do not publish without human voice/model/visual review.
"""
import json, os, subprocess, tempfile, wave, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
PHOTO=Path(os.environ['PI5_PHOTO'])
OUT=Path(os.environ.get('PI5_OUTPUT',str(ROOT/'output/pi5_review_20s.mp4'))).resolve()
OUT.parent.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SOURCE='https://commons.wikimedia.org/wiki/File:Raspberry-Pi_5.jpg'
SHA='62fbc077641e2db042b6c17ecc977ab05a82bc7c864e624eaa044de0cba0b01c'
assert hashlib.sha256(PHOTO.read_bytes()).hexdigest()==SHA,'Source image checksum mismatch'

def cmd(*args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-3500:])
    return p.stdout

# Existing Aivis script creates genuinely new voice and measured per-sentence timing.
voice=ROOT/'output/raspberry_pi5_narration.wav'
timing=ROOT/'output/raspberry_pi5_timing.json'
assert voice.exists() and timing.exists(),'Fresh Aivis narration and timings required'
with wave.open(str(voice)) as w: duration=w.getnframes()/w.getframerate()
assert 14.8<=duration<=20.0, f'Fresh voice duration {duration:.2f}s outside usable range'
# Pad at most five seconds with short closing tail, never reuse old 11.4s audio.
scenes=[('本体はこれ',4,'zoom_in'),('小さなパソコン',4,'pan_left'),('接続イメージ',4,'pan_right'),('使い方の例',4,'zoom_out'),('まずは公式情報を確認',4,'zoom_in')]
with tempfile.TemporaryDirectory() as folder:
    tmp=Path(folder)
    assets={}; sequence=[]
    base=Image.open(PHOTO).convert('RGB')
    font=ImageFont.truetype(FONT,74)
    small=ImageFont.truetype(FONT,43)
    for i,(heading,seconds,motion) in enumerate(scenes):
        image=Image.new('RGB',(1080,1920),(15,20,31)); d=ImageDraw.Draw(image)
        # Photo is the dominant visual; never represent mock UI as genuine screen capture.
        fitted=base.copy(); fitted.thumbnail((1060,1300))
        image.paste(fitted,((1080-fitted.width)//2,290+(1200-fitted.height)//2))
        d=ImageDraw.Draw(image)
        d.text((65,95),heading,font=font,fill='white')
        if i in (2,3): d.text((65,1650),'説明用の再現イメージ／実写操作ではありません',font=small,fill='white')
        d.text((65,1790),'写真: LeGeekLinux / CC0 1.0',font=small,fill='white')
        name=f'photo_{i}'; p=tmp/f'{name}.png';image.save(p)
        assets[name]={'path':p.name,'type':'image','commercial_use':True,'derivatives_allowed':True,'privacy_review':'approved','rights_evidence':SOURCE,'rights_basis':'CC0 1.0; verify source page independently before publishing','source_type':'Wikimedia Commons; LeGeekLinux'}
        sequence.append({'asset_id':name,'seconds':seconds,'motion':motion})
    # Renderer requires audio duration within 0.35 seconds of 20s.
    wav=tmp/'narration.wav'
    cmd('ffmpeg','-v','error','-y','-i',str(voice),'-af','apad','-t','20','-c:a','pcm_s16le',str(wav))
    caps=json.loads(timing.read_text(encoding='utf-8'))
    assert caps and all(0<=x['start']<x['end']<=20.05 for x in caps)
    (tmp/'captions.json').write_text(json.dumps(caps,ensure_ascii=False),encoding='utf-8')
    config={'mode':'review','narration':wav.name,'captions':'captions.json','output':str(OUT),'assets':assets,'scenes':sequence}
    (tmp/'config.json').write_text(json.dumps(config,ensure_ascii=False),encoding='utf-8')
    cmd('python3',str(ROOT/'video_engine/portrait_v2/build.py'),'--config',str(tmp/'config.json'))
    info=json.loads(cmd('ffprobe','-v','error','-show_streams','-show_format','-of','json',str(OUT)))
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'])==(1080,1920)
    assert 19.8<=float(info['format']['duration'])<=20.3
    assert float(a.get('duration',info['format']['duration']))>=19.5
    cmd('ffmpeg','-v','error','-xerror','-i',str(OUT),'-f','null','-')
    result={'status':'TECHNICAL_PASS_HUMAN_REVIEW_REQUIRED','file':str(OUT),'source':SOURCE,'creator':'LeGeekLinux','license':'CC0 1.0','image_sha256':SHA,'voice_duration':duration,'video_duration':info['format']['duration'],'resolution':[v['width'],v['height']],'captions':caps,'model_commercial_rights':'UNVERIFIED; DO NOT PUBLISH','photo_reused':'one independently sourced photo, repeated across five scenes; visual quality limitation','video_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()}
    (OUT.parent/'pi5_v9_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
