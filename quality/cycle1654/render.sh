#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?input mp4 required}"; OUT="${2:?output mp4 required}"
FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
ffmpeg -hide_banner -loglevel warning -y -i "$SRC" -vf "drawbox=x=80:y=1640:w=920:h=12:color=white@0.2:t=fill,drawbox=x=80:y=1640:w='min(920,920*t/12)':h=12:color=0x34d399:t=fill,drawtext=fontfile=$FONT:text='STEP 1 / 4':fontcolor=white:fontsize=34:x=85:y=1670:enable='lt(t,3)',drawtext=fontfile=$FONT:text='STEP 2 / 4':fontcolor=white:fontsize=34:x=85:y=1670:enable='between(t,3,5.999)',drawtext=fontfile=$FONT:text='STEP 3 / 4':fontcolor=white:fontsize=34:x=85:y=1670:enable='between(t,6,8.999)',drawtext=fontfile=$FONT:text='STEP 4 / 4':fontcolor=white:fontsize=34:x=85:y=1670:enable='gte(t,9)'" -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -an -movflags +faststart "$OUT"
