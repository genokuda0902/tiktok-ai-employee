"""Review-only media gate. Refuse to claim Japanese narration based on an audio track."""
from pathlib import Path
import subprocess

def check_audio(media: Path, narration_verified: bool=False, captions_synced: bool=False, rights_approved: bool=False, human_approved: bool=False):
    if not media.is_file(): raise FileNotFoundError(media)
    probe=subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',str(media)],capture_output=True,text=True,check=True)
    return {'audio_track_present':bool(probe.stdout.strip()),'japanese_narration_verified':narration_verified,'publication_approved':bool(probe.stdout.strip()) and narration_verified and captions_synced and rights_approved and human_approved}
