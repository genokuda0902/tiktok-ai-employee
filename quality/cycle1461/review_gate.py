"""Fail-closed review of a locally generated MP4; no upload/posting."""
import json, subprocess, sys
from pathlib import Path

def inspect(path):
    p=Path(path)
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
    streams=data['streams']
    videos=[s for s in streams if s['codec_type']=='video']
    audios=[s for s in streams if s['codec_type']=='audio']
    return {'video_present':bool(videos),'width':videos[0].get('width') if videos else None,'height':videos[0].get('height') if videos else None,'audio_present':bool(audios),'japanese_narration_verified':False,'speech_synced_captions_verified':False,'posting_allowed':False,'status':'PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
