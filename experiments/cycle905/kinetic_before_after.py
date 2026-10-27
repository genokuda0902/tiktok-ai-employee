"""Offline, genre-neutral kinetic before/after instruction scene.

Renders *only* a replaceable upper scene overlay. It never modifies narration,
subtitle band, privacy controls, or publication status. Source media remains local.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1080
OVERLAY_H = 920
OVERLAY_Y = 300
FPS = 30
FRAME_COUNT = 87
SCENE_START = 14.5
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work': 'AI・仕事効率化',
    'business': 'ビジネス',
    'education': '学習',
    'health': '健康',
    'cooking': '料理',
    'travel': '旅行',
    'beauty': '美容',
    'finance': 'お金',
    'pets': 'ペット',
    'entertainment': '娯楽',
}
# No claims, fabricated results, source screenshots, or personal identifiers.
SCENE_TEXT = {
    'ai_work': ('もっと良くして', '数字を先頭にして', '3行でまとめて'),
    'business': ('分かりやすくして', '結論を先頭にして', '理由を2点に絞って'),
    'education': ('簡単にして', '例を先に見せて', '要点を3つに絞って'),
    'health': ('詳しく教えて', '一般情報と明記して', '注意点を先に示して'),
    'cooking': ('もっとおいしく', '手順を番号で示して', '時間の目安を添えて'),
    'travel': ('旅程を良くして', '移動順を先に示して', '乗換えを明記して'),
    'beauty': ('きれいにして', '手順を分けて示して', '注意点を添えて'),
    'finance': ('分かりやすく', '前提条件を先に示して', '出典を明記して'),
    'pets': ('詳しく教えて', '安全上の注意を先に', '確認項目を示して'),
    'entertainment': ('面白くして', '冒頭を短くして', '結末を簡潔にして'),
}

def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)

def txt(d, xy, s, size=48, color='#112a44', bold=False):
    d.text(xy, s, fill=color, font=font(size, bold))

def card(d, xy, radius=28, fill='#ffffff', outline=None, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def static_stage(stage: int, genre: str) -> Image.Image:
    if genre not in GENRES: raise ValueError('unknown genre')
    if stage not in (0, 1, 2): raise ValueError('unknown stage')
    ng, first, second = SCENE_TEXT[genre]
    im = Image.new('RGBA', (CANVAS_W, OVERLAY_H), (0,0,0,0))
    d = ImageDraw.Draw(im)
    card(d, (58, 6, 1022, 878), radius=38, fill='#f4f8ff')
    txt(d, (96, 42), '修正を「具体的に・1つずつ」', 47, bold=True)
    d.line((96, 122, 984, 122), fill='#d5e2f2', width=4)
    if stage == 0:
        card(d, (92, 170, 988, 670), fill='#ffebeb')
        card(d, (130, 212, 285, 285), radius=18, fill='#e9465a')
        txt(d, (164, 219), 'NG', 42, '#ffffff', True)
        txt(d, (132, 335), ng, 72, '#202d42', True)
        card(d, (130, 540, 950, 625), radius=18, fill='#fff9f9')
        txt(d, (158, 556), '何を変えるか分からない', 43, '#b33349', True)
        txt(d, (130, 744), '01 / 曖昧な依頼', 39, '#60768c', True)
    elif stage == 1:
        card(d, (92, 170, 988, 670), fill='#dcf7ed')
        card(d, (130, 212, 285, 285), radius=18, fill='#149d76')
        txt(d, (165, 219), 'OK', 42, '#ffffff', True)
        txt(d, (130, 340), first, 59, '#143e37', True)
        txt(d, (130, 440), second, 59, '#143e37', True)
        d.rounded_rectangle((120, 324, 957, 529), radius=20, outline='#28c4a4', width=7)
        txt(d, (130, 744), '02 / 変更点を明確に', 39, '#60768c', True)
    else:
        card(d, (92, 158, 988, 340), fill='#dff6fa')
        txt(d, (130, 185), '1回目', 38, '#008e9d', True)
        txt(d, (130, 242), first, 54, '#142b45', True)
        card(d, (92, 380, 988, 558), fill='#dff6fa')
        txt(d, (130, 401), '確認してから 2回目', 36, '#008e9d', True)
        txt(d, (130, 463), second, 54, '#142b45', True)
        card(d, (120, 616, 960, 720), radius=24, fill='#143d5a')
        txt(d, (174, 636), '一度に全部を直そうとしない', 43, '#ffffff', True)
        txt(d, (130, 774), '03 / 1つずつ確認', 39, '#60768c', True)
    return im

def phase(frame: int) -> int:
    if not 0 <= frame < FRAME_COUNT: raise ValueError('frame out of range')
    return min(frame // 29, 2)

def opacity(frame: int, stage: int) -> float:
    """Crossfade 6 frames at boundaries, fade to underlying video at edges."""
    start, end = stage*29, (stage+1)*29
    if stage == 0: enter = min(1.0, (frame+1)/6)
    else: enter = min(1.0, max(0.0, (frame-start+1)/6))
    if stage == 2: leave = min(1.0, max(0.0, (FRAME_COUNT-frame)/6))
    else: leave = min(1.0, max(0.0, (end-frame)/6))
    return max(0.0, min(enter, leave))

def render_frame(frame: int, genre: str, stages=None) -> Image.Image:
    stages = stages or [static_stage(i, genre) for i in range(3)]
    s = phase(frame)
    # Keep source visible at transition: blend old and new overlay alpha.
    if s > 0 and frame % 29 < 6:
        f = (frame % 29 + 1)/6
        im = Image.blend(stages[s-1], stages[s], f)
    else:
        im = stages[s].copy()
    # Gentle vertical reveal (max 10 px) without touching subtitle band.
    nudge = round(10 * (1 - min(1, frame % 29 / 10)))
    if nudge:
        moved = Image.new('RGBA', im.size, (0,0,0,0))
        moved.alpha_composite(im, (0, -nudge))
        im = moved
    edge = min(1.0, (frame+1)/5, (FRAME_COUNT-frame)/5)
    if edge < 1.0:
        a = im.getchannel('A').point(lambda x: round(x*edge))
        im.putalpha(a)
    return im

def render_sequence(output: Path, genre: str):
    if genre not in GENRES: raise ValueError('unknown genre')
    output.mkdir(parents=True, exist_ok=True)
    stages = [static_stage(i, genre) for i in range(3)]
    for i in range(FRAME_COUNT):
        render_frame(i, genre, stages).save(output / f'frame_{i:03d}.png', optimize=True)

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--genre', choices=list(GENRES), default='ai_work')
    p.add_argument('--output', type=Path, required=True)
    a=p.parse_args()
    render_sequence(a.output, a.genre)
