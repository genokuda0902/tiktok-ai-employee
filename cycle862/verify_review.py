"""Independent codec/pixel/audio checks. No ASR or human speech claims."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from actionable_outro import sha,check_streams,START,N,ROI

def run(cmd):subprocess.run(cmd,check=True,timeout=120,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def snap(src,frame,out):
 run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss',f'{frame/30:.6f}','-i',str(src),'-frames:v','1','-y',str(out)])
 return np.asarray(Image.open(out).convert('RGB'),dtype=np.float32)
def adts(src,dst):
 run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(src),'-map','0:a:0','-c:a','copy','-f','adts','-y',str(dst)])
 return sha(dst)
def verify(before,after):
 check_streams(before);check_streams(after)
 run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(after),'-map','0:v:0','-f','null','-'])
 run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(after),'-map','0:a:0','-f','null','-'])
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);a=adts(before,td/'a.adts');b=adts(after,td/'b.adts')
  samples=[]
  for f in (632,650,679):
   old=snap(before,f,td/f'old_{f}.png');new=snap(after,f,td/f'new_{f}.png')
   x,y,w,h=ROI
   visual=float(np.mean(np.abs(old[y:y+h,x:x+w]-new[y:y+h,x:x+w])))
   caption=float(np.mean(np.abs(old[1490:1840,40:1040]-new[1490:1840,40:1040])))
   samples.append({'frame':f,'picture_mean_abs_pixel_delta':round(visual,3),'subtitle_mean_abs_pixel_delta':round(caption,3)})
  old=snap(before,400,td/'outside_old.png');new=snap(after,400,td/'outside_new.png')
  outside=float(np.mean(np.abs(old-new)))
 checks={'codec_resolution_frame_count':True,'full_video_decode':True,'full_audio_decode':True,'AAC_elementary_bitstream_identical':a==b,'edited_picture_changes':all(z['picture_mean_abs_pixel_delta']>10 for z in samples),'caption_region_unchanged_within_encoding_tolerance':all(z['subtitle_mean_abs_pixel_delta']<3 for z in samples),'other_scene_unchanged_within_encoding_tolerance':outside<3,'no_publishing_or_rights_claim':True}
 return {'before_sha256':sha(before),'after_sha256':sha(after),'audio_adts_sha256':a,'samples':samples,'outside_scene_mean_abs_pixel_delta':round(outside,3),'checks':checks,'all_pass':all(checks.values()),'limits':['No ASR transcript / Japanese semantic verification','No phone playback','No source media rights approval','No v33 direct comparison']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('before');p.add_argument('after');p.add_argument('report');a=p.parse_args()
 r=verify(a.before,a.after);Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
 if not r['all_pass']:raise SystemExit(1)