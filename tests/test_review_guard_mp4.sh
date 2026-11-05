#!/usr/bin/env bash
set -euo pipefail
VIDEO="${1:?MP4 path required}"
test -s "$VIDEO"
test "$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$VIDEO")" = "1080"
test "$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VIDEO")" = "1920"
test "$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$VIDEO")" = "aac"
ffmpeg -v error -i "$VIDEO" -f null -
echo "PASS: dimension, AAC and full decode"
