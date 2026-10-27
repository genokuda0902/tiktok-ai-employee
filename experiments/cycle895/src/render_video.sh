#!/usr/bin/env bash
set -euo pipefail
SOURCE="$1"; DIR="$2"; OUT="$3"
ffmpeg -hide_banner -loglevel error -y -i "$SOURCE" \
  -loop 1 -framerate 30 -i "$DIR/document_state_1.png" \
  -loop 1 -framerate 30 -i "$DIR/document_state_2.png" \
  -loop 1 -framerate 30 -i "$DIR/document_state_3.png" \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,6.20,7.08)'[a];[a][2:v]overlay=0:0:enable='between(t,7.09,7.97)'[b];[b][3:v]overlay=0:0:enable='between(t,7.98,8.85)',format=yuv420p[v]" \
  -map "[v]" -map 0:a:0 -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -r 30 -frames:v 691 -c:a copy -movflags +faststart "$OUT"
