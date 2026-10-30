#!/usr/bin/env python3
"""Local private full MP4 technical QA; not a publication or ASR approval."""
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
import cv2, numpy as np

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(' '.join(map(str,cmd))+'\n'+p.stderr[-1000:])
    return p.stdout

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def verify(before,after,report):
    before,after,report=map(Path,(before,after,report))
    data=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(after)]))
    s=data['streams'];v=next(x for x in s if x['codec_type']=='video');a=next(x for x in s if x['codec_type']=='audio');sub=next(x for x in s if x['codec_type']=='subtitle')
    assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])==('h264',1080,1920,'30/1')
    assert (a['codec_name'],a['sample_rate'],a['tags']['language'])==('aac','48000','jpn')
    assert (sub['codec_name'],sub['tags']['language'])==('mov_text','jpn')
    assert 23.02<float(data['format']['duration'])<23.05
    run(['ffmpeg','-v','error','-xerror','-i',str(after),'-map','0:v:0','-f','null','-'])
    run(['ffmpeg','-v','error','-xerror','-i',str(after),'-map','0:a:0','-f','null','-'])
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        hashes={}
        for name,path in (('before',before),('after',after)):
            adts=tmp/(name+'.aac');srt=tmp/(name+'.srt')
            run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(adts)])
            run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:s:0',str(srt)])
            hashes[name]={'aac_adts_sha256':digest(adts),'srt_sha256':digest(srt),'srt_cues':srt.read_text(encoding='utf8').count('-->')}
    assert hashes['before']==hashes['after'],hashes
    assert hashes['after']['srt_cues']==8
    c0,c1=cv2.VideoCapture(str(before)),cv2.VideoCapture(str(after))
    assert c0.isOpened() and c1.isOpened()
    count0=int(c0.get(cv2.CAP_PROP_FRAME_COUNT));count1=int(c1.get(cv2.CAP_PROP_FRAME_COUNT))
    assert count0==count1==691
    stats=[]
    for t in (0.7,3.2,6.8,9.4,12.5,13.1,13.4,13.7,14.0,14.2,14.35,14.6,17.8,20.5,22.5):
        frames=[]
        for cap in (c0,c1):
            cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,fr=cap.read();assert ok;frames.append(fr)
        diff=cv2.absdiff(*frames)
        stats.append({'sec':t,'card_mean_abs':round(float(diff[985:1150,85:995].mean()),4),
                      'caption_mean_abs':round(float(diff[1320:1810,50:1030].mean()),4)})
    c0.release();c1.release()
    assert min(x['card_mean_abs'] for x in stats if 13.1<=x['sec']<=14.2)>8
    assert max(x['caption_mean_abs'] for x in stats)<2.5
    assert max(x['card_mean_abs'] for x in stats if x['sec']<12.9 or x['sec']>14.5)<2.5
    result={'output_sha256':digest(after),'source_sha256':digest(before),'full_video_decode':'PASS','full_audio_decode':'PASS',
            'resolution':'1080x1920','fps':30,'frames':691,'duration_seconds':float(data['format']['duration']),
            'video_codec':'h264','audio_codec':'aac','audio_sample_rate':48000,'japanese_metadata':True,
            'subtitle_format':'mov_text','subtitle_cues':8,'audio_subtitle_hashes_identical':True,
            'stream_hashes':hashes,'samples':stats,'max_sample_caption_mean_abs':max(x['caption_mean_abs'] for x in stats),
            'independent_asr':'UNAVAILABLE','semantic_caption_sync':'NOT_VERIFIED','phone_playback':'NOT_TESTED',
            'publication_approved':False}
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('before');p.add_argument('after');p.add_argument('report');x=p.parse_args()
    print(json.dumps(verify(x.before,x.after,x.report),ensure_ascii=False))
