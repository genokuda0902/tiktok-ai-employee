"""Zero-cost reusable vertical video slide progress overlay."""
import subprocess
from pathlib import Path
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def filtergraph(sections=5,duration=22.625):
    if sections<1 or duration<=0: raise ValueError('invalid section configuration')
    f=['drawbox=x=78:y=145:w=924:h=9:color=white@0.20:t=fill']
    for i in range(sections):
        start=i*duration/sections; end=(i+1)*duration/sections
        x=78+i*924/sections
        f.append(f"drawbox=x={int(x)}:y=145:w={int(924/sections)-4}:h=9:color=white@0.94:t=fill:enable='between(t,{start:.3f},{end:.3f})'")
        f.append(f"drawtext=fontfile={FONT}:text='{i+1:02d} / {sections:02d}':fontsize=29:fontcolor=white:x=82:y=175:box=1:boxcolor=black@0.45:boxborderw=12:enable='between(t,{start:.3f},{end:.3f})'")
    return ','.join(f)
def render(src,out):
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nk=1:nw=1',str(src)],text=True).strip())
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-vf',filtergraph(duration=duration),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)],check=True)
if __name__=='__main__':
    import sys
    render(Path(sys.argv[1]),Path(sys.argv[2]))
