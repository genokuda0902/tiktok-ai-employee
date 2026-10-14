"""Cycle584 video compositor: source fingerprint required, no publishing."""
import argparse, hashlib, json, subprocess
from pathlib import Path
from arith_hook import DEFAULT, FPS, frame, state

BASE_SHA='f715195494b0ce40a4d13414bbb3ede63f45bdaa43fb47ba128fb2583b6092e0'
CAPTIONS=((0,2,'手計算の前に、合計720を確認'),(2,4,'4か月分の売上を入力'),
 (4,6,'SUM関数でも合計720'),(6,9,'数字を入力して集計を指示'),
 (9,12,'B2:B5 を選択する'),(12,16,'グラフの数値も確認'),
 (16,18,'手入力と関数を比較'),(18,19,'保存して、あとで試そう'),
 (19,20,'手計算の前に、合計720を確認'))

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def run(cmd,log):
 p=subprocess.run(cmd,capture_output=True,text=True)
 Path(log).write_text(' '.join(map(str,cmd))+'\nexit='+str(p.returncode)+'\n'+p.stderr)
 if p.returncode:raise RuntimeError('ffmpeg error; inspect '+str(log))

def build(source,output):
 source,output=Path(source),Path(output)
 if not source.is_file() or sha(source)!=BASE_SHA:raise ValueError('source absent or SHA mismatch')
 output.parent.mkdir(parents=True,exist_ok=True)
 # 2s introduction + 1s reversed re-entry of frames 0..29.
 seg=output.parent/'intro_and_loop.mp4'
 command=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(FPS),'-i','-',
 '-vf','scale=1080:1920:flags=lanczos','-an','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',str(seg)]
 with (output.parent/'segment.log').open('w') as log:
  p=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
  try:
   for i in list(range(60))+list(range(29,-1,-1)):
    p.stdin.write(frame(DEFAULT,i).tobytes())
  finally:p.stdin.close()
  if p.wait():raise RuntimeError('segment encode failed')
 graph=('[1:v]trim=start=0:end=2,setpts=PTS-STARTPTS[a];'
        '[0:v]trim=start=2:end=19,setpts=PTS-STARTPTS[b];'
        '[1:v]trim=start=2:end=3,setpts=PTS-STARTPTS[c];'
        '[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]')
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),'-i',str(seg),
 '-filter_complex',graph,'-map','[v]','-map','0:a:0','-map','0:s:0?',
 '-c:v','libx264','-preset','ultrafast','-crf','20','-r','30','-c:a','copy','-c:s','mov_text',
 '-t','20','-movflags','+faststart',str(output)],output.parent/'render.log')
 qa={'cycle':584,'source_sha256':BASE_SHA,'output_sha256':sha(output),
 'change':'truthful 4-step arithmetic hook and consistent loop re-entry; 0-2s and 19-20s',
 'valid_prefix_totals':list(DEFAULT.running_totals()),'genre_support':10,
 'reference_video_direct_comparison':False,'synthetic_demo':True,
 'japanese_narration':False,'audio_caption_sync_verified':False,
 'rights_approved':False,'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED',
 'blockers':['JAPANESE_NARRATION_ABSENT','AUDIO_CAPTION_SYNC_UNVERIFIED','RIGHTS_UNVERIFIED'],
 'cost_jpy':0}
 (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 return qa

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
 a=ap.parse_args();print(json.dumps(build(a.source,a.output),ensure_ascii=False,indent=2))
