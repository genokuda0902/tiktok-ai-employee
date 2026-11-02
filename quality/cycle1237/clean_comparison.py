#!/usr/bin/env python3
"""Repair a visibly obstructed Before/After illustration using an original, offline vector panel.

Only the reviewed scene's illustration ROI is replaced. Narration, subtitles,
headings, chapters and audio are preserved. No posting, network or paid APIs.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1080,1920,30
ROI=(44,474,1000,805)
PALETTES={'ai':'#55E4D2','business':'#70B9F6','money':'#E2C66F',
 'learning':'#9BC4F6','health':'#70D2B1','food':'#F4B280',
 'travel':'#80D5E5','beauty':'#ECA5CD','career':'#AAB4F7','life':'#A7D39A'}
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def rgb(s): return tuple(bytes.fromhex(s.lstrip('#')))
def font(size,bold=False): return ImageFont.truetype(BOLD if bold else REG,round(size))
def command(args):
 p=subprocess.run([str(a) for a in args],capture_output=True)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-1500:])
 return p.stdout

def probe(path): return json.loads(command(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',path]))
def streams(info):
 return (next(s for s in info['streams'] if s['codec_type']=='video'),
         next(s for s in info['streams'] if s['codec_type']=='audio'))
def audio_hash(path):
 return hashlib.sha256(command(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def validate_scene(start,end,chapters):
 if not (0<=start<end and 0.5<=end-start<=5): raise ValueError('invalid scene interval')
 if not any(abs(float(c['start_time'])-start)<.05 and abs(float(c['end_time'])-end)<.05 for c in chapters):
  raise ValueError('interval must match a real chapter')

def render_panel(genre='ai',before='もっと良くして',after='見出しを短くして'):
 if genre not in PALETTES: raise ValueError('unsupported genre')
 if max(len(before),len(after))>14 or not before or not after: raise ValueError('text exceeds safe area')
 S=2; pw,ph=840,702; w,h=pw*S,ph*S
 a=rgb(PALETTES[genre]); bg=Image.new('RGBA',(w,h)); pix=bg.load()
 for y in range(h):
  for x in range(w):
   glow=math.exp(-((x/w-.86)**2/.22+(y/h-.08)**2/.25))*0.35
   pix[x,y]=(int(5+14*glow),int(12+35*glow),int(24+39*glow),255)
 d=ImageDraw.Draw(bg)
 def rrect(b,r,fill,outline=None,width=1):
  d.rounded_rectangle(tuple(round(v*S) for v in b),radius=round(r*S),fill=fill,
    outline=outline,width=round(width*S))
 def text(x,y,s,size,color,bold=False):
  d.text((x*S,y*S),s,font=font(size*S,bold),fill=color,stroke_width=0)
 rrect((1,1,pw-2,ph-2),24,None,(*a,125),2)
 rrect((18,18,455,76),14,(11,64,69,245),(*a,185),1)
 text(35,27,'修正は「1点」に絞る',28,(232,250,247),True)
 text(662,36,'実演 / 架空例',16,(195,226,227))
 rrect((28,107,pw-28,280),22,(16,17,32,255),(99,119,149,255),2)
 rrect((46,124,211,173),12,(104,47,68,255),(170,82,111,255),1)
 text(70,129,'BEFORE',25,(255,227,234),True)
 text(64,190,'「'+before+'」',40,(252,251,255),True)
 text(620,207,'何を直す？',20,(199,206,220))
 d.line([(pw//2*S,294*S),(pw//2*S,352*S)],fill=(*a,230),width=4*S)
 d.polygon([(pw//2*S-12*S,343*S),(pw//2*S+12*S,343*S),(pw//2*S,362*S)],fill=(*a,240))
 rrect((28,379,pw-28,564),22,(6,54,60,255),(*a,225),3)
 rrect((46,397,180,446),12,(13,100,103,255),(*a,170),1)
 text(64,403,'AFTER',25,(228,255,251),True)
 text(64,467,'「'+after+'」',40,(249,255,255),True)
 for x,t in [(28,'対象：見出し'),(300,'変更：短くする'),(573,'範囲：1点だけ')]:
  rrect((x,602,x+229,660),12,(13,59,65,255),(*a,105),1)
  text(x+14,615,t,20,(225,247,246))
 bg=bg.resize(ROI[2:],Image.Resampling.LANCZOS)
 overlay=Image.new('RGBA',(W,H),(0,0,0,0)); overlay.alpha_composite(bg,(ROI[0],ROI[1])); return overlay

def render(source,output,genre='ai',start=13.733,end=16.633,report=None):
 source=Path(source);output=Path(output)
 if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('missing source or same path')
 info=probe(source); v,a=streams(info)
 if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',W,H,'30/1','aac'):
  raise ValueError('unsupported source codec or geometry')
 frames=int(v['nb_frames']); validate_scene(start,end,info['chapters'])
 output.parent.mkdir(parents=True,exist_ok=True)
 png=output.parent/(output.stem+'_overlay.png');render_panel(genre).save(png)
 last=end-1/FPS
 filter_graph=f"[0:v][1:v]overlay=0:0:enable='between(t,{start:.3f},{last:.3f})':format=auto[v]"
 command(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-loop','1','-framerate',FPS,'-i',png,
  '-filter_complex',filter_graph,'-map','[v]','-map','0:a:0','-map_chapters','0',
  '-c:v','libx264','-preset','medium','-crf','21','-x264-params','aq-mode=3:aq-strength=1.0',
  '-pix_fmt','yuv420p','-frames:v',frames,'-c:a','copy','-movflags','+faststart',output])
 out=probe(output); ov,oa=streams(out)
 if (ov['width'],ov['height'],ov['r_frame_rate'],int(ov['nb_frames']))!=(W,H,'30/1',frames): raise RuntimeError('frame geometry changed')
 if audio_hash(source)!=audio_hash(output): raise RuntimeError('AAC bitstream changed')
 if len(info['chapters'])!=len(out['chapters']): raise RuntimeError('chapters changed')
 command(['ffmpeg','-v','error','-xerror','-i',output,'-map','0:v:0','-map','0:a:0','-f','null','-'])
 qa={'genre':genre,'genres_supported':len(PALETTES),'source_bytes':source.stat().st_size,'output_bytes':output.stat().st_size,
  'resolution':[W,H],'fps':FPS,'frames':frames,'chapters':len(out['chapters']),
  'duration_s':float(out['format']['duration']),'audio_aac_sha256':audio_hash(output),'audio_bitstream_identical':True,
  'full_av_decode':'PASS','subtitle_semantics':'NOT VERIFIED (no independent ASR)',
  'source_rights':'NOT VERIFIED','employee_approval':'NOT GRANTED','publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
 if report: Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 return qa

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--genre',choices=sorted(PALETTES),default='ai');p.add_argument('--report')
 args=p.parse_args();print(json.dumps(render(args.source,args.output,args.genre,report=args.report),ensure_ascii=False))
