"""Validate synthetic MP4 technically; does not grant publication approval."""
import argparse,json,subprocess
from pathlib import Path
def validate(mp4:Path,ass:Path):
 p=subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(mp4)],capture_output=True,text=True,check=True)
 streams=json.loads(p.stdout)['streams']
 v=next(s for s in streams if s['codec_type']=='video')
 a=next(s for s in streams if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'h264','30/1',775)
 assert a['codec_name']=='aac' and a['sample_rate']=='48000' and float(a['duration'])>25.5
 text=ass.read_text()
 assert text.count('Dialogue: 0,')==24 and text.count('Dialogue: 1,')==1
 assert '保存して、明日ひとつ試そう' in text
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-map','0:v:0','-f','null','-'],check=True)
 return True
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--mp4',required=True,type=Path);p.add_argument('--ass',required=True,type=Path)
 a=p.parse_args();validate(a.mp4,a.ass);print('Synthetic CI MP4 technical QA: PASS; publication NOT approved')
