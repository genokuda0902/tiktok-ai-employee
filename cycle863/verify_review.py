"""Technical-only review of a locally generated MP4; no publication approval."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from proof_compare import FRAMES,FPS,START,COUNT,ROI,check_streams,sha256

def run(*args):return subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=140)

def audio_hash(path):
 p=run('ffmpeg','-v','error','-nostdin','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-')
 return hashlib.sha256(p.stdout).hexdigest()

def frame(path,n,folder):
 dest=Path(folder)/(Path(path).stem+f'_{n}.png')
 run('ffmpeg','-v','error','-nostdin','-i',str(path),'-vf',f'select=eq(n\\,{n})','-vsync','0','-frames:v','1','-y',str(dest))
 return np.asarray(Image.open(dest).convert('RGB'),dtype=np.float32)

def verify(source,out):
 check_streams(source);check_streams(out)
 for p in (source,out):run('ffmpeg','-v','error','-nostdin','-i',str(p),'-map','0:v:0','-map','0:a:0','-f','null','-')
 a0,a1=audio_hash(source),audio_hash(out)
 if a0!=a1:raise AssertionError('AAC elementary streams differ')
 samples=[]
 with tempfile.TemporaryDirectory() as td:
  for n in (420,435,460,485,502,520):
   a,b=frame(source,n,td),frame(out,n,td)
   x,y,w,h=ROI
   picture=float(np.abs(a[y:y+h,x:x+w]-b[y:y+h,x:x+w]).mean())
   captions=float(np.abs(a[1490:1840,60:1010]-b[1490:1840,60:1010]).mean())
   samples.append({'frame':n,'in_edit':START<=n<START+COUNT,'picture_mean_pixel_delta':round(picture,3),'caption_mean_pixel_delta':round(captions,3)})
 if any(s['picture_mean_pixel_delta']<12 for s in samples if s['in_edit']):raise AssertionError('no meaningful changed picture')
 if any(s['caption_mean_pixel_delta']>2.0 for s in samples):raise AssertionError('caption area drift too large')
 return {'source_sha256':sha256(source),'output_sha256':sha256(out),'audio_adts_sha256':a0,'audio_identical':True,'full_video_audio_decode':True,'stream_format':'1080x1920 H264 30fps 691 frames AAC 48kHz','changed_frames':COUNT,'samples':samples,'japanese_speech_transcribed':False,'caption_semantics_verified':False,'smartphone_playback_verified':False,'rights_approved':False,'human_approval':False,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
 result=verify(a.source,a.output);Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))