"""Review-only: hook and pacing overlay for synthetic approved-source videos."""
from pathlib import Path
import subprocess, json, sys

def filtergraph(duration=12):
    if duration <= 0: raise ValueError("duration must be positive")
    return ("drawbox=x=0:y=1220:w='iw*min(t/12,1)':h=12:color=0x22d3ee@0.95:t=fill,"
            "drawbox=x=30:y=80:w=660:h=145:color=0x10243b@0.94:t=fill:enable='lt(t,1.5)',"
            "drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:"
            "text='SUM関数を12秒で理解':fontcolor=white:fontsize=45:x=55:y=124:enable='lt(t,1.5)',"
            "drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:"
            "text='REVIEW ONLY / 日本語音声なし':fontcolor=white:fontsize=22:"
            "box=1:boxcolor=0x7f1d1d@0.95:boxborderw=7:x=18:y=18")

def render(source,dest):
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-vf',filtergraph(),'-c:v','libx264','-preset','ultrafast','-crf','24','-c:a','copy','-movflags','+faststart',str(dest)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))

if __name__=='__main__':
    source=Path(sys.argv[1]); dest=Path(sys.argv[2]); result=render(source,dest)
    dest.with_suffix('.probe.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
