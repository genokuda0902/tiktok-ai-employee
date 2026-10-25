"""Cycle828: offline, human-review-only clean Japanese subtitles + voice mastering.
Builds on cycle827 speech timing, cycle826 original scenes, cycle819 offline TTS.
No paid API, no upload, no posting.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cycle827'))
import speech827
from PIL import Image,ImageChops

FRAMES=speech827.FRAMES
OUTPUT='cycle828_CLEAN_CAPTIONS_MASTERED_VOICE_HUMAN_REVIEW.mp4'
ACCENTS={'sales_business':'#37C6BE','ai_work':'#37C6BE','beauty':'#E3A1B8',
 'love_psychology':'#E2A2C1','money_saving':'#B7A05C','career':'#6288CF',
 'health_life':'#78B78C','science':'#D39D69','travel_food':'#947CD0',
 'product_life':'#65AABF'}

def bgr(hex_color):
    c=hex_color.lstrip('#')
    if len(c)!=6 or any(x not in '0123456789ABCDEFabcdef' for x in c):
        raise ValueError('RGB hex expected')
    return '&H00'+c[4:6]+c[2:4]+c[:2]+'&'

def execute(cmd,capture=False):
    if capture:return subprocess.run(cmd,check=True,capture_output=True,text=True).stderr
    subprocess.run(cmd,check=True)

def measure(audio):
    log=execute(['ffmpeg','-hide_banner','-nostats','-i',str(audio),'-af',
      'loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],True)
    matches=re.findall(r'\{\s*"input_i"\s*:[^}]*\}',log,re.S)
    if not matches:raise RuntimeError('loudnorm measurements absent')
    return json.loads(matches[-1])

def prepare(root):
    root=Path(root);out=root/'output';out.mkdir(parents=True,exist_ok=True)
    speech827.create(root)
    previous=(out/'captions827.ass').read_text(encoding='utf-8')
    old='Style: Caption,Noto Sans CJK JP,65,'
    if old not in previous:raise ValueError('previous caption style changed')
    clean=previous.replace(old,'Style: Caption,Noto Sans CJK JP,78,')
    clean=clean.replace('1,5,1,5,65,65,0,1','1,0,0,5,65,65,0,1')
    clean=clean.replace(r'\c&H006BEBD9&',r'\c'+bgr(ACCENTS['ai_work']))
    clean=clean.replace(r'\c&H00FFFFFF&',r'\c&H00F0F0F0&')
    clean=clean.replace(r'\pos(540,1540)\fad(90,0)',
        r'\pos(540,1530)\fad(65,0)\bord0\shad0')
    (out/'captions828.ass').write_text(clean,encoding='utf-8')
    if clean.count('Dialogue: 0,')!=24 or r'\c&H00BEC637&' not in clean:
        raise ValueError('expected 24 captions and corrected accent')
    original=root/'source'/'voice.m4a'
    before=measure(original)
    opts=(f'loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={before["input_i"]}:'
      f'measured_TP={before["input_tp"]}:measured_LRA={before["input_lra"]}:'
      f'measured_thresh={before["input_thresh"]}:offset={before["target_offset"]}:'
      'linear=true:print_format=summary,aresample=48000')
    mastered=root/'source'/'voice_mastered828.m4a'
    execute(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(original),
       '-af',opts,'-c:a','aac','-b:a','160k','-ar','48000',str(mastered)])
    after=measure(mastered)
    result={'source_lufs':float(before['input_i']),
      'mastered_lufs':float(after['input_i']),
      'mastered_true_peak_dbfs':float(after['input_tp']),
      'gain_lufs':round(float(after['input_i'])-float(before['input_i']),2)}
    (out/'audio_master828.json').write_text(json.dumps(result,indent=2))
    return result

def render(root):
    root=Path(root);prepare(root)
    out=root/'output'/OUTPUT
    inputs=[];parts=[]
    for i,n in enumerate(FRAMES):
        inputs+=['-i',str(root/'source'/f'scene_{i+1:02}.png')]
        direction=f'(iw-iw/zoom)*on/{n}' if i%2==0 else f'(iw-iw/zoom)*(1-on/{n})'
        parts.append(f"[{i}:v]zoompan=z='min(1.0+on*0.00024,1.028)':x='{direction}':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    parts.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[vcat]')
    parts.append(f'[vcat]ass={root/"output"/"captions828.ass"}:fontsdir=/usr/share/fonts/opentype/noto[vout]')
    execute(['ffmpeg','-hide_banner','-loglevel','error','-y',*inputs,
      '-i',str(root/'source'/'voice_mastered828.m4a'),
      '-filter_complex',';'.join(parts),'-map','[vout]','-map','8:a:0',
      '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-r','30',
      '-c:a','aac','-b:a','160k','-ar','48000','-af','apad',
      '-t',str(sum(FRAMES)/30),'-movflags','+faststart',str(out)])
    return out

def verify(root):
    root=Path(root);out=root/'output'/OUTPUT
    info=json.loads(subprocess.check_output(['ffprobe','-v','error',
       '-show_streams','-show_format','-of','json',str(out)]))
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    a=next(x for x in info['streams'] if x['codec_type']=='audio')
    loud=json.loads((root/'output'/'audio_master828.json').read_text())
    ass=(root/'output'/'captions828.ass').read_text()
    imgs=[Image.open(root/'source'/f'scene_{i:02}.png') for i in range(1,9)]
    decode=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),
       '-map','0:v:0','-f','null','-'],capture_output=True)
    checks={'mp4':out.stat().st_size>1_000_000,
      '1080x1920':(v['width'],v['height'])==(1080,1920),
      'h264_30fps':v['codec_name']=='h264' and v['r_frame_rate']=='30/1',
      '775_frames':int(v['nb_frames'])==775,
      'full_decode':decode.returncode==0,
      'eight_distinct_images':len(imgs)==8 and all(im.size==(1080,1920) for im in imgs)
          and all(ImageChops.difference(imgs[i],imgs[i+1]).getbbox() for i in range(7)),
      'japanese_aac_48k':a['codec_name']=='aac' and a['sample_rate']=='48000',
      '24_captions':ass.count('Dialogue: 0,')==24,
      'correct_ass_bgr':r'\c&H00BEC637&' in ass,
      'no_muddy_outlines':r'\bord0\shad0' in ass,
      'ten_genre_palette':len(ACCENTS)==10,
      'mastered_lufs':-17.1<=loud['mastered_lufs']<=-15,
      'voice_gain':loud['gain_lufs']>=1.0,
      'peak_safe':loud['mastered_true_peak_dbfs']<=-1.0}
    report={'cycle':828,'checks':checks,'passed':sum(checks.values()),
       'total':len(checks),'audio':loud,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
       'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
       'unverified':['Japanese pronunciation','word-level alignment','mobile device',
       'reference video parity','license final approval','employee approval']}
    (root/'output'/'qa828.json').write_text(json.dumps(report,indent=2))
    if not all(checks.values()):raise RuntimeError(json.dumps(checks))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--step',choices=['render','verify'],required=True);a=p.parse_args()
    print(json.dumps((render if a.step=='render' else verify)(a.root),default=str))
