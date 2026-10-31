"""cycle1078: genuine LibreOffice Calc screen recording in scene 03.

Input capture is a real local Xvfb/x11grab recording of fictional data.
No private MP4 or capture is committed. Fail closed on input SHA256.
Japanese narration and eight burned-in subtitles are inherited unchanged.
Independent ASR/semantic caption validation is NOT claimed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

FPS=30
W,H=1080,1920
SCENE_START_FRAME,SCENE_END_FRAME=174,256
CAPTION_SAFE_Y=1280
CAPTURE_CROP=(56,156,680,360)
TARGET=(82,345,876,465)
PALETTES={
    'ai_work':'0x19c8bd','finance':'0xf2c36a','education':'0x75a8fc',
    'health':'0x78e0ac','travel':'0xf8a9bb','beauty':'0xd5a6fb',
    'food':'0xffa673','career':'0x70ceef','productivity':'0xb8e271',
    'lifestyle':'0xf6c97e',
}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()

def probe(path):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(x for x in d['streams'] if x['codec_type']=='video')
    a=next((x for x in d['streams'] if x['codec_type']=='audio'),None)
    return {'codec':v['codec_name'],'width':v['width'],'height':v['height'],
            'fps':v['r_frame_rate'],'frames':int(v.get('nb_frames') or 0),
            'duration':float(d['format']['duration']),
            'audio':a['codec_name'] if a else None,
            'sample_rate':int(a['sample_rate']) if a else None}

def filtergraph(genre,label_header,label_detail):
    if genre not in PALETTES:raise ValueError('unknown genre')
    if TARGET[1]+TARGET[3] >= CAPTION_SAFE_Y:raise AssertionError('capture overlaps caption-safe area')
    start=SCENE_START_FRAME/FPS;end=(SCENE_END_FRAME-1)/FPS
    x,y,cw,ch=CAPTURE_CROP
    tx,ty,tw,th=TARGET
    return (
        f'[1:v]fps={FPS},trim=duration={(SCENE_END_FRAME-SCENE_START_FRAME)/FPS:.9f},'
        f'setpts=PTS-STARTPTS+{start}/TB,crop={cw}:{ch}:{x}:{y},'
        f'scale={tw}:{th-3}:flags=lanczos,pad={tw}:{th}:0:1:color=0xeff4f8[app];'
        f"[0:v]drawbox=x=63:y=294:w=964:h=599:color=0x09283b:t=fill:enable='between(t,{start},{end})'[bg];"
        f'[bg][app]overlay=x={tx}:y={ty}:eof_action=pass:shortest=0:'
        f"enable='between(t,{start},{end})'[a];"
        f"[a]drawbox=x=72:y=169:w=800:h=42:color=0x001b2b:t=fill:enable='between(t,{start},{end})'[b];"
        f"[b]drawbox=x=73:y=207:w=180:h=4:color={PALETTES[genre]}:t=fill:enable='between(t,{start},{end})'[c];"
        f"[c]drawbox=x=70:y=1055:w=920:h=101:color=0x001b2b:t=fill:enable='between(t,{start},{end})'[d];"
        f"[d]drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:"
        f"textfile={label_header}:fontsize=23:fontcolor=0xb7d2e1:x=75:y=176:enable='between(t,{start},{end})'[e];"
        f"[e]drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:"
        f"textfile={label_detail}:fontsize=23:fontcolor=0xb7d2e1:x=75:y=1080:enable='between(t,{start},{end})'[v]"
    )

def render(source,capture,out,source_sha,capture_sha,genre='ai_work',smoke=False):
    if genre not in PALETTES:raise ValueError('unknown genre')
    if sha256(source)!=source_sha:raise ValueError('source SHA256 mismatch; fail closed')
    if sha256(capture)!=capture_sha:raise ValueError('capture SHA256 mismatch; fail closed')
    src=probe(source);cap=probe(capture)
    if (src['codec'],src['width'],src['height'],src['fps'],src['audio'],src['sample_rate']) != ('h264',W,H,'30/1','aac',48000):
        raise ValueError('unsupported source video/audio')
    if (cap['width'],cap['height'],cap['fps']) != (1440,900,'30/1'):
        raise ValueError('expected 1440x900/30fps capture')
    if cap['duration'] < (SCENE_END_FRAME-SCENE_START_FRAME)/FPS:
        raise ValueError('capture shorter than scene')
    if src['duration'] < SCENE_END_FRAME/FPS or (not smoke and abs(src['duration']-23.033333)>0.08):
        raise ValueError('unexpected source duration')
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        head=Path(td)/'header.txt';head.write_text('LIVE CALC RECORDING / FICTIONAL DATA',encoding='utf-8')
        detail=Path(td)/'detail.txt';detail.write_text('実アプリ操作録画／架空データ／投稿前に人が確認',encoding='utf-8')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(capture),
             '-filter_complex',filtergraph(genre,head,detail),'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),
             '-c:a','copy','-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
    return probe(out)

def smoke_test():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);source=td/'synthetic.mp4';capture=td/'synthetic_capture.mp4';out=td/'rendered.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=#061b29:s=1080x1920:r=30:d=9',
          '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=9',
          '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(source)],check=True)
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1440x900:rate=30:duration=3',
          '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(capture)],check=True)
        p=render(source,capture,out,sha256(source),sha256(capture),smoke=True)
        subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
        assert p['codec']=='h264' and p['audio']=='aac'
        print('PASS synthetic 9s A/V decode; no private media in CI')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('source','capture','out','source-sha','capture-sha'):
        ap.add_argument('--'+k)
    ap.add_argument('--genre',default='ai_work',choices=list(PALETTES))
    ap.add_argument('--smoke',action='store_true')
    a=ap.parse_args()
    if a.smoke:smoke_test()
    else:print(json.dumps(render(a.source,a.capture,a.out,a.source_sha,a.capture_sha,a.genre),ensure_ascii=False,indent=2))
