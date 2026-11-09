#!/usr/bin/env bash
set -euo pipefail
INPUT="$1"; OUTPUT="$2"
FILTER='fade=t=out:st=4.964:d=0.10,fade=t=in:st=5.064:d=0.10,fade=t=out:st=10.028:d=0.10,fade=t=in:st=10.128:d=0.10,fade=t=out:st=15.092:d=0.10,fade=t=in:st=15.192:d=0.10,fade=t=out:st=20.156:d=0.10,fade=t=in:st=20.256:d=0.10'
ffmpeg -hide_banner -loglevel error -y -i "$INPUT" -map 0:v:0 -map 0:a:0 -map 0:s? -vf "$FILTER" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a copy -c:s copy -movflags +faststart "$OUTPUT"
