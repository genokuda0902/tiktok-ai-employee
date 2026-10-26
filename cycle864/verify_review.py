"""Private local technical checks only; NOT speech transcription or publication approval."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np
from cinematic_laptop import sha256,check_streams,START,COUNT,FRAMES

def verify(src,out):
 src,out=Path(src),Path(out);check_streams(src);check_streams(out)
 for p in (src,out):subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,timeout=120)
 with tempfile.TemporaryDirectory() as d:
  hashes=[]
  for i,p in enumerate((src,out)):
   path=Path(d)/f'{i}.aac'
   subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts',str(path)],check=True,timeout=45)
   hashes.append(sha256(path))
 a,b=cv2.VideoCapture(str(src)),cv2.VideoCapture(str(out));indices=(508,527,555,582,620)
 samples=[]
 for ix in indices:
  a.set(cv2.CAP_PROP_POS_FRAMES,ix);b.set(cv2.CAP_PROP_POS_FRAMES,ix)
  ok1,f1=a.read();ok2,f2=b.read()
  if not(ok1 and ok2):raise RuntimeError(f'cannot read frame {ix}')
  delta=np.abs(f1.astype(np.float32)-f2.astype(np.float32))
  samples.append(dict(frame=ix,scene_delta=round(float(delta[330:1450,:,:].mean()),3),caption_delta=round(float(delta[1490:1840,:,:].mean()),3)))
 a.release();b.release()
 if hashes[0]!=hashes[1]:raise ValueError('audio bitstream changed')
 if not all(s['scene_delta']>15 for s in samples[:4]):raise ValueError('no meaningful visual change')
 if not all(s['caption_delta']<2 for s in samples):raise ValueError('caption region changed')
 return dict(source_sha256=sha256(src),output_sha256=sha256(out),audio_adts_sha256=hashes[0],audio_identical=True,full_decode=True,frames=FRAMES,changed_frames=COUNT,scene_samples=samples,subtitle_region_preserved=True,speech_semantics_verified=False,smartphone_verified=False,publication_approved=False)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
 r=verify(a.source,a.output);Path(a.report).write_text(json.dumps(r,indent=2,ensure_ascii=False));print(json.dumps(r,ensure_ascii=False,indent=2))