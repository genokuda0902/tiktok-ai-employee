"""Offline synthetic 2-second CI: no user media and no automatic publication."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import cv2
from flash_guard import render, luma, probe


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def stream_hash(path, kind):
    return run(['ffmpeg','-v','error','-i',str(path),'-map','0:'+kind,
                '-c','copy','-f','hash','-hash','SHA256','-'])


def frame(path, n):
    cap=cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES,n)
    ok,f=cap.read()
    cap.release()
    if not ok:raise AssertionError('Failed to decode frame '+str(n))
    return f


def main():
    with tempfile.TemporaryDirectory(prefix='cycle996-synthetic-') as t:
        t=Path(t)
        srt=t/'synthetic.srt'
        srt.write_text('1\n00:00:00,000 --> 00:00:02,000\n合成字幕（公開禁止）\n',encoding='utf-8')
        src=t/'base.mp4'; out=t/'guard.mp4'; report=t/'report.json'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-f','lavfi','-i','color=c=0x142638:s=1080x1920:r=30:d=1',
             '-f','lavfi','-i','color=c=0xf4f2ef:s=1080x1920:r=30:d=1',
             '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
             '-i',str(srt),'-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]',
             '-map','[v]','-map','2:a:0','-map','3:s:0',
             '-c:v','libx264','-preset','ultrafast','-crf','30','-pix_fmt','yuv420p',
             '-c:a','aac','-c:s','mov_text','-metadata:s:a:0','language=jpn',
             '-metadata:s:s:0','language=jpn',str(src)])
        result=render(src,out,report,'ai_work',[30],review_only=True,preset='ultrafast')
        assert result['guarded_cuts']==[30],result
        for kind in ('a:0','s:0'):
            assert stream_hash(src,kind)==stream_hash(out,kind),kind
        before=abs(luma(frame(src,30))-luma(frame(src,29)))
        after=abs(luma(frame(out,30))-luma(frame(out,29)))
        assert after < before*0.55,(before,after)
        assert int(next(s for s in probe(out)['streams'] if s['codec_type']=='video')['nb_frames'])==60
        for kind in ('v:0','a:0'):
            run(['ffmpeg','-v','error','-xerror','-i',str(out),'-map','0:'+kind,'-f','null','-'])
        print(json.dumps({'synthetic':True,'before_jump':before,'after_jump':after,
                          'streams':[s['codec_name'] for s in probe(out)['streams']],
                          'frames':60,'status':'PASS','publication_approved':False},indent=2))

if __name__=='__main__':main()
