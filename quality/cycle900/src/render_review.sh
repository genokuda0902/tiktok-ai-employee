#!/usr/bin/env bash
set -euo pipefail
# Run: bash render_review.sh INPUT_PRIVATE_MP4 OUTPUT_PRIVATE_MP4 OVERLAY_DIRECTORY
# Never uploads, posts, merges or exposes private source media.
SOURCE="$1"; OUTPUT="$2"; OVERLAYS="$3"
mkdir -p "$(dirname "$OUTPUT")"
FRAMES="$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=noprint_wrappers=1:nokey=1 "$SOURCE")"
[[ "$FRAMES" =~ ^[0-9]+$ ]] || { echo "ERROR: source frame count unavailable" >&2; exit 2; }
ffmpeg -hide_banner -loglevel error -y -i "$SOURCE" \
  -loop 1 -framerate 30 -i "$OVERLAYS/focus_0.png" \
  -loop 1 -framerate 30 -i "$OVERLAYS/focus_1.png" \
  -loop 1 -framerate 30 -i "$OVERLAYS/focus_2.png" \
  -filter_complex "[0:v][1:v]overlay=x=70:y=350:enable='between(t,11.60,12.53)':eof_action=pass[v1];[v1][2:v]overlay=x=70:y=350:enable='between(t,12.54,13.49)':eof_action=pass[v2];[v2][3:v]overlay=x=70:y=350:enable='between(t,13.50,14.49)':eof_action=pass,format=yuv420p[v]" \
  -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 19 \
  -r 30 -c:a copy -movflags +faststart -frames:v "$FRAMES" "$OUTPUT"
