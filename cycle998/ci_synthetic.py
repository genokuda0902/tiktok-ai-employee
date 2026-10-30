"""Synthetic-only CI: no private media; no publication rights implied."""
import json,subprocess,tempfile
from pathlib import Path
import cv2
from ghost_free_guard import render,luma,probe

def run(args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def frame(p,i):
    c=cv2.VideoCapture(str(p));c.set(cv2.CAP_PROP_POS_FRAMES,i);ok,f=c.read();c.release()
    if not ok:raise RuntimeError('synthetic frame decode failed')
    return f

with tempfile.TemporaryDirectory(prefix='cycle998-') as tmp:
    t=Path(tmp);srt=t/'sub.srt';src=t/'src.mp4';out=t/'out.mp4'
    srt.write_text('1\n00:00:00,000 --> 00:00:02,000\n合成字幕・公開禁止\n',encoding='utf8')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','lavfi','-i','color=c=0x40556a:s=1080x1920:r=30:d=1',
         '-f','lavfi','-i','color=c=0xbfc3c8:s=1080x1920:r=30:d=1',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
         '-i',str(srt),'-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]',
         '-map','[v]','-map','2:a:0','-map','3:s:0','-c:v','libx264',
         '-preset','ultrafast','-crf','30','-pix_fmt','yuv420p','-c:a','aac',
         '-c:s','mov_text','-metadata:s:a:0','language=jpn',
         '-metadata:s:s:0','language=jpn',str(src)])
    r=render(src,out,t/'report.json','ai_work',[30],review_only=True)
    a=abs(luma(frame(src,30))-luma(frame(src,29)))
    b=abs(luma(frame(out,30))-luma(frame(out,29)))
    assert b<a*.5,(a,b)
    assert int(next(s for s in probe(out)['streams'] if s['codec_type']=='video')['nb_frames'])==60
    for kind in ['v:0','a:0']:
        run(['ffmpeg','-v','error','-xerror','-i',str(out),'-map','0:'+kind,'-f','null','-'])
    print(json.dumps({'synthetic_only':True,'jump_before':round(a,2),
                      'jump_after':round(b,2),'frames':60,'status':'PASS',
                      'publication_approved':False}))
