"""Review-only deterministic technical checks. No semantic ASR or publication approval."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np

def cmd(*args):return subprocess.check_output(args,stderr=subprocess.STDOUT)
def stream_hash(path):
    # ADTS AAC elementary stream, excludes MP4 container metadata.
    h=hashlib.sha256()
    p=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for b in iter(lambda:p.stdout.read(1<<20),b''):h.update(b)
    if p.wait():raise RuntimeError('audio demux failed '+p.stderr.read().decode())
    return h.hexdigest()
def compare_roi(src,dst,frames=None):
    a=cv2.VideoCapture(str(src));b=cv2.VideoCapture(str(dst));data=[]
    count=min(int(a.get(cv2.CAP_PROP_FRAME_COUNT)),int(b.get(cv2.CAP_PROP_FRAME_COUNT)))
    if count<=0:raise RuntimeError("empty comparison video")
    if frames is None:frames=sorted(set(min(count-1,x) for x in (10,50,75,150,400,640)))
    try:
        for i in frames:
            a.set(cv2.CAP_PROP_POS_FRAMES,i);b.set(cv2.CAP_PROP_POS_FRAMES,i)
            ok1,x=a.read();ok2,y=b.read()
            if not (ok1 and ok2):raise RuntimeError('missing comparison frame')
            # lower subtitle ROI is below protected picture panel
            lower=float(np.abs(x[1400:1750].astype('int16')-y[1400:1750].astype('int16')).mean())
            middle=float(np.abs(x[476:1234,86:994].astype('int16')-y[476:1234,86:994].astype('int16')).mean())
            data.append({'frame':i,'caption_roi_mean_abs_difference':round(lower,3),'picture_roi_mean_abs_difference':round(middle,3)})
    finally:a.release();b.release()
    return data
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',a.output,'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    s=stream_hash(a.source);t=stream_hash(a.output)
    r={'source_aac_adts_sha256':s,'output_aac_adts_sha256':t,'aac_bitstream_identical':s==t,
       'frame_comparisons':compare_roi(a.source,a.output),'full_av_decode_pass':True,
       'caption_meaning_verified':False,'japanese_speech_naturalness_verified':False,
       'public_release_approved':False}
    Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False))
    if not r['aac_bitstream_identical']:raise SystemExit('AAC stream changed')