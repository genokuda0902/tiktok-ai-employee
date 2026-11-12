"""Fail-closed media QA: audio stream is not evidence of Japanese narration."""
import json
import subprocess

def inspect(path):
    result = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
    data=json.loads(result.stdout)
    video=next((s for s in data['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    return {'video':video is not None,'width':video.get('width',0) if video else 0,'height':video.get('height',0) if video else 0,'audio_stream':audio is not None}

def approved_for_posting(metadata):
    return all(metadata.get(key) is True for key in ('japanese_narration_verified','timed_captions_verified','assets_rights_approved','employee_approved'))
