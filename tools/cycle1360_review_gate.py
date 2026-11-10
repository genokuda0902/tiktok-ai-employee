"""Safe review-only render gate for synthetic Excel demos; no publishing."""
from pathlib import Path
import json, subprocess

def inspect_video(path: Path):
    probe = subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height','-show_entries','format=duration','-of','json',str(path)],check=True,capture_output=True,text=True)
    info=json.loads(probe.stdout)
    video=[s for s in info['streams'] if s['codec_type']=='video']
    audio=[s for s in info['streams'] if s['codec_type']=='audio']
    return {'native_vertical_1080': bool(video and video[0].get('width')==1080 and video[0].get('height')==1920),'has_audio':bool(audio),'duration':float(info['format']['duration'])}

def publication_allowed(meta):
    required=('narration_verified','spoken_caption_sync_verified','asset_rights_verified','human_approved')
    return all(meta.get(k) is True for k in required)

if __name__=='__main__':
    import sys
    report=inspect_video(Path(sys.argv[1]));report['posting_allowed']=False
    print(json.dumps(report,ensure_ascii=False))
