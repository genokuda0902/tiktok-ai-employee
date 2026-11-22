#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-cycle1641_REVIEW_ONLY.mp4}"
FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'color=c=0x101827:s=1080x1920:r=24:d=20' -vf "drawbox=x=70:y=280:w=940:h=1320:color=0x1e293b:t=fill,drawbox=x=70:y=280:w=940:h=14:color=0x38bdf8:t=fill,drawtext=fontfile=${FONT}:text='制作レビュー / 音声復旧':fontcolor=white:fontsize=62:x=110:y=360,drawtext=fontfile=${FONT}:text='課題：日本語音声が未生成':fontcolor=0xffd166:fontsize=48:x=110:y=600:enable='between(t,0,7)',drawtext=fontfile=${FONT}:text='改善：再生成手順をGitHubへ':fontcolor=0x7dd3fc:fontsize=48:x=110:y=600:enable='between(t,7,14)',drawtext=fontfile=${FONT}:text='次回：音声と字幕を同期':fontcolor=0xa7f3d0:fontsize=48:x=110:y=600:enable='gte(t,14)',drawtext=fontfile=${FONT}:text='無音 / 公開禁止 / 社員確認前':fontcolor=white:fontsize=44:x=110:y=1320,drawbox=x=110:y=1460:w='860*t/20':h=16:color=0x38bdf8:t=fill" -an -c:v libx264 -preset ultrafast -crf 27 -pix_fmt yuv420p -movflags +faststart "$OUT"
ffmpeg -v error -i "$OUT" -f null -
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json "$OUT"
