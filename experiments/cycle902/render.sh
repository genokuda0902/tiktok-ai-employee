#!/usr/bin/env bash
set -euo pipefail
# Usage: bash render.sh PRIVATE_SOURCE_MP4 PRIVATE_OUTPUT_MP4 PNG_DIR
# Local only; NEVER publish source or finished media to public GitHub.
SOURCE="$1"; OUTPUT="$2"; PNG_DIR="$3"
mkdir -p "$(dirname "$OUTPUT")"
FRAMES="$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=noprint_wrappers=1:nokey=1 "$SOURCE")"
[[ "$FRAMES" =~ ^[0-9]+$ ]] || exit 2
ffmpeg -hide_banner -loglevel error -y -i "$SOURCE" \
 -loop 1 -framerate 30 -i "$PNG_DIR/stage_0.png" \
 -loop 1 -framerate 30 -i "$PNG_DIR/stage_1.png" \
 -loop 1 -framerate 30 -i "$PNG_DIR/stage_2.png" \
 -filter_complex "[0:v][1:v]overlay=x=70:y=350:enable='gte(t,2.9)*lt(t,3.83)':eof_action=pass[v1];[v1][2:v]overlay=x=70:y=350:enable='gte(t,3.83)*lt(t,4.80)':eof_action=pass[v2];[v2][3:v]overlay=x=70:y=350:enable='gte(t,4.80)*lt(t,5.80)':eof_action=pass,format=yuv420p[v]" \
 -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 19 -r 30 \
 -c:a copy -movflags +faststart -frames:v "$FRAMES" "$OUTPUT"
