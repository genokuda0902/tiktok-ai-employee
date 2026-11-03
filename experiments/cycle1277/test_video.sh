#!/usr/bin/env bash
set -euo pipefail
video="${1:?MP4 path}"
test -s "$video"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$video" | grep -qx '1080,1920'
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=nw=1:nk=1 "$video" | grep -qx 'aac'
ffmpeg -v error -i "$video" -f null -
echo "PASS: video/audio decoded, dimensions and AAC checked"
