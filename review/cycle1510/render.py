"""Cycle1510 review-only synthetic spreadsheet footage focus overlay; no narration claim."""
import argparse
import subprocess

def focus_filter():
    return ("drawbox=x=64:y=930:w=952:h=176:color=0x071a2e@0.86:t=fill:enable='between(t,3,6)',"
            "drawbox=x=64:y=930:w=10:h=176:color=0x22d3ee:t=fill:enable='between(t,3,6)',"
            "drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:"
            "text='ここに注目：合計の計算':fontcolor=white:fontsize=48:"
            "x=106:y=982:enable='between(t,3,6)'")

def render(src, dst):
    cmd=['ffmpeg','-hide_banner','-y','-i',str(src),'-vf',focus_filter()+',scale=1080:1920:flags=lanczos,fps=24,format=yuv420p',
         '-map','0:v:0','-map','0:a:0?','-c:v','libx264','-preset','veryfast','-crf','22','-c:a','aac','-b:a','128k','-movflags','+faststart',str(dst)]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return cmd

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');a=p.parse_args()
    render(a.source,a.output)
