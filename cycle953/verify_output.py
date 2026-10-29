"""Local private MP4 QA; no audio transcription or publication approval claims."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np

def run(*args):return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout

def ffprobe(path):
    return json.loads(run('ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels','-show_entries','format=duration,size','-of','json',str(path)))

def audio_sha(path):
    return hashlib.sha256(run('ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1')).hexdigest()

def verify(source,output):
    meta=ffprobe(output)
    v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',691)
    assert (a['codec_name'],a['sample_rate'],a['channels'])==('aac','48000',2)
    assert abs(float(meta['format']['duration'])-23.033333)<.01
    run('ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-')
    asrc,aout=audio_sha(source),audio_sha(output)
    assert asrc==aout,'AAC elementary stream changed'
    ca,cb=cv2.VideoCapture(str(source)),cv2.VideoCapture(str(output))
    all_caption=[];all_outside=[];target=[];idx=0
    while True:
        ok,a=ca.read();ok2,b=cb.read()
        if not ok and not ok2:break
        assert ok and ok2
        # 1/8 downsample; entire frame, every one of 691 frames.
        aa=cv2.resize(a,(135,240));bb=cv2.resize(b,(135,240))
        diff=np.abs(aa.astype(np.int16)-bb.astype(np.int16)).mean(axis=2)
        all_caption.append(float(diff[187:231].mean())) # y>=1496 through caption block
        if 87<=idx<174:target.append(float(diff[:187].mean()))
        else:all_outside.append(float(diff.mean()))
        idx+=1
    ca.release();cb.release()
    assert idx==691
    assert len(target)==87
    assert min(target)>2,'cinematic insert did not change every target frame'
    assert max(all_caption)<3.0,'caption drift unexpectedly large'
    assert max(all_outside)<3.0,'outside-window frames unexpectedly changed'
    return {'full_av_decode':'PASS','width':1080,'height':1920,'fps':30,'frames':691,
            'duration_seconds':float(meta['format']['duration']),'video_codec':'h264',
            'audio_codec':'aac','audio_sample_rate':48000,'audio_channels':2,
            'aac_adts_sha256':aout,'aac_adts_identical':True,
            'modified_frames':len(target),'target_frame_delta_mean':round(float(np.mean(target)),3),
            'caption_region_max_mean_delta':round(max(all_caption),3),
            'outside_window_max_mean_delta':round(max(all_outside),3),
            'independent_japanese_asr':'NOT_AVAILABLE','subtitle_speech_semantics':'UNVERIFIED',
            'mobile_device_playback':'UNVERIFIED','publication':'NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output');ap.add_argument('--json',required=True)
    a=ap.parse_args();r=verify(Path(a.source),Path(a.output))
    Path(a.json).write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False,indent=2))
