#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

p = Path('output/AI時短ラボ_01_完成版.mp4')
if not p.exists() or p.stat().st_size < 10000:
    raise SystemExit('MP4 missing or too small')
raw = subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)], text=True)
info = json.loads(raw)
streams = info.get('streams', [])
videos = [s for s in streams if s.get('codec_type') == 'video']
audios = [s for s in streams if s.get('codec_type') == 'audio']
errors = []
if not videos: errors.append('no video stream')
if not audios: errors.append('no audio stream')
if videos and (videos[0].get('width') != 1080 or videos[0].get('height') != 1920): errors.append('not 1080x1920')
duration = float(info.get('format', {}).get('duration', 0) or 0)
if duration < 10: errors.append('duration too short')
report = {'technical_pass': not errors, 'errors': errors, 'duration_sec': duration, 'video_codec': videos[0].get('codec_name') if videos else None, 'audio_codec': audios[0].get('codec_name') if audios else None, 'has_audio': bool(audios), 'resolution': f"{videos[0].get('width')}x{videos[0].get('height')}" if videos else None, 'note': 'Technical QA only; not a content/viral quality score.'}
Path('output/qa_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
if errors: raise SystemExit('Technical QA failed: ' + ', '.join(errors))
