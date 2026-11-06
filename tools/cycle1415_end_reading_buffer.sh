#!/usr/bin/env bash
set -euo pipefail
INPUT="${1:?input MP4}"; OUTPUT="${2:?output MP4}"
# Reusable end-reading buffer: 0.7s visual freeze plus audio silence.
ffmpeg -hide_banner -loglevel error -y -i "$INPUT" \
  -filter_complex '[0:v]tpad=stop_mode=clone:stop_duration=0.7[v];[0:a]apad=pad_dur=0.7[a]' \
  -map '[v]' -map '[a]' -c:v libx264 -preset veryfast -crf 19 \
  -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart "$OUTPUT"
ffmpeg -v error -i "$OUTPUT" -f null -
ffprobe -v error -show_entries stream=codec_name,width,height -show_entries format=duration -of json "$OUTPUT"
