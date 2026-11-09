#!/usr/bin/env bash
set -euo pipefail
input="${1:?input mp4}"; output="${2:?output mp4}"
ffmpeg -hide_banner -loglevel error -y -i "$input" -map 0 -c copy -movflags +faststart "$output"
python3 "$(dirname "$0")/test_faststart.py" "$output"
