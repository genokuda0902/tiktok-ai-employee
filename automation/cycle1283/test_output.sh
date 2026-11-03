#!/usr/bin/env bash
set -euo pipefail
file="$1"
[ -s "$file" ]
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$file" | grep -qx '1080,1920'
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$file" | grep -qx 'aac'
ffmpeg -v error -xerror -i "$file" -f null -
echo PASS
