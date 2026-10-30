"""Local review-only QA; never interprets codec validation as publication approval."""
import json
from pathlib import Path
import subprocess
import cv2
import numpy as np
from flash_guard import luma,probe,sha256


def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout


def stream_hash(path,stream):
    return run(['ffmpeg','-v','error','-i',str(path),'-map','0:'+stream,
                '-c','copy','-f','hash','-hash','SHA256','-']).strip()


def read_frame(cap,index):
    cap.set(cv2.CAP_PROP_POS_FRAMES,index)
    ok,frame=cap.read()
    if not ok:raise ValueError('Failed frame '+str(index))
    return frame


def verify(before,after,report):
    before,after,report=map(Path,(before,after,report))
    p0,p1=probe(before),probe(after)
    streams0=[s['codec_name'] for s in p0['streams']]
    streams1=[s['codec_name'] for s in p1['streams']]
    assert streams0==streams1==['h264','aac','mov_text']
    assert p1['streams'][0]['width']==1080 and p1['streams'][0]['height']==1920
    assert p1['streams'][0]['r_frame_rate']=='30/1'
    assert p1['streams'][0]['nb_frames']=='691'
    assert p1['streams'][1]['sample_rate']=='48000'
    for k in ('a:0','s:0'):
        assert stream_hash(before,k)==stream_hash(after,k)
    for k in ('v:0','a:0'):
        run(['ffmpeg','-v','error','-xerror','-i',str(after),'-map','0:'+k,'-f','null','-'])
    captions=run(['ffmpeg','-v','error','-i',str(after),'-map','0:s:0','-f','srt','-'])
    assert len(captions.split('-->'))==9
    assert any('\u3040'<=c<='\u9fff' for c in captions)
    c0=cv2.VideoCapture(str(before));c1=cv2.VideoCapture(str(after))
    deltas=[]
    for cut in [174,348,522]:
        orig0=read_frame(c0,cut-1);orig1=read_frame(c0,cut)
        new0=read_frame(c1,cut-1);new1=read_frame(c1,cut)
        a=abs(luma(orig1)-luma(orig0));b=abs(luma(new1)-luma(new0))
        assert b < a*0.55,(cut,a,b)
        deltas.append({'frame':cut,'before':round(a,3),'after':round(b,3),
                       'reduction_percent':round(100*(1-b/a),2)})
    samples=[0,87,173,174,175,176,178,260,347,348,349,351,434,521,522,523,525,608,690]
    caption_deltas=[]
    for i in samples:
        a=read_frame(c0,i);b=read_frame(c1,i)
        caption_deltas.append(float(np.abs(a[1450:1800].astype(np.int16)-b[1450:1800].astype(np.int16)).mean()))
    c0.release();c1.release()
    assert max(caption_deltas)<4.0,max(caption_deltas)
    data={'status':'PASS','source_sha256':sha256(before),'output_sha256':sha256(after),
          'streams':streams1,'resolution':'1080x1920','fps':30,'frames':691,
          'duration':float(p1['format']['duration']),
          'audio_bitstream_identical':True,'subtitle_bitstream_identical':True,
          'japanese_subtitle_cues':len(captions.split('-->'))-1,
          'full_video_decode':True,'full_audio_decode':True,
          'boundary_jump_deltas':deltas,
          'max_caption_region_mean_abs_diff':round(max(caption_deltas),4),
          'independent_asr':False,'mobile_device_playback':False,
          'publication_approved':False}
    report.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    return data

if __name__=='__main__':
    import sys
    print(json.dumps(verify(*sys.argv[1:4]),ensure_ascii=False))
