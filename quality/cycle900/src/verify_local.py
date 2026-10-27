"""Technical checks only; does not approve content, rights, pronunciation, or ASR."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=index,codec_name,width,height,r_frame_rate,sample_rate,channels,nb_frames:format=duration,size',
        '-of','json',str(p)]))

def audio_hash(p):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0',
        '-c:a','copy','-f','adts','-'])
    return hashlib.sha256(data).hexdigest()

def verify(src,out):
    from voice_pause_transitions import CUT_FRAMES,EFFECT_BOTTOM
    p=probe(out); v=p['streams'][0]; a=p['streams'][1]
    assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])==('h264',1080,1920,'30/1')
    assert a['codec_name']=='aac' and int(a['sample_rate'])==48000
    assert abs(float(p['format']['duration'])-23.033333)<.04
    assert audio_hash(src)==audio_hash(out)
    for f in (src,out):
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(f),'-map','0:v:0',
            '-map','0:a:0','-f','null','-'],check=True)
    c1,c2=cv2.VideoCapture(str(src)),cv2.VideoCapture(str(out))
    caption_max=0.; changed=[]; unchanged=[]; total=0
    cutset={i for c in CUT_FRAMES for i in range(c-2,c+3)}
    while True:
        ok1,im1=c1.read(); ok2,im2=c2.read()
        if not ok1 or not ok2: break
        x1=im1[1490:1840:4,::4]; x2=im2[1490:1840:4,::4]
        caption_max=max(caption_max,float(np.mean(cv2.absdiff(x1,x2))))
        a1=im1[50:EFFECT_BOTTOM:4,::4];a2=im2[50:EFFECT_BOTTOM:4,::4]
        delta=float(np.mean(cv2.absdiff(a1,a2)))
        if total in cutset: changed.append(delta)
        else: unchanged.append(delta)
        total+=1
    c1.release();c2.release()
    assert total==691,(total,'frame count')
    assert len(changed)==35,(len(changed),'affected frames')
    assert float(np.mean(changed))>float(np.mean(unchanged))+1.0
    assert max(changed)>max(unchanged)+2.0
    assert caption_max<3.0,caption_max
    return {'video':v,'audio':a,'duration':float(p['format']['duration']),
        'audio_adts_sha256':audio_hash(out),'audio_bit_exact':True,
        'frame_count':total,'edited_frame_count':len(changed),
        'edited_region_mean_delta_min':round(min(changed),3),
        'edited_region_mean_delta_max':round(max(changed),3),
        'outside_effect_max_mean_delta':round(max(unchanged),3),
        'edited_region_mean_delta_average':round(float(np.mean(changed)),3),
        'outside_effect_mean_delta_average':round(float(np.mean(unchanged)),3),
        'caption_roi_max_mean_delta':round(caption_max,3),
        'full_av_decode':'PASS','japanese_asr_semantic_match':'NOT_TESTED',
        'mobile_playback':'NOT_TESTED','publication_approved':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);ap.add_argument('report',type=Path)
    a=ap.parse_args();r=verify(a.source,a.output);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
