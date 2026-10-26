"""Independent technical checks. Does not perform ASR or semantic subtitle verification."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np
START,COUNT,N=422,88,691

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def audio_hash(p):
 with tempfile.TemporaryDirectory() as d:
  q=Path(d)/'audio.aac'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts',str(q)],check=True,timeout=60)
  return sha(q)

def inspect(old,new):
 for p in (old,new):subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,timeout=150)
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(new)],text=True))
 v=next(x for x in data['streams'] if x['codec_type']=='video');a=next(x for x in data['streams'] if x['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']),a['sample_rate'])==(1080,1920,'30/1',691,'48000')
 old_cap,new_cap=cv2.VideoCapture(str(old)),cv2.VideoCapture(str(new)); idx=0;changed=0;caption=[];outside=[];inside=[]
 try:
  while True:
   ok1,x=old_cap.read();ok2,y=new_cap.read()
   if not ok1 and not ok2:break
   if ok1!=ok2:raise AssertionError('frame count mismatch')
   diff=cv2.absdiff(x[::4,::4],y[::4,::4]); caption.append(float(diff[1490//4:1840//4].mean()))
   m=float(diff[285//4:1450//4].mean())
   if START<=idx<START+COUNT:
    changed+=m>3;inside.append(m)
   elif idx%30==0:outside.append(m)
   idx+=1
 finally:old_cap.release();new_cap.release()
 ah,bh=audio_hash(old),audio_hash(new)
 if idx!=N or changed!=COUNT or max(caption)>1.5 or max(outside)>1.5 or ah!=bh:
  raise AssertionError(f'QA FAIL frames={idx} changed={changed} caption={max(caption):.4f} outside={max(outside):.4f} audio={ah==bh}')
 return {'source_sha256':sha(old),'output_sha256':sha(new),'frame_count':idx,'changed_frames':changed,
  'changed_picture_mean_delta':round(float(np.mean(inside)),3),'caption_roi_max_mean_delta':round(max(caption),4),
  'outside_scene_sample_max_delta':round(max(outside),4),'audio_adts_identical':True,'audio_adts_sha256':bh,
  'video_audio_full_decode':'PASS','japanese_audio_preserved':True,'japanese_transcription_verified':False,
  'caption_semantic_sync_verified':False,'phone_playback_verified':False,'publication_approved':False}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('old','new','report'):p.add_argument('--'+k,required=True)
 a=p.parse_args();d=inspect(a.old,a.new);Path(a.report).write_text(json.dumps(d,ensure_ascii=False,indent=2));print(json.dumps(d,ensure_ascii=False,indent=2))