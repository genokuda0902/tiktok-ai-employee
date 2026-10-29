#!/usr/bin/env python3
"""Review-only upper-artwork loop bridge. Never publishes or uploads user media."""
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image
W,H,FPS=1080,1920,30
HARD_SAFE_BOTTOM,FADE_BOTTOM=1180,1230
BRIDGE_SECONDS=0.55
PALETTES={
 'ai_work':'#13d5d1','finance':'#f0ba52','learning':'#5baceb',
 'health':'#65cda4','travel':'#ed9f5e','food':'#e4a66c',
 'science':'#9e94ec','history':'#b8a27d','business':'#51c4de',
 'lifestyle':'#dd98c4'}
def run(cmd):
 return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for part in iter(lambda:f.read(1<<20),b''):h.update(part)
 return h.hexdigest()
def probe(path):
 return json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
def verify_genre(genre,synthetic=False):
 if genre not in PALETTES:raise ValueError('Unknown genre')
 if genre!='ai_work' and not synthetic:raise ValueError('Unreviewed genre layout: fail closed')
def make_bridge_image(first_frame,out,genre='ai_work',synthetic=False):
 verify_genre(genre,synthetic)
 im=Image.open(first_frame).convert('RGBA')
 if im.size!=(W,H):raise ValueError('First frame must be 1080x1920')
 alpha=Image.new('L',(W,H),0)
 values=([255]*HARD_SAFE_BOTTOM+
  [round(255*(FADE_BOTTOM-1-y)/(FADE_BOTTOM-HARD_SAFE_BOTTOM))
   for y in range(HARD_SAFE_BOTTOM,FADE_BOTTOM)]+
  [0]*(H-FADE_BOTTOM))
 for y in range(H):alpha.paste(int(values[y]),(0,y,W,y+1))
 im.putalpha(alpha)
 Path(out).parent.mkdir(parents=True,exist_ok=True)
 im.save(out)
 return out
def render(source,output,genre='ai_work',synthetic=False,first_frame=None):
 verify_genre(genre,synthetic)
 source,output=Path(source),Path(output)
 output.parent.mkdir(parents=True,exist_ok=True)
 assets=output.parent/'assets';assets.mkdir(exist_ok=True)
 info=probe(source)
 v=next(s for s in info['streams'] if s['codec_type']=='video')
 if (v['width'],v['height'],v['r_frame_rate'])!=(W,H,'30/1'):raise ValueError('Unexpected source format')
 frames=int(v['nb_read_frames']);duration=frames/FPS
 if duration<=BRIDGE_SECONDS+2:raise ValueError('Source too short')
 if first_frame is None:
  first_frame=assets/'first.png'
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-frames:v','1',str(first_frame)])
 bridge=make_bridge_image(first_frame,assets/'loop_bridge.png',genre,synthetic)
 start=round(duration-BRIDGE_SECONDS,6)
 filt=(f'[1:v]format=rgba,fade=t=in:st={start}:d={BRIDGE_SECONDS}:alpha=1[bridge];'
       f'[0:v][bridge]overlay=0:0:format=auto:shortest=1[v]')
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-loop','1','-framerate',str(FPS),'-i',str(bridge),
      '-filter_complex',filt,'-map','[v]','-map','0:a:0',
      '-c:v','libx264','-preset','veryfast','-crf','19',
      '-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(frames),
      '-c:a','copy','-movflags','+faststart',str(output)])
 return {'cycle':977,'frames':frames,'duration':duration,'bridge_start':start,
         'bridge_duration':BRIDGE_SECONDS,'genre':genre,'genres_configured':len(PALETTES),
         'source_sha256':sha256(source),'output_sha256':sha256(output),
         'independent_japanese_asr':'NOT_AVAILABLE','publication_approved':False}
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
 p.add_argument('--first-frame');p.add_argument('--report')
 a=p.parse_args();result=render(a.source,a.output,a.genre,a.synthetic,a.first_frame)
 if a.report:Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
