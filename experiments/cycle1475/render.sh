#!/usr/bin/env bash
set -euo pipefail
INPUT="${1:?input mp4}"; OUTPUT="${2:?output mp4}"
FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
ffmpeg -hide_banner -loglevel error -y -i "$INPUT" -vf "drawbox=x=45:y=1480:w=990:h=115:color=0x091225@0.98:t=fill,drawtext=fontfile=$FONT:text='要点表示・音声の書き起こしではありません':fontcolor=white:fontsize=33:x=70:y=1503,drawtext=fontfile=$FONT:text='字幕同期・素材権利は未確認／公開前に要審査':fontcolor=0xFFD58B:fontsize=27:x=70:y=1550" -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUTPUT"
