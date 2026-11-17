"""Fail-closed audio and publication QA, shared across all video genres."""
import json
import subprocess

def inspect(path, japanese_narration_verified=False, captions_synced=False, assets_approved=False, human_approved=False):
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))
    streams=probe.get('streams',[])
    video=next((s for s in streams if s.get('codec_type')=='video'),None)
    audio=next((s for s in streams if s.get('codec_type')=='audio'),None)
    duration=float(probe.get('format',{}).get('duration',0))
    issues=[]
    if not video or video.get('width',0)<720 or video.get('height',0)<1280: issues.append('video_resolution')
    if duration<=0: issues.append('duration')
    if not audio: issues.append('audio_missing')
    if not japanese_narration_verified: issues.append('japanese_narration_unverified')
    if not captions_synced: issues.append('caption_sync_unverified')
    if not assets_approved: issues.append('asset_rights_unapproved')
    if not human_approved: issues.append('human_approval_missing')
    return {'duration':duration,'width':video.get('width') if video else None,'height':video.get('height') if video else None,'audio_codec':audio.get('codec_name') if audio else None,'issues':issues,'posting_allowed':not issues,'status':'APPROVED' if not issues else 'PUBLICATION_NOT_APPROVED'}
