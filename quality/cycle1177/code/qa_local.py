#!/usr/bin/env python3
"""Optional local QA: compare acoustic pauses with second caption-line reveals.
Requires opencv-python and numpy. No ASR; never uploads private media.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
import cv2,numpy as np
from speech_pause_cue import probe,get_chapters,find_silences,select_cues

def aac_sha(path):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
                                  '-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])
    return hashlib.sha256(data).hexdigest()

def scan(src,dst,cue_frames):
    a=cv2.VideoCapture(str(src));b=cv2.VideoCapture(str(dst))
    counts=[];samples=[];f=0
    while True:
        ok,af=a.read();ok2,bf=b.read()
        if not ok or not ok2:
            if ok!=ok2:raise RuntimeError('frame count mismatch')
            break
        roi=af[1520:1595,120:685]
        blue,green,red=cv2.split(roi)
        counts.append(int(((green>105)&(green>red*1.18)&(green>blue*.98)&(red<185)).sum()))
        if f in cue_frames:
            aa=af.astype(np.int16);bb=bf.astype(np.int16)
            cue=(slice(1500,1610),slice(25,125))
            caption=(slice(1440,1600),slice(125,690))
            samples.append({'t':round(f/30,3),
              'cue_roi_mad':round(float(np.abs(aa[cue]-bb[cue]).mean()),3),
              'caption_text_mad':round(float(np.abs(aa[caption]-bb[caption]).mean()),3)})
        f+=1
    a.release();b.release()
    return f,counts,samples

def detect_reveals(counts,chapters):
    times=[]
    for start,end in chapters:
        lo=int((start+.28)*30);hi=min(len(counts)-2,int((end-.1)*30))
        window=counts[lo:hi+1]
        threshold=max(750,int(max(window,default=0)*.24))
        reveal=None
        for j in range(len(window)-2):
            if min(window[j:j+3])>=threshold:
                reveal=round((lo+j)/30,3);break
        times.append(reveal)
    return times

def main(src,dst,out):
    chapters=get_chapters(probe(src));cues=select_cues(chapters,find_silences(src))
    frames,counts,samples=scan(src,dst,{int((c+.18)*30) for c in cues})
    reveals=detect_reveals(counts,chapters)
    if frames!=675 or len(cues)!=len(chapters) or any(t is None for t in reveals):
        raise RuntimeError('invalid frame count or cue coverage')
    offsets=[round(t-(c-.025),3) for t,c in zip(reveals,cues)]
    assert aac_sha(src)==aac_sha(dst),'AAC bitstream modified'
    assert all(abs(t)<.5 for t in offsets),'caption reveal too far from audio pause'
    assert all(s['cue_roi_mad']>2 and s['caption_text_mad']<2 for s in samples)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True)
    result={'frames':frames,'pause_cues_s':cues,'caption_reveals_s':reveals,
            'caption_minus_pause_end_s':offsets,'sampled_roi_differences':samples,
            'aac_bitstream_identical':True,'full_decode':'PASS',
            'independent_japanese_asr':'NOT VERIFIED','publication':'NOT APPROVED'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
