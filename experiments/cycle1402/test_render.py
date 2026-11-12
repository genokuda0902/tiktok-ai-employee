import json, subprocess
from pathlib import Path
p=Path(__file__).parent
m=json.loads((p/'manifest.json').read_text())
assert not m['publication_approved'] and not m['japanese_narration'] and not m['speech_synced_captions']
srt=(p/'scene_captions.srt').read_text()
assert srt.count('-->')==5
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'cycle1402_REVIEW_ONLY.mp4')]))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==(1080,1920)
assert abs(float(probe['format']['duration'])-20)<0.1
assert not any(s['codec_type']=='audio' for s in probe['streams'])
subprocess.run(['ffmpeg','-v','error','-i',str(p/'cycle1402_REVIEW_ONLY.mp4'),'-f','null','-'],check=True)
print('PASS review-only video; narration explicitly absent')
