"""cycle791: render scene-summary captions in reserved mobile-safe band.
NOT an ASR transcript, NOT proof of media rights, NOT publication authorization.
Uses free FFmpeg/libass and Noto Sans CJK JP.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ('ai_productivity','finance','career','business','education',
          'lifestyle','science','travel','health','entertainment')
FPS=30
WIDTH,HEIGHT=1080,1920

def validate(config):
    if (config.get('mode') != 'review_only' or
            config.get('publication_approved') is not False or
            config.get('rights_reviewed') is not False):
        raise ValueError('Fail closed: human approval and rights review required')
    if config.get('genre') not in GENRES:
        raise ValueError('Unsupported genre')
    if config.get('canvas') != [WIDTH,HEIGHT] or config.get('fps') != FPS:
        raise ValueError('Invalid portrait canvas or fps')
    if config.get('subtitle_kind') != 'scene_summary_not_verified_transcript':
        raise ValueError('Do not claim these captions are verified narration')
    safe=config.get('safe_area',{})
    if (safe.get('top_px'),safe.get('bottom_px'),safe.get('left_px'),safe.get('right_px')) != (1350,1530,100,980):
        raise ValueError('Unsafe caption geometry')
    duration=float(config.get('duration_seconds',0))
    if not (15<=duration<=25):
        raise ValueError('Duration must be within short-video contract')
    cues=config.get('cues',[])
    if not (6<=len(cues)<=12):
        raise ValueError('Expected 6..12 scene summaries')
    last=0.0
    for cue in cues:
        a,b,s=float(cue['start']),float(cue['end']),cue['text']
        if abs(a-last)>0.002 or b-a<1.0 or b>duration+0.002:
            raise ValueError('Gap, overlap or invalid cue duration')
        if not isinstance(s,str) or not (2<=len(s)<=23) or '\\N' in s or '\n' in s:
            raise ValueError('Cue must fit one readable Japanese line')
        if any(ch in s for ch in ('{','}','\\')):
            raise ValueError('ASS markup must not be injected')
        last=b
    if abs(last-duration)>0.002:
        raise ValueError('Captions must cover full video')
    return True

def timestamp(t):
    centi=round(float(t)*100)
    h,r=divmod(centi,360000)
    m,r=divmod(r,6000)
    s,c=divmod(r,100)
    return f'{h}:{m:02d}:{s:02d}.{c:02d}'

def build_ass(cfg):
    validate(cfg)
    header='''[Script Info]
Title: cycle791 scene-summary review only
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SafeSummary,Noto Sans CJK JP,55,&H00FFFFFF,&H00FFFFFF,&H00071A25,&H78061627,1,0,0,0,100,100,0,0,3,14,0,2,100,100,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines=[]
    for cue in cfg['cues']:
        lines.append(f"Dialogue: 0,{timestamp(cue['start'])},{timestamp(cue['end'])},SafeSummary,,0,0,0,,{cue['text']}")
    return header+'\n'.join(lines)+'\n'

def run(command):
    p=subprocess.run(command,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError('command failed: '+' '.join(command)+'\n'+p.stderr[-2500:])
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries',
                           'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration',
                           '-of','json',str(path)]))

def verify_mp4(path,expected_duration):
    data=probe(path)
    streams=data['streams']
    video=next(x for x in streams if x['codec_type']=='video')
    audio=next(x for x in streams if x['codec_type']=='audio')
    assert video['codec_name']=='h264' and video['width']==WIDTH and video['height']==HEIGHT
    assert video['r_frame_rate']=='30/1' and audio['codec_name']=='aac'
    assert abs(float(data['format']['duration'])-expected_duration)<0.10
    run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'])
    return {'duration':float(data['format']['duration']),'frames':int(video.get('nb_frames') or 0),
            'width':WIDTH,'height':HEIGHT,'video_codec':'h264','audio_codec':'aac','full_decode':'PASS'}

def render(input_path,output_path,config_path,ass_path,report_path):
    cfg=json.loads(Path(config_path).read_text(encoding='utf-8'))
    ass=build_ass(cfg)
    Path(ass_path).parent.mkdir(parents=True,exist_ok=True)
    Path(ass_path).write_text(ass,encoding='utf-8')
    input_path=Path(input_path);output_path=Path(output_path)
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(input_path),
         '-vf',f'ass={ass_path}','-map','0:v:0','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output_path)])
    check=verify_mp4(output_path,float(cfg['duration_seconds']))
    check.update({'cycle':791,'status':'HUMAN_REVIEW','publication_approved':False,
                  'rights_reviewed':False,'caption_type':cfg['subtitle_kind'],
                  'cues':len(cfg['cues']),'sha256':hashlib.sha256(output_path.read_bytes()).hexdigest(),
                  'voice_transcript_verified':False,'semantic_caption_sync_verified':False,
                  'input':str(input_path),'output':str(output_path)})
    Path(report_path).parent.mkdir(parents=True,exist_ok=True)
    Path(report_path).write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf-8')
    return check

def main():
    ap=argparse.ArgumentParser()
    for name in ('input','output','config','ass','report'):
        ap.add_argument('--'+name,required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.input,a.output,a.config,a.ass,a.report),ensure_ascii=False))
if __name__=='__main__': main()
