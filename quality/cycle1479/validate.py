"""Review-only MP4 QA. Fails closed if narration is missing."""
import json, subprocess, sys
from pathlib import Path

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def check(path):
    data=probe(path)
    streams=data['streams']
    video=next((s for s in streams if s['codec_type']=='video'),None)
    audio=next((s for s in streams if s['codec_type']=='audio'),None)
    issues=[]
    if not video or video.get('width',0)<720 or video.get('height',0)<1280: issues.append('resolution')
    if not audio: issues.append('japanese_narration_missing')
    if not Path(path).with_suffix('.srt').exists(): issues.append('subtitle_missing')
    # Human rights/privacy/employee approval cannot be inferred from technical metadata.
    issues.append('manual_approval_required')
    return {'publication_approved':False,'issues':issues}

if __name__=='__main__':
    print(json.dumps(check(sys.argv[1]),ensure_ascii=False,indent=2))
