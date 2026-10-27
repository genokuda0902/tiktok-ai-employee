#!/usr/bin/env bash
# cycle903: local-only render; never upload private MP4 to public GitHub.
set -euo pipefail
SRC="${1:?private source mp4 required}"
OUT="${2:?private output mp4 required}"
HERE="$(cd "$(dirname "$0")" && pwd)"
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
[[ -f "$FONT" ]] || { echo "Japanese font missing" >&2; exit 2; }
FRAMES="$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nw=1:nk=1 "$SRC")"
[[ "$FRAMES" == "691" ]] || { echo "Unexpected baseline; review manually" >&2; exit 3; }
FILTER="$(PYTHONPATH="$HERE" python - "$HERE" "$FONT" <<'PY'
from pathlib import Path
from mobile_readability_lens import TEXT,ffmpeg_filter
import sys
p=Path(sys.argv[1])
for i,(title,detail) in enumerate(TEXT):
    (p/f"stage_{i}_title.txt").write_text(title,encoding="utf-8")
    (p/f"stage_{i}_detail.txt").write_text(detail,encoding="utf-8")
print(ffmpeg_filter(sys.argv[2],str(p)))
PY
)"
mkdir -p "$(dirname "$OUT")"
ffmpeg -hide_banner -loglevel error -y -i "$SRC" -vf "$FILTER" -map 0:v:0 -map 0:a:0 -c:v libx264 -preset ultrafast -crf 19 -r 30 -frames:v "$FRAMES" -c:a copy -movflags +faststart "$OUT"
