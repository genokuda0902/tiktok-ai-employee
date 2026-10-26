"""Offline technical QA; no ASR or rights/quality approval claims."""
import argparse,hashlib,json,subprocess,cv2,numpy as np
from pathlib import Path

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def audio_sha(path,tmp):
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(tmp)],check=True)
    return sha(tmp)
def info(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))
def frame(path,i):
    cap=cv2.VideoCapture(str(path));cap.set(cv2.CAP_PROP_POS_FRAMES,i);ok,f=cap.read();cap.release()
    if not ok:raise RuntimeError('frame missing '+str(i))
    return f

def verify(old,new,output):
    old,new=Path(old),Path(new);v=info(new)
    vv=next(x for x in v['streams'] if x['codec_type']=='video')
    aa=next(x for x in v['streams'] if x['codec_type']=='audio')
    assert vv['width']==1080 and vv['height']==1920 and vv['codec_name']=='h264' and vv['r_frame_rate']=='30/1' and int(vv['nb_frames'])==691
    assert aa['codec_name']=='aac' and aa['sample_rate']=='48000'
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(new),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    with __import__('tempfile').TemporaryDirectory() as d:
        old_a=audio_sha(old,Path(d)/'old.aac');new_a=audio_sha(new,Path(d)/'new.aac')
    assert old_a==new_a,'audio stream changed'
    differences=[];protected=[];unmodified=[]
    for i in [175,190,207,225,244]:
        a,b=frame(old,i),frame(new,i)
        differences.append(round(float(np.abs(a[340:1210,50:1030].astype('int16')-b[340:1210,50:1030].astype('int16')).mean()),3))
        protected.append(round(float(np.abs(a[1250:1810].astype('int16')-b[1250:1810].astype('int16')).mean()),3))
    for i in [90,360,600]:
        a,b=frame(old,i),frame(new,i)
        unmodified.append(round(float(np.abs(a.astype('int16')-b.astype('int16')).mean()),3))
    assert min(differences)>15,'new visual scene not changed'
    assert max(protected)<4,'caption area unexpectedly modified'
    assert max(unmodified)<4,'other scenes unexpectedly modified'
    r={'cycle':857,'video_codec':'h264','width':1080,'height':1920,'fps':30,'frames':691,
       'duration_seconds':round(float(v['format']['duration']),3),'audio_codec':'aac','sample_rate':48000,
       'aac_elementary_stream_equal':True,'aac_sha256':new_a,
       'modified_scene_mean_abs_pixel_difference':differences,
       'protected_caption_region_mean_abs_difference':protected,
       'other_scene_mean_abs_difference':unmodified,
       'full_audio_video_decode':True,'source_sha256':sha(old),'output_sha256':sha(new),
       'speech_transcription_verified':False,'caption_semantic_sync_verified':False,
       'source_rights_approved':False,'phone_playback_verified':False,
       'publication_approved':False,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    Path(output).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('old');p.add_argument('new');p.add_argument('output');a=p.parse_args();verify(a.old,a.new,a.output)