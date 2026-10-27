"""cycle906: collision-safe, readable, synthetic save-flow panel.

Render 87 RGBA overlays for scene 07 (17.4s--20.3s) of a private
1080x1920 / 30fps video. Never handles real accounts or posting.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1100
FPS, FRAMES, START_SEC = 30, 87, 17.4
SAFE_RECT = (52, 20, 1028, 1070)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work': ('週次報告テンプレート', '目的：週次報告を作る', '条件：数字と根拠を示す', '形式：見出しと箇条書き'),
    'business': ('提案書テンプレート', '目的：提案を整理する', '条件：前提を明記する', '形式：結論から書く'),
    'education': ('学習計画テンプレート', '目的：学習計画を作る', '条件：復習日を入れる', '形式：表でまとめる'),
    'health': ('健康メモのひな形', '目的：記録を整理する', '条件：診断はしない', '形式：日付ごとに書く'),
    'cooking': ('献立メモのひな形', '目的：献立を考える', '条件：材料を確認する', '形式：手順を番号で書く'),
    'travel': ('旅行計画テンプレート', '目的：行程を整理する', '条件：移動を確認する', '形式：時間順に書く'),
    'beauty': ('ケア記録テンプレート', '目的：手順を整理する', '条件：注意点を記載', '形式：順番に書く'),
    'finance': ('家計メモのひな形', '目的：支出を整理する', '条件：数字を確認する', '形式：項目別に書く'),
    'pets': ('ペット記録のひな形', '目的：様子を記録する', '条件：変化を確認する', '形式：日付順に書く'),
    'entertainment': ('企画メモのひな形', '目的：企画をまとめる', '条件：対象を明記する', '形式：3項目で書く'),
}
INK = '#15304C'
MUTED = '#49637E'
BLUE = '#1166B3'
TEAL = '#007F78'
WHITE = '#FFFFFF'

def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)

def fit_size(draw, text, max_width, start=58, minimum=34, bold=True):
    for size in range(start, minimum-1, -1):
        if draw.textbbox((0, 0), text, font=font(size, bold))[2] <= max_width:
            return size
    raise ValueError(f'text cannot fit safely: {text!r}')

def draw_text(draw, xy, text, max_width, start=56, min_size=34, fill=INK, bold=True, audit=None):
    size = fit_size(draw, text, max_width, start, min_size, bold)
    bbox = draw.textbbox(xy, text, font=font(size, bold))
    assert bbox[2] <= xy[0] + max_width, (text, bbox)
    assert 0 <= bbox[1] and bbox[3] < HEIGHT - 20, (text, bbox)
    draw.text(xy, text, fill=fill, font=font(size, bold))
    if audit is not None:
        audit.append({'text': text, 'font_px': size, 'bbox': bbox})
    return bbox

def rounded(draw, rect, fill, radius=25, outline=None, width=3):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)

def draw_stage(stage: int, genre: str, audit=None):
    if genre not in GENRES or stage not in (0, 1, 2):
        raise ValueError('invalid genre or stage')
    name, *lines = GENRES[genre]
    im = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rounded(d, SAFE_RECT, '#F4F8FE', 36, '#D5E5F6', 4)
    rounded(d, (94, 56, 292, 126), BLUE, 20)
    draw_text(d, (121, 63), f'STEP {stage+1}/3', 155, 39, 34, WHITE, audit=audit)
    titles = ['名前をつける', '指示を整理する', '保存前に確認']
    draw_text(d, (102, 164), titles[stage], 850, 66, 48, audit=audit)
    d.line((102, 265, 974, 265), fill='#CFDDEB', width=4)
    if stage == 0:
        rounded(d, (102, 310, 978, 596), WHITE, 24, '#C8D7E9', 3)
        draw_text(d, (138, 343), 'テンプレート名', 790, 39, 36, MUTED, audit=audit)
        rounded(d, (132, 416, 946, 532), '#EAF6FF', 18, '#2C87D1', 5)
        draw_text(d, (157, 433), name, 750, 55, 37, audit=audit)
        draw_text(d, (118, 677), 'あとで探せる名前にする', 840, 44, 37, TEAL, audit=audit)
    elif stage == 1:
        for i, line in enumerate(lines):
            y = 308 + i * 148
            rounded(d, (102, y, 978, y+121), WHITE, 20, '#C9DBEA', 3)
            rounded(d, (125, y+22, 190, y+93), '#D9F6F0', 17)
            draw_text(d, (146, y+31), str(i+1), 34, 40, 36, TEAL, audit=audit)
            draw_text(d, (216, y+28), line, 725, 48, 34, audit=audit)
        draw_text(d, (118, 787), '目的・条件・形式を明確に', 840, 40, 34, TEAL, audit=audit)
    else:
        checks = ['名前が分かりやすい', '指示が具体的', '内容を自分で確認']
        for i, check in enumerate(checks):
            y = 308 + i * 148
            rounded(d, (102, y, 978, y+121), WHITE, 20, '#C9DBEA', 3)
            rounded(d, (129, y+27, 193, y+93), '#D9F6F0', 18)
            draw_text(d, (148, y+34), '✓', 36, 42, 36, TEAL, audit=audit)
            draw_text(d, (220, y+30), check, 718, 49, 35, audit=audit)
        draw_text(d, (118, 787), '確認後に手動で保存', 840, 40, 34, TEAL, audit=audit)
    for i, label in enumerate(('名前', '指示', '確認')):
        x = 102 + i * 292
        selected = i == stage
        rounded(d, (x, 888, x+268, 965), BLUE if selected else '#E5EFF9', 18)
        draw_text(d, (x+42, 903), f'{i+1}  {label}', 200, 36, 30, WHITE if selected else MUTED, audit=audit)
    draw_text(d, (102, 1003), '架空の画面例・実際の保存操作なし', 850, 29, 27, MUTED, False, audit=audit)
    return im

def render_frame(frame: int, genre: str, stages=None):
    if not 0 <= frame < FRAMES:
        raise ValueError('frame out of range')
    stages = stages if stages is not None else [draw_stage(s, genre) for s in range(3)]
    s = min(frame // 29, 2)
    out = stages[s].copy()
    if s and frame % 29 < 7:
        out = Image.blend(stages[s-1], stages[s], (frame % 29 + 1) / 7)
    edge = min(1.0, (frame+1)/6, (FRAMES-frame)/6)
    if edge < 1.0:
        out.putalpha(out.getchannel('A').point(lambda a: round(a * edge)))
    return out

def render_sequence(output: Path, genre: str):
    output.mkdir(parents=True, exist_ok=True)
    stages = [draw_stage(s, genre) for s in range(3)]
    for i in range(FRAMES):
        render_frame(i, genre, stages).save(output / f'frame_{i:03d}.png', optimize=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--genre', choices=GENRES, default='ai_work')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    render_sequence(args.output, args.genre)
