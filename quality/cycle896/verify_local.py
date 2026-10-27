"""Full technical comparison; does not perform Japanese ASR or rights checks."""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2
from proof_magnifier import START,END,TOTAL,probe,sha256

def audio_hash(p):
    out=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'],timeout=120)
    return hashlib.sha256(out).hexdigest()

def verify(src,dst):
    a=cv2.VideoCapture(str(src));b=cv2.VideoCapture(str(dst))
    target=[];other=[];cap=[];n=0
    while True:
        ok1,x=a.read();ok2,y=b.read()
        if not ok1 and not ok2:break
        if not(ok1 and ok2):raise AssertionError('Mismatched frame counts')
        if n>=TOTAL:raise AssertionError('Too many frames')
        d=cv2.absdiff(x,y)
        cap.append(float(d[1490:1840].mean()))
        v=float(d[180:1390,66:1014].mean())
        (target if START<=n<END else other).append(v)
        n+=1
    a.release();b.release()
    assert n==TOTAL,(n,TOTAL)
    assert len(target)==END-START
    assert min(target)>2,min(target)
    assert max(cap)<3,max(cap)
    assert max(other)<3,max(other)
    assert audio_hash(src)==audio_hash(dst)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True,timeout=120)
    info=probe(dst);v=next(x for x in info['streams'] if x['codec_type']=='video');aud=next(x for x in info['streams'] if x['codec_type']=='audio')
    assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',TOTAL)
    assert (aud['codec_name'],int(aud['sample_rate']))==('aac',48000)
    return {'cycle':896,'source_sha256':sha256(src),'output_sha256':sha256(dst),'frames':n,'target_changed_frames':len(target),'min_target_mae':round(min(target),3),'max_caption_region_mae':round(max(cap),3),'max_untargeted_mae':round(max(other),3),'audio_adts_sha256':audio_hash(dst),'audio_bitstream_identical':True,'full_av_decode':'PASS','video':'H264 1080x1920 30fps','audio':'AAC 48kHz stereo','subtitle_visual_region':'PRESERVED (not semantic match)','japanese_asr':'UNVERIFIED','real_device':'UNVERIFIED','publication':'NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('source','output','report'):ap.add_argument('--'+k,required=True)
    a=ap.parse_args();r=verify(Path(a.source),Path(a.output));Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=False,indent=2))
