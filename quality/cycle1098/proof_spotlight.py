"""Review-only moving proof spotlight for three lines in a fictional Writer demo.

No private media is shipped. Source must be SHA-pinned. This is a visual
reimplementation, not an original v33 renderer or Japanese ASR.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw

FPS = 30
PALETTES = {'ai_work':'#36d9dc','money':'#f1c267','career':'#75baf7',
            'business':'#6ed9ae','health':'#ffa09b','study':'#b7a5f8',
            'lifestyle':'#f5add4','technology':'#66d7fc','travel':'#ffcf8d',
            'mindset':'#a6e7be'}
START = 525  # 17.5 seconds; within the Writer document scene
COUNT = 72   # 2.4 seconds, ending before the next chapter
RECTS = [(136,544,809,614),(136,612,809,681),(136,680,809,749)]
SAFE_CAPTION_Y = 1490

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def cmd(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(f'{args[0]}: {p.stderr[-1200:]}')
    return p.stdout

def validate(m):
    if set(m) != {'genre','synthetic_scenario','review_only','rights_status','contains_private_data'}:
        raise ValueError('manifest schema mismatch')
    if m['genre'] not in PALETTES: raise ValueError('genre not approved')
    if m['synthetic_scenario'] is not True or m['review_only'] is not True:
        raise ValueError('review gate failed')
    if m['rights_status']!='unverified' or m['contains_private_data'] is not False:
        raise ValueError('privacy/rights gate failed')
    if START+COUNT > 609: raise ValueError('spotlight crosses chapter cut')
    if any(y0<270 or y1>920 or y1>=SAFE_CAPTION_Y or x0<50 or x1>900
           for x0,y0,x1,y1 in RECTS): raise ValueError('unsafe overlay geometry')
    return True

def smooth(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)

def make_overlay(frame, genre):
    if not 0<=frame<COUNT: raise ValueError('frame outside spotlight')
    if genre not in PALETTES: raise ValueError('invalid palette')
    rgb=tuple(bytes.fromhex(PALETTES[genre][1:]))
    im=Image.new('RGBA',(1080,920),(0,0,0,0));d=ImageDraw.Draw(im)
    stage=min(2,frame//24)
    within=frame%24
    fade=min(smooth(within/5),smooth((23-within)/5))
    x0,y0,x1,y1=RECTS[stage]
    a=round(170*fade)
    # Thin stroke outside text and a tiny cue at the left margin.
    d.rounded_rectangle((x0,y0,x1,y1),radius=12,
                        outline=rgb+(a,),width=4)
    d.ellipse((x0-16,(y0+y1)//2-8,x0,(y0+y1)//2+8),fill=rgb+(round(220*fade),))
    return im

def probe(path):
    return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def adts_sha(path):
    with tempfile.TemporaryDirectory() as tmp:
        f=Path(tmp)/'sound.aac'
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),
             '-map','0:a:0','-c:a','copy','-f','adts',str(f)])
        return sha(f)

def render(source,out,source_sha,manifest):
    validate(manifest)
    if sha(source)!=source_sha: raise ValueError('source SHA mismatch; refuse output')
    data=probe(source)
    v=next((s for s in data['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    if not v or not a or (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])!=(1080,1920,'h264','30/1') or a['codec_name']!='aac':
        raise ValueError('source must be 1080x1920 30fps H264 + AAC')
    n=int(v.get('nb_frames') or round(float(data['format']['duration'])*FPS))
    if n!=691: raise ValueError('unexpected source timeline')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for i in range(COUNT): make_overlay(i,manifest['genre']).save(p/f'focus_{i:03d}.png')
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-itsoffset',str(START/FPS),'-framerate',str(FPS),'-start_number','0',
             '-i',str(p/'focus_%03d.png'),
             '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(n),
             '-movflags','+faststart',str(out)])
    return {'source_sha256':source_sha,'output_sha256':sha(out),
            'audio_bitstream_identical':adts_sha(source)==adts_sha(out),
            'changed_frames':COUNT,'first_frame':START,'last_frame':START+COUNT-1,
            'release':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
            'japanese_asr':'NOT_VERIFIED'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--source-sha',required=True)
    ap.add_argument('--out',required=True);ap.add_argument('--manifest',required=True)
    ap.add_argument('--report')
    args=ap.parse_args();m=json.loads(Path(args.manifest).read_text())
    r=render(args.source,args.out,args.source_sha,m)
    if args.report: Path(args.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
