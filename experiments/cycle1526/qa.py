"""Fail-closed publication QA for any of the 10 genres."""
import json, subprocess
from pathlib import Path

def probe(path):
 p=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
 return json.loads(p.stdout)

def evaluate(meta, *, narration_verified=False, captions_synced=False, assets_approved=False, human_approved=False):
 streams=meta.get('streams',[])
 videos=[s for s in streams if s.get('codec_type')=='video']
 audios=[s for s in streams if s.get('codec_type')=='audio']
 checks={'video_present':bool(videos),'vertical':bool(videos and videos[0].get('height',0)>videos[0].get('width',0)),
 'audio_track_present':bool(audios),'japanese_narration_verified':bool(audios and narration_verified),
 'speech_synced_captions_verified':bool(audios and narration_verified and captions_synced),
 'assets_approved':assets_approved,'human_approved':human_approved}
 return {'approved':all(checks.values()),'checks':checks}
if __name__=='__main__':
 import sys
 p=Path(sys.argv[1]); m=probe(p); print(json.dumps({'probe':m,'qa':evaluate(m)},ensure_ascii=False,indent=2))
