"""Minimal FFmpeg stderr metadata adapter for zero-apt CI; not a full ffprobe replacement.
Only supports the two read-only query formats used by cycle790.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

def metadata(path):
    if not Path(path).is_file():raise FileNotFoundError(path)
    r=subprocess.run(['ffmpeg','-hide_banner','-i',str(path)],capture_output=True,text=True)
    s=r.stderr
    d=re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)',s)
    v=re.search(r'Video:\s*([\w]+)[^\n]*?(\d{3,5})x(\d{3,5})[^\n]*?(\d+(?:\.\d+)?)\s*fps',s)
    a=re.search(r'Audio:\s*([\w]+)',s)
    if not (d and v and a):raise RuntimeError('Cannot extract H.264/AAC metadata from FFmpeg')
    dur=int(d[1])*3600+int(d[2])*60+float(d[3]);fps=float(v[4]);num=round(dur*fps)
    return {'format':{'duration':str(dur)},'streams':[
        {'codec_type':'video','codec_name':v[1],'width':int(v[2]),'height':int(v[3]),'nb_frames':str(num),'r_frame_rate':f'{round(fps)}/1'},
        {'codec_type':'audio','codec_name':a[1]}]}

def main(argv):
    data=metadata(argv[-1]);video=data['streams'][0]
    if 'csv=p=0' in argv:
        print(f"{video['width']},{video['height']},{video['r_frame_rate']}")
    elif 'json' in argv:
        print(json.dumps(data))
    else:
        raise ValueError('Only cycle790 JSON/CSV read-only queries supported')
if __name__=='__main__':main(sys.argv[1:])
