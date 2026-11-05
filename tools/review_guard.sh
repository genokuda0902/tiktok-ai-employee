#!/usr/bin/env bash
set -euo pipefail
INPUT="${1:?input MP4 required}"
OUTPUT="${2:?output MP4 required}"
FONT="${FONT:-/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc}"
ffmpeg -hide_banner -loglevel error -y -i "$INPUT" \
  -vf "drawbox=x=0:y=1810:w=iw:h=80:color=black@0.82:t=fill,drawtext=fontfile=${FONT}:text='検証用サンプル  ／  社員承認前・投稿禁止':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=1832" \
  -map 0:v:0 -map 0:a:0 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUTPUT"
