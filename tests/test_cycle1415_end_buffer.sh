#!/usr/bin/env bash
set -euo pipefail
INPUT="${1:?input}"; OUTPUT="${2:?output}"
bash tools/cycle1415_end_reading_buffer.sh "$INPUT" "$OUTPUT"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$OUTPUT" | grep -qx '1080,1920'
python3 - "$INPUT" "$OUTPUT" <<'PY'
import json,subprocess,sys
def duration(path):
    return float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',path]))['format']['duration'])
delta=duration(sys.argv[2])-duration(sys.argv[1])
assert 0.65 <= delta <= 0.75, delta
print('PASS: added 0.7s end reading buffer')
PY
