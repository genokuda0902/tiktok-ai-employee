#!/usr/bin/env python3
"""Technical QA only: not Japanese ASR, rights clearance, or human approval."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np
from calc_gui_scene import START,END,SAFE_Y,metadata,sha

def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def qa(source,output):
    source,output=Path(source),Path(output)
    v1,a1,p1=metadata(source);v2,a2,p2=metadata(output)
    assert v1[0]['codec_name']==v2[0]['codec_name']=='h264'
    assert (v2[0]['width'],v2[0]['height'],v2[0]['r_frame_rate'])==(1080,1920,'30/1')
    assert a1[0]['codec_name']==a2[0]['codec_name']=='aac'
    assert a2[0]['sample_rate']=='48000'
    assert v1[0]['nb_frames']==v2[0]['nb_frames']
    expected_frames=int(v1[0]['nb_frames'])
    assert abs(float(p1['format']['duration'])-float(p2['format']['duration']))<.05
    for p in (source,output):
        run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'])
    with tempfile.TemporaryDirectory() as td:
        hashes=[]
        for i,p in enumerate((source,output)):
            q=Path(td)/f'{i}.aac'
            run(['ffmpeg','-v','error','-y','-i',str(p),'-vn','-c:a','copy','-f','adts',str(q)])
            hashes.append(sha(q))
    assert hashes[0]==hashes[1], 'Audio changed'
    c1=cv2.VideoCapture(str(source));c2=cv2.VideoCapture(str(output))
    max_caption=0.;max_outside=0.;change=[];count=0
    while True:
        ok1,f1=c1.read();ok2,f2=c2.read()
        if not ok1 and not ok2:break
        assert ok1 and ok2
        if count%4==0:
            r1=f1[SAFE_Y::4,::4];r2=f2[SAFE_Y::4,::4]
            max_caption=max(max_caption,float(np.mean(cv2.absdiff(r1,r2))))
        if START<=count<END and count%3==0:
            change.append(float(np.mean(cv2.absdiff(f1[:SAFE_Y:8,::8],f2[:SAFE_Y:8,::8]))))
        if not START<=count<END and count%8==0:
            max_outside=max(max_outside,float(np.mean(cv2.absdiff(f1[::8,::8],f2[::8,::8]))))
        count+=1
    c1.release();c2.release()
    assert count==expected_frames
    assert max_caption<3.0, f'Caption region altered: {max_caption}'
    assert max_outside<3.0, f'Outside scene altered: {max_outside}'
    assert float(np.mean(change))>10, 'No meaningful GUI change'
    return {'input_sha256':sha(source),'output_sha256':sha(output),'frames':count,'caption_max_mae_255':round(max_caption,4),'outside_scene_max_mae_255':round(max_outside,4),'scene_mean_mae_255':round(float(np.mean(change)),4),'audio_adts_sha256':hashes[0],'audio_identical':True,'full_video_audio_decode':'PASS','japanese_transcription':'NOT_VERIFIED','subtitle_semantic_timing':'NOT_VERIFIED','smartphone_playback':'NOT_VERIFIED','review_only':True,'publication_approved':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--report',required=True);a=p.parse_args()
 r=qa(a.source,a.output);Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
