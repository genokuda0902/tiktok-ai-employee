#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/render.py"
ffmpeg -y -loglevel error -i "$DIR/cycle1392_base.mp4" -vf 'scale=1080:1920:flags=lanczos,fade=t=in:st=0:d=0.3,fade=t=out:st=11.7:d=0.3' -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -movflags +faststart "$DIR/cycle1392_REVIEW_ONLY.mp4"
python3 "$DIR/test_render.py" "$DIR/cycle1392_REVIEW_ONLY.mp4"
