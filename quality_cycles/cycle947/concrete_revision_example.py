"""cycle947: safe illustrative revision example for 10 genre video templates.

Renders ONLY a local fictional example, not an actual ChatGPT output.
No web access, uploads, publication, paid services or external assets.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRE_ACCENTS = {
    'ai_productivity': '#10BFAE', 'career': '#448AFF',
    'finance': '#16A36D', 'education': '#795BCE',
    'health': '#169CB2', 'travel': '#EF9F34',
    'food': '#E9774F', 'beauty': '#D977B4',
    'lifestyle': '#26A39B', 'technology': '#538DE6',
}
STAGE_TIMES = ((15.55, 16.10), (16.10, 16.55), (16.55, 17.35))
CANVAS = (930, 322)
POSITION = (76, 986)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def render_overlay(stage: int, genre: str = 'ai_productivity') -> Image.Image:
    if stage not in (1, 2, 3):
        raise ValueError('stage must be 1, 2 or 3')
    if genre not in GENRE_ACCENTS:
        raise ValueError('unknown genre')
    accent = GENRE_ACCENTS[genre]
    im = Image.new('RGBA', CANVAS, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, 927, 318), radius=30,
                        fill='#F4F8F8', outline=accent, width=4)
    d.rounded_rectangle((25, 22, 422, 79), radius=14, fill='#006A62')
    d.text((45, 29), 'AFTER｜具体的な修正指示', font=font(32, True), fill='white')
    d.text((655, 40), '架空の表示例', font=font(24), fill='#667980')
    d.text((44, 98), '冒頭の見出しだけ', font=font(49, True), fill='#142D3C')
    if stage >= 2:
        d.text((44, 167), '15文字以内に短くして', font=font(47, True), fill='#142D3C')
        d.rounded_rectangle((43, 228, 880, 233), radius=2, fill=accent)
    if stage >= 3:
        d.rounded_rectangle((30, 247, 900, 304), radius=14, fill='#D5F3EB')
        d.text((49, 250), '修正後の見出し例：今週の成果',
               font=font(34, True), fill='#07534F')
    return im


def make_assets(folder: Path, genre: str = 'ai_productivity') -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for stage in (1, 2, 3):
        path = folder / f'revision_stage{stage}.png'
        render_overlay(stage, genre).save(path)
        paths.append(path)
    return paths


def ffmpeg_command(src: Path, dst: Path, assets: list[Path]) -> list[str]:
    if len(assets) != 3:
        raise ValueError('expected three overlays')
    cmd = ['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', str(src)]
    for asset in assets:
        cmd += ['-loop', '1', '-framerate', '30', '-i', str(asset)]
    graph = '[0:v]format=yuv420p[v0];'
    for idx, (start, end) in enumerate(STAGE_TIMES, 1):
        graph += (f'[v{idx-1}][{idx}:v]overlay=x={POSITION[0]}:y={POSITION[1]}:'
                  f"enable='gte(t,{start})*lt(t,{end})':format=auto[v{idx}];")
    graph = graph.rstrip(';')
    return cmd + ['-filter_complex', graph, '-map', '[v3]', '-map', '0:a:0',
                  '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                  '-pix_fmt', 'yuv420p', '-r', '30', '-frames:v', '691',
                  '-c:a', 'copy', '-movflags', '+faststart', str(dst)]


def main() -> None:
    import subprocess
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--genre', choices=GENRE_ACCENTS, default='ai_productivity')
    args = ap.parse_args()
    assets = make_assets(args.output.parent / 'overlay_assets', args.genre)
    subprocess.run(ffmpeg_command(args.input, args.output, assets), check=True)


if __name__ == '__main__':
    main()
