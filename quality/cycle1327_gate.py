"""Shared review gate: silent MP4s cannot pass publication QA."""
import json
import subprocess


def inspect(path):
    result = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
    info = json.loads(result.stdout)
    streams = info.get('streams', [])
    videos = [s for s in streams if s.get('codec_type') == 'video']
    audio = [s for s in streams if s.get('codec_type') == 'audio']
    errors = []
    if not videos: errors.append('missing_video')
    elif int(videos[0].get('width',0)) < 1080 or int(videos[0].get('height',0)) < 1920: errors.append('low_resolution')
    if not audio: errors.append('missing_japanese_narration_audio')
    # Audio existence alone does NOT prove speech, language, or synchronization.
    return {'review_only': True, 'publication_approved': False, 'errors': errors, 'audio_present': bool(audio)}
