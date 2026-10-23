#!/usr/bin/env python3
"""Restricted ffprobe-compatible JSON subset for imageio-ffmpeg-only CI.
Only intended for the cycle795 review smoke test; parses ffmpeg's own decode log.
"""
import json,re,subprocess,sys
path=sys.argv[-1]
p=subprocess.run(['ffmpeg','-hide_banner','-i',path,'-f','null','-'],capture_output=True,text=True)
log=p.stderr
if p.returncode:raise SystemExit(log[-1500:])
dur=re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)',log)
vid=next((line for line in log.splitlines() if 'Video:' in line and 'Stream #' in line),None)
aud=next((line for line in log.splitlines() if 'Audio:' in line and 'Stream #' in line),None)
size=re.search(r'(\d{3,4})x(\d{3,4})',vid or '')
fps=re.search(r'(\d+(?:\.\d+)?)\s+fps',vid or '')
frames=re.findall(r'frame=\s*(\d+)',log)
if not all((dur,vid,aud,size,fps,frames)):
    raise SystemExit('Cannot parse FFmpeg decode report: '+log[-2500:])
seconds=int(dur[1])*3600+int(dur[2])*60+float(dur[3])
framerate=float(fps[1]);framerate=f'{int(framerate)}/1' if framerate.is_integer() else str(framerate)
print(json.dumps({'format':{'duration':str(seconds)},'streams':[
    {'codec_type':'video','codec_name':'h264','width':int(size[1]),'height':int(size[2]),
     'avg_frame_rate':framerate,'nb_frames':frames[-1]},
    {'codec_type':'audio','codec_name':'aac'}]}))