"""Review-only native-resolution Japanese fact-check panel for 10 genre slide videos.

No user data, proprietary media, network access, paid APIs, or publishing operations.
"""
from __future__ import annotations
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Sequence
from PIL import Image, ImageDraw, ImageFont

PANEL_W, PANEL_H = 940, 1020
VIDEO_W, VIDEO_H = 1080, 1920
PANEL_X, PANEL_Y = 70, 350
CAPTION_Y = 1450
GENRES = (
    'ai', 'beauty', 'romance', 'saving', 'sales',
    'career', 'health', 'trivia', 'travel', 'product_comparison',
)
REVIEW_STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
POLICY = {'human_approval_required': True, 'automatic_posting': False,
          'public_upload': False, 'paid_service': False, 'merge_without_approval': False}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

@dataclass(frozen=True)
class Check:
    title: str
    explanation: str

CHECKS = (
    Check('数字と根拠', '実績・出典を自分で照合'),
    Check('抜け・誤り', '重要な条件や固有名詞を確認'),
    Check('伝わる表現', '読み手に誤解がないか確認'),
)

def validate(genre: str, focus: int, checks: Sequence[Check] = CHECKS) -> None:
    if genre not in GENRES:
        raise ValueError('unapproved genre')
    if focus not in (0, 1, 2):
        raise ValueError('focus must be 0, 1 or 2')
    if len(checks) != 3:
        raise ValueError('exactly three human review steps required')
    for item in checks:
        if not item.title or not item.explanation or len(item.title) > 12 or len(item.explanation) > 24:
            raise ValueError('invalid review text length')
    if PANEL_Y + PANEL_H >= CAPTION_Y:
        raise ValueError('caption safe zone violated')
    if PANEL_X + PANEL_W > VIDEO_W:
        raise ValueError('horizontal overflow')
    if POLICY['automatic_posting'] or POLICY['paid_service'] or POLICY['public_upload']:
        raise ValueError('release gate violated')

def font(size: int, bold: bool = False):
    path = FONT_BOLD if bold else FONT
    if not Path(path).is_file() and os.environ.get("CI"):
        # CI validates geometry without distributing font files.
        # Production rendering requires Noto CJK for Japanese glyph quality.
        return ImageFont.load_default(size=size)
    return ImageFont.truetype(path, size)

def render_panel(path: Path, focus: int, genre: str = 'ai') -> Path:
    validate(genre, focus)
    im = Image.new('RGBA', (PANEL_W, PANEL_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for inset, alpha in ((1, 22), (6, 20), (12, 14)):
        d.rounded_rectangle((inset, 9+inset, PANEL_W-inset, PANEL_H-1), radius=36,
                            fill=(0, 13, 37, alpha))
    d.rounded_rectangle((5, 4, PANEL_W-6, PANEL_H-16), radius=36,
                        fill=(246, 250, 255, 255))
    d.rounded_rectangle((6, 4, PANEL_W-7, 146), radius=35, fill=(8, 41, 82, 255))
    d.rectangle((6, 100, PANEL_W-7, 146), fill=(8, 41, 82, 255))
    d.text((45, 21), 'AIの出力を確認する', font=font(56, True), fill='#FFFFFF')
    d.text((47, 101), '確認するのは人。3つの観点で見直す。', font=font(26), fill='#9BEAE7')
    d.rounded_rectangle((38, 175, PANEL_W-39, 357), radius=25, fill='#E4EDF9')
    d.rounded_rectangle((57, 193, 281, 244), radius=16, fill='#0D62AD')
    d.text((75, 196), '架空の出力例', font=font(26, True), fill='white')
    d.text((62, 253), '「問い合わせ対応を改善しました」', font=font(38, True), fill='#102C4D')
    d.text((62, 310), '→ その根拠は？ 何が変わった？', font=font(27), fill='#33627B')
    rows = ((386, 553), (567, 734), (748, 915))
    for i, ((y0,y1), check) in enumerate(zip(rows,CHECKS)):
        selected = (i == focus)
        fill = '#DDFCF5' if selected else '#FFFFFF'
        outline = '#00A996' if selected else '#C9D7E9'
        d.rounded_rectangle((39, y0, PANEL_W-40, y1), radius=24, fill=fill,
                            outline=outline, width=5 if selected else 2)
        d.rounded_rectangle((59, y0+36, 157, y0+132), radius=21,
                            fill='#00A996' if selected else '#DBE7F5')
        d.text((73, y0+49), f'{i+1:02d}', font=font(40, True),
               fill='white' if selected else '#2A648F')
        d.text((184, y0+22), check.title, font=font(46, True), fill='#102C4D')
        d.text((186, y0+93), check.explanation, font=font(29), fill='#405D75')
        if selected:
            d.ellipse((PANEL_W-90, y0+22, PANEL_W-58, y0+54), fill='#00A996')
    d.text((55, 941), '※デモ画面｜AIが自動で確認した結果ではありません',
           font=font(22), fill='#64788B')
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)
    return path

def render_all(output_dir: Path, genre: str = 'ai') -> list[Path]:
    return [render_panel(output_dir / f'focus_{i}.png', i, genre) for i in range(3)]

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('output_dir', type=Path)
    p.add_argument('--genre', choices=GENRES, default='ai')
    a = p.parse_args()
    for x in render_all(a.output_dir, a.genre):
        print(x)
