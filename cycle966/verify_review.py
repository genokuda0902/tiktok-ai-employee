"""Local completed-video QA; not a speech recognition or rights approval."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np

def call(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=240)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1500:])
 return p.stdout

def probe(p):return json.loads(call(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def adts(p):return hashlib.sha256(call(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def check(src,dst):
 d=probe(dst);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
 assert v['codec_name']=='h264' and (v['width'],v['height'],v['avg_frame_rate'])==(1080,1920,'30/1')
 assert int(v['nb_frames'])==691 and abs(float(d['format']['duration'])-691/30)<0.03
 assert a['codec_name']=='aac' and (int(a['sample_rate']),a['channels'])==(48000,2)
 for selector in ('0:v:0','0:a:0'):call(['ffmpeg','-v','error','-xerror','-i',str(dst),'-map',selector,'-f','null','-'])
 assert adts(src)==adts(dst),'AAC changed'
 x=cv2.VideoCapture(str(src));y=cv2.VideoCapture(str(dst));n=0;protected=0;inside=[];outside=[]
 while True:
  ok1,f=x.read();ok2,g=y.read()
  if not ok1 and not ok2:break
  assert ok1 and ok2
  delta=float(np.abs(cv2.resize(f[1490:1850],(270,90)).astype('int16')-cv2.resize(g[1490:1850],(270,90)).astype('int16')).mean())
  protected=max(protected,delta)
  upper=float(np.abs(cv2.resize(f[150:1350],(135,150)).astype('int16')-cv2.resize(g[150:1350],(135,150)).astype('int16')).mean())
  (inside if 174<=n<261 else outside).append(upper);n+=1
 x.release();y.release()
 assert n==691 and protected<3 and np.mean(inside)>15 and max(outside)<4,(n,protected,np.mean(inside),max(outside))
 return {'source_sha256':sha(src),'output_sha256':sha(dst),'video':'H264 1080x1920 30fps 691 frames','duration':float(d['format']['duration']),'audio':'AAC 48kHz stereo','full_av_decode':'PASS','audio_adts_sha256':adts(dst),'audio_bitstream_identical':True,'caption_protected_max_mean_delta_255':round(protected,4),'scene03_mean_delta_255':round(float(np.mean(inside)),4),'outside_scene_max_delta_255':round(max(outside),4),'japanese_asr':'UNVERIFIED','smartphone':'UNVERIFIED','publication':'NOT APPROVED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args();r=check(a.source,a.output);Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))
