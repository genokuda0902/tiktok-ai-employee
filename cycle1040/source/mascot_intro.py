#!/usr/bin/env python3
"""Original procedural mascot opening for a review-only Japanese MP4.

No external images, logo assets, network, posting or publication. Existing
subtitle region y>=1280 and AAC track are deliberately not modified.
"""
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS = 30
W, H = 1080, 1920
SAFE_Y = 1280
INTRO_FRAMES = 45  # 1.5 seconds, direct cut to original proof shot (no ghosted UI)
SOURCE_FRAMES = 691
SOURCE_SHA = '64971783c4bc51007cdb65a09014952a744a1fad8a87ce0f8bbf7dccef571623'
GENRES = ('ai_work','beauty','romance_psychology','money_saving','sales_business',
          'career','health_lifestyle','science_trivia','travel_food',
          'product_comparison_lifestyle')
PALETTES = {
 'ai_work': ('#49E8F4','#FFE267'), 'beauty':('#FFBADB','#FFF0B9'),
 'romance_psychology':('#C8ADFF','#FFD7E4'), 'money_saving':('#7EE9B6','#FFE58A'),
 'sales_business':('#67C9FF','#FFD47B'), 'career':('#95C5FF','#FFF0AA'),
 'health_lifestyle':('#86E9BF','#FFF2C0'), 'science_trivia':('#8DE8F7','#E4C8FF'),
 'travel_food':('#FFCF85','#B3F0E4'), 'product_comparison_lifestyle':('#FFAD8E','#D2E8FF')}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()


def run(args, binary=False):
 p=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:
  raise RuntimeError(f"command failed: {args[0]}\n{p.stderr.decode(errors='replace')[-3000:]}")
 return p.stdout if binary else p.stdout.decode()


def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))


def audio_sha(path):
 return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()


def validate(source, expected_sha, genre, review_only):
 if not review_only:raise ValueError('human review flag is mandatory')
 if genre!='ai_work':raise ValueError('other genres require approved source media')
 if expected_sha!=SOURCE_SHA or sha(source)!=expected_sha:raise ValueError('source SHA mismatch')
 p=probe(source)
 v=[s for s in p['streams'] if s['codec_type']=='video']
 a=[s for s in p['streams'] if s['codec_type']=='audio']
 if len(v)!=1 or len(a)!=1 or len(p['streams'])!=2:raise ValueError('requires exactly one video/audio stream')
 if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],int(v[0]['nb_frames']),a[0]['codec_name'],int(a[0]['sample_rate'])) != ('h264',W,H,'30/1',SOURCE_FRAMES,'aac',48000):
  raise ValueError('unexpected source format')
 return p


def font(size):return ImageFont.truetype(FONT,size)


def hexrgb(color):
 color=color.lstrip('#')
 return tuple(int(color[i:i+2],16) for i in (0,2,4))


def alpha_at(n):
 if n<0 or n>=INTRO_FRAMES:raise ValueError('outside intro')
 # A direct 1.5s cut avoids double-exposed UI text during transparency fades.
 return 1.0


def intro_frame(n,genre='ai_work'):
 if genre not in GENRES:raise ValueError('unknown genre')
 a=alpha_at(n)
 cyan,yellow=PALETTES[genre]
 t=n/FPS
 # Original art only: navy background, abstract data rings, friendly robot.
 im=Image.new('RGBA',(W,SAFE_Y),(6,17,39,255))
 d=ImageDraw.Draw(im)
 for k in range(0,SAFE_Y,4):
  d.rectangle((0,k,W,k+4),fill=(6+int(k/SAFE_Y*4),17+int(k/SAFE_Y*14),39+int(k/SAFE_Y*20),255))
 # soft halo behind robot
 halo=Image.new('RGBA',(W,SAFE_Y));hd=ImageDraw.Draw(halo)
 hd.ellipse((125,325,965,1130),fill=(*hexrgb(cyan),80))
 halo=halo.filter(ImageFilter.GaussianBlur(105));im=Image.alpha_composite(im,halo)
 d=ImageDraw.Draw(im)
 # Abstract radial HUD and motion lines
 for radius in (355,410):
  d.arc((540-radius,720-radius,540+radius,720+radius),20+n*2,250+n*2,fill=(*hexrgb(cyan),90),width=4)
 for i in range(8):
  x=60+i*140
  d.rounded_rectangle((x,1100+int(8*math.sin(t*3+i)),x+64,1112+int(8*math.sin(t*3+i))),radius=5,fill=(31,111,145,110))
 # top kicker and title: not an exact screenshot of any source UI
 d.rounded_rectangle((72,58,430,113),radius=22,fill=(12,67,95,255),outline=cyan,width=3)
 d.text((102,64),'AI × 時短 / 01',font=font(30),fill='white')
 d.text((72,154),'まだ手作業で',font=font(84),fill='white',stroke_width=3,stroke_fill=(0,8,25))
 d.text((72,260),'集計してるの？',font=font(85),fill=yellow,stroke_width=4,stroke_fill=(0,8,25))
 # body float
 bob=math.sin(t*3.7)*13
 cx,cy=540,760+bob
 # lower ground shadow
 d.ellipse((260,1055,830,1125),fill=(2,8,25,190))
 # antenna
 d.line((cx,cy-310,cx,cy-365),fill=(184,231,245,255),width=19)
 d.ellipse((cx-23,cy-394,cx+23,cy-350),fill=cyan,outline='white',width=4)
 # arms behind body (one pointing, one waving)
 wave=math.sin(t*6)*18
 d.line([(cx-195,cy+145),(cx-320,cy+75),(cx-365,cy-30+wave)],fill=(190,224,245,255),width=47,joint='curve')
 d.ellipse((cx-395,cy-68+wave,cx-330,cy+4+wave),fill=(246,251,255,255),outline=(80,160,203,255),width=7)
 d.line([(cx+190,cy+140),(cx+292,cy+28),(cx+307,cy-105)],fill=(183,222,243,255),width=47,joint='curve')
 d.ellipse((cx+278,cy-150,cx+337,cy-65),fill=(246,251,255,255),outline=(80,160,203,255),width=7)
 d.line((cx+306,cy-120,cx+313,cy-203),fill=(246,251,255,255),width=22)
 d.ellipse((cx+301,cy-216,cx+327,cy-189),fill=cyan)
 # body shell and bright front plate
 d.rounded_rectangle((cx-205,cy+45,cx+205,cy+365),radius=135,fill=(188,222,246,255),outline=(255,255,255,255),width=11)
 d.rounded_rectangle((cx-146,cy+104,cx+146,cy+300),radius=80,fill=(13,48,89,255),outline=(67,176,224,255),width=9)
 d.text((cx-57,cy+157),'AI',font=font(80),fill=cyan)
 # neck
 d.rounded_rectangle((cx-72,cy-60,cx+72,cy+105),radius=27,fill=(135,192,226,255),outline=(234,250,255,255),width=8)
 # head shell, faceplate, animated eyes
 d.rounded_rectangle((cx-250,cy-285,cx+250,cy+88),radius=150,fill=(230,245,254,255),outline=(255,255,255,255),width=14)
 d.rounded_rectangle((cx-204,cy-236,cx+204,cy+42),radius=115,fill=(6,30,61,255),outline=(61,145,192,255),width=9)
 blink=(n%71 in (32,33))
 eye_h=9 if blink else 66
 for ex in (cx-103,cx+103):
  d.rounded_rectangle((ex-35,cy-140-eye_h//2,ex+35,cy-140+eye_h//2),radius=min(30,eye_h//2),fill=cyan)
  if not blink:d.ellipse((ex-16,cy-170,ex+2,cy-152),fill=(255,255,255,230))
 d.arc((cx-80,cy-130,cx+80,cy+5),18,162,fill=(96,237,244,255),width=10)
 # tiny evidence card / promise below, safe above 1280
 d.rounded_rectangle((120,1145,960,1243),radius=32,fill=(9,51,73,245),outline=cyan,width=3)
 d.text((205,1160),'Excel作業を、AIで効率化',font=font(45),fill='white')
 # Force an opaque illustration: no ghosted source UI through HUD strokes.
 im.putalpha(255)
 return im


def render(source,dest,report,expected_sha=SOURCE_SHA,genre='ai_work',review_only=False):
 source,dest,report=map(Path,(source,dest,report))
 if len({source.resolve(),dest.resolve(),report.resolve()})!=3 or dest.exists() or report.exists():
  raise ValueError('output paths collide or already exist')
 validate(source,expected_sha,genre,review_only)
 dest.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='mascot1040_') as temp:
  tmp=Path(temp)
  for n in range(INTRO_FRAMES):intro_frame(n,genre).save(tmp/f'{n:03d}.png')
  run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',source,
       '-framerate',str(FPS),'-i',tmp/'%03d.png',
       '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[v]',
       '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
       '-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p',
       '-frames:v',str(SOURCE_FRAMES),'-c:a','copy','-metadata:s:a:0','language=jpn',
       '-movflags','+faststart',dest])
 run(['ffmpeg','-v','error','-xerror','-i',dest,'-f','null','-'])
 p=probe(dest);v=next(s for s in p['streams'] if s['codec_type']=='video')
 if (v['width'],v['height'],int(v['nb_frames']))!=(W,H,SOURCE_FRAMES):raise RuntimeError('invalid output video')
 if audio_sha(source)!=audio_sha(dest):raise RuntimeError('AAC elementary stream changed')
 result={'source_sha256':expected_sha,'output_sha256':sha(dest),'video':'H264 1080x1920 30fps',
         'frames':SOURCE_FRAMES,'duration_seconds':float(p['format']['duration']),
         'original_robot_intro_frames':INTRO_FRAMES,'protected_subtitle_y':SAFE_Y,
         'audio_adts_sha256':audio_sha(dest),'full_av_decode':'PASS',
         'independent_japanese_asr':'NOT_VERIFIED','rights':'NOT_VERIFIED',
         'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for key in ('source','dest','report'):ap.add_argument('--'+key,required=True)
 ap.add_argument('--expected-sha',default=SOURCE_SHA)
 ap.add_argument('--genre',default='ai_work');ap.add_argument('--review-only',action='store_true')
 args=ap.parse_args()
 print(json.dumps(render(args.source,args.dest,args.report,args.expected_sha,args.genre,args.review_only),ensure_ascii=False))
