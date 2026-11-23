#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-/tmp/cycle1657_REVIEW_ONLY.mp4}"
FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'color=c=0x101827:s=1080x1920:r=24:d=12' -vf "drawbox=x=75:y=310:w=930:h=1120:color=0x20354b:t=fill,drawbox=x=110:y=1010:w=860:h=24:color=0x29495c:t=fill,drawbox=x=110:y=1010:w='min(860\\,t*71.67)':h=24:color=0x55d6d2:t=fill,drawtext=fontfile=$FONT:text='AI動画 品質検査':fontsize=65:fontcolor=white:x=(w-text_w)/2:y=420,drawtext=fontfile=$FONT:text='音声生成 復旧待ち':fontsize=54:fontcolor=0xffce72:x=(w-text_w)/2:y=650,drawtext=fontfile=$FONT:text='字幕と発話の同期 未検証':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=830,drawtext=fontfile=$FONT:text='REVIEW ONLY':fontsize=46:fontcolor=0xff9e9e:x=(w-text_w)/2:y=1190,drawtext=fontfile=$FONT:text='社員承認前・投稿禁止':fontsize=42:fontcolor=white:x=(w-text_w)/2:y=1300" -an -c:v libx264 -preset veryfast -pix_fmt yuv420p -movflags +faststart "$OUT"
