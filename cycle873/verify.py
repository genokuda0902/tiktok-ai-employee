"""Technical whole-file QA only. Does not establish Japanese ASR or semantic caption sync."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np
START,COUNT,N=90,80,691

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
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(new)],text=True))
 v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']),a['sample_rate'])==(1080,1920,'30/1',691,'48000')
 aa,bb=cv2.VideoCapture(str(old)),cv2.VideoCapture(str(new));idx=0;changed=0;roi=[];inside=[];outside=[]
 try:
  while True:
   ok1,x=aa.read();ok2,y=bb.read()
   if not ok1 and not ok2:break
   if ok1!=ok2:raise AssertionError('frame count mismatch')
   diff=cv2.absdiff(x[::4,::4],y[::4,::4]);r=float(diff[1490//4:1840//4].mean());roi.append(r)
   m=float(diff[132//4:1490//4].mean())
   if START<=idx<START+COUNT:
    changed+=m>3;inside.append(m)
   elif idx%30==0:outside.append(m)
   idx+=1
 finally:aa.release();bb.release()
 ah,bh=audio_hash(old),audio_hash(new)
 if idx!=N or changed!=COUNT or max(roi)>1.5 or max(outside)>1.5 or ah!=bh:
  raise AssertionError(f'gate failed frames={idx} changed={changed} roi={max(roi):.3f} outside={max(outside):.3f} audio={ah==bh}')
 return {'source_sha256':sha(old),'output_sha256':sha(new),'frame_count':idx,'changed_frames':changed,
 'scene_mean_pixel_delta':round(float(np.mean(inside)),3),'caption_roi_max_mean_delta':round(max(roi),4),
 'outside_scene_sample_max_delta':round(max(outside),4),'audio_adts_identical':ah==bh,'audio_adts_sha256':bh,
 'video_audio_decode':'PASS','japanese_voice_inherited':True,'japanese_transcription_verified':False,
 'caption_semantic_sync_verified':False,'source_rights_approved':False,'phone_playback_verified':False,
 'publication_approved':False}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('old','new','report'):p.add_argument('--'+n,required=True)
 x=p.parse_args();data=inspect(x.old,x.new)
 Path(x.report).write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps(data,ensure_ascii=False,indent=2))
