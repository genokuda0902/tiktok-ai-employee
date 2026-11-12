import json, subprocess
from pathlib import Path
p=Path(__file__).parent
m=json.loads((p/'manifest.json').read_text())
assert m['publication_approved'] is False
assert m['japanese_narration'] is False
assert m['speech_synced_captions'] is False
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'cycle1401_REVIEW_ONLY.mp4')]))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==(1080,1920)
assert 9.9<float(probe['format']['duration'])<10.1
assert not any(s['codec_type']=='audio' for s in probe['streams'])
subprocess.run(['ffmpeg','-v','error','-i',str(p/'cycle1401_REVIEW_ONLY.mp4'),'-f','null','-'],check=True)
print('PASS')
