#!/usr/bin/env bash
set -euo pipefail
IN="${1:?input mp4}"; OUT="${2:?output mp4}"
ffmpeg -hide_banner -loglevel error -y -i "$IN" -vf "drawbox=x=0:y=0:w=iw:h=ih:color=white@0.12:t=fill:enable='between(t,8.0,8.20)+between(t,16.0,16.20)',drawbox=x=0:y=0:w=iw:h=12:color=white@0.75:t=fill:enable='between(t,8.0,8.55)+between(t,16.0,16.55)'" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
