#!/usr/bin/env bash
set -euo pipefail
input="${1:?input mp4 required}"
output="${2:?output mp4 required}"
ffmpeg -hide_banner -loglevel error -y -i "$input" -map 0:v:0 -map 0:a:0 -map 0:s? -vf 'deband=1thr=0.006:2thr=0.006:3thr=0.006:4thr=0.006:range=12:blur=1' -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a copy -c:s copy -movflags +faststart "$output"
