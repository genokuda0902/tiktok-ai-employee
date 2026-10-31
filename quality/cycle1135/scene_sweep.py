"""Original decorative scene-sweep overlay for 1080x1920 review videos.
Never changes the inherited audio or captions; not a speech alignment check.
"""
from pathlib import Path
from PIL import Image
import subprocess
PALETTES={'ai_workflow':'#5ce0d1','business':'#6aaeff','finance':'#e3bf75','health':'#73d6a7','beauty':'#ef9bbd','travel':'#77d4ed','education':'#a79bf4','lifestyle':'#f1ba88','technology':'#8bd5fa','entertainment':'#e59be7'}
CUTS=[2.8,5.6,8.4,11.2,14.,16.8,19.6]
def make_sweep(path,color='#5ce0d1',width=600,height=64):
    rgb=tuple(int(color[i:i+2],16) for i in (1,3,5))
    im=Image.new('RGBA',(width,height))
    px=im.load()
    for y in range(height):
        fy=max(0,1-abs(y-(height-1)/2)/(height/2))**1.8
        for x in range(width):
            fx=max(0,1-abs(x-(width-1)/2)/(width/2))**1.4
            px[x,y]=(*rgb,round(100*fx*fy))
    im.save(path)
    return im
def overlay_expr(cuts=CUTS,duration=.22,width=1080,stripe=600):
    active='+'.join(f'between(t,{c:.2f},{c+duration:.2f})' for c in cuts)
    return f'if(gt({active},0),-{stripe}+mod(t,2.8)*{(width+stripe)/duration:.5f},NAN)'
def render(src,dest,stripe):
    filt=f"[0:v][1:v]overlay=x='{overlay_expr()}':y=365:eval=frame:shortest=1:format=auto,format=yuv420p[v]"
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-loop','1','-framerate','30','-i',str(stripe),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-r','30','-c:a','copy','-movflags','+faststart',str(dest)],check=True)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');p.add_argument('--genre',choices=PALETTES,default='ai_workflow')
    a=p.parse_args();s=Path(a.output).with_suffix('.sweep.png');make_sweep(s,PALETTES[a.genre]);render(a.input,a.output,s)
