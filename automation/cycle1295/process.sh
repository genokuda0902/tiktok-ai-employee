#!/usr/bin/env bash
set -euo pipefail
src="$1"; out="$2"
ffmpeg -hide_banner -loglevel error -y -i "$src" -map 0:v:0 -map 0:a:0 -map_chapters 0 -c copy -movflags +faststart "$out"
python3 "$(dirname "$0")/test_output.py" "$src" "$out"
