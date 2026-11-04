"""Review-only opening hook overlay; no private assets or auto-posting."""
from pathlib import Path
import subprocess
import sys
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def hook_filter(duration=2.8):
    if not 0 < duration <= 5:
        raise ValueError('hook duration must be within 0-5 seconds')
    e=f'between(t,0,{duration})'
    return (f"drawbox=x=60:y=260:w=960:h=350:color=0x07172b@0.94:t=fill:enable='{e}',"
            f"drawbox=x=60:y=260:w=16:h=350:color=0x00d6df:t=fill:enable='{e}',"
            f"drawtext=fontfile={FONT}:text='AIの回答、そのまま使う？':fontsize=61:fontcolor=white:x=(w-text_w)/2:y=345:enable='{e}',"
            f"drawtext=fontfile={FONT}:text='3つの確認でミスを防ぐ':fontsize=49:fontcolor=0x8ef9ff:x=(w-text_w)/2:y=465:enable='{e}'")
def render(source,target):
    source,target=Path(source),Path(target)
    if not source.is_file(): raise FileNotFoundError(source)
    target.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',hook_filter(),'-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)],check=True)
if __name__=='__main__':
    render(sys.argv[1],sys.argv[2])
