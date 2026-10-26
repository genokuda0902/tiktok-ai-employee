"""Independent technical A/V, protected subtitle region, and AAC equality checks."""
from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path
import cv2,numpy as np
from prompt_legibility import stream_info,sha256,WINDOW,SCENE_COVER

def aac_sha(path):
    p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],capture_output=True,check=True)
    return hashlib.sha256(p.stdout).hexdigest()

def run(source,output,dest):
    va,aa=stream_info(source);vb,ab=stream_info(output)
    checks={'resolution':(vb['width'],vb['height'])==(1080,1920),
            'video_codec':vb['codec_name']=='h264',
            'audio_codec':ab['codec_name']=='aac',
            'fps':vb['r_frame_rate']=='30/1',
            'frame_count':int(vb['nb_frames'])==int(va['nb_frames'])==691,
            'aac_elementary_stream_equal':aac_sha(source)==aac_sha(output)}
    c1=cv2.VideoCapture(str(source));c2=cv2.VideoCapture(str(output))
    protected=[];changed=[]
    x0,y0,x1,y1=SCENE_COVER
    for i in [260,290,320]:
        c1.set(cv2.CAP_PROP_POS_FRAMES,i);c2.set(cv2.CAP_PROP_POS_FRAMES,i)
        ok1,a=c1.read();ok2,b=c2.read()
        if not(ok1 and ok2):raise RuntimeError('frame read failed')
        mask=np.ones((1920,1080),dtype=bool);mask[y0:y1,x0:x1]=False
        protected.append(float(np.abs(a.astype('float32')-b.astype('float32'))[mask].mean()))
        changed.append(float(np.abs(a[y0:y1,x0:x1].astype('float32')-b[y0:y1,x0:x1].astype('float32')).mean()))
    c1.release();c2.release()
    checks['protected_region_mean_diff_below_3']=max(protected)<3
    checks['scene04_actually_changed']=min(changed)>12
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    checks['full_av_decode']=True
    report={'checks':checks,'all_technical_checks_pass':all(checks.values()),
            'protected_region_mean_pixel_diff':protected,'scene04_mean_pixel_diff':changed,
            'source_sha256':sha256(source),'output_sha256':sha256(output),
            'aac_sha256':aac_sha(output),'independent_japanese_transcription':False,
            'semantic_caption_alignment_verified':False,'smartphone_playback_verified':False,
            'publication_approved':False}
    Path(dest).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    if not report['all_technical_checks_pass']:raise AssertionError(report)
    return report

if __name__=='__main__':
    print(json.dumps(run(*sys.argv[1:4]),ensure_ascii=False))
