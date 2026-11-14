"""Review-only burn-in Japanese captions. Requires rights-cleared source, ffmpeg and libass."""
from pathlib import Path
import argparse, subprocess, json

def render(source: Path, captions: Path, output: Path):
    source, captions, output = map(Path, (source,captions,output))
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError('Missing source or captions; do not substitute private assets')
    output.parent.mkdir(parents=True, exist_ok=True)
    style='FontName=Noto Sans CJK JP,FontSize=19,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=175'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'subtitles={captions.resolve()}:force_style={style}','-map','0:v:0','-map','0:s:0','-c:v','libx264','-preset','ultrafast','-crf','24','-pix_fmt','yuv420p','-c:s','mov_text','-movflags','+faststart',str(output)],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height','-of','json',str(output)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert (video['width'],video['height'])==(1080,1920)
    assert any(s['codec_type']=='subtitle' for s in probe['streams'])
    assert not any(s['codec_type']=='audio' for s in probe['streams'])
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    return probe

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--captions',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    print(json.dumps(render(Path(a.source),Path(a.captions),Path(a.output)),ensure_ascii=False))
