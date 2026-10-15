"""Cycle585: splice original vector motion into verified cycle584; no posting."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from evidence_motion import DEMO,FPS,frame,bar_state

SOURCE_SHA='b9e7304e9929a521dfd03f3cb3c28a13bd8e29147642f48c9f03000b400ba191'

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()

def run(cmd,log):
 p=subprocess.run(cmd,capture_output=True,text=True)
 Path(log).write_text('COMMAND: '+' '.join(map(str,cmd))+'\nexit='+str(p.returncode)+'\n'+p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError('ffmpeg failed; '+str(log))

def build(source,output):
 source,output=Path(source),Path(output)
 if not source.exists() or sha(source)!=SOURCE_SHA:raise ValueError('cycle584 source missing or checksum mismatch')
 output.parent.mkdir(parents=True,exist_ok=True)
 segment=output.parent/'motion_segment.mp4'
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(FPS),'-i','-',
      '-vf','scale=1080:1920:flags=lanczos','-an','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',str(segment)]
 with (output.parent/'segment.log').open('w') as log:
  p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  try:
   for i in range(120):p.stdin.write(frame(DEMO,i).tobytes())
  finally:p.stdin.close()
  if p.wait():raise RuntimeError('segment encode failed')
 graph=('[0:v]trim=start=0:end=12,setpts=PTS-STARTPTS[a];'
        '[1:v]setpts=PTS-STARTPTS[b];'
        '[0:v]trim=start=16:end=20,setpts=PTS-STARTPTS[c];'
        '[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]')
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),'-i',str(segment),
      '-filter_complex',graph,'-map','[v]','-map','0:a:0','-map','0:s:0?',
      '-c:v','libx264','-preset','ultrafast','-crf','20','-r','30','-c:a','copy','-c:s','mov_text',
      '-t','20','-movflags','+faststart',str(output)],output.parent/'render.log')
 qa={'cycle':585,'source_sha256':SOURCE_SHA,'output_sha256':sha(output),
     'change':'12-16s evidence-first graph animation, numeric labels appear only at completion',
     'verified_values':list(DEMO.values),'verified_total':sum(DEMO.values),
     'genre_contract':10,'synthetic_demo':True,'reference_video_direct_comparison':False,
     'japanese_narration':False,'audio_caption_sync_verified':False,
     'rights_approved':False,'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED',
     'blockers':['JAPANESE_NARRATION_ABSENT','AUDIO_CAPTION_SYNC_UNVERIFIED','RIGHTS_UNVERIFIED'],
     'cost_jpy':0}
 (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
 return qa

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 a=p.parse_args();print(json.dumps(build(a.source,a.output),ensure_ascii=False,indent=2))
