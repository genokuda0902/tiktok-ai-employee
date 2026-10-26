"""Private technical QA. Not a transcript, rights check, or publication approval."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np
from clean_hook import sha256,media_info,START,COUNT,FRAMES

def verify(src,out):
 src,out=Path(src),Path(out)
 media_info(src);media_info(out)
 for p in (src,out):
  subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,timeout=120)
 with tempfile.TemporaryDirectory() as d:
  hashes=[]
  for j,p in enumerate((src,out)):
   a=Path(d)/f'{j}.aac'
   subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts',str(a)],check=True,timeout=45)
   hashes.append(sha256(a))
 if hashes[0]!=hashes[1]:raise RuntimeError('audio bitstream changed')
 cap0,cap1=cv2.VideoCapture(str(src)),cv2.VideoCapture(str(out)); samples=[]
 for idx in (0,15,32,60,82,110):
  cap0.set(cv2.CAP_PROP_POS_FRAMES,idx);cap1.set(cv2.CAP_PROP_POS_FRAMES,idx)
  ok0,a=cap0.read();ok1,b=cap1.read()
  if not(ok0 and ok1):raise RuntimeError('frame read failed')
  delta=np.abs(a.astype(np.float32)-b.astype(np.float32))
  samples.append(dict(frame=idx,visual_delta=round(float(delta[330:1450].mean()),3),caption_delta=round(float(delta[1490:1840].mean()),3)))
 cap0.release();cap1.release()
 if not all(x['visual_delta']>20 for x in samples[:5]):raise RuntimeError('opening change too small')
 if not all(x['caption_delta']<2 for x in samples):raise RuntimeError('subtitle safe region changed')
 return dict(source_sha256=sha256(src),output_sha256=sha256(out),audio_adts_sha256=hashes[0],audio_bit_identical=True,full_audio_video_decode=True,frames=FRAMES,changed_frames=COUNT,samples=samples,caption_region_preserved=True,independent_speech_transcription=False,semantic_caption_alignment=False,smartphone_playback=False,public_rights_approved=False,employee_approved=False,publication_approved=False)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
 r=verify(a.source,a.output);Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
