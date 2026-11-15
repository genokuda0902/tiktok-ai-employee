"""Review-only MP4 validation; no publication approval implied."""
import json
import subprocess
import sys


def inspect(path):
    raw = subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)], text=True)
    info = json.loads(raw)
    streams = info['streams']
    video = next((s for s in streams if s['codec_type']=='video'), None)
    audio = next((s for s in streams if s['codec_type']=='audio'), None)
    errors = []
    if not video or video.get('width',0)*16 != video.get('height',0)*9:
        errors.append('vertical 9:16 video required')
    if not audio:
        errors.append('Japanese narration absent: no audio stream')
    if float(info.get('format',{}).get('duration',0)) <= 0:
        errors.append('duration missing')
    return {'posting_allowed':False,'review_only':True,'errors':errors,'audio_present':bool(audio)}

if __name__=='__main__':
    print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
