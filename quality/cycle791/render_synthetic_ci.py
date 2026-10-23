"""CI-only full-duration synthetic-tone technical video (NOT original video)."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from render_summary_captions import build_ass,validate

def command(cmd,check=True):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if check and p.returncode:
        raise RuntimeError(' '.join(cmd)+'\n'+p.stderr[-3500:])
    return p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    ap.add_argument('--config',required=True)
    a=ap.parse_args()
    if not a.output.endswith('_SYNTHETIC_TONE_REVIEW_ONLY.mp4'):
        raise ValueError('Synthetic output filename must explicitly state its limitation')
    cfg=json.loads(Path(a.config).read_text(encoding='utf-8'))
    validate(cfg)
    import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    ass=out.with_suffix('.ass');ass.write_text(build_ass(cfg),encoding='utf-8')
    duration=float(cfg['duration_seconds'])
    cmd=[ffmpeg,'-hide_banner','-loglevel','error','-y',
         '-f','lavfi','-i','color=c=0x082437:s=1080x1920:r=30:d=23.8',
         '-f','lavfi','-i',f'sine=frequency=392:sample_rate=48000:duration={duration}',
         '-vf',f'ass={ass}', '-c:v','libx264',
         '-preset','ultrafast','-crf','31','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','96k','-movflags','+faststart',str(out)]
    command(cmd)
    p=command([ffmpeg,'-hide_banner','-i',str(out)],check=False)
    meta=p.stderr
    if not all(x in meta for x in ('Video: h264','1080x1920','30 fps','Audio: aac')):
        raise RuntimeError('Synthetic video format mismatch:\n'+meta[-2200:])
    m=re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)',meta)
    if not m:raise RuntimeError('Duration missing')
    actual=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
    if abs(actual-duration)>.11:
        raise RuntimeError(f'Duration mismatch {actual} vs {duration}')
    command([ffmpeg,'-v','error','-xerror','-i',str(out),'-f','null','-'])
    report={'cycle':791,'kind':'synthetic_tone_not_Japanese_narration',
            'not_the_23_843_second_original_user_video':True,
            'duration_seconds':actual,'width':1080,'height':1920,
            'video_codec':'h264','audio_codec':'aac','audio':'synthetic_tone',
            'japanese_caption_cues':len(cfg['cues']),
            'full_decode':'PASS','publication_approved':False,'rights_reviewed':False,
            'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
    out.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
