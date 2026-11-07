#!/usr/bin/env bash
set -euo pipefail
FILE="${1:?mp4}"
ffmpeg -v error -i "$FILE" -f null -
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$FILE" | grep -qx '1080,1920'
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=nw=1:nk=1 "$FILE" | grep -qx 'aac'
