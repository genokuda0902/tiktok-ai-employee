#!/usr/bin/env python3
"""Review-only Japanese UI chrome overlay for 9:16 slide videos.

No uploads, posting, network, or paid API. Keeps original audio bitstream via stream copy.
The overlay is generic to 10 genre titles; the scene-specific mask is for the
existing eight-slide AI-work sample only. Adapt regions per template before use.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
GENRE_LABELS = {
    'ai_work': 'AI時短ワーク', 'business': '仕事のコツ',
    'money': 'お金の知識', 'learning': '学びの習慣',
    'health': '健康の基本', 'lifestyle': '暮らしの工夫',
    'psychology': '心の仕組み', 'science': '科学の発見',
    'history': '歴史の発見', 'travel': '旅のヒント',
}
FONT_PATHS = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
# Coordinates refer to the 1080x1920 original AI-work sample. Do not blindly
# reuse these masks for other layouts; use a template-specific geometry profile.
GLOBAL_PATCHES = [
    ((62, 59, 402, 134), (3, 8, 22, 255)),
    ((477, 65, 575, 117), (3, 8, 22, 255)),
    ((789, 63, 879, 119), (4, 9, 24, 255)),
    ((68, 1780, 635, 1874), (2, 6, 19, 255)),
]
SCENE1_PATCHES = [
    ((92, 220, 350, 279), (14, 96, 108, 255)),
]
LATER_PATCHES = [
    ((89, 175, 246, 232), (3, 23, 42, 255)),
    ((88, 341, 502, 398), (3, 23, 42, 255)),
]

def font(size: int, path: str | None = None) -> ImageFont.FreeTypeFont:
    for candidate in ([path] if path else []) + FONT_PATHS:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    raise FileNotFoundError('Install a Japanese-capable Noto Sans CJK font')

def render_layers(out_dir: str | Path, genre: str = 'ai_work', font_path: str | None = None) -> list[Path]:
    if genre not in GENRE_LABELS:
        raise ValueError('Unknown genre: ' + genre)
    p = Path(out_dir); p.mkdir(parents=True, exist_ok=True)
    layers = [Image.new('RGBA', (W, H), (0, 0, 0, 0)) for _ in range(3)]
    texts = [
        [(GENRE_LABELS[genre], (80, 72), 33, '#D6F8F7'),
         ('音声', (486, 72), 27, '#DDE8F2'),
         ('手順', (795, 71), 28, '#DDE8F2'),
         ('確認用サンプル｜社員承認前・投稿禁止', (76, 1812), 26, '#91A6B7')],
        [('01 ／ 最初の一歩', (104, 228), 27, '#C9FFFF')],
        [('今日の要点', (97, 182), 27, '#48E0D5'),
         ('AI時短術 ／ 公開前確認', (95, 347), 26, '#BBCFDE')],
    ]
    for i, (layer, patches, labels) in enumerate(zip(layers, [GLOBAL_PATCHES, SCENE1_PATCHES, LATER_PATCHES], texts)):
        d = ImageDraw.Draw(layer)
        for rect, color in patches: d.rectangle(rect, fill=color)
        for label, xy, size, color in labels: d.text(xy, label, font=font(size, font_path), fill=color, stroke_width=0)
        path = p / ('global.png' if i == 0 else ('scene1.png' if i == 1 else 'scene2to8.png'))
        layer.save(path)
    return [p / name for name in ('global.png', 'scene1.png', 'scene2to8.png')]

def build_ffmpeg_cmd(src: str | Path, dest: str | Path, layers: list[Path], duration: float, scene1_end: float) -> list[str]:
    if not (0 < scene1_end < duration): raise ValueError('Invalid scene1 end')
    if len(layers) != 3: raise ValueError('Three overlay layers required')
    fc = (
        "[0:v][1:v]overlay=0:0:shortest=1:format=auto[v1];"
        f"[v1][2:v]overlay=0:0:enable='lt(t,{scene1_end:.6f})':shortest=1:format=auto[v2];"
        f"[v2][3:v]overlay=0:0:enable='gte(t,{scene1_end:.6f})':shortest=1:format=auto[v]"
    )
    args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(src)]
    for path in layers: args += ['-framerate', '30', '-loop', '1', '-i', str(path)]
    args += ['-filter_complex', fc, '-map', '[v]', '-map', '0:a:0',
             '-map_metadata', '0', '-map_chapters', '0', '-t', str(duration),
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
             '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(dest)]
    return args

def render(src: str | Path, dest: str | Path, genre: str = 'ai_work', scene1_end: float = 94 / 30,
           duration: float = 22.5, font_path: str | None = None) -> None:
    layers = render_layers(Path(dest).parent / 'overlay_layers', genre, font_path)
    subprocess.run(build_ffmpeg_cmd(src, dest, layers, duration, scene1_end), check=True)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('input_mp4'); ap.add_argument('output_mp4')
    ap.add_argument('--genre', choices=GENRE_LABELS.keys(), default='ai_work')
    ap.add_argument('--duration', type=float, default=22.5)
    ap.add_argument('--scene1-end', type=float, default=94/30)
    args = ap.parse_args()
    render(args.input_mp4, args.output_mp4, args.genre, args.scene1_end, args.duration)

if __name__ == '__main__': main()
